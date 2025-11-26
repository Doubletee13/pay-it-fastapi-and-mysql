from app.routes.database import get_db
from app.schema.products_schema import ProductCreate, ProductResponse, ProductUpdate
from datetime import datetime
from typing import Annotated, List
from app.models.user import User
from app.models.farmer import Farmer
from fastapi import APIRouter, Depends, Request, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.product import Product
from app.middlewares.auth import AuthMiddleware
import logging
import pymysql



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


router = APIRouter(prefix="/products", tags=["Products"])

db_dependency = Annotated[Session, Depends(get_db)]


# EXCEPTION ERROR FUNCTION
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


# CRUD OPERATIONS

def create_product(db, product: ProductCreate, current_user: User, request: Request):
    
    farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()

    if not farmer:
        farmer = Farmer(user_id=current_user.id)
        db.add(farmer)
        try:
            db.commit()
            db.refresh(farmer)
        except Exception as e:
            db.rollback()
            raiseError(e, request)

    new_product = Product(
        farmer_id=farmer.id,
        **product.dict()
    )

    db.add(new_product)

    try:
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raiseError(e, request)

 

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



def delete_product(db: db_dependency, product, request: Request):
    try:
        db.delete(product)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raiseError(
            "This product cannot be deleted because it is linked to an active order.",
            request
        )



# ROUTES

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate,db: db_dependency,request: Request,current_user = Depends(AuthMiddleware)):
    
    if not (product.price and product.category_id and product.quantity):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="All fields required"
        )

    new_product = create_product(db, product, current_user, request)

    return {
        "success": True,
        "data": new_product,
        "message": "Product created successfully"
    }


@router.get("/")
def get_products(db: db_dependency, request: Request):
    products = get_all_products(db)

    if not products:
        raiseError("No available products", request)

    return {
        "success": True,
        "data": products, 
        "message": "Products retrieved successfully"
    }


@router.get("/{product_id}")
def get_a_product(db: db_dependency, product_id:int, request: Request):
    product = get_product(db,product_id)

    if not product:
        raiseError("Product doesn't exist", request)
    return {
        "success": True,
        "data": product, 
        "message": "Product retrieved successfully"
    }



@router.get("/me/", response_model=List[ProductResponse])
def get_user_products(db: db_dependency, current_user = Depends(AuthMiddleware)):

    farmer = current_user.farmer  

    if not farmer:
        return []  

    return farmer.products  

    


@router.put("/{product_id}")
def update(product_id: int, product: ProductUpdate, db: db_dependency, request: Request,current_user = Depends(AuthMiddleware)):
    product = update_product(db, product_id, product)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    updated_product = ProductResponse(
        id = product.id, 
        price = product.price,
        category_id = product.category_id,
        quantity = product.quantity,
        farmer_id = product.farmer_id,
        created_at = product.created_at,
        updated_at = datetime.utcnow()
    )

    
    return {
        "success": True,
        "data":updated_product,
        "message": "Product details updated successfully"
    }



@router.delete("/me/{product_id}")
def delete_product_route(
    product_id: int, 
    db: db_dependency, 
    request: Request, 
    current_user = Depends(AuthMiddleware)
):

    farmer = current_user.farmer
    if not farmer:
        raiseError("You are not a farmer", request)

    product = get_product(db, product_id)
    if not product:
        raiseError("Product doesn't exist", request)

    if product.farmer_id != farmer.id:
        raiseError("Unauthorized user", request)

    delete_product(db, product, request)

    return {
        "success": True,
        "message": "Product deleted successfully"
    }



