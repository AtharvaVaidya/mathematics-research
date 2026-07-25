#!/usr/bin/env python3
"""Exact characteristic-zero reconnaissance in the canonical k=1 C basis.

This is a discovery script, not a verifier.  It reconstructs the first
weight-eight radial consistency equations over Q using the seven explicit
Hamiltonian kernel modes.  The finite-field calculations prove that their
radical is the origin; the purpose here is to expose characteristic-zero
factorizations and elimination patterns that may admit a structural proof.
"""

from __future__ import annotations

import argparse
import subprocess

import sympy as sp


w = sp.symbols("w")
X = sp.symbols("X0:7")

WPoly = dict[int, sp.Expr]


def wadd(*polynomials: WPoly) -> WPoly:
    result: WPoly = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = sp.expand(
                result.get(exponent, 0) + coefficient
            )
            if result[exponent] == 0:
                del result[exponent]
    return result


def wmultiply(left: WPoly, right: WPoly) -> WPoly:
    result: WPoly = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = sp.expand(
                result.get(exponent, 0)
                + left_coefficient * right_coefficient
            )
            if result[exponent] == 0:
                del result[exponent]
    return result


def wderivative(polynomial: WPoly) -> WPoly:
    return {
        exponent - 1: sp.expand(exponent * coefficient)
        for exponent, coefficient in polynomial.items()
        if exponent
    }


def wscale(polynomial: WPoly, scalar: sp.Expr) -> WPoly:
    return {
        exponent: sp.expand(scalar * coefficient)
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient != 0
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


def lower_support(
    vertical_bound: int,
    radial_degree: int,
    outer: int,
) -> list[int]:
    assert radial_degree < outer
    if radial_degree > 0:
        return list(range(vertical_bound - radial_degree + 1))
    if radial_degree == 0:
        return list(range(1, vertical_bound + 1))
    if radial_degree >= -vertical_bound:
        return list(range(-radial_degree, vertical_bound + 1))
    return []


def rational_rref_affine(
    matrix: list[list[sp.Rational]],
    source: list[sp.Expr],
) -> tuple[list[sp.Expr], list[sp.Expr], list[int]]:
    work = [list(row) for row in matrix]
    rhs = [sp.expand(value) for value in source]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column] != 0
            ),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        rhs[pivot_row], rhs[selected] = rhs[selected], rhs[pivot_row]
        inverse = 1 / work[pivot_row][column]
        work[pivot_row] = [
            sp.cancel(coefficient * inverse)
            for coefficient in work[pivot_row]
        ]
        rhs[pivot_row] = sp.expand(rhs[pivot_row] * inverse)
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                sp.cancel(
                    work[row][index]
                    - multiplier * work[pivot_row][index]
                )
                for index in range(column_count)
            ]
            rhs[row] = sp.expand(
                rhs[row] - multiplier * rhs[pivot_row]
            )
        pivots.append(column)
        pivot_row += 1

    solution = [sp.Integer(0) for _ in range(column_count)]
    for row, column in enumerate(pivots):
        solution[column] = sp.expand(-rhs[row])
    constraints = [
        sp.factor(rhs[row])
        for row in range(pivot_row, row_count)
        if rhs[row] != 0
    ]
    return solution, constraints, pivots


def c_pair(
    deficit: int,
    parameter: dict[int, sp.Rational],
    u: list[sp.Rational],
    v: list[sp.Rational],
) -> tuple[WPoly, WPoly]:
    c = 5 - deficit
    a: WPoly = {}
    b: WPoly = {}
    for exponent, coefficient in parameter.items():
        for index, outer in enumerate(u):
            value = (
                sp.Rational(
                    c * index + deficit - 3 - 2 * exponent,
                    c,
                )
                * coefficient
                * outer
            )
            if value:
                a[exponent + index] = sp.expand(
                    a.get(exponent + index, 0) + value
                )
        for index, outer in enumerate(v):
            value = (
                sp.Rational(
                    c * index + deficit - 2 - 3 * exponent,
                    c,
                )
                * coefficient
                * outer
            )
            if value:
                b[exponent + index] = sp.expand(
                    b.get(exponent + index, 0) + value
                )
    a = {exponent: value for exponent, value in a.items() if value != 0}
    b = {exponent: value for exponent, value in b.items() if value != 0}
    return a, b


def outer_pair() -> tuple[list[sp.Rational], list[sp.Rational]]:
    u = [
        sp.Rational(1),
        sp.Rational(1),
        sp.Rational(6, 25),
        sp.Rational(9, 250),
    ]
    v = [
        sp.Rational(1),
        sp.Rational(2, 3),
        sp.Rational(6, 25),
        sp.Rational(36, 875),
        sp.Rational(18, 4375),
    ]
    U = sum(coefficient * w**index for index, coefficient in enumerate(u))
    V = sum(coefficient * w**index for index, coefficient in enumerate(v))
    edge = sp.expand(U * V + 2 * w * U * sp.diff(V, w)
                     - 3 * w * sp.diff(U, w) * V)
    assert edge == 1
    return u, v


def canonical_modes(
    u: list[sp.Rational],
    v: list[sp.Rational],
) -> dict[int, tuple[tuple[WPoly, WPoly], ...]]:
    u_square: dict[int, sp.Rational] = {}
    for left, left_coefficient in enumerate(u):
        for right, right_coefficient in enumerate(u):
            u_square[left + right] = (
                u_square.get(left + right, 0)
                + left_coefficient * right_coefficient
            )
    high_d1 = {
        exponent - 1: coefficient
        for exponent, coefficient in u_square.items()
        if exponent >= 2 and coefficient
    }
    high_d4 = {2: sp.Rational(1)}
    parameters = {
        1: ({0: sp.Rational(1)}, high_d1),
        2: (
            {1: sp.Rational(1)},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(v)
                if exponent >= 2
            },
        ),
        3: (
            {1: sp.Rational(1)},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(u)
                if exponent >= 2
            },
        ),
        4: (high_d4,),
    }
    modes = {
        deficit: tuple(
            c_pair(deficit, parameter, u, v)
            for parameter in parameters_at_deficit
        )
        for deficit, parameters_at_deficit in parameters.items()
    }
    # Check every displayed mode lies in the exact support window.
    for deficit, pairs in modes.items():
        p_support = set(lower_support(4, 2 - deficit, 2))
        q_support = set(lower_support(6, 3 - deficit, 3))
        for a, b in pairs:
            assert set(a) <= p_support
            assert set(b) <= q_support
    return modes


def equations() -> list[sp.Expr]:
    u, v = outer_pair()
    modes = canonical_modes(u, v)
    p_blocks: dict[int, WPoly] = {
        2: {index - 1: coefficient for index, coefficient in enumerate(u)}
    }
    q_blocks: dict[int, WPoly] = {
        3: {index - 1: coefficient for index, coefficient in enumerate(v)}
    }
    parameter_offset = {1: 0, 2: 2, 3: 4, 4: 6}
    constraints: list[sp.Expr] = []

    for deficit in range(1, 9):
        p_degree = 2 - deficit
        q_degree = 3 - deficit
        output_degree = 4 - deficit
        p_support = lower_support(4, p_degree, 2)
        q_support = lower_support(6, q_degree, 3)
        source: WPoly = {}
        for left_degree, left in p_blocks.items():
            for right_degree, right in q_blocks.items():
                if left_degree + right_degree - 1 == output_degree:
                    source = wadd(
                        source,
                        bracket(
                            left_degree,
                            left,
                            right_degree,
                            right,
                        ),
                    )
        columns = [
            bracket(p_degree, {exponent: sp.Integer(1)}, 3, q_blocks[3])
            for exponent in p_support
        ]
        columns.extend(
            bracket(2, p_blocks[2], q_degree, {exponent: sp.Integer(1)})
            for exponent in q_support
        )
        row_exponents = sorted(
            set(source).union(*(set(column) for column in columns))
        )
        matrix = [
            [
                sp.Rational(column.get(exponent, 0))
                for column in columns
            ]
            for exponent in row_exponents
        ]
        source_vector = [
            source.get(exponent, sp.Integer(0))
            for exponent in row_exponents
        ]
        solution, new_constraints, pivots = rational_rref_affine(
            matrix,
            source_vector,
        )
        kernel_count = len(modes.get(deficit, ()))
        assert len(columns) - len(pivots) == kernel_count
        if kernel_count:
            offset = parameter_offset[deficit]
            for local_index, (a_mode, b_mode) in enumerate(
                modes[deficit]
            ):
                parameter = X[offset + local_index]
                for index, exponent in enumerate(p_support):
                    solution[index] = sp.expand(
                        solution[index]
                        + parameter * a_mode.get(exponent, 0)
                    )
                split = len(p_support)
                for index, exponent in enumerate(q_support):
                    solution[split + index] = sp.expand(
                        solution[split + index]
                        + parameter * b_mode.get(exponent, 0)
                    )
        split = len(p_support)
        p_blocks[p_degree] = {
            exponent: coefficient
            for exponent, coefficient in zip(p_support, solution[:split])
            if coefficient != 0
        }
        q_blocks[q_degree] = {
            exponent: coefficient
            for exponent, coefficient in zip(
                q_support,
                solution[split:],
            )
            if coefficient != 0
        }
        constraints.extend(new_constraints)

    assert len(constraints) == 18
    return constraints


def singular_text(polynomial: sp.Expr) -> str:
    _denominator, cleared = sp.Poly(
        sp.expand(polynomial),
        *X,
        domain=sp.QQ,
    ).clear_denoms()
    return sp.sstr(cleared.as_expr()).replace("**", "^")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--singular", action="store_true")
    parser.add_argument("--branch-y0", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    constraints = equations()
    if not args.quiet:
        for index, equation in enumerate(constraints):
            print(f"E{index:02d} = {sp.factor(equation)}")

    if args.branch_y0:
        x0, x1, x2, x3, x4, x5, _x6 = X
        substitutions = {
            x0: 2 * x1,
            x3: sp.Rational(3, 2) * x2,
            x5: x4,
        }
        constraints = [
            sp.expand(equation.subs(substitutions))
            for equation in constraints
        ]
        constraints = [equation for equation in constraints if equation != 0]

    if args.singular or args.branch_y0:
        ideal = ",\n".join(singular_text(equation) for equation in constraints)
        variables = (
            "(X1,X2,X4,X6)"
            if args.branch_y0
            else "(X1,X3,X5,X6,X0,X2,X4)"
        )
        program = f"""ring R=0,(X1,X3,X5,X6,X0,X2,X4),lp;
option(redSB);
ideal I={ideal};
ideal G=std(I);
print("LEX SIZE "+string(size(G)));
for (int i=1;i<=size(G);i++) {{
  poly L=lead(G[i]);
  if (size(L)==1) {{ print(L); }}
}}
"""
        program = program.replace(
            "ring R=0,(X1,X3,X5,X6,X0,X2,X4),lp;",
            f"ring R=0,{variables},lp;",
        )
        result = subprocess.run(
            ["Singular", "-q"],
            input=program,
            text=True,
            capture_output=True,
            check=True,
        )
        print(result.stdout)


if __name__ == "__main__":
    main()
