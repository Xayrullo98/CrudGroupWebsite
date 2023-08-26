from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class ExtraWorks(Base):
    __tablename__ = "ExtraWorks"
    id = Column(Integer, primary_key=True)
    work = Column(String(200),nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    user = relationship("Users",back_populates="extraworks")
