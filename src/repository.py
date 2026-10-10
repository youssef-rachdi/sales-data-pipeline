from pathlib import Path

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from src.database import engine
from src.logging_config.logger import logger
from src.models import RawSales


TRANSFORM_SQL = text(
    (Path(__file__).parent / "sql" / "transform_sales.sql").read_text(encoding="utf-8")
)


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