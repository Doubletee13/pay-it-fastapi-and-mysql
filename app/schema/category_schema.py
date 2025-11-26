from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class ProductCategory(BaseModel):
    name: str
    description: str



