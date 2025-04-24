from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    reload: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_prefix="SERVER_")

load_dotenv()
