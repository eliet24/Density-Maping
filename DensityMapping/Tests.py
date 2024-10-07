from BaseClasses.Business import Business
from BaseClasses.BusinessType import BusinessType
from BaseClasses.MapGrid import MapGrid, BestLocationInfo
import numpy as np
from matplotlib import pyplot as plt
from BaseClasses.Point import Point


def main_old():
    # Example usage
    x_axis_len = 10
    y_axis_len = 10
    scaled_square_len = 1

    grid_squares_values3 = np.random.randint(0, 101, size=(x_axis_len, y_axis_len)).tolist()

    # Create an instance of MapGrid
    map_grid = MapGrid(x_axis_len=x_axis_len, y_axis_len=y_axis_len, grid_square_len=scaled_square_len, grid_squares_values=grid_squares_values3)
    map_grid.print_grid_values()

    # Example business data
    business_radius = 1.0
    business_center = Point(x=0.0, y=0.0)
    new_business = Business(radius=business_radius, circle_center=business_center, business_id=1, req_income=50.0,
                            business_type=BusinessType.FOOD, business_var=3.0)
    new_business2 = Business(radius=business_radius, circle_center=business_center, business_id=2, req_income=121.0,
                             business_type=BusinessType.HEALTH_AND_COSMETICS, business_var=3.0)

    # Create a figure and axis for visualization
    fig, ax = plt.subplots()

    # Visualize initial grid
    map_grid.visualize_grid(ax)
    plt.pause(2)  # Pause to view the initial grid

    # Find the best location for the new business
    best_location_info = map_grid.find_best_location(new_business)

    # Print the results
    best_location_info.print_location_info()
    map_grid.put_business_on_grid(new_business, best_location_info)
    map_grid.print_grid_values()

    # Visualize grid with the first business
    map_grid.visualize_grid(ax)  # Update the grid visualization
    map_grid.visualize_bizns_on_grid(ax, [new_business])
    plt.pause(2)  # Pause to view the grid with the first business

    # Find the best location for the second business
    best_location_info2 = map_grid.find_best_location(new_business2)
    best_location_info2.print_location_info()
    map_grid.put_business_on_grid(new_business2, best_location_info2)
    map_grid.print_grid_values()

    # Visualize grid with the second business
    map_grid.visualize_grid(ax)  # Update the grid visualization
    map_grid.visualize_bizns_on_grid(ax, [new_business, new_business2])
    plt.pause(2)  # Pause to view the grid with the second business

    plt.tight_layout()
    plt.show()  # Keep the plot open at the end




def main():
    # Example usage
    x_axis_len = 20
    y_axis_len = 20
    scaled_square_len = 1

    grid_squares_values3 = np.random.randint(0, 101, size=(x_axis_len, y_axis_len)).tolist()

    # Create an instance of MapGrid
    map_grid = MapGrid(x_axis_len=x_axis_len, y_axis_len=y_axis_len, grid_square_len=scaled_square_len,
                       grid_squares_values=grid_squares_values3)
    map_grid.print_grid_values()

    # Example business data
    business_radius = 1.0
    business_center = Point(x=0.0, y=0.0)

    # Create a figure and axis for visualization
    fig, ax = plt.subplots()

    # Visualize initial grid
    map_grid.visualize_grid(ax)
    plt.pause(5)  # Pause to view the initial grid

    for i in range(1, 10):
        new_business = Business(radius=i/2, circle_center=business_center, business_id=i, req_income=50.0 + i,
                                business_type=BusinessType.FOOD, business_var=3.0)
        # Find the best location for the new business
        # best_location_info = map_grid.find_best_location(new_business)
        best_locations_info = map_grid.find_locations(new_business)
        if not best_locations_info:
            print("No suitable locations found for the business income requirements")
            return
        else:
            selected_location = max(best_locations_info, key=lambda BestLocationInfo:BestLocationInfo.best_income_found)
            # Print the results
            # best_location_info.print_location_info()
            selected_location.print_location_info()
            # map_grid.put_business_on_grid(new_business, best_location_info)
            map_grid.put_business_on_grid(new_business, selected_location)
            map_grid.print_grid_values()

            # Visualize grid with the first business
            map_grid.visualize_grid(ax)  # Update the grid visualization
            map_grid.visualize_bizns_on_grid(ax, [new_business])
            plt.pause(1)  # Pause to view the grid

    plt.tight_layout()
    plt.show()  # Keep the plot open at the end




# run Tests
main()
# cProfile.run('main()')