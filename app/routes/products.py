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


# EXCEPTION ERROR FUNCTION
def raiseError(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail = {
            "status": "error",
            "message": f"failed to create product: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )


# CRUD OPERATIONS

def create_product(db: db_dependency, product: ProductCreate):
    db_product = Product(**product.dict())

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)
 


def get_product(db: db_dependency, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(db: db_dependency):
    return db.query(Product).all()



def update_product(db: db_dependency, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None

 
    update_data = product.dict(exclude_unset=True)
   
    for key, value in update_data.items():
        if key == "price":
            db_product.price = value
        elif key == "category":
            db_product.category = value
        elif key == "quantity":
            db_product.quantity = value
        
        

    db.commit()
    db.refresh(db_product)
    return db_product



def get_products_by_user(db: db_dependency, user_id):
    user_products = db.query(Product).filter(Product.user_id == user_id).all()

    if not user_products:
        return None

    return user_products

    

def delete_product(db: db_dependency, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True




# ROUTES

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: db_dependency):
    
    if not product.price or not product.category or not product.quantity or not product.user_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields required")

    user = db.query(User).filter(User.id == product.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Cannot add a product as user does not exist")
   
    new_product = create_product(db, product)

    return {
        "success": True,
        "data": new_product, 
        "message": "Product Created successfully"
    }


@router.get("/")
def get_products(db: db_dependency):
    products = get_all_products(db)

    return {
        "success": True,
        "data": products, 
        "message": "Products retrieved successfully"
    }


@router.get("/{product_id}")
def get_a_product(db: db_dependency, product_id:int):
    product = get_product(db,product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return {
        "success": True,
        "data": product, 
        "message": "Product retrieved successfully"
    }

@router.get("/users/{user_id}")
def get_products_of_user(db: db_dependency, user_id:int):

    user_products = get_products_by_user(db,user_id)

    if not user_products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return {
        "success": True,
        "data": user_products, 
        "message": f"Product/Products by User with ID {user_id} retrieved successfully"
    }


@router.patch("/{product_id}")
def update(product_id: int, product: ProductUpdate, db: db_dependency):
    product = update_product(db, product_id, product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    updated_product = ProductResponse(
        id = product.id, 
        price = product.price,
        category = product.category,
        quantity = product.quantity,
        user_id = product.user_id,
        created_at = product.created_at,
        updated_at = datetime.utcnow()
    )

    
    return {
        "success": True,
        "data":updated_product,
        "message": "Product details updated successfully"
    }



@router.delete("/{product_id}")
def delete(product_id: int, db: db_dependency):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return {
        "success": True,
        "message": "Product deleted successfully"
    }


