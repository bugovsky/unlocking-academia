from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from backend.db.base import Session


@asynccontextmanager
async def create_session(
    session_maker: async_sessionmaker[AsyncSession] | None = None,
):
    if session_maker is None:
        session_maker = Session

    async with session_maker.begin() as session:
        yield session