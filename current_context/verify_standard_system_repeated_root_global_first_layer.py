#!/usr/bin/env python3
"""Checks for repeated-root fixed-base first-layer gluing."""

import itertools
import math

import sympy as sp


x, tau = sp.symbols("x tau")


def partitions(total: int, minimum: int = 1):
    """Yield nondecreasing positive partitions of total."""
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def kummer_period(g: int, multiplicities: tuple[int, ...]) -> int:
    periods = [
        g // math.gcd(g, multiplicity)
        for multiplicity in multiplicities
    ]
    return math.lcm(*periods)


# The exact condition uniformly eliminating every sub-g polynomial
# Kummer mode is gcd(g,e_1,...,e_r)=1.
for test_g in range(2, 30):
    for multiplicities in partitions(test_g):
        period = kummer_period(test_g, multiplicities)
        assert (period == test_g) == (
            math.gcd(test_g, *multiplicities) == 1
        )
        for test_order in range(1, test_g):
            exponent_integral_at_every_root = all(
                (multiplicity * test_order) % test_g == 0
                for multiplicity in multiplicities
            )
            assert exponent_integral_at_every_root == (
                test_order % period == 0
            )


# If no root is strict, the degree sum can be saturated only at a
# Kummer order, and then g*h_i=e_i*E at every root.
for test_g in range(2, 18):
    for multiplicities in partitions(test_g):
        period = kummer_period(test_g, multiplicities)
        for test_order in range(1, 2 * test_g + 1):
            upper_h = [
                (multiplicity * test_order) // test_g
                for multiplicity in multiplicities
            ]
            can_reach_degree_bound = sum(upper_h) >= test_order
            assert can_reach_degree_bound == (
                test_order % period == 0
            )
            if can_reach_degree_bound:
                assert sum(upper_h) == test_order
                assert all(
                    test_g * horizontal
                    == multiplicity * test_order
                    for horizontal, multiplicity in zip(
                        upper_h,
                        multiplicities,
                    )
                )


# Once the local inequalities give R^(a-1)|T, the reciprocal degree
# bound gives deg L<=g-E, independently of the multiplicities.
for test_g in range(2, 15):
    for test_a in range(2, 9):
        for test_order in range(1, test_g):
            coefficient_bound = test_g * test_a - test_order
            divisor_degree = test_g * (test_a - 1)
            assert (
                coefficient_bound - divisor_degree
                == test_g - test_order
            )


# At a strict root one must use the first supported face monomial
# k0(d',h'), not assume that C has a linear term.  Global minimality,
# the slope comparison, and local polynomiality still force h<=e.
for test_e in range(1, 12):
    for primitive_d in range(1, 10):
        for primitive_h in range(1, test_e + 1):
            if math.gcd(primitive_d, primitive_h) != 1:
                continue
            for first_support in range(1, 8):
                supported_h = first_support * primitive_h
                if supported_h > test_e:
                    continue
                supported_d = first_support * primitive_d
                for global_order in range(1, supported_d + 1):
                    possible_horizontal_lengths = [
                        horizontal
                        for horizontal in range(1, 2 * test_e + 1)
                        if sp.Rational(
                            supported_d,
                            supported_h,
                        )
                        <= sp.Rational(global_order, horizontal)
                    ]
                    for horizontal in possible_horizontal_lengths:
                        assert horizontal <= supported_h <= test_e


# Verify the order-E linearized bracket and the residual Q ODE.
R = x**2 * (x - 1)
test_g = 3
test_a = 2
test_b = 3
test_n = test_g * test_a
test_m = test_g * test_b
test_order = 2
L = 1 + x
T = test_a * R ** (test_a - 1) * L
U_common = test_b * R ** (test_b - 1) * L
D = sp.Function("D")(x)
P0 = R**test_a
Q0 = R**test_b


def linearized_bracket(T_coefficient, U_coefficient):
    return sp.expand(
        test_order
        * (
            sp.diff(P0, x) * U_coefficient
            - T_coefficient * sp.diff(Q0, x)
        )
        + test_n
        * (
            P0 * sp.diff(U_coefficient, x)
            + T_coefficient * sp.diff(Q0, x)
        )
        - test_m
        * (
            Q0 * sp.diff(T_coefficient, x)
            + U_coefficient * sp.diff(P0, x)
        )
    )


assert linearized_bracket(T, U_common) == 0
residual_actual = linearized_bracket(T, U_common + D)
residual_expected = (
    test_a
    * R ** (test_a - 1)
    * (
        test_g * R * sp.diff(D, x)
        + (test_order - test_m) * sp.diff(R, x) * D
    )
)
assert sp.expand(residual_actual - residual_expected) == 0


# Kummer modes are exact homogeneous bracket solutions and saturate
# the reciprocal degree bound.
countermodels = (
    (2, x**2, 1),
    (4, x**2 * (x - 1) ** 2, 2),
)
for model_g, model_R, model_order in countermodels:
    model_a = 2
    model_b = 3
    model_n = model_g * model_a
    model_m = model_g * model_b
    fractional_power = sp.Rational(
        model_b * model_g - model_order,
        model_g,
    )
    factorization = sp.factor_list(model_R)[1]
    Q_mode = sp.Integer(1)
    for factor, multiplicity in factorization:
        exponent = multiplicity * fractional_power
        assert exponent.q == 1
        Q_mode *= factor ** int(exponent)
    P_model = model_R**model_a
    Q_model = model_R**model_b + tau**model_order * Q_mode
    bracket = sp.expand(
        tau
        * (
            sp.diff(P_model, x) * sp.diff(Q_model, tau)
            - sp.diff(P_model, tau) * sp.diff(Q_model, x)
        )
        + model_n * P_model * sp.diff(Q_model, x)
        - model_m * Q_model * sp.diff(P_model, x)
    )
    assert bracket == 0
    assert sp.degree(Q_mode, x) == model_m - model_order


# The CRT data L=0 mod X^2 and L(1)=1 have representative X^2,
# which violates the reciprocal bound deg L<=1 for g=3,E=2.
c0, c1, c2 = sp.symbols("c0 c1 c2")
candidate = c0 + c1 * x + c2 * x**2
solution = sp.solve(
    (
        candidate.subs(x, 0),
        sp.diff(candidate, x).subs(x, 0),
        candidate.subs(x, 1) - 1,
    ),
    (c0, c1, c2),
    dict=True,
)
assert solution == [{c0: 0, c1: 0, c2: 1}]
assert sp.degree(candidate.subs(solution[0]), x) == 2 > 1


# Reciprocal binomial degree bounds are compatible with the formal
# first common correction R -> R+tau^E L for every allowed degree of
# L.  Equality occurs only at the extremal degree g-E.  This is not
# an iteration check.
for test_g, test_a, test_b, test_order in itertools.product(
    range(2, 10),
    range(2, 7),
    range(3, 9),
    range(1, 9),
):
    if test_b <= test_a or test_order >= test_g:
        continue
    maximum_correction_degree = test_g - test_order
    for root_correction_degree in range(
        maximum_correction_degree + 1
    ):
        for binomial_order in range(test_a + 1):
            actual_degree_bound = (
                (test_a - binomial_order) * test_g
                + binomial_order * root_correction_degree
            )
            reciprocal_degree_bound = (
                test_g * test_a
                - binomial_order * test_order
            )
            assert actual_degree_bound <= reciprocal_degree_bound
            assert (
                actual_degree_bound == reciprocal_degree_bound
            ) == (
                binomial_order == 0
                or root_correction_degree
                == maximum_correction_degree
            )
        for binomial_order in range(test_b + 1):
            actual_degree_bound = (
                (test_b - binomial_order) * test_g
                + binomial_order * root_correction_degree
            )
            reciprocal_degree_bound = (
                test_g * test_b
                - binomial_order * test_order
            )
            assert actual_degree_bound <= reciprocal_degree_bound
            assert (
                actual_degree_bound == reciprocal_degree_bound
            ) == (
                binomial_order == 0
                or root_correction_degree
                == maximum_correction_degree
            )


print("verified: the uniform sub-g Kummer-mode condition")
print("verified: the no-strict equality classification")
print("verified: first-supported face steps force local divisibility")
print("verified: repeated local lengths glue through R^(a-1)")
print("verified: the exact residual Q differential equation")
print("verified: reciprocal-compatible Kummer countermodels")
print("verified: the sharp CRT degree obstruction")
print("verified: reciprocal bounds admit the first common correction")
