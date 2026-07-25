#!/usr/bin/env python3
"""Deterministic weighted-projective unit certificates for case-c n=3.

The affine chart equations used by
``scratch_case_c_n3_generic_charts_Q.py`` come from equations homogeneous
for weights (1,1,2,2,3,3,4).  Rather than homogenizing the normalized
affine charts with an eighth variable, this verifier stays in the original
weighted-homogeneous presentation.  It proves emptiness of a chart by
showing that a power of its chart coordinate belongs to the homogeneous
ideal:

    L != 0      : L^N in (f, F5, F6, selected F7);
    L = 0,A != 0: A^N in (f, L, F5, F6, selected F7).

The preferred backend works directly over the algebraic coefficient field
``Q(s)/(f)`` and uses Singular's ordinary exact ``std`` algorithm.  Thus
the certificate does not rely on a modular reconstruction heuristic.  A
faster experimental backend keeps ``s`` as a weight-zero variable and uses
``modStd``; it is useful for discovery but is not the publication witness.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pickle
import shutil
import subprocess
import time

import sympy as sp

from route_bd_case_c_n3_generic_charts import polynomial_weights
from route_bd_case_c_n3_hurwitz_bridge import (
    NVAR,
    ParameterPolynomial,
    QuotientElement,
    parameter_coefficient,
)
from route_bd_universal_hamiltonian_endpoint_squares import substitute
from scratch_case_c_n3_generic_charts_Q import (
    DEFAULT_CACHE,
    minpoly_text,
    polynomial_text,
)


WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
ZERO_MONOMIAL = (0,) * NVAR
# X2 has already been replaced by (169/48) X0^2 in every imposed row.
ACTIVE_VARIABLES = (0, 1, 3, 4, 5, 6)


def chart_coordinates(
    imposed: list[ParameterPolynomial],
) -> tuple[ParameterPolynomial, ParameterPolynomial, ParameterPolynomial]:
    """Return the unique weight-five row and its chart forms L and A."""
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    zero = QuotientElement.coerce(0)
    one = QuotientElement.coerce(1)
    survivor, = [
        equation
        for equation in imposed
        if equation and polynomial_weights(equation) == {5}
    ]

    linear_form = parameter_coefficient(survivor, 6, 1)
    l_x1 = linear_form.terms[(0, 1, 0, 0, 0, 0, 0)]
    l_y0 = linear_form.terms[(1, 0, 0, 0, 0, 0, 0)]
    assert l_x1 and l_y0
    L = parameters[1] * l_x1 + parameters[0] * l_y0
    assert polynomial_weights(L) == {1}

    x1_on_l_zero = parameters[0] * (-l_y0 / l_x1)
    l_zero_survivor = substitute(
        survivor,
        parameters,
        {1: x1_on_l_zero},
        zero,
        one,
    )
    coefficient_x5 = parameter_coefficient(l_zero_survivor, 5, 1)
    a_x3 = coefficient_x5.terms[(0, 0, 0, 1, 0, 0, 0)]
    a_y0_square = coefficient_x5.terms[(2, 0, 0, 0, 0, 0, 0)]
    assert a_x3 and a_y0_square
    A = parameters[3] * a_x3 + (
        parameters[0] * parameters[0] * a_y0_square
    )
    assert polynomial_weights(A) == {2}
    return survivor, L, A


def change_to_l_coordinate(
    imposed: list[ParameterPolynomial],
    survivor: ParameterPolynomial,
) -> list[ParameterPolynomial]:
    """Use X1 as the new coordinate L, preserving all source weights."""
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    zero = QuotientElement.coerce(0)
    one = QuotientElement.coerce(1)
    linear_form = parameter_coefficient(survivor, 6, 1)
    l_x1 = linear_form.terms[(0, 1, 0, 0, 0, 0, 0)]
    l_y0 = linear_form.terms[(1, 0, 0, 0, 0, 0, 0)]
    old_x1 = (
        parameters[1] - parameters[0] * l_y0
    ) * (one / l_x1)
    changed = [
        substitute(
            equation,
            parameters,
            {1: old_x1},
            zero,
            one,
        )
        for equation in imposed
    ]
    changed_survivor, = [
        equation
        for equation in changed
        if equation and polynomial_weights(equation) == {5}
    ]
    assert (
        parameter_coefficient(changed_survivor, 6, 1).terms
        == parameters[1].terms
    )
    return changed


def rational_weighted_ring(
    variable_order: tuple[int, ...] = ACTIVE_VARIABLES,
) -> str:
    variables = ",".join(
        ("s", *(f"X{i}" for i in variable_order))
    )
    weights = ",".join(
        ("0", *(str(WEIGHTS[index]) for index in variable_order))
    )
    return (
        'LIB "modstd.lib";\n'
        f"ring R=0,({variables}),wp({weights});\n"
        "option(redSB);"
    )


def algebraic_ring(
    eliminant: sp.Poly,
    ordering: str,
    variable_order: tuple[int, ...] = ACTIVE_VARIABLES,
) -> str:
    variables = ",".join(f"X{i}" for i in variable_order)
    weights = ",".join(str(WEIGHTS[index]) for index in variable_order)
    order_text = f"wp({weights})" if ordering == "wp" else ordering
    return (
        f"ring R=(0,s),({variables}),{order_text};\n"
        f"minpoly={minpoly_text(eliminant)};\n"
        "option(redSB);"
    )


def certificate_program(
    label: str,
    eliminant: sp.Poly,
    generators: list[ParameterPolynomial],
    target: ParameterPolynomial,
    max_power: int,
    backend: str,
    expected_power: int,
) -> str:
    if backend in (
        "algebraic-std",
        "algebraic-slimgb",
        "algebraic-dp-slimgb",
        "algebraic-l-lex-slimgb",
        "algebraic-l-wp-slimgb",
        "algebraic-lift",
    ):
        l_elimination = backend in (
            "algebraic-l-lex-slimgb",
            "algebraic-l-wp-slimgb",
        )
        ring = algebraic_ring(
            eliminant,
            (
                "lp"
                if backend == "algebraic-l-lex-slimgb"
                else "dp" if backend == "algebraic-dp-slimgb" else "wp"
            ),
            (
                (0, 3, 4, 5, 6, 1)
                if l_elimination
                else ACTIVE_VARIABLES
            ),
        )
        ideal = ",\n".join(polynomial_text(row) for row in generators)
        standard_basis = (
            "ideal H=slimgb(J);"
            if backend in (
                "algebraic-slimgb",
                "algebraic-dp-slimgb",
                "algebraic-l-lex-slimgb",
                "algebraic-l-wp-slimgb",
            )
            else "ideal H=std(J);"
        )
    else:
        ring = rational_weighted_ring(
            (
                (0, 3, 4, 5, 6, 1)
                if backend == "rational-l-wp-modstd"
                else ACTIVE_VARIABLES
            )
        )
        ideal = ",\n".join(
            (
                minpoly_text(eliminant),
                *(polynomial_text(row) for row in generators),
            )
        )
        standard_basis = "ideal H=modStd(J,1);"
    if backend == "rational-modsyz":
        augmented = ",\n".join(
            (
                minpoly_text(eliminant),
                *(polynomial_text(row) for row in generators),
                f"({polynomial_text(target)})^{expected_power}",
            )
        )
        return "\n".join(
            (
                ring,
                f"ideal M=\n{augmented};",
                'if (homog(M)!=1) { print("ERROR NONHOMOGENEOUS INPUT"); exit; }',
                "module S=modSyz(M);",
                "int exactzero=0;",
                "int last=ncols(M);",
                "poly check;",
                "for (int column=1; column<=ncols(S); column++) {",
                "  if (S[column][last]==1 || S[column][last]==-1) {",
                "    check=0;",
                "    for (int row=1; row<=last; row++) {",
                "      check=check+M[row]*S[column][row];",
                "    }",
                "    if (check==0) { exactzero=1; break; }",
                "  }",
                "}",
                f'print("Q5 WEIGHTED {label} TARGET_POWER '
                f'{expected_power}");',
                f'print("Q5 WEIGHTED {label} EXACT_REMAINDER_ZERO "'
                "+string(exactzero));",
            )
        )
    homogeneity_check = (
        ()
        if backend in (
            "algebraic-dp-slimgb",
            "algebraic-l-lex-slimgb",
        )
        else (
            'if (homog(J)!=1) { '
            'print("ERROR NONHOMOGENEOUS INPUT"); exit; }',
        )
    )
    if backend == "algebraic-lift":
        return "\n".join(
            (
                ring,
                f"ideal J=\n{ideal};",
                f"poly target={polynomial_text(target)};",
                *homogeneity_check,
                f"ideal T=target^{expected_power};",
                "matrix U;",
                'matrix C=lift(J,T,U,"slimgb");',
                "matrix E=matrix(T)*U-matrix(J)*C;",
                "ideal Rem=ideal(E);",
                "int exactzero=(size(Rem)==0);",
                f'print("Q5 WEIGHTED {label} TARGET_POWER '
                f'{expected_power}");',
                f'print("Q5 WEIGHTED {label} EXACT_REMAINDER_ZERO "'
                "+string(exactzero));",
            )
        )
    return "\n".join(
        (
            ring,
            f"ideal J=\n{ideal};",
            f"poly target={polynomial_text(target)};",
            *homogeneity_check,
            standard_basis,
            "int targetpower=0;",
            "poly tp=1;",
            f"for (int exponent=1; exponent<={max_power}; exponent++) {{",
            "  tp=tp*target;",
            "  if (reduce(tp,H)==0) { targetpower=exponent; break; }",
            "}",
            f'print("Q5 WEIGHTED {label} TARGET_POWER "'
            '+string(targetpower));',
            f'if (targetpower>0) {{ print("Q5 WEIGHTED {label} '
            'EXACT_REMAINDER_ZERO 1"); }',
        )
    )


def run_chart(
    label: str,
    eliminant: sp.Poly,
    generators: list[ParameterPolynomial],
    target: ParameterPolynomial,
    max_power: int,
    backend: str,
    expected_power: int,
) -> int:
    start = time.monotonic()
    result = subprocess.run(
        ["Singular", "-q"],
        input=certificate_program(
            label,
            eliminant,
            generators,
            target,
            max_power,
            backend,
            expected_power,
        ),
        text=True,
        capture_output=True,
        check=True,
    )
    output = result.stdout + result.stderr
    assert "error occurred" not in output.lower(), output
    assert "ERROR NONHOMOGENEOUS INPUT" not in output, output
    marker = f"Q5 WEIGHTED {label} TARGET_POWER "
    line = next(
        (line for line in output.splitlines() if marker in line),
        None,
    )
    assert line is not None, output
    exponent = int(line.rsplit(" ", 1)[1])
    assert exponent > 0, output
    assert (
        f"Q5 WEIGHTED {label} EXACT_REMAINDER_ZERO 1" in output
    ), output
    print(output.strip(), flush=True)
    print(
        f"Q5 WEIGHTED {label} EXACT IN {time.monotonic() - start:.1f}s",
        flush=True,
    )
    return exponent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chart",
        choices=("all", "L_NE_0", "L_EQ_0_A_NE_0"),
        default="all",
    )
    parser.add_argument("--max-power", type=int, default=256)
    parser.add_argument(
        "--backend",
        choices=(
            "algebraic-std",
            "algebraic-slimgb",
            "algebraic-dp-slimgb",
            "algebraic-l-lex-slimgb",
            "algebraic-l-wp-slimgb",
            "algebraic-lift",
            "rational-modstd",
            "rational-l-wp-modstd",
            "rational-modsyz",
        ),
        default="algebraic-std",
        help=(
            "choose an exact algebraic-field certificate backend or an "
            "experimental rational modular backend"
        ),
    )
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    args = parser.parse_args()
    assert shutil.which("Singular")
    assert args.cache.exists(), "run exact-Q reconstruction verifier first"

    with args.cache.open("rb") as stream:
        cache = pickle.load(stream)
    s, eliminant, _, _ = cache["outer"]
    exact_imposed = cache["imposed"]
    assert eliminant.gens == (s,)
    QuotientElement.configure(eliminant)

    survivor, L, A = chart_coordinates(exact_imposed)
    if args.backend in (
        "algebraic-l-lex-slimgb",
        "algebraic-l-wp-slimgb",
        "rational-l-wp-modstd",
    ):
        assert args.chart == "L_NE_0"
        exact_imposed = change_to_l_coordinate(exact_imposed, survivor)
        survivor, = [
            equation
            for equation in exact_imposed
            if equation and polynomial_weights(equation) == {5}
        ]
        L = ParameterPolynomial.variable(1)
    weight_six = [
        equation
        for equation in exact_imposed
        if equation and polynomial_weights(equation) == {6}
    ]
    weight_seven = [
        equation
        for equation in exact_imposed
        if equation and polynomial_weights(equation) == {7}
    ]
    assert len(weight_six) == 3
    assert len(weight_seven) == 5

    requested = (
        ("L_NE_0", "L_EQ_0_A_NE_0")
        if args.chart == "all"
        else (args.chart,)
    )
    for chart in requested:
        if chart == "L_NE_0":
            # This is the same minimal deficit-seven choice (0,1) as in
            # the normalized affine computation.
            generators = [survivor, *weight_six, *weight_seven[:2]]
            target = L
            expected_power = 23
        else:
            assert args.backend not in (
                "algebraic-l-lex-slimgb",
                "algebraic-l-wp-slimgb",
                "rational-l-wp-modstd",
            )
            # This is the same minimal deficit-seven choice (0,) after
            # imposing L=0.
            generators = [L, survivor, *weight_six, weight_seven[0]]
            target = A
            expected_power = 8
        run_chart(
            chart,
            eliminant,
            generators,
            target,
            args.max_power,
            args.backend,
            expected_power,
        )
    print("RESULT: REQUESTED WEIGHTED-PROJECTIVE CHARTS CERTIFIED EXACTLY")


if __name__ == "__main__":
    main()
