#!/usr/bin/env python3
"""Verify the outer-quartic adjoint/transvectant no-go.

The calculation is exact over the two rational and one cubic factors
of the certified outer Hurwitz algebra modulo 32003.
"""

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
    poly_multiply,
    poly_power,
    remainder_matrix,
    signed_tuple,
)
from route_bd_fbar_obstruction import K


FACTORS = (
    (
        "rational factor 1",
        K(26839),
        {
            4: (
                (-15118, 0, 0),
                (4149, 0, 0),
                (6224, 0, 0),
                (-13264, 0, 0),
            ),
            5: (
                (5862, 0, 0),
                (574, 0, 0),
                (1637, 0, 0),
                (-7634, 0, 0),
            ),
        },
        (-11441, 0, 0),
    ),
    (
        "rational factor 2",
        K(16621),
        {
            4: (
                (6356, 0, 0),
                (11610, 0, 0),
                (-6102, 0, 0),
                (-7721, 0, 0),
            ),
            5: (
                (-11106, 0, 0),
                (12957, 0, 0),
                (14206, 0, 0),
                (2100, 0, 0),
            ),
        },
        (6477, 0, 0),
    ),
    (
        "cubic factor",
        K(0, 1),
        {
            4: (
                (-3045, 2843, 11230),
                (4745, 7246, 562),
                (-14747, 1856, 7785),
                (-13464, 9604, -2707),
            ),
            5: (
                (11507, 9334, -14560),
                (-9388, -14360, 8299),
                (-5638, -12989, 10936),
                (-4378, -12647, -8654),
            ),
        },
        (-10846, 9591, 15152),
    ),
)


def coefficient_matrix(columns: list[Poly], exponents: range) -> list[list[K]]:
    return [
        [column.get(exponent, K()) for column in columns]
        for exponent in exponents
    ]


def monomial_columns(exponents: range) -> list[Poly]:
    return [{exponent: ONE} for exponent in exponents]


def bracket_top_coefficient(
    p_degree: int,
    p_exponent: int,
    q_degree: int,
    q_exponent: int,
) -> int:
    """Coefficient of h^(p_exponent+q_exponent) in the radial bracket."""

    return p_degree * q_exponent - q_degree * p_exponent


def verify_factor(
    label: str,
    parameter: K,
    expected_minors: dict[int, tuple[tuple[int, int, int], ...]],
    expected_combined_minor: tuple[int, int, int],
) -> None:
    u, v, quartic = outer_data(parameter)
    p2, q3 = outer_blocks(u, v)
    columns4, _, _ = operator_columns(4, p2, q3)
    columns5, _, _ = operator_columns(5, p2, q3)

    assert len(columns4) == 19
    assert len(columns5) == 17
    assert sorted(set().union(*(set(column) for column in columns4))) == list(
        range(19)
    )
    assert sorted(set().union(*(set(column) for column in columns5))) == list(
        range(1, 19)
    )

    modulus = {0: ONE}
    for jet_length in range(1, 6):
        modulus = poly_multiply(modulus, quartic)
        expected_dimension = 4 * jet_length
        ranks = {}
        for deficit, columns in ((4, columns4), (5, columns5)):
            matrix = remainder_matrix(columns, modulus)
            rank = matrix_rank(matrix)
            ranks[deficit] = rank
            if jet_length <= 4:
                assert rank == expected_dimension
                minor = determinant(
                    [row[:expected_dimension] for row in matrix]
                )
                assert signed_tuple(minor) == expected_minors[deficit][
                    jet_length - 1
                ]
        if jet_length == 5:
            assert ranks == {4: 18, 5: 17}

    quartic_fifth = poly_power(quartic, 5)

    # Degree < 20 polynomials identify with k[h]/(E^5).
    w4_basis = monomial_columns(range(20))
    w5_basis = monomial_columns(range(1, 20))
    assert matrix_rank(remainder_matrix(w4_basis, quartic_fifth)) == 20
    assert matrix_rank(remainder_matrix(w5_basis, quartic_fifth)) == 19

    # Both images together fill every coefficient through h^18.
    combined = columns4 + columns5
    combined_matrix = coefficient_matrix(combined, range(19))
    assert matrix_rank(combined_matrix) == 19

    # Columns 0,...,16,18 of L4 and column 6 of L5 give a common
    # nonzero 19x19 minor.  Column 6 is the first B-column of L5.
    selected = list(range(17)) + [18] + [len(columns4) + 6]
    combined_minor = determinant(
        [[row[column] for column in selected] for row in combined_matrix]
    )
    assert signed_tuple(combined_minor) == expected_combined_minor

    # Every new-block column has zero h^19 coefficient.
    assert all(not column.get(19, K()) for column in combined)

    print(
        f"{label}: E^j ranks are 4j through j=4; "
        "E^5 ranks (18,17); combined rank 19; "
        f"minor {signed_tuple(combined_minor)}"
    )


def verify_top_source_formulas() -> None:
    # Deficit four:
    # [p_1,q_0] contributes 12 at exponents (7,12);
    # [p_0,q_1] contributes -8 at exponents (8,11);
    # [p_-1,q_2] has maximum exponent 18.
    assert bracket_top_coefficient(1, 7, 0, 12) == 12
    assert bracket_top_coefficient(0, 8, 1, 11) == -8
    assert 8 + 10 == 18

    # Deficit five:
    # [p_1,q_-1] and [p_-1,q_1] give the two h^19 terms.
    # [p_0,q_0] vanishes identically and [p_-2,q_2] stops at h^18.
    assert bracket_top_coefficient(1, 7, -1, 12) == 19
    assert bracket_top_coefficient(-1, 8, 1, 11) == -19
    assert bracket_top_coefficient(0, 8, 0, 12) == 0
    assert 8 + 10 == 18


def main() -> None:
    for data in FACTORS:
        verify_factor(*data)
    verify_top_source_formulas()
    print("case-c outer-quartic adjoint no-go checks passed")


if __name__ == "__main__":
    main()
