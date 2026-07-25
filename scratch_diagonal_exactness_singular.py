#!/usr/bin/env python3
"""Modular geometry of the diagonal hyperelliptic exactness locus."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import sympy as sp


def exactness_conditions(
) -> tuple[tuple[sp.Symbol, ...], list[sp.Expr], sp.Expr]:
    q = sp.symbols("q")
    c = sp.symbols("c0:7")
    r = sp.symbols("r0:11")
    polynomial = q**7 + sum(c[index] * q**index for index in range(7))
    primitive = sum(r[index] * q**index for index in range(11))
    equation = sp.Poly(
        2 * polynomial * sp.diff(primitive, q)
        - 3 * sp.diff(polynomial, q) * primitive
        - 2 * q**16,
        q,
    )
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    for degree in range(16, 5, -1):
        coefficient = sp.expand(
            equation.coeff_monomial(q**degree).subs(substitutions)
        )
        variable = r[degree - 6]
        solutions = sp.solve(coefficient, variable, dict=False)
        assert len(solutions) == 1
        substitutions[variable] = solutions[0]
    conditions = []
    for degree in range(6):
        value = sp.factor(
            equation.coeff_monomial(q**degree).subs(substitutions)
        )
        numerator = sp.together(value).as_numer_denom()[0]
        conditions.append(sp.expand(numerator.subs(c[0], 1)))
    discriminant = sp.discriminant(polynomial.subs(c[0], 1), q)
    return c[1:], conditions, sp.expand(discriminant)


def singular_text(
    variables: tuple[sp.Symbol, ...],
    conditions: list[sp.Expr],
    discriminant: sp.Expr,
    prime: int,
    saturate_discriminant: bool,
) -> str:
    variable_text = ",".join(str(variable) for variable in variables)
    ideal_text = ",\n".join(sp.sstr(condition) for condition in conditions)
    saturation = (
        f"""
LIB "elim.lib";
poly discriminant={sp.sstr(discriminant)};
ideal D=discriminant;
ideal S=sat(I,D);
I=S;
"""
        if saturate_discriminant
        else ""
    )
    return f"""
ring R={prime},({variable_text}),dp;
option(redSB);
ideal I=
{ideal_text};
{saturation}
ideal J=std(I);
print("DIM");
print(dim(J));
print("VDIM");
print(vdim(J));
print("BASIS");
print(J);
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=32003)
    parser.add_argument("--saturate-discriminant", action="store_true")
    arguments = parser.parse_args()
    variables, conditions, discriminant = exactness_conditions()
    source = singular_text(
        variables,
        conditions,
        discriminant,
        arguments.prime,
        arguments.saturate_discriminant,
    )
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "diagonal_exactness.sing"
        path.write_text(source)
        completed = subprocess.run(
            ["Singular", "-q", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
