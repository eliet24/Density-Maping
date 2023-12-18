
import math

from Business import BusinessType
from Point import Point


class Square:
    def __init__(self, square_len: float, square_index_row: int, square_index_column: int, val: float):
        self.square_len = square_len
        self.square_index_row = square_index_row
        self.square_index_column = square_index_column
        self.value = val
        self.business_on_square = {
            BusinessType.FOOD: 0,
            BusinessType.FASHION: 0,
            BusinessType.HEALTH_AND_COSMETICS: 0,
            BusinessType.ELECTRONICS: 0
        }

    # getters & setters
    def get_length(self):
        return self.square_len

    def get_value(self):
        return self.value

    def get_row(self):
        return self.square_index_row

    def get_column(self):
        return self.square_index_column

    def get_business_on_square(self):
        return self.business_on_square

    def set_length(self, length: float):
        self.square_len = length

    def set_value(self, val: float):
        self.value = val

    def set_row(self, row: int):
        self.square_index_row = row

    def set_column(self, col: int):
        self.square_index_column = col

    # functions
    def square_center_point(self):
        square_center = Point(
            self.square_len * self.square_index_column - (self.square_len / 2),
            self.square_len * self.square_index_row - (self.square_len / 2)
        )
        return square_center

    def calc_diagonal(self):
        return math.sqrt(2) * self.square_len

    def get_square_info(self):
        return f"Square at grid index ({self.square_index_row}, {self.square_index_column}) with value {self.value}"
