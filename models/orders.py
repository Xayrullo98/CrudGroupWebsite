import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Identity,Float,Date
from sqlalchemy.orm import relationship, backref

import db
from db import Base
from models.customers import Customers


class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True, )
    savdo_id = Column(Integer,nullable=False, )
    customer_id = Column(Integer,ForeignKey('Customers.id'), nullable=False)
    comment = Column(String(200),nullable=True)
    user_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    type=Column(String(20), nullable=True, )
    order_status = Column(String(30),nullable=True)
    updated_day = Column(Date(),default=func.now(), nullable=True, )
    summ = Column(Float,nullable=True,default=0)
    rest_summ = Column(Float,nullable=True,default=0)
    discount = Column(Float,nullable=True,default=0)
    real_summ = Column(Float,nullable=True,default=0)
    payment_summ = Column(Float,nullable=True,default=0)
    created_date = Column(Date(), nullable=True, default=None)
    design_date = Column(Date(), nullable=True, default=None)
    programming_date = Column(Date(), nullable=True, default=None)
    deploy_date = Column(Date(), nullable=True, default=None)
    control_date = Column(Date(), nullable=True, default=None)

    history = relationship("Kpi_History",back_populates="order")
    customer = relationship("Customers",back_populates="orders",lazy='joined')
    user = relationship("Users",back_populates = 'order')
    assignment = relationship('Assignment_division', back_populates='order')
    division = relationship('Project_division', back_populates='order')
    