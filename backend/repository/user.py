from uuid import UUID

from sqlalchemy import select

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.user import CreateUser, User
from backend.utils.security import get_password_hash


class UserRepo:
    async def get_user_by_email(self, email: str) -> db.User:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.email == email)
            return (await db_session.execute(query)).scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> db.User:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.id == user_id)
            return (await db_session.execute(query)).scalar_one_or_none()


    async def create_user(self, user_data: CreateUser) -> db.User:
        async with create_session() as db_session:
            db_user = db.User(
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                password=get_password_hash(user_data.password.get_secret_value()),
                role=user_data.role,
                domain=user_data.domain,
            )
            db_session.add(db_user)
            await db_session.flush()
            return db_user