from sqlalchemy import Column, Integer, String, DateTime, Enum, func, Numeric, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship





class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    price = Column(Numeric(10,2), nullable=False)
    category = Column(Enum('grains','tubers','vegetables','fruits','livestock','cereals','latex','oils'), nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", on_delete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    owner = relationship("User", back_populates="products")