from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.routes.enums import OrderStatus





class OrderCreate(BaseModel):
    product_id: int
    unit_price: float
    quantity: int
    # total_amount is removed because we calculate it

class OrderResponse(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    unit_price: float
    quantity: int
    total_amount: float
    order_status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    order_status: Optional[OrderStatus] = None
