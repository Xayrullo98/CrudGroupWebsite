from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Float, Text
from sqlalchemy.orm import relationship

from db import Base


class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    customer_monitoring_id = Column(Integer, ForeignKey("Customer_monitoring.id"), nullable=False)
    text = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    customer = relationship('Customers', back_populates='comment')
    customer_monitoring = relationship('Customer_monitoring', back_populates='comment')


