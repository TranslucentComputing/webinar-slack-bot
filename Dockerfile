# Dockerfile for a Python application
# Author: Patryk Golabek
# Copyright: Translucent Computing Inc. 2023

# Define the Python version to use at build time. Default is set to 3.9-slim
ARG PYTHON_VERSION=3.9-slim

# Use the Python version as defined in PYTHON_VERSION
FROM python:${PYTHON_VERSION} AS builder

LABEL maintainer="Patryk Golabek <patryk@translucentcomputing.com>"

# environment variable
ENV APP=/app \
    PYTHONPATH="/app:$PYTHONPATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH=/root/.local/bin:$POETRY_HOME/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends tini=0.19.0-1 && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir $APP

WORKDIR $APP

# Install the requirements using pip.
RUN python3 -m pip install --upgrade pip setuptools && python3 -m pip install poetry

# Copying Poetry configuration files before copying the entire application optimizes caching
COPY poetry.lock pyproject.toml ./

# Install dependencies using Poetry
RUN poetry install --no-root --only main

# --- New Stage: Final Image ---

FROM python:${PYTHON_VERSION}

# Non-root user for improved security
# UID/GID are set to a high number to avoid conflicts and security issues
ARG user=nonroot
ARG group=nonroot
ARG uid=10001
ARG gid=10000

ENV USER=${user} \
    HOME=/home/${user} \
    APP=${HOME}/app \
    PATH=${HOME}/.local/bin:$PATH \
    PYTHONUSERBASE=${HOME}/.local \
    HOST=0.0.0.0 \
    LOG_LEVEL=debug \
    LOG_PATH=logging.json

ARG PORT=3000
ENV PORT $PORT

# Copy pip dependencies into a directory accessible to the non-root user
COPY --from=builder /root/.local ${HOME}/.local

# Copy Poetry installation
COPY --from=builder $POETRY_HOME $POETRY_HOME

# Setup non-root user and app directory
RUN groupadd -r ${group} -g ${gid} && \
    useradd -u ${uid} -l -r -g ${group} -s /bin/bash -c "Docker image user" ${user} && \
    mkdir -p ${APP} && \
    chown -R ${user}:${group} ${APP} && \
    chown -R ${user}:${group} /home/${user}/.local

WORKDIR ${APP}

# Copy the rest of the code.
COPY --chown=${user}:${group} . .

# Switch to the non-root user
USER ${uid}:${gid}

# Define the port number to expose at build time.
EXPOSE $PORT

# Copy tini from builder stage
COPY --from=builder /usr/bin/tini /usr/bin/tini
# Use tini as the entry point, handling signals and zombie processes.
ENTRYPOINT ["/usr/bin/tini", "--"]

# The command to run the app when the container is started.
CMD python3 -m uvicorn run:application --workers 1 --host ${HOST} --port ${PORT} --log-config ${LOG_PATH} --log-level ${LOG_LEVEL} --access-log --proxy-headers
