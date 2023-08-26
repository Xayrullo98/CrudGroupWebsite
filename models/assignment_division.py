from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Float
from sqlalchemy.orm import relationship, backref

from db import Base
from models.customers import Customers
from models.orders import Orders
from models.trades import Trades


class Assignment_division(Base):
    __tablename__ = "Assignment_division"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer,ForeignKey("Orders.id"), nullable=False)
    programmer_type = Column(String(50), nullable=True)
    programmer_title = Column(String(50), nullable=True)
    worker_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    work_price = Column(Float, nullable=True,default=0)
    currency = Column(String(30), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    deadline_status = Column(Boolean, nullable=True, default=None)
    order = relationship('Orders', back_populates='assignment')
    worker = relationship('Users', back_populates='user')


