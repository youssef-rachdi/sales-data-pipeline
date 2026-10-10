from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import engine


def start_pipeline_run(pipeline_name: str, source_file: str) -> int:
    with Session(engine) as session:
        run_id = session.execute(
            text(
                """
                INSERT INTO pipeline_runs
                    (pipeline_name, started_at, status, source_file)
                VALUES (:pipeline_name, :started_at, 'RUNNING', :source_file)
                RETURNING run_id
                """
            ),
            {
                "pipeline_name": pipeline_name,
                "started_at": datetime.now(),
                "source_file": source_file,
            },
        ).scalar_one()
        session.commit()
    return run_id


def finish_pipeline_run(
    run_id: int,
    status: str,
    rows_processed: int = 0,
    error_message: str | None = None,
) -> None:
    with Session(engine) as session:
        session.execute(
            text(
                """
                UPDATE pipeline_runs
                SET finished_at = :finished_at,
                    status = :status,
                    rows_processed = :rows_processed,
                    error_message = :error_message
                WHERE run_id = :run_id
                """
            ),
            {
                "finished_at": datetime.now(),
                "status": status,
                "rows_processed": rows_processed,
                "error_message": error_message,
                "run_id": run_id,
            },
        )
        session.commit()