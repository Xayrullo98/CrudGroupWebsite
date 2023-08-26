from sqlalchemy import Column, Date, Integer, Numeric, DateTime, Time, String, Boolean, Text, ForeignKey, func
from db import Base
from sqlalchemy.orm import relationship, backref
from models.users import *


class Attandance(Base):
    __tablename__ = "Attandance"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(20), default='')
    user_id = Column(Integer, ForeignKey('Users.id'), default=0)
    working_period = Column(DateTime(timezone=True), nullable=True)
    authorizator = Column(String(50), default='')
    datetime = Column(DateTime(timezone=True), default=func.now())

    user = relationship('Users', back_populates='attandances')
