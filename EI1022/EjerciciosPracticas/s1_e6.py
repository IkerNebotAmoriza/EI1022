from math import sqrt


def myfunction(a, b, c):
    if a == 0 or ((b ** 2) - (4 * a * c)) < 0:
        return "No tiene solución."

    if b == 0:
        if -(c / a) < 0:
            return "No tiene solución."
        return sqrt(-(c / a)), -sqrt(-(c / a))

    if c == 0:
        return 0, -(b / a)

    else:
        return (-b + sqrt((b ** 2) - 4 * a * c)) / 2, (-b - sqrt((b ** 2) - 4 * a * c)) / 2
