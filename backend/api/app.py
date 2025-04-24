from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.api.v1 import user, post, request, comment, rating, auth


def create_app() -> FastAPI:
    app = FastAPI(title="Unlocking Academia")
    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(user.router, prefix="/user", tags=["Users"])
    app.include_router(post.router, prefix="/post", tags=["Posts"])
    app.include_router(request.router, prefix="/request", tags=["Requests"])
    app.include_router(comment.router, prefix="/comment", tags=["Comments"])
    app.include_router(rating.router, prefix="/rating", tags=["Rating"])

    return app

backend_app = create_app()