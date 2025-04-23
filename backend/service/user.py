from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.user import UserRepo
from backend.schema.user import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo: Annotated[UserRepo, Depends()]):
        self._user_repo = user_repo

    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self._user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return self._build_user(user)

    async def get_not_students(self) -> list[User]:
        users = await self._user_repo.get_not_students()

        return [self._build_user(user) for user in users]

    async def create_user(self, user_data: UserCreate) -> User:
        user_by_email = await self._user_repo.get_user_by_email(email=user_data.email)
        if user_by_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user = await self._user_repo.create_user(user_data)
        return self._build_user(user)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> User:
        updated_user = await self._user_repo.update_user(user_id, user_data)
        if updated_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return self._build_user(user=updated_user)

    @staticmethod
    def _build_user(user: db.User) -> User:
        return User(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            role=user.role,
            domain=user.domain,
        )