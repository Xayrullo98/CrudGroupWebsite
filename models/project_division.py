from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Float,Text
from sqlalchemy.orm import relationship

from db import Base



class Project_division(Base):
    __tablename__ = "Project_division"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer,ForeignKey("Orders.id"), nullable=False)
    worker_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    text = Column(Text,nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    deadline_status = Column(Boolean, nullable=True, default=None)

    order = relationship('Orders', back_populates='division')
    worker = relationship('Users', back_populates='division')



