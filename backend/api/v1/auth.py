from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.schema.auth import Token
from backend.service.auth import AuthService
from backend.utils.client.auth.jwt import JWTClient

router = APIRouter()


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends()],
    jwt_client: Annotated[JWTClient, Depends()],
) -> Token:
    user = await auth_service.validate_credentials(email=form_data.username, password=form_data.password)

    access_token = jwt_client.create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")