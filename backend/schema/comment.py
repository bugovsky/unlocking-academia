from uuid import UUID

from pydantic import BaseModel

from backend.schema.base import HasID


class CommentCreate(BaseModel):
    content: str

class Comment(HasID):
    content: str
    author_id: UUID
    post_id: UUID