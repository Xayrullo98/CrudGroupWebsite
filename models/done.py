from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Done(Base):
    __tablename__ = "Dones"
    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("Todos.id"), nullable=True,)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    result = Column(Boolean, nullable=True, default=None)

    todo = relationship('Todo', back_populates='doness')
