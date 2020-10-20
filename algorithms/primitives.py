class Point:
    """Class to represent regular 2D point"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)


class LineSegment:
    """Class to represent 2D line segment passing through two points"""
    def __init__(self, p1: Point, p2: Point):
        if p1 == p2:
            raise ValueError(
                f"Cannot create {self.__class__.__name__} passing through the same point"
            )
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return (
            (self.p1 == other.p1 and self.p2 == other.p2) or
            (self.p1 == other.p2 and self.p2 == other.p1)
        )

    # def __mul__(self, other):
    #     # (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    #     # ax = self.p1
    #     a = self.p1
    #     b = self.p2
    #     c = other.p2


# TODO: google two constructors in python
def line_segment_from_coordinates(p1_x, p1_y, p2_x, p2_y):
    """Syntatic sugar to faster build line from raw coordinates"""
    return LineSegment(Point(x=p1_x, y=p1_y), Point(x=p2_x, y=p2_y))
