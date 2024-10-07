import math
import numpy as np
import matplotlib.pyplot as plt
from Business import Business, BusinessType
from Point import Point
from Square import Square
from MapGrid import MapGrid, BestLocationInfo

# ... (your existing code)

class Simulation:
    def __init__(self, map_grid):
        self.map_grid = map_grid
        self.fig, self.ax = plt.subplots()

    def plot_grid(self):
        for row in self.map_grid.grid:
            for square in row:
                square.plot_square()

    def plot_business(self, business):
        business.plot_business()

    def animate_simulation(self, business, best_location_info):
        # Animate the movement of the business and highlight the best location
        self.ax.clear()
        self.plot_grid()
        self.plot_business(business)

        for i in range(len(best_location_info.affected_squares_list)):
            square = best_location_info.affected_squares_list[i]
            square.plot_square(self.ax, color='red', alpha=0.5)

        plt.pause(0.1)

    def run_simulation(self, business):
        best_location_info = self.map_grid.find_best_location(business)
        self.plot_grid()
        self.plot_business(business)
        plt.pause(0.1)

        for i in range(len(best_location_info.affected_squares_list)):
            square = best_location_info.affected_squares_list[i]
            square.plot_square(self.ax, color='red', alpha=0.5)

        plt.pause(0.1)

        # Continue the simulation or additional animation steps as needed...

# Your existing code for classes and functions

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

    # Create an instance of Simulation
    simulation = Simulation(map_grid)

    # Example business data
    business_radius = 1
    business_center = Point(0.0, 0.0)
    new_business = Business(business_radius, business_center, 1, 50.0, 2, 3)

    # Run the simulation
    simulation.run_simulation(new_business)

    # Find 2nd the best location for the new business
    # best_location_info = map_grid.find_best_location(new_business)

    # Continue the simulation or additional animation steps as needed...

    plt.show()  # Display the final plot

# run Tests
main()
