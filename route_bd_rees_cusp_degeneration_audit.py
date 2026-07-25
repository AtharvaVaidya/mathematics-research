#!/usr/bin/env python3
"""Exact checks for the Rees/cusp-complement audit.

This verifier checks the algebraic identities in
``current_context/REES_CUSP_DEGENERATION_AUDIT.md``.  It does not claim
that the total Rees map is finite.  The point of the audit is precisely
that two additional statements would be needed:

* the critical-line identity q(y)^2 = L*p(y)^3; and
* containment of the relative nonproper-value set in the fixed cusp.

The pure-power conclusion uses these assumptions:

* the constant field is algebraically closed of characteristic zero;
* L is nonzero and the full vertical vertices give
  deg(p)=8, deg(q)=12;
* p and q satisfy q^2=L*p^3;
* [P,Q]=x^2; and
* additive target normalization gives P(0,0)=Q(0,0)=0.

Unique factorization first gives p=a*h^2, q=b*h^3 with deg(h)=4.
On the generic open set h!=0, the Jacobian calculation below gives
h' | h^2.  If h has r distinct roots, then

    deg(h'/gcd(h,h')) = r-1.

The quotient is coprime to h, so divisibility by h^2 forces r=1.
Thus h=c*(y-y0)^4.  Additive normalization gives h(0)=0 and hence y0=0.
"""

from __future__ import annotations

import sympy as sp

from route_bd_verify import (
    C_P_VERTICES,
    C_Q_VERTICES,
    lattice_points,
)


def jacobian(
    left: sp.Expr,
    right: sp.Expr,
    x: sp.Symbol,
    y: sp.Symbol,
) -> sp.Expr:
    return sp.expand(
        sp.diff(left, x) * sp.diff(right, y)
        - sp.diff(left, y) * sp.diff(right, x)
    )


def verify_rees_support_and_jacobian() -> None:
    """Check polynomiality of the lifted supports and the chain rule."""

    p_support = lattice_points(C_P_VERTICES)
    q_support = lattice_points(C_Q_VERTICES)

    # x^a*y^b has radial z-degree 2*a-b.  The Rees powers are therefore
    # 2-(2*a-b) for P and 3-(2*a-b) for Q.
    assert all(2 - 2 * a + b >= 0 for a, b in p_support)
    assert all(3 - 2 * a + b >= 0 for a, b in q_support)
    assert max(2 * a - b for a, b in p_support) == 2
    assert max(2 * a - b for a, b in q_support) == 3

    # The required vertical vertices make the critical-line restrictions
    # nonconstant of exact degrees 8 and 12.
    p_vertical = sorted(b for a, b in p_support if a == 0)
    q_vertical = sorted(b for a, b in q_support if a == 0)
    assert p_vertical == list(range(9))
    assert q_vertical == list(range(13))

    x, y, s = sp.symbols("x y s", nonzero=True)
    X, Y = sp.symbols("X Y")
    p = sp.Function("p")(X, Y)
    q = sp.Function("q")(X, Y)
    P_s = s**2 * p.subs({X: x / s**2, Y: s * y})
    Q_s = s**3 * q.subs({X: x / s**2, Y: s * y})
    rees_jacobian = sp.simplify(jacobian(P_s, Q_s, x, y))
    source_jacobian = (
        sp.diff(p, X) * sp.diff(q, Y)
        - sp.diff(p, Y) * sp.diff(q, X)
    ).subs({X: x / s**2, Y: s * y})
    assert sp.simplify(rees_jacobian - s**4 * source_jacobian) == 0
    # If [P,Q](X,Y)=X^2, this is s^4*(x/s^2)^2=x^2.
    assert sp.simplify(s**4 * (x / s**2) ** 2 - x**2) == 0


def verify_critical_line_cusp_identity() -> None:
    """Check the exact restriction of the cusp equation to x=0."""

    y, s, L = sp.symbols("y s L")
    p = sp.Function("p")
    q = sp.Function("q")
    P_line = s**2 * p(s * y)
    Q_line = s**3 * q(s * y)
    assert sp.expand(
        Q_line**2 - L * P_line**3
        - s**6 * (q(s * y) ** 2 - L * p(s * y) ** 3)
    ) == 0


def verify_pure_power_local_calculation() -> None:
    """Check the determinant, x-adic leading term, and S-boundary value."""

    P, Q, a, b, h = sp.symbols("P Q a b h", nonzero=True)
    L = b**2 / a**3
    t = a * Q / (b * P)
    n = Q**2 - L * P**3
    target_determinant = sp.simplify(
        sp.diff(t, P) * sp.diff(n, Q)
        - sp.diff(t, Q) * sp.diff(n, P)
    )
    target_on_cusp = sp.simplify(
        target_determinant.subs({P: a * h**2, Q: b * h**3})
    )
    assert target_on_cusp == b * h**2 / a

    # If n=x^r*A and t|_(x=0)=h(y), then the x^(r-1) coefficient
    # of [t,n] is -r*h'*A(0,y).
    x, y = sp.symbols("x y")
    h_y = sp.Function("h")(y)
    A = sp.Function("A")(x, y)
    t_series = h_y + x * sp.Function("u")(x, y)
    for order in range(1, 7):
        n_series = x**order * A
        normalized_leading = sp.simplify(
            jacobian(t_series, n_series, x, y) / x ** (order - 1)
        ).subs(x, 0)
        assert sp.simplify(
            normalized_leading
            + order * sp.diff(h_y, y) * A.subs(x, 0)
        ) == 0

    # For deg(h)=4, the multiplicity-partition argument has residual
    # derivative degree r_distinct-1.  Divisibility forces one root.
    for multiplicities in (
        (4,),
        (3, 1),
        (2, 2),
        (2, 1, 1),
        (1, 1, 1, 1),
    ):
        distinct_roots = len(multiplicities)
        gcd_degree = sum(multiplicity - 1 for multiplicity in multiplicities)
        residual_degree = 3 - gcd_degree
        assert residual_degree == distinct_roots - 1
        assert (residual_degree == 0) == (distinct_roots == 1)

    A0, B0 = sp.symbols("A0 B0", nonzero=True)
    p_boundary = A0 * y**8
    q_boundary = B0 * y**12
    S_boundary = sp.simplify(
        -2 * q_boundary / (3 * sp.diff(p_boundary, y))
    )
    assert S_boundary == -B0 * y**5 / (12 * A0)


def verify_cusp_factorization_pdes() -> None:
    """Check equations obtained from Q^2-L*P^3=x^3*S."""

    x, y, L = sp.symbols("x y L")
    P = sp.Function("P")(x, y)
    Q = sp.Function("Q")(x, y)
    S = sp.Function("S")(x, y)
    n = Q**2 - L * P**3

    assert sp.simplify(jacobian(P, n, x, y) - 2 * Q * jacobian(P, Q, x, y)) == 0
    assert sp.simplify(
        jacobian(Q, n, x, y)
        - 3 * L * P**2 * jacobian(P, Q, x, y)
    ) == 0

    factored = x**3 * S
    assert sp.simplify(
        jacobian(P, factored, x, y)
        - x**2 * (x * jacobian(P, S, x, y) - 3 * sp.diff(P, y) * S)
    ) == 0
    assert sp.simplify(
        jacobian(Q, factored, x, y)
        - x**2 * (x * jacobian(Q, S, x, y) - 3 * sp.diff(Q, y) * S)
    ) == 0


def verify_support_contained_countermodel() -> None:
    """Check the exact support-contained non-etale Rees family."""

    x, y, s, L = sp.symbols("x y s L")
    P = x + y
    Q = x**2 * y + x * y**2 + y**3 / 3
    assert jacobian(P, Q, x, y) == x**2

    p_support = set(lattice_points(C_P_VERTICES))
    q_support = set(lattice_points(C_Q_VERTICES))
    assert {(1, 0), (0, 1)} <= p_support
    assert {(2, 1), (1, 2), (0, 3)} <= q_support

    P_s = x + s**3 * y
    Q_s = x**2 * y + s**3 * x * y**2 + s**6 * y**3 / 3
    assert jacobian(P_s, Q_s, x, y) == x**2
    critical_cusp = sp.expand(
        (Q_s**2 - L * P_s**3).subs(x, 0)
    )
    assert critical_cusp == s**12 * y**6 / 9 - L * s**9 * y**3
    assert critical_cusp != 0


def main() -> None:
    verify_rees_support_and_jacobian()
    verify_critical_line_cusp_identity()
    verify_pure_power_local_calculation()
    verify_cusp_factorization_pdes()
    verify_support_contained_countermodel()
    print("verified polynomial Rees support and total Jacobian x^2")
    print("verified the exact critical-line cusp condition")
    print("verified cusp compatibility forces the pure y^8/y^12 boundary")
    print("verified Q^2-LP^3=x^3*S gives the two first-order PDEs")
    print("verified the support-contained non-etale Rees countermodel")
    print("RESULT: finite-etale Rees descent needs two additional global lemmas")


if __name__ == "__main__":
    main()
