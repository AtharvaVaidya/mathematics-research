#!/usr/bin/env python3
"""Exact modular projective obstruction for the GGHV case-c branch.

This verifier rewrites case c in

    z = x*y,  w = z*y,  {z,w}=w

and solves [P,Q]=x^2 in descending z-degree over Fbar_32003.  The common
degree-(2,3) edge is the same degree-21 Belyi pair as in the a/b branch.
After the two irrelevant additive constants are removed, the 165 remaining
lower coefficients are polynomial functions of seven kernel parameters of
weights

    (1, 1, 2, 2, 3, 3, 4).

The rows of z-degree 3 through -11 give 79 weighted-homogeneous consistency
equations.  Over each of the two rational and one cubic field factors of the
five-point Hurwitz algebra, Singular verifies that their quotient has vector
space dimension 328 and that X0^32,...,X6^32 vanish.  Thus the geometric
fiber is supported only at the origin, so its weighted projectivization is
empty.  The three cubic conjugates are handled at once over F_(32003^3).
In fact, the first 19 equations, of weights at most eight, already have
origin-only radical over every factor; their quotient dimension is 380.

Rows of z-degree -12 through -21 contain no new coefficients.  They are not
needed for projective emptiness: imposing fewer equations already has only
the geometric origin, and adding the terminal equations can only shrink that
fiber.  At the reduced origin the recursion also makes every lower
coefficient vanish.  ``--check-terminal-r1`` additionally verifies by
Gröbner reduction that all terminal rows lie in the first rational
consistency ideal.

Run:

    .venv/bin/python route_bd_case_c_radial_obstruction.py

Singular 4.4 or newer must be available on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable

from route_bd_fbar_obstruction import (
    K,
    ONE,
    ZERO,
    outer_coefficients,
)


NVAR = 7
PARAMETER_WEIGHTS = (1, 1, 2, 2, 3, 3, 4)


@dataclass
class SP:
    terms: dict[tuple[int, ...], K]

    def __init__(
        self,
        value: int | K = 0,
        terms: dict[tuple[int, ...], K] | None = None,
    ) -> None:
        if terms is None:
            coefficient = K.coerce(value)
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
    def coerce(value: int | K | SP) -> SP:
        return value if isinstance(value, SP) else SP(value)

    @staticmethod
    def variable(index: int) -> SP:
        exponent = [0] * NVAR
        exponent[index] = 1
        return SP(terms={tuple(exponent): ONE})

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
        result: dict[tuple[int, ...], K] = {}
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

    def term_count(self) -> int:
        return len(self.terms)

    def total_degree(self) -> int:
        return max((sum(monomial) for monomial in self.terms), default=-1)

    def weighted_degrees(self) -> set[int]:
        return {
            sum(
                exponent * weight
                for exponent, weight in zip(monomial, PARAMETER_WEIGHTS)
            )
            for monomial in self.terms
        }

    def singular(self, allow_extension: bool = False) -> str:
        variables = tuple(f"X{index}" for index in range(NVAR))
        pieces: list[str] = []
        for monomial in sorted(self.terms, reverse=True):
            coefficient = self.terms[monomial]
            if allow_extension:
                coefficient_text = coefficient.singular()
            else:
                assert not coefficient.c1 and not coefficient.c2
                signed = (
                    coefficient.c0
                    if coefficient.c0 <= 32003 // 2
                    else coefficient.c0 - 32003
                )
                coefficient_text = str(signed)
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


@dataclass
class RadialSystem:
    constraints: list[SP]
    terminal_constraints: list[SP]
    profiles: list[tuple[int, int, int]]
    p_blocks: dict[int, WPoly]
    q_blocks: dict[int, WPoly]


def p_exponents(radial_degree: int) -> list[int]:
    if radial_degree == 1:
        return list(range(0, 8))
    if radial_degree == 0:
        # The omitted w^0 coefficient is the additive constant in P.
        return list(range(1, 9))
    if -8 <= radial_degree <= -1:
        return list(range(-radial_degree, 9))
    return []


def q_exponents(radial_degree: int) -> list[int]:
    if radial_degree == 2:
        return list(range(0, 11))
    if radial_degree == 1:
        return list(range(0, 12))
    if radial_degree == 0:
        # The omitted w^0 coefficient is the additive constant in Q.
        return list(range(1, 13))
    if -12 <= radial_degree <= -1:
        return list(range(-radial_degree, 13))
    return []


def verify_support_inventory() -> None:
    """Check the complete case-c support and its polynomial coordinate map."""

    outer_p = [(2, exponent) for exponent in range(-1, 7)]
    outer_q = [(3, exponent) for exponent in range(-1, 10)]
    lower_p = [
        (degree, exponent)
        for degree in range(1, -14, -1)
        for exponent in p_exponents(degree)
    ]
    lower_q = [
        (degree + 1, exponent)
        for degree in range(1, -14, -1)
        for exponent in q_exponents(degree + 1)
    ]
    assert len(lower_p) + len(lower_q) == 165
    assert len(set(outer_p + lower_p)) == len(outer_p) + len(lower_p)
    assert len(set(outer_q + lower_q)) == len(outer_q) + len(lower_q)

    # z^i*w^j = x^(i+j)*y^(i+2j); every listed term is polynomial.
    for radial_degree, w_degree in outer_p + outer_q + lower_p + lower_q:
        assert radial_degree + w_degree >= 0
        assert radial_degree + 2 * w_degree >= 0
    assert (0 + 8, 0 + 2 * 8) == (8, 16)
    assert (0 + 12, 0 + 2 * 12) == (12, 24)
    assert (4 - 2, 4 + 2 * (-2)) == (2, 0)


def wadd(*polynomials: WPoly) -> WPoly:
    result: WPoly = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, SP()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def wscale(polynomial: WPoly, scalar: int | K | SP) -> WPoly:
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
    """Coefficient of z^(p_degree+q_degree-1) in the bracket."""

    core = wadd(
        wscale(wmultiply(p, wderivative(q)), p_degree),
        wscale(wmultiply(wderivative(p), q), -q_degree),
    )
    return {exponent + 1: coefficient for exponent, coefficient in core.items()}


def constant_wpoly(coefficients: dict[int, K]) -> WPoly:
    return {exponent: SP(coefficient) for exponent, coefficient in coefficients.items()}


def rref_affine(
    matrix: list[list[K]],
    source: list[SP],
    free_parameters: Iterable[SP],
) -> tuple[list[SP], list[SP], list[int]]:
    """Solve matrix*x + source=0 and retain exact cokernel rows."""

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
        if pivot_row == row_count:
            break

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
    return solution, consistency, pivots


def solve_stage(
    p_blocks: dict[int, WPoly],
    q_blocks: dict[int, WPoly],
    p_degree: int,
    p_exponents: list[int],
    q_degree: int,
    q_exponents: list[int],
    free_parameters: Iterable[SP],
) -> tuple[WPoly, WPoly, list[SP], tuple[int, int, int]]:
    output_degree = p_degree + 2
    assert q_degree == p_degree + 1

    source: WPoly = {}
    for left_degree, left in p_blocks.items():
        for right_degree, right in q_blocks.items():
            if left_degree + right_degree - 1 == output_degree:
                source = wadd(
                    source,
                    bracket(left_degree, left, right_degree, right),
                )

    columns: list[WPoly] = []
    for exponent in p_exponents:
        columns.append(
            bracket(
                p_degree,
                {exponent: SP(1)},
                3,
                q_blocks[3],
            )
        )
    for exponent in q_exponents:
        columns.append(
            bracket(
                2,
                p_blocks[2],
                q_degree,
                {exponent: SP(1)},
            )
        )

    row_exponents = sorted(
        set(source).union(
            *(set(column) for column in columns)
        )
    )
    matrix = [
        [
            column.get(exponent, SP()).terms.get((0,) * NVAR, ZERO)
            for column in columns
        ]
        for exponent in row_exponents
    ]
    source_vector = [source.get(exponent, SP()) for exponent in row_exponents]
    solution, consistency, pivots = rref_affine(
        matrix, source_vector, free_parameters
    )
    split = len(p_exponents)
    p_block = dict(zip(p_exponents, solution[:split]))
    q_block = dict(zip(q_exponents, solution[split:]))
    p_block = {
        exponent: coefficient
        for exponent, coefficient in p_block.items()
        if coefficient
    }
    q_block = {
        exponent: coefficient
        for exponent, coefficient in q_block.items()
        if coefficient
    }
    return (
        p_block,
        q_block,
        consistency,
        (len(columns), len(pivots), len(row_exponents) - len(pivots)),
    )


def build_radial_system(
    outer_parameter: K,
    include_terminal: bool = False,
    verbose: bool = True,
) -> RadialSystem:
    u, v = outer_coefficients(outer_parameter)
    p_blocks: dict[int, WPoly] = {
        2: constant_wpoly(
            {-1: ONE} | {index - 1: u[index] for index in range(1, 8)}
        )
    }
    q_blocks: dict[int, WPoly] = {
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
    all_constraints: list[SP] = []
    profiles: list[tuple[int, int, int]] = []
    solved_coefficient_count = 0
    for stage, p_degree in enumerate(range(1, -14, -1), start=1):
        q_degree = p_degree + 1
        p_support = p_exponents(p_degree)
        q_support = q_exponents(q_degree)

        p_block, q_block, constraints, profile = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
            p_support,
            q_degree,
            q_support,
            free_by_degree.get(p_degree, ()),
        )
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        profiles.append(profile)
        solved_coefficient_count += profile[0]
        all_constraints.extend(constraints)
        radial_weight = 2 - p_degree
        assert radial_weight == 3 - q_degree
        assert all(
            coefficient.weighted_degrees() == {radial_weight}
            for coefficient in tuple(p_block.values()) + tuple(q_block.values())
        )
        assert all(
            constraint.weighted_degrees() == {radial_weight}
            for constraint in constraints
        )
        max_terms = max(
            (constraint.term_count() for constraint in constraints),
            default=0,
        )
        max_degree = max(
            (constraint.total_degree() for constraint in constraints),
            default=-1,
        )
        if verbose:
            print(
                "stage",
                stage,
                "Pdeg",
                p_degree,
                "Qdeg",
                q_degree,
                "profile(vars,rank,coker)",
                profile,
                "new_constraints",
                len(constraints),
                "constraint_max_terms",
                max_terms,
                "constraint_max_degree",
                max_degree,
                "total_constraints",
                len(all_constraints),
                flush=True,
            )

    expected_profiles = [
        (19, 17, 1),
        (20, 18, 1),
        (20, 18, 1),
        (19, 18, 2),
        (17, 17, 2),
        (15, 15, 4),
        (13, 13, 5),
        (11, 11, 6),
        (9, 9, 7),
        (7, 7, 8),
        (5, 5, 9),
        (4, 4, 9),
        (3, 3, 9),
        (2, 2, 9),
        (1, 1, 9),
    ]
    assert profiles == expected_profiles
    assert solved_coefficient_count == 165
    assert len(all_constraints) == 79

    all_terminal_constraints: list[SP] = []
    if include_terminal:
        for output_degree in range(-12, -22, -1):
            residual: WPoly = {}
            for left_degree, left in p_blocks.items():
                for right_degree, right in q_blocks.items():
                    if left_degree + right_degree - 1 == output_degree:
                        residual = wadd(
                            residual,
                            bracket(
                                left_degree,
                                left,
                                right_degree,
                                right,
                            ),
                        )
            stage_terminal_constraints = [
                coefficient for coefficient in residual.values() if coefficient
            ]
            assert all(
                constraint.weighted_degrees() == {4 - output_degree}
                for constraint in stage_terminal_constraints
            )
            all_terminal_constraints.extend(stage_terminal_constraints)
            if verbose:
                print(
                    "terminal output degree",
                    output_degree,
                    "constraints",
                    len(stage_terminal_constraints),
                    "max_terms",
                    max(
                        (
                            constraint.term_count()
                            for constraint in stage_terminal_constraints
                        ),
                        default=0,
                    ),
                    "max_degree",
                    max(
                        (
                            constraint.total_degree()
                            for constraint in stage_terminal_constraints
                        ),
                        default=-1,
                    ),
                    flush=True,
                )
    return RadialSystem(
        constraints=all_constraints,
        terminal_constraints=all_terminal_constraints,
        profiles=profiles,
        p_blocks=p_blocks,
        q_blocks=q_blocks,
    )


def run(
    outer_parameter: K,
    maximum_stage: int = 15,
    include_terminal: bool = False,
    verbose: bool = True,
) -> list[SP]:
    """Compatibility entry point; production verification uses all 15 stages."""

    if maximum_stage != 15:
        raise ValueError("the exact obstruction requires all 15 radial stages")
    system = build_radial_system(
        outer_parameter,
        include_terminal=include_terminal,
        verbose=verbose,
    )
    return system.constraints + system.terminal_constraints


def emit_rational_singular(
    outer_parameter: K,
    include_terminal: bool = False,
) -> str:
    constraints = run(
        outer_parameter,
        maximum_stage=15,
        include_terminal=include_terminal,
        verbose=False,
    )
    equations = ",\n".join(
        constraint.singular() for constraint in constraints
    )
    powers = "\n".join(
        f'reduce(X{index}^32,G);'
        for index in range(NVAR)
    )
    return f"""ring R=32003,(X0,X1,X2,X3,X4,X5,X6),dp;
ideal I=
{equations};
ideal G=std(I);
"VDIM";
vdim(G);
"VARIABLE POWERS";
{powers}
"""


def emit_cubic_singular(include_terminal: bool = False) -> str:
    constraints = run(
        K(0, 1),
        maximum_stage=15,
        include_terminal=include_terminal,
        verbose=False,
    )
    equations = ",\n".join(
        constraint.singular(allow_extension=True)
        for constraint in constraints
    )
    powers = "\n".join(
        f'reduce(X{index}^32,G);'
        for index in range(NVAR)
    )
    return f"""ring R=(32003,t),(X0,X1,X2,X3,X4,X5,X6),dp;
minpoly=t^3-11133*t^2-11294*t-6180;
ideal I=
{equations};
ideal G=std(I);
"VDIM";
vdim(G);
"VARIABLE POWERS";
{powers}
"""


def singular_certificate_program(
    label: str,
    system: RadialSystem,
    allow_extension: bool,
    check_terminal: bool,
) -> str:
    equations = ",\n".join(
        constraint.singular(allow_extension=allow_extension)
        for constraint in system.constraints
    )
    prefix_equations = ",\n".join(
        constraint.singular(allow_extension=allow_extension)
        for constraint in system.constraints
        if next(iter(constraint.weighted_degrees())) <= 8
    )
    ring = (
        "ring R=(32003,t),(X0,X1,X2,X3,X4,X5,X6),dp;\n"
        "minpoly=t^3-11133*t^2-11294*t-6180;"
        if allow_extension
        else "ring R=32003,(X0,X1,X2,X3,X4,X5,X6),dp;"
    )
    power_checks = "\n".join(
        (
            f"poly power_remainder_{index}=reduce(X{index}^32,G);"
            f"\nif (power_remainder_{index}!=0) {{ certified=0; }}"
        )
        for index in range(NVAR)
    )
    prefix_power_checks = "\n".join(
        (
            f"poly prefix_power_remainder_{index}=reduce(X{index}^32,G8);"
            f"\nif (prefix_power_remainder_{index}!=0) {{ certified=0; }}"
        )
        for index in range(NVAR)
    )
    terminal_check = ""
    if check_terminal:
        terminal_equations = ",\n".join(
            constraint.singular(allow_extension=allow_extension)
            for constraint in system.terminal_constraints
        )
        terminal_check = f"""
ideal terminal_rows=
{terminal_equations};
ideal terminal_remainders=reduce(terminal_rows,G);
if (size(terminal_remainders)!=0) {{ certified=0; }}
"""
    return f"""{ring}
option(redSB);
ideal I8=
{prefix_equations};
ideal G8=std(I8);
int prefix_quotient_dimension=vdim(G8);
ideal I=
{equations};
ideal G=std(I);
int quotient_dimension=vdim(G);
int certified=1;
if (prefix_quotient_dimension!=380) {{ certified=0; }}
if (quotient_dimension!=328) {{ certified=0; }}
{prefix_power_checks}
{power_checks}
{terminal_check}
print("RADIAL {label} WEIGHT<=8 VDIM "+string(prefix_quotient_dimension));
print("RADIAL {label} VDIM "+string(quotient_dimension));
if (certified==1)
{{
    print("RADIAL {label} CERTIFIED");
}}
else
{{
    print("RADIAL {label} FAILED");
}}
"""


def verify_factor_with_singular(
    label: str,
    outer_parameter: K,
    allow_extension: bool,
    check_terminal: bool = False,
) -> None:
    print(f"building exact radial system for {label}", flush=True)
    system = build_radial_system(
        outer_parameter,
        include_terminal=check_terminal,
        verbose=False,
    )
    assert len(system.constraints) == 79
    print(
        f"{label}: 165 lower coefficients, 7 parameters, "
        f"{len(system.constraints)} consistency equations",
        flush=True,
    )
    if check_terminal:
        print(
            f"{label}: {len(system.terminal_constraints)} terminal rows "
            "will be reduced modulo the consistency ideal",
            flush=True,
        )
    program = singular_certificate_program(
        label,
        system,
        allow_extension=allow_extension,
        check_terminal=check_terminal,
    )
    result = subprocess.run(
        ["Singular", "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
    )
    output = result.stdout + result.stderr
    print(result.stdout.strip(), flush=True)
    assert f"RADIAL {label} CERTIFIED" in output
    assert f"RADIAL {label} FAILED" not in output
    assert "error occurred" not in output.lower()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--factor",
        choices=("all", "r1", "r2", "cubic"),
        default="all",
        help="outer field factor to verify (default: all five geometric points)",
    )
    parser.add_argument(
        "--check-terminal-r1",
        action="store_true",
        help=(
            "also generate the costly terminal rows and reduce them modulo "
            "the first rational consistency ideal"
        ),
    )
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help="verify the exact recursion but do not invoke Singular",
    )
    args = parser.parse_args()

    verify_support_inventory()
    assert shutil.which("Singular") or args.structure_only
    factors = {
        "r1": (K(26839), False),
        "r2": (K(16621), False),
        "cubic": (K(0, 1), True),
    }
    selected = factors if args.factor == "all" else {args.factor: factors[args.factor]}
    for label, (outer_parameter, allow_extension) in selected.items():
        terminal = args.check_terminal_r1 and label == "r1"
        if args.structure_only:
            system = build_radial_system(
                outer_parameter,
                include_terminal=terminal,
                verbose=False,
            )
            print(
                f"RADIAL {label} STRUCTURE: 165 coefficients, "
                f"{len(system.constraints)} consistency equations"
            )
        else:
            verify_factor_with_singular(
                label,
                outer_parameter,
                allow_extension,
                check_terminal=terminal,
            )

    if not args.structure_only:
        if args.factor == "all":
            print("RESULT: CASE-c MODULAR WEIGHTED PROJECTIVE FIBER IS EMPTY")
            print(
                "RESULT: all two rational plus three cubic-conjugate "
                "Hurwitz points are certified"
            )
        else:
            print(f"RESULT: CASE-c MODULAR FACTOR {args.factor} IS CERTIFIED")


if __name__ == "__main__":
    main()
