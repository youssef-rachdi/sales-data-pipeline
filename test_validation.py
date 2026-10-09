import pandas as pd

from src.validation import validate_sales_data


dataframe = pd.read_csv("data/sales_invalid_type.csv")

result = validate_sales_data(dataframe)

print(f"Validation result: {result}")
