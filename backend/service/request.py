from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.params import Depends

from backend.db import models as db
from backend.repository.request import RequestRepo
from backend.repository.user import UserRepo
from backend.schema.comment import Comment, CommentCreate
from backend.schema.request import Request, RequestCreate, RequestClose, Type
from backend.utils.client.smtp import send_email


class RequestService:
    def __init__(self, request_repo: Annotated[RequestRepo, Depends()], user_repo: Annotated[UserRepo, Depends()]):
        self._request_repo = request_repo
        self._user_repo = user_repo

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

        recipient = await self._user_repo.get_user_by_id(request_data.recipient_id)
        if recipient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
        author = await self._user_repo.get_user_by_id(user_id)
        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

        subject_template = "Unlocking Academia. {topic}"
        subject = ""
        if request_data.type is Type.QUESTION:
            subject = subject_template.format(topic="Вопрос от студента")
        if request_data.type is Type.CONSULTATION:
            subject = subject_template.format(topic="Запись на консультацию")
        body = (
            f"Вам поступил запрос от {author.firstname} {author.lastname}\n\n"
            f"{request_data.question}\n\n"
            f"Канал связи с автором запроса - {author.email}.\n\n"
            f"Данное письмо сформировано автоматически.\n\n"
        )

        try:
            await send_email(to_email=recipient.email, subject=subject, body=body)
        except Exception as e:
            print(f"Failed to send email to {recipient.email}: {str(e)}")

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