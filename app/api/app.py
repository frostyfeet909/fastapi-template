import traceback
from contextlib import asynccontextmanager
from datetime import datetime
from os import path
from typing import Callable, cast

from api.endpoints import v1
from core import security
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from stores import db
from stores.db import engine

DIR__static = path.abspath(path.join(__file__, "..", "static"))
origins = [
    "http://127.0.0.1:5173",  # TODO: env?
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    try:
        async with db.get_async_connection() as conn:
            res = await db.execute_async_query_result_single(conn, "SELECT 1 as result;")

        if res.get("result") == 1:
            print("[+] Async connection is functioning")
        else:
            print("[!] Check the async connection", res)
    except:
        print("[!!] Async connction was not setup!")
        traceback.print_exc()

    # Only needed for scopes
    engine.dispose_sync_engine()

    yield

    # shutdown
    try:
        engine.dispose_sync_engine()
    except:
        pass
    try:
        await engine.dispose_async_engine()
    except:
        pass


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

# Mount API Version
app.mount(v1.PATH__route, v1.app)
app.mount("/", v1.app)  # Latest version

# Mount Files
app.mount("/static", StaticFiles(directory=DIR__static), name="static")

# Mount Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_request_middleware(request: Request, call_next: Callable[[Request], Response]) -> Response:
    """Log request."""
    start_time = datetime.utcnow()

    response = await call_next(request)
    response = cast(Response, response)

    process_time = datetime.utcnow() - start_time
    user_id = (
        security.get_sub(token)
        if (token := response.headers.get("Authorization") or request.headers.get("Authorization"))
        else None
    )
    print("{0} took {1}".format(user_id, process_time))
    """
    await log_request(utc_time=start_time, ms_taken=process_time.microseconds, http_method=request.method, status_code=response.status_code,
                      path="/" + str(request.url).removeprefix(str(request.base_url)), client_application_name=str(request.base_url),
                      user_id=user_id)
    """
    return response
