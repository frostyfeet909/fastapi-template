from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import CursorResult
from stores.db.engine import async_engine
from stores.db.util import format_output

if TYPE_CHECKING:
    from typing import AsyncIterator, Union

    from sqlalchemy.ext.asyncio import AsyncConnection

QUERY__limit_single = " LIMIT 1"


@asynccontextmanager
async def get_async_connection() -> "AsyncIterator[AsyncConnection]":
    conn = await async_engine.connect()
    try:
        yield conn
    except Exception as ex:
        await conn.rollback()
        print("[!] Rolled back with exception {0}".format(ex))
        raise ex
    finally:
        await conn.close()


async def depend_async_connection() -> "AsyncIterator[AsyncConnection]":
    conn = await async_engine.connect()
    try:
        yield conn
    except Exception as ex:
        await conn.rollback()
        print("[!] Rolled back with exception {0}".format(ex))
        raise ex
    finally:
        await conn.close()


async def execute_async(
    conn: "AsyncConnection",
    query: str,
    params: dict | list[dict] | BaseModel | None = None,
    result: bool = False,
    commit: bool = False,
) -> "Union[CursorResult, None]":
    if isinstance(params, BaseModel):
        params = params.model_dump()  # type: ignore

    cur = await conn.execute(sqlalchemy.text(query), params)

    if commit:
        await conn.commit()

    if result:
        return cur
    else:
        cur.close()


async def execute_async_query(
    conn: "AsyncConnection", query: str, params: dict | list[dict] | BaseModel | None = None, commit: bool = False
) -> None:
    """Execute query with params, no result"""
    await execute_async(conn, query, params, result=False, commit=commit)


async def execute_async_query_result(
    conn: "AsyncConnection",
    query: str,
    params: dict | list[dict] | BaseModel | None = None,
    commit: bool = False,
    return_list: bool = True,
) -> dict | list[dict]:
    """Execute query with params, with result"""
    result = cast(CursorResult, await execute_async(conn, query, params, result=True, commit=commit))
    keys = list(result.keys())
    values = result.fetchall()

    return format_output(keys, values, return_list=return_list)


async def execute_async_query_result_single(
    conn: "AsyncConnection",
    query: str,
    params: dict | list[dict] | BaseModel | None = None,
    commit: bool = False,
    fail_on_multiple: bool = False,
    query_limit: bool = False,
) -> dict:
    """Execute query with params, with single result"""
    query = (
        query + QUERY__limit_single
        if query_limit and not fail_on_multiple and not query.endswith(QUERY__limit_single)
        else query
    )
    result = cast(CursorResult, await execute_async(conn, query, params, result=True, commit=commit))
    keys = list(result.keys())
    values = result.fetchone()

    if fail_on_multiple and (not values or result.fetchone()):
        result.close()
        raise ValueError("Incorrect number of rows returned")

    result.close()

    return cast(dict, format_output(keys, values, single=True))
