import math

from Business import Business
from Point import Point
from Square import Square


# class that holds the info about the best area for business location
class BestLocationInfo:
    def __init__(self, best_location_center: Point, best_profit: float, affected_squares_list: list):
        self.best_location_center = best_location_center
        self.best_profit = best_profit
        for i in affected_squares_list:
            self.affected_squares_list.append(affected_squares_list.pop(i))


class MapGrid:
    def __init__(self, x_axis_len, y_axis_len, scaled_square_len, grid_squares_values):
        self.scaled_square_len = scaled_square_len
        self.x_axis_len = x_axis_len
        self.y_axis_len = y_axis_len
        # 2D list (a list of lists) called self.grid, Initializing each element of the grid with a new Square object
        self.grid = [[Square(scaled_square_len, i, j, grid_squares_values[i + j]) for j in range(x_axis_len)] for i in
                     range(y_axis_len)]

    def calc_2_squares_dist(self, square1: Square, square2: Square):
        return self.calc_2_points_dist(square1.calc_square_center(), square2.calc_square_center())

    def calc_2_points_dist(self, a: Point, b: Point):
        return abs(((a.get_y() - b.get_y()) ** 2 + (a.get_x() - b.get_x()) ** 2) ** 0.5)

    def find_size_ratio(self, business: Business):
        return int(math.floor(business.circle_to_square() / self.scaled_square_len))

    # function that calculates the best location for new business and return BestLocation object member
    def find_best_location(self, new_business: Business):
        cord_x, cord_y = 0, 0
        max_sum = 0
        business_size_ratio = self.find_size_ratio(new_business)
        init_center = new_business.find_init_center(business_size_ratio)
        scanned_squares_list = []
        best_location_area = []
        for row in range(1, self.y_axis_len):
            for col in range(1, self.x_axis_len):
                temp_sum, scanned_squares_list = self.calc_square_sum(business_size_ratio, row, col, init_center, new_business.get_var(), scanned_squares_list)
                if temp_sum >= max_sum:  # if the new sum is better then the previous max
                    max_sum = temp_sum
                    # update the best area center found
                    cord_x = (col * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len
                    cord_y = (row * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len
                    # clear the squares list of the previous best area
                    for i in best_location_area:
                        best_location_area.pop(i)
                    # append new squares list of the new best area
                    for j in scanned_squares_list:
                        best_location_area.append(scanned_squares_list.pop(j))
                # update the x_index of the scanning center point
                init_center.set_x(init_center.get_x() + self.scaled_square_len)
        # update the y_index of the scanning center point
        init_center.set_y(init_center.get_y() + self.scaled_square_len)

        best_center_found = Point(cord_x, cord_y)
        best_area_info = BestLocationInfo(Point(cord_x, cord_y), max_sum, best_location_area)
        # set the location of the new business (center point)
        new_business.set_center(best_center_found)
        # return BestLocationInfo object that stores all the data
        return best_area_info

    # function for claculating sum of sub area inside of the grid returns the profit calculated (square_sum)
    # and list of the scanned squares
    def calc_square_sum(self, size_ratio: int, i: int, j: int, midpoint: Point, var: float, squares_list: list):
        square_sum = 0
        squares_list.clear()

        for k in range(i, size_ratio + i):
            row_sum = 0
            for m in range(j, size_ratio + j):
                small_square_center = Point(m * self.scaled_square_len - (self.scaled_square_len / 2),
                                            k * self.scaled_square_len - (self.scaled_square_len / 2))
                dist_impact = self.calc_2_points_dist(midpoint, small_square_center)
                row_sum += self.grid[k][m].get_value() * self.gauss_value(dist_impact, var)
                squares_list.append(self.grid[k][m])

            square_sum += row_sum
        return square_sum, squares_list

    def gauss_value(self, x, var):
        return (1 / (2 * 3.14159 * var) ** 0.5) * (2.71828 ** (-1 * (x ** 2) / (2 * var ** 2)))


