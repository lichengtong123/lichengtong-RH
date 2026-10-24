"""学习笔记第 17 篇的数值表：J_0 的零点截断、周期 Fourier 部分和与零点函数系最小二乘拟合的误差比较。
依赖 mpmath、numpy、sympy；默认30位工作精度。缓存仅写系统临时目录。
运行 --dps 50 可独立复算；--check 可直接核对文中表格的三位小数。
"""
import argparse
import json
from pathlib import Path
import tempfile

import numpy as np
import mpmath as mp

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--dps", type=int, default=30)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
if args.dps < 20:
    parser.error("--dps must be at least 20")
mp.mp.dps = args.dps
K = 400
cache_dir = Path(tempfile.gettempdir()) / "rh-note17-cache"
cache_dir.mkdir(exist_ok=True)
zf = cache_dir / f"zeros-{K}-{args.dps}.json"
if zf.exists():
    Z = [mp.mpc(re, im) for re, im in json.loads(zf.read_text())]
else:
    Z = [mp.zetazero(k) for k in range(1, K + 1)]
    zf.write_text(json.dumps([[str(z.real), str(z.imag)] for z in Z]))
print("mpmath", mp.__version__, "numpy", np.__version__, "dps", args.dps, flush=True)
print('gamma_100', Z[99].imag, 'gamma_400', Z[399].imag)

from sympy import primerange
pp = []  # (p^k, 1/k)
for p in primerange(2, 2000):
    q, k = p, 1
    while q < 2000:
        pp.append((q, 1.0 / k)); q *= p; k += 1
pp.sort()
def J0(x):
    s = 0.0
    for q, w in pp:
        if q < x: s += w
        elif q == x: s += w / 2
        else: break
    return s

xs = np.round(np.arange(13.0, 35.0001, 0.05), 10)
jumps = [q for q, _ in pp if 13 <= q <= 35]
far = np.array([min(abs(x - q) for q in jumps) >= 0.5 for x in xs])
J = np.array([J0(x) for x in xs])

# Riemann terms
def tailint(x):
    return mp.quad(lambda t: 1 / (t * (t * t - 1) * mp.log(t)), [x, mp.inf])
base = np.array([float(mp.li(x) - mp.log(2) + tailint(x)) for x in xs])
cache = cache_dir / f"terms-{K}-{args.dps}-441.npy"
if cache.exists():
    T = np.load(cache, allow_pickle=False)
    if T.shape != (K, len(xs)):
        raise ValueError("Unexpected cached array shape")
else:
    T = np.zeros((K, len(xs)), dtype=complex)
    for k in range(K):
        r = Z[k]
        for i, x in enumerate(xs):
            T[k, i] = complex(mp.ei(r * mp.log(x)))
        if (k + 1) % 50 == 0:
            print("Ei rows", k + 1, "of", K, flush=True)
    np.save(cache, T)
def riemann(Kk):
    return base - 2 * np.real(T[:Kk].sum(axis=0))

# Fourier of J0 on [a,b)
def fourier(a, b, N, x):
    L = b - a
    # piecewise constant on [a,b): breakpoints
    qs = [q for q, _ in pp if a < q < b]
    edges = [a] + qs + [b]
    vals = [J0((edges[i] + edges[i + 1]) / 2) for i in range(len(edges) - 1)]
    t = x - a
    c0 = sum(v * (edges[i + 1] - edges[i]) for i, v in enumerate(vals)) / L
    S = np.full_like(t, c0)
    for n in range(1, N + 1):
        w = 2 * np.pi * n / L
        an = sum(v * (np.sin(w * (edges[i + 1] - a)) - np.sin(w * (edges[i] - a))) / w for i, v in enumerate(vals)) * 2 / L
        bn = sum(v * (-np.cos(w * (edges[i + 1] - a)) + np.cos(w * (edges[i] - a))) / w for i, v in enumerate(vals)) * 2 / L
        S += an * np.cos(w * t) + bn * np.sin(w * t)
    return S

def stats(A):
    e = A - J
    return np.sqrt(np.mean(e ** 2)), np.max(np.abs(e[far]))

res = {}
for Kk in [25, 50, 100, 200, 250, 400]:
    res['R%d' % Kk] = stats(riemann(Kk))
for (a, b) in [(10, 40), (2, 100), (2, 1000)]:
    for N in [25, 100]:
        res['F[%d,%d)N%d' % (a, b, N)] = stats(fourier(a, b, N, xs))
# Free-coefficient fits are diagnostics, not the original explicit formula.
for Kk in [25, 100]:
    B = np.vstack([np.ones_like(xs), base] + [np.real(T[k]) for k in range(Kk)] + [np.imag(T[k]) for k in range(Kk)]).T
    for threshold in [None, 1e-10, 1e-8]:
        coef, _, rank, singular = np.linalg.lstsq(B, J, rcond=threshold)
        condition = singular[0] / singular[-1]
        print(f"LS diagnostic K={Kk} rcond={threshold} rank={rank}/{B.shape[1]} "
              f"condition={condition:.3e} rms/max={stats(B @ coef)}")
for k, v in res.items():
    print(f'{k:20s} rms={v[0]:.4f} maxfar={v[1]:.4f}')

if args.check:
    expected = {
        "R25": (0.136, 0.168), "R50": (0.104, 0.106),
        "R100": (0.072, 0.076), "R200": (0.047, 0.048),
        "R250": (0.039, 0.043), "R400": (0.026, 0.030),
        "F[10,40)N25": (0.137, 0.267), "F[10,40)N100": (0.040, 0.041),
        "F[2,100)N25": (0.289, 0.536), "F[2,100)N100": (0.107, 0.175),
        "F[2,1000)N25": (10.19, 15.76), "F[2,1000)N100": (3.06, 5.64),
    }
    for name, target in expected.items():
        tolerance = 0.0051 if name.startswith("F[2,1000)") else 0.00051
        if max(abs(a - b) for a, b in zip(res[name], target)) > tolerance:
            raise AssertionError((name, res[name], target))
    print("All displayed table entries agree with the recomputation.")
