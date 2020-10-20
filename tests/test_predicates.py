from algorithms.predicates import turn, points_turn_value, line_segments_turn_value
from algorithms.primitives import Point, LineSegment


def test_turn_left():
    assert 1 == turn(
        Point(5, 10),
        Point(5, 20),
        Point(0, 15)
    )


def test_turn_right():
    assert -1 == turn(
        Point(5, 10),
        Point(5, 20),
        Point(15, 15)
    )


def test_turn_colinear():
    assert 0 == turn(
        Point(5, 10),
        Point(5, 20),
        Point(5, 30)
    )


def test_points_and_line_segments_turns_are_the_same():
    p1 = Point(5, 10)
    p2 = Point(5, 20)
    p3 = Point(15, 15)
    assert points_turn_value(p1, p2, p3) == line_segments_turn_value(LineSegment(p1, p2), LineSegment(p1, p3))
