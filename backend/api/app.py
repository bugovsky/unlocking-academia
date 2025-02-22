from fastapi import FastAPI

from backend.api.v1 import user, post, request, comment, rating, auth


def create_app() -> FastAPI:
    app = FastAPI(title="Unlocking Academia")
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(user.router, prefix="/user", tags=["Users"])
    app.include_router(post.router, prefix="/post", tags=["Posts"])
    app.include_router(request.router, prefix="/request", tags=["Requests"])
    app.include_router(comment.router, prefix="/comment", tags=["Comments"])
    app.include_router(rating.router, prefix="/rating", tags=["Rating"])

    return app

backend_app = create_app()