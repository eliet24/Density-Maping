import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import tkinter as tk
from tkinter.simpledialog import askfloat, askinteger
import math
import random
import matplotlib.colors as mcolors
import numpy as np
from plotly.subplots import make_subplots
from scipy.stats import multivariate_normal
import openpyxl
from tkinter.filedialog import askopenfilename
from tkinter import *
import customtkinter
import plotly.graph_objects as go
from scipy.stats import multivariate_normal

# Define canvas as a global variable
canvas = None  # Initialize canvas variable


# Function to draw the grid
def draw_grid(square_size, grid_size):
    global canvas
    fig, ax = plt.subplots()

    # Draw grid of squares
    for i in range(grid_size):
        for j in range(grid_size):
            square = plt.Rectangle((i * square_size, j * square_size), square_size, square_size, fill=None,
                                   edgecolor='black')
            ax.add_patch(square)

    plt.xlim(0, grid_size * square_size)
    plt.ylim(0, grid_size * square_size)
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=8)
    canvas.draw()

    # Return the axis to keep a reference
    return ax


# Function to draw value on a square
def draw_value_on_square(value, row, column, square_size, ax):
    x = column * square_size + square_size / 2
    y = row * square_size + square_size / 2

    ax.text(x, y, str(value), ha='center', va='center', color='black', fontweight='bold')


# Function to handle "Put Values On Grid" button click event
def on_put_values_on_grid_button_click():
    global canvas  # Use the global canvas variable

    file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")], title="Choose an Excel file")

    if file_path:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # Get the grid size
        grid_size = int(grid_size_entry.get())

        # Flatten the values in the A column
        values = [cell.value for row in sheet.iter_cols(min_col=1, max_col=1, max_row=grid_size ** 2) for cell in row]

        # Draw grid and circles
        square_size = float(square_size_entry.get())
        ax = draw_grid(square_size, grid_size)
        circles = []  # Assume no circles for now

        # Iterate through the values and put them on the grid
        for i, value in enumerate(values):
            # Calculate the row and column indices based on the grid size
            row = i // grid_size
            column = i % grid_size

            # Draw value on the grid
            draw_value_on_square(value, row, column, square_size, ax)

        # Draw circles
        draw_grid_with_circles(square_size, grid_size, circles, ax)

        # Update the canvas outside the loop
        canvas.draw()


''''# Function to draw a value on the grid
def draw_value_on_grid(value, row, column):
    # Calculate the center of the grid square
    center_x = (column - 0.5) * float(square_size_entry.get())
    center_y = (row - 0.5) * float(square_size_entry.get())

    # Draw the value on the grid
    plt.text(center_x, center_y, str(value), ha='center', va='center', color='black', fontweight='bold')
    on_draw_button_click.canvas.draw()
'''


def draw_grid_with_circles(square_size, grid_size, circles, ax):
    # Draw grid of squares
    for i in range(grid_size):
        for j in range(grid_size):
            square = plt.Rectangle((i * square_size, j * square_size), square_size, square_size, fill=None,
                                   edgecolor='black')
            ax.add_patch(square)

    # Draw circles
    for i, circle in enumerate(circles, start=1):
        center_x, center_y, radius, color, _ = circle
        circle_patch = Circle((center_x, center_y), radius, fill=None, edgecolor=color)
        ax.add_patch(circle_patch)
        ax.text(center_x, center_y, str(i), ha='center', va='center', color='black', fontweight='bold')

    # Set axis limits and display grid
    ax.set_xlim(0, grid_size * square_size)
    ax.set_ylim(0, grid_size * square_size)
    ax.set_aspect('equal', adjustable='box')


'''def draw_3d_perspective(circles):
    fig_3d = plt.figure()
    ax_3d = fig_3d.add_subplot(111, projection='3d')

    for circle in circles:
        center_x, center_y, radius, color, variance = circle
        if variance is not None:
            x = np.linspace(center_x - 3 * variance, center_x + 3 * variance, 100)
            y = np.linspace(center_y - 3 * variance, center_y + 3 * variance, 100)
            x, y = np.meshgrid(x, y)

            pos = np.empty(x.shape + (2,))
            pos[:, :, 0] = x
            pos[:, :, 1] = y

            rv = multivariate_normal([center_x, center_y], [[variance, 0], [0, variance]])
            z = rv.pdf(pos)

            ax_3d.plot_surface(x, y, z, color=color, alpha=0.5)
        else:
            # If variance is not provided, use a default value or handle accordingly
            # You can modify this part based on your specific requirements
            pass

    ax_3d.set_xlabel('X')
    ax_3d.set_ylabel('Y')
    ax_3d.set_zlabel('Z')

    plt.show()
'''


# Function to draw 3D perspective for all circles on the same axis
def draw_3d_perspective(circles):
    fig = go.Figure()

    for i, circle in enumerate(circles):
        center_x, center_y, radius, color, variance = circle
        if variance is not None:
            x = np.linspace(center_x - 3 * variance, center_x + 3 * variance, 100)
            y = np.linspace(center_y - 3 * variance, center_y + 3 * variance, 100)
            x, y = np.meshgrid(x, y)

            pos = np.empty(x.shape + (2,))
            pos[:, :, 0] = x
            pos[:, :, 1] = y

            rv = multivariate_normal([center_x, center_y], [[variance, 0], [0, variance]])
            z = rv.pdf(pos)

            # Add trace for each circle to the same figure
            fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], opacity=0.5, showscale=False))

    # Set scene camera for better perspective
    fig.update_layout(scene=dict(camera=dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=1.25, y=1.25, z=1.25))))

    # Show the plot
    fig.show()


# Function to handle "Move Circle" button click event
def on_move_circle_button_click():
    circle_number = askinteger("Move Circle", "Enter the circle number to move:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1
        new_center_x = askfloat("Move Circle", "Enter new X coordinate for the center of the circle:")
        new_center_y = askfloat("Move Circle", "Enter new Y coordinate for the center of the circle:")
        if new_center_x is not None and new_center_y is not None:
            # Check if variance is present in the original circle
            if len(new_circles[circle_index]) == 5:
                new_circles[circle_index] = (
                    new_center_x,
                    new_center_y,
                    new_circles[circle_index][2],
                    new_circles[circle_index][3],
                    new_circles[circle_index][4],
                )
            else:
                new_circles[circle_index] = (
                    new_center_x,
                    new_center_y,
                    new_circles[circle_index][2],
                    new_circles[circle_index][3],
                )
            on_draw_button_click.canvas.draw()

            # Update the 3D perspective view
            on_3d_perspective_button_click()


# Function to handle "Delete Circle" button click event
def on_delete_circle_button_click():
    circle_number = askinteger("Delete Circle", "Enter the number of the circle to delete:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        del new_circles[circle_number - 1]
        on_draw_button_click.canvas.draw()
        update_circle_list()


# Function to handle "Change Radius" button click event
def on_change_radius_button_click():
    circle_number = askinteger("Change Radius", "Enter the circle number to change radius:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        circle_index = circle_number - 1
        new_radius = askfloat("Change Radius", "Enter the new radius of the circle:")
        if new_radius is not None:
            # Check if variance is present in the original circle
            if len(new_circles[circle_index]) == 5:
                new_circles[circle_index] = (
                    new_circles[circle_index][0],
                    new_circles[circle_index][1],
                    new_radius,
                    new_circles[circle_index][3],
                    new_circles[circle_index][4],
                )
            else:
                new_circles[circle_index] = (
                    new_circles[circle_index][0],
                    new_circles[circle_index][1],
                    new_radius,
                    new_circles[circle_index][3],
                )
            on_draw_button_click.canvas.draw()


# Function to handle "Draw Grid" button click event
def on_draw_button_click():
    global canvas  # Use the global canvas variable
    square_size = float(square_size_entry.get())
    grid_size = int(grid_size_entry.get())

    # Check if the entries are empty and provide default values
    circles = []
    for circle_info in new_circles:
        center_x, center_y, radius, color, variance = circle_info
        circles.append((center_x, center_y, radius, color, variance))

    if not hasattr(on_draw_button_click, 'canvas') or on_draw_button_click.canvas is None:
        # If canvas is not created yet, create it
        fig, ax = plt.subplots()
        on_draw_button_click.canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = on_draw_button_click.canvas.get_tk_widget()
        canvas_widget.grid(row=4, column=0, columnspan=8)

    # Use the stored canvas to get the axes
    ax = on_draw_button_click.canvas.figure.gca()

    # Clear previous drawings
    ax.clear()

    # Draw grid
    ax = draw_grid(square_size, grid_size)

    # Draw circles
    for i, circle_info in enumerate(circles):
        center_x, center_y, radius, color, variance = circle_info
        circle_patch = Circle((center_x, center_y), radius, fill=None, edgecolor=color)
        ax.add_patch(circle_patch)
        ax.text(center_x, center_y, str(i + 1), ha='center', va='center', color='white', fontweight='bold')

    # Draw the canvas
    on_draw_button_click.canvas.draw()


# Function to handle "Delete Circle" button click event
def on_delete_circle_button_click():
    circle_number = askinteger("Delete Circle", "Enter the number of the circle to delete:")
    if circle_number is not None and 1 <= circle_number <= len(new_circles):
        del new_circles[circle_number - 1]
        on_draw_button_click.canvas.draw()
        update_circle_list()


# delete all the grid elements and the grid
def on_delete_all_button_click():
    global canvas, new_circles
    new_circles = []  # Clear the list of circles
    if hasattr(on_delete_all_button_click, 'canvas') and on_delete_all_button_click.canvas is not None:
        on_delete_all_button_click.canvas.get_tk_widget().destroy()  # Destroy the canvas widget
        on_delete_all_button_click.canvas = None  # Reset the canvas variable



# Function to handle "3D Perspective" button click event
def on_3d_perspective_button_click():
    draw_3d_perspective(new_circles)


# Function to handle "Add Circle" button click event
def on_add_circle_button_click():
    new_center_x = askfloat("Add Circle", "Enter X coordinate for the center of the new circle:")
    new_center_y = askfloat("Add Circle", "Enter Y coordinate for the center of the new circle:")
    new_radius = askfloat("Add Circle", "Enter the radius of the new circle:")
    new_variance = askfloat("Add Circle", "Enter the variance of the new circle:")

    if (
        new_center_x is not None
        and new_center_y is not None
        and new_radius is not None
        and new_variance is not None
    ):
        # Generate a random color for the new circle
        color = random.choice(list(mcolors.TABLEAU_COLORS.values()))

        new_circles.append((new_center_x, new_center_y, new_radius, color, new_variance))
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
                distance_label.configure(
                    text=f"Distance between centers: {distance:.2f} (Circles {circle_number1} and {circle_number2})")

                # Use the stored canvas to get the axes
                ax = on_draw_button_click.canvas.figure.gca()

                # Plot the line on the axes
                ax.plot(
                    [center1[0], center2[0]],
                    [center1[1], center2[1]],
                    linestyle='--',
                    color='blue'
                )

                # Draw the canvas
                on_draw_button_click.canvas.draw()

            else:
                distance_label.config(text="Invalid circle numbers. Please choose different circles.")
        else:
            distance_label.config(text="Invalid input. Please enter valid circle numbers.")
    else:
        distance_label.config(text="Add at least two circles to calculate distance.")


# Function to update the circle list display
def update_circle_list():
    circle_list_text.configure(state=tk.NORMAL)
    circle_list_text.delete(1.0, tk.END)
    for i, circle in enumerate(new_circles, start=1):
        circle_list_text.insert(tk.END, f"Circle {i}: Center ({circle[0]}, {circle[1]}), Radius {circle[2]}\n")
    circle_list_text.configure(state=tk.DISABLED)


# Function to handle "Refresh" button click event
def on_refresh_button_click():
    on_draw_button_click()


# Create the main window
#window = tk.Tk()
window = customtkinter.CTk()

window.title("Grid and Circle Drawer")

# Create and place the "Put Values On Grid" button
# put_values_on_grid_button = ttk.Button(window, text="Put Values On Grid", command=on_put_values_on_grid_button_click)
put_values_on_grid_button = customtkinter.CTkButton(window, text="Put Values On Grid", command=on_put_values_on_grid_button_click)
put_values_on_grid_button.grid(row=3, column=0)

# delete_all_button = ttk.Button(window, text="Delete All", command=on_delete_all_button_click)
delete_all_button = customtkinter.CTkButton(window, text="Delete All", command=on_delete_all_button_click)
delete_all_button.grid(row=4, column=0)

# Create and place widgets in the window
# tk.Label(window, text="Square Size:").grid(row=0, column=0)
customtkinter.CTkLabel(window, text="Square Size:").grid(row=0, column=0)
# square_size_entry = ttk.Entry(window)
square_size_entry = customtkinter.CTkEntry(window)
square_size_entry.grid(row=0, column=1)

# tk.Label(window, text="Grid Size:").grid(row=1, column=0)
customtkinter.CTkLabel(window, text="Grid Size:").grid(row=1, column=0)
# grid_size_entry = ttk.Entry(window)
grid_size_entry = customtkinter.CTkEntry(window)
grid_size_entry.grid(row=1, column=1)

# draw_button = ttk.Button(window, text="Draw Grid", command=on_draw_button_click)
draw_button = customtkinter.CTkButton(window, text="Draw Grid", command=on_draw_button_click)
draw_button.grid(row=2, column=0)

# radius_entry = ttk.Entry(window)
# radius_entry = customtkinter.CTkEntry(window)
# radius_entry.grid(row=2, column=2)

# calculate_distance_button = ttk.Button(window, text="Calculate Distance", command=on_calculate_distance_button_click)
calculate_distance_button = customtkinter.CTkButton(window, text="Calculate Distance", command=on_calculate_distance_button_click)
calculate_distance_button.grid(row=3, column=6)

# move_circle_button = ttk.Button(window, text="Move Circle", command=on_move_circle_button_click)
move_circle_button = customtkinter.CTkButton(window, text="Move Circle", command=on_move_circle_button_click)
move_circle_button.grid(row=2, column=4)

# change_radius_button = ttk.Button(window, text="Change Radius", command=on_change_radius_button_click)
change_radius_button = customtkinter.CTkButton(window, text="Change Radius", command=on_change_radius_button_click)
change_radius_button.grid(row=2, column=5)

# add_circle_button = ttk.Button(window, text="Add Circle", command=on_add_circle_button_click)
add_circle_button = customtkinter.CTkButton(window, text="Add Circle", command=on_add_circle_button_click)
add_circle_button.grid(row=2, column=3)

# delete_circle_button = ttk.Button(window, text="Delete Circle", command=on_delete_circle_button_click)
delete_circle_button = customtkinter.CTkButton(window, text="Delete Circle", command=on_delete_circle_button_click)
delete_circle_button.grid(row=2, column=6)

# refresh_button = ttk.Button(window, text="Refresh", command=on_refresh_button_click)
refresh_button = customtkinter.CTkButton(window, text="Refresh", command=on_refresh_button_click)
refresh_button.grid(row=2, column=7)

# distance_label = ttk.Label(window, text="")
distance_label = customtkinter.CTkLabel(window, text="")
distance_label.grid(row=3, column=0, columnspan=8)

# three_d_button = ttk.Button(window, text="3D Perspective", command=on_3d_perspective_button_click)
three_d_button = customtkinter.CTkButton(window, text="3D Perspective", command=on_3d_perspective_button_click)
three_d_button.grid(row=3, column=7)

# Create a text widget to display the list of circles
# circle_list_text = tk.Text(window, height=5, width=40, state=tk.DISABLED)
circle_list_text = customtkinter.CTkTextbox(window, height=5, width=80, state=tk.DISABLED)
circle_list_text.grid(row=10, column=0, columnspan=8)

# List to store information about new circles
new_circles = []

# Start the Tkinter event loop
window.mainloop()

