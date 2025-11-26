from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.database import get_db
from app.models.category import Category
from app.schema.category_schema import ProductCategory
import logging
import pymysql

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[ProductCategory])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
