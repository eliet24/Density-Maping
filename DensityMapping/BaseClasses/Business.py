from typing import Dict, Optional
from matplotlib import pyplot as plt
from .Circle import Circle
from .BusinessType import BusinessType
from .Square import Square
from .Point import Point
from pydantic import BaseModel


"""
------------------------------------------------- Business -------------------------------------------------
Business Class: represents a Business inherits the Circle class
parameters  :
Business_id :    holds a int that represents the business ID
req_income:    holds the requested income for the business
business_type:  holds the business type by the businesses categories that represented as enum in BusinessType Class
business_var:  holds the business normal distribution variance value
found_income:   holds the current business income
business_squares_value_dist : dictionary that maps the profit values that the business uses from every affected square.

functions:
get_business_id,  get_req_profit, get_business_type, get_variance : getters for each of the Business class variables
set_business_id, set_req_profit, set_business_type, set_variance : setters for each of the Business class variables
find_init_center : returns the Business initialized center point by the business size for the location search start
-------------------------------------------------------------------------------------------------------------
"""

class Business(Circle):
    business_id: int
    req_income: float
    business_type: BusinessType
    business_var: float
    found_income: float = 0.0
    business_squares_value_dist: Optional[Dict[Square, float]] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, radius: float, circle_center: Point, business_id: int, req_income: float,
                 business_type: BusinessType, business_var: float,
                 found_income: float = 0.0, business_squares_value_dist: Optional[Dict[Square, float]] = None):
        super().__init__(
            radius=radius,
            circle_center=circle_center,
            business_id=business_id,
            req_income=req_income,
            business_type=business_type,
            business_var=business_var,
            found_income=found_income,
            business_squares_value_dist=business_squares_value_dist
        )

    # getters and Setters
    def get_business_id(self):
        return self.business_id

    def get_req_income(self):
        return self.req_income

    def get_business_type(self):
        return self.business_type

    def get_variance(self):
        return self.business_var

    # setters
    def set_business_id(self, b_id: int):
        self.business_id = b_id

    def set_req_income(self, income: int):
        self.req_income = income

    def set_business_type(self, business_type: BusinessType):
        self.business_type = business_type

    def set_variance(self, var: float):
        self.business_var = var

    # function for finding the initialized business center on the MapGrid
    def find_init_center(self, size_ratio: int):
        return Point(x=size_ratio / 2 * self.circle_to_square(), y=size_ratio / 2 * self.circle_to_square())


