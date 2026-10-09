import pandas as pd


def validate_sales_data(
    dataframe: pd.DataFrame,
) -> list[str]:

    errors = []

    required_columns = {
        "order_id",
        "customer",
        "product",
        "quantity",
        "price",
    }

    # Required columns
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        errors.append(
            f"Missing columns: {sorted(missing_columns)}"
        )
        return errors

    # Null checks
    if dataframe["order_id"].isnull().any():
        errors.append("order_id contains NULL values.")

    if dataframe["customer"].isnull().any():
        errors.append("customer contains NULL values.")

    if dataframe["product"].isnull().any():
        errors.append("product contains NULL values.")

    # Type checks
    if not pd.api.types.is_numeric_dtype(
        dataframe["order_id"]
    ):
        errors.append("order_id must be numeric.")

    if not pd.api.types.is_numeric_dtype(
        dataframe["quantity"]
    ):
        errors.append("quantity must be numeric.")

    if not pd.api.types.is_numeric_dtype(
        dataframe["price"]
    ):
        errors.append("price must be numeric.")

    # Range checks
    if pd.api.types.is_numeric_dtype(dataframe["quantity"]):
        if (dataframe["quantity"] <= 0).any():
            errors.append(
                "quantity must be greater than 0."
            )

    if pd.api.types.is_numeric_dtype(dataframe["price"]):
        if (dataframe["price"] <= 0).any():
            errors.append(
                "price must be greater than 0."
            )

    # Length checks (must match VARCHAR limits in models.py)
    max_lengths = {"customer": 100, "product": 100}

    for column, limit in max_lengths.items():
        too_long = dataframe[column].astype(str).str.len() > limit
        if too_long.any():
            errors.append(
                f"{column} exceeds {limit} characters "
                f"in {int(too_long.sum())} row(s)."
            )
    # Duplicate check
    if dataframe["order_id"].duplicated().any():
        errors.append(
            "Duplicate order_id values found."
        )

    return errors

