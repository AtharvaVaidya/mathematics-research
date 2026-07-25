#!/usr/bin/env python3
"""Seven-parameter diagonal recursion for the case-c Laurent extension.

In z=xy, w=xy^2, case c has

    P=sum(i=-8..2) z^i A_i(w),
    Q=sum(j=-12..3) z^j B_j(w),

with A_2=U/w and B_3=V/w on the known five-point outer Hurwitz
algebra.  The positive radial blocks are the a/b system; negative radial
blocks enter successively and linearly.  This script performs the full
recursion over one modular outer branch, retaining the seven meaningful
kernel parameters of weights (1,1,2,2,3,3,4).
"""

from __future__ import annotations

from dataclasses import dataclass

from route_bd_fbar_obstruction import (
    K,
    ONE,
    T,
    ZERO,
    outer_coefficients,
)


WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
Monomial = tuple[int, ...]


@dataclass
class SP:
    terms: dict[Monomial, K]

    def __init__(
        self,
        value: int | K = 0,
        terms: dict[Monomial, K] | None = None,
    ) -> None:
        if terms is not None:
            self.terms = {
                monomial: coefficient
                for monomial, coefficient in terms.items()
                if coefficient
            }
        else:
            coefficient = K.coerce(value)
            self.terms = (
                {(0,) * len(WEIGHTS): coefficient}
                if coefficient
                else {}
            )

    @staticmethod
    def coerce(value: int | K | SP) -> SP:
        return value if isinstance(value, SP) else SP(value)

    @staticmethod
    def variable(index: int) -> SP:
        monomial = [0] * len(WEIGHTS)
        monomial[index] = 1
        return SP(terms={tuple(monomial): ONE})

    def __bool__(self) -> bool:
        return bool(self.terms)

    def __add__(self, other: int | K | SP) -> SP:
        other = self.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, ZERO) + coefficient
            if not result[monomial]:
                del result[monomial]
        return SP(terms=result)

    __radd__ = __add__

    def __neg__(self) -> SP:
        return SP(
            terms={
                monomial: -coefficient
                for monomial, coefficient in self.terms.items()
            }
        )

    def __sub__(self, other: int | K | SP) -> SP:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | K | SP) -> SP:
        return self.coerce(other) - self

    def __mul__(self, other: int | K | SP) -> SP:
        other = self.coerce(other)
        result: dict[Monomial, K] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left_monomial[index] + right_monomial[index]
                    for index in range(len(WEIGHTS))
                )
                result[monomial] = (
                    result.get(monomial, ZERO)
                    + left_coefficient * right_coefficient
                )
                if not result[monomial]:
                    del result[monomial]
        return SP(terms=result)

    __rmul__ = __mul__

    def weighted_degrees(self) -> set[int]:
        return {
            sum(
                exponent * weight
                for exponent, weight in zip(monomial, WEIGHTS)
            )
            for monomial in self.terms
        }

    def singular(self) -> str:
        variables = tuple(f"x{index}" for index in range(len(WEIGHTS)))
        pieces = []
        for monomial in sorted(self.terms, reverse=True):
            coefficient = self.terms[monomial]
            factors = [
                variable if exponent == 1 else f"{variable}^{exponent}"
                for variable, exponent in zip(variables, monomial)
                if exponent
            ]
            coefficient_text = coefficient.singular()
            if not factors:
                pieces.append(coefficient_text)
            elif coefficient_text == "1":
                pieces.append("*".join(factors))
            elif coefficient_text == "-1":
                pieces.append("-" + "*".join(factors))
            else:
                pieces.append(
                    f"({coefficient_text})*" + "*".join(factors)
                )
        return "+".join(pieces).replace("+-", "-") if pieces else "0"


VARIABLES = tuple(SP.variable(index) for index in range(len(WEIGHTS)))
Laurent = dict[int, SP]


def derivative(poly: Laurent) -> Laurent:
    return {
        exponent - 1: coefficient * exponent
        for exponent, coefficient in poly.items()
        if exponent and coefficient
    }


def add(*polys: Laurent) -> Laurent:
    result: Laurent = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            result[exponent] = result.get(exponent, SP()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def multiply(left: Laurent, right: Laurent) -> Laurent:
    result: Laurent = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, SP())
                + left_coefficient * right_coefficient
            )
            if not result[exponent]:
                del result[exponent]
    return result


def scale_shift(
    poly: Laurent,
    scalar: int | K | SP,
    shift: int,
) -> Laurent:
    scalar = SP.coerce(scalar)
    return {
        exponent + shift: scalar * coefficient
        for exponent, coefficient in poly.items()
        if scalar * coefficient
    }


def bracket_block(
    left_degree: int,
    left: Laurent,
    right_degree: int,
    right: Laurent,
) -> Laurent:
    return add(
        scale_shift(
            multiply(left, derivative(right)),
            left_degree,
            1,
        ),
        scale_shift(
            multiply(derivative(left), right),
            -right_degree,
            1,
        ),
    )


def supports(radial_degree: int, is_q: bool) -> tuple[int, ...]:
    maximum = 12 if is_q else 8
    if radial_degree >= 0:
        return tuple(
            range((13 if is_q else 9) - radial_degree)
        )
    return tuple(range(-radial_degree, maximum + 1))


def rref_with_rhs(
    matrix: list[list[K]],
    rhs: list[SP],
) -> tuple[list[list[K]], list[SP], list[int]]:
    work = [list(row) for row in matrix]
    values = list(rhs)
    pivot_row = 0
    pivots: list[int] = []
    column_count = len(work[0]) if work else 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        values[pivot_row], values[selected] = (
            values[selected],
            values[pivot_row],
        )
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [
            coefficient * inverse
            for coefficient in work[pivot_row]
        ]
        values[pivot_row] *= inverse
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
            values[row] -= multiplier * values[pivot_row]
        pivots.append(column)
        pivot_row += 1
    return work, values, pivots


def solve_stage(
    stage: int,
    a_blocks: dict[int, Laurent],
    b_blocks: dict[int, Laurent],
    free_parameters: tuple[SP | None, ...],
) -> tuple[Laurent | None, Laurent | None, list[SP], dict[str, int]]:
    new_a_degree = stage - 2
    new_b_degree = stage - 1
    a_support = (
        supports(new_a_degree, False)
        if -8 <= new_a_degree <= 1
        else ()
    )
    b_support = (
        supports(new_b_degree, True)
        if -12 <= new_b_degree <= 2
        else ()
    )

    source: Laurent = {}
    for left_degree, left in a_blocks.items():
        for right_degree, right in b_blocks.items():
            if left_degree + right_degree - 1 == stage:
                source = add(
                    source,
                    bracket_block(
                        left_degree,
                        left,
                        right_degree,
                        right,
                    ),
                )

    columns: list[Laurent] = []
    for exponent in a_support:
        columns.append(
            bracket_block(
                new_a_degree,
                {exponent: SP(1)},
                3,
                b_blocks[3],
            )
        )
    for exponent in b_support:
        columns.append(
            bracket_block(
                2,
                a_blocks[2],
                new_b_degree,
                {exponent: SP(1)},
            )
        )
    row_exponents = tuple(
        sorted(
            set(source)
            | {
                exponent
                for column in columns
                for exponent in column
            }
        )
    )
    matrix = [
        [
            column.get(exponent, SP()).terms.get(
                (0,) * len(WEIGHTS),
                ZERO,
            )
            for column in columns
        ]
        for exponent in row_exponents
    ]
    rhs = [source.get(exponent, SP()) for exponent in row_exponents]
    work, values, pivots = rref_with_rhs(matrix, rhs)
    free_columns = [
        column for column in range(len(columns)) if column not in pivots
    ]
    assert len(free_columns) == len(free_parameters)
    solution = [SP() for _ in columns]
    for column, parameter in zip(free_columns, free_parameters):
        solution[column] = parameter if parameter is not None else SP()
    for row, column in enumerate(pivots):
        solution[column] = -values[row] - sum(
            (
                work[row][free] * solution[free]
                for free in free_columns
            ),
            SP(),
        )
    consistency = [
        values[row]
        for row in range(len(pivots), len(values))
        if values[row]
    ]
    a_block = (
        {
            exponent: solution[index]
            for index, exponent in enumerate(a_support)
            if solution[index]
        }
        if a_support
        else None
    )
    b_block = (
        {
            exponent: solution[len(a_support) + index]
            for index, exponent in enumerate(b_support)
            if solution[len(a_support) + index]
        }
        if b_support
        else None
    )
    return a_block, b_block, consistency, {
        "rows": len(row_exponents),
        "variables": len(columns),
        "rank": len(pivots),
        "kernel": len(free_columns),
        "free_columns": tuple(free_columns),
    }


def main() -> None:
    u, v = outer_coefficients(T)
    a_blocks: dict[int, Laurent] = {
        2: {-1: SP(1)}
        | {
            index: SP(coefficient)
            for index, coefficient in enumerate(u[1:])
        }
    }
    b_blocks: dict[int, Laurent] = {
        3: {-1: SP(1)}
        | {
            index: SP(coefficient)
            for index, coefficient in enumerate(v[1:])
        }
    }
    free_by_stage: dict[int, tuple[SP | None, ...]] = {
        3: (VARIABLES[0], VARIABLES[1]),
        # The first free column is the additive P constant.
        2: (None, VARIABLES[2], VARIABLES[3]),
        # The first free column is the additive Q constant.
        1: (None, VARIABLES[4], VARIABLES[5]),
        0: (VARIABLES[6],),
    }
    constraints: list[SP] = []
    for stage in range(3, -12, -1):
        a_block, b_block, new_constraints, stats = solve_stage(
            stage,
            a_blocks,
            b_blocks,
            free_by_stage.get(stage, ()),
        )
        if a_block is not None:
            a_blocks[stage - 2] = a_block
        if b_block is not None:
            b_blocks[stage - 1] = b_block
        constraints.extend(new_constraints)
        term_count = sum(
            len(constraint.terms)
            for constraint in new_constraints
        )
        degrees = sorted(
            {
                degree
                for constraint in new_constraints
                for degree in constraint.weighted_degrees()
            }
        )
        print(
            "stage",
            stage,
            stats,
            "constraints",
            len(new_constraints),
            "terms",
            term_count,
            "weights",
            degrees,
            flush=True,
        )

    # Terminal equations after the final B_-12 block.
    for stage in range(-12, -22, -1):
        source: Laurent = {}
        for left_degree, left in a_blocks.items():
            for right_degree, right in b_blocks.items():
                if left_degree + right_degree - 1 == stage:
                    source = add(
                        source,
                        bracket_block(
                            left_degree,
                            left,
                            right_degree,
                            right,
                        ),
                    )
        terminal = [
            coefficient
            for coefficient in source.values()
            if coefficient
        ]
        constraints.extend(terminal)
        print(
            "terminal",
            stage,
            "constraints",
            len(terminal),
            "terms",
            sum(len(item.terms) for item in terminal),
            "weights",
            sorted(
                {
                    degree
                    for item in terminal
                    for degree in item.weighted_degrees()
                }
            ),
            flush=True,
        )

    print(
        "TOTAL",
        len(constraints),
        "terms",
        sum(len(item.terms) for item in constraints),
    )


if __name__ == "__main__":
    main()
