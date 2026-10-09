import os

import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()


def create_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
        )
    except psycopg2.OperationalError as error:
        raise ConnectionError(
            "Could not connect to PostgreSQL. Check that the database server "
            "is running and that the DATABASE_* values in .env are correct."
        ) from error


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST", "localhost"),
    port=int(os.getenv("DATABASE_PORT", "5432")),
    database=os.getenv("DATABASE_NAME"),
)

engine = create_engine(DATABASE_URL)


def initialize_database() -> None:
    """Create the tables required by the sales pipeline when absent."""
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_id SERIAL PRIMARY KEY,
                pipeline_name VARCHAR(100) NOT NULL,
                source_file TEXT NOT NULL,
                started_at TIMESTAMP NOT NULL,
                finished_at TIMESTAMP,
                status VARCHAR(20) NOT NULL,
                rows_processed INTEGER NOT NULL DEFAULT 0,
                error_message TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER PRIMARY KEY,
                customer VARCHAR(100) NOT NULL,
                product VARCHAR(100) NOT NULL,
                quantity INTEGER NOT NULL,
                price NUMERIC(12, 2) NOT NULL,
                total_amount NUMERIC(12, 2) NOT NULL,
                order_value_category VARCHAR(10) NOT NULL
            );
            """
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
