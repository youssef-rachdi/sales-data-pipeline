from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.database import engine
from src.logging_config.logger import logger
from src.models import RawSales, Sales


TRANSFORM_SQL = text("""
INSERT INTO sales (order_id, customer, product, quantity, price,
                   total_amount, order_value_category)
SELECT DISTINCT ON (order_id)
       order_id, customer, product, quantity, price,
       quantity * price,
       CASE WHEN quantity * price >= 500 THEN 'High' ELSE 'Low' END
FROM raw_sales
ORDER BY order_id, loaded_at DESC, raw_id DESC
ON CONFLICT (order_id) DO UPDATE SET
    customer = EXCLUDED.customer,
    product = EXCLUDED.product,
    quantity = EXCLUDED.quantity,
    price = EXCLUDED.price,
    total_amount = EXCLUDED.total_amount,
    order_value_category = EXCLUDED.order_value_category
""")


class SalesRepository:
    def upsert_many(self, records: list[dict]) -> None:
        with Session(engine) as session:
            stmt = pg_insert(Sales).values(records)
            stmt = stmt.on_conflict_do_update(
                index_elements=["order_id"],
                set_={
                    "customer": stmt.excluded.customer,
                    "product": stmt.excluded.product,
                    "quantity": stmt.excluded.quantity,
                    "price": stmt.excluded.price,
                    "total_amount": stmt.excluded.total_amount,
                    "order_value_category": stmt.excluded.order_value_category,
                },
            )
            session.execute(stmt)
            session.commit()
        logger.info(f"Upserted {len(records)} rows via SalesRepository.")


class RawSalesRepository:
    def append(self, records: list[dict], run_id: int, source_file: str) -> None:
        rows = [{**r, "run_id": run_id, "source_file": source_file} for r in records]
        with Session(engine) as session:
            session.execute(pg_insert(RawSales).values(rows))
            session.commit()
        logger.info(f"Appended {len(rows)} rows to raw_sales.")

    def transform_to_sales(self) -> None:
        with Session(engine) as session:
            session.execute(TRANSFORM_SQL)
            session.commit()
        logger.info("Transformed raw_sales into sales (SQL).")
