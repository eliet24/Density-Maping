from MapGrid import BestLocationInfo, MapGrid
import math
import numpy as np
from Business import Business, BusinessType
from Point import Point
from Square import Square
import cProfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def main():
    # Example usage
    x_axis_len = 4
    y_axis_len = 4
    x_axis_len2 = 10
    y_axis_len2 = 10
    scaled_square_len = 1

    grid_squares_values2 = [[100.0, 2.0, 3.0, 4.0],
                           [5.0, 13.0, 13.0, 18.0],
                           [9.0, 15.0, 60.0, 30.0],
                           [6.0, 7.0, 10.0, 11.0]]

    grid_squares_values = []
    num = 25
    for i in range(y_axis_len):
        col = []
        for j in range(x_axis_len):
            col.append(num)
            num -= 1
        grid_squares_values.append(col)

    grid_squares_values3 = [[9, 2.0, 3.0, 4.0, 1, 3, 1, 3, 1, 3],
                            [10, 2.0, 3.0, 4.0, 1, 3, 1, 3, 1, 3],
                            [11, 2.0, 3.0, 4.0, 1, 3, 1, 3, 1, 3],
                            [12.0, 3.0, 4.0, 5, 1, 3, 1, 3, 1, 3],
                            [13.0, 2.0, 3.0, 4.0,1,3,1,3,1,3],
                            [14.0, 2.0, 3.0, 4.0,1,3,1,3,1,3],
                            [100.0, 2.0, 3.0, 4.0,1,3,1,3,1,3],
                            [5.0, 13.0, 13.0, 18.0, 1,3,1,3,1,3],
                            [9.0, 15.0, 60.0, 30.0,1,3,1,3,1,3],
                            [6.0, 7.0, 10.0, 11.0, 1,3,1,3,1,3]]

    # Create an instance of MapGrid
    # map_grid = MapGrid(x_axis_len, y_axis_len, scaled_square_len, grid_squares_values2)
    map_grid = MapGrid(x_axis_len2, y_axis_len2, scaled_square_len, grid_squares_values3)
    map_grid.print_grid_values()
    # Example business data
    business_radius = 1
    business_center = Point(0.0, 0.0)
    new_business = Business(business_radius, business_center, 1, 50.0, 2, 3)
    new_business2 = Business(business_radius, business_center, 1, 42.0, 2, 3)

    # Find the best location for the new business
    best_location_info = map_grid.find_best_location(new_business)

    # Print the results
    best_location_info.print_location_info()
    map_grid.put_business_on_grid(new_business, best_location_info)
    map_grid.print_grid_values()

    map_grid.visualize_grid([new_business])

    # Find 2nd the best location for the new business

    best_location_info2 = map_grid.find_best_location(new_business2)
    best_location_info2.print_location_info()
    map_grid.put_business_on_grid(new_business2, best_location_info2)
    map_grid.print_grid_values()

    map_grid.visualize_grid([new_business2])


    ''' 
    # --------------- For Testing getting list of best locations -----------------
    best_locations = map_grid.find_locations(new_business2)
    map_grid.print_all_found_locations_info(best_locations)
    map_grid.put_business_on_grid(new_business2, best_locations[0])
    map_grid.print_grid_values()
    map_grid.visualize_grid([new_business2])
    '''


# run Tests
main()
# cProfile.run('main()')