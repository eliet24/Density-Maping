import math

from Business import Business
from Point import Point
from Square import Square


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
        return

    def find_size_ratio(self, business: Business):
        return int(math.floor(business.circle_to_square() / self.scaled_square_len))

    def find_best_location(self, new_business: Business):
        cord_x, cord_y = 0, 0
        max_sum = 0
        business_size_ratio = self.find_size_ratio(new_business)
        init_center = new_business.find_init_center(business_size_ratio)

        for row in range(1, self.y_axis_len):
            for col in range(1, self.x_axis_len):
                temp_sum = self.calc_square_sum(business_size_ratio, row, col, init_center, new_business.get_var())
                if temp_sum >= max_sum:
                    max_sum = temp_sum
                    cord_x = (col * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len
                    cord_y = (row * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len

                init_center.set_x(init_center.get_x() + self.scaled_square_len)

        init_center.set_y(init_center.get_y() + self.scaled_square_len)

        best_center_found = Point(cord_x, cord_y)
        new_business.set_center(best_center_found)
        return best_center_found

    def calc_square_sum(self, size_ratio, i: int, j: int, midpoint: Point, var: float):
        row_sum, square_sum = 0, 0

        for k in range(i, size_ratio + i):
            row_sum = 0
            for l in range(j, size_ratio + j):
                square_center_x = l * self.scaled_square_len - (self.scaled_square_len / 2)
                square_center_y = k * self.scaled_square_len - (self.scaled_square_len / 2)
                small_square_center = Point(square_center_x, square_center_y)
                x = self.calc_2_points_dist(midpoint, small_square_center)
                row_sum += self.grid[k][l].get_value() * self.gauss_value(x, var)

            square_sum += row_sum

        return square_sum

    def gauss_value(self, x, var):
        gauss_func_x = (1 / (2 * 3.14159 * var) ** 0.5) * (2.71828 ** (-1 * (x ** 2) / (2 * var ** 2)))
        return gauss_func_x

