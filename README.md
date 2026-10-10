# Sales Data Pipeline

ELT pipeline for sales data: CSV -> PostgreSQL, with validation, raw layer, SQL transform, and Parquet snapshot.

## Architecture

data/sales.csv -> validation -> raw_sales (append-only) -> SQL transform -> sales (upsert, idempotent)
Also: Parquet snapshot in data/processed. Tracking in pipeline_runs and logs/pipeline.log.

## Run

    docker compose up -d postgres
    docker compose run --rm pipeline

Requires a .env file with DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD (never committed).

## Test

    python -m pytest tests -v

## Design decisions

- ELT: raw data is kept as received; transformations are re-runnable in SQL.
- Idempotency: ON CONFLICT DO UPDATE, so reruns never duplicate rows.
- Atomicity: each write is a single transaction (partial failure was tested).
- Data quality: every table constraint has a matching validation check.
- Docker: reproducible environment.

## Deferred on purpose

PySpark (data too small), MinIO (image pull issue), Airflow (optional).