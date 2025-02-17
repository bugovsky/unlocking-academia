from uuid import UUID

from sqlalchemy import select

from backend.db.utils import create_session
from backend.db import models as db


class UserRepo:
    async def get_user_by_email(self, email: str) -> db.User:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.email == email)
            return (await db_session.execute(query)).scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> db.User:
        async with create_session() as db_session:
            query = select(db.User).where(db.User.id == user_id)
            return (await db_session.execute(query)).scalar_one_or_none()