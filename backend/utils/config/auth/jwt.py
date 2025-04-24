import datetime

from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict, BaseSettings


class JWTSettings(BaseSettings):
    algorithm: str
    secret_key: str
    access_token_expired: datetime.timedelta

    model_config = SettingsConfigDict(env_prefix="JWT_")

load_dotenv()
jwt_settings = JWTSettings()