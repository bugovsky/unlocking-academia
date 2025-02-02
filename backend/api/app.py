from fastapi import FastAPI

from backend.api.v1 import user, post, request



def create_app() -> FastAPI:
    app = FastAPI(title="Unlocking Academia")
    app.include_router(user.router, prefix="/users", tags=['Users'])
    app.include_router(post.router, prefix="/posts", tags=['Posts'])
    app.include_router(request.router, prefix="/requests", tags=['Requests'])

    return app

backend_app = create_app()