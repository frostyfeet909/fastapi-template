from typing import TYPE_CHECKING

from schemas import user as user_schema
from stores import db

if TYPE_CHECKING:
    from typing import Union

    from pydantic import EmailStr
    from sqlalchemy.ext.asyncio import AsyncConnection

QUERY_INS__user = """INSERT INTO "user" (email_address, username, password_hash, role, profile_picture_url) VALUES (:email_address, :username, :password_hash, :role, :profile_picture_url) RETURNING *;"""
QUERY_SEL__user_by_username_with_scopes = """
SELECT u.*,
       (SELECT rs.scopes
        FROM role_scopes rs
        WHERE rs.role = u.role) AS scopes
FROM "user" u
WHERE u.username = :username
LIMIT 1
"""
QUERY_SEL__user_by_email_address_with_scopes = """
SELECT u.*,
       (SELECT rs.scopes
        FROM role_scopes rs
        WHERE rs.role = u.role) AS scopes
FROM "user" u
WHERE u.email_address = :email_address
LIMIT 1
"""
QUERY_SEL__user = """
SELECT u.id,
       email_address,
       username,
       profile_picture_url,
       role,
       is_enabled,
       created_at,
       updated_at
FROM "user" u
WHERE u.id = :id
LIMIT 1
"""
QUERY_SEL__user_by_username = """
SELECT u.id,
       email_address,
       username,
       profile_picture_url,
       role,
       is_enabled,
       created_at,
       updated_at
FROM "user" u
WHERE u.username = :username
LIMIT 1
"""
QUERY_SEL__users = """
SELECT u.id,
       email_address,
       username,
       profile_picture_url,
       role,
       is_enabled,
       created_at,
       updated_at
FROM "user" u
"""
QUERY_SEL__username_exists = """SELECT EXISTS(SELECT 1 FROM "user" u WHERE u.username = :username) as result"""
QUERY_SEL__email_address_exists = (
    """SELECT EXISTS(SELECT 1 FROM "user" u WHERE u.email_address = :email_address) as result"""
)


async def async_select_user_by_username_with_scopes(
    conn: "AsyncConnection", username: str
) -> user_schema.ScopedUser | None:
    """Select user from username if exists."""
    user = await db.execute_async_query_result_single(
        conn, QUERY_SEL__user_by_username_with_scopes, {"username": username}
    )

    if user:
        user = user_schema.ScopedUser(**user)

    return user


async def async_select_user_by_email_address_with_scopes(
    conn: "AsyncConnection", email_address: "Union[str, EmailStr]"
) -> user_schema.ScopedUser | None:
    """Select user from username if exists."""
    user = await db.execute_async_query_result_single(
        conn, QUERY_SEL__user_by_email_address_with_scopes, {"email_address": str(email_address)}
    )

    if user:
        user = user_schema.ScopedUser(**user)

    return user


async def async_select_user(conn: "AsyncConnection", id: int) -> user_schema.User:
    """Select user from username."""
    user = await db.execute_async_query_result_single(conn, QUERY_SEL__user, {"id": id})
    user = user_schema.User(**user)
    return user


async def async_select_user_by_username(conn: "AsyncConnection", username: str) -> user_schema.User:
    """Select user from username."""
    user = await db.execute_async_query_result_single(conn, QUERY_SEL__user_by_username, {"username": username})
    user = user_schema.User(**user)
    return user


async def async_select_users(conn: "AsyncConnection") -> list[user_schema.User]:
    """Select users."""
    users = await db.execute_async_query_result(conn, QUERY_SEL__users)
    users = [user_schema.User(**user) for user in users]
    return users


async def async_select_exists_email_address(conn: "AsyncConnection", user: user_schema.NewUser) -> bool:
    email_exists = await db.execute_async_query_result_single(
        conn, QUERY_SEL__email_address_exists, {"email_address": user.email_address}
    )
    return email_exists["result"]


async def async_select_exists_username(conn: "AsyncConnection", user: user_schema.NewUser) -> bool:
    username_exists = await db.execute_async_query_result_single(
        conn, QUERY_SEL__username_exists, {"username": user.username}
    )
    return username_exists["result"]


async def async_insert_user(conn: "AsyncConnection", user_details: user_schema.NewUserProcessed) -> user_schema.User:
    """Insert user. Will not fail gracefully - check duplicates first"""
    user = await db.execute_async_query_result_single(conn, QUERY_INS__user, user_details, commit=True)
    user = user_schema.User(**user)
    return user
