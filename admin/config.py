from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AdminSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5000

    # TODO как подружить flask-админ с асинхронным клиентом и нужно ли?
    db_url: str = Field(..., description="URL БД для подключения внутри Flask-приложения")
    db_echo: bool = True
    secret_key: str

    model_config = SettingsConfigDict(env_prefix="ADMIN_", strict=False)

load_dotenv()
admin_settings = AdminSettings()