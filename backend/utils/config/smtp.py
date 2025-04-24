from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender: str

    model_config = SettingsConfigDict(env_prefix="EMAIL_")

load_dotenv()
smtp_settings = SMTPSettings()