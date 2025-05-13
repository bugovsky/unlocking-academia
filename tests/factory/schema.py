from polyfactory.factories.pydantic_factory import ModelFactory

from backend.schema.auth import Token, TokenData
from backend.schema.comment import Comment, CommentCreate
from backend.schema.post import Post, PostCreate, PostUpdate
from backend.schema.rating import RatingCreate, RatingByUser, PostRating, RatingUpdate
from backend.schema.request import Request, RequestCreate, RequestClose
from backend.schema.user import User, UserCreate, UserUpdate, UserTryingToAuth

class UserFactory(ModelFactory[User]):
    ...

class UserCreateFactory(ModelFactory[UserCreate]):
    @classmethod
    def email(cls):
        return cls.__faker__.email(domain="hse.ru")


class UserUpdateFactory(ModelFactory[UserUpdate]):
    ...

class UserTryingToAuthFactory(ModelFactory[UserTryingToAuth]):
    ...

class PostFactory(ModelFactory[Post]):
    ...

class PostCreateFactory(ModelFactory[PostCreate]):
    ...

class PostUpdateFactory(ModelFactory[PostUpdate]):
    ...

class CommentFactory(ModelFactory[Comment]):
    ...

class CommentCreateFactory(ModelFactory[CommentCreate]):
    ...

class RequestFactory(ModelFactory[Request]):
    ...

class RequestCreateFactory(ModelFactory[RequestCreate]):
    ...

class RequestCloseFactory(ModelFactory[RequestClose]):
    ...

class RatingCreateFactory(ModelFactory[RatingCreate]):
    ...

class RatingByUserFactory(ModelFactory[RatingByUser]):
    ...

class PostRatingFactory(ModelFactory[PostRating]):
    ...

class RatingUpdateFactory(ModelFactory[RatingUpdate]):
    ...