from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class OtherWorks(Base):
    __tablename__ = "OtherWorks"
    id = Column(Integer, primary_key=True)
    work = Column(String(200),nullable=False)
    worker_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    jarima = Column(Float,nullable=True,default=0)
    deadline = Column(DateTime(timezone=True),  nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    result = Column(Boolean, nullable=True, default=None)
    user_id = Column(Integer,nullable=False)
    user = relationship("Users",back_populates="otherworks")