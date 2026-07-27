#!/usr/bin/env python3
"""Exact symbolic checks for the nodal parity-thickening note."""

from __future__ import annotations

import math

import sympy as sp


x, y, s = sp.symbols("x y s")


# ---------------------------------------------------------------------------
# Rank-one separated classification.

p0 = sp.Function("p0")(x)
q0 = sp.Function("q0")(x)
p1 = sp.Function("p1")(x)
q1 = sp.Function("q1")(x)
phi = sp.Function("phi")(y)

F = p0 + p1 * phi
G = q0 + q1 * phi
jacobian = sp.expand(sp.diff(F, x) * sp.diff(G, y) - sp.diff(F, y) * sp.diff(G, x))
R = sp.diff(p0, x) * q1 - p1 * sp.diff(q0, x)
W = sp.diff(p1, x) * q1 - p1 * sp.diff(q1, x)
assert sp.simplify(jacobian - sp.diff(phi, y) * (R + W * phi)) == 0


# The exact nodal ansatz.
lam = sp.symbols("lambda", nonzero=True)
A = sp.Function("A")(y)
Bfun = sp.Function("B")(y)
F_nodal = x**2 + A
G_nodal = x**3 - x + x * Bfun
J_nodal = sp.Poly(
    sp.expand(
        sp.diff(F_nodal, x) * sp.diff(G_nodal, y)
        - sp.diff(F_nodal, y) * sp.diff(G_nodal, x)
    ),
    x,
)
assert J_nodal.coeff_monomial(x**2) == 2 * sp.diff(Bfun, y) - 3 * sp.diff(A, y)
assert sp.simplify(
    J_nodal.coeff_monomial(1) - sp.diff(A, y) * (1 - Bfun)
) == 0

# Check the square-root solution through a long exact truncation.
order = 20
A_series = sp.series(
    sp.Rational(2, 3) * (1 - sp.sqrt(1 - 3 * lam * y)),
    y,
    0,
    order,
).removeO()
B_series = sp.Rational(3, 2) * A_series
residual = sp.series(
    sp.diff(A_series, y) * (1 - B_series) - lam,
    y,
    0,
    order - 1,
).removeO()
assert sp.expand(residual) == 0


# ---------------------------------------------------------------------------
# Parity reduction and top-face equation.

Pfun = sp.Function("P")(s, y)
Qfun = sp.Function("Q")(s, y)
F_parity = Pfun.subs(s, x**2)
G_parity = x * Qfun.subs(s, x**2)
J_parity = sp.expand(
    sp.diff(F_parity, x) * sp.diff(G_parity, y)
    - sp.diff(F_parity, y) * sp.diff(G_parity, x)
)
expected_parity = (
    2
    * s
    * (sp.diff(Pfun, s) * sp.diff(Qfun, y) - sp.diff(Pfun, y) * sp.diff(Qfun, s))
    - sp.diff(Pfun, y) * Qfun
).subs(s, x**2)
assert sp.simplify(J_parity - expected_parity) == 0

m_sym, n_sym = sp.symbols("m n", positive=True, integer=True)
pm = sp.Function("pm")(s)
qn = sp.Function("qn")(s)
top_face = 2 * s * (
    n_sym * sp.diff(pm, s) * qn - m_sym * pm * sp.diff(qn, s)
) - m_sym * pm * qn
assert sp.simplify(
    top_face / (pm * qn)
    - (
        2
        * s
        * sp.diff(sp.log(pm**n_sym / qn**m_sym), s)
        - m_sym
    )
) == 0

# The gcd condition is equivalent to the strict two-adic inequality.
def v2(value: int) -> int:
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


for m0 in range(1, 100):
    for n0 in range(1, 100):
        gcd_condition = m0 % 2 == 0 and (m0 // 2) % math.gcd(m0, n0) == 0
        assert gcd_condition == (v2(m0) > v2(n0))


# ---------------------------------------------------------------------------
# Coefficient identities used in the low-support obstructions.

def parity_residual(P: sp.Expr, Q: sp.Expr) -> sp.Poly:
    expr = (
        2 * s * (sp.diff(P, s) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, s))
        - sp.diff(P, y) * Q
        - 1
    )
    return sp.Poly(sp.expand(expr), y)


# n=1 recurrence.
M = 7
b = sp.Function("b")(s)
p = [sp.Function(f"p{i}")(s) for i in range(M + 1)]
P_generic = sum(p[i] * y**i for i in range(M + 1))
Q_linear = s - 1 + b * y
coeffs = parity_residual(P_generic, Q_linear)
for r in range(M + 1):
    expected = (
        2 * s * b * sp.diff(p[r], s)
        - r * (2 * s * sp.diff(b, s) + b) * p[r]
        - (r + 1) * (3 * s - 1) * (p[r + 1] if r < M else 0)
        - (1 if r == 0 else 0)
    )
    assert sp.simplify(coeffs.coeff_monomial(y**r) - expected) == 0


# m=2 recurrence.
N = 7
a = sp.Function("a")(s)
c = sp.Function("c")(s)
q = [sp.Function(f"q{i}")(s) for i in range(N + 1)]
P_quadratic = s + a * y + c * y**2
Q_generic = sum(q[j] * y**j for j in range(N + 1))
coeffs = parity_residual(P_quadratic, Q_generic)
for r in range(1, N + 1):
    expected = (
        2 * s * (r + 1) * (q[r + 1] if r < N else 0)
        + 2 * s * r * sp.diff(a, s) * q[r]
        - 2 * s * a * sp.diff(q[r], s)
        - a * q[r]
        + 2 * s * (r - 1) * sp.diff(c, s) * q[r - 1]
        - 4 * s * c * sp.diff(q[r - 1], s)
        - 2 * c * q[r - 1]
    )
    assert sp.simplify(coeffs.coeff_monomial(y**r) - expected) == 0


# Explicit (4,2) coefficient system.
a, u, v, w, b, c = [
    sp.Function(name)(s) for name in ("a", "u", "v", "w", "b", "c")
]
P42 = s + a * y + u * y**2 + v * y**3 + w * y**4
Q42 = s - 1 + b * y + c * y**2
C42 = parity_residual(P42, Q42)
expected42 = {
    0: -3 * s * a + 2 * s * b + a - 1,
    1: (
        -2 * s * a * sp.diff(b, s)
        + 2 * s * b * sp.diff(a, s)
        + 4 * s * c
        - 6 * s * u
        - a * b
        + 2 * u
    ),
    2: (
        -2 * s * a * sp.diff(c, s)
        + 2 * s * b * sp.diff(u, s)
        + 4 * s * c * sp.diff(a, s)
        - 4 * s * u * sp.diff(b, s)
        - 9 * s * v
        - a * c
        - 2 * b * u
        + 3 * v
    ),
    3: (
        2 * s * b * sp.diff(v, s)
        + 4 * s * c * sp.diff(u, s)
        - 4 * s * u * sp.diff(c, s)
        - 6 * s * v * sp.diff(b, s)
        - 12 * s * w
        - 3 * b * v
        - 2 * c * u
        + 4 * w
    ),
    4: (
        2 * s * b * sp.diff(w, s)
        + 4 * s * c * sp.diff(v, s)
        - 6 * s * v * sp.diff(c, s)
        - 8 * s * w * sp.diff(b, s)
        - 4 * b * w
        - 3 * c * v
    ),
    5: 4 * (s * c * sp.diff(w, s) - 2 * s * w * sp.diff(c, s) - c * w),
}
for degree, expected in expected42.items():
    assert sp.simplify(C42.coeff_monomial(y**degree) - expected) == 0


# Explicit (4,3) coefficient system, focusing on the four equations used.
d = sp.Function("d")(s)
Q43 = Q42 + d * y**3
C43 = parity_residual(P42, Q43)
expected43 = {
    1: expected42[1],
    2: expected42[2] + 6 * s * d,
    3: (
        -2 * s * a * sp.diff(d, s)
        + 2 * s * b * sp.diff(v, s)
        + 4 * s * c * sp.diff(u, s)
        + 6 * s * d * sp.diff(a, s)
        - 4 * s * u * sp.diff(c, s)
        - 6 * s * v * sp.diff(b, s)
        - 12 * s * w
        - a * d
        - 3 * b * v
        - 2 * c * u
        + 4 * w
    ),
    5: (
        4 * s * c * sp.diff(w, s)
        + 6 * s * d * sp.diff(v, s)
        - 6 * s * v * sp.diff(d, s)
        - 8 * s * w * sp.diff(c, s)
        - 4 * c * w
        - 3 * d * v
    ),
    6: 2 * (
        3 * s * d * sp.diff(w, s)
        - 4 * s * w * sp.diff(d, s)
        - 2 * d * w
    ),
}
for degree, expected in expected43.items():
    assert sp.simplify(C43.coeff_monomial(y**degree) - expected) == 0


# The first support pair left by the proved filters is (4,5).
survivors = []
for m0 in range(1, 13):
    for n0 in range(1, 13):
        if not (v2(m0) > v2(n0)):
            continue
        if n0 == 1 or m0 == 2 or (m0, n0) in {(4, 2), (4, 3)}:
            continue
        survivors.append((m0, n0))
assert min(survivors, key=lambda pair: (pair[0], pair[1])) == (4, 5)


# Check the forced (4,5) leading powers.
k = sp.symbols("k", integer=True, nonnegative=True)
assert sp.simplify(5 * (2 + 4 * k) - 4 * (2 + 5 * k) - 2) == 0

print("nodal parity Keller thickening checks passed")
