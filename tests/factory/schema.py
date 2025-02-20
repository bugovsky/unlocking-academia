from polyfactory.factories.pydantic_factory import ModelFactory

from backend.schema.comment import Comment
from backend.schema.post import Post
from backend.schema.user import User
from backend.schema.request import Request

class UserFactory(ModelFactory[User]):
    ...


class PostFactory(ModelFactory[Post]):
    ...


class RequestFactory(ModelFactory[Request]):
    ...


class CommentFactory(ModelFactory[Comment]):
    ...