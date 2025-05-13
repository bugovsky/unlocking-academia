import uuid
from fastapi import HTTPException, status

import pytest

from backend.schema.post import Post
from backend.service.post import PostService
from tests.factory.models import PostFactory
from tests.factory.schema import PostCreateFactory, PostUpdateFactory


@pytest.fixture
def post_service(mocked_post_repo):
    return PostService(post_repo=mocked_post_repo)

@pytest.fixture
def post_id():
    return uuid.uuid4()


class TestPostService:
    async def test_get_posts_success(self, post_service, mocked_post_repo):
        posts = PostFactory.batch(size=3)
        mocked_post_repo.get_posts.return_value = posts

        result = await post_service.get_posts()

        assert len(result) == 3
        assert all(isinstance(post, Post) for post in result)
        mocked_post_repo.get_posts.assert_called_once_with()

    async def test_get_post_by_id_success(self, post_service, mocked_post_repo, post_id):
        post = PostFactory.build(id=post_id)
        mocked_post_repo.get_post_by_id.return_value = post

        result = await post_service.get_post_by_id(post_id)

        assert isinstance(result, Post)
        assert result.id == post_id
        mocked_post_repo.get_post_by_id.assert_called_once_with(post_id)

    async def test_get_post_by_id_not_found(self, post_service, mocked_post_repo, post_id):
        mocked_post_repo.get_post_by_id.return_value = None

        with pytest.raises(HTTPException) as err:
            await post_service.get_post_by_id(post_id)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_post_repo.get_post_by_id.assert_called_once_with(post_id)

    async def test_create_post_success(self, post_service, mocked_post_repo):
        post_data = PostCreateFactory.build()
        post = PostFactory.build()
        mocked_post_repo.create_post.return_value = post

        result = await post_service.create_post(post_data)

        assert isinstance(result, Post)
        mocked_post_repo.create_post.assert_called_once_with(post_data)

    async def test_update_post_success(self, post_service, mocked_post_repo, post_id):
        post_data = PostUpdateFactory.build()
        post = PostFactory.build(id=post_id)
        mocked_post_repo.update_post.return_value = post

        result = await post_service.update_post(post_id, post_data)

        assert isinstance(result, Post)
        assert result.id == post_id
        mocked_post_repo.update_post.assert_called_once_with(post_id, post_data)

    async def test_update_post_not_found(self, post_service, mocked_post_repo, post_id):
        post_data = PostUpdateFactory.build()
        mocked_post_repo.update_post.return_value = None

        with pytest.raises(HTTPException) as err:
            await post_service.update_post(post_id, post_data)

        assert err.value.status_code == status.HTTP_404_NOT_FOUND
        mocked_post_repo.update_post.assert_called_once_with(post_id, post_data)