"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askfloat, askinteger
import math


def draw_grid_with_circles(square_size, grid_size, circles):
    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Draw grid of squares
    for i in range(grid_size):
        for j in range(grid_size):
            square = plt.Rectangle((i * square_size, j * square_size), square_size, square_size, fill=None,
                                   edgecolor='black')
            ax.add_patch(square)

    # Draw circles
    for i, circle in enumerate(circles, start=1):
        center_x, center_y, radius = circle
        circle_patch = Circle((center_x, center_y), radius, fill=True, color='red')
        ax.add_patch(circle_patch)
        ax.text(center_x, center_y, str(i), ha='center', va='center', color='white', fontweight='bold')

    # Set axis limits and display grid
    plt.xlim(0, grid_size * square_size)
    plt.ylim(0, grid_size * square_size)
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=7)
    canvas.draw()

    # Return the canvas to keep a reference
    return canvas


# Function to handle "Draw Grid" button click event
def on_draw_button_click():
    square_size = float(square_size_entry.get())
    grid_size = int(grid_size_entry.get())

    # Check if the entries are empty and provide default values
    circles = []
    for circle_info in new_circles:
        center_x, center_y, radius = circle_info
        circles.append((center_x, center_y, radius))

    # Draw grid and circles, keep the canvas reference
    canvas = draw_grid_with_circles(square_size, grid_size, circles)
    # Store the canvas reference in a global variable
    on_draw_button_click.canvas = canvas


# Function to handle "Move Circle" button click event
def on_move_circle_button_click():
    circle_number = askinteger("Move Circle", "Enter the circle number to move:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1  # Convert to zero-based index
        new_center_x = askfloat("Move Circle", "Enter new X coordinate for the center of the circle:")
        new_center_y = askfloat("Move Circle", "Enter new Y coordinate for the center of the circle:")
        if new_center_x is not None and new_center_y is not None:
            new_circles[circle_index] = (
            new_center_x, new_center_y, new_circles[circle_index][2])  # Keep the radius unchanged
            on_draw_button_click.canvas.draw()


# Function to handle "Change Radius" button click event
def on_change_radius_button_click():
    circle_number = askinteger("Change Radius", "Enter the circle number to change radius:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1  # Convert to zero-based index
        new_radius = askfloat("Change Radius", "Enter the new radius of the circle:")
        if new_radius is not None:
            new_circles[circle_index] = (new_circles[circle_index][0], new_circles[circle_index][1], new_radius)
            on_draw_button_click.canvas.draw()


# Function to handle "Add Circle" button click event
def on_add_circle_button_click():
    new_center_x = askfloat("Add Circle", "Enter X coordinate for the center of the new circle:")
    new_center_y = askfloat("Add Circle", "Enter Y coordinate for the center of the new circle:")
    new_radius = askfloat("Add Circle", "Enter the radius of the new circle:")
    if new_center_x is not None and new_center_y is not None and new_radius is not None:
        new_circles.append((new_center_x, new_center_y, new_radius))
        update_circle_list()
        on_draw_button_click()


# Function to handle "Calculate Distance" button click event
def on_calculate_distance_button_click():
    if len(new_circles) >= 2:
        # Prompt the user to choose the circles
        circle_number1 = askinteger("Calculate Distance", "Enter the number of the first circle:")
        circle_number2 = askinteger("Calculate Distance", "Enter the number of the second circle:")

        if circle_number1 is not None and circle_number2 is not None:
            if 1 <= circle_number1 <= len(new_circles) and 1 <= circle_number2 <= len(
                    new_circles) and circle_number1 != circle_number2:
                center1 = (new_circles[circle_number1 - 1][0], new_circles[circle_number1 - 1][1])
                center2 = (new_circles[circle_number2 - 1][0], new_circles[circle_number2 - 1][1])
                distance = math.sqrt((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2)
                distance_label.config(
                    text=f"Distance between centers: {distance:.2f} (Circles {circle_number1} and {circle_number2})")

                # Draw a line between the centers of the chosen circles
                plt.plot([center1[0], center2[0]], [center1[1], center2[1]], linestyle='--', color='blue')
                on_draw_button_click.canvas.draw()

            else:
                distance_label.config(text="Invalid circle numbers. Please choose different circles.")
        else:
            distance_label.config(text="Invalid input. Please enter valid circle numbers.")
    else:
        distance_label.config(text="Add at least two circles to calculate distance.")


# Function to update the circle list display
def update_circle_list():
    circle_list_text.config(state=tk.NORMAL)
    circle_list_text.delete(1.0, tk.END)
    for i, circle in enumerate(new_circles, start=1):
        circle_list_text.insert(tk.END, f"Circle {i}: Center ({circle[0]}, {circle[1]}), Radius {circle[2]}\n")
    circle_list_text.config(state=tk.DISABLED)


# Function to handle "Refresh" button click event
def on_refresh_button_click():
    on_draw_button_click()


# Create the main window
window = tk.Tk()
window.title("Grid and Circle Drawer")

# Create and place widgets in the window
tk.Label(window, text="Square Size:").grid(row=0, column=0)
square_size_entry = ttk.Entry(window)
square_size_entry.grid(row=0, column=1)

tk.Label(window, text="Grid Size:").grid(row=1, column=0)
grid_size_entry = ttk.Entry(window)
grid_size_entry.grid(row=1, column=1)

draw_button = ttk.Button(window, text="Draw Grid", command=on_draw_button_click)
draw_button.grid(row=2, column=0, columnspan=2)

radius_entry = ttk.Entry(window)
radius_entry.grid(row=2, column=2)

calculate_distance_button = ttk.Button(window, text="Calculate Distance", command=on_calculate_distance_button_click)
calculate_distance_button.grid(row=2, column=3)

move_circle_button = ttk.Button(window, text="Move Circle", command=on_move_circle_button_click)
move_circle_button.grid(row=2, column=4)

change_radius_button = ttk.Button(window, text="Change Radius", command=on_change_radius_button_click)
change_radius_button.grid(row=2, column=5)

add_circle_button = ttk.Button(window, text="Add Circle", command=on_add_circle_button_click)
add_circle_button.grid(row=2, column=6)

refresh_button = ttk.Button(window, text="Refresh", command=on_refresh_button_click)
refresh_button.grid(row=2, column=7)

distance_label = ttk.Label(window, text="")
distance_label.grid(row=3, column=0, columnspan=8)

# Create a text widget to display the list of circles
circle_list_text = tk.Text(window, height=5, width=40, state=tk.DISABLED)
circle_list_text.grid(row=10, column=0, columnspan=8)

# List to store information about new circles
new_circles = []

# Start the Tkinter event loop
window.mainloop()

"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askfloat, askinteger
import math
import random
import matplotlib.colors as mcolors


def draw_grid_with_circles(square_size, grid_size, circles):
    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Draw grid of squares
    for i in range(grid_size):
        for j in range(grid_size):
            square = plt.Rectangle((i * square_size, j * square_size), square_size, square_size, fill=None,
                                   edgecolor='black')
            ax.add_patch(square)

    # Draw circles
    for i, circle in enumerate(circles, start=1):
        center_x, center_y, radius, color = circle
        circle_patch = Circle((center_x, center_y), radius, fill=True, color=color)
        ax.add_patch(circle_patch)
        ax.text(center_x, center_y, str(i), ha='center', va='center', color='white', fontweight='bold')

    # Set axis limits and display grid
    plt.xlim(0, grid_size * square_size)
    plt.ylim(0, grid_size * square_size)
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=7)
    canvas.draw()

    # Return the canvas to keep a reference
    return canvas


# Function to handle "Draw Grid" button click event
def on_draw_button_click():
    square_size = float(square_size_entry.get())
    grid_size = int(grid_size_entry.get())

    # Check if the entries are empty and provide default values
    circles = []
    for circle_info in new_circles:
        center_x, center_y, radius, color = circle_info
        circles.append((center_x, center_y, radius, color))

    # Draw grid and circles, keep the canvas reference
    canvas = draw_grid_with_circles(square_size, grid_size, circles)
    # Store the canvas reference in a global variable
    on_draw_button_click.canvas = canvas


# Function to handle "Move Circle" button click event
def on_move_circle_button_click():
    circle_number = askinteger("Move Circle", "Enter the circle number to move:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1  # Convert to zero-based index
        new_center_x = askfloat("Move Circle", "Enter new X coordinate for the center of the circle:")
        new_center_y = askfloat("Move Circle", "Enter new Y coordinate for the center of the circle:")
        if new_center_x is not None and new_center_y is not None:
            new_circles[circle_index] = (
                new_center_x, new_center_y, new_circles[circle_index][2], new_circles[circle_index][3]
            )  # Keep the radius and color unchanged
            on_draw_button_click.canvas.draw()

# Function to handle "Change Radius" button click event
def on_change_radius_button_click():
    circle_number = askinteger("Change Radius", "Enter the circle number to change radius:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1  # Convert to zero-based index
        new_radius = askfloat("Change Radius", "Enter the new radius of the circle:")
        if new_radius is not None:
            new_circles[circle_index] = (
                new_circles[circle_index][0], new_circles[circle_index][1], new_radius, new_circles[circle_index][3]
            )  # Keep the center coordinates and color unchanged
            on_draw_button_click.canvas.draw()


# Function to handle "Add Circle" button click event
def on_add_circle_button_click():
    new_center_x = askfloat("Add Circle", "Enter X coordinate for the center of the new circle:")
    new_center_y = askfloat("Add Circle", "Enter Y coordinate for the center of the new circle:")
    new_radius = askfloat("Add Circle", "Enter the radius of the new circle:")

    if new_center_x is not None and new_center_y is not None and new_radius is not None:
        # Generate a random color for the new circle
        color = random.choice(list(mcolors.TABLEAU_COLORS.values()))

        new_circles.append((new_center_x, new_center_y, new_radius, color))
        update_circle_list()
        on_draw_button_click()


# Function to handle "Calculate Distance" button click event
def on_calculate_distance_button_click():
    if len(new_circles) >= 2:
        # Prompt the user to choose the circles
        circle_number1 = askinteger("Calculate Distance", "Enter the number of the first circle:")
        circle_number2 = askinteger("Calculate Distance", "Enter the number of the second circle:")

        if circle_number1 is not None and circle_number2 is not None:
            if 1 <= circle_number1 <= len(new_circles) and 1 <= circle_number2 <= len(
                    new_circles) and circle_number1 != circle_number2:
                center1 = (new_circles[circle_number1 - 1][0], new_circles[circle_number1 - 1][1])
                center2 = (new_circles[circle_number2 - 1][0], new_circles[circle_number2 - 1][1])
                distance = math.sqrt((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2)
                distance_label.config(
                    text=f"Distance between centers: {distance:.2f} (Circles {circle_number1} and {circle_number2})")

                # Draw a line between the centers of the chosen circles
                plt.plot([center1[0], center2[0]], [center1[1], center2[1]], linestyle='--', color='blue')
                on_draw_button_click.canvas.draw()

            else:
                distance_label.config(text="Invalid circle numbers. Please choose different circles.")
        else:
            distance_label.config(text="Invalid input. Please enter valid circle numbers.")
    else:
        distance_label.config(text="Add at least two circles to calculate distance.")


# Function to update the circle list display
def update_circle_list():
    circle_list_text.config(state=tk.NORMAL)
    circle_list_text.delete(1.0, tk.END)
    for i, circle in enumerate(new_circles, start=1):
        circle_list_text.insert(tk.END, f"Circle {i}: Center ({circle[0]}, {circle[1]}), Radius {circle[2]}\n")
    circle_list_text.config(state=tk.DISABLED)


# Function to handle "Refresh" button click event
def on_refresh_button_click():
    on_draw_button_click()


# Create the main window
window = tk.Tk()
window.title("Grid and Circle Drawer")

# Create and place widgets in the window
tk.Label(window, text="Square Size:").grid(row=0, column=0)
square_size_entry = ttk.Entry(window)
square_size_entry.grid(row=0, column=1)

tk.Label(window, text="Grid Size:").grid(row=1, column=0)
grid_size_entry = ttk.Entry(window)
grid_size_entry.grid(row=1, column=1)

draw_button = ttk.Button(window, text="Draw Grid", command=on_draw_button_click)
draw_button.grid(row=2, column=0, columnspan=2)

radius_entry = ttk.Entry(window)
radius_entry.grid(row=2, column=2)

calculate_distance_button = ttk.Button(window, text="Calculate Distance", command=on_calculate_distance_button_click)
calculate_distance_button.grid(row=2, column=3)

move_circle_button = ttk.Button(window, text="Move Circle", command=on_move_circle_button_click)
move_circle_button.grid(row=2, column=4)

change_radius_button = ttk.Button(window, text="Change Radius", command=on_change_radius_button_click)
change_radius_button.grid(row=2, column=5)

add_circle_button = ttk.Button(window, text="Add Circle", command=on_add_circle_button_click)
add_circle_button.grid(row=2, column=6)

refresh_button = ttk.Button(window, text="Refresh", command=on_refresh_button_click)
refresh_button.grid(row=2, column=7)

distance_label = ttk.Label(window, text="")
distance_label.grid(row=3, column=0, columnspan=8)

# Create a text widget to display the list of circles
circle_list_text = tk.Text(window, height=5, width=40, state=tk.DISABLED)
circle_list_text.grid(row=10, column=0, columnspan=8)

# List to store information about new circles
new_circles = []

# Start the Tkinter event loop
window.mainloop()






