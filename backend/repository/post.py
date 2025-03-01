import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.post import PostCreate, PostUpdate


class PostRepo:
    async def get_post_by_id(self, post_id: UUID) -> db.Post:
        async with create_session() as db_session:
            return await self._get_post_by_id(db_session, post_id)

    async def create_post(self, post_data: PostCreate) -> db.User:
        async with create_session() as db_session:
            post = db.Post(
                content=post_data.content,
                media_urls=post_data.media_urls,
                domain=post_data.domain,
            )
            db_session.add(post)
            await db_session.flush()
            return post

    async def update_post(self, post_id: UUID, post_data: PostUpdate) -> db.Post | None:
        async with create_session() as db_session:
            post = await self._get_post_by_id(db_session, post_id)
            if post is None:
                return None
            post.content = post.content
            post.domain = post.domain
            post.media_urls = post_data.media_urls
            post.views = post_data.views
            post.updated_at = datetime.datetime.now()
            return post

    @staticmethod
    async def _get_post_by_id(db_session: AsyncSession, post_id: UUID) -> db.Post:
        query = select(db.Post).where(db.Post.id == post_id)
        return (await db_session.execute(query)).scalar_one_or_none()