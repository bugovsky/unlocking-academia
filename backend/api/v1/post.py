from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException
import logging

from backend.schema.post import PostCreate, Post, PostUpdate
from backend.schema.user import User, Role
from backend.service.post import PostService
from backend.utils.client.auth.jwt import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[Post])
async def get_posts(post_service: Annotated[PostService, Depends()]):
    logger.debug("get_posts called")
    return await post_service.get_posts()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post: PostCreate, user: Annotated[User, Depends(get_current_user)], post_service: Annotated[PostService, Depends()]
):
    if user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource."
        )
    return await post_service.create_post(post_data=post)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_post(
    post_id: UUID, post_service: Annotated[PostService, Depends()]
):
    return await post_service.get_post_by_id(post_id)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(
    post_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    post_update: PostUpdate,
    post_service: Annotated[PostService, Depends()]
):
    if user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource."
        )
    return await post_service.update_post(post_id, post_update)
