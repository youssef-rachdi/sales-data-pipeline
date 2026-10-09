import pandas as pd

from src.validation import validate_sales_data


def make_df(**overrides):
    row = {
        "order_id": [1, 2],
        "customer": ["Ali", "Sara"],
        "product": ["Laptop", "Mouse"],
        "quantity": [1, 2],
        "price": [1200.0, 25.0],
    }
    row.update(overrides)
    return pd.DataFrame(row)


def test_valid_data_has_no_errors():
    assert validate_sales_data(make_df()) == []


def test_missing_column_is_reported():
    df = make_df().drop(columns=["price"])
    errors = validate_sales_data(df)
    assert any("Missing columns" in e for e in errors)


def test_null_customer_is_reported():
    df = make_df(customer=["Ali", None])
    errors = validate_sales_data(df)
    assert "customer contains NULL values." in errors


def test_non_numeric_quantity_is_reported():
    df = make_df(quantity=[1, "two"])
    errors = validate_sales_data(df)
    assert "quantity must be numeric." in errors


def test_non_positive_price_is_reported():
    df = make_df(price=[1200.0, 0.0])
    errors = validate_sales_data(df)
    assert "price must be greater than 0." in errors


def test_duplicate_order_id_is_reported():
    df = make_df(order_id=[1, 1])
    errors = validate_sales_data(df)
    assert "Duplicate order_id values found." in errors


def test_customer_longer_than_100_chars_is_reported():
    df = make_df(customer=["A" * 150, "Sara"])
    errors = validate_sales_data(df)
    assert "customer exceeds 100 characters in 1 row(s)." in errors
