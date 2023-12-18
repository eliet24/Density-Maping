from Point import Point


class Circle:
    def __init__(self, rad: float, center: Point):
        self.radius = rad
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

    def circle_to_square(self):   # return length of edge of the equivalent square
        return float(2 * self.radius)

    # square outside circle
    @staticmethod
    def circle_to_square_static(radius: float):   # return length of edge of the equivalent square
        return float(2 * radius)
