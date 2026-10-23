"""Reproduce the fixed-parameter example; requires mpmath, not interval arithmetic."""
from pathlib import Path
import mpmath as mp


def calculate(dps):
    with mp.workdps(dps):
        t = mp.mpf('0.095')
        value = mp.quad(lambda u: mp.exp(-u) / (1 + t * u), [0, 1, 10, mp.inf])
        partial = mp.mpf(0)
        rows = []
        for n in range(1, 26):
            partial += (-1) ** (n - 1) * mp.factorial(n - 1) * t ** (n - 1)
            bound = mp.factorial(n) * t ** n
            integral = t ** n * mp.quad(
                lambda u: mp.exp(-u) * u ** n / (1 + t * u),
                [0, 1, n, 2 * n, mp.inf],
            )
            remainder = value - partial
            assert 0 < integral < bound
            assert (-1) ** n * remainder > 0
            assert mp.almosteq(abs(remainder), integral, rel_eps=mp.mpf('1e-60'))
            rows.append((n, bound, integral))
        return value, rows


def main():
    value, rows = calculate(80)
    reference, checked = calculate(120)
    with mp.workdps(80):
        assert abs(value - reference) < mp.mpf('1e-70')
        for first, second in zip(rows, checked):
            assert first[0] == second[0]
            assert all(abs(a - b) < mp.mpf('1e-70') for a, b in zip(first[1:], second[1:]))
    bound_min = min(rows, key=lambda r: r[1])
    error_min = min(rows, key=lambda r: r[2])
    assert bound_min[0] == 10 and error_min[0] == 11
    folder = Path(__file__).resolve().parent / 'figures'
    folder.mkdir(exist_ok=True)
    csv = ['N,bound,error']
    csv.extend(f'{n},{mp.nstr(bound, 18)},{mp.nstr(error, 18)}' for n, bound, error in rows)
    (folder / 'truncation-data.csv').write_text('\n'.join(csv) + '\n', encoding='ascii')
    macros = {
        'trialF': mp.nstr(value, 16),
        'trialBoundN': str(bound_min[0]),
        'trialErrorN': str(error_min[0]),
        'trialBoundMin': mp.nstr(bound_min[1], 18),
        'trialErrorMin': mp.nstr(error_min[2], 18),
    }
    summary = '\n'.join('\\newcommand{\\' + key + '}{' + val + '}' for key, val in macros.items())
    (folder / 'truncation-summary.tex').write_text(summary + '\n', encoding='ascii')
    print(f'Validated 25 rows at 80/120 digits. Minimum bound N={bound_min[0]}; error N={error_min[0]}.')


if __name__ == '__main__':
    main()
