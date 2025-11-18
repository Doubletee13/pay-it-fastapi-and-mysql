from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.routes.enums import Category, Gender

class ProductCreate(BaseModel):
    price: float
    category: str
    quantity: int
    user_id: int
    
   

 

  



class ProductResponse(BaseModel):
    id: int 
    price: float
    category: str
    quantity: int
    user_id: int
    created_at: datetime
    updated_at: datetime



class ProductUpdate(BaseModel):
    price: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    password: Optional[str] = None
    
    

 




    

        