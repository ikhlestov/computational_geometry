from algorithms.predicates import turn
from algorithms.primitives import Point


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
