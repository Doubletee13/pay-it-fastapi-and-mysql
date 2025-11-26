from app.routes.database import get_db
from app.schema.order_schema import OrderCreate, OrderResponse, OrderUpdate
from datetime import datetime
from typing import Annotated,List
from app.models.user import User
from app.models.farmer import Farmer
from app.models.buyer import Buyer
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.order import Order
from app.middlewares.auth import AuthMiddleware
import logging
import pymysql



logger = logging.getLogger(__name__)


router = APIRouter(prefix="/orders", tags=["Orders"])

db_dependency = Annotated[Session, Depends(get_db)]


def raiseError(e: str, request: Request):
 
    method = request.method.upper()

    if method == "POST":
        message = f"Failed to create record: {e}"
    elif method == "GET":
        message = f"Failed to fetch record: {e}"
    elif method in ("PUT", "PATCH"):
        message = f"Failed to update record: {e}"
    elif method == "DELETE":
        message = f"Failed to delete record: {e}"
    else:
        message = f"Error: {e}"

    logger.error(message)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "status": "error",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(order_request: OrderCreate, db: db_dependency, request: Request, current_user: User = Depends(AuthMiddleware)):

    
    buyer = db.query(Buyer).filter(Buyer.user_id == current_user.id).first()
    if not buyer:
        buyer = Buyer(user_id=current_user.id)
        db.add(buyer)
        db.commit()
        db.refresh(buyer)

    total_amount = order_request.unit_price * order_request.quantity

    
    new_order = Order(
        buyer_id=buyer.id,
        product_id=order_request.product_id,
        unit_price=order_request.unit_price,
        quantity=order_request.quantity,
        total_amount=total_amount
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.put("/{order_id}", status_code=200, response_model=OrderResponse)
def update_order(order_id: int, order_request: OrderUpdate, db: db_dependency, request: Request, current_user: User = Depends(AuthMiddleware)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raiseError("Order doesn't exist", request)

    
    buyer = db.query(Buyer).filter(Buyer.id == order.buyer_id, Buyer.user_id == current_user.id).first()
    if not buyer:
        raiseError("Unauthorized user", request)

    update_data = order_request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

   
    order.total_amount = order.unit_price * order.quantity

    db.commit()
    db.refresh(order)
    return order



@router.get("/", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db), request: Request = None):
    orders = db.query(Order).all()
    if not orders:
        raiseError("No available orders", request)
    return orders



@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def get_order(order_id: int, db: db_dependency,request: Request, current_user: User = Depends(AuthMiddleware)):
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raiseError("Order doesn't exist", request)

    
    buyer = db.query(Buyer).filter(Buyer.id == order.buyer_id, Buyer.user_id == current_user.id).first()
    if not buyer:
        raiseError("Unauthorized user", request)

    return order



@router.get("/me/", response_model=List[OrderResponse])
def get_user_orders(db: db_dependency, current_user: User = Depends(AuthMiddleware)):

    buyer = current_user.buyer 
    if not buyer:
        return []  
    
    return buyer.orders  



@router.delete("/me/{order_id}", status_code=200)
def delete_order(order_id: int, db: db_dependency, request: Request, current_user: User = Depends(AuthMiddleware)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raiseError("Order doesn't exist", request)

  
    buyer = db.query(Buyer).filter(Buyer.id == order.buyer_id, Buyer.user_id == current_user.id).first()
    if not buyer:
        raiseError("Unauthorized user", request)

    db.delete(order)
    db.commit()
    return {
        "success": True,
        "message": "Order deleted successfully"
    }



