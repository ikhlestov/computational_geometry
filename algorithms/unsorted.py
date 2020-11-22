import math
import sys
import bisect
from collections import namedtuple
from typing import List

from algorithms.predicates import turn, line_segments_turn_value
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
    z_1 = line_segments_turn_value(LineSegment(l1.p1, l1.p2), LineSegment(l1.p1, l2.p1))
    z_2 = line_segments_turn_value(LineSegment(l1.p1, l1.p2), LineSegment(l1.p1, l2.p2))
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


def point_belongs_to_a_polygon(z_point: Point, polygon: List[Point]):
    # just a sanity check for the easiest case
    for polygon_point in polygon:
        if polygon_point == z_point:
            return True  # test point the same as a polygon point

    # check intersection of each polygon edge and point-infinity line
    distant_coordinate = int(sys.maxsize ** .5 / 1000)
    point_ray = LineSegment(z_point, Point(distant_coordinate, z_point.y))
    # identify intersection point for each edge
    intersected_points = []
    for idx in range(len(polygon)):
        next_idx = (idx + 1) % len(polygon)
        edge = LineSegment(polygon[idx], polygon[next_idx])
        intersection_point = lines_segment_intersection_point(point_ray, edge)
        if intersection_point:
            if Point(*intersection_point) == z_point:
                return True
            intersected_points.append(intersection_point)
    return len(intersected_points) % 2


def get_triangle_centroid(p1: Point, p2: Point, p3: Point):
    centroid_x = (p1.x + p2.x + p3.x) / 3
    centroid_y = (p1.y + p2.y + p3.y) / 3
    return Point(centroid_x, centroid_y)


def polar_angle(p1: Point, p2: Point):
    """Get polar angle between two points(p1 is origin) and imaginary axis"""
    # "shift" everyting to 0
    x = p2.x - p1.x
    y = p2.y - p1.y
    return math.atan2(y, x)


class PointsPolygonChecker:
    """Check if point belong to a polygon or not in O(log(n)) time"""
    def __init__(self, polygon: List[Point]):
        """Pre-process polygon vertices to be able faster answer to a query.

        Note: We assume that polygon vertices were provided in
        left-order direction

        Complexity: O(n)
        """
        if len(polygon) < 3:
            raise ValueError("Cannot process polygon with less than 3 vertices")
        self.centroid = get_triangle_centroid(*polygon[:3])
        # Here we sort vertices according to an angle, not as a regular counterclockwise direction
        angles_to_vertex = sorted(
            [(polar_angle(self.centroid, vertex), vertex) for vertex in polygon]
        )
        self.angles = [item[0] for item in angles_to_vertex]
        self.vertices = [item[1] for item in angles_to_vertex]

    def __call__(self, z: Point):
        """Check if z belongs to a polygon"""
        z_angle = polar_angle(self.centroid, z)
        sector_right_idx = bisect.bisect(self.angles, z_angle)
        # if we meet edge for bisect search - take next round element
        if not sector_right_idx or sector_right_idx == len(self.angles):
            sector_left_idx = len(self.angles) - 1
            sector_right_idx = 0
        else:
            sector_left_idx = sector_right_idx - 1
        sector_point_right = self.vertices[sector_right_idx]
        sector_point_left = self.vertices[sector_left_idx]
        turn_ = turn(sector_point_left, sector_point_right, z)
        if turn_ == -1:
            return False
        return True
