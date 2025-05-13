from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from backend.api.app import create_app
from backend.schema.user import Role
from backend.service.auth import AuthService
from backend.service.comment import CommentService
from backend.service.post import PostService
from backend.service.rating import RatingService
from backend.service.request import RequestService
from backend.service.user import UserService
from backend.utils.client.auth.jwt import get_current_user
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION
from tests.factory.schema import UserFactory


@pytest.fixture
def mocked_auth_service(mocker):
    return mocker.create_autospec(AuthService)


@pytest.fixture
def mocked_comment_service(mocker):
    return mocker.create_autospec(CommentService)


@pytest.fixture
def mocked_post_service(mocker):
    return mocker.create_autospec(PostService)


@pytest.fixture
def mocked_rating_service(mocker):
    return mocker.create_autospec(RatingService)


@pytest.fixture
def mocked_request_service(mocker):
    return mocker.create_autospec(RequestService)


@pytest.fixture
def mocked_user_service(mocker):
    return mocker.create_autospec(UserService)


@pytest.fixture(scope="session")
def backend_app():
    return create_app()


@pytest.fixture(scope="session")
def unknown_user_id():
    return uuid4()


@pytest.fixture
def backend_client(
    backend_app,
    mocked_auth_service,
    mocked_comment_service,
    mocked_post_service,
    mocked_rating_service,
    mocked_request_service,
    mocked_user_service,
    unknown_user_id,
):
    def mocked_get_current_user(user_id: UUID | None = None, role: Role | None = None):
        if user_id is None or role is None:
            raise CREDENTIALS_EXCEPTION
        if user_id == unknown_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserFactory.build(id=user_id, role=role)

    backend_app.dependency_overrides = {
        AuthService: lambda: mocked_auth_service,
        CommentService: lambda: mocked_comment_service,
        PostService: lambda: mocked_post_service,
        RatingService: lambda: mocked_rating_service,
        RequestService: lambda: mocked_request_service,
        UserService: lambda: mocked_user_service,
        get_current_user: mocked_get_current_user,
    }

    with TestClient(backend_app) as test_client:
        yield test_client

    backend_app.dependency_overrides.clear()