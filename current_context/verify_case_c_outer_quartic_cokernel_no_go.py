#!/usr/bin/env python3
"""Verify the case-c outer-quartic remainder no-go over Fbar_32003.

The geometric conclusion is explained in
CASE_C_OUTER_QUARTIC_COKERNEL_NO_GO.md.  This script checks the exact
deficit-four/five operator ranks and the displayed nonzero minors of their
reductions modulo E and E^2 on all three factors of the outer Hurwitz
algebra.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from route_bd_case_c_radial_obstruction import (
    PARAMETERS,
    constant_wpoly,
    p_exponents,
    q_exponents,
    solve_stage,
)
from route_bd_fbar_obstruction import K, ONE, PRIME, outer_coefficients


Poly = dict[int, K]


def poly_add(*polynomials: Poly) -> Poly:
    result: Poly = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, K()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def poly_scale(polynomial: Poly, scalar: K) -> Poly:
    return {
        exponent: scalar * coefficient
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, K())
                + left_coefficient * right_coefficient
            )
            if not result[exponent]:
                del result[exponent]
    return result


def poly_power(polynomial: Poly, exponent: int) -> Poly:
    result = {0: ONE}
    for _ in range(exponent):
        result = poly_multiply(result, polynomial)
    return result


def bracket(
    p_degree: int,
    p: Poly,
    q_degree: int,
    q: Poly,
) -> Poly:
    """Return w*(p_degree*p*q' - q_degree*p'*q)."""

    result: Poly = {}
    for p_exponent, p_coefficient in p.items():
        for q_exponent, q_coefficient in q.items():
            coefficient = (
                p_degree * q_exponent - q_degree * p_exponent
            ) * p_coefficient * q_coefficient
            exponent = p_exponent + q_exponent
            if coefficient:
                result[exponent] = (
                    result.get(exponent, K()) + coefficient
                )
                if not result[exponent]:
                    del result[exponent]
    return result


def poly_remainder(dividend: Poly, divisor: Poly) -> Poly:
    remainder = dict(dividend)
    divisor_degree = max(divisor)
    divisor_lead = divisor[divisor_degree]
    while remainder and max(remainder) >= divisor_degree:
        remainder_degree = max(remainder)
        shift = remainder_degree - divisor_degree
        factor = remainder[remainder_degree] / divisor_lead
        subtraction = {
            exponent + shift: -factor * coefficient
            for exponent, coefficient in divisor.items()
        }
        remainder = poly_add(remainder, subtraction)
    return remainder


def matrix_rank(matrix: list[list[K]]) -> int:
    work = [list(row) for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [entry * inverse for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def determinant(matrix: list[list[K]]) -> K:
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    work = [list(row) for row in matrix]
    result = ONE
    for column in range(size):
        selected = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if selected is None:
            return K()
        if selected != column:
            work[column], work[selected] = work[selected], work[column]
            result = -result
        pivot = work[column][column]
        result *= pivot
        inverse = pivot.inverse()
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            multiplier = work[row][column] * inverse
            for index in range(column, size):
                work[row][index] -= multiplier * work[column][index]
    return result


def signed(value: int) -> int:
    value %= PRIME
    return value if value <= PRIME // 2 else value - PRIME


def signed_tuple(value: K) -> tuple[int, int, int]:
    return tuple(
        signed(coefficient)
        for coefficient in (value.c0, value.c1, value.c2)
    )


def outer_data(parameter: K) -> tuple[Poly, Poly, Poly]:
    u_coefficients, v_coefficients = outer_coefficients(parameter)
    u = {
        exponent: coefficient
        for exponent, coefficient in enumerate(u_coefficients)
        if coefficient
    }
    v = {
        exponent: coefficient
        for exponent, coefficient in enumerate(v_coefficients)
        if coefficient
    }
    leading_ratio = v_coefficients[10] ** 2 / u_coefficients[7] ** 3
    quartic = poly_add(
        {exponent + 1: coefficient for exponent, coefficient in poly_multiply(v, v).items()},
        poly_scale(poly_power(u, 3), -leading_ratio),
    )
    assert max(quartic) == 4
    return u, v, quartic


def outer_blocks(u: Poly, v: Poly) -> tuple[Poly, Poly]:
    p2 = {-1: ONE} | {
        index - 1: u[index]
        for index in range(1, 8)
        if u.get(index)
    }
    q3 = {-1: ONE} | {
        index - 1: v[index]
        for index in range(1, 11)
        if v.get(index)
    }
    return p2, q3


def profiles_through_deficit_five(
    parameter: K,
) -> tuple[tuple[int, int, int], ...]:
    """Run only the five exact stages needed here, not the full system."""

    u, v = outer_coefficients(parameter)
    p_blocks = {
        2: constant_wpoly(
            {-1: ONE} | {index - 1: u[index] for index in range(1, 8)}
        )
    }
    q_blocks = {
        3: constant_wpoly(
            {-1: ONE} | {index - 1: v[index] for index in range(1, 11)}
        )
    }
    free_by_degree = {
        1: PARAMETERS[0:2],
        0: PARAMETERS[2:4],
        -1: PARAMETERS[4:6],
        -2: PARAMETERS[6:7],
    }
    profiles: list[tuple[int, int, int]] = []
    for p_degree in (1, 0, -1, -2, -3):
        q_degree = p_degree + 1
        p_block, q_block, _constraints, profile = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
            p_exponents(p_degree),
            q_degree,
            q_exponents(q_degree),
            free_by_degree.get(p_degree, ()),
        )
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        profiles.append(profile)
    return tuple(profiles)


def operator_columns(
    deficit: int,
    p2: Poly,
    q3: Poly,
) -> tuple[list[Poly], tuple[int, ...], tuple[int, ...]]:
    p_degree = 2 - deficit
    q_degree = 3 - deficit
    p_support = tuple(range(-p_degree, 9))
    q_support = tuple(range(-q_degree, 13))
    columns = [
        bracket(p_degree, {exponent: ONE}, 3, q3)
        for exponent in p_support
    ]
    columns.extend(
        bracket(2, p2, q_degree, {exponent: ONE})
        for exponent in q_support
    )
    return columns, p_support, q_support


def remainder_matrix(
    columns: Iterable[Poly],
    modulus: Poly,
) -> list[list[K]]:
    degree = max(modulus)
    reduced = [poly_remainder(column, modulus) for column in columns]
    return [
        [column.get(exponent, K()) for column in reduced]
        for exponent in range(degree)
    ]


def verify_factor(
    label: str,
    parameter: K,
    expected_minor4: tuple[int, int, int],
    expected_minor8: tuple[int, int, int],
) -> None:
    u, v, quartic = outer_data(parameter)
    p2, q3 = outer_blocks(u, v)

    # The complete radial solve includes the source rows.  These are the
    # exact profiles (number of new variables, rank, cokernel dimension).
    profiles = profiles_through_deficit_five(parameter)
    assert profiles[3] == (19, 18, 2)
    assert profiles[4] == (17, 17, 2)

    columns4, p_support4, q_support4 = operator_columns(4, p2, q3)
    assert p_support4 == tuple(range(2, 9))
    assert q_support4 == tuple(range(1, 13))
    assert len(columns4) == 19
    matrix4 = remainder_matrix(columns4, quartic)
    assert matrix_rank(matrix4) == 4
    minor4 = determinant([row[:4] for row in matrix4])
    assert signed_tuple(minor4) == expected_minor4

    columns5, p_support5, q_support5 = operator_columns(5, p2, q3)
    assert p_support5 == tuple(range(3, 9))
    assert q_support5 == tuple(range(2, 13))
    assert len(columns5) == 17
    quartic_square = poly_multiply(quartic, quartic)
    matrix5 = remainder_matrix(columns5, quartic_square)
    assert matrix_rank(matrix5) == 8
    minor5 = determinant([row[:8] for row in matrix5])
    assert signed_tuple(minor5) == expected_minor8

    print(
        f"{label}: profiles (19,18,2), (17,17,2); "
        f"remainder ranks 4, 8; minors "
        f"{signed_tuple(minor4)}, {signed_tuple(minor5)}"
    )


def main() -> None:
    # Source-pair inventories after separating the two new-block summands.
    assert [(r, 1 - r) for r in (1, 0, -1)] == [
        (1, 0),
        (0, 1),
        (-1, 2),
    ]
    assert [(r, -r) for r in (1, 0, -1, -2)] == [
        (1, -1),
        (0, 0),
        (-1, 1),
        (-2, 2),
    ]

    verify_factor(
        "rational factor 1",
        K(26839),
        (-15118, 0, 0),
        (574, 0, 0),
    )
    verify_factor(
        "rational factor 2",
        K(16621),
        (6356, 0, 0),
        (12957, 0, 0),
    )
    verify_factor(
        "cubic factor",
        K(0, 1),
        (-3045, 2843, 11230),
        (-9388, -14360, 8299),
    )
    print("RESULT: RAW REMAINDER MODULO E OR E^2 IS NOT A COKERNEL INVARIANT")


if __name__ == "__main__":
    main()
