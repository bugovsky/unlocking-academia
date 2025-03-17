from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    decode_responses: bool = True

    model_config = SettingsConfigDict(env_prefix="REDIS_")

redis_settings = RedisSettings()