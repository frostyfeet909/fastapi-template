from pydantic import Field, RedisDsn, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    NEED_INSECURE_URI: bool = False
    NEED_CELERY_BROKER_URI: bool = False
    NEED_CELERY_BACKEND_URI: bool = False

    HOST: str | None = Field(default="localhost")
    PORT: int | None = Field(default=6379)
    PASSWORD: SecretStr | None = None

    INSECURE_URI: RedisDsn | None = None
    CELERY_BROKER_URI: RedisDsn | None = None
    CELERY_BACKEND_URI: RedisDsn | None = None

    @field_validator("INSECURE_URI")
    @classmethod
    def validate_insecure_uri(cls, value: RedisDsn | None, values: ValidationInfo) -> RedisDsn | None:
        if values.data.get("NEED_INSECURE_URI"):
            value = cls.validate_redis_uri(value, values, "0", requires_password=False)
            if not value:
                raise ValueError("A insecure URI is required.")

            return value
        else:
            return None

    @field_validator("CELERY_BROKER_URI")
    @classmethod
    def validate_redis_broker_uri(cls, value: RedisDsn | None, values: ValidationInfo) -> RedisDsn | None:
        if values.data.get("NEED_CELERY_BROKER_URI"):
            value = cls.validate_redis_uri(value, values, "0")
            if not value:
                raise ValueError("A celery broker URI is required.")

            return value
        else:
            return None

    @field_validator("CELERY_BACKEND_URI")
    @classmethod
    def validate_redis_backend_uri(cls, value: RedisDsn | None, values: ValidationInfo) -> RedisDsn | None:
        if values.data.get("NEED_CELERY_BACKEND_URI"):
            value = cls.validate_redis_uri(value, values, "1")
            if not value:
                raise ValueError("A celery backend URI is required.")

            return value
        else:
            return None

    @classmethod
    def validate_redis_uri(
        cls, value: RedisDsn | None, values: ValidationInfo, db: str, requires_password: bool = True
    ) -> RedisDsn | None:
        if value:
            return value
        elif (host := values.data.get("HOST")) and (port := values.data.get("PORT")):
            if requires_password and values.data.get("PASSWORD"):
                password = values.data.get("PASSWORD").get_secret_value()
            else:
                password = None

            return RedisDsn.build(
                scheme="redis",
                host=host,
                port=port,
                password=password,
                path=f"/{db}",
            )

        return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="REDIS_")


settings = RedisSettings()
