import sys

from stores.db import init as postgres_init
from stores.db.engine import sync_engine
from stores.task_queue import init as redis_init


def main():
    if not sync_engine:
        raise ValueError("[!!] A sync engine must be defined for setup.")

    postgres_init.main()
    redis_init.main()
    sys.exit(0)


if __name__ == "__main__":
    main()
