from uuid import uuid4

import pytest
from sqlalchemy import select, delete

from backend.db.models import Post, Comment, Rating, Request, User
from backend.db.utils import create_session
from backend.repository.user import UserRepo
from backend.schema.user import Role
from tests.factory.schema import UserCreateFactory, UserUpdateFactory


@pytest.fixture()
def user_repo():
    return UserRepo()

@pytest.fixture(autouse=True)
async def clear_db(session_maker, engine):
    yield

    async with create_session(session_maker) as db_session:
        tables = [Request, Comment, Rating, Post, User]

        for table in tables:
            query = delete(table)
            await db_session.execute(query)

        await db_session.commit()

class TestUserRepo:
    async def test_get_user_by_email(self, create_user, user_repo):
        email = "test@hse.ru"
        await create_user(firstname="Test", lastname="User", email=email, password="hash", role=Role.STUDENT)
        user_repo = UserRepo()

        result = await user_repo.get_user_by_email(email)

        assert isinstance(result, User)
        assert result.email == email

    async def test_get_user_by_id(self, create_user, user_repo):
        user_id = uuid4()
        await create_user(id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT)

        result = await user_repo.get_user_by_id(user_id)

        assert isinstance(result, User)
        assert result.id == user_id

    async def test_get_not_students(self, create_user, user_repo):
        await create_user(firstname="Test1", lastname="User1", email="test1@hse.ru", password="hash", role=Role.EXPERT),
        await create_user(firstname="Test2", lastname="User2", email="test2@hse.ru", password="hash", role=Role.ADMIN)
        await create_user(firstname="Test3", lastname="User3", email="test3@hse.ru", password="hash", role=Role.STUDENT)

        result = await user_repo.get_not_students()

        assert len(result) == 2
        assert all(isinstance(user, User) for user in result)
        assert {user.email for user in result} == {"test1@hse.ru", "test2@hse.ru"}

    async def test_create_user(self, user_repo, session_maker):
        user_data = UserCreateFactory.build(firstname="test", lastname="test")

        result = await user_repo.create_user(user_data)

        assert isinstance(result, User)
        assert result.email == user_data.email

        async with create_session(session_maker) as db_session:
            query = select(User).where(User.id == result.id)
            db_user = (await db_session.execute(query)).scalar_one()
            assert db_user.email == user_data.email

    async def test_update_user(self, create_user, user_repo, session_maker):
        user_id = uuid4()
        await create_user(id=user_id, firstname="Old", lastname="User", password="hash", role=Role.STUDENT)
        user_data = UserUpdateFactory.build(firstname="New", lastname="User")

        result = await user_repo.update_user(user_id, user_data)

        assert isinstance(result, User)
        assert result.firstname == "New"

        async with create_session(session_maker) as db_session:
            query = select(User).where(User.id == user_id)
            db_user = (await db_session.execute(query)).scalar_one()
            assert db_user.firstname == "New"