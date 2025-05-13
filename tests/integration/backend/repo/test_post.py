import asyncio
from uuid import uuid4

import pytest
from sqlalchemy import select

from sqlalchemy import delete

from backend.db.models import Post, Comment, Rating, Request, User
from backend.db.utils import create_session
from backend.repository.post import PostRepo
from backend.schema.base import Domain
from tests.factory.schema import PostCreateFactory, PostUpdateFactory

@pytest.fixture
def post_repo():
    return PostRepo()

@pytest.fixture(autouse=True)
async def clear_db(session_maker, engine):
    yield

    async with create_session(session_maker) as db_session:
        tables = [Request, Comment, Rating, Post, User]

        for table in tables:
            query = delete(table)
            await db_session.execute(query)

        await db_session.commit()


class TestPostRepo:
    async def test_get_posts(self, create_post, post_repo):
        posts = [
            create_post(content="Post 1", domain=[Domain.CS]),
            create_post(content="Post 2", domain=[Domain.DB])
        ]
        await asyncio.gather(*posts)

        result = await post_repo.get_posts()

        assert len(result) == 2
        assert all(isinstance(post, Post) for post in result)

    async def test_get_post_by_id(self, create_post, post_repo):
        post_id = uuid4()
        await create_post(id=post_id, content="Test post", domain=[Domain.CS])

        result = await post_repo.get_post_by_id(post_id)

        assert isinstance(result, Post)
        assert result.id == post_id
        assert result.content == "Test post"

    async def test_create_post(self, create_post, post_repo, session_maker):
        post_data = PostCreateFactory.build()

        result = await post_repo.create_post(post_data)

        assert isinstance(result, Post)
        assert result.content == post_data.content
        assert result.domain == post_data.domain

        async with create_session(session_maker) as db_session:
            query = select(Post).where(Post.id == result.id)
            db_post = (await db_session.execute(query)).scalar_one()
        assert db_post.content == post_data.content

    async def test_update_post(self, create_post, post_repo, session_maker):
        post_id = uuid4()
        await create_post(id=post_id, content="Old content", domain=[Domain.CS], views=0)
        post_data = PostUpdateFactory.build(content="New content", domain=[Domain.DB], views=10)

        result = await post_repo.update_post(post_id, post_data)

        assert isinstance(result, Post)
        assert result.content == "Old content"
        assert result.domain == [Domain.CS]
        assert result.views == post_data.views

        async with create_session(session_maker) as db_session:
            query = select(Post).where(Post.id == post_id)
            db_post = (await db_session.execute(query)).scalar_one()
        assert db_post.views == post_data.views