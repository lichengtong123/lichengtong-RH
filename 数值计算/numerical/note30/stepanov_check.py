# Stepanov 方法的数值核对（学习笔记 30）
# 1) 对小素数 p 实际解出辅助多项式 R，检验：R≠0，R 在 S 的每一点上至少 ℓ 重零点，ℓ|S| ≤ deg R
# 2) 对大素数 p 比较 |S|、Stepanov 上界 p/2+m+(m+2)^{3/2}√p 与 Weil 界
import math, sys

def trim(a):
    while a and a[-1] == 0: a.pop()
    return a
def add(a, b, p):
    n = max(len(a), len(b)); r = [0]*n
    for i, x in enumerate(a): r[i] = x
    for i, x in enumerate(b): r[i] = (r[i] + x) % p
    return trim(r)
def mul(a, b, p):
    if not a or not b: return []
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i+j] = (r[i+j] + x*y) % p
    return trim(r)
def scal(c, a, p): return trim([(c*x) % p for x in a])
def deriv(a, p): return trim([(i*a[i]) % p for i in range(1, len(a))])
def pw(a, n, p):
    r = [1]
    for _ in range(n): r = mul(r, a, p)
    return r
def shift(a, n): return [0]*n + a if a else []
def ev(a, x, p):
    v = 0
    for c in reversed(a): v = (v*x + c) % p
    return v

def nullvec(M, ncols, p):
    # 返回 M v = 0 的一个非零解（mod p）
    rows = [r[:] for r in M]; piv = []; r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if pr is None: continue
        rows[r], rows[pr] = rows[pr], rows[r]
        inv = pow(rows[r][c], p-2, p)
        rows[r] = [(x*inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                t = rows[i][c]
                rows[i] = [(x - t*y) % p for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
        if r == len(rows): break
    free = [c for c in range(ncols) if c not in piv][0]
    v = [0]*ncols; v[free] = 1
    for i, c in enumerate(piv): v[c] = (-rows[i][free]) % p
    return v

def params(p, m):
    c = (p-1)//2
    l = math.isqrt(p//(m+1))
    while (l+1)*(l+1)*(m+1) <= p: l += 1
    while l*l*(m+1) > p: l -= 1
    J = (l+1)//2 + 1
    K = c - m
    return c, l, J, K

def construct(p, f):
    m = len(f)-1
    c, l, J, K = params(p, m)
    fp = deriv(f, p)
    # 未知量：r_j 的系数 (A 型) 与 s_j 的系数 (B 型)，j<J，次数 ≤ K
    unknowns = [(t, j, i) for t in (0, 1) for j in range(J) for i in range(K+1)]
    cols = []
    for (t, j, i) in unknowns:
        N = l + (c if t else 0); g = [0]*i + [1]
        col = []
        for k in range(l):
            # 第 k 阶导数的 T_k 部分：g_k(x)·x^j
            Tk = shift(g, j)
            width = K + k*(m-1) + J
            col += (Tk + [0]*width)[:width]
            # 求下一阶：(N, g) -> (N-1, N f' g + f g')
            g = add(scal(N % p, mul(fp, g, p), p), mul(f, deriv(g, p), p), p); N -= 1
        cols.append(col)
    nr = len(cols[0]); nc = len(cols)
    M = [[cols[jj][ii] for jj in range(nc)] for ii in range(nr)]
    assert nc > nr, (nc, nr)
    v = nullvec(M, nc, p)
    # 组装 R = f^l Σ (r_j + s_j f^c) x^{jp}
    fc = pw(f, c, p); A = []; B = []
    for idx, (t, j, i) in enumerate(unknowns):
        if v[idx]:
            term = shift([v[idx]], i + j*p)
            if t: B = add(B, term, p)
            else: A = add(A, term, p)
    R = mul(pw(f, l, p), add(A, mul(fc, B, p), p), p)
    S = [x for x in range(p) if ev(fc, x, p) == 1]
    def mult(P, x0):
        e = 0; Q = P[:]
        while Q and ev(Q, x0, p) == 0:
            # 除以 (x - x0)
            n = len(Q)-1; q = [0]*n; acc = 0
            for kk in range(n, 0, -1):
                acc = (acc*x0 + Q[kk]) % p; q[kk-1] = acc
            Q = trim(q); e += 1
        return e
    ms = [mult(R, x) for x in S]
    return dict(p=p, m=m, l=l, J=J, K=K, unknowns=nc, equations=nr,
                R_nonzero=bool(R), degR=len(R)-1, S=len(S), min_mult=min(ms),
                bound_deg=l*m + K + c*m + (J-1)*p)

def legendre_sum(p, f):
    c = (p-1)//2; S = Sp = z = 0; s = 0
    for x in range(p):
        v = ev(f, x, p)
        if v == 0: z += 1; continue
        if pow(v, c, p) == 1: S += 1; s += 1
        else: Sp += 1; s -= 1
    return S, Sp, z, s

if __name__ == '__main__':
    print('== 1. 构造辅助多项式 ==')
    for p, f in [(67, [1, 1, 0, 1]), (101, [1, 1, 0, 1]), (149, [3, 0, 2, 0, 1]), (97, [0, 1])]:
        r = construct(p, f)
        print(r)
        assert r['R_nonzero'] and r['min_mult'] >= r['l'] and r['degR'] <= r['bound_deg']
        assert r['l']*r['S'] <= r['degR']
    print('== 2. 大素数上的比较：f = x^3 + x + 1 ==')
    f = [1, 1, 0, 1]; m = 3
    for p in [10007, 100003, 1000003]:
        S, Sp, z, s = legendre_sum(p, f)
        ub = p/2 + m + (m+2)**1.5*math.sqrt(p)
        print(f'p={p}  |S|={S}  p/2={p/2}  Stepanov上界={ub:.1f}  '
              f'Σ(f/p)={s}  Weil界 2√p={2*math.sqrt(p):.1f}')
    print('== 3. 参数不等式检查（16(m+1) ≤ p ≤ 20000, 1 ≤ m ≤ 8）==')
    bad = 0
    for m in range(1, 9):
        for p in range(16*(m+1), 20000):
            if p < 3 or any(p % d == 0 for d in range(2, math.isqrt(p)+1)): continue
            c, l, J, K = params(p, m)
            eqs = sum(K + k*(m-1) + J for k in range(l))
            ok = 2*J*(K+1) > eqs and K >= 0 and 2*K + m <= p-1 and l < p
            ub_exact = m + (K + c*m + (J-1)*p)/l
            ok = ok and ub_exact <= p/2 + m + (m+2)**1.5*math.sqrt(p)
            if not ok: bad += 1; print('fail', m, p)
    print('失败个数：', bad)
