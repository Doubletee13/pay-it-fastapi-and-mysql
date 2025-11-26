from sqlalchemy import Column, Integer, String, DateTime, Enum, func, Numeric, ForeignKey
from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.routes.enums import OrderStatus






class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", on_delete="RESTRICT"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id", on_delete="CASCADE"), nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
    order_status = Column(Enum(OrderStatus.PENDING.value,OrderStatus.COMPLETED.value,OrderStatus.FAILED.value), nullable=False, server_default=OrderStatus.PENDING.value)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)

    products = relationship("Product", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")
