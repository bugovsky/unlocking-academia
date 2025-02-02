from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine


class DBSettings(BaseSettings):
    url: str
    # TODO как подружить flask-админ с асинхронным клиентом?
    sync_url: str

    model_config = SettingsConfigDict(env_prefix="DB_")

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: str) -> str:
        try:
            make_url(value)
            return value
        except Exception as e:
            raise ValueError(f"Invalid database URL: {e}") from e

    @property
    def engine(self) -> AsyncEngine:
        return create_async_engine(url=make_url(self.url), echo=True)
