# Stage 1: Build stage
FROM python:3.11 AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    INSTALL_PATH=/init-backend
ENV PYTHONPATH=$INSTALL_PATH

# Set the working directory
WORKDIR $INSTALL_PATH

# Copy only the dependency files
COPY pyproject.toml poetry.lock $INSTALL_PATH/

# Install poetry and project dependencies without creating a virtual environment
RUN pip3 install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-directory --no-ansi --only main,init --directory $INSTALL_PATH

# Stage 2: Production stage
FROM build AS production

# Copy the project dependencies from the build stage
ENV PYTHONDONTWRITEBYTECODE=1 \
    POSTGRES_NEED_SYNC_URI=true \
    REDIS_NEED_INSECURE_URI=true \
    INSTALL_PATH=/init-backend
ENV PYTHONPATH=$INSTALL_PATH

# Copy your application code
COPY /app $INSTALL_PATH

# Set the working directory
WORKDIR $INSTALL_PATH

# Set the command to run your application
CMD [ "python3", "stores/init.py" ]
