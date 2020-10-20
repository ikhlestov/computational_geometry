import math
from collections import namedtuple

from algorithms.predicates import turn, turn_value
from algorithms.primitives import Point, LineSegment


ThreePoints = namedtuple('ThreePoints', ['start', 'middle', 'end'])


def points_distance(p1, p2):
    """Calculates distances between two points"""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def lines_segment_intersection(l1: LineSegment, l2: LineSegment):
    """Check that two lines intersect with each other"""
    # Note: turns identification can be replaces with vectors pairs multiplication
    l2_p1_turn_over_l1 = turn(a=l1.p1, b=l1.p2, c=l2.p1)
    l2_p2_turn_over_l1 = turn(a=l1.p1, b=l1.p2, c=l2.p2)
    l1_p1_turn_over_l2 = turn(a=l2.p1, b=l2.p2, c=l1.p1)
    l1_p2_turn_over_l2 = turn(a=l2.p1, b=l2.p2, c=l1.p2)

    all_points_on_one_line = not any([
        l2_p1_turn_over_l1,
        l2_p2_turn_over_l1,
        l1_p1_turn_over_l2,
        l1_p2_turn_over_l2
    ])

    if all_points_on_one_line:
        three_points_cases = [
            ThreePoints(l1.p1, l2.p1, l1.p2),
            ThreePoints(l1.p1, l2.p2, l1.p2),
            ThreePoints(l2.p1, l1.p1, l2.p2),
            ThreePoints(l2.p1, l1.p2, l2.p2),
        ]
        for three_point in three_points_cases:
            segment_length = points_distance(three_point.start, three_point.end)
            summed_chunks_length = (
                points_distance(three_point.start, three_point.middle) +
                points_distance(three_point.middle, three_point.end)
            )
            if math.isclose(segment_length, summed_chunks_length):
                return True
        else:
            return False
    
    return (
        (
            l2_p1_turn_over_l1 * l2_p2_turn_over_l1 <= 0 and
            l1_p1_turn_over_l2 * l1_p2_turn_over_l2 < 0
         ) or
        (
            l2_p1_turn_over_l1 * l2_p2_turn_over_l1 < 0 and
            l1_p1_turn_over_l2 * l1_p2_turn_over_l2 <= 0
        )
    )


def lines_segment_intersection_point(l1: LineSegment, l2: LineSegment):
    if not lines_segment_intersection(l1, l2):
        return None
    z_1 = turn_value(l1.p1, l1.p2, l2.p1)
    z_2 = turn_value(l1.p1, l1.p2, l2.p2)
    try:
        fraction = abs(z_1 / (z_2 - z_1))
    # edge case with parallel lines were detected
    except ZeroDivisionError:
        return None
    a = l1.p1
    b = l1.p2
    c = l2.p1
    d = l2.p2
    o_x = c.x + (d.x - c.x) * fraction
    o_y = c.y + (d.y - c.y) * fraction
    return o_x, o_y


def point_belongs_to_line(line_segm: LineSegment, point: Point):
    """Check that point belongs to a line or not

    Inspiration: https://code-live.ru/solutions/cpp/9/
    """
    if line_segm.p1.x == line_segm.p2.x:
        return (
            point.x == line_segm.p1.x and
            point.y >= min(line_segm.p1.y, line_segm.p2.y) and
            line_segm.p1.x <= max(line_segm.p1.y, line_segm.p2.y)
        )

    k = (line_segm.p2.y - line_segm.p1.y) / (line_segm.p2.x - line_segm.p1.x);
    c = line_segm.p1.y - k * line_segm.p1.x;

    return point.y == point.x * k + c
