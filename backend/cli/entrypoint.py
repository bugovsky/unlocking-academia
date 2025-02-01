import typer
import uvicorn

from backend.api.config import ServerSettings
from backend.db.base import Base
from backend.db.config import DBSettings

backend_app = typer.Typer(short_help="Запуск backend-приложения")


@backend_app.command(name="backend", short_help="Запустить fastapi-сервер")
async def run():
    async def create_tables():
        async with DBSettings().setup_db().begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    await create_tables()
    uvicorn.run(
        "backend.api.app:backend_app",
        **ServerSettings().model_dump(),
    )