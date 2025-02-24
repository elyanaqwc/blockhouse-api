from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text, DECIMAL

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,nullable=False)
    symbol = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_type = Column(String, nullable=False)
    side = Column(String, nullable=False)
    status = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'))




