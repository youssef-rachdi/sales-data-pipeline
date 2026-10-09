from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
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