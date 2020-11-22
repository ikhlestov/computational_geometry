import pytest

from algorithms import lines_segment_intersection, point_belongs_to_line, \
    lines_segment_intersection_point, point_belongs_to_a_polygon, polar_angle, PointsPolygonChecker
from algorithms.primitives import line_segment_from_coordinates, Point


def test_lines_segment_intersection_positive_case():
    l1 = line_segment_from_coordinates(0, 0, 10, 10)
    l2 = line_segment_from_coordinates(10, 0, 0, 10)
    assert lines_segment_intersection(l1, l2)
    assert lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_negative_case():
    l1 = line_segment_from_coordinates(0, 0, 10, 10)
    l2 = line_segment_from_coordinates(20, 0, 30, 10)
    assert not lines_segment_intersection(l1, l2)
    assert not lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_edge_case_a():
    """Case when one point from line segment L2 lies on line segment L2"""
    l1 = line_segment_from_coordinates(10, 10, 20, 10)
    l2 = line_segment_from_coordinates(15, 10, 40, 40)
    assert lines_segment_intersection(l1, l2)
    assert lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_edge_case_b():
    """Case when end point from line segment L2 lies within direction
    of line segment L1 but outside of its boundaries"""
    l1 = line_segment_from_coordinates(10, 10, 20, 10)
    l2 = line_segment_from_coordinates(30, 10, 25, 15)
    assert not lines_segment_intersection(l1, l2)
    assert not lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_edge_case_c():
    """Line segment L2 'follows' initial segment L1 but not intersects it"""
    l1 = line_segment_from_coordinates(5, 0, 10, 3)
    l2 = line_segment_from_coordinates(15, 6, 20, 9)
    assert not lines_segment_intersection(l1, l2)
    assert not lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_edge_case_d():
    """Line segment L2 totaly lies on line segment L1"""
    l1 = line_segment_from_coordinates(5, 0, 20, 9)
    l2 = line_segment_from_coordinates(10, 3, 15, 6)
    assert lines_segment_intersection(l1, l2)
    assert lines_segment_intersection(l2, l1)


def test_lines_segment_intersection_edge_case_e():
    """Line segment L2 parially lies on line segment L1"""
    l1 = line_segment_from_coordinates(5, 0, 15, 6)
    l2 = line_segment_from_coordinates(10, 3, 20, 9)
    assert lines_segment_intersection(l1, l2)
    assert lines_segment_intersection(l2, l1)


# lines_segment_intersection_point tests
def test_lines_segment_intersection_point_case_1():
    l1 = line_segment_from_coordinates(0, 0, 10, 10)
    l2 = line_segment_from_coordinates(0, 10, 10, 0)
    assert (5, 5) == lines_segment_intersection_point(l1, l2)
    assert (5, 5) == lines_segment_intersection_point(l2, l1)


def test_lines_segment_intersection_point_case_2():
    l1 = line_segment_from_coordinates(0, 0, 8, 4)
    l2 = line_segment_from_coordinates(0, 6, 12, 0)
    assert (6, 3) == lines_segment_intersection_point(l1, l2)
    assert (6, 3) == lines_segment_intersection_point(l2, l1)


def test_lines_segment_intersection_point_case_3():
    l1 = line_segment_from_coordinates(5, 0, 20, 9)
    l2 = line_segment_from_coordinates(10, 3, 15, 6)
    assert None == lines_segment_intersection_point(l1, l2)
    assert None == lines_segment_intersection_point(l2, l1)


def test_lines_segment_intersection_point_case_4():
    l1 = line_segment_from_coordinates(5, 0, 10, 3)
    l2 = line_segment_from_coordinates(20, 9, 15, 6)
    assert None == lines_segment_intersection_point(l1, l2)
    assert None == lines_segment_intersection_point(l2, l1)


def test_lines_segment_intersection_point_case_5():
    """Case when one point from line segment L2 lies on line segment L2"""
    l1 = line_segment_from_coordinates(10, 10, 20, 10)
    l2 = line_segment_from_coordinates(15, 10, 40, 40)
    assert (15, 10) == lines_segment_intersection_point(l1, l2)
    assert (15, 10) == lines_segment_intersection_point(l2, l1)


# point_belongs_to_line tests
def test_point_belongs_to_line_positive():
    l1 = line_segment_from_coordinates(5, 0, 15, 6)
    p1 = Point(10, 3)
    assert point_belongs_to_line(l1, p1)

    l2 = line_segment_from_coordinates(0, 0, 0, 10)
    p2 = Point(0, 5)
    assert point_belongs_to_line(l2, p2)

    # Point outside line segment but on the same line
    l3 = line_segment_from_coordinates(5, 0, 10, 3)
    p3 = Point(15, 6)
    assert point_belongs_to_line(l3, p3)

    l4 = line_segment_from_coordinates(0, 0, 0, 10)
    p4 = Point(0, 12)
    assert point_belongs_to_line(l4, p4)


def test_point_belongs_to_line_negative():
    l1 = line_segment_from_coordinates(5, 0, 10, 3)
    p1 = Point(20, 6)
    assert not point_belongs_to_line(l1, p1)

    l3 = line_segment_from_coordinates(0, 0, 0, 10)
    p3 = Point(1, 10)
    assert not point_belongs_to_line(l3, p3)


# point_belongs_to_a_polygon
def test_point_belongs_to_a_polygon_true():
    """
    _________
    |       |
    |       |
    |       |
    |       |
    ---------
    """
    polygon = [
        Point(0, 0),
        Point(0, 10),
        Point(10, 10),
        Point(10, 0)
    ]
    
    # point exist inside tha polygon
    p1 = Point(5, 5)
    assert point_belongs_to_a_polygon(p1, polygon)

    # point belongs to a polygon edge
    p2 = Point(0, 5)
    assert point_belongs_to_a_polygon(p2, polygon)

    # point is the same as on of polygon edges
    p3 = Point(10, 10)
    assert point_belongs_to_a_polygon(p3, polygon)


def test_point_belongs_to_a_polygon_false():
    """
    _________
    |  /\\  |
    | /  \\ |
    |/    \\|
    """
    polygon = [
        Point(0, 0),
        Point(0, 10),
        Point(10, 10),
        Point(10, 0),
        Point(5, 9),
    ]

    # point lies on "inside" concave part of polygon
    p1 = Point(5, 5)
    assert not point_belongs_to_a_polygon(p1, polygon)

    p2 = Point(5, 0)
    assert not point_belongs_to_a_polygon(p2, polygon)

    p3 = Point(12, 0)
    assert not point_belongs_to_a_polygon(p3, polygon)


# points belongs to a polygon check, multi requests
def test_PointsPolygonChecker_true():
    """
    _________
    |       |
    |       |
    |       |
    |       |
    ---------
    """
    points_polygon_checker = PointsPolygonChecker([
        Point(0, 0),
        Point(10, 0),
        Point(10, 10),
        Point(0, 10),
    ])

    # point exist inside tha polygon
    assert points_polygon_checker(Point(5, 5))

    # point belongs to a polygon edge
    assert points_polygon_checker(Point(0, 5))

    # point is the same as on of polygon edges
    assert points_polygon_checker(Point(10, 10))


def test_PointsPolygonChecker_false():
    """
    _________
    |       |
    |       |
    |       |
    |       |
    ---------
    """
    points_polygon_checker = PointsPolygonChecker([
        Point(0, 0),
        Point(10, 0),
        Point(10, 10),
        Point(0, 10),
    ])

    # point lies on "inside" concave part of polygon
    assert not points_polygon_checker(Point(11, 11))

    assert not points_polygon_checker(Point(5, 43))

    assert not points_polygon_checker(Point(12, 0))



def test_polar_angle():
    ans1 = polar_angle(Point(0, 0), Point(-1, -1))
    ans2 = polar_angle(Point(1, 1), Point(0, 0))
    assert ans1 == ans2 == pytest.approx(-2.356194490192345)
