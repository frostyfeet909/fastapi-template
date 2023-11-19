from typing import TYPE_CHECKING, cast

from stores import db

if TYPE_CHECKING:
    from sqlalchemy import Connection
    from sqlalchemy.ext.asyncio import AsyncConnection

QUERY_SEL__default_role_name = """SELECT r.name FROM role r WHERE r.is_default IS TRUE LIMIT 1"""
QUERY_SEL__scopes = """SELECT s.name, s.description FROM scope s"""


async def async_select_default_role_name(conn: "AsyncConnection") -> str:
    role = await db.execute_async_query_result_single(conn, QUERY_SEL__default_role_name)
    return role["name"]


def select_scopes(conn: "Connection") -> list[dict]:
    role = db.execute_query_result(conn, QUERY_SEL__scopes)
    return cast(list[dict], role)
