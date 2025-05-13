import random

from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from backend.db.models import User, Rating, Request, Comment, Post
from backend.schema.base import Domain
from backend.schema.request import Type
from backend.schema.user import Role
from backend.utils.security import get_password_hash


class UserFactory(SQLAlchemyFactory[User]):
    @classmethod
    def email(cls):
        return cls.__faker__.email(domain="edu.hse.ru")

    @classmethod
    def password(cls):
        return get_password_hash(cls.__faker__.pystr(min_chars=6))

    @classmethod
    def role(cls):
        return random.choice(list(Role))

    @classmethod
    def domain(cls):
        return random.sample(list(Domain), k=random.randint(0, len(Domain))) or None


class CommentFactory(SQLAlchemyFactory[Comment]):
    ...


class PostFactory(SQLAlchemyFactory[Post]):
    @classmethod
    def domain(cls):
        return random.sample(list(Domain), k=random.randint(1, len(Domain))) or None


class RatingFactory(SQLAlchemyFactory[Rating]):
    ...


class RequestFactory(SQLAlchemyFactory[Request]):
    @classmethod
    def type(cls):
        return random.choice(list(Type))

