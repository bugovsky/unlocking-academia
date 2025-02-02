from uuid import UUID

from pydantic import BaseModel, Field


class CreateRating(BaseModel):
    grade: int


class Rating(BaseModel):
    grade: int = Field(ge=0, le=10)
    post_id: UUID


class UpdateRating(BaseModel):
    grade: int