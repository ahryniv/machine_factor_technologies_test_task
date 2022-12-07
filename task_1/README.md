# Task 1

!!!!!!!!!!!!!!!!!!!!!!!!
TASK 1.2 IS NOT FINISHED. I DIDN'T FIND A WAY HOW TO RUN BATCH OF 20,000 RECORDS IN 30 SECONDS

## How to run

## Docker
Prerequisites:
* Docker

Steps:
* Run `docker-compose up`

## Local set up
Prerequisites:
* Python >= 3.10
* Poetry >= 1.0.0
* PostgreSQL

Steps:
* Run `poetry shell`
* Run `poetry install`
* Set environment variables 
* Run `alembic upgrade heads`
* Run `python task_1_1.py`
* Run `python task_1_2.py`

### Check code
* Run `flake8`
* Run `mypy src`

## Environment variables
Alternatively you can set up additional environment variables

| Variable           | Description         | Default   |
|--------------------|---------------------|-----------|
| POSTGRES_USER      | PostgreSQL user     | postgres  |
| POSTGRES_PASSWORD  | PostgreSQL password | ""        |
| POSTGRES_DB        | PostgreSQL DB name  | posgres   |
| POSTGRES_HOSTNAME  | PostgreSQL host     | localhost |
| POSTGRES_PORT      | PostgreSQL port     | 20        |
