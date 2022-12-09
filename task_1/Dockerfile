FROM python:3.10.3-slim-buster as dependencies
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.2.2 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80
RUN apt-get update && apt-get install -y curl git gcc libpq-dev -y
ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=$POETRY_HOME/bin:$PATH
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY src ./src
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi

# -------------------------------------------------------------------------------------------------------------------- #


FROM python:3.10.3-slim-buster as build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80
RUN apt-get update && apt-get install libpq-dev -y --no-install-recommends \
       && rm -rf /var/lib/apt/lists/*
COPY --from=dependencies /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/
WORKDIR /app
COPY src ./src
COPY run_task_1_1.py ./run_task_1_1.py
COPY run_task_1_2.py ./run_task_1_2.py
COPY alembic.ini ./alembic.ini
COPY src/scripts/cron-docker-entrypoint.sh ./cron-docker-entrypoint.sh
RUN chmod +x ./cron-docker-entrypoint.sh
CMD ["sh", "cron-docker-entrypoint.sh"]
