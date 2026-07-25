#!/usr/bin/env python3
"""Exact identities for global/Pfaff obstructions on the quadratic pseudoplane.

This verifier supports four structural statements documented in
``current_context/QUADRATIC_PSEUDOPLANE_GLOBAL_DARBOUX_AUDIT.md``:

* the Laurent symplectic presentation and the weight-minus-one Pfaff ODE;
* reduction of all finite-weight eigenvectors to one auxiliary variable;
* an adversarial Laurent-cylinder Darboux pair whose Pfaff potential
  cannot be homogenized by any polynomial target symplectomorphism;
* the standard locally nilpotent Hamiltonian and the divisor identities
  used in the class-group collision theorem.

The class-group, slice-theorem, and polynomial-PDE conclusions are proofs
over arbitrary degrees; the script checks their exact algebraic identities,
not a bounded coefficient search.
"""

from __future__ import annotations

import sympy as sp


r, w, s = sp.symbols("r w s", nonzero=True)


def bracket_rw(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.factor(
        sp.diff(left, r) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, r)
    )


def euler_rw(polynomial: sp.Expr) -> sp.Expr:
    return sp.expand(
        -2 * r * sp.diff(polynomial, r)
        + w * sp.diff(polynomial, w)
    )


def verify_pseudoplane_laurent_chart() -> None:
    u = 1 / r
    v = r**2 * w**2 - r
    assert sp.factor(w**2 - u - u**2 * v) == 0
    assert bracket_rw(u, v) == -2 * w
    assert bracket_rw(u, w) == -u**2
    assert sp.factor(bracket_rw(v, w) - (1 + 2 * u * v)) == 0


def verify_weight_minus_one_ode() -> None:
    """Check the Pfaff eigen-ODE and its Picard--Vessiot parametrization."""
    index = sp.symbols("i", integer=True)
    A = sp.Function("A")(s)
    F = sp.Function("F")(s)

    def bracket_sw(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.expand(
            w**2
            * (
                sp.diff(left, s) * sp.diff(right, w)
                - sp.diff(left, w) * sp.diff(right, s)
            )
        )

    h = A / w
    homogeneous = w**index * F
    expected = -w**index * (
        A * sp.diff(F, s) + index * sp.diff(A, s) * F
    )
    assert sp.simplify(bracket_sw(homogeneous, h) - expected) == 0

    R = sp.Function("R")(s)
    p_solution = A ** (-index) * R ** (index + 1)
    q_solution = A ** (-index) * R**index
    r_rule = {sp.diff(R, s): R / A}
    p_equation = (
        A * sp.diff(p_solution, s)
        + index * sp.diff(A, s) * p_solution
        - (index + 1) * p_solution
    )
    q_equation = (
        A * sp.diff(q_solution, s)
        + index * sp.diff(A, s) * q_solution
        - index * q_solution
    )
    assert sp.simplify(p_equation.xreplace(r_rule)) == 0
    assert sp.simplify(q_equation.xreplace(r_rule)) == 0

    # With Y=wR/A one has {R,Y}=Y^2.  This is checked after replacing
    # R'=R/A, without asking SymPy to represent a differential extension.
    Y = w * R / A
    bracket_R_Y = bracket_sw(R, Y).xreplace(r_rule)
    assert sp.simplify(bracket_R_Y - Y**2) == 0

    X, Y_symbol = sp.symbols("X Y", nonzero=True)
    p = sp.Function("p")(Y_symbol)
    q = sp.Function("q")(Y_symbol)
    # In the bracket {X,Y}=Y^2, P=X p(Y), Q=q(Y).
    reduced_bracket = sp.diff(X * p, X) * sp.diff(q, Y_symbol) * Y_symbol**2
    assert reduced_bracket == Y_symbol**2 * p * sp.diff(q, Y_symbol)


def verify_adversarial_pfaff_pair() -> None:
    """A Darboux pair whose potential resists target homogenization."""
    P = r**2
    Q = w / (2 * r) + r / 2
    h = sp.Rational(3, 2) * r * w - r**3 / 6
    assert bracket_rw(P, Q) == 1
    assert sp.factor(
        bracket_rw(P, h) + euler_rw(P) + P
    ) == 0
    assert sp.factor(
        bracket_rw(Q, h) + euler_rw(Q)
    ) == 0

    # beta=w dr+2r dw=P dQ+dh.
    beta_minus_pfaff_dr = (
        w - P * sp.diff(Q, r) - sp.diff(h, r)
    )
    beta_minus_pfaff_dw = (
        2 * r - P * sp.diff(Q, w) - sp.diff(h, w)
    )
    assert sp.factor(beta_minus_pfaff_dr) == 0
    assert sp.factor(beta_minus_pfaff_dw) == 0

    # The degree-two field extension Frac(C[r^{+-1},w])/C(P,Q) has
    # involution sigma(r,w)=(-r,-w-2r^2).
    sigma = {r: -r, w: -w - 2 * r**2}
    assert sp.factor(P.xreplace(sigma) - P) == 0
    assert sp.factor(Q.xreplace(sigma) - Q) == 0
    h_sigma = sp.expand(h.xreplace(sigma))
    assert sp.factor(h - h_sigma + sp.Rational(10, 3) * r**3) == 0

    # The unique weight-minus-one candidate with the same anti-invariant
    # part is H0=5rw/3.  Hence the required target primitive would be
    # K=h-H0=-PQ/3.
    H0 = sp.Rational(5, 3) * r * w
    K = sp.factor(h - H0)
    assert sp.factor(K + P * Q / 3) == 0

    # If a target symplectomorphism (F,G) had
    # F dG-X dY=d(cXY), then
    # (1+c)X G_X-cY G_Y=0.  At c=-1/3 every nonconstant monomial
    # X^aY^b has eigenvalue (2a+b)/3 != 0.
    a, b = sp.symbols("a b", integer=True, nonnegative=True)
    c = -sp.Rational(1, 3)
    eigenvalue = sp.factor((1 + c) * a - c * b)
    assert sp.simplify(eigenvalue - (2 * a + b) / 3) == 0
    for left_degree in range(8):
        for right_degree in range(8):
            if left_degree + right_degree:
                assert eigenvalue.subs(
                    {a: left_degree, b: right_degree}
                ) != 0


def verify_lnd_and_boundary_divisors() -> None:
    u, v = sp.symbols("u v")

    def d_u(polynomial: sp.Expr) -> sp.Expr:
        return sp.expand(
            -2 * w * sp.diff(polynomial, v)
            - u**2 * sp.diff(polynomial, w)
        )

    assert d_u(u) == 0
    assert d_u(w) == -u**2
    assert d_u(d_u(w)) == 0
    assert d_u(v) == -2 * w
    assert d_u(d_u(v)) == 2 * u**2
    assert d_u(d_u(d_u(v))) == 0

    # On w=0 the equation factors into the two disjoint reduced boundary
    # components D=(u,w) and H=(1+uv,w).
    assert sp.factor(u * (1 + u * v)) == u * (u * v + 1)
    assert sp.gcd(sp.Poly(u, u, v), sp.Poly(1 + u * v, u, v)) == 1


def verify_known_etale_endomorphism() -> None:
    """Check the degree-two pseudo-plane endomorphism and its multiplier."""
    u = 1 / r
    v = r**2 * w**2 - r
    uv = sp.factor(u * v)
    U = w**2
    V = 4 * v
    W = w * (1 + 2 * uv)
    assert sp.factor(W**2 - U - U**2 * V) == 0
    assert sp.factor(bracket_rw(U, V) - 4 * (-2 * W)) == 0
    assert sp.factor(bracket_rw(U, W) - 4 * (-U**2)) == 0
    assert sp.factor(
        bracket_rw(V, W) - 4 * (1 + 2 * U * V)
    ) == 0


def main() -> None:
    verify_pseudoplane_laurent_chart()
    verify_weight_minus_one_ode()
    verify_adversarial_pfaff_pair()
    verify_lnd_and_boundary_divisors()
    verify_known_etale_endomorphism()
    print("verified: weight-minus-one Pfaff eigenvector reduction")
    print("verified: non-homogenizable Laurent Pfaff countermodel")
    print("verified: LND and class-group boundary identities")
    print("verified: known degree-two etale pseudoplane endomorphism")
    print("RESULT: QUADRATIC PSEUDOPLANE GLOBAL STRUCTURE PASSES")


if __name__ == "__main__":
    main()
