from pydantic import BaseModel,constr,EmailStr,validator, Field, model_validator
from typing import Optional
from datetime import datetime
from app.routes.enums import Category, Gender
import re




class UserCreate(BaseModel):
    name: str = Field(min_length=4, max_length=20)
    phone: str = Field(min_length=11) 
    email: EmailStr
    password: str = Field(min_length=6, pattern=r'')  
    confirm_password: str  
    gender: Gender
    category: Category
    location:str = Field(min_length=3)

    @validator('phone')
    def validate_number(cls, value):
        if len(value) != 11:
            raise ValueError('Phone number must be 11 long')
        if not any(number.isdigit() for number in value) :
            raise ValueError('Phone number must be digits')
        return value

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain alteast one uppercase letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain alteast one lowercase letter')

        if not re.search(r"\d",value):
            raise ValueError('password must contain alteast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain alteast one special character')

        return value

    @model_validator(mode = "after")
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('password must match')

        return self

    


    


  



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
    name: Optional[str] = Field(None,min_length=4, max_length=20)
    phone: Optional[str] = Field(None,min_length=11)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None,min_length=6)
    gender: Optional[Gender] = None
    category: Optional[Category] = None
    location: Optional[str] = Field(None,min_length=11)


    @validator('phone')
    def validate_password(cls, value):
        if len(value)!= 11:
            raise ValueError('Phone number must be 11 long')
        if not value.isdigit():
            raise ValueError('Phone number must be digits')
        return value

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError('password must contain alteast one uppercase letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('password must contain alteast one lowercase letter')

        if not re.search(r"\d",value):
            raise ValueError('password must contain alteast one numeric value')
        if not re.search(r"[^A-Za-z0-9]", value):
            raise ValueError('password must contain alteast one special character')

        return value
  




    

        