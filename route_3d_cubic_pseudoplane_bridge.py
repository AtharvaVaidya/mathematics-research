#!/usr/bin/env python3
"""Exact audit of the 3D-fiber/cubic-pseudo-plane bridge."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    x, y, z, c, t, a, b = sp.symbols("x y z c t a b")
    P3 = (1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y)
    Q3 = (
        y
        + 3 * x * (1 + x * y) ** 2 * z
        + 3 * x * y**2 * (4 + 3 * x * y)
    )
    R3 = 2 * x - 3 * x**2 * y - x**3 * z
    jac3 = sp.factor(
        sp.det(
            sp.Matrix(
                [[sp.diff(f, q) for q in (x, y, z)] for f in (P3, Q3, R3)]
            )
        )
    )
    assert jac3 == -2

    fiber_z = (2 * x - 3 * x**2 * y - c) / x**3
    Pc = sp.factor(P3.subs(z, fiber_z).subs(y, t / x))
    Qc = sp.factor(Q3.subs(z, fiber_z).subs(y, t / x))
    assert sp.simplify(
        Pc - (t + 1) * (x * (t + 2) - c * (t + 1) ** 2) / x**3
    ) == 0
    assert sp.simplify(
        Qc - (x * (4 * t + 6) - 3 * c * (t + 1) ** 2) / x**2
    ) == 0
    jac_fiber = sp.factor(
        sp.det(sp.Matrix([[sp.diff(f, q) for q in (x, t)] for f in (Pc, Qc)]))
    )
    assert jac_fiber == 2 / x**4

    Pa = sp.factor(Pc.subs(x, 1 / a))
    Qa = sp.factor(Qc.subs(x, 1 / a))
    assert sp.expand(
        Pa - (a**2 * (t + 1) * (t + 2) - c * a**3 * (t + 1) ** 3)
    ) == 0
    assert sp.expand(
        Qa - (2 * a * (2 * t + 3) - 3 * c * a**2 * (t + 1) ** 2)
    ) == 0
    jac_completion = sp.factor(
        sp.det(sp.Matrix([[sp.diff(f, q) for q in (a, t)] for f in (Pa, Qa)]))
    )
    assert jac_completion == -2 * a**2

    s = sp.symbols("s")
    t_from_s = (s / a - 3) / 2
    assert sp.simplify(
        Pa.subs(c, 0).subs(t, t_from_s) - (s**2 - a**2) / 4
    ) == 0
    assert sp.simplify(Qa.subs(c, 0).subs(t, t_from_s) - 2 * s) == 0

    u = a**3
    w = a * (1 + 3 * a**3 * b)
    v = 9 * b + 27 * a**3 * b**2 + 27 * a**6 * b**3
    assert sp.expand(w**3 - u - u**2 * v) == 0
    jac_uw = sp.factor(
        sp.det(sp.Matrix([[sp.diff(f, q) for q in (a, b)] for f in (u, w)]))
    )
    assert jac_uw == 9 * u**2

    U, W = sp.symbols("U W")
    f = sp.Function("f")(U, W)
    g = sp.Function("g")(U, W)
    f_pull = f.subs({U: u, W: w})
    g_pull = g.subs({U: u, W: w})
    pull_jac = sp.expand(
        sp.det(
            sp.Matrix(
                [[sp.diff(expr, q) for q in (a, b)] for expr in (f_pull, g_pull)]
            )
        )
    )
    surface_bracket = -U**2 * (
        sp.diff(f, U) * sp.diff(g, W) - sp.diff(f, W) * sp.diff(g, U)
    )
    assert sp.simplify(pull_jac + 9 * surface_bracket.subs({U: u, W: w})) == 0

    # The restricted c=0 pair is canonical on u=x^3, w=t, but transforms
    # nontrivially under the cubic deck group.
    Pu = (t + 1) * (t + 2) / x**2
    Qu = 2 * (2 * t + 3) / x
    jac_u_t = sp.factor(jac_fiber.subs(c, 0) / (3 * x**2))
    bracket_u_w = sp.factor(-x**6 * jac_u_t)
    assert bracket_u_w == -sp.Rational(2, 3)

    # Dubouloz--Palka's cyclic degree-three etale endomorphism of
    # S(3,3,1)=B3.  Reduce first by the surface equation and then by the
    # primitive-cube-root equation epsilon^2+epsilon+1=0.
    epsilon = sp.symbols("epsilon")
    tau = sp.symbols("tau")
    R1_tau = 1 + (epsilon - 1) * tau
    quotient, remainder = sp.div(
        sp.expand(R1_tau**3 - 1),
        tau * (tau - 1),
        tau,
    )

    def reduce_epsilon(expression: sp.Expr) -> sp.Expr:
        return sp.Poly(
            sp.expand(expression), epsilon
        ).rem(
            sp.Poly(epsilon**2 + epsilon + 1, epsilon)
        ).as_expr()

    R0_tau = reduce_epsilon(quotient)
    assert reduce_epsilon(remainder) == 0
    t_surface = -U * sp.symbols("V")

    # Use fresh surface generators to avoid collision with the formal U,W
    # used in the generic pullback calculation above.
    uu, vv, ww = sp.symbols("uu vv ww")
    t_surface = -uu * vv
    eta_u = ww**3
    eta_v = vv * reduce_epsilon(R0_tau.subs(tau, t_surface))
    eta_w = ww * reduce_epsilon(R1_tau.subs(tau, t_surface))

    def reduce_surface(expression: sp.Expr) -> sp.Expr:
        reduced_w = sp.rem(
            sp.Poly(sp.expand(expression), ww),
            sp.Poly(ww**3 - uu - uu**2 * vv, ww),
        ).as_expr()
        return sp.factor(reduce_epsilon(reduced_w))

    def surface_bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        raw = (
            -3 * ww**2
            * (
                sp.diff(left, uu) * sp.diff(right, vv)
                - sp.diff(left, vv) * sp.diff(right, uu)
            )
            - uu**2
            * (
                sp.diff(left, uu) * sp.diff(right, ww)
                - sp.diff(left, ww) * sp.diff(right, uu)
            )
            + (1 + 2 * uu * vv)
            * (
                sp.diff(left, vv) * sp.diff(right, ww)
                - sp.diff(left, ww) * sp.diff(right, vv)
            )
        )
        return reduce_surface(raw)

    assert reduce_surface(
        eta_w**3 - eta_u - eta_u**2 * eta_v
    ) == 0
    multiplier = 3 * (1 - epsilon)
    assert reduce_surface(
        surface_bracket(eta_u, eta_w) + multiplier * eta_u**2
    ) == 0
    assert reduce_surface(
        surface_bracket(eta_u, eta_v) + 3 * multiplier * eta_w**2
    ) == 0
    assert reduce_surface(
        surface_bracket(eta_v, eta_w)
        - multiplier * (1 + 2 * eta_u * eta_v)
    ) == 0

    print("3D determinant:", jac3)
    print("fiber Jacobian:", jac_fiber)
    print("polynomial completion Jacobian:", jac_completion)
    print("cubic pseudo-plane pullback multiplier:", -9)
    print("Kummer-cover Darboux bracket:", bracket_u_w)
    print("Dubouloz-Palka degree-three multiplier:", multiplier)
    print("RESULT: EXACT CUBIC PSEUDO-PLANE BRIDGE PASSES")


if __name__ == "__main__":
    main()
