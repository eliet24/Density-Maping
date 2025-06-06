import math
from typing import Optional, Dict, TYPE_CHECKING
from .BusinessType import BusinessType
from .Point import Point
from pydantic import BaseModel, Field
"""
------------------------------------------ Square ----------------------------------------------
Square Class: represents a Square that is the building block of the Grid
parameters:
square_len : length of square's edge
square_index_row : the row's index in which the square located on the grid
square_index_column : the column's index in which the square located on the grid
value : holds the square's value, the revenue - purchasing power on the square
Business_on_square : dictionary that maps the number of Businesses of each type that affect the square.
square_value_dist : dictionary that maps the value of profit taken from the square by each kind of business.
functions:
get_length, get_value,get_row, get_business_on_square : getters for each of the Square class varibles
set_length, set_value, set_row, set_column : setters ffor each of the Square class varibles
square_center_point : calculating and returns the square's center Point -> [Point]
calc_diagonal : calculates and returns the length of the squares diagonal -> [float]
get_square_info: returns the square's info as a string -> [string]
------------------------------------------------------------------------------------------------
"""


class Square(BaseModel):
    square_len: float
    square_index_row: int
    square_index_column: int
    value: float
    businessTypes_values_dist: Dict[BusinessType, float] = Field(default_factory=lambda: {
        BusinessType.FASHION: 0.0,
        BusinessType.FOOD: 0.0,
        BusinessType.HEALTH_AND_WELLNESS: 0.0,
        BusinessType.ELECTRONICS_AND_TECH: 0.0,
        BusinessType.BEAUTY_AND_PERSONAL_CARE: 0.0,
        BusinessType.AUTOMOTIVE: 0.0,
        BusinessType.FINANCE_AND_INSURANCE: 0.0,
        BusinessType.ENTERTAINMENT_AND_MEDIA: 0.0,
        BusinessType.EDUCATION: 0.0,
        BusinessType.HOSPITALITY_AND_TOURISM: 0.0,
        BusinessType.AGRICULTURE_AND_FARMING: 0.0,
        BusinessType.LEGAL_SERVICES: 0.0,
        BusinessType.NIGHTLIFE: 0.0,
        BusinessType.PETS_AND_ANIMALS: 0.0
    })
    businessTypes_on_square: Dict[BusinessType, int] = Field(default_factory=lambda: {
        BusinessType.FASHION: 0.0,
        BusinessType.FOOD: 0.0,
        BusinessType.HEALTH_AND_WELLNESS: 0.0,
        BusinessType.ELECTRONICS_AND_TECH: 0.0,
        BusinessType.BEAUTY_AND_PERSONAL_CARE: 0.0,
        BusinessType.AUTOMOTIVE: 0.0,
        BusinessType.FINANCE_AND_INSURANCE: 0.0,
        BusinessType.ENTERTAINMENT_AND_MEDIA: 0.0,
        BusinessType.EDUCATION: 0.0,
        BusinessType.HOSPITALITY_AND_TOURISM: 0.0,
        BusinessType.AGRICULTURE_AND_FARMING: 0.0,
        BusinessType.LEGAL_SERVICES: 0.0,
        BusinessType.NIGHTLIFE: 0.0,
        BusinessType.PETS_AND_ANIMALS: 0.0
    })

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, square_len: float, square_index_row: int, square_index_column: int, value: float,
                 businesstypes_values_dist: Dict[BusinessType, float] = None,
                 businesstypes_on_square: Dict[BusinessType, int] = None):
        super().__init__(square_len=square_len, square_index_row=square_index_row,
                         square_index_column=square_index_column, value=value)

        if businesstypes_values_dist is None:
            self.businessTypes_values_dist = {
                BusinessType.FASHION: value,
                BusinessType.FOOD: value,
                BusinessType.HEALTH_AND_WELLNESS: value,
                BusinessType.ELECTRONICS_AND_TECH: value,
                BusinessType.BEAUTY_AND_PERSONAL_CARE: value,
                BusinessType.AUTOMOTIVE: value,
                BusinessType.FINANCE_AND_INSURANCE: value,
                BusinessType.ENTERTAINMENT_AND_MEDIA: value,
                BusinessType.EDUCATION: value,
                BusinessType.HOSPITALITY_AND_TOURISM: value,
                BusinessType.AGRICULTURE_AND_FARMING: value,
                BusinessType.LEGAL_SERVICES: value,
                BusinessType.NIGHTLIFE: value,
                BusinessType.PETS_AND_ANIMALS: value,
            }
        else:
            self.businessTypes_values_dist = businesstypes_values_dist

        if businesstypes_on_square is None:
            self.businessTypes_on_square = {
                BusinessType.FASHION: 1,
                BusinessType.FOOD: 1,
                BusinessType.HEALTH_AND_WELLNESS: 1,
                BusinessType.ELECTRONICS_AND_TECH: 1,
                BusinessType.BEAUTY_AND_PERSONAL_CARE: 1,
                BusinessType.AUTOMOTIVE: 1,
                BusinessType.FINANCE_AND_INSURANCE: 1,
                BusinessType.ENTERTAINMENT_AND_MEDIA: 1,
                BusinessType.EDUCATION: 1,
                BusinessType.HOSPITALITY_AND_TOURISM: 1,
                BusinessType.AGRICULTURE_AND_FARMING: 1,
                BusinessType.LEGAL_SERVICES: 1,
                BusinessType.NIGHTLIFE: 1,
                BusinessType.PETS_AND_ANIMALS: 1,
            }
        else:
            self.businessTypes_on_square = businesstypes_on_square


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
            x=self.square_len * (self.square_index_column + 1) - (self.square_len / 2),
            y=self.square_len * (self.square_index_row + 1) - (self.square_len / 2))
        return square_center

    def calc_diagonal(self):
        return math.sqrt(2) * self.square_len

    def get_square_info(self):
        # return f"Square at grid index ({self.square_index_row}, {self.square_index_column}) with value {self.value}"
        print(
            f"Square at grid index ({self.square_index_column}, {self.square_index_row}) with value {self.value} with center point:")
        self.square_center_point().print_point()

    def get_value_by_businessType(self, business_type: BusinessType):
        return self.businessTypes_values_dist[business_type]

    def set_value_by_BusinessType(self, business_type: BusinessType, value: float):
        self.businessTypes_values_dist[business_type] = value

    def get_number_of_businesses(self, business_type: BusinessType):
        return self.businessTypes_on_square[business_type]

    def increment_number_of_businesses(self, business_type: BusinessType):
        self.businessTypes_on_square[business_type] += 1

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
