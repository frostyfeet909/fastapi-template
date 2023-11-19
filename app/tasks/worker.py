from stores.task_queue import app


@app.task(acks_late=True)
def test_celery() -> str:
    return "hey"
