def left_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))

def right_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 1) * h) for i in range(n))

def mid_rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))

def trapezoidal(f, a, b, n):
    h = (b - a) / n
    return h * (0.5 * f(a) + 0.5 * f(b) + sum(f(a + i * h) for i in range(1, n)))

def simpson(f, a, b, n):
    if n % 2:
        n += 1
    h = (b - a) / n
    return h / 3 * (f(a) + 2 * sum(f(a + i * h) for i in range(2, n, 2)) +
                    4 * sum(f(a + i * h) for i in range(1, n, 2)) + f(b))

def runge_method(method, f, a, b, eps, n=4):
    try:
        I1 = method(f, a, b, n)
        n *= 2
        I2 = method(f, a, b, n)
        p = 4 if method == simpson else 2
        while abs(I2 - I1) / (2 ** p - 1) > eps:
            I1 = I2
            n *= 2
            I2 = method(f, a, b, n)
            if n > 1e6:
                raise ValueError(4)
        return I2, n
    except Exception:
        raise