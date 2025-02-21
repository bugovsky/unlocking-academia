from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.comment import CommentRepo
from backend.repository.post import PostRepo
from backend.schema.comment import Comment, CommentCreate


class CommentService:
    def __init__(self, comment_repo: Annotated[CommentRepo, Depends()], post_repo: Annotated[PostRepo, Depends()]):
        self._comment_repo = comment_repo
        self._post_repo = post_repo

    async def get_post_comments(self, post_id: UUID) -> list[Comment]:
        if await self._post_repo.get_post_by_id(post_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        comments = await self._comment_repo.get_post_comments(post_id)
        return [self._build_comment(comment) for comment in comments]

    async def create_comment(self, post_id: UUID, user_id: UUID, comment_data: CommentCreate) -> Comment:
        if await self._post_repo.get_post_by_id(post_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        comment = await self._comment_repo.create_comment(post_id, user_id, comment_data)
        return self._build_comment(comment)

    @staticmethod
    def _build_comment(comment: db.Comment) -> Comment:
        return Comment(id=comment.id, content=comment.content, author_id=comment.author_id, post_id=comment.post_id)