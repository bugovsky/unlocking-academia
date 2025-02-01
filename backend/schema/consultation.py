import enum


@enum.unique
class Status(enum.StrEnum):
    PENDING = "pending"
    REJECTED = "rejected"
    ACCEPTED = "accepted"