from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 16379
    db: int = 0
    decode_responses: bool = True

    model_config = SettingsConfigDict(env_prefix="REDIS_")

load_dotenv()
redis_settings = RedisSettings()