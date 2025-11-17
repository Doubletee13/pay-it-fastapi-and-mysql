from pydantic import BaseModel,constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: constr(min_length=4, max_length=20)
    phone: constr(min_length=11)
    email: str
    password: str
    gender: str
    category: str
    location: str

  



class UserResponse(BaseModel):
    id: int 
    name: str
    phone: str
    email: str
    gender: str
    category: str
    location: str
    created_at: datetime
    updated_at: datetime



class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
  




    

        