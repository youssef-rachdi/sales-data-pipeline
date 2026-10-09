from pathlib import Path

import pandas as pd


def load_sales_data(file_path: str | Path) -> pd.DataFrame:
    """Read sales data from the requested CSV file."""
    return pd.read_csv(
        file_path,
        dtype={"price": "float64"},
    )
