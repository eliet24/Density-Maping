
import math
import numpy as np
from Business import BusinessType
from Point import Point

"""
------------------------------------------ Square ----------------------------------------------
Square Class: represents a Square that is the building block of the Grid
parameters:
square_len : length of square's edge
square_index_row : the row's index in which the square located on the grid
square_index_column : the column's index in which the square located on the grid
value : holds the square's value, the revenue - purchasing power on the square
Business_on_square : dictionary that maps the number of Businesses of each type that affect the square.
functions:
get_length, get_value,get_row, get_business_on_square : getters for each of the Square class varibles
set_length, set_value, set_row, set_column : setters ffor each of the Square class varibles
square_center_point : calculating and returns the square's center Point -> [Point]
calc_diagonal : calculates and returns the length of the squares diagonal -> [float]
get_square_info: returns the square's info as a string -> [string]
------------------------------------------------------------------------------------------------
"""


class Square:
    def __init__(self, square_len: float, square_index_row: int, square_index_column: int, value: float):
        self.square_len = square_len
        self.square_index_row = square_index_row
        self.square_index_column = square_index_column
        self.value = value
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

    def square_center_point(self):
        square_center = Point(
            self.square_len * (self.square_index_column + 1) - (self.square_len / 2),
            self.square_len * (self.square_index_row + 1) - (self.square_len / 2))
        return square_center

    def calc_diagonal(self):
        return math.sqrt(2) * self.square_len

    def get_square_info(self):
        # return f"Square at grid index ({self.square_index_row}, {self.square_index_column}) with value {self.value}"
        print(f"Square at grid index ({self.square_index_column}, {self.square_index_row}) with value {self.value} with center point:")
        self.square_center_point().print_point()

    # For simulation
    def plot_square(self):
        """
        Plot a text-based representation of the square.
        """
        print(f"Square at grid index ({self.square_index_column}, {self.square_index_row}) with value {self.value}:")

        for i in range(int(self.square_len)):
            row_values = []
            for j in range(int(self.square_len)):
                row_values.append(str(self.value))
            print(" ".join(row_values))