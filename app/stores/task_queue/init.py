from config.redis_config import settings as redis_settings
from stores.task_queue.engine import client


def change_redis_password():
    print("[*] Changing redis password")
    response = client.execute_command("CONFIG SET", "requirepass", redis_settings.PASSWORD.get_secret_value())
    if not response:
        raise RuntimeError("[!!] Failed to change redis password")


def main():
    print("[*] Starting redis init")
    change_redis_password()

    print("[*] Completed")


if __name__ == "__main__":
    main()
