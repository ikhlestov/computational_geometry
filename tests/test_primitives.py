import pytest

from algorithms.primitives import Point, LineSegment, Vector, line_segment_from_coordinates


### Points
def test_points_equal():
    assert Point(10, 20) == Point(10, 20)
    assert Point(10, 20) == Point(10.0, 20.0)
    assert Point(2.13, 14.17) == Point(2.13, 14.17)


def test_points_not_equal():
    assert Point(0, 1) != Point(0, 2)
    assert Point(1, 0) != Point(2, 0)

def test_point__add__():
    assert Point(12, 15) == (Point(2, 10) + Point(10, 5))


def test_point__sub__():
    assert Point(12, 15) - Point(2, 10) == Point(10, 5)


def test_point__neg__():
    assert -Point(10, 20) == Point(-10, -20)


### Lines segments
def test_line_segment_equal():
    p1 = Point(0, 1)
    p2 = Point(10, 20)
    l1 = LineSegment(p1, p2)
    l2 = LineSegment(p1, p2)
    l3 = LineSegment(p2, p1)
    assert l1 == l2
    assert l1 == l3


def test_line_segment_not_equal():
    l1 = LineSegment(Point(1, 2), Point(3, 4))
    l2 = LineSegment(Point(5, 6), Point(7, 8))
    assert l1 != l2


def test_line_segment_impossible_to_create():
    p1 = Point(0, 1)
    with pytest.raises(ValueError):
        LineSegment(p1, p1)


### Vectors
def test_vectors_properties():
    Vector(Point(10, 0), Point(0, 0)).len == 10
    Vector(Point(0, 10), Point(0, 0)).len == 10
    Vector(Point(0, 0), Point(10, 0)).len == 10
    Vector(Point(0, 0), Point(0, 10)).len == 10
    Vector(Point(0, 0), Point(3, 4)).len == 5
    Vector(Point(1, 2), Point(4, 6)).len == 5


def test_vector_angle():
    v1 = Vector(Point(0, 0), Point(0, 10))
    v2 = Vector(Point(0, 0), Point(20, 0))
    assert v1.angle(v2) == 90

    v2 = Vector(Point(0, 0), Point(0, -10))
    assert v1.angle(v2) == 180

    v2 = Vector(Point(0, 0), Point(-10, 0))
    assert v1.angle(v2) == 90  # even it should be 270

    v2 = Vector(Point(0, 0), Point(0, 10))
    assert v1.angle(v2) == 0


### Helper methods
def test_line_segment_from_coordinates():
    p1_x, p1_y, p2_x, p2_y = list(range(1, 5))
    line_1 = line_segment_from_coordinates(p1_x, p1_y, p2_x, p2_y)
    line_2 = LineSegment(Point(x=p1_x, y=p1_y), Point(x=p2_x, y=p2_y))
    assert line_1 == line_2


