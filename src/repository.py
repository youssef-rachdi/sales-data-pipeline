from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.database import engine
from src.models import Sales
from src.logging_config.logger import logger


class SalesRepository:
    def __init__(self, session: Session | None = None):
        self._session = session

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
