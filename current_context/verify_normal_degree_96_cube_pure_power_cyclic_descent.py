#!/usr/bin/env python3
"""Exact checks for the pure-power cyclic-descent note."""

from __future__ import annotations

import sympy as sp


u, v, z, w = sp.symbols("u v z w")
m, n = sp.symbols("m n", integer=True, positive=True)
lam, gamma, alpha, beta = sp.symbols(
    "lam gamma alpha beta", nonzero=True
)

# The differential normalization after u -> v=u^m and z=v^(-1).
quotient_bracket = lam / (m * gamma * v ** (n + 1))
assert sp.simplify(
    m * u ** (m - 1) * quotient_bracket.subs(v, u**m)
    - lam / (gamma * u ** (m * n + 1))
) == 0
assert sp.simplify(
    -z ** (-2) * quotient_bracket.subs(v, z ** (-1))
    + lam * z ** (n - 1) / (m * gamma)
) == 0

time = alpha + beta * v ** (-n)
assert sp.simplify(
    sp.diff(time, v) + n * beta / v ** (n + 1)
) == 0

# The primitive common-critical model which shows that the gcd
# hypothesis in the ramification lemma is necessary.
P = (
    w**9
    + 6 * z * w**7
    + 21 * z**2 * w**5
    + 35 * z**3 * w**3
    + sp.Rational(63, 2) * z**4 * w
)
Q = w**6 + 4 * z * w**4 + 10 * z**2 * w**2 + 6 * z**3

bracket = sp.expand(
    sp.diff(P, z) * sp.diff(Q, w)
    - sp.diff(P, w) * sp.diff(Q, z)
)
assert bracket == -567 * z**6
assert sp.gcd(
    sp.Poly(sp.diff(P, w).subs(z, 0), w),
    sp.Poly(sp.diff(Q, w).subs(z, 0), w),
).as_expr() == 3 * w**5

# The finite-map certificate for the cusp.  Away from the axes, a
# common nonzero zero would give a common root of these two polynomials.
X = sp.symbols("X")
q_reduced = X**3 + 4 * X**2 + 10 * X + 6
p_reduced = (
    X**4
    + 6 * X**3
    + 21 * X**2
    + 35 * X
    + sp.Rational(63, 2)
)
assert sp.resultant(q_reduced, p_reduced, X) == sp.Rational(567, 8)

# Exact two-ended only-j curve which disproves a one-place inequality.
t, Z, j, epsilon = sp.symbols("t Z j epsilon", nonzero=True)
C = t**2
D = sp.Rational(8, 9) * Z / t**4
Q_centered = (
    -sp.Rational(128, 81) * Z**2 / t**10
    - sp.Rational(2, 3) * j
    + epsilon * t**3
)
a = 4 * (-32 * Z**2 + 27 * epsilon * t**13) / (27 * t**12)
b = (
    -32
    * Z
    * (-64 * Z**2 + 81 * epsilon * t**13)
    / (729 * t**18)
)

I10 = sp.Rational(3, 8) * (
    3 * C**2 * a
    - 12 * C * Q_centered
    - 8 * C * j
    - 6 * D**2
)
I11 = sp.Rational(3, 8) * (
    3 * C**2 * b
    + 6 * C * D * a
    - 12 * D * Q_centered
    - 8 * D * j
)
I12 = sp.Rational(1, 8) * (
    3 * C**3
    - 3 * C**2 * a**2
    + 18 * C * D * b
    + 12 * C * Q_centered * a
    + 8 * C * a * j
    + 6 * D**2 * a
    - 18 * Q_centered**2
    - 24 * Q_centered * j
)
I13 = (
    sp.Rational(9, 8) * C**2 * D
    - b * I10 / 3
    - a * I11 / 6
)
A5_two_ended = (
    -18 * C**3 * a
    + 36 * C**2 * Q_centered
    + 3 * C**2 * a**3
    - 18 * C**2 * b**2
    + 24 * C**2 * j
    + 72 * C * D**2
    - 36 * C * D * a * b
    - 12 * C * Q_centered * a**2
    - 8 * C * a**2 * j
    - 6 * D**2 * a**2
    + 72 * D * Q_centered * b
    + 48 * D * b * j
) / 576


def reduce_epsilon(expression: sp.Expr) -> sp.Expr:
    """Reduce modulo epsilon**2=1/6."""
    numerator, denominator = sp.together(expression).as_numer_denom()
    remainder = sp.rem(
        sp.Poly(numerator, epsilon),
        sp.Poly(epsilon**2 - sp.Rational(1, 6), epsilon),
    ).as_expr()
    return sp.factor(remainder / denominator)


assert reduce_epsilon(I10) == 0
assert reduce_epsilon(I11) == 0
assert reduce_epsilon(I12 - j**2) == 0
assert reduce_epsilon(I13 - Z) == 0
expected_two_ended = (
    sp.Rational(4, 27) * Z**2 / t**6 - epsilon * t**7 / 16
)
assert reduce_epsilon(A5_two_ended - expected_two_ended) == 0

# The quadratic coefficient curve underlying the two-ended example.
Q_test, C_test, W_test = sp.symbols("Q_test C_test W_test")
u0_z_curve = (
    2187 * C_test**13
    - 13122 * C_test**10 * Q_test**2
    - 17496 * C_test**10 * Q_test * j
    - 5832 * C_test**10 * W_test
    - 41472 * C_test**5 * Q_test * Z**2
    - 27648 * C_test**5 * Z**2 * j
    - 32768 * Z**4
)
assert sp.factor(sp.discriminant(u0_z_curve, Q_test)) == (
    38263752
    * C_test**20
    * (3 * C_test**3 - 8 * W_test + 8 * j**2)
)

# The U=0, V!=0 Newton polygon and its five nonhorizontal outer
# profiles.  Negative pole degrees mean zeros at the place.
x, C0, D0, V_level, W_level = sp.symbols(
    "x C0 D0 V_level W_level", nonzero=True
)
C_var, D_var = sp.symbols("C_var D_var")
u0_v_curve = (
    -6561 * C_var**8 * D_var**2
    + 11664 * C_var**6 * D_var * Z
    + 384 * C_var**5 * V_level**2
    - 11664 * C_var**4 * D_var**3 * V_level
    - 5184 * C_var**4 * Z**2
    + 10368 * C_var**2 * D_var**2 * V_level * Z
    + 1024
    * C_var**2
    * V_level**2
    * (j**2 - W_level)
    + 2048 * C_var * D_var * V_level**3
    - 5184 * D_var**4 * V_level**2
)
u0_v_A5 = -(
    2187 * C_var**8 * D_var
    - 1944 * C_var**6 * Z
    - 5832 * C_var**4 * D_var**2 * V_level
    + 3456 * C_var**2 * D_var * V_level * Z
    + 512 * C_var * V_level**3
    - 1152 * D_var**3 * V_level**2
) / (20736 * C_var**3 * V_level)


def laurent_lead(expression: sp.Expr) -> tuple[int, sp.Expr]:
    """Return the largest x-exponent and its Laurent coefficient."""
    coefficients: dict[int, sp.Expr] = {}
    for term in sp.Add.make_args(sp.expand(expression)):
        exponent = int(term.as_powers_dict().get(x, 0))
        coefficients[exponent] = (
            coefficients.get(exponent, 0) + term / x**exponent
        )
    degree = max(
        exponent
        for exponent, coefficient in coefficients.items()
        if coefficient != 0
    )
    return degree, sp.factor(coefficients[degree])


profile_data = (
    (
        1,
        4,
        9,
        {D0: -sp.Rational(9, 8) * C0**4 / V_level},
        sp.Rational(405, 1024) * C0**9 / V_level**2,
    ),
    (
        -3,
        -1,
        6,
        {C0: sp.Rational(81, 32) * D0**3 / V_level},
        -sp.Rational(2048, 4782969) * V_level**4 / D0**6,
    ),
    (
        -1,
        -1,
        2,
        {
            D0: -C0 * (j**2 - W_level) / (2 * V_level),
        },
        -sp.Rational(2, 81) * V_level**2 / C0**2,
    ),
    (
        -1,
        -4,
        2,
        {
            W_level: j**2,
            D0: -sp.Rational(3, 16) * C0**4 / V_level,
        },
        -sp.Rational(2, 81) * V_level**2 / C0**2,
    ),
    (
        2,
        -3,
        7,
        {
            D0**2: sp.Rational(128, 2187)
            * V_level**2
            / C0**3,
        },
        -sp.Rational(27, 256) * C0**5 * D0 / V_level,
    ),
)

for c_pole, d_pole, a5_pole, edge_relation, expected_lead in (
    profile_data
):
    scaled_curve = u0_v_curve.subs(
        {
            C_var: C0 * x**c_pole,
            D_var: D0 * x**d_pole,
        }
    )
    _, curve_lead = laurent_lead(scaled_curve)
    assert sp.factor(curve_lead.subs(edge_relation)) == 0

    scaled_a5 = sp.cancel(
        u0_v_A5.subs(
            {
                C_var: C0 * x**c_pole,
                D_var: D0 * x**d_pole,
            }
        )
    )
    a5_numerator, a5_denominator = sp.together(
        scaled_a5
    ).as_numer_denom()
    numerator_degree, numerator_lead = laurent_lead(a5_numerator)
    denominator_degree, denominator_lead = laurent_lead(
        a5_denominator
    )
    assert numerator_degree - denominator_degree == a5_pole
    actual_lead = sp.factor(
        (numerator_lead / denominator_lead).subs(edge_relation)
    )
    assert sp.factor(actual_lead - expected_lead) == 0

print("verified: cyclic quotient and inverse-coordinate Jacobian factors")
print("verified: primitive n=7 common-critical cusp")
print("verified: cusp finite-map resultant 567/8")
print("verified: exact two-ended U=V=0, W=j^2, Z!=0 curve")
print("verified: exhaustive U=0, V!=0 Newton-edge terminal orders")
