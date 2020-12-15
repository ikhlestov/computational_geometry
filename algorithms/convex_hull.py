from .predicates import points_turn_value
from .unsorted import get_triangle_centroid
from .primitives import Point, Vector

def naive(points):
    edges = []
    for p1 in points:
        for p2 in points:
            points_are_edge = True
            if p1 == p2:
                continue
            for p3 in points:
                if p3 == p1 or p3 == p2:
                    continue
                turn = points_turn_value(p1, p2, p3)
                if turn >= 0:
                    points_are_edge = False
                    break
            if points_are_edge:
                edges.append([p1, p2])
    return edges


def graham(points):
    points_to_y = [(point.y, point) for point in points]
    points_to_y = sorted(points_to_y)
    lower_y_coord_point = points_to_y[0][1]
    hor_line_end_point = Point(lower_y_coord_point.x + 5000, lower_y_coord_point.y)
    hor_vector = Vector(lower_y_coord_point, hor_line_end_point)
    cos_to_points = []
    for point in points:
        if point == lower_y_coord_point:
            continue
        z_to_point_vector = Vector(lower_y_coord_point, point)
        cos = hor_vector.cos(z_to_point_vector)
        cos_to_points.append((cos, point))
    cos_to_points = sorted(cos_to_points)
    sorted_points = [p[1] for p in cos_to_points]
    hull = [lower_y_coord_point, sorted_points[0], sorted_points[1]]
    for point in sorted_points[2:]:
        while True:
            prev_point = hull[-1]
            prev_prev_point = hull[-2]
            turn = points_turn_value(point, prev_point, prev_prev_point)
            # in case of right turn
            if turn < 0:
                hull.pop(-1)
            else:
                hull.append(point)
                break
    edges = []
    for idx in range(len(hull)):
        edges.append((hull[idx], hull[(idx + 1) % len(hull)]))
    return edges, sorted_points
