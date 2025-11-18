from app.routes.database import get_db
from app.schema.users_schema import UserCreate, UserResponse, UserUpdate
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, defer
from app.models.user import User
import logging
import bcrypt


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session, Depends(get_db)]


def create_user(db: db_dependency, user: UserCreate):
    db_user = User(**user.dict(exclude=({"confirm_password"})))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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







@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: db_dependency):
    
    if not user.name or not user.email or not user.phone or not user.location or not user.gender or not user.category or not user.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All fields required")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with this email already exists.")

    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User already exists.")

    salt = bcrypt.gensalt(rounds=12)

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    user.password = hashed_password
    new_user = create_user(db, user)

    

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
        "message": "User retrieved successfully"
    }


@router.get("/{user_id}")
def get_a_user(db: db_dependency, user_id:int):
    user = get_user(db,user_id)

    if not user:
        raise HTTPException(404, "User not found")
    return {
        "success": True,
        "data": user, 
        "message": "User retrieved successfully"
    }


@router.patch("/{user_id}")
def update(user_id: int, data: UserUpdate, db: db_dependency):
    user = update_user(db, user_id, data)
    if not user:
        raise HTTPException(404, "User not found")

    updated_user = UserResponse(
        id = user.id, 
        name = user.name,
        phone = user.phone,
        email = user.email,
        gender = user.gender,
        category = user.category,
        location = user.location,
        created_at = user.created_at,
        updated_at = datetime.utcnow()
    )

    
    return {
        "success": True,
        "data":updated_user,
        "message": "User details updated successfully"
    }


@router.delete("/{user_id}")
def delete(user_id: int, db: db_dependency):
    if not delete_user(db, user_id):
        raise HTTPException(404, "User not found")
    return {
        "success": True,
        "message": "User deleted successfully"
    }