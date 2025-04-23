from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Depends

from backend.schema.user import UserCreate, User, UserUpdate
from backend.service.user import UserService

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UserCreate, user_service: Annotated[UserService, Depends()]):
    return await user_service.create_user(user_data=user)

@router.get("/experts", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_not_students(user_service: Annotated[UserService, Depends()]):
    return await user_service.get_not_students()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: UUID, user_service: Annotated[UserService, Depends()]):
    return await user_service.get_user_by_id(user_id)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: UUID, user_data: UserUpdate, user_service: Annotated[UserService, Depends()]):
    return await user_service.update_user(user_id, user_data)