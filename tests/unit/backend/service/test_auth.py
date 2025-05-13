from fastapi import HTTPException

import pytest

from backend.schema.user import UserTryingToAuth
from backend.service.auth import AuthService
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION
from backend.utils.security import get_password_hash
from tests.factory.models import UserFactory


@pytest.fixture
def auth_service(mocked_user_repo):
    return AuthService(user_repo=mocked_user_repo)

@pytest.fixture
def password():
    return "secret_password"


class TestAuthService:
    async def test_validate_credentials_success(self, auth_service, mocked_user_repo, password):
        hashed_password = get_password_hash(password)
        user = UserFactory.build(password=hashed_password)
        mocked_user_repo.get_user_by_email.return_value = user

        result = await auth_service.validate_credentials(email=user.email, password=password)

        assert isinstance(result, UserTryingToAuth)
        assert result.id == user.id
        mocked_user_repo.get_user_by_email.assert_called_once_with(email=user.email)

    async def test_validate_credentials_user_not_found(self, auth_service, mocked_user_repo):
        mocked_user_repo.get_user_by_email.return_value = None

        with pytest.raises(HTTPException) as err:
            await auth_service.validate_credentials(email="invalid@hse.ru", password="wrong")

        assert err.value is CREDENTIALS_EXCEPTION
        mocked_user_repo.get_user_by_email.assert_called_once_with(email="invalid@hse.ru")

    async def test_validate_credentials_wrong_password(self, auth_service, mocked_user_repo):
        user = UserFactory.build()
        mocked_user_repo.get_user_by_email.return_value = user

        with pytest.raises(HTTPException) as err:
            await auth_service.validate_credentials(email=user.email, password="wrong")

        assert err.value is CREDENTIALS_EXCEPTION
        mocked_user_repo.get_user_by_email.assert_called_once_with(email=user.email)