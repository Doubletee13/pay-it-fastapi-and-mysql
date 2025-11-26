from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    price: float
    category_id: int
    quantity: int
   
    
   

 

  



class ProductResponse(BaseModel):
    id: int 
    price: float
    category_id:int
    quantity: int
    farmer_id: int
    created_at: datetime
    updated_at: datetime



class ProductUpdate(BaseModel):
    price: Optional[float] = None
    category_id: Optional[int] =None
    quantity: Optional[int] = None
    
    
    

 




    

        