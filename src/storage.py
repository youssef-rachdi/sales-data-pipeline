from pathlib import Path
import pandas as pd

from src.logging_config.logger import logger


PARQUET_DIR = Path("data/processed")


def save_dataframe_to_parquet(
    dataframe: pd.DataFrame,
    file_name: str,
) -> Path:
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PARQUET_DIR / file_name

    dataframe.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
    )

    logger.info(f"Data saved to Parquet: {output_path}")

    return output_path
