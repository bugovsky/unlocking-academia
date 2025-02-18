from uuid import UUID

from fastapi import APIRouter, status

from backend.schema.user import CreateUser, User, UpdateUser
from tests.factory.schema import UserFactory

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: CreateUser):
    return UserFactory.build()


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: UUID):
    return UserFactory.build()


@router.patch('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: UUID, user_info: UpdateUser):
    return UserFactory.build(**user_info.model_dump())