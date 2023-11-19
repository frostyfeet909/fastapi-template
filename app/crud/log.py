from typing import TYPE_CHECKING

from stores import db

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncConnection

QUERY_INS__log = """
    INSERT INTO log (utc_time, api_name, operation_name, host_name, http_method, path, resource_id, client_application_name, user_id, status_code, ms_taken, ms_threshold, error_code, error_id, correlation_id, session_id) VALUES 
    (:utc_time, :api_name, :operation_name, :host_name, :http_method, :path, :resource_id, :client_application_name, :user_id, :status_code, :ms_taken, :ms_threshold, :error_code, :error_id, :correlation_id, :session_id)
    """


async def async_insert_log(
    conn: AsyncConnection,
    utc_time: datetime,
    api_name: str,
    operation_name: str,
    host_name: str,
    http_method: str,
    path: str,
    resource_id: int,
    client_application_name: str,
    user_id: UUID,
    status_code: int,
    ms_taken: int,
    ms_threshold: int,
    error_code: int,
    error_id: UUID,
    correlation_id: UUID,
    session_id: UUID,
) -> None:
    """Set role in conn to username"""
    query = {
        "utc_time": utc_time,
        "api_name": api_name,
        "operation_name": operation_name,
        "host_name": host_name,
        "http_method": http_method,
        "path": path,
        "resource_id": resource_id,
        "client_application_name": client_application_name,
        "user_id": user_id,
        "status_code": status_code,
        "ms_taken": ms_taken,
        "ms_threshold": ms_threshold,
        "error_code": error_code,
        "error_id": error_id,
        "correlation_id": correlation_id,
        "session_id": session_id,
    }
    await db.execute_async_query(conn, QUERY_INS__log, query, commit=True)
