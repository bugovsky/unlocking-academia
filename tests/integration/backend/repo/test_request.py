from uuid import uuid4

import pytest

from sqlalchemy import select, delete

from backend.db.models import Post, Comment, Rating, Request, User
from backend.db.utils import create_session
from backend.repository.request import RequestRepo
from backend.schema.user import Role
from tests.factory.schema import RequestCreateFactory, RequestCloseFactory

@pytest.fixture()
def request_repo():
    return RequestRepo()

@pytest.fixture(autouse=True)
async def clear_db(session_maker, engine):
    yield

    async with create_session(session_maker) as db_session:
        tables = [Request, Comment, Rating, Post, User]

        for table in tables:
            query = delete(table)
            await db_session.execute(query)

        await db_session.commit()

class TestRequestRepo:
    async def test_get_request_by_id(self, create_request, create_user, request_repo):
        request_id = uuid4()
        user_id = uuid4()
        await create_user(id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT)
        await create_request(id=request_id, question="Test question", type="question", author_id=user_id, recipient_id=user_id)

        result = await request_repo.get_request_by_id(request_id)

        assert isinstance(result, Request)
        assert result.id == request_id
        assert result.question == "Test question"

    async def test_get_user_requests(self, create_request, create_user, request_repo):
        user_id = uuid4()
        await create_user(id=user_id, firstname="Test", lastname="User", password="hash", role=Role.STUDENT)
        await create_request(question="Request 1", type="question", author_id=user_id, recipient_id=user_id),
        await create_request(question="Request 2", type="consultation", author_id=user_id, recipient_id=user_id)

        result = await request_repo.get_user_requests(user_id)

        assert len(result) == 2
        assert all(isinstance(request, Request) for request in result)

    async def test_create_request(self, create_user, request_repo, session_maker):
        user_id = uuid4()
        recipient_id = uuid4()
        await create_user(id=user_id, firstname="Test", lastname="User", email="test@hse.ru", password="hash", role=Role.STUDENT)
        await create_user(id=recipient_id, firstname="Test2", lastname="User2", email="test2@hse.ru", password="hash", role=Role.EXPERT)
        request_data = RequestCreateFactory.build(recipient_id=recipient_id)

        result = await request_repo.create_request(user_id, request_data)

        assert isinstance(result, Request)
        assert result.question == request_data.question
        assert result.author_id == user_id
        assert result.recipient_id == recipient_id

        async with create_session(session_maker) as db_session:
            query = select(Request).where(Request.id == result.id)
            db_request = (await db_session.execute(query)).scalar_one()
            assert db_request.question == request_data.question

    async def test_close_request(self, create_request, create_user, request_repo, session_maker):
        request_id = uuid4()
        user_id = uuid4()
        await create_user(id=user_id, firstname="Test", lastname="User", email="test@hse.ru", password="hash", role="student")
        await create_request(id=request_id, question="Test question", type="question", author_id=user_id, recipient_id=user_id)
        request_data = RequestCloseFactory.build()

        result = await request_repo.close_request(request_id, request_data)

        assert isinstance(result, Request)
        assert result.response == request_data.response

        async with create_session(session_maker) as db_session:
            query = select(Request).where(Request.id == request_id)
            db_request = (await db_session.execute(query)).scalar_one()
            assert db_request.response == request_data.response