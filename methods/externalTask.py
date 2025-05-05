import math

def find_discontinuities(f, a, b, samples=1000, threshold=1e8):
    step = (b - a) / samples
    raw_points = set()

    for i in range(math.ceil(a), math.floor(b) + 1):
        try:
            value = f(i)
            if math.isnan(value) or math.isinf(value) or abs(value) > threshold:
                raw_points.add(i)
        except:
            raw_points.add(i)

    for i in range(samples + 1):
        x = a + i * step
        try:
            value = f(x)
            if math.isnan(value) or math.isinf(value) or abs(value) > threshold:
                raw_points.add(x)
        except:
            raw_points.add(x)

    sorted_points = sorted(raw_points)
    discontinuities = []

    for x in sorted_points:
        if not discontinuities or abs(x - discontinuities[-1]) > step:
            discontinuities.append(x)

    return discontinuities

def try_to_compute(f, x, threshold=1e4):
    try:
        value = f(x)
        if math.isnan(value) or math.isinf(value) or abs(value) > threshold:
            return None
        return value
    except:
        return None
