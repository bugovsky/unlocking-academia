from uuid import UUID

from pydantic import BaseModel


class CreateComment(BaseModel):
    content: str

class Comment(BaseModel):
    content: str
    author_id: UUID
    post_id: UUID