import os
from datetime import date, timedelta, datetime
from enum import Enum
import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional
import databases
import sqlalchemy
from sqlalchemy import create_engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from BaseClasses import Circle, MapGrid, Square, User, BusinessType, Business, Point

from BaseClasses.User import User, RelationshipStatus
from BaseClasses.Area import AreaBase, Area

# Database setup
DATABASE_URL = "sqlite:///./business_areas.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Security
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database models
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String),
    sqlalchemy.Column("user_birth_date", sqlalchemy.Date),
    sqlalchemy.Column("user_income", sqlalchemy.Float),
    sqlalchemy.Column("user_relationship_status", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
)

areas = sqlalchemy.Table(
    "areas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.user_id")),
    sqlalchemy.Column("area_type", sqlalchemy.String),
    sqlalchemy.Column("shape_type", sqlalchemy.String),
    sqlalchemy.Column("coordinates", sqlalchemy.JSON),
    sqlalchemy.Column("radius", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("missing_businesses", sqlalchemy.JSON),
    sqlalchemy.Column("business_data", sqlalchemy.String),
)

# Create database engine and tables
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current directory where main.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the FastAPI_app directory
fastapi_app_dir = os.path.join(current_dir, "FastAPI_app")

# Check if directory exists and mount it
if os.path.exists(fastapi_app_dir):
    app.mount("/FastAPI_app", StaticFiles(directory=fastapi_app_dir), name="fastapi_app")
else:
    print(f"Warning: Directory {fastapi_app_dir} does not exist")


# Pydantic models


class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_birth_date: date
    user_income: float
    user_relationship_status: RelationshipStatus
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


'''
Function For Password, Tokens and Authentications
'''


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(user_id: str, password: str):
    user = await database.fetch_one(users.select().where(users.c.user_id == user_id))
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = await database.fetch_one(users.select().where(users.c.user_id == user_id))
    if user is None:
        raise credentials_exception
    return user


# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# API endpoints

# User creation
@app.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        query = users.insert().values(
            user_id=user.user_id,
            user_name=user.user_name,
            user_birth_date=user.user_birth_date,
            user_income=user.user_income,
            user_relationship_status=user.user_relationship_status.value,
            hashed_password=hashed_password
        )
        await database.execute(query)
        return {"status": "success", "message": f"User {user.user_name} created successfully"}
    except ValidationError as ve:
        raise HTTPException(
            status_code=422,
            detail=[{"loc": err["loc"], "msg": err["msg"]} for err in ve.errors()]
        )
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail="User ID already registered")
    except Exception as e:
        print(f"Server error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# **Updated Authentication Token Endpoint**
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create the access token with user_id as subject
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_id"]}, expires_delta=access_token_expires
    )

    # Return token and success message
    return {"access_token": access_token, "token_type": "bearer",
            "message": f"User {user['user_id']} is logged in successfully"}


# Create a new area
@app.post("/areas/", response_model=Area)
async def create_area(area: AreaBase, current_user: dict = Depends(get_current_user)):
    area_data = area.dict()
    area_data["user_id"] = current_user["user_id"]

    if isinstance(area_data["missing_businesses"], list):
        area_data["missing_businesses"] = area_data["missing_businesses"]

    query = areas.insert().values(**area_data)
    try:
        last_record_id = await database.execute(query)
        return {**area_data, "area_id": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create area: {str(e)}")


# Get all areas for the current user
@app.get("/areas/", response_model=List[Area])
async def get_user_areas(current_user: dict = Depends(get_current_user)):
    query = areas.select().where(areas.c.user_id == current_user["user_id"])
    return await database.fetch_all(query)


# Serve index.html (for the frontend)
@app.get("/")
async def read_index():
    index_path = os.path.join(fastapi_app_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail=f"index.html not found at {index_path}")


@app.post("/debug/users/")
async def debug_user_create(user_data: dict):
    try:
        print(f"Received data: {user_data}")
        user = UserCreate(**user_data)
        return {"status": "valid", "parsed_data": user.dict()}
    except ValidationError as ve:
        return {"status": "invalid", "errors": ve.errors()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
