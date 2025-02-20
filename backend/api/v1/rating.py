from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends

from backend.schema.rating import RatingCreate, RatingByUser, RatingUpdate, PostRating
from backend.schema.user import User
from backend.service.rating import RatingService
from backend.utils.client.auth.jwt import get_current_user

router = APIRouter()


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=RatingByUser)
async def rate_post(
    post_id: UUID,
    rating: RatingCreate,
    user: Annotated[User, Depends(get_current_user)],
    rating_service: Annotated[RatingService, Depends()],
):
    return await rating_service.rate(post_id=post_id, user_id=user.id, rating_data=rating)


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRating)
async def get_post_rating(
    post_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    rating_service: Annotated[RatingService, Depends()],
):
    return await rating_service.get_post_rating(post_id)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=RatingByUser)
async def update_post_rating(
    post_id: UUID,
    updated_rating: RatingUpdate,
    user: Annotated[User, Depends(get_current_user)],
    rating_service: Annotated[RatingService, Depends()],
):
    return await rating_service.update_rating(post_id=post_id, user_id=user.id, rating_data=updated_rating)