from pydantic import BaseModel, Field, EmailStr, validator, model_validator
import re 


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

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


class LoginResponse(BaseModel):
    access_token: str 
    token_type:str = 'bearer'
    email: str 
    user_id: int
