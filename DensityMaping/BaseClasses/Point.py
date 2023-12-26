"""
------------------- Point ----------------
Point Class: represents a point on the grid
parameters:
x : points x_axis value
y : points y_axis value
functions:
get_x, get_y : get the classes x, y values
set_x, set_y  : set the classes x, y values
------------------------------------------
"""


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # getters
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # setters
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y


