# Parquet WebSocket

WebSocket server which replays historical trade data in chronological order from the given parquet file.

## How to run

## Docker
Prerequisites:
* Docker

Steps:
* Put parquet file into the `./data` directory
* Set `PARQUET_FILE` environment variable to the needed file in `docker-compose.yml` with the `/app/data` prefix (e. g. `/app/data/trades_sample.parquet`)
* Run `docker-compose up`
* Connect to `ws://localhost:4000/ws` with external ws client

## Local set up
Prerequisites:
* Python >= 3.10
* Poetry >= 1.0.0

Steps:
* Run `poetry shell`
* Run `poetry install`
* Put parquet file into the `./data` directory
* Set `PARQUET_FILE` environment variable to the needed file (e. g. `./data/trades_sample.parquet`)
* Run `python server.py`
* Connect to `ws://localhost:{PORT}/ws` with external ws client

## Environment variables
Alternatively you can set up additional environment variables

| Variable      | Description                    | Default |
|---------------|--------------------------------|---------|
| PARQUET_FILE  | Path to the parquet file       | -       |
| PORT          | Server port                    | 80      |
| LOG_LEVEL     | Log level [10, 20, 30, 40, 50] | 20      |
