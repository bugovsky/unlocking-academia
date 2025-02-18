import datetime

from pydantic_settings import SettingsConfigDict, BaseSettings


class JWTSettings(BaseSettings):
    algorithm: str
    secret_key: str
    access_token_expired: datetime.timedelta

    model_config = SettingsConfigDict(env_prefix="JWT_")

jwt_settings = JWTSettings()