import enum

from pydantic import BaseModel, Field, EmailStr, SecretStr

from backend.schema.base import Domain, HasID


@enum.unique
class Role(enum.StrEnum):
    STUDENT = "student"
    EXPERT = "expert"
    ADMIN = "admin"


class CreateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr
    password: SecretStr
    role: Role = Role.STUDENT
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])


class User(HasID):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr
    role: Role = Role.STUDENT
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])
