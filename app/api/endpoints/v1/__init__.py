from config.metadata_config import settings as init_settings

__version__ = "v1.0.0"
__author__ = init_settings.CONTACT_NAME
__license__ = init_settings.LICENSE_NAME
__maintainer__ = init_settings.CONTACT_NAME
__email__ = init_settings.CONTACT_EMAIL

"""
v1 of API endpoints.
"""

import json
import os

from api.endpoints.v1.oauth import router as oauth_router
from config.application_config import settings
from fastapi import FastAPI

from .index import router as index_router
from .user import router as security_router

FILE__openapi_tags = os.path.join(os.path.dirname(os.path.realpath(__file__)), "openapi_tags.json")
PATH__route = "/v1"
PATH__docs = "/docs"

openapi_tags = None
with open(FILE__openapi_tags, "r") as file:
    openapi_tags = json.load(file)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    openapi_tags=openapi_tags,
    version=__version__,
    contact=init_settings.CONTACT,
    license_info=init_settings.LICENSE,
    docs_url=PATH__docs,
)
app.include_router(index_router)
app.include_router(security_router)
app.include_router(oauth_router)

__all__ = ["app", "FILE__openapi_tags", "PATH__route", "PATH__docs"]
