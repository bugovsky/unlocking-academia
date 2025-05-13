import uuid
from fastapi import HTTPException, status

import pytest

from backend.schema.comment import Comment
from backend.service.comment import CommentService
from tests.factory.models import CommentFactory, PostFactory
from tests.factory.schema import CommentCreateFactory


@pytest.fixture
def comment_service(mocked_comment_repo, mocked_post_repo):
    return CommentService(comment_repo=mocked_comment_repo, post_repo=mocked_post_repo)


class TestCommentService:
    async def test_get_post_comments_success(self, comment_service, mocked_comment_repo, mocked_post_repo):
        post = PostFactory.build()
        post_id = post.id
        comments = CommentFactory.batch(size=2, post_id=post_id)
        mocked_post_repo.get_post_by_id.return_value = post
        mocked_comment_repo.get_post_comments.return_value = comments

        result = await comment_service.get_post_comments(post_id)

        assert len(result) == 2
        assert all(isinstance(comment, Comment) for comment in result)
        mocked_post_repo.get_post_by_id.assert_called_once_with(post_id)
        mocked_comment_repo.get_post_comments.assert_called_once_with(post_id)

    async def test_get_post_comments_post_not_found(self, comment_service, mocked_comment_repo, mocked_post_repo):
        post = PostFactory.build()
        post_id = post.id
        mocked_post_repo.get_post_by_id.return_value = None

        with pytest.raises(HTTPException) as err:
            await comment_service.get_post_comments(post_id)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_post_repo.get_post_by_id.assert_called_once_with(post_id)

    async def test_create_comment_success(self, comment_service, mocked_comment_repo, mocked_post_repo):
        post = PostFactory.build()
        post_id = post.id
        user_id = uuid.uuid4()
        comment_data = CommentCreateFactory.build()
        comment = CommentFactory.build(post_id=post_id, author_id=user_id)
        mocked_post_repo.get_post_by_id.return_value = post
        mocked_comment_repo.create_comment.return_value = comment

        result = await comment_service.create_comment(post_id, user_id, comment_data)

        assert isinstance(result, Comment)
        assert result.post_id == post_id
        mocked_post_repo.get_post_by_id.assert_called_once_with(post_id)
        mocked_comment_repo.create_comment.assert_called_once_with(post_id, user_id, comment_data)