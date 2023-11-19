from typing import Annotated

from api.dependencies import RESPONSES__validation, get_or_404
from api.endpoints.v1.oauth import get_and_validate_user, validate_user
from core import gravitar
from crud import role as role_queries
from crud import user as user_queries
from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from schemas import user as user_schema
from sqlalchemy.ext.asyncio import AsyncConnection
from stores import db

router = APIRouter(prefix="/users", tags=["users"])

RESPONSES__user = {status.HTTP_404_NOT_FOUND: {"description": "User not found."}}


@router.get(
    "/me",
    summary="Get current user.",
    response_model=user_schema.User,
    responses={**RESPONSES__validation, **RESPONSES__user},
)
async def get_me(
    user: Annotated[user_schema.User, Security(get_and_validate_user, scopes=["user.me"])]
) -> user_schema.User:
    """
    Get details on the current user.\n
    - **email address**
    - **username**
    """
    return user


@router.get(
    "/{id}",
    summary="Get user.",
    response_model=user_schema.User,
    responses={**RESPONSES__validation, **RESPONSES__user},
)
async def get_user(
    conn: Annotated[AsyncConnection, Depends(db.depend_async_connection)],
    user_id: user_schema.path_user_id,
    _: Annotated[user_schema.User, Security(validate_user)],
) -> dict:
    """
    Get details on the user.\n
    - **email address**
    - **username**
    """
    user = await user_queries.async_select_user(conn, user_id)
    return get_or_404(user, "User")


@router.get("/", summary="Get users.", response_model=list[user_schema.User], responses={**RESPONSES__validation})
async def get_users(
    conn: Annotated[AsyncConnection, Depends(db.depend_async_connection)],
    _: Annotated[user_schema.User, Security(validate_user)],
) -> list[user_schema.User]:
    """
    Get details on the user.\n
    - **email address**
    - **username**
    """
    user = await user_queries.async_select_users(conn)
    return user


@router.post(
    "/",
    summary="Create user.",
    response_model=user_schema.User,
    status_code=status.HTTP_201_CREATED,
    responses={
        **RESPONSES__validation,
        status.HTTP_409_CONFLICT: {"description": "The email address or username already exists for another account."},
    },
)
async def post_user(
    response: Response,
    conn: Annotated[AsyncConnection, Depends(db.depend_async_connection)],
    user: user_schema.NewUser,
) -> user_schema.User:
    """
    Create user with the following details.
    """
    # Duplicate Validation
    email_exists = await user_queries.async_select_exists_email_address(conn, user)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="The email address already exists for another account."
        )
    username_exists = await user_queries.async_select_exists_username(conn, user)
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="The username already exists for another account."
        )

    profile_picture_url = gravitar.generate(user.email_address)
    role = await role_queries.async_select_default_role_name(conn)

    user = user_schema.NewUserProcessed(**user.model_dump(), profile_picture_url=profile_picture_url, role=role)

    user = await user_queries.async_insert_user(conn, user)
    response.headers["Location"] = router.prefix + "/{user_id}".format(user_id=user.id)
    return user
