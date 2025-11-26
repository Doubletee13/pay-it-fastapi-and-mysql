import logging
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import  Session
from fastapi import FastAPI
from .models.base import Base
from .models.user import User
from .models.product import Product
from .models.category import Category
from .models.order import Order
from .models.buyer import Buyer
from .models.farmer import Farmer
from .routes.database import engine, get_db
from .routes import users
from .routes import products
from .routes import auths
from .routes import categories
from .routes import orders





logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger(__name__)

max_retries = 10
retries = 0


while retries < max_retries:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Connected to MySQL and created tables")
        break
    except OperationalError as e:
        retries += 1
        logger.warning(f"MySQL not ready (attempt {retries}/{max_retries}): {e}")
        time.sleep(2)
else:
    logger.error("Could not connect to MySQL after multiple retries")
    raise RuntimeError("Database connection failed")




app = FastAPI(
    title="PayIt App",
    version="0.0.1",
    description="Our Market Place For Farmers And Buyers",
)



@app.on_event("startup")
def populate_categories():
    logger.info("Populating default categories...")

    db = next(get_db())
    default_categories = [
        {"name": "Vegetables", "description": "All kinds of vegetables"},
        {"name": "Fruits", "description": "Fresh fruits and berries"},
        {"name": "Tubers", "description": "Root crops such as yam, cassava, and potatoes"},
        {"name": "Livestock", "description": "Animals such as cattle, goats, sheep, and poultry"},
        {"name": "Cereals", "description": "Cereal crops such as maize, rice, wheat, and millet"},
        {"name": "Latex", "description": "Natural latex products such as rubber and related extracts"},
        {"name": "Oils", "description": "Oil producing crops such as palm oil, groundnut oil, and soybean oil"},
    ]

    for cat in default_categories:
        if not db.query(Category).filter_by(name=cat["name"]).first():
            db.add(Category(**cat))
            logger.info(f"Added category: {cat['name']}")

    db.commit()
    db.close()
    logger.info("Category population completed")

@app.get("/")
def index():
    return {"message": "Welcome to PayIt App"}

logger.info("Registering routers...")
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auths.router)
app.include_router(categories.router)
app.include_router(orders.router)
logger.info("Routers registered successfully")