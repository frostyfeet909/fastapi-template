import secrets

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN_EXPIRES_MINUTES: int = Field(default=30, gt=0)
    TOKEN_ALGORITHM: str = "HS256"
    SECRET_KEY: SecretStr = secrets.token_urlsafe(64)

    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str | None = None
    PROJECT_URL: HttpUrl | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="APP_")


settings = Settings()
