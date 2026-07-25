#!/usr/bin/env python3
"""Exact k=1,2 nonlinear reconnaissance for the (2,3) radial complex.

This companion to ``route_bd_universal_radial_rank.py`` carries the full
descending recursion through every lower coefficient for the same two tiny
outer problems.  It computes the weighted consistency ideals in the stable
seven parameters and asks Singular whether their geometric zero set is only
the origin.  It also checks the stronger finite-jet statement: equations of
weights at most eight already reduce X0^32,...,X6^32 to zero.

The calculation is deliberately limited to k=1,2.  Its purpose is to test
whether the k=3 bounded obstruction reflects a uniform mechanism, not to
launch a broad degree enumeration.
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from typing import Iterable

from route_bd_universal_radial_rank import (
    FQ2,
    ONE,
    ZERO,
    lower_support,
    outer_coefficients,
)


NVAR = 7
WEIGHTS = (1, 1, 2, 2, 3, 3, 4)


@dataclass
class SP:
    terms: dict[tuple[int, ...], FQ2]

    def __init__(
        self,
        value: int | FQ2 = 0,
        terms: dict[tuple[int, ...], FQ2] | None = None,
    ) -> None:
        if terms is None:
            coefficient = FQ2.coerce(value)
            self.terms = (
                {(0,) * NVAR: coefficient} if coefficient else {}
            )
        else:
            self.terms = {
                monomial: coefficient
                for monomial, coefficient in terms.items()
                if coefficient
            }

    @staticmethod
    def coerce(value: int | FQ2 | SP) -> SP:
        return value if isinstance(value, SP) else SP(value)

    @staticmethod
    def variable(index: int) -> SP:
        exponent = [0] * NVAR
        exponent[index] = 1
        return SP(terms={tuple(exponent): ONE})

    def __bool__(self) -> bool:
        return bool(self.terms)

    def __add__(self, other: int | FQ2 | SP) -> SP:
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

    def __sub__(self, other: int | FQ2 | SP) -> SP:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | FQ2 | SP) -> SP:
        return self.coerce(other) - self

    def __mul__(self, other: int | FQ2 | SP) -> SP:
        other = self.coerce(other)
        result: dict[tuple[int, ...], FQ2] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left_monomial[index] + right_monomial[index]
                    for index in range(NVAR)
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

    def singular(self, extension: bool) -> str:
        variables = tuple(f"X{index}" for index in range(NVAR))
        pieces: list[str] = []
        for monomial in sorted(self.terms, reverse=True):
            coefficient = self.terms[monomial]
            c0 = (
                coefficient.c0
                if coefficient.c0 <= 32003 // 2
                else coefficient.c0 - 32003
            )
            c1 = (
                coefficient.c1
                if coefficient.c1 <= 32003 // 2
                else coefficient.c1 - 32003
            )
            assert extension or c1 == 0
            if extension and c1:
                coefficient_text = (
                    f"({c0}+({c1})*s)" if c0 else f"({c1})*s"
                )
            else:
                coefficient_text = str(c0)
            factors = [
                variable if exponent == 1 else f"{variable}^{exponent}"
                for variable, exponent in zip(variables, monomial)
                if exponent
            ]
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


PARAMETERS = tuple(SP.variable(index) for index in range(NVAR))
WPoly = dict[int, SP]


def wadd(*polynomials: WPoly) -> WPoly:
    result: WPoly = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, SP()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def wscale(polynomial: WPoly, scalar: int | FQ2 | SP) -> WPoly:
    scalar = SP.coerce(scalar)
    return {
        exponent: scalar * coefficient
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient
    }


def wmultiply(left: WPoly, right: WPoly) -> WPoly:
    result: WPoly = {}
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


def wderivative(polynomial: WPoly) -> WPoly:
    return {
        exponent - 1: exponent * coefficient
        for exponent, coefficient in polynomial.items()
        if exponent and exponent * coefficient
    }


def bracket(
    p_degree: int,
    p: WPoly,
    q_degree: int,
    q: WPoly,
) -> WPoly:
    core = wadd(
        wscale(wmultiply(p, wderivative(q)), p_degree),
        wscale(wmultiply(wderivative(p), q), -q_degree),
    )
    return {
        exponent + 1: coefficient
        for exponent, coefficient in core.items()
    }


def rref_affine(
    matrix: list[list[FQ2]],
    source: list[SP],
    free_parameters: Iterable[SP],
) -> tuple[list[SP], list[SP], int]:
    work = [list(row) for row in matrix]
    rhs = list(source)
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
        rhs[pivot_row], rhs[selected] = rhs[selected], rhs[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [
            coefficient * inverse for coefficient in work[pivot_row]
        ]
        rhs[pivot_row] *= inverse
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
            rhs[row] -= multiplier * rhs[pivot_row]
        pivots.append(column)
        pivot_row += 1

    free_columns = [
        column for column in range(column_count) if column not in pivots
    ]
    free_parameters = tuple(free_parameters)
    assert len(free_columns) == len(free_parameters)
    solution = [SP() for _ in range(column_count)]
    for column, parameter in zip(free_columns, free_parameters):
        solution[column] = parameter
    for row, column in enumerate(pivots):
        solution[column] = -rhs[row] - sum(
            (
                work[row][free] * solution[free]
                for free in free_columns
            ),
            SP(),
        )
    consistency = [
        rhs[row] for row in range(pivot_row, row_count) if rhs[row]
    ]
    return solution, consistency, len(pivots)


def consistency_equations(k: int) -> tuple[list[SP], int]:
    u, v = outer_coefficients(k)
    p_blocks: dict[int, WPoly] = {
        2: {
            index - 1: SP(coefficient)
            for index, coefficient in enumerate(u)
        }
    }
    q_blocks: dict[int, WPoly] = {
        3: {
            index - 1: SP(coefficient)
            for index, coefficient in enumerate(v)
        }
    }
    p_bound = 2 * (k + 1)
    q_bound = 3 * (k + 1)
    free_by_deficit = {
        1: PARAMETERS[0:2],
        2: PARAMETERS[2:4],
        3: PARAMETERS[4:6],
        4: PARAMETERS[6:7],
    }
    constraints: list[SP] = []
    coefficient_count = 0

    for deficit in range(1, 3 * (k + 2) + 1):
        p_degree = 2 - deficit
        q_degree = 3 - deficit
        output_degree = 4 - deficit
        p_support = lower_support(p_bound, p_degree, 2)
        q_support = lower_support(q_bound, q_degree, 3)
        coefficient_count += len(p_support) + len(q_support)

        source: WPoly = {}
        for left_degree, left in p_blocks.items():
            for right_degree, right in q_blocks.items():
                if left_degree + right_degree - 1 == output_degree:
                    source = wadd(
                        source,
                        bracket(left_degree, left, right_degree, right),
                    )

        columns: list[WPoly] = [
            bracket(
                p_degree,
                {exponent: SP(1)},
                3,
                q_blocks[3],
            )
            for exponent in p_support
        ]
        columns.extend(
            bracket(
                2,
                p_blocks[2],
                q_degree,
                {exponent: SP(1)},
            )
            for exponent in q_support
        )
        row_exponents = sorted(
            set(source).union(*(set(column) for column in columns))
        )
        matrix = [
            [
                column.get(exponent, SP()).terms.get((0,) * NVAR, ZERO)
                for column in columns
            ]
            for exponent in row_exponents
        ]
        source_vector = [
            source.get(exponent, SP()) for exponent in row_exponents
        ]
        solution, new_constraints, rank = rref_affine(
            matrix,
            source_vector,
            free_by_deficit.get(deficit, ()),
        )
        split = len(p_support)
        p_block = {
            exponent: coefficient
            for exponent, coefficient in zip(p_support, solution[:split])
            if coefficient
        }
        q_block = {
            exponent: coefficient
            for exponent, coefficient in zip(q_support, solution[split:])
            if coefficient
        }
        assert rank + len(free_by_deficit.get(deficit, ())) == len(columns)
        assert all(
            coefficient.weighted_degrees() == {deficit}
            for coefficient in tuple(p_block.values()) + tuple(q_block.values())
        )
        assert all(
            equation.weighted_degrees() == {deficit}
            for equation in new_constraints
        )
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        constraints.extend(new_constraints)
    return constraints, coefficient_count


def singular_program(k: int, equations: list[SP]) -> str:
    extension = k == 2
    ring = (
        "ring R=(32003,s),(X0,X1,X2,X3,X4,X5,X6),dp;\n"
        "minpoly=s^2+9432*s-2820;"
        if extension
        else "ring R=32003,(X0,X1,X2,X3,X4,X5,X6),dp;"
    )
    ideal = ",\n".join(
        equation.singular(extension=extension) for equation in equations
    )
    prefix_ideal = ",\n".join(
        equation.singular(extension=extension)
        for equation in equations
        if next(iter(equation.weighted_degrees())) <= 8
    )
    full_powers = "\n".join(
        (
            f"poly remainder_{index}=reduce(X{index}^32,G);"
            f"\nif (remainder_{index}!=0) {{ certified=0; }}"
        )
        for index in range(NVAR)
    )
    prefix_powers = "\n".join(
        (
            f"poly prefix_remainder_{index}=reduce(X{index}^32,G8);"
            f"\nif (prefix_remainder_{index}!=0) {{ certified=0; }}"
        )
        for index in range(NVAR)
    )
    expected_dimension = {1: 243, 2: 225}[k]
    expected_prefix_dimension = {1: 255, 2: 247}[k]
    prefix_nilpotence = {
        1: (11, 11, 6, 6, 4, 4, 3),
        2: (11, 6, 6, 3, 4, 4, 3),
    }[k]
    sharp_prefix_checks = "\n".join(
        (
            f"poly sharp_remainder_{index}=reduce("
            f"X{index}^{exponent},G8);"
            f"\nif (sharp_remainder_{index}!=0) {{ certified=0; }}"
            f"\npoly previous_remainder_{index}=reduce("
            f"X{index}^{exponent - 1},G8);"
            f"\nif (previous_remainder_{index}==0) {{ certified=0; }}"
        )
        for index, exponent in enumerate(prefix_nilpotence)
    )
    return f"""{ring}
option(redSB);
ideal I8=
{prefix_ideal};
ideal G8=std(I8);
int prefix_dimension=vdim(G8);
ideal I=
{ideal};
ideal G=std(I);
int dimension=vdim(G);
int certified=1;
if (prefix_dimension!={expected_prefix_dimension}) {{ certified=0; }}
if (dimension!={expected_dimension}) {{ certified=0; }}
{prefix_powers}
{sharp_prefix_checks}
{full_powers}
print("k={k} WEIGHT<=8 VDIM "+string(prefix_dimension));
print("k={k} SHARP PREFIX POWERS {prefix_nilpotence}");
print("k={k} VDIM "+string(dimension));
if (certified==1) {{ print("k={k} ORIGIN ONLY"); }}
else {{ print("k={k} NOT CERTIFIED"); }}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, choices=(1, 2))
    args = parser.parse_args()
    ks = (args.k,) if args.k else (1, 2)
    for k in ks:
        equations, coefficient_count = consistency_equations(k)
        print(
            f"k={k}: {coefficient_count} coefficients, "
            f"{len(equations)} consistency equations",
            flush=True,
        )
        result = subprocess.run(
            ["Singular", "-q"],
            input=singular_program(k, equations),
            text=True,
            capture_output=True,
            check=True,
        )
        output = result.stdout + result.stderr
        print(result.stdout.strip(), flush=True)
        assert f"k={k} ORIGIN ONLY" in output
        assert f"k={k} NOT CERTIFIED" not in output
        assert "error occurred" not in output.lower()
    if args.k:
        print(f"RESULT: k={args.k} LOWER WEIGHTED FIBER IS ORIGIN-ONLY")
    else:
        print("RESULT: k=1,2 LOWER WEIGHTED FIBERS ARE ORIGIN-ONLY")
    print("RESULT: WEIGHT <= 8 ALREADY SUFFICES IN BOTH TINY CASES")


if __name__ == "__main__":
    main()
