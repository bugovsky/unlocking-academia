import uuid
import pytest
from fastapi import status

from backend.schema.comment import Comment
from backend.schema.user import Role
from tests.factory.schema import CommentFactory, CommentCreateFactory, UserFactory


@pytest.fixture(scope="class")
def post_id():
    return uuid.uuid4()


class TestComment:
    def test_create_comment_success(self, backend_client, mocked_comment_service, post_id):
        user = UserFactory.build(role=Role.STUDENT)
        comment_data = CommentCreateFactory.build()
        expected_comment = CommentFactory.build(post_id=post_id, author_id=user.id)
        mocked_comment_service.create_comment.return_value = expected_comment

        response = backend_client.post(
            f"/comment/{post_id}",
            params={"user_id": str(user.id), "role": user.role},
            json=comment_data.model_dump()
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.model_validate(response.json()) == expected_comment
        mocked_comment_service.create_comment.assert_called_once_with(
            post_id=post_id, user_id=user.id, comment_data=comment_data
        )

    def test_create_comment_unauthorized(self, backend_client, mocked_comment_service, post_id):
        comment_data = CommentCreateFactory.build()

        response = backend_client.post(
            f"/comment/{post_id}",
            json=comment_data.model_dump()
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Could not validate credentials"

    def test_create_comment_unknown_user(self, backend_client, mocked_comment_service, post_id, unknown_user_id):
        comment_data = CommentCreateFactory.build()

        response = backend_client.post(
            f"/comment/{post_id}",
            params={"user_id": str(unknown_user_id), "role": Role.STUDENT},
            json=comment_data.model_dump()
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    def test_get_post_comments_success(self, backend_client, mocked_comment_service, post_id):
        expected_comments = CommentFactory.batch(size=2, post_id=post_id)
        mocked_comment_service.get_post_comments.return_value = expected_comments

        response = backend_client.get(f"/comment/{post_id}")

        assert response.status_code == status.HTTP_200_OK
        assert [Comment.model_validate(item) for item in response.json()] == expected_comments
        mocked_comment_service.get_post_comments.assert_called_once_with(post_id)