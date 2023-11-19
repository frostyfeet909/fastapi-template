import os
import traceback
from os import path
from typing import TYPE_CHECKING

from config.postgres_config import settings
from sqlalchemy import URL
from sqlalchemy_utils import functions as sqlalchemy_utils
from stores import db
from stores.db.util import convert_pydantic_to_sqlalchemy_uri

if TYPE_CHECKING:
    from typing import Iterator, Union

    from pydantic import PostgresDsn

DIR__migrations = path.abspath(path.join(__file__, "..", "migrations"))
EXT__sql = ".sql"


def create(url: "Union[PostgresDsn, URL, str]" = settings.SYNC_URI):
    if not isinstance(url, URL):
        url = convert_pydantic_to_sqlalchemy_uri(url)
    print("[+] Creating {0}".format(url))
    sqlalchemy_utils.create_database(url)


def drop(url: "Union[PostgresDsn, URL, str]" = settings.SYNC_URI):
    if not isinstance(url, URL):
        url = convert_pydantic_to_sqlalchemy_uri(url)
    print("[-] Dropping {0}".format(url))
    sqlalchemy_utils.drop_database(url)


def exists(url: "Union[PostgresDsn, URL, str]" = settings.SYNC_URI) -> bool:
    if not isinstance(url, URL):
        url = convert_pydantic_to_sqlalchemy_uri(url)
    return sqlalchemy_utils.database_exists(url)


def get_migrations() -> "Iterator[str]":
    migrations = sorted(
        [
            path.join(DIR__migrations, migration)
            for migration in os.listdir(DIR__migrations)
            if path.isdir(path.join(DIR__migrations, migration))
        ]
    )

    for migration in migrations:
        files = sorted(
            [
                path.join(migration, file)
                for file in os.listdir(migration)
                if path.isfile(path.join(migration, file)) and file.endswith(EXT__sql)
            ]
        )
        for file_name in files:
            with open(file_name) as file:
                if content := file.read():
                    print("[+]    - {0}".format(file_name))
                    yield content


def migrate():
    print("[*] Executing Migrations:")
    with db.get_connection() as conn:
        for query in get_migrations():
            db.execute_query(conn, query)

        conn.commit()
        print("Finished!")


def main():
    if exists():
        drop()

    create()

    try:
        migrate()
        print("[*] Completed")
    except Exception as ex:
        print("[!!] Could not init")
        traceback.print_exc()

        raise ex


if __name__ == "__main__":
    main()
