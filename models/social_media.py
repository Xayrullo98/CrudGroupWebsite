from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class SocialMedia(Base):
    __tablename__ = "SocialMedia"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    link = Column(String(300),nullable=False)
    source_id = Column(Integer,ForeignKey("Customers.id"),nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    customer = relationship('Customers', back_populates='social')