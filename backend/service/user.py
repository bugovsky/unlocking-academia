from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.repository.user import UserRepo
from backend.schema.user import User, CreateUser


class UserService:
    def __init__(self, user_repo: Annotated[UserRepo, Depends()]):
        self._user_repo = user_repo

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self._user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return User(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            role=user.role,
            domain=user.domain,
        )

    async def create_user(self, user_data: CreateUser) -> User:
        user_by_email = await self._user_repo.get_user_by_email(email=user_data.email)
        if user_by_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user = await self._user_repo.create_user(user_data)
        return User(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            role=user.role,
            domain=user.domain,
        )