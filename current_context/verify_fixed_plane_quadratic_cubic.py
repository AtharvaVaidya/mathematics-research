#!/usr/bin/env python3
"""Exclude fixed-plane pairs of target degrees at most two and three.

The nonsquare leading-coefficient theorem handles every quadratic
Hamiltonian whose c^2 coefficient is not a square.  On the square locus,
write that coefficient as

    (h0+h1*t+h2*t^2+h3*t^3)^2.

The absent t term forces h0*h1=0.  Up to scaling there are four affine
charts.  This verifier constructs the full coefficient equations for an
arbitrary partner of target degree at most three and asks Singular for the
exact Gröbner basis over Q on every chart.
"""

from pathlib import Path
import shutil
import subprocess

import sympy as sp


SINGULAR = shutil.which("Singular")
if SINGULAR is None:
    raise RuntimeError("Singular is required for this exact verifier")

t, c = sp.symbols("t c")
A, B, C = sp.symbols("A B C")
h0, h1, h2, h3 = sp.symbols("h0 h1 h2 h3")
linear_a, linear_b, linear_c = sp.symbols(
    "linear_a linear_b linear_c"
)
partner_coefficients = sp.symbols("v0:19")

a = sp.expand(t + t**2 - c * t**3)
b = sp.expand(2 + 4 * t - 3 * c * t**2)

# The unique quadratic target form whose leading c coefficient is h^2.
coefficient_aa = h3**2
coefficient_ab = sp.Rational(2, 3) * h3 * h2
coefficient_ac = -2 * (h3 * h0 + h2 * h1)
coefficient_bb = (h2**2 + 2 * h3 * h1) / 9
coefficient_bc = -(h1**2 + 2 * h2 * h0) / 3
coefficient_cc = h0**2

hamiltonian = sp.expand(
    coefficient_aa * a**2
    + coefficient_ab * a * b
    + coefficient_ac * a * c
    + coefficient_bb * b**2
    + coefficient_bc * b * c
    + coefficient_cc * c**2
    + linear_a * a
    + linear_b * b
    + linear_c * c
)
leading_c2 = sp.Poly(hamiltonian, c).coeff_monomial(c**2)
h = h0 + h1 * t + h2 * t**2 + h3 * t**3
assert sp.expand(leading_c2 - h**2 + 2 * h0 * h1 * t) == 0

target_monomials: list[sp.Expr] = []
for total_degree in range(1, 4):
    for exponent_a in range(total_degree, -1, -1):
        for exponent_b in range(
            total_degree - exponent_a, -1, -1
        ):
            exponent_c = total_degree - exponent_a - exponent_b
            target_monomials.append(
                A**exponent_a * B**exponent_b * C**exponent_c
            )
assert len(target_monomials) == 19

partner = sp.expand(
    sum(
        coefficient
        * monomial.subs({A: a, B: b, C: c})
        for coefficient, monomial in zip(
            partner_coefficients, target_monomials
        )
    )
)

charts = [
    (
        "h0=0,h1=1",
        {h0: 0, h1: 1},
        [h2, h3],
    ),
    (
        "h0=1,h1=0",
        {h0: 1, h1: 0},
        [h2, h3],
    ),
    (
        "h0=h1=0,h2=1",
        {h0: 0, h1: 0, h2: 1},
        [h3],
    ),
    (
        "h0=h1=h2=0,h3=1",
        {h0: 0, h1: 0, h2: 0, h3: 1},
        [],
    ),
]


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


for chart_name, substitutions, free_h in charts:
    # Clearing the fixed denominators by multiplying U by 9 is harmless:
    # a partner rescales inversely.
    chart_hamiltonian = sp.expand(
        9 * hamiltonian.subs(substitutions)
    )
    bracket_defect = sp.Poly(
        sp.expand(
            sp.diff(chart_hamiltonian, t) * sp.diff(partner, c)
            - sp.diff(chart_hamiltonian, c) * sp.diff(partner, t)
            - 1
        ),
        t,
        c,
    )
    equations = [coefficient for _, coefficient in bracket_defect.terms()]
    variables = (
        free_h
        + [linear_a, linear_b, linear_c]
        + list(partner_coefficients)
    )
    script = (
        "option(redSB);\n"
        f"ring r=0,({','.join(map(str, variables))}),dp;\n"
        f"ideal I={','.join(singular(eq) for eq in equations)};\n"
        "ideal G=std(I);\n"
        'if (size(G)==1 && string(G[1])==\"1\") '
        '{ print(\"UNIT_IDEAL\"); } '
        'else { print(\"NONUNIT\"); G; }\n'
        "quit;\n"
    )
    result = subprocess.run(
        [SINGULAR, "--no-tty"],
        input=script,
        text=True,
        capture_output=True,
        check=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    if "UNIT_IDEAL" not in result.stdout:
        raise AssertionError(
            f"unresolved square-leading chart {chart_name}:\n"
            f"{result.stdout}\n{result.stderr}"
        )
    print(f"verified rational unit ideal on chart {chart_name}")

print(
    "RESULT: NO FIXED-PLANE PAIR WITH TARGET DEGREES <= 2 AND <= 3"
)
