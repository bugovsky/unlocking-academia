import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from backend.db.base import Base
from backend.db.utils import create_session
from tests.factory.models import UserFactory, PostFactory, CommentFactory, RatingFactory, RequestFactory


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer(
        "postgres:17.4-alpine3.21", driver="psycopg_async", port=5432
    ).with_bind_ports(5432, 50365)
    with postgres:
        yield postgres

@pytest.fixture(scope="session")
def engine(postgres_container):
    return create_async_engine(postgres_container.get_connection_url(), echo=False)

@pytest.fixture(scope="session")
async def db_engine(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="session")
def session_maker(db_engine):
    return async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def create_user(session_maker):
    async def _create_user(**kwargs):
        async with create_session(session_maker) as db_session:
            user = UserFactory.build(**kwargs)
            db_session.add(user)
            await db_session.flush()
            return user
    return _create_user


@pytest.fixture
async def create_post(session_maker):
    async def _create_post(**kwargs):
        async with create_session(session_maker) as db_session:
            post = PostFactory.build(**kwargs)
            db_session.add(post)
            await db_session.flush()
            return post
    return _create_post


@pytest.fixture
async def create_comment(session_maker):
    async def _create_comment(**kwargs):
        async with create_session(session_maker) as db_session:
            comment = CommentFactory.build(**kwargs)
            db_session.add(comment)
            await db_session.flush()
            return comment
    return _create_comment


@pytest.fixture
async def create_rating(session_maker):
    async def _create_rating(**kwargs):
        async with create_session(session_maker) as db_session:
            rating = RatingFactory.build(**kwargs)
            db_session.add(rating)
            await db_session.flush()
            return rating
    return _create_rating


@pytest.fixture
async def create_request(session_maker):
    async def _create_request(**kwargs):
        async with create_session(session_maker) as db_session:
            request = RequestFactory.build(**kwargs)
            db_session.add(request)
            await db_session.flush()
            return request
    return _create_request