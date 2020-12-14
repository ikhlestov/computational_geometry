from .predicates import points_turn_value

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
    result = []
    for idx in range(len(points) - 1):
        result.append((points[idx], points[idx + 1]))
    return result
