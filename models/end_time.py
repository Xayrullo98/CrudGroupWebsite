from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float,TIME
from sqlalchemy.orm import relationship

from db import Base


class End_time(Base):
    __tablename__ = "End_time"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(TIME(timezone=True), nullable=False)
    status = Column(Boolean, nullable=False, default=True)


