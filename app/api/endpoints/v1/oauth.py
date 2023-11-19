import traceback
from typing import Annotated, cast

from config.application_config import settings
from core import security
from crud import role as role_queries
from crud import user as user_queries
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import ExpiredSignatureError, JWTError, jwt  # type: ignore
from pydantic import SecretStr
from schemas import token
from schemas import user as user_schemas
from sqlalchemy.ext.asyncio import AsyncConnection
from stores import db


def get_scopes() -> dict[str, str]:
    scopes = None
    with db.get_connection() as conn:
        scopes = role_queries.select_scopes(conn)  # noqa
    return {scope["name"]: scope["description"] or "" for scope in scopes}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token", description="Login password flow.", scopes=get_scopes())
router = APIRouter(tags=["users"])


@router.post(
    "/token",
    summary="Login via username and password.",
    response_model=token.Token,
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Incorrect username or password or scope"}},
)
async def login_username_password(
    conn: Annotated[AsyncConnection, Depends(db.depend_async_connection)],
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict:
    """
    Login via username and password.
    """
    form.password = SecretStr(form.password)
    user = await user_queries.async_select_user_by_username_with_scopes(conn, form.username)
    authenticate = user and security.verify_password(form.password, user.password_hash)

    if not authenticate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        user = cast(user_schemas.User, user)
    if any(scope not in user.scopes for scope in form.scopes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect scope",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = user.username
    scopes = form.scopes if form.scopes else user.scopes
    access_token = security.create_access_token(
        data={"sub": sub, "scopes": scopes}  # , **{"user": user.model_dump(exclude={"password_hash", "scopes"})}
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_and_validate_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    conn: Annotated[AsyncConnection, Depends(db.depend_async_connection)],
) -> user_schemas.User:
    """Validate user scope, return user."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    payload = await validate_user(security_scopes, token)

    if username := payload.get("sub"):
        user = await user_queries.async_select_user_by_username(conn, username)
    else:
        user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="User not found.",
            headers={"WWW-Authenticate": authenticate_value},
        )

    return user


async def validate_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Validate user scope, return jwt."""
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.TOKEN_ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired.",
            headers={"WWW-Authenticate": authenticate_value},
        )
    except JWTError:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": authenticate_value},
        )

    token_scopes = set(scopes) if (scopes := payload.get("scopes")) else set()
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions.",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return payload
