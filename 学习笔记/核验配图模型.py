"""Check the elementary models in the figures of notes 07 and 10."""

import cmath
from fractions import Fraction
import math
import unittest


class FigureModels(unittest.TestCase):
    def test_unit_vector_hexagon(self):
        points = [0j, 1, 1.5 + math.sqrt(3) * 1j / 2,
                  1 + math.sqrt(3) * 1j, math.sqrt(3) * 1j,
                  -0.5 + math.sqrt(3) * 1j / 2, 0j]
        for k, (left, right) in enumerate(zip(points, points[1:])):
            self.assertAlmostEqual(abs(right - left - cmath.exp(1j * k * math.pi / 3)), 0, places=13)

    def test_all_discrete_plot_samples(self):
        for n in range(1, 81):
            fixed = abs(sum(cmath.exp(1j * k * math.pi / 3) for k in range(n))) / n
            moving = abs(sum(cmath.exp(1j * k * math.pi / n) for k in range(n))) / n
            self.assertAlmostEqual(fixed, 2 * abs(math.sin(n * math.pi / 6)) / n, places=13)
            self.assertAlmostEqual(moving, 1 / (n * math.sin(math.pi / (2 * n))), places=13)
        self.assertLess(abs(moving - 2 / math.pi), 0.00005)

    def test_exact_rational_transform_points(self):
        expected = [(Fraction(1, 5), Fraction(8, 5)),
                    (Fraction(0), Fraction(1)),
                    (Fraction(1, 13), Fraction(8, 13))]
        for x, (u, v) in zip([Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)], expected):
            y = Fraction(1, 2)
            self.assertEqual(1 - x / (x*x + y*y), u)
            self.assertEqual(y / (x*x + y*y), v)

    def test_circle_identity_and_pair_sum(self):
        for x in [-2, 0.25, 0.5, 0.75, 2]:
            for y in [-2, -0.5, 0.5, 2]:
                z = complex(x, y)
                self.assertAlmostEqual(abs(1 - 1/z)**2, 1 + (1 - 2*x)/abs(z)**2, places=13)
        q = cmath.exp(2j * math.pi / 5)
        total = (1 - q) + (1 - q.conjugate())
        self.assertEqual(total.imag, 0)
        self.assertGreaterEqual(total.real, 0)
        self.assertAlmostEqual(total.real, 2 * (1 - math.cos(2*math.pi/5)), places=13)


if __name__ == '__main__':
    unittest.main(verbosity=2)
