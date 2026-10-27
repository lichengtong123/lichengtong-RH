"""Fourier sum of the period-30 extension of pi(x)-6 on [10, 40)."""

import math
from pathlib import Path


EDGES = (10, 11, 13, 17, 19, 23, 29, 31, 37, 40)
VALUES = tuple(range(-2, 7))
PERIOD = 30
ORDER = 100


def coefficients():
    mean = sum(v * (b - a) for a, b, v in
               zip(EDGES[:-1], EDGES[1:], VALUES)) / PERIOD
    terms = []
    for n in range(1, ORDER + 1):
        k = 2 * math.pi * n / PERIOD
        an = bn = 0.0
        for a, b, value in zip(EDGES[:-1], EDGES[1:], VALUES):
            a, b = a - 10, b - 10
            an += value * (math.sin(k * b) - math.sin(k * a))
            bn += value * (math.cos(k * a) - math.cos(k * b))
        terms.append((k, 2 * an / (PERIOD * k),
                      2 * bn / (PERIOD * k)))
    return mean, terms


def partial_sum(x, mean, terms):
    t = x - 10
    return mean + sum(a * math.cos(k * t) + b * math.sin(k * t)
                      for k, a, b in terms)


if __name__ == "__main__":
    mean, terms = coefficients()
    output = Path(__file__).with_name("fourier_data.dat")
    with output.open("w", encoding="ascii") as stream:
        stream.write("x y\n")
        for i in range(1000):
            x = 10 + 25 * i / 999
            stream.write(f"{x:.6f} {partial_sum(x, mean, terms):.6f}\n")
    print(f"Generated {output.name}: N={ORDER}, period={PERIOD}, mean={mean:.12g}")
