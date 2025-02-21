from uuid import UUID

from sqlalchemy import select

from backend.db.utils import create_session
from backend.db import models as db
from backend.schema.comment import CommentCreate


class CommentRepo:
    async def get_post_comments(self, post_id: UUID) -> list[db.Comment]:
        async with create_session() as db_session:
            query = select(db.Comment).where(db.Comment.post_id == post_id)
            return (await db_session.execute(query)).scalars().all()

    async def create_comment(self, post_id: UUID, user_id: UUID, comment_data: CommentCreate) -> db.Comment:
        async with create_session() as db_session:
            comment = db.Comment(
                content=comment_data.content,
                post_id=post_id,
                author_id=user_id,
            )
            db_session.add(comment)
            await db_session.flush()
            return comment