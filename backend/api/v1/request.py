from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends

from backend.schema.request import RequestCreate, Request, RequestClose
from backend.schema.user import User
from backend.service.request import RequestService
from backend.utils.client.auth.jwt import get_current_user

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Request)
async def create_request(
    request: RequestCreate,
    user: Annotated[User, Depends(get_current_user)],
    request_service: Annotated[RequestService, Depends()],
):
    return await request_service.create_request(user_id=user.id, request_data=request)


@router.get("/{request_id}", status_code=status.HTTP_200_OK, response_model=Request)
async def get_request(
    request_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    request_service: Annotated[RequestService, Depends()],
):
    return await request_service.get_request_by_id(user_id=user.id, request_id=request_id)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[Request])
async def get_user_requests(
    user: Annotated[User, Depends(get_current_user)],
    request_service: Annotated[RequestService, Depends()],
):
    return await request_service.get_user_requests(user_id=user.id)


@router.patch("/{request_id}", status_code=status.HTTP_200_OK, response_model=Request)
async def close_request(
    request_id: UUID,
    responded_request: RequestClose,
    user: Annotated[User, Depends(get_current_user)],
    request_service: Annotated[RequestService, Depends()],
):
    return await request_service.close_request(user_id=user.id, request_id=request_id, request_data=responded_request)