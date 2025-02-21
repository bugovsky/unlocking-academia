from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.request import RequestRepo
from backend.schema.comment import Comment, CommentCreate
from backend.schema.request import Request, RequestCreate, RequestClose


class RequestService:
    def __init__(self, request_repo: Annotated[RequestRepo, Depends()]):
        self._request_repo = request_repo

    async def get_request_by_id(self, user_id: UUID, request_id: UUID) -> Request:
        request = await self._request_repo.get_request_by_id(request_id)
        if request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request.author_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to request failed")

        return self._build_request(request)

    async def get_user_requests(self, user_id: UUID) -> list[Request]:
        requests = await self._request_repo.get_user_requests(user_id)

        return [self._build_request(request) for request in requests]

    async def create_request(self, user_id: UUID, request_data: RequestCreate) -> Request:
        request = await self._request_repo.create_request(user_id, request_data)
        return self._build_request(request)

    async def close_request(self, user_id: UUID, request_id: UUID, request_data: RequestClose) -> Request:
        request = await self._request_repo.get_request_by_id(request_id)
        if request is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request.recipient_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access to request failed")

        closed_request = await self._request_repo.close_request(request_id, request_data)
        return self._build_request(request=closed_request)

    @staticmethod
    def _build_request(request: db.Request) -> Request:
        return Request(
            id=request.id,
            type=request.type,
            question=request.question,
            response=request.response,
            author_id=request.author_id,
            recipient_id=request.recipient_id,
        )