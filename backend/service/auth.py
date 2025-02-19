from typing import Annotated

from fastapi.params import Depends

from backend.repository.user import UserRepo
from backend.schema.user import UserTryingToAuth
from backend.utils.exception.auth.jwt import CREDENTIALS_EXCEPTION
from backend.utils.security import verify_password, get_password_hash


class AuthService:
    def __init__(self, user_repo: Annotated[UserRepo, Depends()]):
        self._user_repo = user_repo

    async def validate_credentials(self, email: str, password: str):
        user = await self._user_repo.get_user_by_email(email=email)

        if user is None:
            raise CREDENTIALS_EXCEPTION

        possible_user = UserTryingToAuth(
            firstname=user.firstname,
            lastname=user.lastname,
            id=user.id,
            password=user.password,
            email=user.email,
            role=user.role,
        )
        if not verify_password(password, possible_user.password.get_secret_value()):
            raise CREDENTIALS_EXCEPTION
        return possible_user