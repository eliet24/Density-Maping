from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import date


class BusinessType(Enum):
    FASHION = 1
    FOOD = 2
    HEALTH_AND_COSMETICS = 3
    ELECTRONICS = 4


class RelationshipStatus(Enum):
    MARRIED = 1
    BACHELOR = 2
    DIVORCE = 3
    IN_RELATIONSHIP = 4


class Point(BaseModel):
    x: float
    y: float


class Circle(BaseModel):
    radius: float
    circle_center: Point


class Square(BaseModel):
    square_len: float
    square_index_row: int
    square_index_column: int
    value: float
    square_value_dist: Dict[BusinessType, float] = Field(default_factory=lambda: {
        BusinessType.FOOD: 0.0,
        BusinessType.FASHION: 0.0,
        BusinessType.HEALTH_AND_COSMETICS: 0.0,
        BusinessType.ELECTRONICS: 0.0
    })
    business_on_square: Dict[BusinessType, int] = Field(default_factory=lambda: {
        BusinessType.FOOD: 0,
        BusinessType.FASHION: 0,
        BusinessType.HEALTH_AND_COSMETICS: 0,
        BusinessType.ELECTRONICS: 0
    })


class Business(Circle):
    business_id: int
    req_income: float
    business_type: BusinessType
    business_var: float
    found_income: float = 0.0
    business_squares_value_dist: Optional[Dict[Square, float]] = None


class Customer(BaseModel):
    cust_id: str
    cust_name: str
    cust_birth_date: date
    cust_income: float
    cust_relationship_status: RelationshipStatus
    cust_businesses: Optional[List[Business]] = []
    cust_saved_locations: Optional[List[Point]] = []


class MapGrid(BaseModel):
    grid_square_len: float
    x_axis_len: int
    y_axis_len: int
    grid: List[List[Square]]

    class Config:
        arbitrary_types_allowed = True
