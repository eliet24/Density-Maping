from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, User, Category, Location, UserCreate, CategoryCreate, Category as CategorySchema, LocationCreate, Location as LocationSchema
from database import SessionLocal, engine

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# - - - - - - - - - - - Routes - - - - - - - - - - -

# Route to create a category
@app.post("/categories/", response_model=CategorySchema)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_crud(db=db, category=category)

# Route to create a location
@app.post("/locations/", response_model=LocationSchema)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return create_location_crud(db=db, location=location)

# Route to get all categories
@app.get("/categories/", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return get_categories_crud(db=db)

# Route to get all locations
@app.get("/locations/", response_model=List[LocationSchema])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_locations_crud(db=db, skip=skip, limit=limit)

# - - - - - - - - - - - CRUD Operations - - - - - - - - - - -

# Create category
def create_category_crud(db: Session, category: CategoryCreate):
    db_category = Category(parent_id=category.parent_id, name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Create location
def create_location_crud(db: Session, location: LocationCreate):
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

# Get all categories
def get_categories_crud(db: Session):
    return db.query(Category).all()

# Get all locations
def get_locations_crud(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()
