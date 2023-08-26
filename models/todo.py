from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Todo(Base):
    __tablename__ = "Todos"
    id = Column(Integer, primary_key=True)
    work = Column(String(300), nullable=False)
    worker_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    jarima = Column(Float, nullable=False, default=0)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    doness = relationship('Done', back_populates='todo', order_by="Done.id.desc()", lazy="joined", uselist=False)
    worker = relationship('Users',back_populates='todos')