import re

from pydantic import Field, PostgresDsn, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    NEED_ASYNC_URI: bool = False
    NEED_SYNC_URI: bool = False

    USER: str | None = None
    DB: str | None = None
    PASSWORD: SecretStr | None = None
    HOST: str | None = Field(default="localhost")

    ASYNC_URI: PostgresDsn | None = None
    SYNC_URI: PostgresDsn | None = None

    _PATTERN__postgres_password = re.compile(r":(\w)*@")

    @field_validator("SYNC_URI")
    @classmethod
    def validate_postgres_sync_uri(cls, value: PostgresDsn | None, values: ValidationInfo) -> PostgresDsn | None:
        if values.data.get("NEED_SYNC_URI"):
            value = cls.validate_postgres_uri(value, values, "postgresql+psycopg2")
            if not value:
                raise ValueError("A sync URI is required.")

            return value
        else:
            return None

    @field_validator("ASYNC_URI")
    @classmethod
    def validate_postgres_async_uri(cls, value: PostgresDsn | None, values: ValidationInfo) -> PostgresDsn | None:
        if values.data.get("NEED_ASYNC_URI"):
            value = cls.validate_postgres_uri(value, values, "postgresql+asyncpg")
            if not value:
                raise ValueError("A async URI is required.")

            return value
        else:
            return None

    """
    @field_serializer("ASYNC_URI", "SYNC_URI")
    def serialize_postgres_uri(self, value: PostgresDsn | None, _info) -> str | None:
        print("calles")
        return re.sub(self._PATTERN__postgres_password, ":********@", str(value)) if value else None
    """

    @classmethod
    def validate_postgres_uri(
        cls, value: PostgresDsn | None, values: ValidationInfo, scheme: str
    ) -> PostgresDsn | None:
        if value:
            return value
        elif (
            (user := values.data.get("USER"))
            and (password := values.data.get("PASSWORD"))
            and (db := values.data.get("DB"))
            and (host := values.data.get("HOST"))
        ):
            return PostgresDsn.build(
                scheme=scheme,
                username=user,
                password=password.get_secret_value(),
                host=host,
                path=f"/{db}",
            )

        return value

    @classmethod
    def get_secret_postgres_dsn(cls, value: PostgresDsn) -> str:
        return re.sub(cls._PATTERN__postgres_password, ":********@", value)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="POSTGRES_")


settings = PostgresSettings()
