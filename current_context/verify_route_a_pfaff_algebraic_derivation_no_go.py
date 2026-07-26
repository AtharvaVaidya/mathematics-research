#!/usr/bin/env python3
"""Exact checks for the Route A Pfaff algebraic-flow obstruction.

The theorem-level argument is recorded in
``current_context/ROUTE_A_PFAFF_ALGEBRAIC_DERIVATION_NO_GO.md``.
This script checks:

* the Pfaff eigenfunction/invariant identities on the Laurent chart;
* the standard weight -1 versus weight 0 bracket formula;
* a family of affine-modification countermodels showing that constant
  units plus finite function-field degree do not force local finiteness.
"""

from __future__ import annotations

import sympy as sp


r, w = sp.symbols("r w", nonzero=True)


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """The bracket {r,w}=1 on the Laurent chart."""
    return sp.factor(
        sp.diff(left, r) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, r)
    )


def euler(polynomial: sp.Expr) -> sp.Expr:
    """The standard Euler derivation in r=1/u,w coordinates."""
    return sp.expand(
        -2 * r * sp.diff(polynomial, r)
        + w * sp.diff(polynomial, w)
    )


def verify_pfaff_delta() -> None:
    """Check Delta(P)=P and Delta(Q)=0 in the exact Laurent Pfaff model."""
    P = r**2
    Q = w / (2 * r) + r / 2
    h = sp.Rational(3, 2) * r * w - r**3 / 6

    def delta(polynomial: sp.Expr) -> sp.Expr:
        return sp.factor(bracket(h, polynomial) - euler(polynomial))

    assert bracket(P, Q) == 1
    assert sp.factor(delta(P) - P) == 0
    assert sp.factor(delta(Q)) == 0

    # Here Delta is locally finite: this is the complementary Laurent
    # warning, where nonconstant units remain.
    assert sp.factor(delta(r) - r / 2) == 0
    assert sp.factor(delta(w) - (w - r**2) / 2) == 0


def verify_terminal_homogeneous_formula() -> None:
    """Check {vw A(uv), F(uv)}=s(1+s) A(s)F'(s)."""
    # On u != 0, one has u=1/r, v=r^2 w^2-r=r*s and s=uv=rw^2-1.
    s = r * w**2 - 1
    xi = sp.symbols("xi")
    A = sp.Function("A")
    F = sp.Function("F")
    p = r * w * s * A(s)
    q = F(s)
    derivative = sp.diff(F(xi), xi).subs(xi, s)
    expected = s * (1 + s) * A(s) * derivative

    assert sp.factor(bracket(p, q) - expected) == 0
    assert sp.factor(euler(p) + p) == 0
    assert sp.factor(euler(q)) == 0


def verify_affine_modification_countermodels() -> None:
    """Check the non-locally-finite family for representative d."""
    a, z = sp.symbols("a z")

    for d in range(1, 9):
        P = a**d * z
        Q = a**d * (1 - z)

        def derivation(polynomial: sp.Expr) -> sp.Expr:
            return sp.factor(
                a * z * sp.diff(polynomial, a) / d
                + z * (1 - z) * sp.diff(polynomial, z)
            )

        assert sp.factor(derivation(P) - P) == 0
        assert sp.factor(derivation(Q)) == 0
        assert sp.factor(P + Q - a**d) == 0

        jacobian = sp.factor(
            sp.diff(P, a) * sp.diff(Q, z)
            - sp.diff(P, z) * sp.diff(Q, a)
        )
        assert sp.factor(jacobian + d * a ** (2 * d - 1)) == 0

        # Iterates of z have strictly increasing z-degree.  The note
        # proves this for every iterate from the leading term.
        iterate = z
        for order in range(1, 9):
            iterate = sp.expand(derivation(iterate))
            assert sp.degree(iterate, z) == order + 1
            assert sp.LC(sp.Poly(iterate, z)) != 0


def main() -> None:
    verify_pfaff_delta()
    verify_terminal_homogeneous_formula()
    verify_affine_modification_countermodels()
    print("verified: Pfaff Delta has eigenfunction P and invariant Q")
    print("verified: standard weight (-1,0) bracket has s(1+s) factor")
    print("verified: finite-degree affine modifications are non-locally-finite")
    print("RESULT: ROUTE A PFAFF ALGEBRAIC-FLOW OBSTRUCTION PASSES")


if __name__ == "__main__":
    main()
