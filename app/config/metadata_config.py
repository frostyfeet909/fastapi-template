from pydantic import EmailStr, FieldValidationInfo, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MetadataSettings(BaseSettings):
    CONTACT_NAME: str | None = None
    CONTACT_URL: HttpUrl | None = None
    CONTACT_EMAIL: EmailStr | None = None
    CONTACT: dict | None = None

    LICENSE_NAME: str | None = None
    LICENSE_URL: HttpUrl | None = None
    LICENSE: dict | None = None

    @field_validator("CONTACT", mode="before")
    def assemble_contact(cls, value: dict, values: FieldValidationInfo) -> dict:  # noqa
        values = values.data
        if value:
            return value
        else:
            value = {}
            if val := values.get("CONTACT_NAME"):
                value["name"] = val
            if val := values.get("CONTACT_URL"):
                value["url"] = val
            if val := values.get("CONTACT_EMAIL"):
                value["email"] = val
            return value

    @field_validator("LICENSE", mode="before")
    def assemble_license(cls, value: dict, values: FieldValidationInfo) -> dict:  # noqa
        values = values.data
        if value:
            return value
        else:
            value = {}
            if val := values.get("LICENSE_NAME"):
                value["name"] = val
            if val := values.get("LICENSE_URL"):
                value["url"] = val

            return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="META_")


settings = MetadataSettings()
