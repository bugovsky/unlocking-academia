import pytest

from backend.repository.comment import CommentRepo
from backend.repository.post import PostRepo
from backend.repository.rating import RatingRepo
from backend.repository.request import RequestRepo
from backend.repository.user import UserRepo

@pytest.fixture
def mocked_user_repo(mocker):
    return mocker.create_autospec(UserRepo)

@pytest.fixture
def mocked_comment_repo(mocker):
    return mocker.create_autospec(CommentRepo)

@pytest.fixture
def mocked_post_repo(mocker):
    return mocker.create_autospec(PostRepo)

@pytest.fixture
def mocked_rating_repo(mocker):
    return mocker.create_autospec(RatingRepo)

@pytest.fixture
def mocked_request_repo(mocker):
    return mocker.create_autospec(RequestRepo)