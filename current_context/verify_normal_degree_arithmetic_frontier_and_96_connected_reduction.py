#!/usr/bin/env python3
"""Exact checks for the corrected (9,6) arithmetic and connected reduction."""

from __future__ import annotations

import math

import sympy as sp


# ---------------------------------------------------------------------------
# All arithmetic reductions through m = 9.


def partial_simple(value: int) -> bool:
    return value in (1, 4) or bool(sp.isprime(value))


unresolved: list[tuple[int, int, int, int, int, int, int, int]] = []
for m0 in range(2, 10):
    for n0 in range(1, m0):
        common = math.gcd(m0, n0)
        a0, b0 = m0 // common, n0 // common
        for t0 in sp.divisors(common):
            # b=1 is removed by F -> F - const*G**a.
            if b0 == 1:
                continue
            # A high shear has total-degree gcd t*p.
            if t0 in (1, 2):
                continue
            # One total degree is p, 4p, or a product of two primes.
            if partial_simple(a0 * t0) or partial_simple(b0 * t0):
                continue
            unresolved.append(
                (m0, n0, common, a0, b0, t0, a0 * t0, b0 * t0)
            )

assert unresolved == [(9, 6, 3, 3, 2, 3, 9, 6)]

# Check the exact high-shear factorization for representative s in every
# t-chart at the first survivor.
for s0 in range(0, 31):
    d0 = 3
    t0 = math.gcd(d0, s0)
    if s0 == 0:
        assert t0 == d0
    for L0 in (101, 103):
        p0 = s0 // t0 + (d0 // t0) * L0
        deg_f = 3 * s0 + 9 * L0
        deg_g = 2 * s0 + 6 * L0
        assert deg_f == 3 * t0 * p0
        assert deg_g == 2 * t0 * p0
        assert math.gcd(deg_f, deg_g) == t0 * p0


# ---------------------------------------------------------------------------
# Connected-cover approximate roots and explicit normal form.

w, t = sp.symbols("w t")
a, b, c, d, q, j = sp.symbols("a b c d q j")
ap, bp, cp, dp, qp = sp.symbols("ap bp cp dp qp")
variables = (a, b, c, d, q)
derivatives = (ap, bp, cp, dp, qp)
velocity = dict(zip(variables, derivatives))


def deriv(expression: sp.Expr) -> sp.Expr:
    return sp.expand(
        sum(
            sp.diff(expression, variable) * velocity[variable]
            for variable in variables
        )
    )


unit = 1 + a * t**2 + b * t**3 + c * t**4 + d * t**5 + q * t**6


def polynomial_part(power_numerator: int) -> sp.Expr:
    """Polynomial part of g**(power_numerator/6) at w=infinity."""
    series = sp.expand(
        t ** (-power_numerator)
        * sp.series(
            unit ** sp.Rational(power_numerator, 6),
            t,
            0,
            power_numerator + 7,
        ).removeO()
    )
    nonpositive = sum(
        term
        for term in sp.Add.make_args(series)
        if term.as_powers_dict().get(t, 0) <= 0
    )
    return sp.expand(nonpositive.subs(t, 1 / w))


g = w**6 + a * w**4 + b * w**3 + c * w**2 + d * w + q
f = sp.expand(polynomial_part(9) + j * polynomial_part(3))

Lcoef = (
    3 * a**4
    - 24 * a**2 * c
    - 24 * a * b**2
    + 64 * a * j
    + 96 * a * q
    + 96 * b * d
    + 48 * c**2
) / 128
Pcoef = (
    3 * a**3 * b
    - 6 * a**2 * d
    - 12 * a * b * c
    - 2 * b**3
    + 16 * b * j
    + 24 * b * q
    + 24 * c * d
) / 32

expected_f = (
    w**9
    + sp.Rational(3, 2) * a * w**7
    + sp.Rational(3, 2) * b * w**6
    + 3 * (a**2 + 4 * c) * w**5 / 8
    + 3 * (a * b + 2 * d) * w**4 / 4
    + (-a**3 + 12 * a * c + 6 * b**2 + 16 * j + 24 * q) * w**3 / 16
    - 3 * (a**2 * b - 4 * a * d - 4 * b * c) * w**2 / 16
    + Lcoef * w
    + Pcoef
)
assert sp.expand(f - expected_f) == 0

bracket = sp.Poly(
    sp.expand(deriv(f) * sp.diff(g, w) - sp.diff(f, w) * deriv(g)),
    w,
)

# Every upper coefficient vanishes identically.
for power in range(14, 4, -1):
    assert sp.expand(bracket.coeff_monomial(w**power)) == 0


# ---------------------------------------------------------------------------
# Exact first integrals and triangular identities.

I10 = sp.Rational(3, 128) * (
    3 * a**5
    - 24 * a**3 * c
    - 36 * a**2 * b**2
    + 32 * a**2 * j
    + 48 * a**2 * q
    + 96 * a * b * d
    + 48 * a * c**2
    + 48 * b**2 * c
    - 128 * c * j
    - 192 * c * q
    - 96 * d**2
)
I11 = sp.Rational(3, 128) * (
    15 * a**4 * b
    - 24 * a**3 * d
    - 72 * a**2 * b * c
    - 24 * a * b**3
    + 64 * a * b * j
    + 96 * a * b * q
    + 96 * a * c * d
    + 48 * b**2 * d
    + 48 * b * c**2
    - 128 * d * j
    - 192 * d * q
)
I12 = -sp.Rational(1, 512) * (
    15 * a**6
    - 132 * a**4 * c
    - 288 * a**3 * b**2
    + 128 * a**3 * j
    + 192 * a**3 * q
    + 672 * a**2 * b * d
    + 336 * a**2 * c**2
    + 768 * a * b**2 * c
    - 512 * a * c * j
    - 768 * a * c * q
    - 384 * a * d**2
    + 72 * b**4
    - 384 * b**2 * j
    - 576 * b**2 * q
    - 1152 * b * c * d
    - 192 * c**3
    + 1536 * j * q
    + 1152 * q**2
)
I13 = -sp.Rational(1, 128) * (
    15 * a**5 * b
    - 21 * a**4 * d
    - 96 * a**3 * b * c
    - 48 * a**2 * b**3
    + 64 * a**2 * b * j
    + 96 * a**2 * b * q
    + 120 * a**2 * c * d
    + 120 * a * b**2 * d
    + 144 * a * b * c**2
    - 64 * a * d * j
    - 96 * a * d * q
    + 48 * b**3 * c
    - 128 * b * c * j
    - 192 * b * c * q
    - 96 * b * d**2
    - 144 * c**2 * d
)

R4 = bracket.coeff_monomial(w**4)
R3 = bracket.coeff_monomial(w**3)
R2 = bracket.coeff_monomial(w**2)
R1 = bracket.coeff_monomial(w)
R0 = bracket.coeff_monomial(1)

assert sp.expand(R4 - deriv(I10)) == 0
assert sp.expand(R3 - deriv(I11)) == 0
assert sp.expand(R2 - deriv(I12) - a * R4 / 2) == 0
assert sp.expand(R1 - deriv(I13) - b * R4 / 3 - a * R3 / 3) == 0
assert sp.expand(R0 - d * deriv(Pcoef) + Lcoef * qp) == 0


# Weighted homogeneity and mu_3 characters.
weight_map = {a: 2, b: 3, c: 4, d: 5, q: 6, j: 6}


def weights(expression: sp.Expr) -> set[int]:
    result: set[int] = set()
    for exponents, _ in sp.Poly(expression, *weight_map).terms():
        result.add(
            sum(
                weight * exponent
                for weight, exponent in zip(weight_map.values(), exponents)
            )
        )
    return result


for expression, expected_weight in (
    (I10, 10),
    (I11, 11),
    (I12, 12),
    (I13, 13),
):
    assert weights(expression) == {expected_weight}

assert 10 % 3 == 1
assert 11 % 3 == 2
assert 12 % 3 == 0
assert 13 % 3 == 1


# ---------------------------------------------------------------------------
# Centered variables and complete connected-chart decomposition.

C0, D0, Q0, K = sp.symbols("C0 D0 Q0 K")
centered_substitution = {
    c: C0 + a**2 / 4,
    d: D0 + a * b / 2,
    q: Q0 + b**2 / 4,
}
centered_I10 = sp.Rational(3, 8) * (
    3 * C0**2 * a - 12 * C0 * Q0 - 8 * C0 * j - 6 * D0**2
)
centered_I11 = sp.Rational(3, 8) * (
    3 * C0**2 * b
    + 6 * C0 * D0 * a
    - 12 * D0 * Q0
    - 8 * D0 * j
)
centered_I12 = sp.Rational(1, 8) * (
    3 * C0**3
    - 3 * C0**2 * a**2
    + 18 * C0 * D0 * b
    + 12 * C0 * Q0 * a
    + 8 * C0 * a * j
    + 6 * D0**2 * a
    - 18 * Q0**2
    - 24 * Q0 * j
)
centered_I13 = sp.Rational(1, 16) * (
    18 * C0**2 * D0
    - 9 * C0**2 * a * b
    - 6 * C0 * D0 * a**2
    + 24 * C0 * Q0 * b
    + 16 * C0 * b * j
    + 12 * D0**2 * b
    + 12 * D0 * Q0 * a
    + 8 * D0 * a * j
)

for original, centered in (
    (I10, centered_I10),
    (I11, centered_I11),
    (I12, centered_I12),
    (I13, centered_I13),
):
    assert sp.expand(original.subs(centered_substitution) - centered) == 0

assert sp.expand(
    centered_I13
    - sp.Rational(9, 8) * C0**2 * D0
    + b * centered_I10 / 3
    + a * centered_I11 / 6
) == 0

# C0=0 gives the common (3,2) approximate root and zero bracket.
rho = w**3 + a * w / 2 + b / 2
Qconst = sp.symbols("Qconst")
Czero_substitution = {
    c: a**2 / 4,
    d: a * b / 2,
    q: b**2 / 4 + Qconst,
}
assert sp.expand(g.subs(Czero_substitution) - (rho**2 + Qconst)) == 0
assert sp.expand(
    f.subs(Czero_substitution)
    - (rho**3 + (sp.Rational(3, 2) * Qconst + j) * rho)
) == 0

# D0=0, C0!=0 branch: exact rational parametrization and terminal coefficient.
a_branch = 4 * (3 * Q0 + 2 * j) / (3 * C0)
Rpoly = 6 * Q0**2 + 8 * j * Q0 + sp.Rational(8, 3) * K
Spoly = 21 * Rpoly + 32 * (j**2 - K)
branch_substitution = {
    a: a_branch,
    b: 0,
    c: C0 + a_branch**2 / 4,
    d: 0,
    q: Q0,
}
assert sp.expand(
    centered_I12.subs({a: a_branch, b: 0, D0: 0})
    - K
    + (-3 * C0**3 + 8 * K + 18 * Q0**2 + 24 * Q0 * j) / 8
) == 0
assert sp.factor(
    Lcoef.subs(branch_substitution)
    - (21 * C0**3 + 32 * (j**2 - K)) / (24 * C0)
    - (-3 * C0**3 + 8 * K + 18 * Q0**2 + 24 * Q0 * j)
    / (6 * C0)
) == 0

# S has two distinct roots exactly away from the cusp level, and a common
# R,S root is possible exactly at that level.
Qvar = sp.symbols("Qvar")
R_in_Q = Rpoly.subs(Q0, Qvar)
S_in_Q = Spoly.subs(Q0, Qvar)
assert sp.expand(
    sp.discriminant(S_in_Q, Qvar) - 12096 * (j**2 - K)
) == 0
assert sp.expand(
    sp.resultant(R_in_Q, S_in_Q, Qvar) - 36864 * (j**2 - K) ** 2
) == 0

# Exceptional cusp parametrization.
v = sp.symbols("v")
cusp_substitution = {
    a: 4 * v,
    b: 0,
    c: 10 * v**2,
    d: 0,
    q: 6 * v**3 - sp.Rational(2, 3) * j,
}
f_cusp = sp.expand(f.subs(cusp_substitution))
g_cusp = sp.expand(g.subs(cusp_substitution))
expected_f_cusp = (
    w**9
    + 6 * v * w**7
    + 21 * v**2 * w**5
    + 35 * v**3 * w**3
    + sp.Rational(63, 2) * v**4 * w
)
expected_g_cusp = (
    w**6
    + 4 * v * w**4
    + 10 * v**2 * w**2
    + 6 * v**3
    - sp.Rational(2, 3) * j
)
assert sp.expand(f_cusp - expected_f_cusp) == 0
assert sp.expand(g_cusp - expected_g_cusp) == 0
assert sp.expand(
    sp.diff(f_cusp, v) * sp.diff(g_cusp, w)
    - sp.diff(f_cusp, w) * sp.diff(g_cusp, v)
    + 567 * v**6
) == 0

T = sp.symbols("T")
cusp_g_quotient = T**3 + 4 * T**2 + 10 * T + 6
cusp_f_quotient = (
    T**4 + 6 * T**3 + 21 * T**2 + 35 * T + sp.Rational(63, 2)
)
assert sp.resultant(cusp_g_quotient, cusp_f_quotient, T) == sp.Rational(
    567, 8
)

# Local valuation equation in the cusp chart.  Symbolically,
# 7r+s-1=3s and s<=3r imply 7r-1=2s<=6r, hence r<=1.
# Positivity gives r=1, and substitution gives s=3, the excluded tied case.
r_sym, s_sym = sp.symbols("r_sym s_sym", integer=True, positive=True)
assert sp.expand(2 * (3 * r_sym) - (7 * r_sym - 1)) == 1 - r_sym
assert (7 * 1 - 1) // 2 == 3


# ---------------------------------------------------------------------------
# General cube-h upper chart: all character constants survive.

kappa8, kappa7, kappa5, kappa4, kappa3, kappa2, kappa1 = sp.symbols(
    "kappa8 kappa7 kappa5 kappa4 kappa3 kappa2 kappa1"
)
f_cube = sp.expand(
    polynomial_part(9)
    + kappa8 * polynomial_part(8)
    + kappa7 * polynomial_part(7)
    + kappa5 * polynomial_part(5)
    + kappa4 * polynomial_part(4)
    + kappa3 * polynomial_part(3)
    + kappa2 * polynomial_part(2)
    + kappa1 * polynomial_part(1)
)
bracket_cube = sp.Poly(
    sp.expand(
        deriv(f_cube) * sp.diff(g, w) - sp.diff(f_cube, w) * deriv(g)
    ),
    w,
)
for power in range(14, 4, -1):
    assert sp.expand(bracket_cube.coeff_monomial(w**power)) == 0
assert sp.Poly(f_cube, w).coeff_monomial(w**8) == kappa8

x, y, z = sp.symbols("x y z")
F_cube_example = (x * y) ** 9 + (x * y) ** 8
G_cube_example = (x * y) ** 6
assert sp.expand(F_cube_example.subs(y, z / x)) == z**9 + z**8
assert sp.expand(G_cube_example.subs(y, z / x)) == z**6


# ---------------------------------------------------------------------------
# Exact a != 0 weighted-infinity chart.

leading = [
    sp.together(expression.subs({a: 1, j: 0}))
    for expression in (I10, I11, I12, I13)
]
groebner = sp.groebner(leading, q, d, c, b, order="lex")


def reduces_to_zero(expression: sp.Expr) -> bool:
    return sp.expand(groebner.reduce(expression)[1]) == 0


assert reduces_to_zero((4 * c - 1) ** 4 * (8 * c - 5))
assert reduces_to_zero(b * (4 * c - 1) ** 4)
assert reduces_to_zero((b - 2 * d) * (4 * c - 1) ** 2)

# Resonant curve and isolated point.
resonant_substitution = {c: sp.Rational(1, 4), b: 2 * d, q: d**2}
isolated_substitution = {
    b: 0,
    c: sp.Rational(5, 8),
    d: 0,
    q: sp.Rational(3, 32),
}
for expression in leading:
    assert sp.expand(expression.subs(resonant_substitution)) == 0
    assert sp.expand(expression.subs(isolated_substitution)) == 0
assert sp.factor(
    leading[0].subs(c, sp.Rational(1, 4))
) == -sp.Rational(9, 16) * (b - 2 * d) ** 2
assert sp.factor(
    leading[2].subs({c: sp.Rational(1, 4), b: 2 * d})
) == -sp.Rational(9, 4) * (q - d**2) ** 2
assert sp.expand(
    leading[0].subs({c: sp.Rational(5, 8), b: 0, d: 0})
    + sp.Rational(27, 512) * (32 * q - 3)
) == 0

S = w**3 + w / 2 + d
g_resonant = sp.expand(g.subs({a: 1, j: 0, **resonant_substitution}))
f_resonant = sp.expand(f.subs({a: 1, j: 0, **resonant_substitution}))
assert sp.expand(g_resonant - S**2) == 0
assert sp.expand(f_resonant - S**3) == 0
assert sp.expand(
    Pcoef.subs({a: 1, j: 0, **resonant_substitution}) - d**3
) == 0
assert sp.expand(
    Lcoef.subs({a: 1, j: 0, **resonant_substitution})
    - sp.Rational(3, 2) * d**2
) == 0

print("verified: all arithmetic criteria leave first only (9,6), d=t=3")
print("verified: connected upper equations give the (3/2,1/2) approximate root")
print("verified: the four first integrals have weights 10,11,12,13")
print("verified: exact triangular identities and terminal d*P' - L*q'")
print("verified: centered split, two-value obstruction, and cuspidal valuation data")
print("verified: cube-h chart retains seven character constants")
print("verified: a!=0 infinity chart is resonant curve plus isolated point")
print("scope: fixed-field, hsop-finiteness, and normality steps are proved in the note")
