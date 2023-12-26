
from enum import Enum
import math

from Circle import Circle
from Point import Point

"""
------------------------------------------------- Business -------------------------------------------------
Business Class: represents a Business inherits the Circle class
parameters:
Business_id: holds a int that represnts the business ID
req_income  : holds the requested income for the business
business_type : holds the business type by the businesses catagories that represented as enum in BusinessType Class
varience : holds the business normal distribution varience value
functions:
get_business_id,  get_req_profit, get_business_type, get_varience : getters for each of the Business class varibles
set_business_id, set_req_profit, set_business_type, set_varience : setters for each of the Business class varibles
find_init_center : returns the Business initialized center point by the business size for the location search start
-------------------------------------------------------------------------------------------------------------
"""


class BusinessType(Enum):
    FASHION = 1
    FOOD = 2
    HEALTH_AND_COSMETICS = 3
    ELECTRONICS = 4


class Business(Circle):
    def __init__(self, radius: float, center: Point, business_id: int, req_income : float, business_type: BusinessType, varience: float):
        super().__init__(radius, center)
        self.business_id = business_id
        self.req_income = req_income
        self.business_type = business_type
        self.varience = varience

    # getters
    def get_business_id(self):
        return self.business_id

    def get_req_profit(self):
        return self.req_profit

    def get_business_type(self):
        return self.business_type

    def get_varience(self):
        return self.varience

    # setters
    def set_business_id(self, b_id: int):
        self.business_id = b_id

    def set_req_profit(self, profit: int):
        self.req_profit = profit

    def set_business_type(self, business_type: BusinessType):
        self.business_type = business_type

    def set_varience(self, var: float):
        self.varience = var

    # functions

    # function for finding size ratio between business size and square grid size
    '''def find_size_ratio(self, map_grid):
        grid_square_length = len(map_grid[0][0])
        squared_business_len = self.circle_to_square()
        return int(math.floor(squared_business_len / grid_square_length))
    '''
    # function for finding the initialized business center on the MapGrid
    def find_init_center(self, size_ratio: int):
        return Point(size_ratio / 2 * self.circle_to_square(), size_ratio / 2 * self.circle_to_square())




