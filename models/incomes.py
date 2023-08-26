from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Float
from sqlalchemy.orm import relationship, backref

from db import Base
from models.customers import Customers
from models.orders import Orders
from models.trades import Trades


class Incomes(Base):
    __tablename__ = "Incomes"
    id = Column(Integer, primary_key=True)
    money = Column(Float, nullable=False)
    type = Column(String(20), nullable=True)
    source_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    order = relationship('Orders', foreign_keys=[source_id],
                         backref=backref('incomes', order_by="desc(Orders.id)"),
                         primaryjoin=lambda: and_(Orders.id == Incomes.source_id))


