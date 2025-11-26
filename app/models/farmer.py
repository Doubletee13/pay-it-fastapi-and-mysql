from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship






class Farmer(Base):
    __tablename__ = 'farmers'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="farmer")
    products = relationship("Product", back_populates="farmer", cascade="all, delete")