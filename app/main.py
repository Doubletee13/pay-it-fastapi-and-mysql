import logging
from fastapi import FastAPI, HTTPException, status
from .models.base import Base
from .models.user import User
from .models.product import Product
from .routes.database import engine
from .routes import users
from .routes import products



logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "PayIt App",
    version = "0.0.1",
    description = "Our Market Place For Framer And Buyers"
    )


@app.get("/")
def index():
    return {
        "message":"welcome to payit app"
    }

app.include_router(users.router)
app.include_router(products.router)