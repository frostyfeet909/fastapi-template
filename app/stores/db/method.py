import traceback
from contextlib import contextmanager
from typing import TYPE_CHECKING, cast

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import CursorResult
from stores.db.engine import sync_engine
from stores.db.util import format_output

if TYPE_CHECKING:
    from typing import Iterator, Union

    from sqlalchemy import Connection

QUERY__limit_single = " LIMIT 1"


@contextmanager
def get_connection() -> "Iterator[Connection]":
    conn = sync_engine.connect()
    try:
        yield conn
    except Exception as ex:
        conn.rollback()
        traceback.print_exc()
        print("[!] Rolled back")
        raise ex
    finally:
        conn.close()


def depend_connection() -> "Iterator[Connection]":
    conn = sync_engine.connect()
    try:
        yield conn
    except Exception as ex:
        conn.rollback()
        print("[!] Rolled back")
        raise ex
    finally:
        conn.close()


def execute(
    conn: "Connection",
    query: str,
    params: dict | list[dict] | BaseModel | None = None,
    result: bool = False,
    commit: bool = False,
) -> "Union[CursorResult, None]":
    """Execute query with params, with or without result.
    Args:
        conn (Connection): Connection to use
        query (str): Query to execute
        params (dict | list[dict] | BaseModel | None, optional): Parameters to pass to query. Defaults to None.
        result (bool, optional): Whether to return result. Defaults to False.
        commit (bool, optional): Whether to commit. Defaults to False.
    Returns:
        Union[CursorResult, None]: Result of query if result=True, else None
    """
    if isinstance(params, BaseModel):
        params = params.model_dump()  # type: ignore

    cur = conn.execute(sqlalchemy.text(query), params)

    if commit:
        conn.commit()

    if result:
        return cur
    else:
        cur.close()


def execute_query(
    conn: "Connection", query: str, params: dict | list[dict] | BaseModel | None = None, commit: bool = False
) -> None:
    """Execute query with params, no result"""
    execute(conn, query, params, result=False, commit=commit)


def execute_query_result(
    conn: "Connection",
    query: str,
    params: dict | list[dict] | BaseModel | None = None,
    commit: bool = False,
    return_list: bool = True,
) -> dict | list[dict]:
    """Execute query with params, with result"""
    result = cast(CursorResult, execute(conn, query, params, result=True, commit=commit))
    keys = list(result.keys())
    values = result.fetchall()

    return format_output(keys, values, return_list=return_list)


def execute_query_result_single(
    conn: "Connection",
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
    result = cast(CursorResult, execute(conn, query, params, result=True, commit=commit))
    keys = list(result.keys())
    values = result.fetchone()

    if fail_on_multiple and (not values or result.fetchone()):
        result.close()
        raise ValueError("Incorrect number of rows returned")
    else:
        result.close()

    return cast(dict, format_output(keys, values, single=True))
