from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Unlocking Academia")

    return app

backend_app = create_app()