from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float
from sqlalchemy.orm import backref, relationship

from db import Base
from models.users import Users


class Expenses(Base):
    __tablename__ = "Expenses"
    id = Column(Integer, primary_key=True)
    money = Column(Float, nullable=False)
    type = Column(String(20), nullable=True)
    source_id = Column(Integer, nullable=False)
    source = Column(String(200), nullable=False)
    user_id = Column(Integer,nullable=False)
    date_time = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    user_for_expenses = relationship('Users', foreign_keys=[source_id],
                                    backref=backref('expenses', order_by="desc(Users.id)"),
                                    primaryjoin=lambda: and_(Users.id == Expenses.source_id))