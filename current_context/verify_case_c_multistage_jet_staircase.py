#!/usr/bin/env python3
"""Verify the case-c multistage quartic-jet staircase.

This is a bounded, theorem-driven audit.  It does not run the full
case-c Groebner certificate.  It checks:

* the ranks of every later new-block operator modulo E^j;
* the first genuinely three-stage trace discriminant for deficits 4,5,6;
* the unique deficit-eight E^3-adjoint; and
* its nonzero value on the pure weight-four mode X6.
"""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from current_context.verify_case_c_cokernel_nonlinear_pairing_no_go import (
    FACTOR_DATA,
    algebra_norm,
    algebra_trace,
    centered,
    cubic_norm,
    dual_basis,
    scaled_outer,
    sp_remainder,
    stage_source,
    subscale,
)
from current_context.verify_case_c_outer_quartic_cokernel_no_go import (
    ONE,
    determinant,
    matrix_rank,
    operator_columns,
    outer_blocks,
    outer_data,
    poly_multiply,
    poly_power,
    poly_remainder,
    remainder_matrix,
    signed_tuple,
)
from route_bd_case_c_radial_obstruction import (
    PARAMETERS,
    SP,
    constant_wpoly,
    p_exponents,
    q_exponents,
    solve_stage,
    wmultiply,
)
from route_bd_fbar_obstruction import K, PRIME, outer_coefficients


EFFECTIVE_RANKS = {
    4: 18,
    5: 17,
    6: 15,
    7: 13,
    8: 11,
    9: 9,
    10: 7,
    11: 5,
    12: 4,
    13: 3,
    14: 2,
    15: 1,
}

EXPECTED = {
    "rational factor 1": {
        "triple_gram": (1894, 0, 0),
        "norm6": (-222, 0, 0),
        "deficit8_x6_square": (-1952, 0, 0),
    },
    "rational factor 2": {
        "triple_gram": (659, 0, 0),
        "norm6": (-1771, 0, 0),
        "deficit8_x6_square": (10399, 0, 0),
    },
    "cubic factor": {
        "triple_gram": (-1130, -8574, -5288),
        "norm6": (6161, 11890, 12835),
        "deficit8_x6_square": (7227, 10262, 13596),
    },
}


def pure_x6_restriction(polynomial: SP) -> SP:
    """Set X0,...,X5 to zero without changing the coefficient field."""

    return SP(
        terms={
            monomial: coefficient
            for monomial, coefficient in polynomial.terms.items()
            if not any(monomial[:6])
        }
    )


def source_through_deficit_eight(
    parameter: K,
) -> tuple[dict[int, SP], tuple[SP, ...]]:
    """Solve only the seven preceding stages and return the stage-8 source."""

    u, v = outer_coefficients(parameter)
    p_blocks = {
        2: constant_wpoly(
            {-1: ONE}
            | {index - 1: u[index] for index in range(1, 8)}
        )
    }
    q_blocks = {
        3: constant_wpoly(
            {-1: ONE}
            | {index - 1: v[index] for index in range(1, 11)}
        )
    }
    free_by_degree = {
        1: PARAMETERS[0:2],
        0: PARAMETERS[2:4],
        -1: PARAMETERS[4:6],
        -2: PARAMETERS[6:7],
    }
    preceding_constraints: list[SP] = []

    for deficit, p_degree in enumerate(range(1, -7, -1), start=1):
        q_degree = p_degree + 1
        source = stage_source(p_blocks, q_blocks, p_degree + 2)
        if deficit == 8:
            return source, tuple(preceding_constraints)

        p_block, q_block, constraints, _profile = solve_stage(
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
        preceding_constraints.extend(constraints)

    raise AssertionError("deficit eight was not reached")


def apply_jet_adjoint(
    source: dict[int, SP],
    adjoint: dict[int, K],
    modulus: dict[int, K],
) -> SP:
    degree = max(modulus)
    product = wmultiply(source, constant_wpoly(adjoint))
    return sp_remainder(product, modulus).get(degree - 1, SP())


def verify_rank_staircase(
    quartic: dict[int, K],
    p2: dict[int, K],
    q3: dict[int, K],
) -> None:
    for deficit, effective_rank in EFFECTIVE_RANKS.items():
        columns, _, _ = operator_columns(deficit, p2, q3)
        modulus = {0: ONE}
        for jet_length in range(1, 7):
            modulus = poly_multiply(modulus, quartic)
            rank = matrix_rank(remainder_matrix(columns, modulus))
            assert rank == min(4 * jet_length, effective_rank)


def verify_factor(label: str, parameter: K) -> dict[str, K]:
    expected = EXPECTED[label]
    u, v, quartic = outer_data(parameter)
    p2, q3 = outer_blocks(u, v)
    verify_rank_staircase(quartic, p2, q3)

    modulus5 = poly_power(quartic, 5)
    free4, basis4 = dual_basis(
        operator_columns(4, p2, q3)[0], modulus5
    )
    free5, basis5 = dual_basis(
        operator_columns(5, p2, q3)[0], modulus5
    )
    assert free4 == [0, 16]
    assert free5 == [0, 18, 19]

    modulus4 = poly_power(quartic, 4)
    free6, basis6 = dual_basis(
        operator_columns(6, p2, q3)[0], modulus4
    )
    assert free6 == [15]
    assert len(basis6) == 1
    assert max(basis6[0]) == 15 and basis6[0][15] == ONE

    x4, x5, x6 = (
        centered(poly_remainder(adjoint, quartic), quartic)
        for adjoint in (basis4[1], basis5[1], basis6[0])
    )
    trace_gram = [
        [
            algebra_trace(poly_multiply(left, right), quartic)
            for right in (x4, x5, x6)
        ]
        for left in (x4, x5, x6)
    ]
    triple_gram = determinant(trace_gram)
    norm6 = algebra_norm(x6, quartic)
    assert signed_tuple(triple_gram) == expected["triple_gram"]
    assert signed_tuple(norm6) == expected["norm6"]

    # The degree-filtered deficit-six line is natural under h -> 7h.
    scalar = K(7)
    scaled_u, scaled_v, scaled_quartic = scaled_outer(u, v, scalar)
    scaled_p2, scaled_q3 = outer_blocks(scaled_u, scaled_v)
    _, scaled_basis6 = dual_basis(
        operator_columns(6, scaled_p2, scaled_q3)[0],
        poly_power(scaled_quartic, 4),
    )
    assert scaled_basis6[0] == subscale(
        basis6[0], scalar, scalar**-15
    )

    # Deficit eight is the first stage whose operator has a unique
    # E^3-adjoint.  Pair it with the exact stage-eight source.
    modulus3 = poly_power(quartic, 3)
    free8, basis8 = dual_basis(
        operator_columns(8, p2, q3)[0], modulus3
    )
    assert free8 == [11]
    assert len(basis8) == 1
    assert max(basis8[0]) == 11 and basis8[0][11] == ONE

    source8, preceding_constraints = source_through_deficit_eight(
        parameter
    )
    assert all(
        not pure_x6_restriction(constraint)
        for constraint in preceding_constraints
    )
    terminal_scalar = apply_jet_adjoint(source8, basis8[0], modulus3)
    pure_terminal = pure_x6_restriction(terminal_scalar)
    target_monomial = (0, 0, 0, 0, 0, 0, 2)
    assert set(pure_terminal.terms) == {target_monomial}
    coefficient = pure_terminal.terms[target_monomial]
    assert signed_tuple(coefficient) == expected["deficit8_x6_square"]

    scaled_modulus3 = poly_power(scaled_quartic, 3)
    _, scaled_basis8 = dual_basis(
        operator_columns(8, scaled_p2, scaled_q3)[0],
        scaled_modulus3,
    )
    assert scaled_basis8[0] == subscale(
        basis8[0], scalar, scalar**-11
    )

    print(
        f"{label}: maximal E^j rank staircase; "
        f"triple Gram {signed_tuple(triple_gram)}; "
        f"deficit-8 X6^2 coefficient {signed_tuple(coefficient)}"
    )
    return {
        "triple_gram": triple_gram,
        "norm6": norm6,
        "deficit8_x6_square": coefficient,
    }


def main() -> None:
    results = [
        verify_factor(label, parameter)
        for label, parameter, _old_expected in FACTOR_DATA
    ]
    expected_total_norms = {
        "triple_gram": -15416,
        "norm6": -1785,
        "deficit8_x6_square": -9989,
    }
    for name, expected in expected_total_norms.items():
        total = results[0][name] * results[1][name] * cubic_norm(
            results[2][name]
        )
        assert not total.c1 and not total.c2
        signed = (
            total.c0
            if total.c0 <= PRIME // 2
            else total.c0 - PRIME
        )
        assert signed == expected
        assert total
    print("case-c multistage jet staircase checks passed")


if __name__ == "__main__":
    main()
