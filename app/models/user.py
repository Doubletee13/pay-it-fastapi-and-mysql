from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.routes.enums import Gender, Category





class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(30), min_length=3, max_length=30, nullable=False)
    phone = Column(String(20), unique=True, min_length=11, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100),nullable=True)
    gender = Column(Enum(Gender.MALE.value,Gender.FEMALE.value), nullable=False) 
    category = Column(Enum('buyer', 'farmer'), nullable=False) 
    location = Column(String(255),min_length=3, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    products = relationship("Product", back_populates="owner", cascade="all, delete")

    