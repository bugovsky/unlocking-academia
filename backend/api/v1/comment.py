from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends

from backend.schema.comment import CommentCreate, Comment
from backend.schema.user import User
from backend.service.comment import CommentService
from backend.utils.client.auth.jwt import get_current_user

router = APIRouter()


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(
    post_id: UUID,
    comment: CommentCreate,
    user: Annotated[User, Depends(get_current_user)],
    comment_service: Annotated[CommentService, Depends()],
):
    return await comment_service.create_comment(post_id, user_id=user.id, comment_data=comment)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=list[Comment])
async def get_post_comments(
    post_id: UUID,
    comment_service: Annotated[CommentService, Depends()],
):
    return await comment_service.get_post_comments(post_id)