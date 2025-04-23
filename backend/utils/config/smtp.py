from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender: str

    model_config = SettingsConfigDict(env_prefix="EMAIL_")

smtp_settings = SMTPSettings()