from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.user import UserCreate, UserUpdate, Role
from backend.utils.security import get_password_hash


class UserRepo:
    async def get_user_by_email(self, email: str) -> db.User:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.email == email)
            return (await db_session.execute(query)).scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> db.User:
        async with create_session() as db_session:
            return await self._get_user_by_id(db_session, user_id)

    async def get_not_students(self) -> list[db.User]:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.role != Role.STUDENT)
            return (await db_session.execute(query)).scalars().all()

    async def create_user(self, user_data: UserCreate) -> db.User:
        async with create_session() as db_session:
            user = db.User(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                password=get_password_hash(user_data.password.get_secret_value()),
                role=user_data.role,
                domain=user_data.domain,
            )
            db_session.add(user)
            await db_session.flush()
            return user

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> db.User | None:
        async with create_session() as db_session:
            user = await self._get_user_by_id(db_session, user_id)
            if user is None:
                return None
            user.firstname = user_data.firstname
            user.lastname = user_data.lastname
            user.domain = user_data.domain
            return user

    @staticmethod
    async def _get_user_by_id(db_session: AsyncSession, user_id: UUID) -> db.User:
        query = select(db.User).where(db.User.id == user_id)
        return (await db_session.execute(query)).scalar_one_or_none()