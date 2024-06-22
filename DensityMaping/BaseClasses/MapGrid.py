import math
from typing import List

import numpy as np

from Business import Business
from Point import Point
from Square import Square
import cProfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pydantic import BaseModel, Field
"""
------------------------------------------------- BestLocationInfo -------------------------------------------------
BestLocationInfo Class: class that holds all the information of the best location for a business
parameters:
best_location_center : holds the Point that is the center of the best location for the business
best_income_found : holds the best profit found for the business
affected_squares_list : [list] that holds all the squares that affected in the location that found
functions:
print_location_squares_info: print all the square's information in the area
-------------------------------------------------------------------------------------------------------------
"""


# class that holds the info about the best area for business location
class BestLocationInfo(BaseModel):
    best_location_center: Point
    best_income_found: float
    affected_squares: List[Square]

    def print_location_info(self):
        print("Best Location Center:", end=" ")
        self.best_location_center.print_point()
        print("Best Income Found " + str(self.best_income_found))
        for square in self.affected_squares:
            square.get_square_info()


"""
# should be changed by Attraction and repulsion between businesses
------------------------------------------------- MapGrid -------------------------------------------------
MapGrid Class: represents the Grid that maps the physical and economic space. consists of Squares.
parameters:
grid_square_len : holds the len of each of the grid's square edge length.
x_axis_len : holds the length of the full x_axis of the Grid
y_axis_len : holds the length of the full y_axis of the Grid
grid: holds the actual 2D list of lists that holds a rows of squares.
functions:
calc_2_squares_dist : calculate and return the distance length of 2 squares centers on the grid -> [float]
                      using the calc_2_points_dist() function
calc_2_points_dist : calculate and return the distance between 2 points on the grid.
find_size_ratio : calculate and return the size ration between the business circles edge length represntation and 
                  the length of the grid's square, important sizes matching for the start of the search algorithm.
find_best_location: gets a Business class object and find for him the best location on the grid 
                    return object of the locations info -> [BestLocationInfo]
calc_square_sum : calculate a square area on the grid which is built from Square objects return the area sum and
                  the area Suares list -> [float, list[Squares]]
gauss_value : calculate the value of the gauss distribution at a certain distance from the mean (business center point)
-------------------------------------------------------------------------------------------------------------
"""


class MapGrid(BaseModel):
    grid_square_len: float
    x_axis_len: int
    y_axis_len: int
    grid: List[List[Square]]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, x_axis_len: int, y_axis_len: int, grid_square_len: float, grid_squares_values: List[List[float]]):
        super().__init__(
            grid_square_len=grid_square_len,
            x_axis_len=x_axis_len,
            y_axis_len=y_axis_len,
            grid=[[Square(square_len=grid_square_len, square_index_row=i, square_index_column=j, value=grid_squares_values[i][j])
                   for j in range(x_axis_len)] for i in range(y_axis_len)]
        )

    def print_grid_values(self):
        print("\n------------The Map Grid values:------------")
        for row in self.grid:
            print(' '.join(map(lambda x: str(x) if x % 1 != 0 else str(int(x)), [square.value for square in row])))
        print("--------------------------------------------\n")

    def calc_2_squares_dist(self, square1: Square, square2: Square):
        return self.calc_2_points_dist(square1.calc_square_center(), square2.calc_square_center())

    def calc_2_points_dist(self, a: Point, b: Point):
        return abs(((a.get_y() - b.get_y()) ** 2 + (a.get_x() - b.get_x()) ** 2) ** 0.5)

    def find_size_ratio(self, business: Business):
        return int(math.floor(business.circle_to_square() / self.grid_square_len))

    def find_best_location(self, new_business: Business) -> BestLocationInfo:
        """
        function that calculates the best location for new business and return BestLocation object member
        """
        cord_x, cord_y = 0, 0
        max_sum = 0
        business_size_ratio = self.find_size_ratio(new_business)
        init_center = new_business.find_init_center(business_size_ratio)
        scanned_squares_list = []
        best_location_area = []

        for row in range(0, self.y_axis_len):
            for col in range(0, self.x_axis_len):
                temp_sum, scanned_squares_list = self.calc_square_sum(business_size_ratio, row, col, init_center, new_business.get_varience(), scanned_squares_list)
                if temp_sum >= max_sum:  # if the new sum is better than the previous max
                    max_sum = temp_sum

                    # update the best area center found
                    cord_x = (col * self.grid_square_len) + ((business_size_ratio / 2) * self.grid_square_len) - self.grid_square_len + 1
                    cord_y = (row * self.grid_square_len) + ((business_size_ratio / 2) * self.grid_square_len) - self.grid_square_len + 1

                    # clear the squares list of the previous best area
                    best_location_area.clear()
                    # append new squares list of the new best area
                    best_location_area.extend(scanned_squares_list[:])

                # update the x_index of the scanning center point
                init_center.set_x(init_center.get_x() + self.grid_square_len)
                # Clear the scanned squares list each iteration
                scanned_squares_list.clear()
            # update the y_index of the scanning center point
            init_center.set_y(init_center.get_y() + self.grid_square_len)
            # Clear the scanned squares list after the loop
            # scanned_squares_list.clear()

        best_center_found = Point(x=cord_x, y=cord_y)
        best_area_info = BestLocationInfo(best_location_center=best_center_found, best_income_found=max_sum, affected_squares=best_location_area)
        # return BestLocationInfo object that stores all the data
        return best_area_info

    def find_locations(self, new_business: Business) -> list[BestLocationInfo]:
        """
        function that calculates the suitable locations for new business and return list of BestLocationinfo objects
        """
        business_size_ratio = self.find_size_ratio(new_business)
        init_center = new_business.find_init_center(business_size_ratio)
        scanned_squares_list = []
        location_area = []
        suitable_locations = []
        for row in range(0, self.y_axis_len):
            for col in range(0, self.x_axis_len):
                temp_sum, scanned_squares_list = self.calc_square_sum(business_size_ratio, row, col, init_center,
                                                                      new_business.get_varience(), scanned_squares_list)
                if temp_sum >= new_business.get_req_income():  # if the calculated sum is better than the req income
                    # update the best area center found
                    cord_x = (col * self.grid_square_len) + (
                                (business_size_ratio / 2) * self.grid_square_len) - self.grid_square_len + 1
                    cord_y = (row * self.grid_square_len) + (
                                (business_size_ratio / 2) * self.grid_square_len) - self.grid_square_len + 1

                    # clear the squares list of the previous best area
                    location_area.clear()
                    # append new squares list of the new best area
                    location_area.extend(scanned_squares_list[:])
                    area_info = BestLocationInfo(Point(cord_x, cord_y), temp_sum, location_area)
                    suitable_locations.append(area_info)
                    # return BestLocationInfo object that stores all the data
                # update the x_index of the scanning center point
                init_center.set_x(init_center.get_x() + self.grid_square_len)
                # Clear the scanned squares list each iteration
                scanned_squares_list.clear()
            # update the y_index of the scanning center point
            init_center.set_y(init_center.get_y() + self.grid_square_len)

        return suitable_locations

    def print_all_found_locations_info(self, found_locations: list[BestLocationInfo]):
        for location in found_locations:
            location.print_location_info()

    def calc_square_sum(self, size_ratio: int, i: int, j: int, midpoint: Point, var: float, squares_list: list):
        """
        for claculating sum of sub area inside the grid returns the profit calculated (square_sum)
        and list of the scanned squares
        """
        square_sum = 0
        squares_list.clear()
        for k in range(i, min(i + size_ratio, self.y_axis_len)):
            row_sum = 0
            for m in range(j, min(j + size_ratio, self.x_axis_len)):
                small_square_center = Point(x=m * self.grid_square_len - (self.grid_square_len / 2) + size_ratio,
                                            y=k * self.grid_square_len - (self.grid_square_len / 2) + size_ratio)
                dist_impact = self.calc_2_points_dist(midpoint, small_square_center)
                # row_sum += self.grid[k][m].get_value() * self.gauss_value(dist_impact, var)    # use For calculation with gauss
                row_sum += self.grid[k][m].get_value()        # use for calculation without gauss
                squares_list.append(self.grid[k][m])
            square_sum += row_sum
        return square_sum, squares_list

    def gauss_value(self, r, var) -> float:
        """
        calculate the gauss value by the variance of the business and specific distance from it
        """
        return (1 / (2 * 3.14159 * var) ** 0.5) * (2.71828 ** (-1 * (r ** 2) / (2 * var ** 2)))

    def put_business_on_grid(self, business: Business, placement: BestLocationInfo):
        """
        initialize best found income value to business and
        update affected by the business squares values (should be changed by correlation to businesses affectivness)
        """
        # set the location of the new business (center point)
        business.set_center(placement.best_location_center)
        business.found_income = placement.best_income_found
        # varible for checking that the effectivness distribution in the area is correct
        income_dist_check = business.found_income
        print(income_dist_check)
        for affected_square in placement.affected_squares:
            '''
            affected_square.value -= affected_square.get_value() * self.gauss_value(
                        self.calc_2_points_dist(placement.best_location_center, affected_square.square_center_point()),
                        business.get_varience())
            income_dist_check -= affected_square.get_value() * self.gauss_value(
                        self.calc_2_points_dist(placement.best_location_center, affected_square.square_center_point()),
                        business.get_varience())
            '''
            income_dist_check -= affected_square.get_value()
            affected_square.value -= affected_square.get_value()

        if income_dist_check != 0:
            print("The affected squares have not been modified correctly! please check!")
            print(income_dist_check)

    # Visualization function inside MapGrid class

    def visualize_grid(self, ax):
        # Clear the existing grid
        ax.clear()

        # Draw grid squares
        for row in self.grid:
            for square in row:
                square_rect = patches.Rectangle((square.square_index_column, square.square_index_row),
                                                self.grid_square_len, self.grid_square_len,
                                                linewidth=1, edgecolor='black', facecolor='none')
                ax.add_patch(square_rect)
                ax.text(square.square_index_column * self.grid_square_len + 0.5 * self.grid_square_len, square.square_index_row * self.grid_square_len + 0.5 * self.grid_square_len,
                        f"{square.value:.1f}", ha='center', va='center', fontsize=6)

        # Set plot limits and aspect ratio
        ax.set_xlim(0, self.x_axis_len * self.grid_square_len)
        ax.set_ylim(0, self.y_axis_len * self.grid_square_len)
        ax.set_aspect('equal', 'box')
        ax.invert_yaxis()  # Invert y axis to match the grid layout

        # Configure ticks and grid lines
        ax.set_xticks(np.arange(0, (self.x_axis_len + 1) * self.grid_square_len, self.grid_square_len))
        ax.set_yticks(np.arange(0, (self.y_axis_len + 1) * self.grid_square_len, self.grid_square_len))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    def visualize_bizns_on_grid(self, ax, businesses: list):
        # Draw businesses as circles
        for business in businesses:
            circle = patches.Circle((business.circle_center.get_x(), business.circle_center.get_y()),
                                    business.radius, linewidth=1, edgecolor='red', facecolor='none')
            ax.add_patch(circle)
            ax.text(business.circle_center.get_x(), business.circle_center.get_y(),
                    f"B{business.business_id}", ha='center', va='center', color='red')

        ax.figure.canvas.draw()  # Redraw the canvas to update with new elements



