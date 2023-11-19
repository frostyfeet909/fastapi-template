from config.metadata_config import settings as _init_settings

__version__ = "v1.0.0"
__author__ = _init_settings.CONTACT_NAME
__license__ = _init_settings.LICENSE_NAME
__maintainer__ = _init_settings.CONTACT_NAME
__email__ = _init_settings.CONTACT_EMAIL

"""
db funcs.
"""

from .method import (
    depend_connection,
    execute_query,
    execute_query_result,
    execute_query_result_single,
    get_connection,
)
from .method_async import (
    depend_async_connection,
    execute_async_query,
    execute_async_query_result,
    execute_async_query_result_single,
    get_async_connection,
)
from .util import pivot
