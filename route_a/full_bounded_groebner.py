#!/usr/bin/env python3
"""Generate and exactly eliminate the full bounded Darboux system.

This search includes every coefficient of *both* P and Q of a common
generator-total-degree bound.  It uses the forced SL_2 normalization of the
linear (v,w)-jets and asks Singular for a Groebner basis over Q.

The degree-three and degree-four runs are separate from verify_all.py because they
requires the external Singular executable.  On macOS it can be installed with

    brew install singular

The supported certified bounds are 2, 3, and 4.  A result "[1]" proves emptiness
only for the displayed common degree bound, not global nonexistence.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

import sympy as sp


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import basis, bracket  # noqa: E402


def normalized_system(degree: int):
    monomials = basis(degree, include_constant=False)
    v_index = monomials.index((0, 1, 0))
    w_index = monomials.index((0, 0, 1))
    free_indices = [
        index for index in range(len(monomials)) if index not in (v_index, w_index)
    ]
    p_variables = sp.symbols(f"p0:{len(free_indices)}")
    q_variables = sp.symbols(f"q0:{len(free_indices)}")
    P = {(0, 1, 0): sp.Integer(1)}
    Q = {(0, 0, 1): sp.Integer(1)}
    P.update({monomials[index]: variable for index, variable in zip(free_indices, p_variables)})
    Q.update({monomials[index]: variable for index, variable in zip(free_indices, q_variables)})
    answer = bracket(P, Q)
    support = sorted(set(answer).union({(0, 0, 0)}))
    equations = [
        sp.expand(answer.get(monomial, 0) - (1 if monomial == (0, 0, 0) else 0))
        for monomial in support
    ]
    equations = [equation for equation in equations if equation != 0]
    return p_variables + q_variables, equations


def singular_executable():
    candidates = [
        shutil.which("Singular"),
        "/opt/homebrew/bin/Singular",
        "/usr/local/bin/Singular",
    ]
    return next((candidate for candidate in candidates if candidate and Path(candidate).is_file()), None)


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


def run(degree: int):
    if degree not in (2, 3, 4):
        raise ValueError("the currently certified full bounds are 2, 3, and 4")
    executable = singular_executable()
    if executable is None:
        raise RuntimeError("Singular was not found; install it with `brew install singular`")
    variables, equations = normalized_system(degree)
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
        raise RuntimeError(f"could not parse Singular output:\n{completed.stdout}") from error
    print(
        f"full normalized degree <= {degree} system: "
        f"{len(variables)} variables, {len(equations)} nonzero equations"
    )
    print(f"reduced Groebner basis size: {basis_size}")
    print(f"normal form of 1: {normal_form}")
    if basis_size != "1" or normal_form != "0":
        raise AssertionError("the bounded ideal was not certified as the unit ideal")
    print(
        f"verified over Q: no Darboux pair has both generator total degrees <= {degree}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, choices=(2, 3, 4), default=4)
    args = parser.parse_args()
    run(args.degree)


if __name__ == "__main__":
    main()
