from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.routes.enums import Gender, Category





class Buyer(Base):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", on_delete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer", cascade="all, delete")