#!/usr/bin/env python3
"""Eliminate unequal-degree Darboux systems exactly over Q.

This complements ``full_bounded_groebner.py``.  Here P has generator total
degree at most two, while Q may have degree five or six.  Since mixing Q into
P could increase the degree of P, the common-degree SL_2 normalization is not
available.  Instead, the two charts below preserve the ordered degree bounds.

Write p_v,p_w,q_v,q_w for the linear boundary coefficients.  The constant
bracket equation is

    p_v*q_w - p_w*q_v = 1.

If p_v is nonzero, scaling and shearing Q by P gives

    p_v=1, q_v=0, q_w=1.

If p_v is zero, the same degree-preserving operations give

    p_v=0, p_w=1, q_v=-1, q_w=0.

These charts exhaust every prospective pair.  Singular reconstructs and
eliminates every remaining coefficient of P and Q over the rationals.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

import sympy as sp


sys.path.insert(0, str(Path(__file__).resolve().parent))

from full_bounded_groebner import singular_executable  # noqa: E402
from route_a_search import basis, bracket  # noqa: E402


def normalized_chart(q_degree: int, chart: int):
    if q_degree not in (5, 6):
        raise ValueError("the currently certified Q-degree bounds are 5 and 6")
    if chart not in (1, 2):
        raise ValueError("chart must be 1 or 2")

    p_monomials = basis(2, include_constant=False)
    q_monomials = basis(q_degree, include_constant=False)
    variables: list[sp.Symbol] = []
    P = {}
    Q = {}

    p_index = 0
    for monomial in p_monomials:
        if chart == 1 and monomial == (0, 1, 0):
            P[monomial] = sp.Integer(1)
        elif chart == 2 and monomial == (0, 1, 0):
            P[monomial] = sp.Integer(0)
        elif chart == 2 and monomial == (0, 0, 1):
            P[monomial] = sp.Integer(1)
        else:
            variable = sp.Symbol(f"p{p_index}")
            p_index += 1
            P[monomial] = variable
            variables.append(variable)

    q_index = 0
    for monomial in q_monomials:
        if chart == 1 and monomial == (0, 1, 0):
            Q[monomial] = sp.Integer(0)
        elif chart == 1 and monomial == (0, 0, 1):
            Q[monomial] = sp.Integer(1)
        elif chart == 2 and monomial == (0, 1, 0):
            Q[monomial] = sp.Integer(-1)
        elif chart == 2 and monomial == (0, 0, 1):
            Q[monomial] = sp.Integer(0)
        else:
            variable = sp.Symbol(f"q{q_index}")
            q_index += 1
            Q[monomial] = variable
            variables.append(variable)

    answer = bracket(P, Q)
    support = sorted(set(answer).union({(0, 0, 0)}))
    equations = [
        sp.expand(
            answer.get(monomial, 0)
            - (1 if monomial == (0, 0, 0) else 0)
        )
        for monomial in support
    ]
    return tuple(variables), tuple(equation for equation in equations if equation != 0)


def singular_program(variables, equations):
    names = ",".join(map(str, variables))
    generators = ",".join(str(equation).replace("**", "^") for equation in equations)
    return "\n".join(
        [
            f"ring r=0,({names}),dp;",
            "option(redSB);",
            f"ideal I={generators};",
            "ideal G=slimgb(I);",
            'print("BASIS_SIZE");',
            "size(G);",
            'print("NORMAL_FORM_OF_ONE");',
            "reduce(1,G);",
            "quit;",
        ]
    )


def run(q_degree: int):
    executable = singular_executable()
    if executable is None:
        raise RuntimeError("Singular was not found; install it with `brew install singular`")

    for chart in (1, 2):
        variables, equations = normalized_chart(q_degree, chart)
        completed = subprocess.run(
            [executable, "-q"],
            input=singular_program(variables, equations),
            text=True,
            capture_output=True,
            check=True,
        )
        lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
        try:
            basis_index = lines.index("BASIS_SIZE")
            normal_index = lines.index("NORMAL_FORM_OF_ONE")
            basis_size = lines[basis_index + 1]
            normal_form = lines[normal_index + 1]
        except (ValueError, IndexError) as error:
            raise RuntimeError(
                f"could not parse Singular output:\n{completed.stdout}"
            ) from error
        print(
            f"chart {chart}: {len(variables)} variables, "
            f"{len(equations)} nonzero equations"
        )
        print(f"  reduced Groebner basis size: {basis_size}")
        print(f"  normal form of 1: {normal_form}")
        if basis_size != "1" or normal_form != "0":
            raise AssertionError(f"chart {chart} was not certified empty")

    print(
        "verified over Q: no ordered Darboux pair has "
        f"deg(P) <= 2 and deg(Q) <= {q_degree}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q-degree", type=int, choices=(5, 6), default=6)
    args = parser.parse_args()
    run(args.q_degree)


if __name__ == "__main__":
    main()
