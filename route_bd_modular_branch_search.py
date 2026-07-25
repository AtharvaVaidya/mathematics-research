#!/usr/bin/env python3
"""Finite-field search for the full GGHV a/b (25+47) branch.

This file is intentionally separate from ``route_bd_verify.py``.  It performs
three exact tasks:

1. Rewrites the 92 coefficient rows using z=x*y^2 and w=y^(-1):

       P=A(z)+B(z)w+C(z)w^2,
       Q=D(z)+E(z)w+F(z)w^2+G(z)w^3.

   Since dx wedge dy = -dz wedge dw, [P,Q]_xy=x^2 is equivalent
   to [P,Q]_(z,w)=-z^2*w^4.  Equating powers of w gives the five
   polynomial identities returned by ``block_equations``.

2. Exhausts every normalized top-block solution over F_5 or F_7.  Normalization
   C_1=1 loses no solutions because (C,G) -> (lambda*C,G/lambda)
   preserves 3*C'*G-2*C*G'.  The search retains C_8,G_2,G_12 != 0.

3. For every retained (C,G), solves the w^3 and w^2 blocks by exact
   modular row reduction, exhausts their affine solution spaces up to a
   configurable dimension bound, and tests the final w^1,w^0 blocks.

The result is either an explicit finite-field solution with all eight polygon vertices
nonzero, or a rigorously exhaustive obstruction for every top pair whose two
intermediate affine dimensions do not exceed ``--max-affine-dimension``.
The default bound is high enough for the dimensions encountered in the current
F_5 and F_7 runs, but the program reports any skipped slice and never calls a partial
search exhaustive.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator, Sequence


P = 5
POLY_ROWS = 20  # degrees 0,...,19 cover every transformed block


def verify_support_reconstruction() -> None:
    """Verify the 25+47 supports and all 975 nonzero terms exactly.

    A transformed monomial z^u*w^k is x^u*y^(2u-k).  For two such
    monomials the transformed determinant is u*l-k*i, while the original
    x,y determinant is its negative.  The output rows are related by
    (r,s)_zw -> (r,2*r-s)_xy.  Checking every monomial pair proves that
    the five blocks below are precisely the original 92-row system, not
    merely a sampled comparison.
    """
    p_monomials = tuple(
        [(degree, 0) for degree in range(0, 9)]
        + [(degree, 1) for degree in range(1, 9)]
        + [(degree, 2) for degree in range(1, 9)]
    )
    q_monomials = tuple(
        [(degree, 0) for degree in range(0, 13)]
        + [(degree, 1) for degree in range(1, 13)]
        + [(degree, 2) for degree in range(2, 13)]
        + [(degree, 3) for degree in range(2, 13)]
    )
    assert len(p_monomials) == 25
    assert len(q_monomials) == 47
    rows: set[tuple[int, int]] = set()
    term_count = 0
    for u, k in p_monomials:
        p_xy = (u, 2 * u - k)
        for i, ell in q_monomials:
            q_xy = (i, 2 * i - ell)
            transformed_determinant = u * ell - k * i
            original_determinant = (
                p_xy[0] * q_xy[1] - p_xy[1] * q_xy[0]
            )
            assert original_determinant == -transformed_determinant
            if not transformed_determinant:
                continue
            transformed_row = (u + i - 1, k + ell - 1)
            original_row = (
                p_xy[0] + q_xy[0] - 1,
                p_xy[1] + q_xy[1] - 1,
            )
            assert original_row == (
                transformed_row[0],
                2 * transformed_row[0] - transformed_row[1],
            )
            rows.add(original_row)
            term_count += 1
    assert len(rows) == 92
    assert term_count == 975
    # x^2 = z^2*w^4, and the sign flips between the two brackets.
    assert (2, 2 * 2 - 4) == (2, 0)


def add(*polynomials: Sequence[int], modulus: int = P) -> list[int]:
    size = max((len(poly) for poly in polynomials), default=0)
    result = [0] * size
    for poly in polynomials:
        for index, coefficient in enumerate(poly):
            result[index] = (result[index] + coefficient) % modulus
    return result


def scale(poly: Sequence[int], scalar: int, modulus: int = P) -> list[int]:
    return [(scalar * coefficient) % modulus for coefficient in poly]


def derivative(poly: Sequence[int], modulus: int = P) -> list[int]:
    return [
        (degree * poly[degree]) % modulus
        for degree in range(1, len(poly))
    ]


def multiply(
    left: Sequence[int], right: Sequence[int], modulus: int = P
) -> list[int]:
    if not left or not right:
        return []
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        if not left_coefficient:
            continue
        for right_degree, right_coefficient in enumerate(right):
            result[left_degree + right_degree] = (
                result[left_degree + right_degree]
                + left_coefficient * right_coefficient
            ) % modulus
    return result


def pad(poly: Sequence[int], size: int = POLY_ROWS) -> list[int]:
    assert len(poly) <= size
    return list(poly) + [0] * (size - len(poly))


def block_equations(
    A: Sequence[int],
    B: Sequence[int],
    C: Sequence[int],
    D: Sequence[int],
    E: Sequence[int],
    F: Sequence[int],
    G: Sequence[int],
    modulus: int = P,
) -> tuple[list[int], ...]:
    """Return coefficients of [P,Q]_(z,w), from w^0 through w^4."""
    Ap, Bp, Cp = (
        derivative(A, modulus),
        derivative(B, modulus),
        derivative(C, modulus),
    )
    Dp, Ep, Fp, Gp = (
        derivative(D, modulus),
        derivative(E, modulus),
        derivative(F, modulus),
        derivative(G, modulus),
    )
    return (
        add(
            multiply(Ap, E, modulus),
            scale(multiply(B, Dp, modulus), -1, modulus),
            modulus=modulus,
        ),
        add(
            scale(multiply(Ap, F, modulus), 2, modulus),
            multiply(Bp, E, modulus),
            scale(multiply(B, Ep, modulus), -1, modulus),
            scale(multiply(C, Dp, modulus), -2, modulus),
            modulus=modulus,
        ),
        add(
            scale(multiply(Ap, G, modulus), 3, modulus),
            scale(multiply(Bp, F, modulus), 2, modulus),
            multiply(Cp, E, modulus),
            scale(multiply(B, Fp, modulus), -1, modulus),
            scale(multiply(C, Ep, modulus), -2, modulus),
            modulus=modulus,
        ),
        add(
            scale(multiply(Bp, G, modulus), 3, modulus),
            scale(multiply(Cp, F, modulus), 2, modulus),
            scale(multiply(B, Gp, modulus), -1, modulus),
            scale(multiply(C, Fp, modulus), -2, modulus),
            modulus=modulus,
        ),
        add(
            scale(multiply(Cp, G, modulus), 3, modulus),
            scale(multiply(C, Gp, modulus), -2, modulus),
            modulus=modulus,
        ),
    )


def top_block(C: Sequence[int], G: Sequence[int], modulus: int = P) -> list[int]:
    return add(
        scale(multiply(derivative(C, modulus), G, modulus), 3, modulus),
        scale(multiply(C, derivative(G, modulus), modulus), -2, modulus),
        modulus=modulus,
    )


def stage_one_block(
    B: Sequence[int],
    C: Sequence[int],
    F: Sequence[int],
    G: Sequence[int],
    modulus: int = P,
) -> list[int]:
    return add(
        scale(multiply(derivative(B, modulus), G, modulus), 3, modulus),
        scale(multiply(derivative(C, modulus), F, modulus), 2, modulus),
        scale(multiply(B, derivative(G, modulus), modulus), -1, modulus),
        scale(multiply(C, derivative(F, modulus), modulus), -2, modulus),
        modulus=modulus,
    )


def stage_two_block(
    A: Sequence[int],
    B: Sequence[int],
    C: Sequence[int],
    E: Sequence[int],
    F: Sequence[int],
    G: Sequence[int],
    modulus: int = P,
) -> list[int]:
    return add(
        scale(multiply(derivative(A, modulus), G, modulus), 3, modulus),
        scale(multiply(derivative(B, modulus), F, modulus), 2, modulus),
        multiply(derivative(C, modulus), E, modulus),
        scale(multiply(B, derivative(F, modulus), modulus), -1, modulus),
        scale(multiply(C, derivative(E, modulus), modulus), -2, modulus),
        modulus=modulus,
    )


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int], modulus: int = P
) -> tuple[list[int], list[int]]:
    num = list(numerator)
    while num and num[-1] % modulus == 0:
        num.pop()
    den = list(denominator)
    while den and den[-1] % modulus == 0:
        den.pop()
    if not den:
        raise ZeroDivisionError("zero polynomial")
    if len(num) < len(den):
        return [], num
    quotient = [0] * (len(num) - len(den) + 1)
    inverse_lead = pow(den[-1], -1, modulus)
    while len(num) >= len(den):
        degree = len(num) - len(den)
        coefficient = num[-1] * inverse_lead % modulus
        quotient[degree] = coefficient
        for index, den_coefficient in enumerate(den):
            num[degree + index] = (
                num[degree + index] - coefficient * den_coefficient
            ) % modulus
        while num and num[-1] == 0:
            num.pop()
    return quotient, num


@dataclass(frozen=True)
class AffineSolution:
    particular: tuple[int, ...]
    basis: tuple[tuple[int, ...], ...]

    @property
    def dimension(self) -> int:
        return len(self.basis)

    def vectors(self, modulus: int = P) -> Iterator[tuple[int, ...]]:
        for parameters in product(range(modulus), repeat=self.dimension):
            vector = list(self.particular)
            for parameter, basis_vector in zip(parameters, self.basis):
                if not parameter:
                    continue
                for index, coefficient in enumerate(basis_vector):
                    vector[index] = (
                        vector[index] + parameter * coefficient
                    ) % modulus
            yield tuple(vector)


class LinearSolver:
    """Reusable exact solver for M*x=rhs over a prime field."""

    def __init__(self, columns: Sequence[Sequence[int]], modulus: int = P):
        self.modulus = modulus
        self.row_count = len(columns[0]) if columns else 0
        self.column_count = len(columns)
        matrix = [
            [columns[column][row] % modulus for column in range(len(columns))]
            for row in range(self.row_count)
        ]
        transform = [
            [int(row == column) for column in range(self.row_count)]
            for row in range(self.row_count)
        ]
        pivots: list[int] = []
        pivot_row = 0
        for column in range(self.column_count):
            selected = next(
                (
                    row
                    for row in range(pivot_row, self.row_count)
                    if matrix[row][column]
                ),
                None,
            )
            if selected is None:
                continue
            matrix[pivot_row], matrix[selected] = (
                matrix[selected],
                matrix[pivot_row],
            )
            transform[pivot_row], transform[selected] = (
                transform[selected],
                transform[pivot_row],
            )
            inverse = pow(matrix[pivot_row][column], -1, modulus)
            matrix[pivot_row] = [
                value * inverse % modulus for value in matrix[pivot_row]
            ]
            transform[pivot_row] = [
                value * inverse % modulus for value in transform[pivot_row]
            ]
            for row in range(self.row_count):
                if row == pivot_row or not matrix[row][column]:
                    continue
                factor = matrix[row][column]
                matrix[row] = [
                    (value - factor * pivot_value) % modulus
                    for value, pivot_value in zip(
                        matrix[row], matrix[pivot_row]
                    )
                ]
                transform[row] = [
                    (value - factor * pivot_value) % modulus
                    for value, pivot_value in zip(
                        transform[row], transform[pivot_row]
                    )
                ]
            pivots.append(column)
            pivot_row += 1
            if pivot_row == self.row_count:
                break
        self.rref = matrix
        self.transform = transform
        self.pivots = tuple(pivots)
        self.rank = len(pivots)
        free = [column for column in range(self.column_count) if column not in pivots]
        basis = []
        for free_column in free:
            vector = [0] * self.column_count
            vector[free_column] = 1
            for row, pivot_column in enumerate(pivots):
                vector[pivot_column] = -matrix[row][free_column] % modulus
            basis.append(tuple(vector))
        self.nullspace = tuple(basis)

    def solve(self, rhs: Sequence[int]) -> AffineSolution | None:
        assert len(rhs) == self.row_count
        transformed_rhs = [
            sum(coefficient * value for coefficient, value in zip(row, rhs))
            % self.modulus
            for row in self.transform
        ]
        if any(transformed_rhs[row] for row in range(self.rank, self.row_count)):
            return None
        particular = [0] * self.column_count
        for row, pivot_column in enumerate(self.pivots):
            particular[pivot_column] = transformed_rhs[row]
        return AffineSolution(tuple(particular), self.nullspace)


def fixed_p_rank_certificate(
    modulus: int, C: Sequence[int]
) -> tuple[
    dict[tuple[int, int], int],
    int,
    tuple[tuple[tuple[int, int], int], ...],
]:
    """Give a sparse left-kernel certificate for one full-polygon fixed P.

    Take A=1+z^8 and B=0, together with the supplied top-compatible C.
    All four P vertices are nonzero.  The returned covector lambda obeys

        lambda^T M(P) = 0,   lambda^T e_(2,0) = 1,

    so rank([M(P)|e])=rank(M(P))+1 and no Q at all can solve the bracket
    equation for this P.  This is a full-support fixed-P obstruction, not
    the forced-edge degeneration from the earlier memo.
    """
    p_specs = tuple(
        [(degree, 0) for degree in range(0, 9)]
        + [(degree, 1) for degree in range(1, 9)]
        + [(degree, 2) for degree in range(1, 9)]
    )
    q_specs = tuple(
        [(degree, 0) for degree in range(0, 13)]
        + [(degree, 1) for degree in range(1, 13)]
        + [(degree, 2) for degree in range(2, 13)]
        + [(degree, 3) for degree in range(2, 13)]
    )
    p_support_xy = tuple((u, 2 * u - k) for u, k in p_specs)
    q_support_xy = tuple((i, 2 * i - ell) for i, ell in q_specs)
    rows = sorted(
        {
            (u + i - 1, v + j - 1)
            for u, v in p_support_xy
            for i, j in q_support_xy
            if u * j - v * i
        }
    )
    assert len(rows) == 92

    p_coefficients: dict[tuple[int, int], int] = {
        (0, 0): 1,
        (8, 16): 1,
    }
    for degree, coefficient in enumerate(C):
        if coefficient:
            p_coefficients[(degree, 2 * degree - 2)] = (
                coefficient % modulus
            )
    assert all(
        p_coefficients.get(vertex)
        for vertex in ((0, 0), (1, 0), (8, 14), (8, 16))
    )

    columns = []
    for i, j in q_support_xy:
        column = []
        for row in rows:
            coefficient = sum(
                (u * j - v * i) * p_coefficient
                for (u, v), p_coefficient in p_coefficients.items()
                if (u + i - 1, v + j - 1) == row
            )
            column.append(coefficient % modulus)
        columns.append(column)
    solver = LinearSolver(columns, modulus)
    rhs = [int(row == (2, 0)) for row in rows]
    transformed_rhs = [
        sum(coefficient * value for coefficient, value in zip(row, rhs))
        % modulus
        for row in solver.transform
    ]
    inconsistent_row = next(
        row
        for row in range(solver.rank, len(rows))
        if transformed_rhs[row]
    )
    inverse_pairing = pow(
        transformed_rhs[inconsistent_row], -1, modulus
    )
    covector = tuple(
        coefficient * inverse_pairing % modulus
        for coefficient in solver.transform[inconsistent_row]
    )
    assert all(
        sum(covector[row] * columns[column][row] for row in range(len(rows)))
        % modulus
        == 0
        for column in range(len(columns))
    )
    assert sum(
        covector[row] * rhs[row] for row in range(len(rows))
    ) % modulus == 1
    sparse_covector = tuple(
        (row, covector[index])
        for index, row in enumerate(rows)
        if covector[index]
    )
    return p_coefficients, solver.rank, sparse_covector


def linear_columns(
    variable_specs: Sequence[tuple[str, int]],
    evaluator,
    lengths: dict[str, int],
) -> list[list[int]]:
    columns = []
    for name, degree in variable_specs:
        values = {key: [0] * length for key, length in lengths.items()}
        values[name][degree] = 1
        columns.append(pad(evaluator(**values)))
    return columns


def enumerate_top_pairs_p5() -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Exhaust normalized C,G satisfying the w^4 equation over F_5.

    Put C=z*c and G=z^2*g.  At z^n the equation becomes

        sum_(i+j=n) (1-3*i+2*j)c_i*g_j = delta_(n,0).

    Modulo 5 the weight is 1+2*n, independent of i.  Thus c*g has
    coefficient one at n=0, coefficient zero except at n=2,7,12,17,
    and no condition in those four exceptional degrees.  With c_0=1,
    g_0=1; g_2 and g_7 are the only free coefficients through degree 10.
    """
    for tail in product(range(5), repeat=7):
        c = (1,) + tail
        if not c[7]:  # C_8 != 0
            continue
        for g2 in range(5):
            for g7 in range(5):
                g = [0] * 11
                g[0] = 1
                g[2] = g2
                g[7] = g7
                for degree in range(1, 11):
                    if degree in (2, 7):
                        continue
                    g[degree] = -sum(
                        c[index] * g[degree - index]
                        for index in range(1, min(7, degree) + 1)
                    ) % 5
                if not g[10]:  # G_12 != 0
                    continue
                if any(
                    sum(
                        c[index] * g[degree - index]
                        for index in range(
                            max(0, degree - 10), min(7, degree) + 1
                        )
                    )
                    % 5
                    for degree in (11, 13, 14, 15, 16)
                ):
                    continue
                C = (0,) + c
                G = (0, 0) + tuple(g)
                target = [0, 0, -1 % 5]
                assert pad(top_block(C, G)) == pad(target)
                yield C, G


def enumerate_top_pairs_p7() -> Iterator[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Exhaust normalized C,G satisfying the w^4 equation over F_7.

    The coefficient of g_n in the triangular recurrence is 1+2*n.
    It vanishes at n=3,10.  Those two rows become constraints and g_3,g_10
    are free.  The loops below cover all 7^7 normalized c-polynomials and
    every value of the two free coefficients; g_10 is restricted to be
    nonzero because it is the required G_12 vertex.
    """
    modulus = 7
    inverses = [0] + [
        pow(coefficient, -1, modulus) for coefficient in range(1, modulus)
    ]
    for tail in product(range(modulus), repeat=7):
        c = (1,) + tail
        if not c[7]:
            continue
        initial_g = [0] * 11
        initial_g[0] = 1
        for degree in (1, 2):
            residual = sum(
                (1 + 2 * degree - 5 * index)
                * c[index]
                * initial_g[degree - index]
                for index in range(1, min(7, degree) + 1)
            ) % modulus
            initial_g[degree] = (
                -residual * inverses[(1 + 2 * degree) % modulus]
            ) % modulus
        degree = 3
        if (
            sum(
                (1 + 2 * degree - 5 * index)
                * c[index]
                * initial_g[degree - index]
                for index in range(1, min(7, degree) + 1)
            )
            % modulus
        ):
            continue
        for g3 in range(modulus):
            g = initial_g[:]
            g[3] = g3
            for degree in range(4, 10):
                residual = sum(
                    (1 + 2 * degree - 5 * index)
                    * c[index]
                    * g[degree - index]
                    for index in range(1, min(7, degree) + 1)
                ) % modulus
                g[degree] = (
                    -residual * inverses[(1 + 2 * degree) % modulus]
                ) % modulus
            degree = 10
            if (
                sum(
                    (1 + 2 * degree - 5 * index)
                    * c[index]
                    * g[degree - index]
                    for index in range(1, 8)
                )
                % modulus
            ):
                continue
            for g10 in range(1, modulus):
                g[10] = g10
                if any(
                    sum(
                        (1 + 2 * degree - 5 * index)
                        * c[index]
                        * g[degree - index]
                        for index in range(
                            max(0, degree - 10), min(7, degree) + 1
                        )
                    )
                    % modulus
                    for degree in range(11, 18)
                ):
                    continue
                C = (0,) + c
                G = (0, 0) + tuple(g)
                target = [0, 0, -1 % modulus]
                assert pad(top_block(C, G, modulus)) == pad(target)
                yield C, G


def make_stage_one_solver(
    C: Sequence[int], G: Sequence[int], modulus: int = P
) -> tuple[LinearSolver, tuple[tuple[str, int], ...]]:
    specs = tuple(
        [("B", degree) for degree in range(1, 9)]
        + [("F", degree) for degree in range(2, 13)]
    )
    columns = linear_columns(
        specs,
        lambda B, F: stage_one_block(B, C, F, G, modulus),
        {"B": 9, "F": 13},
    )
    return LinearSolver(columns, modulus), specs


def make_stage_two_solver(
    C: Sequence[int], G: Sequence[int], modulus: int = P
) -> tuple[LinearSolver, tuple[tuple[str, int], ...]]:
    specs = tuple(
        [("A", degree) for degree in range(1, 9)]
        + [("E", degree) for degree in range(1, 13)]
    )
    columns = linear_columns(
        specs,
        lambda A, E: add(
            scale(
                multiply(
                    derivative(A, modulus), G, modulus
                ),
                3,
                modulus,
            ),
            multiply(derivative(C, modulus), E, modulus),
            scale(
                multiply(C, derivative(E, modulus), modulus),
                -2,
                modulus,
            ),
            modulus=modulus,
        ),
        {"A": 9, "E": 13},
    )
    return LinearSolver(columns, modulus), specs


def unpack(
    vector: Sequence[int],
    specs: Sequence[tuple[str, int]],
    lengths: dict[str, int],
) -> dict[str, list[int]]:
    values = {name: [0] * length for name, length in lengths.items()}
    for coefficient, (name, degree) in zip(vector, specs):
        values[name][degree] = coefficient
    return values


def recover_D_prime(
    A: Sequence[int],
    B: Sequence[int],
    C: Sequence[int],
    E: Sequence[int],
    F: Sequence[int],
) -> list[int] | None:
    # w^1: 2*A'*F+B'*E-B*E'-2*C*D'=0.
    numerator = add(
        scale(multiply(derivative(A), F), 2),
        multiply(derivative(B), E),
        scale(multiply(B, derivative(E)), -1),
    )
    quotient, remainder = poly_divmod(numerator, scale(C, 2))
    if remainder:
        return None
    quotient += [0] * (12 - len(quotient))
    if len(quotient) > 12:
        return None
    # D' has degree <=11.  In characteristic 5, z^4 and z^9 cannot
    # occur in a derivative.  Coefficients D_5,D_10 are otherwise free.
    if quotient[4] or quotient[9]:
        return None
    return quotient


def w1_numerator(
    A: Sequence[int],
    B: Sequence[int],
    E: Sequence[int],
    F: Sequence[int],
    modulus: int = P,
) -> list[int]:
    """Return 2*A'*F+B'*E-B*E', the numerator that must equal 2*C*D'."""
    return add(
        scale(
            multiply(derivative(A, modulus), F, modulus), 2, modulus
        ),
        multiply(derivative(B, modulus), E, modulus),
        scale(
            multiply(B, derivative(E, modulus), modulus), -1, modulus
        ),
        modulus=modulus,
    )


def solve_w1_on_stage_two_affine_space(
    stage_two: AffineSolution,
    stage_two_specs: Sequence[tuple[str, int]],
    B: Sequence[int],
    C: Sequence[int],
    F: Sequence[int],
    modulus: int = P,
) -> tuple[
    AffineSolution,
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
] | None:
    """Intersect an affine w^2 solution space with the linear w^1 block.

    Enumerating all 5^4 stage-two vectors dominated the original search.
    Instead, use its affine parameters together with the ten derivative
    coefficients D'_k allowed in characteristic 5.  The resulting system
    has at most 14 variables and exactly represents the same candidates.

    The return value contains the parameter/D' affine solution, the packed
    stage-two particular vector and basis, and the ordered allowed degrees
    of D'.
    """
    particular_values = unpack(
        stage_two.particular, stage_two_specs, {"A": 9, "E": 13}
    )
    particular_numerator = pad(
        w1_numerator(
            particular_values["A"],
            B,
            particular_values["E"],
            F,
            modulus,
        )
    )

    columns: list[list[int]] = []
    for packed_basis in stage_two.basis:
        values = unpack(packed_basis, stage_two_specs, {"A": 9, "E": 13})
        columns.append(
            pad(w1_numerator(values["A"], B, values["E"], F, modulus))
        )

    allowed_degrees = tuple(
        degree
        for degree in range(12)
        if (degree + 1) % modulus
    )
    for degree in allowed_degrees:
        monomial = [0] * 12
        monomial[degree] = 1
        columns.append(
            pad(
                scale(
                    multiply(C, monomial, modulus), -2, modulus
                )
            )
        )

    solver = LinearSolver(columns, modulus)
    intersection = solver.solve(
        scale(particular_numerator, -1, modulus)
    )
    if intersection is None:
        return None
    return (
        intersection,
        stage_two.particular,
        stage_two.basis,
        allowed_degrees,
    )


def reconstruct_w1_candidate(
    intersection_vector: Sequence[int],
    stage_two_particular: Sequence[int],
    stage_two_basis: Sequence[Sequence[int]],
    allowed_degrees: Sequence[int],
    modulus: int = P,
) -> tuple[tuple[int, ...], list[int]]:
    parameter_count = len(stage_two_basis)
    packed = list(stage_two_particular)
    for parameter, basis_vector in zip(
        intersection_vector[:parameter_count], stage_two_basis
    ):
        if not parameter:
            continue
        for index, coefficient in enumerate(basis_vector):
            packed[index] = (
                packed[index] + parameter * coefficient
            ) % modulus
    D_prime = [0] * 12
    for coefficient, degree in zip(
        intersection_vector[parameter_count:], allowed_degrees
    ):
        D_prime[degree] = coefficient
    return tuple(packed), D_prime


def integrate_derivative(
    D_prime: Sequence[int], modulus: int = P
) -> list[int]:
    D = [0] * 13
    D[0] = 1  # choose the required nonzero (0,0) vertex
    for degree, coefficient in enumerate(D_prime):
        exponent = degree + 1
        if exponent % modulus:
            D[exponent] = coefficient * pow(exponent, -1, modulus) % modulus
        else:
            assert coefficient == 0
            D[exponent] = 0
    return D


def final_blocks_hold(
    A: Sequence[int],
    B: Sequence[int],
    D_prime: Sequence[int],
    E: Sequence[int],
    modulus: int = P,
) -> bool:
    # w^0: A'*E-B*D'=0.
    return not any(
        add(
            multiply(derivative(A, modulus), E, modulus),
            scale(
                multiply(B, D_prime, modulus), -1, modulus
            ),
            modulus=modulus,
        )
    )


@dataclass
class SearchStatistics:
    top_pairs: int = 0
    skipped_top_pairs: int = 0
    stage_one_vectors: int = 0
    consistent_stage_two_slices: int = 0
    stage_two_vectors: int = 0
    w1_consistent: int = 0


def search_full_branch(
    modulus: int,
    top_pairs: Iterable[tuple[tuple[int, ...], tuple[int, ...]]],
    max_affine_dimension: int,
    max_top_pairs: int | None,
) -> tuple[dict[str, tuple[int, ...]] | None, SearchStatistics]:
    statistics = SearchStatistics()
    for C, G in top_pairs:
        statistics.top_pairs += 1
        if max_top_pairs is not None and statistics.top_pairs > max_top_pairs:
            break
        stage_one_solver, stage_one_specs = make_stage_one_solver(
            C, G, modulus
        )
        stage_one = stage_one_solver.solve([0] * POLY_ROWS)
        assert stage_one is not None
        stage_two_solver, stage_two_specs = make_stage_two_solver(
            C, G, modulus
        )
        if (
            stage_one.dimension > max_affine_dimension
            or len(stage_two_solver.nullspace) > max_affine_dimension
        ):
            statistics.skipped_top_pairs += 1
            continue
        for stage_one_vector in stage_one.vectors(modulus):
            statistics.stage_one_vectors += 1
            first = unpack(
                stage_one_vector, stage_one_specs, {"B": 9, "F": 13}
            )
            B, F = first["B"], first["F"]
            fixed_stage_two = add(
                scale(
                    multiply(
                        derivative(B, modulus), F, modulus
                    ),
                    2,
                    modulus,
                ),
                scale(
                    multiply(
                        B, derivative(F, modulus), modulus
                    ),
                    -1,
                    modulus,
                ),
                modulus=modulus,
            )
            stage_two = stage_two_solver.solve(
                scale(pad(fixed_stage_two), -1, modulus)
            )
            if stage_two is None:
                continue
            statistics.consistent_stage_two_slices += 1
            if stage_two.dimension > max_affine_dimension:
                statistics.skipped_top_pairs += 1
                continue
            w1_intersection_data = solve_w1_on_stage_two_affine_space(
                stage_two, stage_two_specs, B, C, F, modulus
            )
            if w1_intersection_data is None:
                continue
            (
                w1_intersection,
                stage_two_particular,
                stage_two_basis,
                allowed_degrees,
            ) = w1_intersection_data
            if w1_intersection.dimension > max_affine_dimension:
                statistics.skipped_top_pairs += 1
                continue
            for intersection_vector in w1_intersection.vectors(modulus):
                statistics.stage_two_vectors += 1
                stage_two_vector, D_prime = reconstruct_w1_candidate(
                    intersection_vector,
                    stage_two_particular,
                    stage_two_basis,
                    allowed_degrees,
                    modulus,
                )
                second = unpack(
                    stage_two_vector, stage_two_specs, {"A": 9, "E": 13}
                )
                A, E = second["A"], second["E"]
                A[0] = 1  # free and required vertex coefficient
                if not A[8]:
                    continue
                statistics.w1_consistent += 1
                if not D_prime[11]:  # D_12 = D'_11/12 must be nonzero
                    continue
                if not final_blocks_hold(
                    A, B, D_prime, E, modulus
                ):
                    continue
                D = integrate_derivative(D_prime, modulus)
                solution = {
                    "A": tuple(A),
                    "B": tuple(B),
                    "C": tuple(C),
                    "D": tuple(D),
                    "E": tuple(E),
                    "F": tuple(F),
                    "G": tuple(G),
                }
                verify_solution(solution, modulus)
                return solution, statistics
    return None, statistics


def verify_solution(
    solution: dict[str, tuple[int, ...]], modulus: int = P
) -> None:
    blocks = block_equations(**solution, modulus=modulus)
    for power, block in enumerate(blocks):
        expected = [0, 0, -1 % modulus] if power == 4 else []
        assert pad(block) == pad(expected)
    A, C = solution["A"], solution["C"]
    D, G = solution["D"], solution["G"]
    assert A[0] and A[8] and C[1] and C[8]
    assert D[0] and D[12] and G[2] and G[12]


def format_solution(solution: dict[str, tuple[int, ...]]) -> str:
    lines = ["explicit transformed F_5 solution:"]
    for name in "ABCDEFG":
        lines.append(f"{name}={solution[name]}")
    lines.append(
        "Here coefficient index u denotes z^u; the w-powers are "
        "A,D:0, B,E:1, C,F:2, G:3."
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prime",
        type=int,
        choices=(5, 7),
        default=5,
        help="finite field to search (both top enumerators are exhaustive)",
    )
    parser.add_argument(
        "--top-only",
        action="store_true",
        help="only count the exhaustive normalized top-block solutions",
    )
    parser.add_argument(
        "--max-affine-dimension",
        type=int,
        default=8,
        help="skip (and explicitly report) affine spaces above this dimension",
    )
    parser.add_argument(
        "--max-top-pairs",
        type=int,
        help="debugging bound; omitting it examines all normalized top pairs",
    )
    args = parser.parse_args()

    verify_support_reconstruction()
    print(
        "verified exact reconstruction: 25 P monomials, 47 Q monomials, "
        "92 rows, 975 nonzero terms"
    )
    top_pairs = tuple(
        enumerate_top_pairs_p5()
        if args.prime == 5
        else enumerate_top_pairs_p7()
    )
    expected_top_count = {5: 292, 7: 234}[args.prime]
    print(
        f"normalized F_{args.prime} top-block solutions: "
        f"{len(top_pairs)}"
    )
    assert len(top_pairs) == expected_top_count
    print(
        "characteristics 2 and 3: top block is impossible with "
        "deg(C)=8, deg(G)=12 (degree argument)"
    )
    p_coefficients, fixed_rank, sparse_covector = fixed_p_rank_certificate(
        args.prime, top_pairs[0][0]
    )
    expected_rank = {5: 44, 7: 45}[args.prime]
    assert fixed_rank == expected_rank
    print(
        "full-polygon fixed-P witness: "
        f"P coefficients={dict(sorted(p_coefficients.items()))}"
    )
    print(
        f"rank(M)={fixed_rank}, rank([M|target])={fixed_rank + 1}; "
        f"left-kernel certificate={sparse_covector}"
    )
    if args.top_only:
        return

    solution, statistics = search_full_branch(
        args.prime,
        iter(top_pairs),
        args.max_affine_dimension, args.max_top_pairs
    )
    print(f"search statistics: {statistics}")
    if solution is None:
        if statistics.skipped_top_pairs:
            print(
                "RESULT: no solution in examined slices; search is not "
                f"exhaustive because {statistics.skipped_top_pairs} slices "
                "exceeded the affine-dimension bound"
            )
        elif (
            args.max_top_pairs is not None
            and statistics.top_pairs > args.max_top_pairs
        ):
            print("RESULT: no solution before the requested top-pair cutoff")
        else:
            print(
                f"RESULT: exhaustive F_{args.prime} obstruction for the "
                "full normalized a/b branch"
            )
    else:
        print(f"RESULT: full a/b branch solution over F_{args.prime}")
        print(format_solution(solution))


if __name__ == "__main__":
    main()
