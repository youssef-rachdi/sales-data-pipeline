import pandas as pd

from src.database import create_connection


def load_sales_to_postgres(dataframe: pd.DataFrame) -> None:
    connection = create_connection()
    cursor = connection.cursor()

    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            order_id INTEGER PRIMARY KEY,
            customer VARCHAR(100) NOT NULL,
            product VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            total_amount NUMERIC(10, 2) NOT NULL
        );
        """

        cursor.execute(create_table_query)

        insert_query = """
        INSERT INTO sales (
            order_id,
            customer,
            product,
            quantity,
            price,
            total_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id)
        DO UPDATE SET
            customer = EXCLUDED.customer,
            product = EXCLUDED.product,
            quantity = EXCLUDED.quantity,
            price = EXCLUDED.price,
            total_amount = EXCLUDED.total_amount;
        """

        for _, row in dataframe.iterrows():
            cursor.execute(
                insert_query,
                (
                    int(row["order_id"]),
                    row["customer"],
                    row["product"],
                    int(row["quantity"]),
                    float(row["price"]),
                    float(row["total_amount"]),
                ),
            )

        connection.commit()

        print("Sales data loaded into PostgreSQL.")

    except Exception:
        connection.rollback()
        print("Database transaction rolled back.")
        raise

    finally:
        cursor.close()
        connection.close()
