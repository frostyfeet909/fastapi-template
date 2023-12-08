from typing import Any

from fastapi import HTTPException, status

RESPONSES__validation = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Either the token has expired or the credentials are not valid. Please re-authenticate."
    },
    status.HTTP_410_GONE: {"description": "Current user not found. Please re-authenticate."},
}


def get_or_404(
    obj: Any,
    object_type: str | None = None,
    status_code: int = status.HTTP_404_NOT_FOUND,
    detail: str = "{object_type} not found.",
) -> Any:
    """Return obj if obj else raise exception."""
    if obj:
        return obj
    else:
        raise HTTPException(
            status_code=status_code,
            detail=(detail.format(object_type=object_type) if object_type else detail),
        )


"""
async def log_request(utc_time: datetime = None, api_name: str = settings.PROJECT_NAME, operation_name: str = None,
                      host_name: str = settings.PROJECT_URL, http_method: str = None, path: str = None, resource_id: int = None,
                      client_application_name: str = None, user_id: UUID = None, status_code: int = None, ms_taken: int = None,
                      ms_threshold: int = None, error_code: int = None, error_id: UUID = None, correlation_id: UUID = None,
                      session_id: UUID = None) -> None:
    # https://authguidance.com/effective-api-logging/
    async with get_async_connection() as conn:
        await async_insert_log(conn, utc_time, api_name, operation_name, host_name, http_method, path, resource_id, client_application_name,
                               user_id, status_code, ms_taken, ms_threshold, error_code, error_id, correlation_id, session_id)
"""
