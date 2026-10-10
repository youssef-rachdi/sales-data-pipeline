from src.ingestion import load_sales_data
from src.validation import validate_sales_data
from src.transformation import transform_sales_data
from src.storage import save_dataframe_to_parquet
from src.repository import RawSalesRepository

from src.pipeline_tracker import (
    start_pipeline_run,
    finish_pipeline_run,
)

from src.logging_config.logger import logger


RAW_COLUMNS = ["order_id", "customer", "product", "quantity", "price"]


def main() -> None:
    pipeline_name = "sales_pipeline"
    source_file = "data/sales.csv"

    run_id = start_pipeline_run(
        pipeline_name=pipeline_name,
        source_file=source_file,
    )

    logger.info(f"Pipeline started. run_id={run_id}")

    try:
        dataframe = load_sales_data(source_file)

        validation_errors = validate_sales_data(dataframe)

        if validation_errors:
            finish_pipeline_run(
                run_id=run_id,
                status="FAILED",
                rows_processed=0,
                error_message=" | ".join(validation_errors),
            )
            logger.error(f"Data validation failed. run_id={run_id}")
            for error in validation_errors:
                logger.error(error)
            return

        logger.info("Data validation passed.")

        raw_repo = RawSalesRepository()
        raw_repo.append(
            dataframe[RAW_COLUMNS].to_dict(orient="records"),
            run_id=run_id,
            source_file=source_file,
        )
        raw_repo.transform_to_sales()

        save_dataframe_to_parquet(
            transform_sales_data(dataframe),
            file_name="sales_transformed.parquet",
        )

        finish_pipeline_run(
            run_id=run_id,
            status="SUCCESS",
            rows_processed=len(dataframe),
        )

        logger.info(
            f"Pipeline completed successfully. "
            f"run_id={run_id}, rows_processed={len(dataframe)}"
        )

    except Exception as error:
        finish_pipeline_run(
            run_id=run_id,
            status="FAILED",
            rows_processed=0,
            error_message=str(error),
        )
        logger.exception(f"Pipeline failed. run_id={run_id}")
        raise


if __name__ == "__main__":
    main()
