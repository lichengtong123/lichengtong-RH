"""Reproduce Chapter 19 finite sums with certified ball arithmetic.

Run from any directory. Generated files go to the book's dat directory and
numerical/ch19/results. No asymptotic implied constant is used as a number.
"""

import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import shutil
import time

import flint
from flint import acb, arb, ctx

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent.parent


def mobius(n):
    if n < 1:
        raise ValueError('Mobius index must be positive')
    value, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            value = -value
        p += 1
    return -value if n > 1 else value


def nu(x):
    x = Fraction(x)
    if x < 2:
        raise ValueError('This experiment requires x >= 2')
    n = 0
    while 2 ** (n + 1) <= x:
        n += 1
    return n


def as_ball(x):
    x = Fraction(x)
    return arb(x.numerator) / x.denominator


def weights(x):
    return [(n, arb(mobius(n)) / n)
            for n in range(1, nu(x) + 1) if mobius(n)]


def primes_up_to(n):
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            for q in range(p * p, n + 1, p):
                sieve[q] = 0
    return [p for p in range(2, n + 1) if sieve[p]]


def pi_exact(x):
    x = Fraction(x)
    return len(primes_up_to(x.numerator // x.denominator))


def pi0_exact(x):
    x = Fraction(x)
    p = pi_exact(x)
    return Fraction(p) - (Fraction(1, 2) if x.denominator == 1
                          and x.numerator in primes_up_to(x.numerator) else 0)


def j0_exact(x):
    x = Fraction(x)
    total = Fraction(0)
    for p in primes_up_to(x.numerator // x.denominator):
        power, k = p, 1
        while power <= x:
            total += Fraction(1, 2 * k) if power == x else Fraction(1, k)
            power *= p
            k += 1
    return total


def xi_at(t):
    s = acb(arb(1) / 2, t)
    value = (s * (s - 1) / 2 * (-s * arb.pi().log() / 2).exp()
             * (s / 2).gamma() * s.zeta())
    if not value.imag.contains(0):
        raise ArithmeticError('Xi(t) should be real')
    return value.real


def certified_zeros(config):
    raw = acb.zeta_zeros(1, config['zero_count'] + 1)
    zeros, records = [], []
    previous = arb(0)
    for k, root in enumerate(raw[:-1], 1):
        gamma = arb(root.imag.mid(), config['zero_isolation_radius'])
        if not gamma.contains(root.imag) or not gamma.lower() > previous:
            raise ArithmeticError('Zero intervals must be disjoint enclosures')
        left, right = xi_at(gamma.lower()), xi_at(gamma.upper())
        if not ((left > 0 and right < 0) or (left < 0 and right > 0)):
            raise ArithmeticError(f'No certified sign change at zero {k}')
        records.append({'index': k, 'gamma': gamma.str(45),
                        'xi_left': left.str(20), 'xi_right': right.str(20)})
        zeros.append(acb(arb(1) / 2, gamma))
        previous = gamma.upper()
    counts = []
    for K in config['K_values']:
        height = ((raw[K - 1].imag + raw[K].imag) / 2).mid()
        if not (height > zeros[K - 1].imag.upper()
                and height < raw[K].imag.lower()):
            raise ArithmeticError('Counting height is not in a zero-free gap')
        count = height.zeta_nzeros().unique_fmpz()
        if count is None or int(count) != K:
            raise ArithmeticError(f'Uncertified total zero count at K={K}')
        counts.append({'K': K, 'T': height.str(45), 'N_T': int(count)})
    # K disjoint sign changes plus N(T)=K exclude missed/off-line/multiple zeros.
    return zeros, records, counts


def finite_values(x, zeros, Ks, M):
    L, terms = as_ball(x).log(), weights(x)
    smooth = sum((c * (L / n).ei() for n, c in terms), arb(0))
    constant = -arb(2).log() * sum((c for _, c in terms), arb(0))
    trivial = -sum((c * (-2 * m * L / n).ei()
                    for m in range(1, M + 1) for n, c in terms), arb(0))
    base, cumulative, values = smooth + constant + trivial, arb(0), {}
    targets = set(Ks)
    for k, root in enumerate(zeros[:max(Ks)], 1):
        # Principal Ei and the horizontal branch differ by imaginary constants;
        # their real parts, hence conjugate-pair contributions, agree.
        cumulative += 2 * sum((c * (root * (L / n)).ei().real
                                for n, c in terms), arb(0))
        if k in targets:
            value = base - cumulative
            if not value.is_finite():
                raise ArithmeticError('Nonfinite ball')
            values[k] = value
    return values


def trivial_tail_bound(x, M):
    L, bound = as_ball(x).log(), arb(0)
    for n, c in weights(x):
        a = 2 * L / n
        bound += abs(c) * (-(M + 1) * a).exp() / (
            a * (M + 1) * (1 - (-a).exp()))
    return bound.upper()


def ball_max(values):
    result = arb(0)
    for value in values:
        result = result.max(value)
    return result


def statistics(xs, data, primes):
    output = {}
    for K, values in data.items():
        far, jumps, overshoots = [], [], []
        for x, value in zip(xs, values):
            distance = min(abs(x - p) for p in primes)
            if distance == 0:
                jumps.append(abs(value - as_ball(pi0_exact(x))))
            elif distance >= Fraction(1, 2):
                far.append(value - pi_exact(x))
            else:
                p = min(primes, key=lambda q: abs(x - q))
                if x > p:
                    overshoots.append((value - pi_exact(p)).max(0))
                else:
                    overshoots.append((pi_exact(p) - 1 - value).max(0))
        output[K] = [ball_max([abs(e) for e in far]),
                     (sum((e * e for e in far), arb(0)) / len(far)).sqrt(),
                     ball_max(jumps), ball_max(overshoots)]
    return output


def display(value, digits=12):
    return f'{float(value.mid()):.{digits}f}'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reproduce():
    config = json.loads((HERE / 'config.json').read_text())
    ctx.prec = config['precision_bits']
    results = HERE / 'results'
    results.mkdir(exist_ok=True)
    start = time.perf_counter()
    zeros, records, counts = certified_zeros(config)
    (results / 'zeros.json').write_text(json.dumps(
        {'intervals': records, 'total_counts': counts}, indent=2) + '\n')
    print('500 zero intervals and total counts verified', flush=True)
    denominator = config['grid_step_denominator']
    xs = [Fraction(i, denominator) for i in range(
        config['grid_start'] * denominator,
        config['grid_end'] * denominator + 1)]
    data = {K: [] for K in config['K_values']}
    for i, x in enumerate(xs):
        values = finite_values(x, zeros, config['K_values'], config['M'])
        for K in data:
            data[K].append(values[K])
        if i % 500 == 0:
            print(f'grid {i}/{len(xs)}', flush=True)
    stats = statistics(xs, data, [p for p in primes_up_to(40) if p >= 10])
    row_lines = []
    stat_records = {}
    for K, values in data.items():
        destination = BOOK / 'dat' / f'riemann_data_{K}.dat'
        legacy = results / 'legacy'
        legacy.mkdir(exist_ok=True)
        if destination.exists() and not (legacy / destination.name).exists():
            shutil.copy2(destination, legacy / destination.name)
        destination.write_text('x pi_KM\n' + ''.join(
            f'{float(x):.2f} {display(v)}\n' for x, v in zip(xs, values)))
        with (results / f'intervals_{K}.csv').open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['x_exact', 'pi_KM_enclosure', 'pi0_exact'])
            for x, v in zip(xs, values):
                writer.writerow([str(x), v.str(40), str(pi0_exact(x))])
        row_lines.append(f'${K}$ & ' + ' & '.join(
            f'${display(v, 3)}$' for v in stats[K]) + r' \\' + '\n')
        stat_records[str(K)] = [v.str(35) for v in stats[K]]
    (BOOK / 'dat' / 'ch19-error-rows.tex').write_text(''.join(row_lines))
    x = Fraction(config['certificate_x'])
    sample = finite_values(x, zeros, config['K_values'], config['M'])
    sample_records, sample_rows = [], []
    for K, value in sample.items():
        center = display(value, config['certificate_digits'])
        enclosure = arb(center, config['certificate_radius'])
        if not enclosure.contains(value):
            raise ArithmeticError('Printed certificate does not enclose result')
        error = enclosure - as_ball(pi0_exact(x))
        sample_records.append({'x': str(x), 'K': K, 'M': config['M'],
                               'finite_sum': value.str(45),
                               'printed_enclosure': enclosure.str(40, more=True),
                               'exact_pi0': str(pi0_exact(x)),
                               'posterior_error': error.str(40, more=True),
                               'trivial_tail_bound': trivial_tail_bound(x, config['M']).str(20)})
        sample_rows.append(f'${K}$ & ${center}$ & ${display(error, 6)}$' + r' \\' + '\n')
    (BOOK / 'dat' / 'ch19-certificate-rows.tex').write_text(''.join(sample_rows))
    ctx.prec = config['check_precision_bits']
    higher_zeros = acb.zeta_zeros(1, config['zero_count'])
    higher_values = finite_values(x, higher_zeros, config['K_values'], config['M'])
    for K in sample:
        if not sample[K].overlaps(higher_values[K]):
            raise ArithmeticError(f'Precision cross-check failed at K={K}')
    ctx.prec = config['precision_bits']
    zero_rows = []
    for k in range(1, 6):
        zero_rows.append(f'{k} & {display(zeros[k-1].imag, 6)} & '
                         f'{k+5} & {display(zeros[k+4].imag, 6)}' + r' \\' + '\n')
    (BOOK / 'dat' / 'ch19-zero-rows.tex').write_text(''.join(zero_rows))
    (results / 'summary.json').write_text(json.dumps(
        {'statistics': stat_records, 'sample': sample_records,
         'higher_precision_values': {str(K): v.str(55) for K, v in higher_values.items()}},
        indent=2) + '\n')
    files = [HERE / 'config.json', HERE / 'reproduce.py', HERE / 'test_reproduce.py',
             HERE / 'requirements.txt',
             *(p for p in sorted(results.glob('*.json')) if p.name != 'manifest.json'),
             *sorted(results.glob('*.csv')),
             *(BOOK / 'dat' / f'riemann_data_{K}.dat' for K in data),
             BOOK / 'dat' / 'ch19-error-rows.tex',
             BOOK / 'dat' / 'ch19-certificate-rows.tex',
             BOOK / 'dat' / 'ch19-zero-rows.tex']
    manifest = {'config': config, 'python': platform.python_version(),
                'python_flint': flint.__version__, 'platform': platform.platform(),
                'elapsed_seconds': time.perf_counter() - start,
                'grid_count': len(xs), 'storage_offset': 0,
                'max_internal_radius': max(float(v.rad()) for vs in data.values() for v in vs),
                'files_sha256': {str(p.relative_to(BOOK)): sha256(p) for p in files},
                'scope': 'Finite sums and finite-height zeros certified using FLINT; '
                         'sample errors compared with exact sieve counts; '
                         'no uniform explicit nontrivial-zero-tail bound claimed.'}
    (results / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'statistics': stat_records, 'sample': sample_records,
                      'elapsed_seconds': manifest['elapsed_seconds']}, indent=2), flush=True)


def verify_artifacts():
    manifest = json.loads((HERE / 'results' / 'manifest.json').read_text())
    for path, expected in manifest['files_sha256'].items():
        if sha256(BOOK / path) != expected:
            raise ArithmeticError(f'Hash mismatch: {path}')
    print('All recorded artifact hashes match')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-artifacts', action='store_true')
    args = parser.parse_args()
    if args.verify_artifacts:
        verify_artifacts()
    else:
        reproduce()
