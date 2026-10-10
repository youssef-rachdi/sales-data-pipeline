from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Sales(Base):
    __tablename__ = "sales"

    order_id = Column(Integer, primary_key=True)
    customer = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    order_value_category = Column(String(10), nullable=False)


class RawSales(Base):
    __tablename__ = "raw_sales"

    raw_id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, nullable=False)
    source_file = Column(Text, nullable=False)
    loaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    order_id = Column(Integer, nullable=False)
    customer = Column(Text, nullable=False)
    product = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
