from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func,Float
from sqlalchemy.orm import relationship

from db import Base


class Worker_expenses(Base):
    __tablename__ = "Worker_expenses"
    id = Column(Integer, primary_key=True)
    money = Column(Float, nullable=False)
    type = Column(String(20), nullable=True)
    comment = Column(String(200), nullable=True)
    user_id = Column(Integer,ForeignKey("Users.id"),nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    user = relationship("Users", back_populates='worker')
