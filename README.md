# Weather Data Engineering

A small data engineering project that collects weather data, loads it into Postgres, orchestrates work with Airflow and dbt, and visualizes results with Superset.

This repository contains a Docker Compose setup that runs:

- Postgres (service: `db`) — container `postgres-container` (host port 5000 -> container 5432)
- Airflow (service: `af`) — container `airflow-container` (host port 8000 -> container 8080)
- dbt (service: `dbt`) — container `dbt-container`, project mounted at `dbt/my_project`
- Superset (services: `superset`, `superset-init`, `superset-websocket`) — default host port 8088 (configurable)
- Redis (service: `redis`)

What's in this repo

- `docker-compose.yml` — main Compose file to start the stack
- `airflow/dags/` — Airflow DAGs (e.g. `orchestrator.py`, `dbt_orchestrator.py`)
- `api-requests/` — small scripts to call APIs and insert records (`api_requests.py`, `insert_records.py`)
- `dbt/my_project/` — dbt project (models, macros, tests)
- `postgres/` — initialization SQL and persisted Postgres data (`postgres/airflow_init.sql`, `postgres/data/`)
- `docker/` — helper scripts and superset config used by Superset services

Quick start (Windows - cmd.exe)

Prerequisites

- Docker Desktop (with Docker Compose plugin)
- At least ~4GB RAM available to Docker

Start the entire stack

```cmd
cd "C:\Users\Iftekhar Alam\PycharmProjects\PythonProject\weather-data-eng"
docker compose up -d --build
```

View logs

```cmd
docker compose logs -f af      # follow Airflow logs
docker compose logs -f db     # follow Postgres logs
docker compose logs -f superset
```

Open services in browser

- Airflow web UI: http://localhost:8000
- Superset web UI: http://localhost:8088 (or the port in `docker/.env`)
- Postgres (direct client): localhost:5000 (DB user/credentials from `docker-compose.yml`)

Notes on credentials and initialization

- Postgres credentials (from `docker-compose.yml`):
  - POSTGRES_DB: `db`
  - POSTGRES_USER: `db_user`
  - POSTGRES_PASSWORD: `db_password`
- The Postgres service mounts `postgres/airflow_init.sql` which runs at container init to prepare the DB for Airflow.
- Persistent Postgres data is stored under `./postgres/data` on the host.

Running dbt

The project lives in `dbt/my_project`. The Compose `dbt` service image is `ghcr.io/dbt-labs/dbt-postgres:1.9.latest`.

From the repo root you can run dbt commands via the `dbt` container:

```cmd
docker compose run --rm dbt deps
docker compose run --rm dbt seed
docker compose run --rm dbt run
docker compose run --rm dbt test
```

Airflow

- DAGs are located in `airflow/dags/` and are mounted into the Airflow container at `/opt/airflow/dags`.
- The `af` service command runs `airflow standalone`, which launches a SQLite metadata DB for quick local testing unless you change the database connection.
- To run a Python script inside the Airflow container (for quick debugging):

```cmd
docker compose exec af bash
# inside the container
python /opt/airflow/api-requests/api_requests.py
```

API scripts and inserting records

- `api-requests/api_requests.py` — script to call external API(s) and retrieve weather data.
- `api-requests/insert_records.py` — helper to insert data into Postgres.

You can either run these inside the `af` container or execute locally with a Python environment if you install dependencies.

Superset

- Superset config and bootstrap scripts are in `docker/` and the Superset services are defined in `docker-compose.yml`.
- Environment overrides are supported via `docker/.env` (required by the Compose file) and `docker/.env-local` (optional).

Troubleshooting

- If the Postgres container fails to start because of existing data, stop the stack and move/backup `postgres/data`.
- Common fixes:
  - Recreate containers: `docker compose down && docker compose up -d --build`
  - Follow logs for a single service: `docker compose logs -f <service>`

Development notes and next steps

- Add instructions for any Python dependencies (requirements.txt) for the scripts in `api-requests/` if you want to run them locally.
- Consider adding a `Makefile` or small wrapper scripts to simplify dbt and Airflow commands.
- Add CI checks for dbt tests and linting for Python code.


