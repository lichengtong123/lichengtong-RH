"""学习笔记第 17 篇的数值表：J_0 的零点截断、周期 Fourier 部分和与零点函数系最小二乘拟合的误差比较。
依赖 mpmath、numpy、sympy；首次运行需计算 400 个零点及相应 Ei 值，耗时数分钟。
"""
import numpy as np, mpmath as mp, pickle, os, sys
mp.mp.dps = 20
K = 400
zf = 'zeros.pkl'  # 缓存，可删除
if os.path.exists(zf):
    Z = pickle.load(open(zf, 'rb'))
else:
    Z = [mp.zetazero(k) for k in range(1, K + 1)]
    pickle.dump(Z, open(zf, 'wb'))
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
cache = 'terms.npy'  # 缓存，可删除
if os.path.exists(cache):
    T = np.load(cache)
else:
    T = np.zeros((K, len(xs)), dtype=complex)
    for k in range(K):
        r = Z[k]
        for i, x in enumerate(xs):
            T[k, i] = complex(mp.ei(r * mp.log(x)))
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
# least squares in zero basis on window, K=100
for Kk in [25, 100]:
    B = np.vstack([np.ones_like(xs), base] + [np.real(T[k]) for k in range(Kk)] + [np.imag(T[k]) for k in range(Kk)]).T
    coef, *_ = np.linalg.lstsq(B, J, rcond=None)
    res['LSzero%d' % Kk] = stats(B @ coef)
for k, v in res.items():
    print(f'{k:20s} rms={v[0]:.4f} maxfar={v[1]:.4f}')
