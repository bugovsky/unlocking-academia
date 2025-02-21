from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.request import RequestCreate, RequestClose


class RequestRepo:
    async def get_request_by_id(self, request_id: UUID) -> db.Request:
        async with create_session() as db_session:
            return await self._get_request_by_id(db_session, request_id)

    async def get_user_requests(self, user_id: UUID) -> list[db.Request]:
        async with create_session() as db_session:
            query = select(db.Request).where(db.Request.author_id == user_id)
            return (await db_session.execute(query)).scalars().all()

    async def create_request(self, user_id: UUID, request_data: RequestCreate) -> db.Request:
        async with create_session() as db_session:
            request = db.Request(
                question=request_data.question,
                type=request_data.type,
                recipient_id=request_data.recipient_id,
                author_id=user_id,
            )
            db_session.add(request)
            await db_session.flush()
            return request

    async def close_request(self, request_id: UUID, request_data: RequestClose) -> db.Request:
        async with create_session() as db_session:
            request = await self._get_request_by_id(db_session, request_id=request_id)
            request.response = request_data.response

            return request

    @staticmethod
    async def _get_request_by_id(db_session: AsyncSession, request_id: UUID) -> db.Request:
        query = select(db.Request).where(db.Request.id == request_id)
        return (await db_session.execute(query)).scalar_one_or_none()