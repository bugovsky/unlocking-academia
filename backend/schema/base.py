import enum
from uuid import UUID

from pydantic import BaseModel


class HasID(BaseModel):
    id: UUID


@enum.unique
class Domain(enum.StrEnum):
    MATHEMATICS = "Математические науки"
    CS = "Компьютерные науки"
    DB = "Базы данных"