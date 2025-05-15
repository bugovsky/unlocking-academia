from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.rating import RatingRepo
from backend.schema.rating import RatingByUser, RatingCreate, RatingUpdate, PostRating


class RatingService:
    def __init__(self, rating_repo: Annotated[RatingRepo, Depends()]):
        self._rating_repo = rating_repo

    async def get_post_rating(self, post_id: UUID) -> PostRating | None:
        post_rating = await self._rating_repo.get_post_rating(post_id)
        if post_rating is None:
            return None

        return PostRating(post_id=post_id, grade=round(post_rating, 2))

    async def rate(self, post_id: UUID, user_id: UUID, rating_data: RatingCreate) -> RatingByUser:
        if await self._rating_repo.get_rating_by_user(post_id=post_id, user_id=user_id) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You have already rated this post")

        rating = await self._rating_repo.rate(post_id, user_id, rating_data)
        return self._build_rating_by_user(rating)

    async def update_rating(self, post_id: UUID, user_id: UUID, rating_data: RatingUpdate) -> RatingByUser:
        if await self._rating_repo.get_rating_by_user(post_id=post_id, user_id=user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="You have not rated this post")

        updated_rating = await self._rating_repo.update_rating(post_id, user_id, rating_data)
        if updated_rating is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post to rate not found")

        return self._build_rating_by_user(rating=updated_rating)

    @staticmethod
    def _build_rating_by_user(rating: db.Rating) -> RatingByUser:
        return RatingByUser(id=rating.id, grade=rating.grade, post_id=rating.post_id)