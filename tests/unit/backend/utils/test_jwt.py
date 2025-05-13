import uuid
from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException

from backend.schema.auth import TokenData
from backend.utils.client.auth.jwt import create_access_token, verify_access_token
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION

@pytest.fixture
def user_id():
    return uuid.uuid4()


class TestJWT:
    def test_create_access_token(self, user_id):
        data = {"sub": str(user_id)}
        token = create_access_token(data)
        decoded = jwt.decode(token, options={"verify_signature": False})

        assert decoded["sub"] == str(user_id)
        assert "exp" in decoded

    def test_create_access_token_with_expires(self, user_id):
        expires_delta = timedelta(minutes=30)
        data = {"sub": str(user_id)}
        token = create_access_token(data, expires_delta)
        decoded = jwt.decode(token, options={"verify_signature": False})

        assert decoded["sub"] == str(user_id)
        assert datetime.fromtimestamp(decoded["exp"]) > datetime.now()

    def test_verify_access_token_success(self, user_id):
        token = create_access_token({"sub": str(user_id)})
        token_data = verify_access_token(token)

        assert isinstance(token_data, TokenData)
        assert token_data.user_id == user_id

    def test_verify_access_token_invalid(self):
        with pytest.raises(HTTPException) as err:
            verify_access_token("invalid_token")

        assert err.value is CREDENTIALS_EXCEPTION

    def test_verify_access_token_no_sub(self):
        token = create_access_token({})
        with pytest.raises(HTTPException) as err:
            verify_access_token(token)

        assert err.value is CREDENTIALS_EXCEPTION
