from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from typing import Optional, List

# SQLAlchemy Base
Base = declarative_base()

# - - - - - - - - - - - Models - - - - - - - - - - -

# Users Table
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)

    locations = relationship("Location", back_populates="user")


# Categories Table
class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey('categories.category_id'), nullable=True)
    name = Column(String, nullable=False, unique=True, index=True)

    parent = relationship("Category", remote_side=[category_id], backref="subcategories")
    locations = relationship("Location", back_populates="category")


# Locations Table
class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    user = relationship("User", back_populates="locations")
    category = relationship("Category", back_populates="locations")


# - - - - - - - - - - - Schemas - - - - - - - - - - -

# User schema
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


# Category schema
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    category_id: int
    subcategories: List["Category"] = []

    class Config:
        orm_mode = True


# Location schema
class LocationBase(BaseModel):
    user_id: int
    category_id: int
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    location_id: int

    class Config:
        orm_mode = True
