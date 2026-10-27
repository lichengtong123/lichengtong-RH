import json
from fractions import Fraction
from pathlib import Path
import unittest

from flint import acb, arb, ctx
import mpmath as mp

from reproduce import (finite_values, j0_exact, mobius, nu, pi0_exact,
                       trivial_tail_bound, weights, xi_at)


class Chapter19Tests(unittest.TestCase):
    def setUp(self):
        ctx.prec = 160

    def test_mobius(self):
        self.assertEqual([mobius(n) for n in range(1, 11)],
                         [1, -1, -1, 0, -1, 1, -1, 0, 0, 1])

    def test_exact_cutoff(self):
        self.assertEqual(nu(Fraction(319999, 10000)), 4)
        self.assertEqual(nu(32), 5)
        self.assertEqual(nu(64), 6)

    def test_midpoint_and_mobius_inversion(self):
        for x in [Fraction(41, 2), Fraction(11), Fraction(16), Fraction(32)]:
            result = Fraction(0)
            for n in range(1, nu(x) + 1):
                # Count prime powers p^k with p^(kn) <= x, preserving midpoint.
                from reproduce import primes_up_to
                for p in primes_up_to(int(x)):
                    k = 1
                    while p ** (k * n) <= x:
                        result += Fraction(mobius(n), n * k) * (
                            Fraction(1, 2) if p ** (k * n) == x else 1)
                        k += 1
            self.assertEqual(result, pi0_exact(x))
        self.assertEqual(j0_exact(Fraction(41, 2)), Fraction(115, 12))

    def test_conjugate_pairs(self):
        root = acb.zeta_zero(1)
        z = root * arb('20.5').log()
        self.assertTrue(z.ei().conjugate().overlaps(z.conjugate().ei()))
        self.assertTrue((z.ei() + z.conjugate().ei()).imag.contains(0))

    def test_tail_bound(self):
        for x in [10, Fraction(41, 2), 32, 40]:
            bound = trivial_tail_bound(x, 10)
            L = arb(str(x)).log()
            explicit = sum((abs(c) * sum((abs((-2*m*L/n).ei())
                           for m in range(11, 41)), arb(0))
                           for n, c in weights(x)), arb(0))
            self.assertTrue(bound > explicit.upper())
            self.assertTrue(bound < arb('1e-7'))

    def test_two_precisions(self):
        ctx.prec = 160
        v160 = finite_values(Fraction(41, 2), acb.zeta_zeros(1, 20), [20], 10)[20]
        ctx.prec = 224
        v224 = finite_values(Fraction(41, 2), acb.zeta_zeros(1, 20), [20], 10)[20]
        self.assertTrue(v160.overlaps(v224))
        self.assertTrue(v224.rad() < v160.rad())

    def test_independent_mpmath_evaluation(self):
        mp.mp.dps = 60
        L = mp.log(mp.mpf(41) / 2)
        terms = [(n, mp.mpf(mobius(n))/n) for n in range(1, 5) if mobius(n)]
        expected = sum(c*mp.ei(L/n) for n, c in terms)
        expected -= mp.log(2)*sum(c for _, c in terms)
        expected -= sum(c*mp.ei(-2*m*L/n) for m in range(1, 11) for n, c in terms)
        for k in range(1, 21):
            root = mp.zetazero(k)
            expected -= 2*mp.re(sum(c*mp.ei(root*L/n) for n, c in terms))
        actual = finite_values(Fraction(41, 2), acb.zeta_zeros(1, 20), [20], 10)[20]
        self.assertTrue(actual.overlaps(arb(mp.nstr(expected, 55))))

    def test_isolation_and_count_example(self):
        root = acb.zeta_zero(1)
        interval = arb(root.imag.mid(), '1e-35')
        a, b = xi_at(interval.lower()), xi_at(interval.upper())
        self.assertTrue((a > 0 and b < 0) or (a < 0 and b > 0))
        self.assertEqual(arb(15).zeta_nzeros().unique_fmpz(), 1)

    def test_generated_certificates(self):
        path = Path(__file__).parent / 'results' / 'summary.json'
        if not path.exists():
            self.skipTest('Run reproduce.py first')
        for record in json.loads(path.read_text())['sample']:
            enclosure = arb(record['printed_enclosure'])
            self.assertTrue(enclosure.contains(arb(record['finite_sum'])))
            self.assertTrue(enclosure.rad() < arb('2e-12'))


if __name__ == '__main__':
    unittest.main()
