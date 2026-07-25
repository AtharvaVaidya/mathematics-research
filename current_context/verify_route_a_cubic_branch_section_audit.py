#!/usr/bin/env python3
"""Exact checks for ROUTE_A_CUBIC_BRANCH_SECTION_AUDIT.md.

The script verifies the hypersurface/chart identities, the internal
class-zero prime, and the explicit S3 cubic branch countermodel.  It does
not replace normalization, purity, cubic inertia theory, or the class
group and mandatory-collision theorems cited in the memo.
"""

from __future__ import annotations

import sympy as sp


def reduce_on_surface(expression: sp.Expr, u: sp.Symbol, v: sp.Symbol,
                      w: sp.Symbol) -> sp.Expr:
    """Return the reduced remainder modulo w^2-u-u^2*v."""

    h = w**2 - u - u**2 * v
    return sp.rem(sp.Poly(sp.expand(expression), w), sp.Poly(h, w)).as_expr()


def canonical_double_chart() -> None:
    a, b = sp.symbols("a b")
    u, v, w = sp.symbols("u v w")

    chart = {
        u: a**2,
        v: 4 * b * (1 + a**2 * b),
        w: a * (1 + 2 * a**2 * b),
    }
    h = w**2 - u - u**2 * v
    assert sp.expand(h.subs(chart)) == 0

    def jac(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(left, a) * sp.diff(right, b)
            - sp.diff(left, b) * sp.diff(right, a)
        )

    pulled_u, pulled_v, pulled_w = chart[u], chart[v], chart[w]
    assert sp.expand(jac(pulled_u, pulled_v) - (-4) * (-2 * pulled_w)) == 0
    assert sp.expand(jac(pulled_u, pulled_w) - (-4) * (-pulled_u**2)) == 0
    assert sp.expand(
        jac(pulled_v, pulled_w) + 4 * (1 + 2 * pulled_u * pulled_v)
    ) == 0

    # u=a^2 exhibits even valuation over D; u-1 splits into two reduced
    # components in the chart, as expected for an unramified double cover.
    assert chart[u] == a**2
    assert sp.factor((u - 1).subs(chart)) == (a - 1) * (a + 1)


def internal_class_zero_prime() -> None:
    u, v, w = sp.symbols("u v w")
    h = w**2 - u - u**2 * v

    # On u=1 the equation solves v=w^2-1, so B/(u-1) is C[w].
    quotient_equation = sp.expand(h.subs(u, 1))
    assert quotient_equation == w**2 - v - 1
    assert sp.solve(quotient_equation, v) == [w**2 - 1]

    # The two standard nonprincipal curves occur as the two reduced
    # components of the principal divisor w=0.
    h_at_w_zero = sp.factor(h.subs(w, 0))
    assert h_at_w_zero == -u * (u * v + 1)

    # The scheme-theoretic multiplicity of D in div(u) is two: after
    # eliminating u^2*v with the surface equation, w^2=u(1+u*v).
    assert reduce_on_surface(w**2 - u * (1 + u * v), u, v, w) == 0


def cubic_branch_countermodel() -> None:
    s, t, x, y, T = sp.symbols("s t x y T")
    target_x = s
    target_y = t**3 - 3 * s * t

    jacobian = sp.expand(
        sp.diff(target_x, s) * sp.diff(target_y, t)
        - sp.diff(target_x, t) * sp.diff(target_y, s)
    )
    assert jacobian == -3 * (s - t**2)

    branch = 4 * x**3 - y**2
    pulled_branch = sp.factor(branch.subs({x: target_x, y: target_y}))
    assert pulled_branch == (s - t**2) ** 2 * (4 * s - t**2)

    # The defining cubic and its discriminant (up to the nonzero factor 27).
    cubic = T**3 - 3 * x * T - y
    discriminant = sp.factor(sp.discriminant(cubic, T))
    assert sp.expand(discriminant - 27 * branch) == 0

    # The branch polynomial is reduced and irreducible.  It has odd
    # valuation in the discriminant, so the cubic discriminant is not a
    # square in C(x,y).
    assert sp.Poly(branch, y).degree() == 2
    assert sp.factor(branch) == branch
    assert sp.gcd(sp.gcd(branch, sp.diff(branch, x)), sp.diff(branch, y)) == 1

    # On the residual sheet C=(4s-t^2), the Jacobian is 9t^2/4 and hence
    # nonzero at its generic point.  On E=(s-t^2), it vanishes simply.
    jac_on_c = sp.expand(jacobian.subs(s, t**2 / 4))
    assert jac_on_c == sp.Rational(9, 4) * t**2
    assert sp.Poly(jacobian, s).degree() == 1
    assert sp.diff(jacobian, s) == -3

    # Both sheets map to the same normalized branch curve.  Parameter r
    # on E and parameter t=-2r on C have identical target images.
    r = sp.symbols("r")
    image_e = (r**2, -2 * r**3)
    image_c = (
        (t**2 / 4).subs(t, -2 * r),
        (t**3 / 4).subs(t, -2 * r),
    )
    assert tuple(map(sp.expand, image_c)) == image_e

    # Pullback of the base area form has exactly the ramification factor.
    area_multiplier = jacobian
    assert sp.cancel(area_multiplier / (s - t**2)) == -3


def abstract_divisor_arithmetic() -> None:
    # In Cl(B)=Z/2, D and H have the nonzero class while a principal
    # retained sheet has class zero.  This records the arithmetic used in
    # the theorem; the class-group computation itself is theorem-level.
    class_D = 1
    class_H = 1
    class_C = 0
    modulus = 2
    assert (2 * class_D) % modulus == 0
    assert (class_D + class_H) % modulus == 0
    assert class_C != class_D
    assert class_C != class_H

    # Kummer parity distinguishes the two quadratic extensions:
    # div(u) has coefficient 2 at D (unramified), whereas a simple cubic
    # discriminant has coefficient 1 at the retained C (ramified).
    valuation_u_at_D = 2
    valuation_discriminant_at_C = 1
    assert valuation_u_at_D % 2 == 0
    assert valuation_discriminant_at_C % 2 == 1


def main() -> None:
    canonical_double_chart()
    internal_class_zero_prime()
    cubic_branch_countermodel()
    abstract_divisor_arithmetic()
    print("verified: canonical degree-two chart lies on S and is etale")
    print("verified: V(u-1) is an internal principal prime")
    print("verified: cubic countermodel has exact 2+1 branch factorization")
    print("verified: deleting E removes exactly the Jacobian zero")
    print("verified: class and Kummer parity consequences are consistent")
    print("RESULT: cubic branches force a class-zero retained sheet,")
    print("        but the audited invariants give no degree-three contradiction")


if __name__ == "__main__":
    main()
