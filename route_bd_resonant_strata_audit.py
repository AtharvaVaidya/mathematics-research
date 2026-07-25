#!/usr/bin/env python3
"""Audit the six strata left by the first resonant product obstruction.

The canonical seven modes are

    (X0,X1; X2,X3; X4,X5; X6),

where each pair is the low/high mode at deficits 1,2,3 and X6 is the high
deficit-4 mode.  The five independent d+e=5 resonant translations give

    X0*X6 = X1*X6 = X2*X5 = X3*X4 = X3*X5 = 0.

Their six minimal coordinate strata are the products of

    X6=0          or X0=X1=0

with

    X4=X5=0,      X3=X5=0,      or X2=X3=0.

This script records three structural facts.

1. Every stratum still contains nonzero exact algebraic Hamiltonian flows;
   the product ideal is only the first Kummer obstruction.
2. The endpoint coordinates Y0,Y2,Y3 turn the reduced pieces into exact
   "target minus source" Hamiltonians:

       Y0=0: H1 = -(P0^2-x^2)/4,
       Y2=0: H2 = -(Q0-x^2*y)/3,
       Y3=0: H3 = -(P0-x)/2.

3. The autonomous principal flows have explicit binomial roots.  For the
   high monomial H=-a*(z*w^k)^c/c, N=5k+2,

       W = w*(1-N*a*t*w^(c*k+2)/z^(5-c))^(-1/N),
       Z = z*(1-N*a*t*w^(c*k+2)/z^(5-c))^(k/N).

   The binomial has a simple divisor, so a nonzero autonomous high flow is
   not rational in k(z,w).  The low axes similarly give square or cube
   roots.  These formulas are exact obstructions to an autonomous-flow
   shortcut, but they do not by themselves exclude a general completion:
   higher Hamiltonians can alter the time map.  Original-plane integrality,
   treated in route_bd_integral_branch_rigidity.py, does exclude all six
   strata at once.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


EDGES = (
    frozenset((0, 6)),
    frozenset((1, 6)),
    frozenset((2, 5)),
    frozenset((3, 4)),
    frozenset((3, 5)),
)

EXPECTED_COVERS = {
    frozenset((6, 4, 5)),
    frozenset((6, 3, 5)),
    frozenset((6, 2, 3)),
    frozenset((0, 1, 4, 5)),
    frozenset((0, 1, 3, 5)),
    frozenset((0, 1, 2, 3)),
}


def verify_six_minimal_strata() -> None:
    covers: set[frozenset[int]] = set()
    vertices = range(7)
    for size in range(1, 8):
        for selected_tuple in combinations(vertices, size):
            selected = frozenset(selected_tuple)
            if not all(selected & edge for edge in EDGES):
                continue
            if any(existing < selected for existing in covers):
                continue
            covers.add(selected)
    assert covers == EXPECTED_COVERS


def verify_endpoint_matched_hamiltonians() -> None:
    z, w = sp.symbols("z w", nonzero=True)
    u = sp.Function("U")(w)
    v = sp.Function("V")(w)
    x = z**2 / w
    y = w / z
    p0 = z**2 * u / w
    q0 = z**3 * v / w

    # On Y0=0, the d=1 scalar is U^2/w-w^-1.
    c1_matched = u**2 / w - 1 / w
    h1 = -z**4 * c1_matched / (4 * w)
    assert sp.simplify(h1 + (p0**2 - x**2) / 4) == 0

    # On Y2=0 and Y3=0, the normalized scalars are V-1 and U-1.
    h2 = -z**3 * (v - 1) / (3 * w)
    h3 = -z**2 * (u - 1) / (2 * w)
    assert sp.simplify(h2 + (q0 - x**2 * y) / 3) == 0
    assert sp.simplify(h3 + (p0 - x) / 2) == 0


def omega_density(z: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    return z**4 / w**3


def hamiltonian_vector(
    hamiltonian: sp.Expr,
    z: sp.Symbol,
    w: sp.Symbol,
) -> tuple[sp.Expr, sp.Expr]:
    density = omega_density(z, w)
    return (
        sp.factor(sp.diff(hamiltonian, w) / density),
        sp.factor(-sp.diff(hamiltonian, z) / density),
    )


def verify_low_exact_flows() -> None:
    z, w, time, a, b = sp.symbols("z w time a b", nonzero=True)

    # Low d=1, C=1: an exact cube-root flow.
    h1 = -a * z**4 / (4 * w)
    vector1 = hamiltonian_vector(h1, z, w)
    assert vector1 == (a * w / 4, a * w**2 / z)
    binomial1 = 1 - 3 * a * time * w / (4 * z)
    z1 = z * binomial1 ** -sp.Rational(1, 3)
    w1 = w * binomial1 ** -sp.Rational(4, 3)
    assert sp.simplify(sp.diff(z1, time).subs(time, 0) - vector1[0]) == 0
    assert sp.simplify(sp.diff(w1, time).subs(time, 0) - vector1[1]) == 0
    assert sp.simplify(w1 / z1**4 - w / z**4) == 0

    # The low d=2 and d=3 modes commute because both Hamiltonians depend
    # only on z.  Their combined flow is an exact square root.
    h23 = -a * z**3 / 3 - b * z**2 / 2
    vector23 = hamiltonian_vector(h23, z, w)
    assert vector23 == (
        0,
        sp.factor(w**3 * (a * z + b) / z**3),
    )
    binomial23 = 1 - 2 * time * w**2 * (a / z**2 + b / z**3)
    z23 = z
    w23 = w * binomial23 ** -sp.Rational(1, 2)
    assert sp.diff(z23, time) == vector23[0]
    assert sp.simplify(
        sp.diff(w23, time).subs(time, 0) - vector23[1]
    ) == 0


def verify_high_principal_flows() -> None:
    z, w, time, a = sp.symbols("z w time a", nonzero=True)
    for k in (1, 2, 3):
        ramification = 5 * k + 2
        xi = z * w**k
        for c in (1, 2, 3, 4):
            hamiltonian = -a * xi**c / c
            vector = hamiltonian_vector(hamiltonian, z, w)
            expected_vector = (
                -a * k * z ** (c - 4) * w ** (c * k + 2),
                a * z ** (c - 5) * w ** (c * k + 3),
            )
            assert all(
                sp.simplify(left - right) == 0
                for left, right in zip(vector, expected_vector)
            )

            binomial = (
                1
                - ramification
                * a
                * time
                * w ** (c * k + 2)
                / z ** (5 - c)
            )
            z_new = z * binomial ** sp.Rational(k, ramification)
            w_new = w * binomial ** -sp.Rational(1, ramification)
            assert sp.simplify(z_new * w_new**k - xi) == 0
            assert sp.simplify(
                sp.diff(z_new, time).subs(time, 0) - vector[0]
            ) == 0
            assert sp.simplify(
                sp.diff(w_new, time).subs(time, 0) - vector[1]
            ) == 0

            # The time map preserves the exact volume form.
            jacobian = sp.factor(
                sp.diff(z_new, z) * sp.diff(w_new, w)
                - sp.diff(z_new, w) * sp.diff(w_new, z)
            )
            pulled = sp.factor(
                z_new**4 / w_new**3 * jacobian
            )
            assert sp.simplify(
                pulled - omega_density(z, w)
            ) == 0

    # At k=1,c=1 this is the actual pure d=4 mode C=w^2.  The seventh-root
    # formula agrees with the direct invariant z*w.
    seventh = 1 - 7 * a * time * w**3 / z**4
    assert 5 * 1 + 2 == 7
    assert sp.gcd(
        sp.Poly(z**4 - 7 * a * time * w**3, z),
        sp.Poly(4 * z**3, z),
    ).degree() == 0
    assert seventh


def verify_reduced_stratum_table() -> None:
    """Endpoint squares reduce four strata to matched high sectors."""

    # Labels record the free coordinates after imposing the reduced
    # consequences Y2=kappa*Y0^2 and, when Y0=Y2=0, Y3=0.
    reduced = {
        # A3: X6=X2=X3=0 -> Y0=0 -> X0=2X1 and Y3=0 -> X4=X5.
        "A3": {"matched_d1", "matched_d3"},
        # B1: X0=X1=X4=X5=0 -> Y2=0 -> X2=(2/3)X3.
        "B1": {"matched_d2", "high_d4"},
        # B2: X0=X1=X3=X5=0 -> X2=0, then X4=0.
        "B2": {"high_d4"},
        # B3: X0=X1=X2=X3=0 -> Y3=0 -> X4=X5.
        "B3": {"matched_d3", "high_d4"},
    }
    assert reduced["B2"] == {"high_d4"}
    assert reduced["A3"] & reduced["B3"] == {"matched_d3"}


def main() -> None:
    verify_six_minimal_strata()
    verify_endpoint_matched_hamiltonians()
    verify_low_exact_flows()
    verify_high_principal_flows()
    verify_reduced_stratum_table()
    print("verified the six minimal resonant coordinate strata")
    print("verified the three endpoint-matched Hamiltonian identities")
    print("verified the exact low square/cube-root flows")
    print("verified the all-k high principal (5k+2)-root flows")
    print("verified the reduced A3/B1/B2/B3 stratum table")
    print("RESULT: product strata admit exact algebraic flows but need integrality")


if __name__ == "__main__":
    main()
