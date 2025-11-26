from app.routes.database import get_db
from app.schema.users_schema import UserCreate, UserData, UserResponse, UserUpdate, UserResponseBack
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session, defer
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.middlewares.auth import AuthMiddleware
import logging
import bcrypt
import pymysql


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["Users"])

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


def create_user(db: db_dependency, user: UserCreate, request: Request):
    db_user = User(**user.dict(exclude=({"confirm_password"})))

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)




def get_user(db: db_dependency, user_id: int):
    return db.query(User).filter(User.id == user_id).options(defer(User.password)).first()


def get_all_users(db: db_dependency):
    return db.query(User).options(defer(User.password)).all()




def delete_user(db: db_dependency, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True




def update_user(db: db_dependency, user_id: int, data: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None



    update_data = data.dict(exclude_unset=True)
   
    for key, value in update_data.items():
        if key == "name":
            db_user.name = value
        elif key == "email":
            db_user.email = value
        elif key == "phone":
            db_user.phone = value
        elif key == "password":
                 salt = bcrypt.gensalt(rounds=12)
                 hashed_password = bcrypt.hashpw(value.encode('utf-8'), salt)
                 db_user.password = hashed_password
        elif key == "location":
            db_user.location = value
        elif key == "gender":
            db_user.gender = value
        elif key == "category":
            db_user.category = value
        

    db.commit()
    db.refresh(db_user)
    return db_user




# ROUTES






@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserResponse)
def create(user: UserCreate, db: db_dependency, request: Request):
    
    if not user.name and not user.email and not user.phone and not user.location and not user.gender and not user.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields required")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with this email already exists.")

    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists.")

    salt = bcrypt.gensalt(rounds=12)

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    user.password = hashed_password
    new_user = create_user(db, user, request)

    

    return {
        "success": True,
        "data": new_user, 
        "message": "User Created successfully"
    }




@router.get("/")
def get_users(db: db_dependency):
    users = get_all_users(db)

    return {
        "success": True,
        "data": users, 
        "message": "Users retrieved successfully"
    }


@router.get("/me")
def get_current_user(db: db_dependency, request: Request, current_user = Depends(AuthMiddleware), response_model = UserResponseBack):
    user = get_user(db, current_user.id)

    
    if not user:
        raiseError("User not found", request)

    delattr(user, 'password')

    return {
        "success": True,
        "data": user,
        "message": "User retrieved successfully"
    }
    






@router.put("/me")
def update_current_user(data: UserUpdate,db: db_dependency, request: Request, current_user = Depends(AuthMiddleware)):
    
    user = update_user(db, current_user.id, data)

    if not user:
        raiseError("User not found", request)

    updated_user = UserResponseBack(
        id = user.id, 
        name = user.name,
        phone = user.phone,
        email = user.email,
        gender = user.gender,
        location = user.location,
        created_at = user.created_at,
        updated_at = datetime.utcnow()
     )

    return {
        "success": True,
        "data": updated_user,
        "message": "Your account details have been updated successfully"
    }



@router.delete("/me")
def delete_user_route(user_id: int, db: db_dependency, request: Request, current_user = Depends(AuthMiddleware)):

    
    if current_user.id != user_id:
        raiseError("You are not allowed to delete another user",request)

    try:
        if not delete_user(db, user_id):
            raiseError("User not found", request)

    except IntegrityError:
        db.rollback()
        raiseError("This user cannot be deleted because they are linked to other records (products, orders, etc.)", request)

    return {
        "success": True,
        "message": "User deleted successfully"
    }
