import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST", "localhost"),
    port=int(os.getenv("DATABASE_PORT", "5432")),
    database=os.getenv("DATABASE_NAME"),
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def initialize_database() -> None:
    """Create the tables required by the pipeline when absent."""
    from src.models import Base

    Base.metadata.create_all(engine)
    with engine.begin() as connection:
        connection.execute(
            text(
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
                )
                """
            )
        )