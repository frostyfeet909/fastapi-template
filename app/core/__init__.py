from config.metadata_config import settings as init_settings

__version__ = "v1.0.0"
__author__ = init_settings.CONTACT_NAME
__license__ = init_settings.LICENSE_NAME
__maintainer__ = init_settings.CONTACT_NAME
__email__ = init_settings.CONTACT_EMAIL

"""
Core funcs such as security.
"""

from .security import (
    check_password_strength,
    create_access_token,
    get_sub,
    hash_password,
    verify_password,
)
