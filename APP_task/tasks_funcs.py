import math

def solve_quadratic_equation(a: float, b: float, c: float) -> list:
    discr = b ** 2 - 4 * a * c

    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        return [x1, x2]
    elif discr == 0:
        x = -b / (2 * a)
        return [x]
    else:
        return ['There are no roots']
