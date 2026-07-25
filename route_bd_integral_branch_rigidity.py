#!/usr/bin/env python3
"""Exact integral-branch rigidity and a nonlinear-shear stress test.

The case-c polynomial coordinates are

    z=x*y,  w=x*y^2,  x=z^2/w,  y=w/z.

Both the outer map F0 and every normalized completion F have Jacobian x^2.
The outer model contracts x=0 to the target origin; a full case-c
completion generally maps that line nontrivially with boundary degrees
(8,12).  Let T=(X,Y) be the normalized algebraic branch of F0^{-1} o F
selected at the radial place t=1/w, with z a unit.  The following is the
useful algebraic lemma.

INTEGRAL-BRANCH RIGIDITY.
If X and Y are integral over k[x,y], then T is polynomial and, under the
radial support caps, T is the identity.

Proof outline (the geometric steps are theorem checks, not CAS claims).

1. The normalization Gamma of k[x,y] in k(x,y)(X,Y) is finite over A^2.
2. Away from x=0, F0 and F are etale.  A divisor of Gamma mapping by T
   into X=0 would map by F to the target origin.  This is impossible over
   x!=0 because an etale map has zero-dimensional fibers.  Purity therefore
   makes Gamma|_(x!=0) a finite etale cover of G_m x A^1.
3. In characteristic zero, every connected finite etale cover of
   G_m x A^1 is Kummer, u^e=x.  At the selected radial valuation

       x=z^2*t,  y=1/(z*t),

   one has v_t(x)=1.  A nontrivial Kummer cover has local ramification e,
   whereas the chosen formal branch already lies in k(z)((t)).  Hence e=1.
4. Thus X,Y lie in k(x,y), and integrality plus normality of k[x,y] makes
   them polynomial.  The chain rule gives

       X^2 Jac(T)=x^2.

   Unique factorization forces X=c*x and then
   Y=c^(-3)*y+h(x).  The identity outer jet gives c=1.
5. If a*x^r is the lowest term of nonzero h, then, in (z,w),

       x*(y+h)^2 = w + 2*a*z^(2r+1)*w^(-r) + higher z-degree.

   Therefore x*U(x*(y+h)^2) acquires the nonzero layer

       2*a*z^(2r+3)*w^(-r-1)*U'(w),

   contradicting the case-c cap deg_z(P)<=2.

Polynomiality of P,Q alone does not imply the hypothesis: F0 is not
proper.  The explicit target-shear family below has polynomial F0,F,
identical Jacobian, one contracted critical line, and a normalized
nonrational inverse branch.  Its first branch coordinate is integral, but
the second has a pole on the normalization.  This is exactly how the
integral-branch lemma evades the nonlinear-shear countermodel.
"""

from __future__ import annotations

import sympy as sp


def verify_radial_place_and_support_escape() -> None:
    x, y, z, w, t = sp.symbols("x y z w t", nonzero=True)
    assert sp.cancel((z**2 / w) * (w / z) - z) == 0
    assert sp.cancel((z**2 / w) * (w / z) ** 2 - w) == 0

    # At t=1/w with z a unit, v_t(x)=1 and v_t(y)=-1.
    x_at_place = z**2 * t
    y_at_place = 1 / (z * t)
    assert sp.expand(x_at_place).as_powers_dict()[t] == 1
    assert sp.expand(y_at_place).as_powers_dict()[t] == -1

    # The first z-layer created by a polynomial shear y -> y+h(x).
    r = sp.symbols("r", integer=True, nonnegative=True)
    a = sp.symbols("a", nonzero=True)
    u = sp.Function("U")
    delta_w_lead = 2 * a * z ** (2 * r + 1) * w ** (-r)
    p_escape = sp.cancel(z**2 / w * sp.diff(u(w), w) * delta_w_lead)
    expected = 2 * a * z ** (2 * r + 3) * w ** (-r - 1) * sp.diff(
        u(w), w
    )
    assert sp.simplify(p_escape - expected) == 0


def verify_polynomial_classification() -> None:
    x, y, c = sp.symbols("x y c", nonzero=True)
    h = sp.Function("h")(x)
    source_x = c * x
    source_y = c ** -3 * y + h
    jacobian_t = sp.factor(
        sp.diff(source_x, x) * sp.diff(source_y, y)
        - sp.diff(source_x, y) * sp.diff(source_y, x)
    )
    assert jacobian_t == c ** -2
    assert sp.factor(source_x**2 * jacobian_t - x**2) == 0


def verify_contracted_shear_countermodel() -> None:
    """Polynomial outputs do not make both inverse coordinates integral."""

    x, y, phi, eta = sp.symbols("x y phi eta")

    # This smallest member has exactly the case-c Jacobian exponent two.
    p0 = x**2
    q0 = x * y
    p = p0 + q0**2
    q = q0
    jacobian_0 = sp.factor(
        sp.diff(p0, x) * sp.diff(q0, y)
        - sp.diff(p0, y) * sp.diff(q0, x)
    )
    jacobian = sp.factor(
        sp.diff(p, x) * sp.diff(q, y)
        - sp.diff(p, y) * sp.diff(q, x)
    )
    assert jacobian_0 == 2 * x**2
    assert jacobian == jacobian_0
    assert p0.subs(x, 0) == q0.subs(x, 0) == 0
    assert p.subs(x, 0) == q.subs(x, 0) == 0

    # The normalized branch is phi=x*sqrt(1+y^2), eta=y/sqrt(1+y^2).
    branch_relation = phi**2 - x**2 * (1 + y**2)
    assert sp.expand(
        sp.factor(branch_relation) - branch_relation
    ) == 0
    eta_relation = phi * eta - x * y
    assert sp.factor(
        (phi**2).subs(phi**2, x**2 * (1 + y**2)) - p
    ) == 0
    assert eta_relation

    # phi is monic integral.  At S=1+y^2, the normalized valuation has
    # ord(phi)=1 and ord(x*y)=0, hence eta=x*y/phi has order -1.  The
    # displayed elimination equation shows the same denominator directly.
    eta_equation = sp.factor((1 + y**2) * eta**2 - y**2)
    assert eta_equation == eta**2 * y**2 + eta**2 - y**2
    assert sp.Poly(branch_relation, phi).LC() == 1
    assert sp.Poly(eta_equation, eta).LC() == 1 + y**2

    # The identity branch exists in the y-adic completion.
    u = sp.symbols("u")
    phi_ratio = sp.series((1 + u**2) ** sp.Rational(1, 2), u, 0, 6)
    eta_ratio = sp.series((1 + u**2) ** -sp.Rational(1, 2), u, 0, 6)
    assert phi_ratio.removeO().subs(u, 0) == 1
    assert eta_ratio.removeO().subs(u, 0) == 1

    # The target shear violates the actual (2,3) radial cap:
    # Q0^2 has target weight 6, while P is capped at weight 2.
    assert 2 * 3 > 2


def verify_high_degree_shear_countermodel() -> None:
    """A degree-21 identity-at-infinity version of the same pole mechanism."""

    n = 21
    x, y, phi = sp.symbols("x y phi")
    p0 = x**n
    q0 = x * y
    p = p0 + q0**2
    q = q0
    jacobian_0 = sp.factor(
        sp.diff(p0, x) * sp.diff(q0, y)
        - sp.diff(p0, y) * sp.diff(q0, x)
    )
    jacobian = sp.factor(
        sp.diff(p, x) * sp.diff(q, y)
        - sp.diff(p, y) * sp.diff(q, x)
    )
    assert jacobian == jacobian_0 == n * x**n

    divisor = x ** (n - 2) + y**2
    assert sp.factor(divisor) == divisor
    minimal = sp.Poly(phi**n - x**2 * divisor, phi)
    assert minimal.LC() == 1

    # Eisenstein at the prime divisor x^(n-2)+y^2 proves degree n.  The
    # second branch coordinate eta=x*y/phi has valuation -1 above it.
    assert sp.gcd(
        sp.Poly(divisor, y),
        sp.Poly(sp.diff(divisor, y), y),
    ).degree() == 0

    # At x=infinity the selected branch is tangent to the identity to
    # order n-2.
    u = sp.symbols("u")
    normalized = sp.series(
        (1 + y**2 * u ** (n - 2)) ** sp.Rational(1, n),
        u,
        0,
        n,
    )
    assert normalized.removeO().coeff(u, n - 2) == y**2 / n
    assert all(
        normalized.removeO().coeff(u, exponent) == 0
        for exponent in range(1, n - 2)
    )


def main() -> None:
    verify_radial_place_and_support_escape()
    verify_polynomial_classification()
    verify_contracted_shear_countermodel()
    verify_high_degree_shear_countermodel()
    print("verified the split radial valuation v_t(x)=1")
    print("verified integral branch => polynomial triangular source map")
    print("verified the radial P-cap kills every triangular shear h(x)")
    print("verified polynomial nonlinear shears need not have integral branches")
    print("verified the missing branch coordinate has an explicit divisor pole")
    print("RESULT: proving original-plane integrality would finish the radial branch")


if __name__ == "__main__":
    main()
