from src.pipeline_tracker import (
    start_pipeline_run,
    finish_pipeline_run,
)


run_id = start_pipeline_run(
    pipeline_name="sales_pipeline_test",
    source_file="test_file.csv",
)

print(f"Pipeline started: {run_id}")


try:
    raise ValueError("Test error: simulated pipeline failure.")

except Exception as error:

    finish_pipeline_run(
        run_id=run_id,
        status="FAILED",
        rows_processed=0,
        error_message=str(error),
    )

    print(f"Pipeline failed: {error}")
