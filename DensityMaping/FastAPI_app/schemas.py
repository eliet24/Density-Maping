from pydantic import BaseModel
from models import BusinessType, RelationshipStatus, Point, Square, Business, Customer, MapGrid
from typing import List, Dict, Optional
from datetime import date


class BusinessCreate(BaseModel):
    radius: float
    circle_center: Point
    business_id: int
    req_income: float
    business_type: BusinessType
    business_var: float
    found_income: float = 0.0
    business_squares_value_dist: Optional[Dict[Square, float]] = None


class CustomerCreate(BaseModel):
    cust_id: str
    cust_name: str
    cust_birth_date: date
    cust_income: float
    cust_relationship_status: RelationshipStatus
    cust_businesses: Optional[List[Business]] = []
    cust_saved_locations: Optional[List[Point]] = []


class MapGridCreate(BaseModel):
    grid_square_len: float
    x_axis_len: int
    y_axis_len: int
    grid: List[List[Square]]
