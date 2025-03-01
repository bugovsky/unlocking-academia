import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, func

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.rating import RatingCreate, RatingUpdate


class RatingRepo:
    async def get_rating_by_user(self, post_id: UUID, user_id: UUID) -> db.Rating:
        async with create_session() as db_session:
            query = select(db.Rating).where(db.Rating.post_id == post_id, db.Rating.user_id==user_id)
            return (await db_session.execute(query)).scalar_one_or_none()

    async def get_post_rating(self, post_id: UUID) -> Decimal:
        async with create_session() as db_session:
            query = select(func.avg(db.Rating.grade)).where(db.Rating.post_id == post_id)
            return (await db_session.execute(query)).scalar_one_or_none()

    async def rate(self, post_id: UUID, user_id: UUID, rating_data: RatingCreate) -> db.Rating:
        async with create_session() as db_session:
            rating = db.Rating(
                user_id=user_id,
                post_id=post_id,
                grade=rating_data.grade,
            )
            db_session.add(rating)
            await db_session.flush()
            return rating

    async def update_rating(self, post_id: UUID, user_id: UUID, rating_data: RatingUpdate) -> db.Rating | None:
        async with create_session() as db_session:
            query = select(db.Rating).where(
                db.Rating.post_id == post_id,
                db.Rating.user_id == user_id

            )
            rating = (await db_session.execute(query)).scalar_one_or_none()
            if rating is None:
                return None

            rating.grade = rating_data.grade
            rating.updated_at = datetime.datetime.now()
            return rating