from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from backend.schema.base import HasID


class RatingCreate(BaseModel):
    grade: int = Field(ge=0, le=10)


class RatingByUser(HasID):
    grade: int
    post_id: UUID


class PostRating(BaseModel):
    grade: Decimal = Field(..., decimal_places=2)
    post_id: UUID


class RatingUpdate(BaseModel):
    grade: int = Field(ge=0, le=10)