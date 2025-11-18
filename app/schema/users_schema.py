from pydantic import BaseModel,constr,EmailStr,validator,constr
from typing import Optional
from datetime import datetime
from app.routes.enums import Category, Gender

class UserCreate(BaseModel):
    name: constr(min_length=4, max_length=20)
    phone: constr(min_length=11)
    email: EmailStr
    password: str
    gender: Gender
    category: Category
    location: str

    @validator('password')
    def validate_password(cls, v):
        if not (8 <= len(v) <= 15):
            raise ValueError('Password must be between 8 and 15 characters long')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password must contain at least one letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

  



class UserResponse(BaseModel):
    id: int 
    name: str
    phone: str
    email: str
    gender: Gender
    category: Category
    location: str
    created_at: datetime
    updated_at: datetime



class UserUpdate(BaseModel):
    name: Optional[constr(min_length=4, max_length=20)] = None
    phone: Optional[constr(min_length=11)] = None
    email: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[Gender] = None
    category: Optional[Category] = None
    location: Optional[str] = None

    @validator('password')
    def validate_password(cls, v):
        if not (8 <= len(v) <= 15):
            raise ValueError('Password must be between 8 and 15 characters long')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password must contain at least one letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
  




    

        