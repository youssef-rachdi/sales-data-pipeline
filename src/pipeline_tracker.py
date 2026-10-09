from datetime import datetime

from src.database import create_connection


def start_pipeline_run(
    pipeline_name: str,
    source_file: str,
) -> int:
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO pipeline_runs (
        pipeline_name,
        started_at,
        status,
        source_file
    )
    VALUES (%s, %s, %s, %s)
    RETURNING run_id;
    """

    cursor.execute(
        query,
        (
            pipeline_name,
            datetime.now(),
            "RUNNING",
            source_file,
        ),
    )

    run_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return run_id


def finish_pipeline_run(
    run_id: int,
    status: str,
    rows_processed: int = 0,
    error_message: str | None = None,
) -> None:
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    UPDATE pipeline_runs
    SET
        finished_at = %s,
        status = %s,
        rows_processed = %s,
        error_message = %s
    WHERE run_id = %s;
    """

    cursor.execute(
        query,
        (
            datetime.now(),
            status,
            rows_processed,
            error_message,
            run_id,
        ),
    )

    connection.commit()

    cursor.close()
    connection.close()
