# Chapter 19 reproducible calculation, version 2.0

Companion code and data for chapter 19 of the book. In the resource repository
this directory sits under `数值计算/`, next to the generated `dat/` files.

## Run

Python 3.11 was used for this run. Install the pinned requirements in an isolated
environment, then run from the parent directory of `numerical/` (`数值计算/` in the repository):

```sh
python3 -m pip install -r numerical/ch19/requirements.txt
python3 numerical/ch19/reproduce.py
python3 -m unittest discover -s numerical/ch19 -v
python3 numerical/ch19/reproduce.py --verify-artifacts
```

The generator resolves paths relative to itself, so its working directory does
not affect outputs. Parameters are in `config.json`; timing and exact platform
versions are recorded in `results/manifest.json`, not hard-coded in the book.

## Scope of the certificate

1. FLINT supplies candidate zeros. The script builds disjoint real intervals
   with radius 1e-35, proves a sign change of real Xi at each pair of endpoints,
   and obtains exact total counts N(T)=K at intermediate heights using FLINT.
   K sign changes plus K zeros counted with multiplicity imply completeness and
   simplicity below those heights. This invokes FLINT; it is not a separate
   implementation of Turing's algorithm and is not a proof of RH.
2. All finite sums use arb/acb at 160 bits, with zero intervals propagated through
   the special functions. The principal Ei's real part equals that of the book's
   horizontal branch; the imaginary branch constants cancel in conjugate pairs.
   Finite results at rational grid points have rigorous enclosures. Decimal
   plot files contain rounded midpoints, not interval certificates.
3. At x=41/2, decimal centers have verified radius 1e-12. The sieve gives the
   independently exact count 8. Subtracting 8 gives certified posterior errors.
   This is NOT an independent prime-counting algorithm using a priori analytic
   tail bounds. The nontrivial-zero-tail bound in the book still has unspecified
   implied constants and is not used as an explicit numerical certificate.
4. The trivial-zero tail has a computable bound derived from
   E1(a*m) <= exp(-a*m)/(a*m) and a geometric series. Its formula is implemented
   in `trivial_tail_bound`; the bound is below 5e-8 on the plotted range.
5. Grid statistics concern 3001 rational samples only, NOT the supremum or RMS
   over a continuous interval. No interpolation error certificate is claimed.

## Outputs

- `dat/riemann_data_{20,60,200,500}.dat`: x and pi_KM itself, no storage offset.
  Both plot and table use x=10+i/100, i=0,...,3000. Three-digit table rounding
  agrees with the old version, but plot curves now use the same denser grid.
- `dat/ch19-*-rows.tex`: generated rows for the zero, error and sample tables.
- `results/zeros.json`: enclosures, Xi endpoint values and total counts.
- `results/intervals_K.csv`: each sample's enclosing ball and exact pi0 target.
- `results/summary.json`: statistics, sample certificates and 224-bit checks.
- `results/manifest.json`: parameter snapshot, environment, timing, numerical
  precision, maximum internal radius, and SHA-256 digests of code and outputs.
- `results/legacy/`: first pre-v2 plot files saved for comparison; never read by
  the new plotting code. They use the old minus-six storage convention.

Keep this directory and the generated `dat` files together; `reproduce.py` is
the only current entry point.

## Checks

The tests exercise Mobius coefficients, exact base-two cutoffs, midpoint counts
and finite Mobius inversion, conjugate pairing, the trivial-tail inequality,
160/224-bit overlap, independent mpmath evaluation, and a sign/count example.
Tests verify generated sample certificate serialization too. Artifact hashes
detect stale or modified output; they do not themselves prove a mathematical
result. Tests and precision agreement are distinct from ball certification.

## References

- [python-flint arb API](https://python-flint.readthedocs.io/en/stable/arb.html)
- [python-flint acb API](https://python-flint.readthedocs.io/en/stable/acb.html)
- [Johansson, Arb (2017)](https://arxiv.org/abs/1611.02831)

The trusted numerical base is the installed python-flint/FLINT implementation.
The exact pip version is pinned; an archival release should additionally record
the platform wheel or lockfile rather than assume all future builds are identical.
