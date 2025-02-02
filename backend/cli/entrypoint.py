import typer
import uvicorn

from backend.api.config import ServerSettings
from backend.db.base import Base, engine

backend_app = typer.Typer(short_help="Запуск backend-приложения")


@backend_app.command(name="backend", short_help="Запустить fastapi-сервер")
def launch_backend():
    async def main():

        async def init_db():
            # TODO потом удалить, импорт будет не нужен
            from backend.db import models

            async with engine.begin() as conn:
                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        await init_db()
        uvicorn.run(
            "backend.api.app:backend_app",
            **ServerSettings().model_dump(),
        )

    import asyncio

    asyncio.run(main())