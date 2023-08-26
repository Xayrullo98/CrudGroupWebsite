from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Float, Text
from sqlalchemy.orm import relationship

from db import Base


class Customer_monitoring(Base):
    __tablename__ = "Customer_monitoring"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    customer_status = Column(String(50),nullable=True,default='')
    operator_date = Column(DateTime(timezone=True),   nullable=True)
    presentation_date = Column(DateTime(timezone=True),   nullable=True)
    searching_date = Column(DateTime(timezone=True),   nullable=True)
    project_date = Column(DateTime(timezone=True),   nullable=True)
    monitoring_status = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    customer = relationship('Customers', back_populates='monitoring')

    comment = relationship('Comment', back_populates='customer_monitoring')

