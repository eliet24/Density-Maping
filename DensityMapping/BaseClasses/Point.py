from pydantic import BaseModel
"""
------------------- Point ----------------
Point Class: represents a point on the grid
parameters:
x : points x_axis value
y : points y_axis value
functions:
get_x, get_y : get the classes x, y values
set_x, set_y  : set the classes x, y values
print_pint  :  print the point indices on the axis in the format: (_x_,_y_)
------------------------------------------
"""


class Point(BaseModel):
    x: float
    y: float


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def print_point(self):
        print("(" + str(self.get_x()) + "," + str(self.get_y()) + ")")

    def calculate_distance_to_other_point(self, other: "Point"):
        return abs(((self.get_y() - other.get_y()) ** 2 + (self.get_x() - other.get_x()) ** 2) ** 0.5)