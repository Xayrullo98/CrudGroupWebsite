from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Date,Float
from sqlalchemy.orm import relationship

from db import Base



class Notification(Base):
    __tablename__ = "Notifications"
    id = Column(Integer, primary_key=True)
    money = Column(Float, nullable=True)
    worker_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
    order_id = Column(Integer,ForeignKey("Orders.id"),nullable=True )
    user_id = Column(Integer, nullable=False)
    savdo_id = Column(Integer, nullable=True)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    name = Column(String(20),nullable=True)
    work = Column(String(200),nullable=True)
    type = Column(String(20),nullable=True)

    user = relationship('Users',back_populates="notifications")
    

    