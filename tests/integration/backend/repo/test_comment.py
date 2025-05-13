import asyncio
from uuid import uuid4

import pytest
from sqlalchemy import select, delete

from backend.db.models import Post, Comment, Rating, Request, User
from backend.db.utils import create_session
from backend.repository.comment import CommentRepo
from backend.schema.base import Domain
from backend.schema.user import Role
from tests.factory.schema import CommentCreateFactory

@pytest.fixture
def comment_repo():
    return CommentRepo()

@pytest.fixture
def post_id():
    return uuid4()


@pytest.fixture
def author_id():
    return uuid4()

@pytest.fixture(autouse=True)
async def clear_db(session_maker, engine):
    yield

    async with create_session(session_maker) as db_session:
        tables = [Request, Comment, Rating, Post, User]

        for table in tables:
            query = delete(table)
            await db_session.execute(query)

        await db_session.commit()

class TestCommentRepo:
    async def test_get_post_comments(self, create_post, create_comment, create_user, comment_repo, post_id, author_id):
        await create_user(id=author_id)
        post = create_post(id=post_id, content="Test post", domain=[Domain.CS])
        comments = [
            create_comment(content="Comment 1", post_id=post_id, author_id=author_id),
            create_comment(content="Comment 2", post_id=post_id, author_id=author_id)
        ]
        data = [post, *comments]
        await asyncio.gather(*data)


        result = await comment_repo.get_post_comments(post_id)

        assert len(result) == 2
        assert all(isinstance(comment, Comment) for comment in result)

    async def test_create_comment(self, session_maker, create_post, create_user, comment_repo, post_id, author_id):
        await create_post(id=post_id, content="Test post", domain=[Domain.CS])
        await create_user(
            id=author_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT
        )
        comment_data = CommentCreateFactory.build()

        result = await comment_repo.create_comment(post_id, author_id, comment_data)

        assert isinstance(result, Comment)
        assert result.content == comment_data.content
        assert result.post_id == post_id
        assert result.author_id == author_id

        async with create_session(session_maker) as db_session:
            query = select(Comment).where(Comment.id == result.id)
            db_comment = (await db_session.execute(query)).scalar_one()
            assert db_comment.content == comment_data.content