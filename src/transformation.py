import numpy as np
import pandas as pd


def transform_sales_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe["total_amount"] = dataframe["quantity"] * dataframe["price"]

    dataframe["order_value_category"] = np.where(
        dataframe["total_amount"] >= 500, "High", "Low"
    )
    return dataframe
