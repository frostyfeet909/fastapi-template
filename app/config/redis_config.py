from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    CELERY_BROKER_URI: RedisDsn = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="REDIS_")


settings = RedisSettings()
