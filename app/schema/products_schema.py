from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.routes.enums import ProductType

class ProductCreate(BaseModel):
    price: float
    category: ProductType
    quantity: int
    user_id: int
    
   

 

  



class ProductResponse(BaseModel):
    id: int 
    price: float
    category: ProductType
    quantity: int
    user_id: int
    created_at: datetime
    updated_at: datetime



class ProductUpdate(BaseModel):
    price: Optional[float] = None
    category: Optional[ProductType] = None
    quantity: Optional[int] = None
    
    
    

 




    

        