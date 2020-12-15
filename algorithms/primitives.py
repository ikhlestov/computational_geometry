import math


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

    def __repr__(self):
        return "Point({:.2f}, {:.2f})".format(self.x, self.y)

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        else:
            return self.y < other.y


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


class Vector(LineSegment):
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.x = end.x - start.x
        self.y = end.y - start.y

    def cos(self, other):
        scalar = self.scalar(other)
        return scalar / (self.len * other.len)

    def scalar(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self, other):
        # return math.degrees(math.acos(self.cos(other)))
        return math.acos(self.cos(other))

    @property
    def len(self):
        return (self.x ** 2 + self.y ** 2) ** .5


# TODO: google two constructors in python
def line_segment_from_coordinates(p1_x, p1_y, p2_x, p2_y):
    """Syntatic sugar to faster build line from raw coordinates"""
    return LineSegment(Point(x=p1_x, y=p1_y), Point(x=p2_x, y=p2_y))
