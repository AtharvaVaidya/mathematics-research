#!/usr/bin/env python3
"""Exact identities for the Route A homogeneous-Pfaff obstruction.

The degree-independent proofs are recorded in
``current_context/ROUTE_A_PFAFF_WEIGHT_MINUS_ONE_AUDIT.md``.  This script
checks the algebraic identities on which those proofs depend:

* the weight-zero centralizer formula for a nonzero weight-minus-one
  Hamiltonian in the quadratic pseudoplane;
* cancellation of the two Pfaff eigenvalues in complementary weights;
* an exact Laurent Darboux pair whose Pfaff potential cannot be made
  homogeneous by a polynomial target symplectomorphism.
"""

from __future__ import annotations

import sympy as sp


r, w = sp.symbols("r w", nonzero=True)


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """The Laurent-chart bracket {r,w}=1."""
    return sp.factor(
        sp.diff(left, r) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, r)
    )


def euler(polynomial: sp.Expr) -> sp.Expr:
    """The Euler field for wt(r)=-2 and wt(w)=1."""
    return sp.expand(
        -2 * r * sp.diff(polynomial, r)
        + w * sp.diff(polynomial, w)
    )


def verify_weight_zero_centralizer_identity() -> None:
    # On B[u^{-1}], s=uv=rw^2-1.  Every element of B of weight zero is
    # F(s), and every element of B of weight -1 is h=vw A(s)=rw*s*A(s).
    s = r * w**2 - 1
    xi = sp.symbols("xi")
    A = sp.Function("A")
    F = sp.Function("F")
    h = r * w * s * A(s)
    weight_zero = F(s)
    derivative = sp.diff(F(xi), xi).subs(xi, s)
    expected = -s * (1 + s) * A(s) * derivative
    assert sp.factor(bracket(weight_zero, h) - expected) == 0

    # If j=-i-1, then {P_i,Q_j} has weight zero and the eigenvalues of
    # the right Hamiltonian derivation delta_h={-,h} add to zero.
    i = sp.symbols("i", integer=True)
    j = -i - 1
    assert sp.simplify(i + j + 1) == 0
    assert sp.simplify(-(i + 1) - j) == 0


def verify_nonhomogenizable_laurent_pair() -> None:
    P = r**2
    Q = w / (2 * r) + r / 2
    h = sp.Rational(3, 2) * r * w - r**3 / 6

    assert bracket(P, Q) == 1
    assert sp.factor(bracket(P, h) + euler(P) + P) == 0
    assert sp.factor(bracket(Q, h) + euler(Q)) == 0

    # beta=w dr+2r dw=P dQ+dh.
    assert sp.factor(w - P * sp.diff(Q, r) - sp.diff(h, r)) == 0
    assert sp.factor(2 * r - P * sp.diff(Q, w) - sp.diff(h, w)) == 0

    # Frac(k[r^{+-1},w])/k(P,Q) is quadratic.  Its involution fixes P,Q.
    sigma = {r: -r, w: -w - 2 * r**2}
    assert sp.factor(P.xreplace(sigma) - P) == 0
    assert sp.factor(Q.xreplace(sigma) - Q) == 0
    h_sigma = sp.expand(h.xreplace(sigma))
    assert sp.factor(h - h_sigma + sp.Rational(10, 3) * r**3) == 0

    # The proof in the memo shows that the unique homogeneous
    # weight-minus-one Laurent polynomial with this anti-invariant part
    # is H0=5rw/3.
    H0 = sp.Rational(5, 3) * r * w
    H0_sigma = sp.expand(H0.xreplace(sigma))
    assert sp.factor(H0 - H0_sigma + sp.Rational(10, 3) * r**3) == 0
    K = sp.factor(h - H0)
    assert sp.factor(K + P * Q / 3) == 0

    # Were a polynomial target change (F,G) to replace h by H0, it
    # would obey F dG-X dY=d(cXY), c=-1/3.  Eliminating F gives the
    # displayed weighted Euler equation for G.  Its polynomial kernel
    # consists only of constants because 2a+b>0 for every nonconstant
    # monomial X^aY^b.
    a, b = sp.symbols("a b", integer=True, nonnegative=True)
    c = -sp.Rational(1, 3)
    eigenvalue = sp.factor((1 + c) * a - c * b)
    assert sp.simplify(eigenvalue - (2 * a + b) / 3) == 0


def main() -> None:
    verify_weight_zero_centralizer_identity()
    verify_nonhomogenizable_laurent_pair()
    print("verified: weight-zero centralizer identity")
    print("verified: complementary Pfaff eigenvalue cancellation")
    print("verified: nonhomogenizable Laurent Pfaff countermodel")
    print("RESULT: ROUTE A PFAFF HOMOGENEOUS OBSTRUCTION PASSES")


if __name__ == "__main__":
    main()
