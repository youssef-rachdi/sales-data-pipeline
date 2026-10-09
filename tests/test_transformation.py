import pandas as pd

from src.transformation import transform_sales_data


def test_total_amount_is_quantity_times_price():
    df = pd.DataFrame({"quantity": [2, 1], "price": [300.0, 75.0]})
    result = transform_sales_data(df)
    assert list(result["total_amount"]) == [600.0, 75.0]


def test_order_value_category_threshold():
    df = pd.DataFrame({"quantity": [1, 1, 1], "price": [499.0, 500.0, 501.0]})
    result = transform_sales_data(df)
    assert list(result["order_value_category"]) == ["Low", "High", "High"]


def test_transform_does_not_mutate_input():
    df = pd.DataFrame({"quantity": [1], "price": [10.0]})
    transform_sales_data(df)
    assert "total_amount" not in df.columns
