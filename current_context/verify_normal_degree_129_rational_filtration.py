#!/usr/bin/env python3
"""Exact checks for the rational-filtration closure in degree (12,9)."""

import sympy as sp


X, N, gamma = sp.symbols("X N gamma")
A, B, z0, z1 = sp.symbols("A B z0 z1")
P_general = X**3 + A * X + B


def D(order, value, polynomial=P_general):
    """Universal normalized scalar operator at bracket order ``order``."""
    return sp.expand(
        -2 * polynomial * sp.diff(value, X)
        + sp.Rational(2, 3) * (18 - order) * sp.diff(polynomial, X) * value
    )


# A nonzero scalar in 33/2 < N < 20 can only come from a linear Z.
# Its X^3 coefficient forces N=17; its X^2 coefficient forces z0=0;
# and its X coefficient forces A=0.  The surviving scalar is -2*B*z1.
Z_linear = z0 + z1 * X
D_linear_17 = sp.Poly(D(17, Z_linear), X)
assert D_linear_17.coeff_monomial(X**3) == 0
assert D_linear_17.coeff_monomial(X**2) == 2 * z0
assert D_linear_17.coeff_monomial(X) == -sp.Rational(4, 3) * A * z1
assert D_linear_17.coeff_monomial(1) == (
    sp.Rational(2, 3) * A * z0 - 2 * B * z1
)
assert sp.expand(D(17, z1 * X).subs(A, 0)) == -2 * B * z1

# For a degree-q leading term, the leading coefficient is a nonzero
# multiple of 18-N-q.  In the open dangerous interval this leaves only
# (q,N)=(1,17) or (0,18).  The latter is a zero operator on constants.
q = sp.symbols("q", integer=True, nonnegative=True)
leading_factor = sp.factor(-2 * q + 2 * (18 - N))
assert sp.solve(leading_factor, N) == [18 - q]
assert D(18, z0) == 0

# The two first-interaction kernel equations integrate to the claimed
# cubic powers.  These identities avoid treating a rational exponent
# as a formal polynomial: they are logarithmic-derivative identities.
Q = sp.Function("Q")(X)
R = sp.Function("R")(X)
order_interaction = gamma + sp.Rational(17, 2)
lower_kernel = sp.factor(D(order_interaction, P_general * Q) / P_general)
later_kernel = sp.factor(D(order_interaction, R))
expected_lower = (
    -2 * P_general * sp.diff(Q, X)
    + (13 - 2 * gamma) * sp.diff(P_general, X) * Q / 3
)
expected_later = (
    -2 * P_general * sp.diff(R, X)
    + (19 - 2 * gamma) * sp.diff(P_general, X) * R / 3
)
assert sp.simplify(lower_kernel - expected_lower) == 0
assert sp.simplify(later_kernel - expected_later) == 0

# If either kernel vanishes, these are the derivatives of
# Q^3/P^(13/2-gamma) and R^3/P^(19/2-gamma), up to nonzero factors.
lower_log_derivative = sp.factor(
    3 * P_general * sp.diff(Q, X)
    - (sp.Rational(13, 2) - gamma) * sp.diff(P_general, X) * Q
)
later_log_derivative = sp.factor(
    3 * P_general * sp.diff(R, X)
    - (sp.Rational(19, 2) - gamma) * sp.diff(P_general, X) * R
)
assert sp.simplify(lower_log_derivative + sp.Rational(3, 2) * lower_kernel) == 0
assert sp.simplify(later_log_derivative + sp.Rational(3, 2) * later_kernel) == 0


# Verify directly that the only later half-lattice kernel, the silent
# order-19 direction, dies at bracket order 53 after all forced
# descendants and an arbitrary six-coefficient order-36 jet are retained.
t = sp.symbols("t")
a, c, k = sp.symbols("a c k")
P = X**3 - 1
S17 = -sp.Rational(1, 2) * X**2 * (X**3 - 3)
V34 = X * (9 * X**3 - 11) / 144
u = sp.symbols("u0:6")
U36 = sum(u[i] * X**i for i in range(6))

delta = {
    12: c * P,
    17: S17,
    18: -sp.Rational(3, 4) * k,
    19: a * X * (X**3 - 3),
    21: a**2 * (X**3 - 3),
    23: 2 * X**2 * a**3 * (3 * X**3 - 5),
    25: 5 * X * a**4 * (3 * X**3 - 5),
    27: 14 * a**5 * (3 * X**3 - 5),
    29: X**2
    * (
        10080 * X**3 * a**6
        + 5 * X**3 * c
        - 14112 * a**6
        - 11 * c
    )
    / 48,
    31: X
    * a
    * (
        15840 * X**3 * a**6
        - 5 * X**3 * c
        - 22176 * a**6
        + 11 * c
    )
    / 24,
    33: a**2
    * (
        51480 * X**3 * a**6
        - 5 * X**3 * c
        - 72072 * a**6
        + 11 * c
    )
    / 24,
    34: V34,
    35: 5
    * X**2
    * a**3
    * (
        24024 * X**3 * a**6
        - 7 * X**3 * c
        - 30888 * a**6
        + 13 * c
    )
    / 12,
    36: U36,
}


def convolution(source, power, order):
    """Coefficient of t^order in a sparse power of ``source``."""
    if power == 0:
        return sp.Integer(1) if order == 0 else sp.Integer(0)
    result = {}
    for source_order, value in source.items():
        result[source_order] = value
    for _ in range(1, power):
        new_result = {}
        for left_order, left_value in result.items():
            for right_order, right_value in source.items():
                total_order = left_order + right_order
                if total_order <= 53:
                    new_result[total_order] = (
                        new_result.get(total_order, 0)
                        + left_value * right_value
                    )
        result = new_result
    return sp.expand(result.get(order, 0))


def polynomial_quotient(numerator, denominator):
    return sp.div(sp.expand(numerator), denominator, X)[0]


def root_part_coefficient(order, exponent):
    """Polynomial part of (P^3+delta)^exponent at a fixed t-order."""
    base_power = 3 * exponent
    assert base_power in (1, 2, 4)
    value = P**base_power if order == 0 else sp.Integer(0)
    # The displayed forced jet begins at order 12, so q<=4 suffices
    # for every coefficient through bracket order 53.
    for power in range(1, 5):
        numerator = convolution(delta, power, order)
        if numerator == 0:
            continue
        denominator_power = 3 * power - base_power
        if denominator_power <= 0:
            term = numerator * P ** (-denominator_power)
        else:
            term = polynomial_quotient(numerator, P**denominator_power)
        value += sp.binomial(exponent, power) * term
    return sp.expand(value)


def f_coefficient(order):
    value = root_part_coefficient(order, sp.Rational(4, 3))
    if order >= 12:
        value -= (
            sp.Rational(2, 3)
            * c
            * root_part_coefficient(order - 12, sp.Rational(2, 3))
        )
    if order >= 18:
        value += k * root_part_coefficient(
            order - 18, sp.Rational(1, 3)
        )
    return sp.expand(value)


def g_coefficient(order):
    return P**3 if order == 0 else delta.get(order, 0)


def bracket_coefficient(order):
    value = 0
    for left_order in range(order + 1):
        f_value = f_coefficient(left_order)
        g_value = g_coefficient(order - left_order)
        if f_value == 0 or g_value == 0:
            continue
        right_order = order - left_order
        value += (
            (left_order - 24) * f_value * sp.diff(g_value, X)
            + (18 - right_order) * sp.diff(f_value, X) * g_value
        )
    return sp.expand(value)


order_53 = sp.Poly(bracket_coefficient(53), X)
equations_53 = order_53.all_coeffs()
solutions_53 = sp.solve(equations_53, [*u, a], dict=True, simplify=False)
assert solutions_53 == [
    {
        u[0]: 0,
        u[1]: 0,
        u[2]: 0,
        u[3]: 0,
        u[4]: 0,
        u[5]: 0,
        a: 0,
    }
]


print("verified the all-rational filtration and order-53 silent-tail death")
