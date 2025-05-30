from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    token: SecretStr

    model_config = SettingsConfigDict(env_prefix="TG_")

load_dotenv()
bot_settings = BotSettings()