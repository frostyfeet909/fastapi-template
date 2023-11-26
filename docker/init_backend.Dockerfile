FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    POSTGRES_NEED_SYNC_URI=true \
    REDIS_NEED_INSECURE_URI=true \
    INSTALL_PATH=/init-backend
ENV PYTHONPATH=$INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY pyproject.toml poetry.lock $INSTALL_PATH/

RUN pip3 install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-directory --no-ansi --only main,init --directory $INSTALL_PATH

COPY /app $INSTALL_PATH

CMD [ "python3", "stores/init.py" ]