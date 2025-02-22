from pydantic import BaseModel, Field

from backend.schema.base import Domain, HasID


class PostCreate(BaseModel):
    content: str = Field(..., max_length=1000)
    media_urls: list[str] | None = Field(None, max_length=5)
    domain: list[Domain] = Field(..., examples=[[Domain.CS], [Domain.DB, Domain.MATHEMATICS]])

class PostUpdate(BaseModel):
    content: str =  Field(..., max_length=1000)
    media_urls: list[str] | None = Field(None, max_length=5)
    domain: list[Domain] = Field(..., examples=[[Domain.CS], [Domain.DB, Domain.MATHEMATICS]])
    views: int = 0

class Post(HasID):
    content: str
    media_urls: list[str] | None
    domain: list[Domain]
    views: int = 0