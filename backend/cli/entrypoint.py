import typer
import uvicorn

from backend.api.config import ServerSettings

backend_app = typer.Typer(short_help="Запуск backend-приложения")


@backend_app.command(name="backend", short_help="Запустить fastapi-сервер")
def launch_backend():
    async def main():
        uvicorn.run("backend.api.app:backend_app", **ServerSettings().model_dump())

    import asyncio

    asyncio.run(main())