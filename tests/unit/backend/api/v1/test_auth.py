from fastapi import status

from backend.schema.auth import Token
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION
from tests.factory.schema import UserTryingToAuthFactory


class TestAuth:
    def test_login_success(self, backend_client, mocked_auth_service):
        user = UserTryingToAuthFactory.build()
        mocked_auth_service.validate_credentials.return_value = user

        response = backend_client.post(
            "/auth/login",
            data={"username": user.email, "password": user.password.get_secret_value()}
        )

        assert response.status_code == status.HTTP_200_OK
        assert Token.model_validate(response.json())
        mocked_auth_service.validate_credentials.assert_called_once_with(
            email=user.email, password=user.password.get_secret_value()
        )

    def test_login_invalid_credentials(self, backend_client, mocked_auth_service):
        mocked_auth_service.validate_credentials.side_effect = CREDENTIALS_EXCEPTION

        response = backend_client.post(
            "/auth/login",
            data={"username": "invalid@hse.ru", "password": "wrong"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Could not validate credentials"
        mocked_auth_service.validate_credentials.assert_called_once_with(
            email="invalid@hse.ru", password="wrong"
        )