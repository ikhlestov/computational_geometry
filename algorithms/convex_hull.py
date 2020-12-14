def naive(points):
    result = []
    for idx in range(len(points)):
        result.append((points[idx], points[idx % len(points)]))
    return result

def graham(points):
    result = []
    for idx in range(len(points) - 1):
        result.append((points[idx], points[idx + 1]))
    return result
