from sqlalchemy import Column, Integer, String, DateTime, Enum, func, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship




class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")
