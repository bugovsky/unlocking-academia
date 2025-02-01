import enum


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