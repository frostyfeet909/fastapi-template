import re
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from config.application_config import settings
from jose import JWTError, jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore

if TYPE_CHECKING:
    from pydantic import SecretStr

PATTERN__password_1 = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
PATTERN__password_2 = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
PATTERN__password_3 = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
PATTERN__password_4 = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
PWD__context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    """Create access token with exp set, using data."""
    decoded = data.copy()

    decoded["exp"] = decoded.get("exp", datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRES_MINUTES))
    encoded = jwt.encode(decoded, settings.SECRET_KEY.get_secret_value(), algorithm=settings.TOKEN_ALGORITHM)
    return encoded


def get_sub(token: str) -> str | None:
    """Get user_id from token."""
    user_id = None
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.TOKEN_ALGORITHM],
            options={"verify_exp": False},
        )
        user_id = payload.get("sub")
    except JWTError:
        pass

    return user_id


def hash_password(password: "SecretStr") -> str:
    """Get hashed password."""
    return PWD__context.hash(password.get_secret_value())


def verify_password(plain_password: "SecretStr", hashed_password: str) -> bool:
    """Verify hashed password vs plain password."""
    return PWD__context.verify(plain_password.get_secret_value(), hashed_password)


def check_password_strength(password: "SecretStr", level: int = 2) -> bool:
    """
    1.
    Minimum eight characters, at least one letter and one number:

    2.
    Minimum eight characters, at least one letter, one number and one special character:

    3.
    Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:

    4.
    Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    """

    if level == 1:
        return PATTERN__password_1.search(password.get_secret_value()) is not None
    elif level == 2:
        return PATTERN__password_2.search(password.get_secret_value()) is not None
    elif level == 3:
        return PATTERN__password_3.search(password.get_secret_value()) is not None
    elif level == 4:
        return PATTERN__password_4.search(password.get_secret_value()) is not None
    else:
        raise NotImplementedError("Password strength level not implemented.")
