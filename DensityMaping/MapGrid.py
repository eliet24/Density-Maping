import math

from Business import Business
from Point import Point
from Square import Square


# class that holds the info about the best area for business location
class BestLocationInfo:
    def __init__(self, best_location_center: Point, best_profit: float, affected_squares_list: list):
        self.best_location_center = best_location_center
        self.best_profit = best_profit
        self.affected_squares_list = affected_squares_list

    def print_location_squares_info(self):
        for square in self.affected_squares_list:
            print(square.get_square_info())


class MapGrid:
    def __init__(self, x_axis_len, y_axis_len, scaled_square_len, grid_squares_values):
        self.scaled_square_len = scaled_square_len
        self.x_axis_len = x_axis_len
        self.y_axis_len = y_axis_len
        # 2D list (a list of lists) called self.grid, Initializing each element of the grid with a new Square object
        self.grid = [[Square(scaled_square_len, i, j, grid_squares_values[i][j]) for j in range(x_axis_len)] for i in
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
        for row in range(0, self.y_axis_len):
            for col in range(0, self.x_axis_len):
                temp_sum, scanned_squares_list = self.calc_square_sum(business_size_ratio, row, col, init_center, new_business.get_var(), scanned_squares_list)
                if temp_sum >= max_sum:  # if the new sum is better then the previous max
                    max_sum = temp_sum
                    # update the best area center found
                    cord_x = (col * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len
                    cord_y = (row * self.scaled_square_len) + ((business_size_ratio / 2) * self.scaled_square_len) - self.scaled_square_len
                    # clear the squares list of the previous best area
                    best_location_area.clear()
                    # append new squares list of the new best area
                    best_location_area.extend(scanned_squares_list[:])
                # update the x_index of the scanning center point
                init_center.set_x(init_center.get_x() + self.scaled_square_len)
        # update the y_index of the scanning center point
        init_center.set_y(init_center.get_y() + self.scaled_square_len)
        # Clear the scanned squares list after the loop
        scanned_squares_list.clear()

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

        for k in range(i, min(i + size_ratio, self.y_axis_len)):
            row_sum = 0
            for m in range(j, min(j + size_ratio, self.x_axis_len)):
                small_square_center = Point(m * self.scaled_square_len - (self.scaled_square_len / 2),
                                            k * self.scaled_square_len - (self.scaled_square_len / 2))
                dist_impact = self.calc_2_points_dist(midpoint, small_square_center)
                # row_sum += self.grid[k][m].get_value() * self.gauss_value(dist_impact, var)    # use For gauss calculations
                row_sum += self.grid[k][m].get_value()
                squares_list.append(self.grid[k][m])

            square_sum += row_sum
        return square_sum, squares_list

    def gauss_value(self, x, var):
        return (1 / (2 * 3.14159 * var) ** 0.5) * (2.71828 ** (-1 * (x ** 2) / (2 * var ** 2)))


def main():
    # Example usage
    x_axis_len = 4
    y_axis_len = 4
    scaled_square_len = 1
    grid_squares_values2 = [[1.0, 2.0, 3.0, 4.0],
                           [5.0, 13.0, 14.0, 8.0],
                           [9.0, 15.0, 16.0, 12.0],
                           [6.0, 7.0, 10.0, 11.0]]
    grid_squares_values = []
    num = 10000
    for i in range(y_axis_len):
        col = []
        for j in range(x_axis_len):
            col.append(num)
            num -= 1
        grid_squares_values.append(col)
    '''
    grid_squares_values = [[1.0, 2.0, 3.0,],
                           [4.0, 5.0, 6.0],
                           [7.0, 8.0, 9.0]]
   '''
    # Create an instance of MapGrid
    map_grid = MapGrid(x_axis_len, y_axis_len, scaled_square_len, grid_squares_values)

    # Example business data
    business_radius = 1.0
    business_center = Point(0.0, 0.0)
    new_business = Business(business_radius, business_center, 1, 50.0, 2, 3)

    # Find the best location for the new business
    best_location_info = map_grid.find_best_location(new_business)

    # Print the results
    print("Best Location Center:" + "(" , best_location_info.best_location_center.get_x(),",",best_location_info.best_location_center.get_y(), ")")
    print("Best Profit:", best_location_info.best_profit)
    best_location_info.print_location_squares_info()



# run Tests
main()
