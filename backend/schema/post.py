from pydantic import BaseModel

from backend.db.models import HasID
from backend.schema.base import Domain


class CreatePost(BaseModel):
    content: str
    media_url: list[str] | None = None
    domain: list[Domain]

class UpdatePost(BaseModel):
    content: str
    media_url: list[str] | None = None
    domain: list[Domain]
    views: int = 0

class Post(HasID):
    content: str
    media_url: list[str] | None = None
    domain: list[Domain]
    views: int = 0