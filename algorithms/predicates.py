from algorithms.primitives import Point, LineSegment


def cross_product(u, v):
    return u.x * v.y - u.y * v.x


def points_turn_value(a: Point, b: Point, c: Point) -> float:
    return cross_product(b - a, c - a)


def line_segments_turn_value(l1: LineSegment, l2: LineSegment) -> float:
    return cross_product(l1.p2 - l1.p1, l2.p2 - l2.p1)



def turn(a: Point, b: Point, c: Point) -> int:
    """Return correspondence of three points.

    1 - left turn (`c` lies left from ab)
    -1 - right turn (`c` lies right from ab)
    0 - collinear

    References: https://habr.com/ru/post/138168/
    """

    turn_value = points_turn_value(a, b, c)
    
    if turn_value > 0:
        return 1  # left
    elif turn_value < 0:
        return -1  # right
    else:
        return 0
