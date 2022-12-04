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
RUN apt-get update && apt-get install -y curl -y
ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=$POETRY_HOME/bin:$PATH
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY parquet_web_socket ./parquet_web_socket
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-ansi

# -------------------------------------------------------------------------------------------------------------------- #

FROM python:3.10.3-slim-buster as app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80
COPY --from=dependencies /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/
WORKDIR /app
COPY parquet_web_socket ./parquet_web_socket
COPY server.py ./server.py
CMD ["python", "server.py"]
