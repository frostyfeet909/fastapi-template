FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    REDIS_NEED_CELERY_BROKER_URI=true \
    INSTALL_PATH=/flower
ENV PYTHONPATH=$INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY pyproject.toml poetry.lock $INSTALL_PATH/

RUN pip3 install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-directory --no-ansi --only main,worker,flower --directory $INSTALL_PATH

COPY /app $INSTALL_PATH
RUN echo "${REDIS_HOST:-redis}://:${REDIS_PASSWORD}@redis:${REDIS_PORT:-6379}"
CMD [ "celery", "-A", "stores.task_queue.app", "flower", "--port=5555" ]