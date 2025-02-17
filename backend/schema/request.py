import enum
from uuid import UUID

from pydantic import BaseModel

from backend.schema.base import HasID


class Type(enum.StrEnum):
    QUESTION = "question"
    CONSULTATION = "consultation"


class CreateRequest(BaseModel):
    question: str
    type: Type
    recipient_id: UUID


class Request(HasID):
    question: str
    type: Type
    response: str | None = None
    author_id: UUID | None = None
    recipient_id: UUID


class CloseRequest(BaseModel):
    response: str