from config.metadata_config import settings as init_settings

__version__ = "v1.0.0"
__author__ = init_settings.CONTACT_NAME
__license__ = init_settings.LICENSE_NAME
__maintainer__ = init_settings.CONTACT_NAME
__email__ = init_settings.CONTACT_EMAIL

"""
v1 of API endpoints.
"""

import os

from config.application_config import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .index import router as index_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=__version__,
    contact=init_settings.CONTACT,
    license_info=init_settings.LICENSE,
    docs_url=None,
    redoc_url=None,
)

DIR__static = os.path.abspath(os.path.join(__file__, "..", "static"))
app.mount("/static", StaticFiles(directory=DIR__static), name="static")

app.include_router(index_router)

__all__ = ["app"]
