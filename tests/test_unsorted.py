import pytest

from algorithms import lines_segment_intersection, point_belongs_to_line
from algorithms.primitives import line_segment_from_coordinates, Point


# lines_segment_intersection tests
# 5, 0
# 10, 3
# 15, 6
# 20, 9

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


# point_belongs_to_line_segment tests
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
