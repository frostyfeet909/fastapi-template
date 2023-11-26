from typing import Annotated

from core.security import check_password_strength
from fastapi import Path
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    PastDatetime,
    SecretStr,
    field_serializer,
    field_validator,
)

field_email_address = Annotated[EmailStr, Field(description="The email address associated with the user account.")]
field_password = Annotated[
    SecretStr, Field(description="The password associated with the user account.", min_length=8, max_length=32)
]
field_password_hash = Annotated[str, Field(description="The users hashed password.")]
field_username = Annotated[
    str, Field(description="The username associated with the user account.", min_length=4, max_length=256)
]
field_is_enabled = Annotated[bool, Field(description="Is the user currently active.")]
path_user_id = Annotated[int, Path(description="The unique ID associated with the user account.")]
field_user_id = Annotated[int, Field(description="The unique ID associated with the user account.")]
field_created_at = Annotated[PastDatetime, Field(description="The creation datetime of the user.")]
field_updated_at = Annotated[PastDatetime, Field(description="The last edit datetime of the user.")]
field_profile_picture_url = Annotated[HttpUrl | None, Field(description="The URL for the profile picture of the user.")]
field_scopes = Annotated[list[str], Field(description="A list of scopes the user has.")]
field_role = Annotated[str, Field(description="The users current role.")]


class BaseUser(BaseModel):
    email_address: field_email_address
    username: field_username


class User(BaseUser):
    """
    Basic user details.
    """

    id: field_user_id
    is_enabled: field_is_enabled
    created_at: field_created_at
    updated_at: field_updated_at
    profile_picture_url: field_profile_picture_url
    role: field_role

    @field_serializer("profile_picture_url")
    def serialize_profile_picture_url(self, value: HttpUrl | None, _info):
        return str(value) if value is not None else None

    @field_serializer("created_at")
    def serialize_created_at(self, value: PastDatetime, _info):
        return value.isoformat()

    @field_serializer("updated_at")
    def serialize_updated_at(self, value: PastDatetime, _info):
        return value.isoformat()


class ScopedUser(User):
    """
    User with scopes for security
    """

    scopes: field_scopes
    password_hash: field_password_hash


class NewUser(BaseUser):
    """
    Basic new user details.
    """

    password: field_password

    @field_validator("password")
    @classmethod
    def validate_regex_password(cls, value: SecretStr) -> SecretStr:
        if not check_password_strength(value):
            raise ValueError(
                "Password was not of sufficient strength - Minimum eight characters, at least one letter, one number and one special character"
            )

        return value


class NewUserProcessed(NewUser):
    """
    New User details after processing.
    """

    role: field_role
    profile_picture_url: field_profile_picture_url

    @field_serializer("profile_picture_url")
    def serialize_profile_picture_url(self, value: HttpUrl | None, _info):
        return str(value) if value is not None else None
