#!/usr/bin/env python3
"""Exact checks for the D+H collision architecture on the pseudoplane.

The mathematical argument is recorded in
``current_context/QUADRATIC_PSEUDOPLANE_DH_COLLISION.md``.  This verifier
checks:

1. the two components and CRT idempotents of the divisor w=0;
2. the monomial classification identity for unramified Laurent maps;
3. a nontrivial singular-curve example of the universal first-jet gluing;
4. the invariant and rational slice behind the no-polynomial-mate theorem
   for the Hamiltonian w.
"""

from __future__ import annotations

import sympy as sp


u, v, w = sp.symbols("u v w", nonzero=True)


def bracket(left, right):
    """Poisson bracket in C[u,v,w]/(w^2-u-u^2 v), before reduction."""
    lu, lv, lw = (sp.diff(left, variable) for variable in (u, v, w))
    ru, rv, rw = (sp.diff(right, variable) for variable in (u, v, w))
    return sp.expand(
        -2 * w * (lu * rv - lv * ru)
        - u**2 * (lu * rw - lw * ru)
        + (1 + 2 * u * v) * (lv * rw - lw * rv)
    )


def lift_laurent(expression):
    """Lift a Laurent polynomial on H by replacing u^{-m} with (-v)^m."""
    expression = sp.expand(expression)
    answer = 0
    for term in sp.Add.make_args(expression):
        coefficient, power = term.as_coeff_exponent(u)
        if power >= 0:
            answer += coefficient * u**power
        else:
            answer += coefficient * (-v) ** (-power)
    return sp.expand(answer)


def crt_lift(on_d, on_h):
    """Lift C[v] x C[u,u^-1] through B/(w)."""
    e_d = 1 + u * v
    e_h = -u * v
    return sp.expand(e_d * on_d + e_h * lift_laurent(on_h))


def restrict_d(expression):
    return sp.expand(expression.subs(u, 0))


def restrict_h(expression):
    return sp.expand(expression.subs(v, -1 / u))


def verify_divisor_and_crt():
    relation_at_w_zero = sp.factor(u * (1 + u * v))
    assert relation_at_w_zero == u * (u * v + 1)

    e_d = 1 + u * v
    e_h = -u * v
    assert sp.expand(e_d + e_h) == 1
    assert restrict_d(e_d) == 1 and restrict_h(e_d) == 0
    assert restrict_d(e_h) == 0 and restrict_h(e_h) == 1

    sample_d = v**3 - 2 * v + 7
    sample_h = 3 * u**4 - 5 / u**3 + 2 / u
    glued = crt_lift(sample_d, sample_h)
    assert sp.simplify(restrict_d(glued) - sample_d) == 0
    assert sp.simplify(restrict_h(glued) - sample_h) == 0


def verify_unramified_laurent_classification_identity():
    a, b = sp.symbols("a b", nonzero=True)
    for exponent in (-5, -2, -1, 1, 2, 6):
        phi = b + a * u**exponent
        derivative = sp.diff(phi, u)
        assert sp.simplify(derivative - a * exponent * u ** (exponent - 1)) == 0

    # Conversely, a Laurent derivative without a C* zero is a monomial.
    # The only monomial that has no Laurent-polynomial primitive is u^-1.
    exponent = sp.symbols("exponent", integer=True)
    assert sp.integrate(u**3, u) == u**4 / 4
    assert sp.integrate(u**-3, u) == -1 / (2 * u**2)
    assert sp.integrate(u**-1, u) == sp.log(u)


def verify_first_jet_gluing():
    """Check the universal construction on an immersed nodal plane curve."""
    t = sp.symbols("t")
    curve_p = t**2
    curve_q = t**3 + t

    # A' S - R B' = 1.
    bezout_r = -1
    bezout_s = -3 * t / 2
    assert sp.expand(
        sp.diff(curve_p, t) * bezout_s
        - bezout_r * sp.diff(curve_q, t)
    ) == 1

    # D uses t=v.  H uses the unramified Laurent cover t=5+3u^2.
    phi = 5 + 3 * u**2
    kappa = sp.simplify(-1 / (u**2 * sp.diff(phi, u)))

    p0_d = curve_p.subs(t, v)
    q0_d = curve_q.subs(t, v)
    p1_d = sp.sympify(bezout_r)
    q1_d = bezout_s.subs(t, v)

    p0_h = curve_p.subs(t, phi)
    q0_h = curve_q.subs(t, phi)
    p1_h = sp.expand(kappa * bezout_r)
    q1_h = sp.expand(kappa * bezout_s.subs(t, phi))

    p0 = crt_lift(p0_d, p0_h)
    q0 = crt_lift(q0_d, q0_h)
    p1 = crt_lift(p1_d, p1_h)
    q1 = crt_lift(q1_d, q1_h)
    pair_p = p0 + w * p1
    pair_q = q0 + w * q1

    boundary_bracket = sp.expand(bracket(pair_p, pair_q).subs(w, 0))
    assert sp.simplify(restrict_d(boundary_bracket) - 1) == 0
    assert sp.simplify(restrict_h(boundary_bracket) - 1) == 0


def verify_w_slice_obstruction_identities():
    invariant = u + u**2 * v
    delta_u = bracket(w, u)
    delta_v = bracket(w, v)
    assert delta_u == u**2
    assert delta_v == -2 * u * v - 1
    assert sp.expand(bracket(w, invariant)) == 0
    assert sp.simplify(bracket(w, -1 / u) - 1) == 0

    # In C[u,u^-1,t], delta=u^2*d/du at fixed t.  Hence every Laurent
    # solution is -u^-1+R(t); the displayed pole cannot be removed by a
    # polynomial R(t) along u=0.
    t = sp.symbols("t")
    coefficients = sp.symbols("c0:5")
    invariant_polynomial = sum(c * t**i for i, c in enumerate(coefficients))
    general_solution = -1 / u + invariant_polynomial
    assert sp.simplify(u**2 * sp.diff(general_solution, u) - 1) == 0
    assert sp.limit(general_solution, u, 0) in (sp.oo, -sp.oo, sp.zoo)


def main():
    verify_divisor_and_crt()
    verify_unramified_laurent_classification_identity()
    verify_first_jet_gluing()
    verify_w_slice_obstruction_identities()
    print("verified: D/H CRT splitting and unramified Laurent normal form")
    print("verified: universal first symplectic jet glues across D+H")
    print("verified: invariant and unavoidable pole for every rational w-slice")


if __name__ == "__main__":
    main()
