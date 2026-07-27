#!/usr/bin/env python3
"""Symbolic filtered obstruction for the saturated E-partition family.

Away from one explicitly audited affine-exponent collision, this
verifies symbolically in E the defect-four obstruction for every
integer E >= 11 for

    g = 2(E+1),  d = x^(E+2) (x^E + ell),
    p0 = d^2 + u*x,  q0 = d^3.

The collision E=12 and the remaining boundary value E=10 are checked
by ordinary polynomial division at the end.
"""

from __future__ import annotations

from collections.abc import Mapping

import sympy as sp


E, ell, u, x = sp.symbols("E ell u x", nonzero=True)
Exponent = tuple[int, int]  # Represents a*E+b.
Sparse = dict[Exponent, sp.Expr]
THRESHOLD = 11
LARGE_COLLISION_VALUES: set[int] = set()


def normalize(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(value))


def assert_no_large_exponent_collision(value: Mapping[Exponent, sp.Expr]) -> None:
    """Record special E where two formal affine exponents coincide."""
    exponents = tuple(value)
    for index, left in enumerate(exponents):
        for right in exponents[index + 1 :]:
            slope = left[0] - right[0]
            intercept = right[1] - left[1]
            if slope == 0 or intercept % slope != 0:
                continue
            collision = intercept // slope
            if collision >= THRESHOLD:
                LARGE_COLLISION_VALUES.add(collision)


def clean(value: Mapping[Exponent, sp.Expr]) -> Sparse:
    output: Sparse = {}
    for exponent, coefficient in value.items():
        simplified = normalize(coefficient)
        if simplified != 0:
            output[exponent] = simplified
    assert_no_large_exponent_collision(output)
    return output


def add(*values: Mapping[Exponent, sp.Expr]) -> Sparse:
    output: Sparse = {}
    for value in values:
        for exponent, coefficient in value.items():
            output[exponent] = output.get(exponent, 0) + coefficient
    return clean(output)


def scale(value: Mapping[Exponent, sp.Expr], coefficient: sp.Expr) -> Sparse:
    return clean(
        {exponent: coefficient * term for exponent, term in value.items()}
    )


def multiply(left: Mapping[Exponent, sp.Expr], right: Mapping[Exponent, sp.Expr]) -> Sparse:
    output: Sparse = {}
    for (a_left, b_left), c_left in left.items():
        for (a_right, b_right), c_right in right.items():
            exponent = (a_left + a_right, b_left + b_right)
            output[exponent] = output.get(exponent, 0) + c_left * c_right
    return clean(output)


def derivative(value: Mapping[Exponent, sp.Expr]) -> Sparse:
    output: Sparse = {}
    for (a_value, b_value), coefficient in value.items():
        degree = a_value * E + b_value
        if degree != 0:
            output[(a_value, b_value - 1)] = coefficient * degree
    return clean(output)


def exponent_difference(left: Exponent, right: Exponent) -> tuple[int, int]:
    return left[0] - right[0], left[1] - right[1]


def positive_for_all_large(exponent: Exponent) -> bool:
    slope, intercept = exponent
    at_threshold = slope * THRESHOLD + intercept
    if slope < 0:
        return False
    return at_threshold > 0


def nonnegative_for_all_large(exponent: Exponent) -> bool:
    return exponent == (0, 0) or positive_for_all_large(exponent)


def leading_exponent(value: Mapping[Exponent, sp.Expr]) -> Exponent:
    assert value
    candidate = max(value, key=lambda exponent: (exponent[0], exponent[1]))
    for exponent in value:
        difference = exponent_difference(candidate, exponent)
        assert nonnegative_for_all_large(difference), (candidate, exponent)
    return candidate


def divide(
    numerator: Mapping[Exponent, sp.Expr],
    denominator: Mapping[Exponent, sp.Expr],
) -> tuple[Sparse, Sparse]:
    remainder = clean(numerator)
    denominator = clean(denominator)
    denominator_degree = leading_exponent(denominator)
    denominator_lead = denominator[denominator_degree]
    quotient: Sparse = {}
    while remainder:
        remainder_degree = leading_exponent(remainder)
        difference = exponent_difference(remainder_degree, denominator_degree)
        if not nonnegative_for_all_large(difference):
            break
        coefficient = normalize(remainder[remainder_degree] / denominator_lead)
        quotient = add(quotient, {difference: coefficient})
        remainder = add(
            remainder,
            scale(
                multiply({difference: coefficient}, denominator),
                -1,
            ),
        )
    return clean(quotient), clean(remainder)


def exact_divide(
    numerator: Mapping[Exponent, sp.Expr],
    denominator: Mapping[Exponent, sp.Expr],
) -> Sparse:
    quotient, remainder = divide(numerator, denominator)
    assert not remainder, remainder
    return quotient


def power(value: Mapping[Exponent, sp.Expr], exponent: int) -> Sparse:
    output: Sparse = {(0, 0): sp.Integer(1)}
    for _ in range(exponent):
        output = multiply(output, value)
    return output


one: Sparse = {(0, 0): sp.Integer(1)}
d: Sparse = {(2, 2): sp.Integer(1), (1, 2): ell}
d1 = derivative(d)
d2 = derivative(d1)
r: Sparse = {(1, 3): -(E**3) * ell**5}

A = add({(0, 0): u}, scale(multiply(d, d1), 2))
B = scale(multiply(power(d, 2), d1), 3)

p1 = scale(d1, -sp.Rational(4, 3) / u**2)
q1 = add(
    {(0, 0): 1 / u},
    scale(multiply(d, d1), -2 / u**2),
)

divided_d1_cube = exact_divide(add(power(d1, 3), scale(r, -1)), d)
p2 = scale(
    add(
        divided_d1_cube,
        scale(multiply(d1, d2), -1),
        scale(multiply(d1, r), -2 / u),
    ),
    sp.Rational(8, 9) / u**5,
)
q2 = add(
    scale(d2, sp.Rational(2, 3) / u**4),
    scale(power(d1, 3), sp.Rational(4, 3) / u**5),
    scale(multiply(multiply(d, d1), d2), -sp.Rational(4, 3) / u**5),
    scale(multiply(multiply(d, d1), r), -sp.Rational(8, 3) / u**6),
)

H3 = add(
    scale(multiply(derivative(p1), q2), 2),
    scale(multiply(p1, derivative(q2)), -1),
    multiply(derivative(p2), q1),
    scale(multiply(p2, derivative(q1)), -2),
)
h3 = scale(H3, -sp.Rational(1, 3))
_, q3 = divide(multiply(q1, h3), B)

q3_degree = leading_exponent(q3)
assert nonnegative_for_all_large(
    exponent_difference((6, 3), q3_degree)
), q3_degree
p3 = exact_divide(add(multiply(A, q3), scale(h3, -1)), B)
p3_degree = leading_exponent(p3)
assert nonnegative_for_all_large(
    exponent_difference((4, 1), p3_degree)
), p3_degree

H4 = add(
    scale(multiply(derivative(p1), q3), 3),
    scale(multiply(p1, derivative(q3)), -1),
    scale(multiply(derivative(p2), q2), 2),
    scale(multiply(p2, derivative(q2)), -2),
    multiply(derivative(p3), q1),
    scale(multiply(p3, derivative(q1)), -3),
)
h4 = scale(H4, -sp.Rational(1, 4))
_, q4 = divide(multiply(q1, h4), B)

definitely_forbidden: set[Exponent] = set()
for exponent in q4:
    difference = exponent_difference(exponent, (6, 2))
    if positive_for_all_large(difference):
        definitely_forbidden.add(exponent)
        continue
    reverse = exponent_difference((6, 2), exponent)
    assert nonnegative_for_all_large(reverse), (
        "degree comparison crosses at or above the threshold",
        exponent,
    )
assert definitely_forbidden == {(6, 3)}, definitely_forbidden

expected = (
    sp.Rational(160, 81)
    * E**3
    * (E + 1) ** 2
    * (188 * E**2 + 393 * E + 183)
    * ell**4
    / u**11
)
actual = q4.get((6, 3), 0)
assert normalize(actual - expected) == 0, (normalize(actual), normalize(expected))
assert LARGE_COLLISION_VALUES == {12}, LARGE_COLLISION_VALUES
print("verified: symbolic defect-four formula away from the sole collision E=12")
print("obstruction =", sp.factor(actual))


def concrete_obstruction(e_value: int) -> tuple[sp.Expr, sp.Expr]:
    g_value = 2 * (e_value + 1)
    d_value = x ** (g_value - e_value) * (x**e_value + ell)
    d1_value = sp.diff(d_value, x)
    field = sp.QQ.frac_field(ell, u)
    A_value = u + 2 * d_value * d1_value
    B_value = 3 * d_value**2 * d1_value
    inverse = sp.invert(A_value, B_value, domain=field)
    p_values = [d_value**2 + u * x, -4 * d1_value / (3 * u**2)]
    q_values = [d_value**3, 1 / u - 2 * d_value * d1_value / u**2]
    for defect in range(2, 5):
        h_value = -sum(
            j * sp.diff(p_values[i], x) * q_values[j]
            - i * p_values[i] * sp.diff(q_values[j], x)
            for i in range(1, defect)
            for j in [defect - i]
        ) / defect
        q_value = sp.rem(
            sp.expand(inverse * h_value),
            B_value,
            x,
            domain=field,
        )
        p_value = sp.cancel((A_value * q_value - h_value) / B_value)
        p_values.append(p_value)
        q_values.append(q_value)
    q4_polynomial = sp.Poly(q_values[4], x)
    return (
        sp.factor(q4_polynomial.coeff_monomial(x ** (3 * g_value - 3))),
        sp.factor(q4_polynomial.coeff_monomial(x ** (3 * g_value - 2))),
    )


boundary_actual = concrete_obstruction(10)
boundary_expected = (sp.factor(expected.subs(E, 10)), sp.Integer(0))
assert all(
    sp.factor(actual - expected_value) == 0
    for actual, expected_value in zip(boundary_actual, boundary_expected)
)
print("verified: boundary case E=10")

for collision_value in sorted(LARGE_COLLISION_VALUES):
    collision_actual = concrete_obstruction(collision_value)
    collision_expected = (
        sp.factor(expected.subs(E, collision_value)),
        sp.Integer(0),
    )
    assert all(
        sp.factor(actual_value - expected_value) == 0
        for actual_value, expected_value in zip(
            collision_actual,
            collision_expected,
        )
    )
    print(f"verified: affine-exponent collision E={collision_value}")

print("verified: defect-four obstruction for every integer E>=10")
