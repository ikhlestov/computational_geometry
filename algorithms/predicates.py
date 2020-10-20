from algorithms.primitives import Point


def turn_value(a: Point, b: Point, c: Point) -> float:
    def cross(p1: Point, p2: Point):
        return p1.x * p2.y - p2.x * p1.y

    determinant = cross(b - a, c - a)
    return determinant


def turn(a: Point, b: Point, c: Point) -> int:
    """Return correspondence of three points.

    1 - left turn (`c` lies left from ab)
    -1 - right turn (`c` lies right from ab)
    0 - collinear

    References: https://habr.com/ru/post/138168/
    """

    determinant = turn_value(a, b, c)
    
    if determinant > 0:
        return 1  # left
    elif determinant < 0:
        return -1  # right
    else:
        return 0
