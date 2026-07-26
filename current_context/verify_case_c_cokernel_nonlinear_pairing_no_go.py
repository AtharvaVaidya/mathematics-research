#!/usr/bin/env python3
"""Verify the first nonlinear case-c cokernel pairing no-go."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from current_context.verify_case_c_outer_quartic_cokernel_no_go import (
    ONE,
    Poly,
    determinant,
    matrix_rank,
    operator_columns,
    outer_blocks,
    outer_data,
    poly_add,
    poly_multiply,
    poly_power,
    poly_remainder,
    poly_scale,
    signed_tuple,
)
from route_bd_case_c_radial_obstruction import (
    PARAMETERS,
    SP,
    bracket,
    constant_wpoly,
    p_exponents,
    q_exponents,
    solve_stage,
    wadd,
    wmultiply,
)
from route_bd_fbar_obstruction import (
    K,
    PRIME,
    outer_coefficients,
)


FACTOR_DATA = (
    (
        "rational factor 1",
        K(26839),
        {
            "norm4": (10393, 0, 0),
            "norm5": (6360, 0, 0),
            "gram": (9117, 0, 0),
            "wronskian": (-3053, 0, 0),
            "det_coefficient": (-6846, 0, 0),
        },
    ),
    (
        "rational factor 2",
        K(16621),
        {
            "norm4": (-14442, 0, 0),
            "norm5": (-6743, 0, 0),
            "gram": (-320, 0, 0),
            "wronskian": (10379, 0, 0),
            "det_coefficient": (14556, 0, 0),
        },
    ),
    (
        "cubic factor",
        K(0, 1),
        {
            "norm4": (9385, -9246, -3198),
            "norm5": (12016, -9857, 15351),
            "gram": (-2013, -13717, 1493),
            "wronskian": (7562, 8638, 10709),
            "det_coefficient": (7767, 11865, -11011),
        },
    ),
)


def nullspace(matrix: list[list[K]]) -> tuple[list[int], list[list[K]]]:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivots: list[int] = []
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
        work[pivot_row] = [
            coefficient * inverse for coefficient in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index]
                - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free = [
        column for column in range(column_count) if column not in pivots
    ]
    basis: list[list[K]] = []
    for free_column in free:
        vector = [K() for _ in range(column_count)]
        vector[free_column] = ONE
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row][free_column]
        basis.append(vector)
    return free, basis


def vector_poly(vector: list[K]) -> Poly:
    return {
        exponent: coefficient
        for exponent, coefficient in enumerate(vector)
        if coefficient
    }


def frobenius_row(column: Poly, modulus: Poly) -> list[K]:
    degree = max(modulus)
    return [
        poly_remainder(
            poly_multiply(column, {exponent: ONE}),
            modulus,
        ).get(degree - 1, K())
        for exponent in range(degree)
    ]


def dual_basis(columns: list[Poly], modulus: Poly) -> tuple[list[int], list[Poly]]:
    free, vectors = nullspace(
        [frobenius_row(column, modulus) for column in columns]
    )
    return free, [vector_poly(vector) for vector in vectors]


def derivative(polynomial: Poly) -> Poly:
    return {
        exponent - 1: exponent * coefficient
        for exponent, coefficient in polynomial.items()
        if exponent and exponent * coefficient
    }


def multiplication_matrix(element: Poly, modulus: Poly) -> list[list[K]]:
    degree = max(modulus)
    columns = [
        poly_remainder(
            poly_multiply(element, {exponent: ONE}),
            modulus,
        )
        for exponent in range(degree)
    ]
    return [
        [columns[column].get(row, K()) for column in range(degree)]
        for row in range(degree)
    ]


def algebra_trace(element: Poly, modulus: Poly) -> K:
    matrix = multiplication_matrix(element, modulus)
    return sum((matrix[index][index] for index in range(len(matrix))), K())


def algebra_norm(element: Poly, modulus: Poly) -> K:
    return determinant(multiplication_matrix(element, modulus))


def centered(element: Poly, modulus: Poly) -> Poly:
    trace = algebra_trace(element, modulus)
    return poly_add(element, {0: -trace / K(max(modulus))})


def subscale(polynomial: Poly, scalar: K, prefactor: K = ONE) -> Poly:
    return {
        exponent: prefactor * coefficient * scalar**exponent
        for exponent, coefficient in polynomial.items()
        if prefactor * coefficient * scalar**exponent
    }


def scaled_outer(
    u: Poly,
    v: Poly,
    scalar: K,
) -> tuple[Poly, Poly, Poly]:
    scaled_u = subscale(u, scalar)
    scaled_v = subscale(v, scalar)
    leading_ratio = scaled_v[10] ** 2 / scaled_u[7] ** 3
    quartic = poly_add(
        {
            exponent + 1: coefficient
            for exponent, coefficient in poly_multiply(
                scaled_v, scaled_v
            ).items()
        },
        poly_scale(poly_power(scaled_u, 3), -leading_ratio),
    )
    return scaled_u, scaled_v, quartic


def sp_remainder(dividend: dict[int, SP], divisor: Poly) -> dict[int, SP]:
    remainder = dict(dividend)
    divisor_degree = max(divisor)
    divisor_lead_inverse = divisor[divisor_degree].inverse()
    while remainder and max(remainder) >= divisor_degree:
        remainder_degree = max(remainder)
        shift = remainder_degree - divisor_degree
        factor = remainder[remainder_degree] * divisor_lead_inverse
        remainder = wadd(
            remainder,
            {
                exponent + shift: -factor * coefficient
                for exponent, coefficient in divisor.items()
            },
        )
    return remainder


def apply_adjoint(source: dict[int, SP], adjoint: Poly, modulus: Poly) -> SP:
    product = wmultiply(source, constant_wpoly(adjoint))
    return sp_remainder(product, modulus).get(19, SP())


def stage_source(
    p_blocks: dict[int, dict[int, SP]],
    q_blocks: dict[int, dict[int, SP]],
    output_degree: int,
) -> dict[int, SP]:
    source: dict[int, SP] = {}
    for left_degree, left in p_blocks.items():
        for right_degree, right in q_blocks.items():
            if left_degree + right_degree - 1 == output_degree:
                source = wadd(
                    source,
                    bracket(left_degree, left, right_degree, right),
                )
    return source


def source_cokernel_determinant(
    parameter: K,
    adjoint4: Poly,
    adjoint5: Poly,
    modulus5: Poly,
) -> tuple[SP, dict[str, SP]]:
    u_coefficients, v_coefficients = outer_coefficients(parameter)
    p_blocks = {
        2: constant_wpoly(
            {-1: ONE}
            | {
                index - 1: u_coefficients[index]
                for index in range(1, 8)
            }
        )
    }
    q_blocks = {
        3: constant_wpoly(
            {-1: ONE}
            | {
                index - 1: v_coefficients[index]
                for index in range(1, 11)
            }
        )
    }
    free_by_degree = {
        1: PARAMETERS[0:2],
        0: PARAMETERS[2:4],
        -1: PARAMETERS[4:6],
        -2: PARAMETERS[6:7],
    }
    values: dict[str, SP] = {}

    for p_degree in (1, 0, -1, -2, -3):
        q_degree = p_degree + 1
        source = stage_source(p_blocks, q_blocks, p_degree + 2)
        if p_degree == -2:
            values["t4"] = source.get(19, SP())
            values["r4"] = apply_adjoint(source, adjoint4, modulus5)
        if p_degree == -3:
            values["t5"] = source.get(19, SP())
            values["r5"] = apply_adjoint(source, adjoint5, modulus5)

        p_block, q_block, _constraints, _profile = solve_stage(
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

    determinant_polynomial = (
        values["t4"] * values["r5"]
        - values["r4"] * values["t5"]
    )
    return determinant_polynomial, values


def verify_factor(
    label: str,
    parameter: K,
    expected: dict[str, tuple[int, int, int]],
) -> dict[str, K]:
    u, v, quartic = outer_data(parameter)
    p2, q3 = outer_blocks(u, v)
    modulus5 = poly_power(quartic, 5)

    columns4, _, _ = operator_columns(4, p2, q3)
    columns5, _, _ = operator_columns(5, p2, q3)
    free4, basis4 = dual_basis(columns4, modulus5)
    free5, basis5 = dual_basis(columns5, modulus5)
    assert free4 == [0, 16]
    assert free5 == [0, 18, 19]

    assert basis4[0] == {0: ONE}
    assert basis5[0] == {0: ONE}
    adjoint4 = basis4[1]
    adjoint5 = basis5[1]
    assert max(adjoint4) == 16 and adjoint4[16] == ONE
    assert max(adjoint5) == 18 and adjoint5[18] == ONE
    assert not adjoint4.get(0, K())
    assert not adjoint5.get(0, K())
    assert not adjoint5.get(19, K())

    # The chosen two L5 representatives restrict independently to W5.
    restriction_rows = [
        frobenius_row({exponent: ONE}, modulus5)
        for exponent in range(1, 20)
    ]
    restriction_matrix = [
        [
            sum(
                (
                    row[index] * vector.get(index, K())
                    for index in range(20)
                ),
                K(),
            )
            for vector in ({0: ONE}, adjoint5)
        ]
        for row in restriction_rows
    ]
    assert matrix_rank(restriction_matrix) == 2

    # Exact scaling law under h -> 7h.
    scalar = K(7)
    scaled_u, scaled_v, scaled_quartic = scaled_outer(u, v, scalar)
    assert scaled_quartic == subscale(
        quartic, scalar, scalar.inverse()
    )
    scaled_p2, scaled_q3 = outer_blocks(scaled_u, scaled_v)
    scaled_modulus5 = poly_power(scaled_quartic, 5)
    _, scaled_basis4 = dual_basis(
        operator_columns(4, scaled_p2, scaled_q3)[0],
        scaled_modulus5,
    )
    _, scaled_basis5 = dual_basis(
        operator_columns(5, scaled_p2, scaled_q3)[0],
        scaled_modulus5,
    )
    assert scaled_basis4[1] == subscale(
        adjoint4, scalar, scalar**-16
    )
    assert scaled_basis5[1] == subscale(
        adjoint5, scalar, scalar**-18
    )

    g4 = poly_remainder(adjoint4, quartic)
    g5 = poly_remainder(adjoint5, quartic)
    x4 = centered(g4, quartic)
    x5 = centered(g5, quartic)
    assert not algebra_trace(x4, quartic)
    assert not algebra_trace(x5, quartic)

    trace44 = algebra_trace(poly_multiply(x4, x4), quartic)
    trace45 = algebra_trace(poly_multiply(x4, x5), quartic)
    trace55 = algebra_trace(poly_multiply(x5, x5), quartic)
    assert trace44 and trace55
    gram = trace44 * trace55 - trace45**2
    wronskian = poly_remainder(
        poly_add(
            poly_multiply(x4, derivative(x5)),
            poly_scale(poly_multiply(derivative(x4), x5), -ONE),
        ),
        quartic,
    )

    invariants = {
        "norm4": algebra_norm(x4, quartic),
        "norm5": algebra_norm(x5, quartic),
        "gram": gram,
        "wronskian": algebra_norm(wronskian, quartic),
    }
    for name, value in invariants.items():
        assert signed_tuple(value) == expected[name], (
            name,
            signed_tuple(value),
            expected[name],
        )
        assert value

    determinant_polynomial, values = source_cokernel_determinant(
        parameter,
        adjoint4,
        adjoint5,
        modulus5,
    )
    assert {
        name: value.term_count() for name, value in values.items()
    } == {"t4": 3, "r4": 3, "t5": 10, "r5": 32}
    assert values["t4"].weighted_degrees() == {4}
    assert values["r4"].weighted_degrees() == {4}
    assert values["t5"].weighted_degrees() == {5}
    assert values["r5"].weighted_degrees() == {5}
    assert determinant_polynomial.term_count() == 76
    assert determinant_polynomial.weighted_degrees() == {9}
    target_monomial = (5, 4, 0, 0, 0, 0, 0)
    determinant_coefficient = determinant_polynomial.terms[target_monomial]
    assert signed_tuple(determinant_coefficient) == expected[
        "det_coefficient"
    ]

    print(
        f"{label}: residual adjoint degrees 16,18; "
        f"(N4,N5,Gram,Wronskian)="
        f"{tuple(signed_tuple(invariants[name]) for name in invariants)}; "
        f"det coefficient {signed_tuple(determinant_coefficient)}"
    )
    return invariants | {"det_coefficient": determinant_coefficient}


def cubic_norm(value: K) -> K:
    result = value ** (PRIME**2 + PRIME + 1)
    assert not result.c1 and not result.c2
    return result


def main() -> None:
    results = [
        verify_factor(label, parameter, expected)
        for label, parameter, expected in FACTOR_DATA
    ]
    expected_total_norms = {
        "norm4": 11948,
        "norm5": 9339,
        "gram": 15804,
        "wronskian": 4832,
        "det_coefficient": -3257,
    }
    for name, expected_signed in expected_total_norms.items():
        total = results[0][name] * results[1][name] * cubic_norm(
            results[2][name]
        )
        signed = total.c0 if total.c0 <= PRIME // 2 else total.c0 - PRIME
        assert signed == expected_signed
        assert total
    print("case-c nonlinear cokernel pairing no-go checks passed")


if __name__ == "__main__":
    main()
