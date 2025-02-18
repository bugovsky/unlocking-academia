import enum

from pydantic import BaseModel, Field, EmailStr, SecretStr

from backend.schema.base import Domain, HasID


@enum.unique
class Role(enum.StrEnum):
    STUDENT = "student"
    EXPERT = "expert"
    ADMIN = "admin"


class CreateUser(BaseModel):
    email: EmailStr
    password: SecretStr
    role: Role = Field(Role.STUDENT, examples=[Role.STUDENT, Role.EXPERT, None])
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


class TryingToAuthUser(User):
    password: SecretStr
