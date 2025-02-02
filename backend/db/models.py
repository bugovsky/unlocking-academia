from datetime import datetime
from tokenize import String
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy_utils as su

from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from backend.db.base import Base
from backend.schema.request import Type
from backend.schema.user import Role, Domain


@so.declarative_mixin
class HasID:
    id: so.Mapped[UUID] = so.mapped_column(default=uuid4, primary_key=True, index=True, unique=True)

@so.declarative_mixin
class Creatable:
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())

@so.declarative_mixin
class Updatable(Creatable):
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())

@so.declarative_mixin
class Deletable(Creatable):
    deleted_at: so.Mapped[datetime | None] = so.mapped_column(sa.DateTime(timezone=True), default=None)


class User(Base, HasID, Creatable):
    __tablename__ = "users"

    firstname: so.Mapped[str] = so.mapped_column(sa.String(50))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(50))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    password: so.Mapped[str] =  so.mapped_column(sa.String)
    role: so.Mapped[Role] = so.mapped_column(nullable=False)
    domain: so.Mapped[list[Domain] | None] = so.mapped_column(
        sa.ARRAY(su.ChoiceType(Domain, impl=sa.String())), nullable=True
    )

    comments: so.Mapped[list["Comment"]] = so.relationship("Comment", back_populates="author", uselist=True)
    ratings: so.Mapped[list["Rating"]] = so.relationship("Rating", back_populates="user", uselist=True)
    requests: so.Mapped[list["Request"]] = so.relationship(
        "Request", back_populates="author", uselist=True, foreign_keys="Request.author_id"
    )
    responses: so.Mapped[list["Request"]] = so.relationship(
        "Request", back_populates="recipient", uselist=True, foreign_keys="Request.recipient_id"
    )


class Comment(Base, HasID, Deletable):
    __tablename__ = "comments"

    content: so.Mapped[str] = so.mapped_column(nullable=False)
    post_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("posts.id"), nullable=False)
    author_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("users.id"), nullable=False)

    post = so.relationship("Post", back_populates="comments")
    author = so.relationship("User", back_populates="comments")


class Rating(Base, HasID, Updatable):
    __tablename__ = "rating"

    grade: so.Mapped[int] = so.mapped_column(nullable=False)
    user_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("users.id"))
    post_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("posts.id"))

    user = so.relationship("User", back_populates="ratings")
    post = so.relationship("Post", back_populates="ratings")


class Post(Base, HasID, Updatable, Deletable):
    __tablename__ = "posts"

    content: so.Mapped[str]
    media_url: so.Mapped[list[str] | None] = so.mapped_column(sa.ARRAY(sa.String), nullable=True)
    domain: so.Mapped[list[Domain]] = so.mapped_column(sa.ARRAY(su.ChoiceType(Domain, impl=sa.String())))
    views: so.Mapped[int] = so.mapped_column(default=0)

    comments: so.Mapped[list[Comment]] = so.relationship("Comment", back_populates="post", uselist=True)
    ratings: so.Mapped[list[Rating]] = so.relationship("Rating", back_populates="post", uselist=True)


class Request(Base, HasID, Updatable):
    __tablename__ = "requests"

    question: so.Mapped[str] = so.mapped_column(nullable=False)
    response: so.Mapped[str] = so.mapped_column(nullable=True)
    type: so.Mapped[Type] = so.mapped_column(nullable=False)
    author_id: so.Mapped[UUID | None] = so.mapped_column(ForeignKey("users.id"), nullable=True)
    recipient_id: so.Mapped[UUID] = so.mapped_column(ForeignKey("users.id"))

    author = so.relationship("User", back_populates="requests", foreign_keys=author_id)
    recipient = so.relationship("User", back_populates="responses", foreign_keys=recipient_id)