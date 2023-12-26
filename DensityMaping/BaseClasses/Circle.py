from Point import Point

"""
------------------------------------------ Circle ----------------------------------------------
Circle Class: represents a Circle on the grid
parameters:
radius : represents the length of the circle's radius [float]
circle_center : Point that represents the circle's center axis on the grid [Point]
functions:
get_radius, get_center : get the Circle's radius/ center point 
set_radius, set_center  : set the Circles' radius/ center point
circle_to_square :  return length of edge of the circle's equivalent square, edge = 2 * radius
------------------------------------------------------------------------------------------------
"""

class Circle:
    def __init__(self, radius: float, center: Point):
        self.radius = radius
        self.circle_center = Point(center.get_x(), center.get_y())

    # getters
    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.circle_center

    # setters
    def set_radius(self, r: float):
        self.radius = r

    def set_center(self, c: Point):
        self.circle_center.set_x(c.get_x())
        self.circle_center.set_y(c.get_y())

    # functions

    # square inside circle
    # def circle_to_square(self, radius):   # return length of edge of the equivalent square
    #     return float(math.sqrt(2) * radius)

    # return length of edge of the equivalent square
    def circle_to_square(self):
        return float(2 * self.radius)

    # square outside circle
    @staticmethod
    def circle_to_square_static(radius: float):   # return length of edge of the equivalent square
        return float(2 * radius)
