import re

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    ASYNC_URI: PostgresDsn | None = None
    SYNC_URI: PostgresDsn | None = None

    _PATTERN__postgres_password = re.compile(r":(\w)*@")

    @classmethod
    def get_secret_postgres_dsn(cls, value: PostgresDsn) -> str:
        return re.sub(cls._PATTERN__postgres_password, ":********@", value)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="POSTGRES_")


settings = PostgresSettings()
