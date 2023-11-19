import sqlalchemy
import sqlalchemy.ext.asyncio as sqlalchemy_async
from config.postgres_config import settings
from stores.db.util import convert_pydantic_to_sqlalchemy_uri

async_engine = None
sync_engine = None

if settings.SYNC_URI:
    uri = convert_pydantic_to_sqlalchemy_uri(settings.SYNC_URI)
    try:
        sync_engine = sqlalchemy.create_engine(uri, pool_pre_ping=True, pool_recycle=3600)
        print("[+] Created sync sync_engine on {0}".format(uri))
    except ModuleNotFoundError:
        pass

if settings.ASYNC_URI:
    uri = convert_pydantic_to_sqlalchemy_uri(settings.ASYNC_URI)
    try:
        async_engine = sqlalchemy_async.create_async_engine(uri, pool_pre_ping=True, pool_recycle=3600)
        print("[+] Created async sync_engine on {0}".format(uri))
    except ModuleNotFoundError:
        pass
