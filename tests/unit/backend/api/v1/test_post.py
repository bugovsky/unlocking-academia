import uuid

import pytest
from fastapi import status

from backend.schema.post import Post
from backend.schema.user import Role
from tests.factory.schema import PostFactory, PostCreateFactory, PostUpdateFactory, UserFactory


@pytest.fixture(scope="class")
def post_id():
    return uuid.uuid4()


class TestPost:
    def test_get_posts(self, backend_client, mocked_post_service):
        expected = PostFactory.batch(size=3)
        mocked_post_service.get_posts.return_value = expected
        response = backend_client.get(url="/post")

        assert response.status_code == status.HTTP_200_OK
        assert [Post.model_validate(item) for item in response.json()] == expected
        mocked_post_service.get_posts.assert_called_once_with()

    def test_create_post_success(self, backend_client, mocked_post_service, mocked_user_service):
        user = UserFactory.build(role=Role.ADMIN)
        post_data = PostCreateFactory.build()
        expected_post = PostFactory.build()
        mocked_user_service.get_user_by_id.return_value = user
        mocked_post_service.create_post.return_value = expected_post

        response = backend_client.post(
            "/post",
            params={"user_id": user.id, "role": user.role},
            json=post_data.model_dump()
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Post.model_validate(response.json()) == expected_post
        mocked_post_service.create_post.assert_called_once_with(post_data=post_data)

    @pytest.mark.parametrize(
        "role", [pytest.param(Role.STUDENT, id="by_student"), pytest.param(Role.EXPERT, id="by_expert")]
    )
    def test_create_post_forbidden(self, backend_client, mocked_user_service, role):
        user = UserFactory.build(role=role)
        post_data = PostCreateFactory.build()
        mocked_user_service.get_user_by_id.return_value = user

        response = backend_client.post(
            "/post",
            params={"user_id": user.id, "role": user.role},
            json=post_data.model_dump()
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "You do not have permission to access this resource."

    def test_get_post_by_id_success(self, backend_client, mocked_post_service, post_id):
        expected_post = PostFactory.build(id=post_id)
        mocked_post_service.get_post_by_id.return_value = expected_post

        response = backend_client.get(f"/post/{post_id}")

        assert response.status_code == status.HTTP_200_OK
        assert Post.model_validate(response.json()) == expected_post
        mocked_post_service.get_post_by_id.assert_called_once_with(post_id)

    def test_update_post_success(self, backend_client, mocked_post_service, mocked_user_service, post_id):
        user = UserFactory.build(role=Role.ADMIN)
        post_update = PostUpdateFactory.build()
        expected_post = PostFactory.build(id=post_id)
        mocked_user_service.get_user_by_id.return_value = user
        mocked_post_service.update_post.return_value = expected_post

        response = backend_client.patch(
            f"/post/{post_id}",
            params={"user_id": user.id, "role": user.role},
            json=post_update.model_dump()
        )

        assert response.status_code == status.HTTP_200_OK
        assert Post.model_validate(response.json()) == expected_post
        mocked_post_service.update_post.assert_called_once_with(post_id, post_update)

    @pytest.mark.parametrize(
        "role", [pytest.param(Role.STUDENT, id="by_student"), pytest.param(Role.EXPERT, id="by_expert")]
    )
    def test_update_post_forbidden(self, backend_client, mocked_user_service, post_id, role):
        user = UserFactory.build(role=role)
        post_update = PostUpdateFactory.build()
        mocked_user_service.get_user_by_id.return_value = user

        response = backend_client.patch(
            f"/post/{post_id}",
            params={"user_id": user.id, "role": user.role},
            json=post_update.model_dump()
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "You do not have permission to access this resource."