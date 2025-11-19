from app.routes.database import get_db
from app.schema.auth_schema import LoginRequest, LoginResponse
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User

from app.auth.jwt import create_access_token
import logging
import bcrypt



logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auths", tags=["Auth"])

db_dependency = Annotated[Session, Depends(get_db)]





# EXCEPTION ERROR FUNCTION
def raiseHttpException(e):
    logger.error(f"failed to create record error: {e}")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = {
            "status": "error",
            "message": f"failed to login: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )



def verify_password(plain_text_password:str, hashed_password:str)-> bool:
    password_verification = plain_text_password

    return bcrypt.checkpw(password_verification.encode('utf-8'), hashed_password.encode('utf-8'))





@router.post("/login", status_code=status.HTTP_200_OK, response_model = LoginResponse)
def create(login_request: LoginRequest, db: db_dependency):

    user = db.query(User).filter(login_request.email == User.email).first()

    if not user:
        raiseHttpException("Email does not exist")

   

    password_match = verify_password(login_request.password, user.password)

    if not password_match:
        raiseHttpException("Invalid password")

    claims = {
        'sub': str(user.id),
        'email': user.email,
        'user_id': str(user.id)
    }

    access_token = create_access_token(claims)

    return LoginResponse(
        access_token = access_token,
        token_type = 'bearer',
        email = user.email,
        user_id = user.id
    )

    


    
   