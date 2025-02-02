from uuid import UUID

from fastapi import APIRouter, status

from backend.schema.comment import CreateComment, Comment
from tests.factory.schema import CommentFactory

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(comment: CreateComment):
    return CommentFactory.build(**comment.model_dump())


@router.get('/{comment_id}', status_code=status.HTTP_200_OK, response_model=Comment)
async def get_comment(comment_id: UUID):
    return CommentFactory.build()