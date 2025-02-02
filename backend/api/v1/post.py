from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.dialects.mssql.information_schema import views

from backend.schema.post import CreatePost, Post, UpdatePost
from backend.schema.user import Domain
from tests.factory.schema import PostFactory

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: CreatePost):
    return Post(**post.model_dump())


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
async def get_post(post_id: UUID):
    return PostFactory.build(views=0)


@router.patch('/{post_id}', status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(post_id: UUID, post_updates: UpdatePost):
    return Post(**post_updates.model_dump())