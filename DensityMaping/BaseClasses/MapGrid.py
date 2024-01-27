import math
import numpy as np
from Business import Business
from Point import Point
from Square import Square
import cProfile

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
class BestLocationInfo:
    def __init__(self, best_location_center: Point, best_income_found: float, affected_squares_list: list[Square]):
        self.best_location_center = best_location_center
        self.best_income_found = best_income_found
        self.affected_squares_list = affected_squares_list

    def print_location_info(self):
        print("Best Location Center:", end=" ")
        self.best_location_center.print_point()
        print("Best Income Found " + str(self.best_income_found))
        for square in self.affected_squares_list:
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


class MapGrid:
    def __init__(self, x_axis_len: float, y_axis_len: float, grid_square_len: float, grid_squares_values: list[list]):
        self.grid_square_len = grid_square_len
        self.x_axis_len = x_axis_len
        self.y_axis_len = y_axis_len
        # 2D list (a list of lists) called self.grid, Initializing each element of the grid with a new Square object
        self.grid = [[Square(grid_square_len, i, j, grid_squares_values[i][j]) for j in range(x_axis_len)] for i in
                     range(y_axis_len)]

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
        '''
         function that calculates the best location for new business and return BestLocation object member
        '''
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

        best_center_found = Point(cord_x, cord_y)
        best_area_info = BestLocationInfo(best_center_found, max_sum, best_location_area)
        # return BestLocationInfo object that stores all the data
        return best_area_info

    def find_locations(self, new_business: Business) -> list[BestLocationInfo]:
        business_size_ratio = self.find_size_ratio(new_business)
        init_center = new_business.find_init_center(business_size_ratio)
        scanned_squares_list = []
        location_area = []
        appropriate_locations = []
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
                    appropriate_locations.append(area_info)
                    # return BestLocationInfo object that stores all the data
                # update the x_index of the scanning center point
                init_center.set_x(init_center.get_x() + self.grid_square_len)
                # Clear the scanned squares list each iteration
                scanned_squares_list.clear()
            # update the y_index of the scanning center point
            init_center.set_y(init_center.get_y() + self.grid_square_len)

        return appropriate_locations

    def print_all_found_locations_info(self, found_locations: list[BestLocationInfo]):
        for location in found_locations:
            location.print_location_info()

    def calc_square_sum(self, size_ratio: int, i: int, j: int, midpoint: Point, var: float, squares_list: list):
        '''
        for claculating sum of sub area inside the grid returns the profit calculated (square_sum)
        and list of the scanned squares
        '''
        square_sum = 0
        squares_list.clear()
        for k in range(i, min(i + size_ratio, self.y_axis_len)):
            row_sum = 0
            for m in range(j, min(j + size_ratio, self.x_axis_len)):
                small_square_center = Point(m * self.grid_square_len - (self.grid_square_len / 2) + size_ratio,
                                            k * self.grid_square_len - (self.grid_square_len / 2) + size_ratio)
                dist_impact = self.calc_2_points_dist(midpoint, small_square_center)
                # row_sum += self.grid[k][m].get_value() * self.gauss_value(dist_impact, var)    # use For calculation with gauss
                row_sum += self.grid[k][m].get_value()        # use for calculation without gauss
                squares_list.append(self.grid[k][m])
            square_sum += row_sum
        return square_sum, squares_list

    def gauss_value(self, r, var):
        '''
        calculate the gauss value by the variance of the business and specific distance from it
        '''
        return (1 / (2 * 3.14159 * var) ** 0.5) * (2.71828 ** (-1 * (r ** 2) / (2 * var ** 2)))

    def put_business_on_grid(self, business: Business, placement: BestLocationInfo):
        '''
        initialize best found income value to business and
        update affected by the business squares values (should be changed by correlation to businesses affectivness)
        '''
        # set the location of the new business (center point)
        business.set_center(placement.best_location_center)
        business.found_income = placement.best_income_found
        # varible for checking that the effectivness distribution in the area is correct
        income_dist_check = business.found_income
        print(income_dist_check)
        for affected_square in placement.affected_squares_list:
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



        # ------------------------> Continue Here <------------------------



def main():
    # Example usage
    x_axis_len = 4
    y_axis_len = 4
    scaled_square_len = 1
    '''grid_squares_values2 = [[1.0, 2.0, 3.0, 4.0],
                           [5.0, 13.0, 14.0, 8.0],
                           [9.0, 15.0, 16.0, 12.0],
                           [6.0, 7.0, 10.0, 11.0]]'''
    grid_squares_values2 = [[100.0, 2.0, 3.0, 4.0],
                           [5.0, 13.0, 13.0, 18.0],
                           [9.0, 15.0, 60.0, 30.0],
                           [6.0, 7.0, 10.0, 11.0]]

    '''   grid_squares_values2 = [[100.0, 2.0, 3.0, 4.0],
                           [5.0, 13.0, 13.0, 18.0],
                           [9.0, 15.0, 9.0, 30.0],
                           [6.0, 7.0, 10.0, 11.0]]'''
    grid_squares_values = []
    num = 25
    for i in range(y_axis_len):
        col = []
        for j in range(x_axis_len):
            col.append(num)
            num -= 1
        grid_squares_values.append(col)

    # Create an instance of MapGrid
    map_grid = MapGrid(x_axis_len, y_axis_len, scaled_square_len, grid_squares_values2)
    map_grid.print_grid_values()
    # Example business data
    business_radius = 1
    business_center = Point(0.0, 0.0)
    new_business = Business(business_radius, business_center, 1, 50.0, 2, 3)
    new_business2 = Business(business_radius, business_center, 1, 110.0, 2, 3)

    # Find the best location for the new business
    best_location_info = map_grid.find_best_location(new_business)

    # Print the results
    best_location_info.print_location_info()
    map_grid.put_business_on_grid(new_business, best_location_info)
    map_grid.print_grid_values()


    # Find 2nd the best location for the new business
    #best_location_info = map_grid.find_best_location(new_business)

    # Print the results
    best_location_info.print_location_info()
    map_grid.put_business_on_grid(new_business, best_location_info)
    map_grid.print_grid_values()

    best_locations = map_grid.find_locations(new_business2)
    map_grid.print_all_found_locations_info(best_locations)
    map_grid.put_business_on_grid(new_business2, best_locations[0])
    map_grid.print_grid_values()

# run Tests
main()
# cProfile.run('main()')
