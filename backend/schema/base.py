import enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class HasID(BaseModel):
    id: UUID = Field(default_factory=uuid4)


@enum.unique
class Domain(enum.StrEnum):
    MATHEMATICS = "Математические науки"
    CS = "Компьютерные науки"
    DB = "Базы данных"