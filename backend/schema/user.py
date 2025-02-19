import enum

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_validator

from backend.schema.base import Domain, HasID


@enum.unique
class Role(enum.StrEnum):
    STUDENT = "student"
    EXPERT = "expert"
    ADMIN = "admin"


class UserCreate(BaseModel):
    firstname: str = Field("Иван", min_length=1, max_length=75)
    lastname: str = Field("Иванов", min_length=1, max_length=75)
    email: EmailStr = Field("user@edu.hse.ru")
    password: SecretStr
    role: Role = Field(Role.STUDENT, examples=[Role.STUDENT, Role.EXPERT, None])
    domain: list[Domain] | None = Field(
        None, examples=[[Domain.DB], [Domain.CS, Domain.MATHEMATICS], None]
    )

    @field_validator("email", mode="after")
    @classmethod
    def validate_hse_domain(cls, v: str) -> str:
        allowed_domain = "hse.ru"
        if not v.casefold().endswith(allowed_domain):
            raise ValueError(f"Only {allowed_domain} emails are allowed.")

        return v

class UserUpdate(BaseModel):
    firstname: str = Field(..., min_length=1, max_length=75)
    lastname: str = Field(..., min_length=1, max_length=75)
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])


class User(HasID):
    firstname: str
    lastname: str
    email: EmailStr
    role: Role = Role.STUDENT
    domain: list[Domain] | None = Field(None, examples=[[Domain.CS, Domain.MATHEMATICS], None])


class UserTryingToAuth(User):
    password: SecretStr
