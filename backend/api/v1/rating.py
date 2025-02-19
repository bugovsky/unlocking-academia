from uuid import UUID

from fastapi import APIRouter, status

from backend.schema.rating import CreateRating, Rating, UpdateRating
from tests.factory.schema import RatingFactory

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Rating)
async def rate_post(rating: CreateRating):
    return RatingFactory.build(**rating.model_dump())


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=Rating)
async def get_post_rating(post_id: UUID):
    return RatingFactory.build(post_id=post_id)


@router.patch("/{post_id}", status_code=status.HTTP_200_OK, response_model=Rating)
async def update_post_rating(post_id: UUID, updated_rating: UpdateRating):
    return RatingFactory.build(**updated_rating.model_dump(), post_id=post_id)