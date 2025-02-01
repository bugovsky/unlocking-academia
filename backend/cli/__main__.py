# TODO потом на клишку как-нибудь перейти

import asyncio

import uvicorn
from backend.db.base import Base, engine

from backend.api.config import ServerSettings

# TODO потом удалить, импорт будет не нужен
from backend.db import models


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def run():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(run())
    uvicorn.run(
        "backend.api.app:backend_app",
        **ServerSettings().model_dump(),
    )