from uuid import UUID

from fastapi import APIRouter, status

from backend.schema.request import CreateRequest, Request, CloseRequest
from tests.factory.schema import RequestFactory

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Request)
async def create_request(request: CreateRequest):
    return RequestFactory.build(**request.model_dump(), response=None)


@router.get("/{request_id}", status_code=status.HTTP_200_OK, response_model=Request)
async def get_request(request_id: UUID):
    return RequestFactory.build()


@router.patch("/{request_id}", status_code=status.HTTP_200_OK, response_model=Request)
async def close_request(request_id: UUID, responded_request: CloseRequest):
    return RequestFactory.build(**responded_request.model_dump())