from contextlib import asynccontextmanager

from backend.db.base import Session


@asynccontextmanager
async def create_session():
    async with Session.begin() as session:
        yield session