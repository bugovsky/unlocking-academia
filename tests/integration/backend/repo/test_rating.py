import asyncio
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import select, delete

from backend.db.models import Post, Comment, Rating, Request, User
from backend.db.utils import create_session
from backend.repository.rating import RatingRepo
from backend.schema.base import Domain
from backend.schema.user import Role
from tests.factory.schema import RatingCreateFactory, RatingUpdateFactory

@pytest.fixture
def rating_repo():
    return RatingRepo()

@pytest.fixture
def post_id():
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


class TestRatingRepo:
    async def test_get_rating_by_user(self, create_user, create_post, create_rating, rating_repo, post_id):
        user_id = uuid4()
        await asyncio.gather(
            create_user(
                id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT
            ),
            create_post(id=post_id, content="Test post", domain=[Domain.CS]),
        )
        await create_rating(grade=8, user_id=user_id, post_id=post_id)

        result = await rating_repo.get_rating_by_user(post_id, user_id)

        assert isinstance(result, Rating)
        assert result.grade == 8
        assert result.user_id == user_id
        assert result.post_id == post_id

    async def test_get_post_rating(self, create_user, create_post, create_rating, rating_repo, post_id):
        user1_id = uuid4()
        user2_id = uuid4()
        await asyncio.gather(
            create_post(id=post_id, content="Test post", domain=[Domain.CS]),
            create_user(
                id=user1_id, firstname="Test1", lastname="User1", password="hash", role=Role.STUDENT
            ),
            create_user(
                id=user2_id, firstname="Test2", lastname="User2", password="hash", role=Role.STUDENT
            )
        )
        await asyncio.gather(
            create_rating(
                grade=8, user_id=user1_id, post_id=post_id
            ),
            create_rating(
                grade=10, user_id=user2_id, post_id=post_id
            )
        )

        result = await rating_repo.get_post_rating(post_id)

        assert isinstance(result, Decimal)
        assert result == Decimal("9.0")

    async def test_rate(self, create_user, create_post, rating_repo, post_id, session_maker):
        user_id = uuid4()
        await asyncio.gather(
            create_user(
                id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT
            ),
            create_post(id=post_id, content="Test post", domain=[Domain.CS])
        )
        rating_data = RatingCreateFactory.build(grade=7)

        result = await rating_repo.rate(post_id, user_id, rating_data)

        assert isinstance(result, Rating)
        assert result.grade == 7
        assert result.user_id == user_id
        assert result.post_id == post_id

        async with create_session(session_maker) as db_session:
            query = select(Rating).where(Rating.id == result.id)
            db_rating = (await db_session.execute(query)).scalar_one()
            assert db_rating.grade == 7

    async def test_update_rating(self, create_user, create_post, create_rating, rating_repo, post_id, session_maker):
        user_id = uuid4()
        await asyncio.gather(
            create_user(
                id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT
            ),
            create_post(id=post_id, content="Test post", domain=[Domain.CS])
        )
        await create_rating(grade=8, user_id=user_id, post_id=post_id)
        rating_data = RatingUpdateFactory.build(grade=9)

        result = await rating_repo.update_rating(post_id, user_id, rating_data)

        assert isinstance(result, Rating)
        assert result.grade == 9

        async with create_session(session_maker) as db_session:
            query = select(Rating).where(Rating.id == result.id)
            db_rating = (await db_session.execute(query)).scalar_one()
        assert db_rating.grade == 9