from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.post import PostRepo
from backend.schema.post import Post, PostCreate, PostUpdate


class PostService:
    def __init__(self, post_repo: Annotated[PostRepo, Depends()]):
        self._post_repo = post_repo

    async def get_post_by_id(self, post_id: UUID) -> Post:
        post = await self._post_repo.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return self._build_post(post)

    async def create_post(self, post_data: PostCreate) -> Post:
        post = await self._post_repo.create_post(post_data)
        return self._build_post(post)

    async def update_post(self, post_id: UUID, post_data: PostUpdate) -> Post:
        updated_post = await self._post_repo.update_post(post_id, post_data)
        if updated_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return self._build_post(post=updated_post)

    @staticmethod
    def _build_post(post: db.Post) -> Post:
        return Post(
            id=post.id,
            content=post.content,
            media_urls=post.media_urls,
            domain=post.domain,
            views=post.views,
        )