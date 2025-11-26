from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta, datetime
import bcrypt
import os


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_TIME'))







def create_access_token(claims: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        if expires_delta:
            expiration_time = datetime.utcnow() + expires_delta
        else:
            expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)


        claims.update({'exp': expiration_time})

        encoded_jwt = jwt.encode(claims, SECRET_KEY, ALGORITHM)

        return encoded_jwt
    except JWTError as e:
        raise e

def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError as e:
        raise


