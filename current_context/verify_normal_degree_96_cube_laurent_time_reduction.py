#!/usr/bin/env python3
"""Exact checks for the full cube-chart Laurent-time reduction."""

from __future__ import annotations

import sympy as sp


w, t = sp.symbols("w t")
x, pole, alpha, beta, lam = sp.symbols(
    "x pole alpha beta lam", nonzero=True
)
a, b, c, d, q = sp.symbols("a b c d q")
ap, bp, cp, dp, qp = sp.symbols("ap bp cp dp qp")
kappa8, kappa7, kappa5, kappa4, j, kappa2, kappa1 = sp.symbols(
    "kappa8 kappa7 kappa5 kappa4 j kappa2 kappa1"
)

variables = (a, b, c, d, q)
velocities = (ap, bp, cp, dp, qp)
velocity = dict(zip(variables, velocities))
parameters = {
    9: sp.Integer(1),
    8: kappa8,
    7: kappa7,
    5: kappa5,
    4: kappa4,
    3: j,
    2: kappa2,
    1: kappa1,
}


def derivative(expression: sp.Expr) -> sp.Expr:
    """Differentiate in x, treating the seven upper constants as constant."""
    return sp.expand(
        sum(
            sp.diff(expression, variable) * velocity[variable]
            for variable in variables
        )
    )


unit = 1 + a * t**2 + b * t**3 + c * t**4 + d * t**5 + q * t**6


def phi_series(last_power: int) -> sp.Expr:
    """Expand Phi(g^(1/6)) through t**last_power, where t=1/w."""
    output = 0
    for exponent, coefficient in parameters.items():
        output += coefficient * t ** (-exponent) * sp.series(
            unit ** sp.Rational(exponent, 6),
            t,
            0,
            exponent + last_power + 1,
        ).removeO()
    return sp.expand(output)


phi_through_five = phi_series(5)
f_in_t = sp.expand(
    sum(
        term
        for term in sp.Add.make_args(phi_through_five)
        if term.as_powers_dict().get(t, 0) <= 0
    )
)
f = sp.expand(f_in_t.subs(t, 1 / w))
g = w**6 + a * w**4 + b * w**3 + c * w**2 + d * w + q

# The approximate-root construction kills every bracket coefficient
# above w**4 for all seven constants.
bracket = sp.Poly(
    sp.expand(
        derivative(f) * sp.diff(g, w)
        - sp.diff(f, w) * derivative(g)
    ),
    w,
)
for power in range(14, 4, -1):
    assert sp.expand(bracket.coeff_monomial(w**power)) == 0


def coefficient_t(expression: sp.Expr, power: int) -> sp.Expr:
    """Extract one Laurent coefficient in t."""
    return sp.expand(expression).coeff(t, power)


# Residue formula (13).  Only the negative tail through t**5 is needed
# for A_1,...,A_5.
negative_tail = sp.expand(f_in_t - phi_through_five)
s_w = sp.series(
    unit ** sp.Rational(1, 6)
    - t
    * sp.diff(unit, t)
    * unit ** sp.Rational(-5, 6)
    / 6,
    t,
    0,
    8,
).removeO()

A: dict[int, sp.Expr] = {}
for ell_index in range(1, 6):
    residue_integrand = sp.series(
        t ** (-(ell_index - 1))
        * unit ** sp.Rational(ell_index - 1, 6)
        * negative_tail
        * s_w,
        t,
        0,
        2,
    ).removeO()
    A[ell_index] = sp.factor(coefficient_t(residue_integrand, 1))


# Expand g_w*s^(-ell) and check the exact Laurent-coordinate chain
# rule for every nonnegative bracket coefficient.  Terms ell>5 start
# in negative w-degree and cannot contribute.
chain_matrix: dict[tuple[int, int], sp.Expr] = {}
g_w = sp.diff(g, w)
for power in range(5):
    for ell_index in range(1, 6):
        series_in_t = sp.series(
            g_w.subs(w, 1 / t)
            * t**ell_index
            * unit ** sp.Rational(-ell_index, 6),
            t,
            0,
            1,
        ).removeO()
        chain_matrix[(power, ell_index)] = coefficient_t(
            series_in_t, -power
        )

for power in range(5):
    reconstructed = sum(
        chain_matrix[(power, ell_index)] * derivative(A[ell_index])
        for ell_index in range(1, 6)
    )
    assert sp.expand(
        bracket.coeff_monomial(w**power) - reconstructed
    ) == 0

# The triangular diagonal is 6.  Once A_1',...,A_4' vanish, the
# constant bracket coefficient is exactly 6*A_5'.
assert chain_matrix[(4, 1)] == 6
assert chain_matrix[(3, 2)] == 6
assert chain_matrix[(2, 3)] == 6
assert chain_matrix[(1, 4)] == 6
assert chain_matrix[(0, 5)] == 6
for power, first_new_index in ((4, 1), (3, 2), (2, 3), (1, 4)):
    assert all(
        chain_matrix[(power, ell_index)] == 0
        for ell_index in range(first_new_index + 1, 6)
    )

# The familiar connected-slice triangular corrections appear exactly.
assert chain_matrix[(2, 1)] == 3 * a
assert chain_matrix[(1, 1)] == 2 * b
assert chain_matrix[(1, 2)] == 2 * a


# Direct checks of the two possibilities in the rational-time
# classification.  Riemann--Hurwitz supplies the exhaustiveness.
constant_r = sp.symbols("constant_r", nonzero=True)
linear_time = lam * x / constant_r + alpha
assert sp.diff(linear_time, x) == lam / constant_r

k = sp.symbols("k", integer=True, positive=True)
pure_pole_time = alpha + beta / (x - pole) ** k
pure_power_r = -lam * (x - pole) ** (k + 1) / (k * beta)
assert sp.simplify(sp.diff(pure_pole_time, x) - lam / pure_power_r) == 0

# The residual family is genuine at the terminal-equation level.
assert sp.diff(-lam / x, x) == lam / x**2

print("verified: full seven-constant upper approximate-root bracket")
print("verified: residue construction of A_1,...,A_5")
print("verified: exact Laurent chain-rule reconstruction of R_4,...,R_0")
print("verified: four conserved Laurent coefficients and terminal 6*A_5'")
print("verified: constant and pure-power rational-time normal forms")
