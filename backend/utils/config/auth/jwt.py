import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class JWTSettings(BaseModel):
    algorithm: str
    secret_key: str
    access_token_expired: datetime.timedelta

    model_config = SettingsConfigDict(env_prefix="JWT_")