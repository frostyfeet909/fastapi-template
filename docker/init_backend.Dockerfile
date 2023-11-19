FROM python:3.11

ENV INSTALL_PATH=/init-backend
ENV PYTHONPATH=$INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN pip install --no-cache-dir poetry==1.6.1
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock $INSTALL_PATH/
RUN poetry install --no-root --no-directory --no-ansi --only main,init --directory $INSTALL_PATH

COPY /app $INSTALL_PATH

CMD [ "python3", "stores/init.py" ]