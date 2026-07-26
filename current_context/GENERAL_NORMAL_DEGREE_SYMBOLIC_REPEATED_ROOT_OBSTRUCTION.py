#!/usr/bin/env python3
"""Symbolic-in-g audit of the repeated-root defect obstruction.

This file is intentionally self-contained.  It uses compact rational
expressions in ``x`` and symbolic powers ``x**G``; no loop over degrees is
part of the proof.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


x, ell, u = sp.symbols("x ell u", nonzero=True)
G = sp.symbols("G", integer=True, positive=True)
N = 3 * G - 4


def dx(value: sp.Expr) -> sp.Expr:
    return sp.diff(value, x)


d = x ** (G - 1) * (x + ell)
d1 = x ** (G - 2) * (G * x + (G - 1) * ell)
d2 = dx(d1)
r = ell ** (2 * G - 2) * x ** (G - 1)

p1 = -4 * d1 / (3 * u**2)
q1 = 1 / u - 2 * d * d1 / u**2

divided = sp.cancel((d1**3 - r) / d)
p2 = sp.Rational(8, 9) / u**5 * (
    divided - d1 * d2 - 2 * d1 * r / u
)
q2 = (
    2 * d2 / (3 * u**4)
    + 4 * d1**3 / (3 * u**5)
    - 4 * d * d1 * d2 / (3 * u**5)
    - 8 * d * d1 * r / (3 * u**6)
)

H3 = 2 * dx(p1) * q2 - p1 * dx(q2) + dx(p2) * q1 - 2 * p2 * dx(q1)
h3 = -H3 / 3
f3 = sp.factor(q1 * h3)


def affine_exponent(power: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """Return a,b with power=a*G+b."""
    polynomial = sp.Poly(sp.expand(power), G)
    assert polynomial.degree() <= 1
    return polynomial.coeff_monomial(G), polynomial.coeff_monomial(1)


def fixed_denominator_terms(value: sp.Expr) -> tuple[list[tuple[sp.Expr, sp.Expr]], int]:
    """Write value=sum c_M*x^M/(x+ell)^p with one fixed p."""
    numerator, denominator = map(sp.factor, sp.together(value).as_numer_denom())
    p = 0
    x_power = denominator.as_powers_dict().get(x, 0)
    quotient = sp.cancel(denominator / x**x_power)
    while sp.cancel(quotient / (x + ell)).is_polynomial(x):
        quotient = sp.cancel(quotient / (x + ell))
        p += 1
    assert not quotient.has(x)
    terms: list[tuple[sp.Expr, sp.Expr]] = []
    for term in sp.Add.make_args(sp.expand(numerator)):
        powers = term.as_powers_dict()
        raw_exponent = powers.get(x, 0)
        exponent = sp.expand(raw_exponent - x_power)
        coefficient = sp.cancel(term / x**raw_exponent / quotient)
        if coefficient.has(x):
            raise AssertionError((term, exponent, sp.factor(coefficient), numerator, denominator))
        terms.append((coefficient, exponent))
    return terms, p


@lru_cache(maxsize=None)
def negative_binomial_tail(p: int, L: sp.Expr) -> sp.Expr:
    """P with (1+z)^(-p)-Taylor_(<L)=(-1)^L z^L P/(1+z)^p."""
    z = sp.symbols("z")
    # The numerator has degree p-1 after removal of z**L.  Its
    # coefficient of z**r is obtained from the last p omitted terms.
    coefficients = []
    for r_index in range(p):
        total = 0
        for s_value in range(1, p - r_index + 1):
            total += (
                (-1) ** (s_value + 1)
                * sp.binomial(L + p - s_value - 1, p - 1)
                * sp.binomial(p, r_index + s_value)
            )
        coefficients.append(sp.factor(total))
    return sp.expand(sum(c * z**i for i, c in enumerate(coefficients)))


def symbolic_tail(value: sp.Expr) -> sp.Expr:
    """Return S in value=value_(<N)+x**N*S, uniformly for G>=5."""
    terms, p = fixed_denominator_terms(value)
    z = sp.symbols("z")
    output = 0
    for coefficient, exponent in terms:
        delta = sp.expand(exponent - N)
        slope, intercept = affine_exponent(delta)
        at_five = sp.expand(delta.subs(G, 5))
        if slope >= 0 and at_five >= 0:
            output += coefficient * x**delta / (x + ell) ** p
            continue
        if not (slope <= 0 and at_five < 0):
            raise AssertionError(("crossing exponent", exponent, delta, slope, at_five))
        L = -delta
        if p == 0:
            continue
        polynomial = negative_binomial_tail(p, L).subs(z, x / ell)
        output += (
            coefficient
            * (-1) ** L
            * ell ** (-L)
            * polynomial
            / (x + ell) ** p
        )
    return sp.factor(output)


S3 = symbolic_tail(f3)

E = ell ** (2 * G - 1)
C = (-1) ** G * sp.Rational(32, 27) / u**10
root_d = -ell
root_d1 = -(G - 1) * ell / G

expected_S3 = (
    C * ell ** (G - 1) * u * (3 * E + (6 * G - 4) * u),
    C
    * ell ** (G - 2)
    * (
        -6 * E**2
        + (-15 * G + 12) * E * u
        + (-10 * G**2 + 16 * G - 6) * u**2
    ),
    2 * G * C * ell ** (G - 1) * u**2,
)

actual_S3 = (
    None,
    None,
    None,
)

def integer_power_normal_form(value: sp.Expr) -> sp.Expr:
    """Normalize signs of affine-in-G integer powers."""
    def one_minus_g(power: sp.Expr) -> sp.Expr:
        if not isinstance(power, sp.Pow) or sp.expand(power.base - (1 - G)) != 0:
            return power
        exponent = sp.Poly(sp.expand(power.exp), G)
        assert exponent.degree() <= 1
        a_value = int(exponent.coeff_monomial(G))
        b_value = int(exponent.coeff_monomial(1))
        sign = sp.Integer(-1) ** b_value * (
            sp.Integer(-1) ** G if a_value % 2 else 1
        )
        return sign * (G - 1) ** power.exp

    value = value.replace(
        lambda item: isinstance(item, sp.Pow)
        and sp.expand(item.base - (1 - G)) == 0,
        one_minus_g,
    )
    value = sp.expand_power_base(value, force=True)
    value = value.replace(
        lambda item: isinstance(item, sp.Pow)
        and sp.expand(item.base - (1 - G)) == 0,
        one_minus_g,
    )

    def parity(power: sp.Expr) -> sp.Expr:
        if not isinstance(power, sp.Pow) or power.base != -1:
            return power
        exponent = sp.Poly(sp.expand(power.exp), G)
        if exponent.degree() > 1:
            return power
        a_value = int(exponent.coeff_monomial(G))
        b_value = int(exponent.coeff_monomial(1))
        return sp.Integer(-1) ** b_value * (
            sp.Integer(-1) ** G if a_value % 2 else 1
        )

    value = value.replace(
        lambda item: isinstance(item, sp.Pow) and item.base == -1,
        parity,
    )
    return sp.factor(sp.powsimp(sp.expand_func(value), force=True))


def integer_power_light(value: sp.Expr) -> sp.Expr:
    """Termwise sign normalization without expensive multivariate factoring."""
    value = sp.expand_power_base(value, force=True)

    def normalize_power(power: sp.Expr) -> sp.Expr:
        if not isinstance(power, sp.Pow):
            return power
        if power.exp.has(G) and power.base.is_polynomial(G):
            factored_base = sp.factor(power.base)
            if factored_base != power.base:
                return integer_power_light(
                    sp.expand_power_base(
                        factored_base ** power.exp,
                        force=True,
                    )
                )
        if sp.expand(power.base - (1 - G)) == 0:
            exponent = sp.Poly(sp.expand(power.exp), G)
            a_value = int(exponent.coeff_monomial(G))
            b_value = int(exponent.coeff_monomial(1))
            sign = sp.Integer(-1) ** b_value * (
                sp.Integer(-1) ** G if a_value % 2 else 1
            )
            return sign * (G - 1) ** power.exp
        if power.base == -1:
            exponent = sp.Poly(sp.expand(power.exp), G)
            a_value = int(exponent.coeff_monomial(G))
            b_value = int(exponent.coeff_monomial(1))
            return sp.Integer(-1) ** b_value * (
                sp.Integer(-1) ** G if a_value % 2 else 1
            )
        return power

    value = value.replace(
        lambda item: isinstance(item, sp.Pow)
        and (item.base == -1 or sp.expand(item.base - (1 - G)) == 0),
        normalize_power,
    )
    value = sp.expand_power_base(sp.expand_func(value), force=True)
    value = value.replace(
        lambda item: isinstance(item, sp.Pow) and item.base == -1,
        normalize_power,
    )
    return value


def removable_jet_at_minus_ell(value: sp.Expr, order: int) -> sp.Expr:
    numerator, denominator = sp.together(value).as_numer_denom()
    p = 0
    x_power = denominator.as_powers_dict().get(x, 0)
    unit = sp.cancel(denominator / x**x_power)
    while sp.cancel(unit / (x + ell)).is_polynomial(x):
        unit = sp.cancel(unit / (x + ell))
        p += 1
    assert not unit.has(x)
    def regular_numerator_jet(j: int) -> sp.Expr:
        return (
            sp.factorial(j)
            * sp.diff(numerator, x, p + j).subs(x, -ell)
            / sp.factorial(p + j)
        )

    if order == 0:
        result = regular_numerator_jet(0) * (-ell) ** (-x_power) / unit
    elif order == 1:
        result = (
            regular_numerator_jet(1) * (-ell) ** (-x_power)
            - x_power
            * regular_numerator_jet(0)
            * (-ell) ** (-x_power - 1)
        ) / unit
    else:
        raise NotImplementedError
    return integer_power_normal_form(result)


actual_S3 = (
    removable_jet_at_minus_ell(S3, 0),
    removable_jet_at_minus_ell(S3, 1),
    integer_power_normal_form(sp.factor(S3.subs(x, root_d1))),
)

for index, (actual, expected) in enumerate(zip(actual_S3, expected_S3)):
    difference = sp.factor(actual - expected)
    if difference != 0:
        raise AssertionError((index, sp.factor(actual), sp.factor(expected), difference))

print("verified: defect-three tail data symbolically for every integer G>=5")


# Exceptional branch at defect three.
special_u = -ell ** (2 * G - 1) / (G - 1)
special_substitution = {u: special_u}
special_A = sp.factor((u + 2 * d * d1).subs(special_substitution))
special_B = 3 * d**2 * d1
special_h3 = sp.factor(h3.subs(special_substitution))
special_f3 = sp.factor(f3.subs(special_substitution))
special_S3 = sp.factor(S3.subs(special_substitution))
special_low3 = sp.factor(special_f3 - x**N * special_S3)

special_C = (-1) ** G * sp.Rational(32, 27) / special_u**10
special_a0 = special_C * ell ** (G - 1) * (
    6 * (G - 1) * E**2
    + 3 * (G - 1) * (4 * G - 5) * E * special_u
    + 2 * (3 * G**3 - 11 * G**2 + 14 * G - 5) * special_u**2
)
special_a1 = special_C * ell ** (G - 2) * (
    6 * (2 * G - 1) * E**2
    + 3 * (8 * G**2 - 13 * G + 4) * E * special_u
    + 2 * (G - 1) * (2 * G - 3) * (3 * G - 1) * special_u**2
)
special_q3 = sp.factor(special_low3 + x**N * (special_a0 + special_a1 * x))
special_p3 = sp.factor(sp.cancel((special_A * special_q3 - special_h3) / special_B))

special_p1 = sp.factor(p1.subs(special_substitution))
special_q1 = sp.factor(q1.subs(special_substitution))
special_p2 = sp.factor(p2.subs(special_substitution))
special_q2 = sp.factor(q2.subs(special_substitution))

special_H4 = (
    3 * dx(special_p1) * special_q3
    - special_p1 * dx(special_q3)
    + 2 * dx(special_p2) * special_q2
    - 2 * special_p2 * dx(special_q2)
    + dx(special_p3) * special_q1
    - 3 * special_p3 * dx(special_q1)
)
special_h4 = sp.factor(-special_H4 / 4)
special_f4 = sp.factor(special_q1 * special_h4)

print("exceptional p3 denominator:", sp.factor(sp.together(special_p3).as_numer_denom()[1]))
print("exceptional f4 denominator:", sp.factor(sp.together(special_f4).as_numer_denom()[1]))


def two_pole_partial_fractions(
    h1: sp.Expr,
    p_order: int,
    h2: sp.Expr,
    q_order: int,
    constant: sp.Expr,
) -> list[tuple[sp.Expr, sp.Expr, int]]:
    """Partial fractions of 1/[constant*(x+h1)^p*(x+h2)^q]."""
    output: list[tuple[sp.Expr, sp.Expr, int]] = []
    delta = h2 - h1
    for pole_order in range(1, p_order + 1):
        j_value = p_order - pole_order
        coefficient = (
            (-1) ** j_value
            * sp.binomial(q_order + j_value - 1, j_value)
            * delta ** (-q_order - j_value)
            / constant
        )
        output.append((sp.factor(coefficient), h1, pole_order))
    reverse_delta = h1 - h2
    for pole_order in range(1, q_order + 1):
        j_value = q_order - pole_order
        coefficient = (
            (-1) ** j_value
            * sp.binomial(p_order + j_value - 1, j_value)
            * reverse_delta ** (-p_order - j_value)
            / constant
        )
        output.append((sp.factor(coefficient), h2, pole_order))
    return output


def two_pole_symbolic_tail_jets(value: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """The double-root Hermite value and derivative of the f4 tail."""
    numerator, denominator = map(sp.factor, sp.together(value).as_numer_denom())
    x_power = denominator.as_powers_dict().get(x, 0)
    h1 = ell
    h2 = (G - 1) * ell / G
    constant = 81 * ell ** (24 * G - 7) * G**2
    expected_denominator = (
        constant * x**x_power * (x + h1) ** 5 * (x + h2) ** 2
    )
    assert sp.factor(denominator - expected_denominator) == 0
    fractions = two_pole_partial_fractions(h1, 5, h2, 2, constant)
    jets: list[list[sp.Expr]] = [[], []]
    jet_specs = ((-h1, 0), (-h1, 1))

    def add_known_fraction(
        scalar: sp.Expr,
        x_exponent: sp.Expr,
        polynomial_value: sp.Expr,
        denominator_factors: tuple[tuple[sp.Expr, int], ...],
    ) -> None:
        def multiply_series(
            left: list[sp.Expr],
            right: list[sp.Expr],
            cap: int,
        ) -> list[sp.Expr]:
            return [
                sum(
                    left[index] * right[degree - index]
                    for index in range(degree + 1)
                )
                for degree in range(cap + 1)
            ]

        for jet_index, (root_value, derivative_order) in enumerate(jet_specs):
            pole_order = 0
            other_factors: list[tuple[sp.Expr, int]] = []
            for shift_value, factor_order in denominator_factors:
                if sp.factor(root_value + shift_value) == 0:
                    pole_order += factor_order
                else:
                    other_factors.append((shift_value, factor_order))
            target_degree = pole_order + derivative_order
            series_value = [
                sp.binomial(x_exponent, degree)
                * root_value ** (x_exponent - degree)
                for degree in range(target_degree + 1)
            ]
            polynomial_series = [
                sp.diff(polynomial_value, x, degree).subs(x, root_value)
                / sp.factorial(degree)
                for degree in range(target_degree + 1)
            ]
            series_value = multiply_series(
                series_value, polynomial_series, target_degree
            )
            for shift_value, factor_order in other_factors:
                denominator_series = [
                    (-1) ** degree
                    * sp.binomial(factor_order + degree - 1, degree)
                    * (root_value + shift_value) ** (-factor_order - degree)
                    for degree in range(target_degree + 1)
                ]
                series_value = multiply_series(
                    series_value, denominator_series, target_degree
                )
            jets[jet_index].append(
                integer_power_normal_form(
                    sp.factor(scalar * series_value[target_degree])
                )
            )

    z = sp.symbols("z")
    stable_from = 5
    for term in sp.Add.make_args(sp.expand(numerator)):
        powers = term.as_powers_dict()
        raw_exponent = powers.get(x, 0)
        exponent = sp.expand(raw_exponent - x_power)
        coefficient = sp.cancel(term / x**raw_exponent)
        assert not coefficient.has(x)
        delta = sp.expand(exponent - N)
        slope, _ = affine_exponent(delta)
        at_five = sp.expand(delta.subs(G, 5))
        if slope >= 0 and at_five >= 0:
            add_known_fraction(
                coefficient / constant,
                delta,
                sp.Integer(1),
                ((h1, 5), (h2, 2)),
            )
            continue
        # A negative slope eventually enters the low Taylor part.
        # Record the first degree at which the classification is stable;
        # the finitely many smaller degrees are checked independently.
        if slope < 0:
            _, intercept = affine_exponent(delta)
            stable_from = max(
                stable_from,
                int(sp.floor(intercept / (-slope))) + 1,
            )
        elif not (slope == 0 and at_five < 0):
            raise AssertionError(("crossing exponent f4", exponent, delta, slope, at_five))
        L = -delta
        for pf_coefficient, shift, pole_order in fractions:
            polynomial = negative_binomial_tail(pole_order, L).subs(
                z, x / shift
            )
            add_known_fraction(
                coefficient
                * pf_coefficient
                * (-1) ** L
                * shift ** (-L),
                sp.Integer(0),
                polynomial,
                ((shift, pole_order),),
            )
    print("exceptional symbolic tail is stable from G =", stable_from)
    return tuple(sp.Add(*entries) for entries in jets)


def removable_jet(value: sp.Expr, root: sp.Expr, order: int) -> sp.Expr:
    """Value/first derivative after removing the pole factor at root."""
    numerator, denominator = sp.together(value).as_numer_denom()
    p_order = 0
    unit = denominator
    while sp.cancel(unit / (x - root)).is_polynomial(x):
        unit = sp.cancel(unit / (x - root))
        p_order += 1

    def w_jet(j_value: int) -> sp.Expr:
        return (
            sp.factorial(j_value)
            * sp.diff(numerator, x, p_order + j_value).subs(x, root)
            / sp.factorial(p_order + j_value)
        )

    unit0 = unit.subs(x, root)
    if order == 0:
        result = w_jet(0) / unit0
    elif order == 1:
        result = w_jet(1) / unit0 - w_jet(0) * dx(unit).subs(x, root) / unit0**2
    else:
        raise NotImplementedError
    return integer_power_normal_form(sp.factor(result))


def additive_laurent_jet(value: sp.Expr, root: sp.Expr, order: int) -> sp.Expr:
    """Extract a regular jet termwise, before combining a large sum."""
    coefficients: list[sp.Expr] = []
    for term in sp.Add.make_args(value):
        numerator, denominator = sp.together(term).as_numer_denom()
        pole_order = 0
        unit = denominator
        while True:
            quotient, remainder = sp.div(
                sp.Poly(unit, x),
                sp.Poly(x - root, x),
            )
            if remainder.as_expr() != 0:
                break
            unit = quotient.as_expr()
            pole_order += 1
        regular_part = numerator / unit
        coefficients.append(
            sp.diff(regular_part, x, pole_order + order).subs(x, root)
            / sp.factorial(pole_order + order)
        )
    coefficient = sp.Add(*coefficients)
    if order == 1:
        # The coefficient of t is the first derivative.
        pass
    return integer_power_normal_form(sp.factor(coefficient))


actual_S4 = two_pole_symbolic_tail_jets(special_f4)
expected_S4 = (
    sp.Rational(32, 81)
    * (G - 1) ** 12
    * (9 * G**2 + 41 * G - 25)
    / ell ** (20 * G - 8),
    sp.Rational(160, 243)
    * G
    * (G - 1) ** 12
    * (11 * G + 8)
    / ell ** (20 * G - 7),
)
for index, (actual, expected) in enumerate(zip(actual_S4, expected_S4)):
    difference = sp.expand(
        sp.together(actual - expected).as_numer_denom()[0]
    )
    difference = sp.Add(
        *(integer_power_light(term) for term in sp.Add.make_args(difference))
    )
    e_g, e_gm1, e_ell, e_sign = sp.symbols(
        "e_g e_gm1 e_ell e_sign"
    )

    def split_affine_exponential(power: sp.Expr) -> sp.Expr:
        if not isinstance(power, sp.Pow):
            return power
        exponent = sp.Poly(sp.expand(power.exp), G)
        if exponent.degree() > 1:
            return power
        a_value = exponent.coeff_monomial(G)
        b_value = exponent.coeff_monomial(1)
        if sp.expand(power.base - ell * (1 - G)) == 0:
            return (
                e_sign**a_value
                * sp.Integer(-1) ** b_value
                * e_ell**a_value
                * ell**b_value
                * e_gm1**a_value
                * (G - 1) ** b_value
            )
        bases = {
            G: e_g,
            G - 1: e_gm1,
            ell: e_ell,
            sp.Integer(-1): e_sign,
        }
        token = None
        for base_value, token_value in bases.items():
            if sp.expand(power.base - base_value) == 0:
                token = token_value
                break
        if token is None:
            return power
        return token ** a_value * power.base ** b_value

    difference = difference.replace(
        lambda item: isinstance(item, sp.Pow),
        split_affine_exponential,
    )
    grouped_coefficients: dict[tuple[sp.Expr, ...], list[sp.Expr]] = {}
    tokens = (e_g, e_gm1, e_ell, e_sign)
    for term in sp.Add.make_args(difference):
        powers = term.as_powers_dict()
        key = tuple(powers.get(token, 0) for token in tokens)
        coefficient = term
        for token, exponent in zip(tokens, key):
            coefficient /= token**exponent
        grouped_coefficients.setdefault(key, []).append(coefficient)
    reduced_coefficients = [
        sp.factor(sp.Add(*coefficients))
        for coefficients in grouped_coefficients.values()
    ]
    if all(coefficient == 0 for coefficient in reduced_coefficients):
        difference = sp.Integer(0)
    if difference != 0:
        raise AssertionError(
            (
                "S4",
                index,
                sp.N((actual - expected).subs({G: 8, ell: 2})),
                len(grouped_coefficients),
                next(
                    coefficient
                    for coefficient in reduced_coefficients
                    if coefficient != 0
                ),
            )
        )

print("verified: exceptional defect-four double-root Hermite data symbolically for G>=8")
print("boundary G=5,6,7 is covered by the independent exact finite verifier")
