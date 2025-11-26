from sqlalchemy import Column, Integer, String, DateTime, Enum, func, Numeric, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship






class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    price = Column(Numeric(10,2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    farmer_id = Column(Integer, ForeignKey("farmers.id", on_delete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    farmer = relationship("Farmer", back_populates="products")
    category = relationship("Category", back_populates="products")
    orders = relationship("Order", back_populates="products")