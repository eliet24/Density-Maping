
from enum import Enum
import math

from Circle import Circle
from Point import Point


class BusinessType(Enum):
    FASHION = 1
    FOOD = 2
    HEALTH_AND_COSMETICS = 3
    ELECTRONICS = 4


class Business(Circle):
    def __init__(self, radius: float, center: Point, business_id: int, profit: int, business_type: BusinessType, var: float):
        super().__init__(radius, center)
        self.business_id = business_id
        self.req_profit = profit
        self.business_type = business_type
        self.var = var

    # getters
    def get_business_id(self):
        return self.business_id

    def get_req_profit(self):
        return self.req_profit

    def get_business_type(self):
        return self.business_type

    def get_var(self):
        return self.var

    # setters
    def set_business_id(self, b_id: int):
        self.business_id = b_id

    def set_req_profit(self, profit: int):
        self.req_profit = profit

    def set_business_type(self, business_type: BusinessType):
        self.business_type = business_type

    def set_var(self, var: float):
        self.var = var

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




