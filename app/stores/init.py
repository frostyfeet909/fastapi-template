from stores.db import init as postgres_init
from stores.db.engine import sync_engine


def main():
    if not sync_engine:
        raise ValueError("[!!] A sync engine must be defined for setup.")

    postgres_init.main()


if __name__ == "__main__":
    main()
