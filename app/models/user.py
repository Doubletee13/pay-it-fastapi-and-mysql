from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from app.models.base import Base
from datetime import datetime





class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=True) #assignment, set boundaries
    gender = Column(Enum('M', 'F'), nullable=False) #assignment, set boundaries
    category = Column(Enum('buyer', 'farmer'), nullable=False) # create Enum
    location = Column(String(255),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    