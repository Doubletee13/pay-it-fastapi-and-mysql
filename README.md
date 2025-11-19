### PayIt API

FastAPI + SQLAlchemy + MySQL backend for managing users and products. Fully containerized with Docker.

#### Features

1. User management (CRUD)

2. Product management (CRUD)

3. MySQL database with SQLAlchemy ORM

4. Docker Compose setup




#### Requirements

1. Docker

2. Docker Compose

#### Setup
Rename .env.example with .env
```bash=
cp .env.example .env

# REPLACE THE VARIABLES WITH YOUR DETAILS
DB_USER=myuser
DB_PASSWORD=yourpassword
```




#### Start the APPLICATION
```bash=
docker-compose up --build
```


#### Access

Swagger: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Postman

#### Example Requests

 

```python=
# Create User
# Method(POST) http://localhost:8000/users

  {
    "name": "John",
    "phone": "08138208901",
    "email": "john@gmail.com",
    "password": "Pa@sssssssss7",
    "confirm_password": "Pa@sssssssss7",
    "gender": "M",
    "category": "buyer",
    "location": "Terminus"
  }
   
    
# Create Product
# Method(POST) http://localhost:8000/products
# Create Product
{

   "price": 500.0,
    "category": "fruits",
    "quantity": 200,
    "user_id": 1
}
```



#### Containers
Services	Port	    Description
payit.api	8000	    FastAPI app
payit_db	3307 → 3306	MySQL DB