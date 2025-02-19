import datetime
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from backend.schema.auth import TokenData
from backend.schema.user import User
from backend.service.user import UserService
from backend.utils.config.auth.jwt import jwt_settings
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# TODO: convert to class somehow?

def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
        return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise CREDENTIALS_EXCEPTION

        return TokenData(user_id=user_id)
    except InvalidTokenError:
        raise CREDENTIALS_EXCEPTION


async def get_current_user(
    user_service: Annotated[UserService, Depends()],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    token_data = verify_access_token(token)
    user = await user_service.get_user_by_id(user_id=token_data.user_id)

    return user