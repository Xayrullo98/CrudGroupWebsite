from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from db import Base

class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    user_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    orders = relationship('Orders', back_populates="customer")
    phones = relationship('Phones', back_populates='owner',lazy='joined')
    social = relationship("SocialMedia",back_populates="customer")
    comment = relationship('Comment', back_populates='customer')
    monitoring= relationship('Customer_monitoring', back_populates='customer')
    