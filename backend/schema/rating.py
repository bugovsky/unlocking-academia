from uuid import UUID

from pydantic import BaseModel, Field

from backend.db.models import HasID


class CreateRating(BaseModel):
    grade: int


class Rating(HasID):
    grade: int = Field(ge=0, le=10)
    post_id: UUID


class UpdateRating(BaseModel):
    grade: int