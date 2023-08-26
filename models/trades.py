from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from db import Base

class Trades(Base):
    __tablename__ = "Trades"
    id = Column(Integer, primary_key=True)
    project_name = Column(String(100), nullable=False)
    quantity = Column(Integer,nullable=False)
    user_id = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('Orders.id',), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)




