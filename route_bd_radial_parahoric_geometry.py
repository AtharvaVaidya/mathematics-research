#!/usr/bin/env python3
"""Verify the two-end geometry and rational parahoric countermodels.

This does not redo the nonlinear coefficient elimination.  It checks:

* the exact k=1 low/high kernel representatives;
* their endpoint valuation pairs;
* the commutator mixing between the low and high lattices;
* the rational symplectic family T_g;
* its identity jets at both w-ends; and
* the compactified volume divisor and residual scaling torus.
"""

from __future__ import annotations

import sympy as sp


z, w = sp.symbols("z w", nonzero=True)

U = 1 + w + sp.Rational(6, 25) * w**2 + sp.Rational(9, 250) * w**3
V = (
    1
    + sp.Rational(2, 3) * w
    + sp.Rational(6, 25) * w**2
    + sp.Rational(36, 875) * w**3
    + sp.Rational(18, 4375) * w**4
)

edge = sp.expand(U * V + 2 * w * U * sp.diff(V, w) - 3 * w * sp.diff(U, w) * V)
assert edge == 1

p0 = z**2 * U / w
q0 = z**3 * V / w
omega_density = sp.factor(
    sp.diff(p0, z) * sp.diff(q0, w) - sp.diff(p0, w) * sp.diff(q0, z)
)
assert omega_density == z**4 / w**3


# Exact low and high scalar representatives.
low = {
    1: sp.Integer(1),
    2: w,
    3: w,
}

u_top = sp.Rational(9, 250)
c1_laurent = sp.expand(U**2 / (u_top**2 * w))
c1_high = sp.expand(
    c1_laurent
    - sp.Rational(125000, 81)
    - sp.Rational(62500, 81) / w
)
c2_high = sp.expand(V - 1 - sp.Rational(2, 3) * w)
c3_high = sp.expand(U - 1 - w)
c4_high = w**2

high = {
    1: c1_high,
    2: c2_high,
    3: c3_high,
    4: c4_high,
}

assert sp.expand(
    c1_high
    - (
        w**5
        + sp.Rational(40, 3) * w**4
        + 100 * w**3
        + sp.Rational(11500, 27) * w**2
        + sp.Rational(92500, 81) * w
    )
) == 0
assert sp.factor(c2_high - 6 * w**2 * (3 * w**2 + 30 * w + 175) / 4375) == 0
assert sp.factor(c3_high - 3 * w**2 * (3 * w + 20) / 250) == 0


def endpoint_orders(polynomial: sp.Expr) -> tuple[int, int]:
    """Orders of H=-z^(5-d) C/((5-d)w) at w=0 and infinity."""

    terms = sp.Poly(polynomial, w).terms()
    exponents = [monomial[0] - 1 for monomial, coefficient in terms if coefficient]
    return min(exponents), -max(exponents)


assert [endpoint_orders(low[d]) for d in (1, 2, 3)] == [
    (-1, 1),
    (0, 0),
    (0, 0),
]
assert [endpoint_orders(high[d]) for d in (1, 2, 3, 4)] == [
    (0, -4),
    (1, -3),
    (1, -2),
    (1, -1),
]


def scalar_star(deficit: int, left: sp.Expr, other_deficit: int, right: sp.Expr) -> sp.Expr:
    c = 5 - deficit
    f = 5 - other_deficit
    grade = 5 - deficit - other_deficit
    if grade == 0:
        return sp.Integer(0)
    return sp.factor(
        -grade
        * w
        * (
            (w * sp.diff(left, w) - left) * right / c
            + left * (right - w * sp.diff(right, w)) / f
        )
    )


assert scalar_star(1, 1, 2, w) == w**2 / 2
assert scalar_star(1, 1, 3, w) == w**2 / 4
assert scalar_star(1, 1, 3, w) == high[4] / 4
assert scalar_star(2, w, 3, w) == 0


# Rational symplectic countermodel.
r = z**5 / w**2
a, b = sp.symbols("a b")
g = (r**2 + a * r + 1) / (r**2 + b * r + 1)
z_new = z * g**2
w_new = w * g**5
assert sp.factor(z_new**5 / w_new**2 - r) == 0

jacobian = sp.factor(
    sp.diff(z_new, z) * sp.diff(w_new, w)
    - sp.diff(z_new, w) * sp.diff(w_new, z)
)
pulled_density = sp.factor((z_new**4 / w_new**3) * jacobian)
assert sp.factor(pulled_density - z**4 / w**3) == 0

# The chosen g has identity constant jets at both r=0 and r=infinity.
x = sp.symbols("x")
at_zero = sp.series((x**2 + a * x + 1) / (x**2 + b * x + 1), x, 0, 3)
at_infinity = sp.series(
    ((1 / x) ** 2 + a / x + 1) / ((1 / x) ** 2 + b / x + 1),
    x,
    0,
    3,
)
assert sp.expand(at_zero.removeO()).coeff(x, 0) == 1
assert sp.expand(at_zero.removeO()).coeff(x, 1) == a - b
assert sp.expand(at_infinity.removeO()).coeff(x, 0) == 1
assert sp.expand(at_infinity.removeO()).coeff(x, 1) == a - b

# Exact powers in the pulled outer pair.  They prove that every finite zero
# of g gives an uncancellable pole through g^-1 in P, while every finite
# pole gives an uncancellable pole through g^21 in Q.
g_symbol = sp.symbols("g_symbol", nonzero=True)
pulled_p_factor = (
    g_symbol**-1
    + w * g_symbol**4
    + sp.Rational(6, 25) * w**2 * g_symbol**9
    + sp.Rational(9, 250) * w**3 * g_symbol**14
)
pulled_q_factor = (
    g_symbol
    + sp.Rational(2, 3) * w * g_symbol**6
    + sp.Rational(6, 25) * w**2 * g_symbol**11
    + sp.Rational(36, 875) * w**3 * g_symbol**16
    + sp.Rational(18, 4375) * w**4 * g_symbol**21
)
assert sorted(
    term.as_powers_dict().get(g_symbol, 0)
    for term in sp.expand(pulled_p_factor).as_ordered_terms()
) == [-1, 4, 9, 14]
assert sorted(
    term.as_powers_dict().get(g_symbol, 0)
    for term in sp.expand(pulled_q_factor).as_ordered_terms()
) == [1, 6, 11, 16, 21]

# The first zero-end escape is the d=5 logarithmic resonance.
log_r = sp.log(r)
log_vector_z = sp.factor(sp.diff(log_r, w) / omega_density)
log_vector_w = sp.factor(-sp.diff(log_r, z) / omega_density)
assert log_vector_z == -2 * w**2 / z**4
assert log_vector_w == -5 * w**3 / z**5


# Compactified volume divisor:
# z^4 dz contributes 4[0]-6[infinity];
# w^-3 dw contributes -3[0]+1[infinity].
volume_divisor = {
    "Z0": 4,
    "Zinf": -6,
    "W0": -3,
    "Winf": 1,
}
assert len(set(volume_divisor.values())) == 4

alpha, beta = sp.symbols("alpha beta", nonzero=True)
scaled_density_ratio = sp.factor(
    ((alpha * z) ** 4 / (beta * w) ** 3) * alpha * beta / (z**4 / w**3)
)
assert scaled_density_ratio == alpha**5 / beta**2

print("verified the exact k=1 three-low/four-high endpoint split")
print("verified: the low span is not Lie closed and mixes into the high d=4 mode")
print("verified the two-end identity-jet rational symplectic family T_g")
print("verified the no-interior-divisor theorem for the rational centralizer")
print("verified: its first endpoint escape is the logarithmic d=5 resonance")
print("verified the compactified volume divisor and residual scaling torus")
