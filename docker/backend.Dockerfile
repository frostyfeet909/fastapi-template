FROM tiangolo/uvicorn-gunicorn:python3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    POSTGRES_NEED_ASYNC_URI=true \
    POSTGRES_NEED_SYNC_URI=true \
    REDIS_NEED_CELERY_BROKER_URI=true \
    INSTALL_PATH=/backend
ENV PYTHONPATH=$INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY pyproject.toml poetry.lock $INSTALL_PATH/

RUN pip3 install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-directory --no-ansi --only main,backend --directory $INSTALL_PATH

COPY /app $INSTALL_PATH/
