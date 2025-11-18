from app.routes.database import get_db
from app.schema.products_schema import ProductCreate, ProductResponse, ProductUpdate
from datetime import datetime
from typing import Annotated
from app.models.user import User
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
import logging



logger = logging.getLogger(__name__)


router = APIRouter(prefix="/products", tags=["Products"])

db_dependency = Annotated[Session, Depends(get_db)]


def create_product(db: db_dependency, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
 



@router.post("/", status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: db_dependency):
    
    if not product.price or not product.category or not product.quantity or not product.user_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields required")
   
    new_product = create_product(db, product)

    return {
        "success": True,
        "data": new_product, 
        "message": "Product Created successfully"
    }



