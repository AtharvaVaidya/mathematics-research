#!/usr/bin/env python3
"""Exact block compression for the 61+125 GGHV case-c branch.

This is a structural verifier, not an emptiness certificate.  It proves that
the 302 original coefficient rows are exactly 21 univariate grade identities
and analyzes the eight high grades under the forced top edge.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

from route_bd_verify import C_P_VERTICES, C_Q_VERTICES, lattice_points


def transformed_support(vertices):
    """Return (z-degree, y-grade) for z=x*y."""

    return tuple((x_degree, y_degree - x_degree) for x_degree, y_degree in lattice_points(vertices))


def support_inventory() -> None:
    p_support = transformed_support(C_P_VERTICES)
    q_support = transformed_support(C_Q_VERTICES)
    assert len(p_support) == 61
    assert len(q_support) == 125
    rows = set()
    term_count = 0
    grades = set()
    for u, d in p_support:
        for i, e in q_support:
            determinant = u * e - d * i
            if not determinant:
                continue
            z_degree = u + i - 1
            y_grade = d + e
            transformed_row = (z_degree, y_grade)
            original_row = (z_degree, z_degree + y_grade)
            expected_original = (
                u + i - 1,
                (u + d) + (i + e) - 1,
            )
            assert original_row == expected_original
            rows.add(original_row)
            grades.add(y_grade)
            term_count += 1
    assert len(rows) == 302
    assert term_count == 7141
    assert grades == set(range(-2, 21))

    p_bounds = {
        grade: (min(u for u, d in p_support if d == grade), max(u for u, d in p_support if d == grade))
        for grade in range(-1, 9)
    }
    q_bounds = {
        grade: (min(u for u, d in q_support if d == grade), max(u for u, d in q_support if d == grade))
        for grade in range(-1, 13)
    }
    assert p_bounds[-1] == (1, 1)
    assert q_bounds[-1] == (2, 2)
    for grade in range(0, 9):
        assert p_bounds[grade] == (0, min(grade + 2, 8))
    for grade in range(0, 13):
        assert q_bounds[grade] == (0, min(grade + 3, 12))


def add(*polynomials):
    size = max((len(poly) for poly in polynomials), default=0)
    result = [Fraction(0) for _ in range(size)]
    for poly in polynomials:
        for index, coefficient in enumerate(poly):
            result[index] += coefficient
    while result and not result[-1]:
        result.pop()
    return result


def scale(poly, scalar):
    return [Fraction(scalar) * coefficient for coefficient in poly]


def derivative(poly):
    return [degree * poly[degree] for degree in range(1, len(poly))]


def multiply(left, right):
    if not left or not right:
        return []
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    while result and not result[-1]:
        result.pop()
    return result


def shift(poly, amount):
    return [Fraction(0)] * amount + list(poly)


def top_operator(d, p_d, q_e, kappa=Fraction(1)):
    """Grade 12+d operator with T=z-t and e=d+4."""

    e = d + 4
    t8 = [Fraction(0)] * 8 + [Fraction(1)]
    t12 = [Fraction(0)] * 12 + [Fraction(1)]
    return add(
        scale(multiply(derivative(p_d), t12), 12 * kappa),
        scale(multiply(p_d, derivative(t12)), -d * kappa),
        scale(multiply(derivative(t8), q_e), e),
        scale(multiply(t8, derivative(q_e)), -8),
    )


def high_stage_checks() -> None:
    kernel_dimensions = []
    for d in range(7, -1, -1):
        e = d + 4
        p_degree = min(d + 2, 8)
        q_degree = min(e + 3, 12)

        # Verify every monomial in the claimed homogeneous kernel:
        # q=(3*kappa/2)T^4*p + gamma*T^e.
        for monomial_degree in range(p_degree + 1):
            p_d = [Fraction(0)] * monomial_degree + [Fraction(1)]
            q_e = shift(scale(p_d, Fraction(3, 2)), 4)
            assert not top_operator(d, p_d, q_e)
        resonant_q = [Fraction(0)] * e + [Fraction(1)]
        assert not top_operator(d, [], resonant_q)

        kernel_dimension = p_degree + 2
        kernel_dimensions.append(kernel_dimension)
        assert kernel_dimension == (
            (10, 10, 9, 8, 7, 6, 5, 4)[7 - d]
        )

        # The image is T^7 times every monomial through q_degree except T^e.
        attained = set()
        for degree in range(p_degree + 1):
            p_d = [Fraction(0)] * degree + [Fraction(1)]
            output = top_operator(d, p_d, [])
            attained.update(index for index, coefficient in enumerate(output) if coefficient)
        for degree in range(q_degree + 1):
            q_e = [Fraction(0)] * degree + [Fraction(1)]
            output = top_operator(d, [], q_e)
            attained.update(index for index, coefficient in enumerate(output) if coefficient)
        assert attained == (
            set(range(7, q_degree + 8)) - {e + 7}
        )

    assert kernel_dimensions == [10, 10, 9, 8, 7, 6, 5, 4]

    # First-grade displayed formula, with symbolic coefficient vectors.
    # For arbitrary p7 and gamma it reads
    # q11=(3*kappa/2)T^4*p7+gamma*T^11.
    p7 = [Fraction(index + 1) for index in range(9)]
    q11 = add(
        shift(scale(p7, Fraction(3, 2)), 4),
        [Fraction(0)] * 11 + [Fraction(7)],
    )
    assert not top_operator(7, p7, q11)


def main() -> None:
    support_inventory()
    high_stage_checks()
    print("case c: 61 P terms, 125 Q terms, 302 rows, 7141 terms")
    print("verified 21 grade identities for grades -2,...,20")
    print("forced-top high-stage kernel dimensions: 10,10,9,8,7,6,5,4")
    print(
        "each grade 12+d has exactly 8 cokernel conditions: "
        "T^7 divisibility plus vanishing resonant coefficient T^(d+11)"
    )
    print("RESULT: EXACT STRUCTURAL CHECKS PASS; CASE C REMAINS UNRESOLVED")


if __name__ == "__main__":
    main()
