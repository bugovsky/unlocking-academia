import enum

from pydantic import BaseModel, Field, EmailStr, SecretStr


@enum.unique
class Role(enum.StrEnum):
    STUDENT = "student"
    EXPERT = "expert"
    ADMIN = "admin"


@enum.unique
class Domain(enum.StrEnum):
    MATHEMATICS = "Математические науки"
    CS = "Компьютерные науки"
    DB = "Базы данных"


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


class User(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr
    role: Role = Role.STUDENT
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])
