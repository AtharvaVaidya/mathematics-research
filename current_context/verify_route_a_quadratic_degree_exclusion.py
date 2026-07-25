#!/usr/bin/env python3
"""Exact local algebra checks for ROUTE_A_QUADRATIC_DEGREE_EXCLUSION.md.

This script checks the elementary hypersurface and Poisson calculations.
It does not purport to verify Zariski's Main Theorem, purity of the branch
locus, or the valuation-theoretic part of the proof.
"""

import sympy as sp


u, v, w = sp.symbols("u v w")
h = w**2 - u - u**2 * v

# The equation is primitive and linear in v, hence irreducible over
# C[u,v,w] by Gauss's lemma.
h_as_v_polynomial = sp.Poly(h, v)
assert h_as_v_polynomial.degree() == 1
assert sp.gcd(u**2, w**2 - u) == 1

# The hypersurface is smooth: h and its three partial derivatives generate
# the unit ideal.  The same calculation says that the Jacobian Poisson
# bivector has no zero on the surface.
h_u = sp.diff(h, u)
h_v = sp.diff(h, v)
h_w = sp.diff(h, w)
smooth_basis = sp.groebner([h, h_u, h_v, h_w], v, w, u, order="lex")
assert list(smooth_basis) == [1]

# Generator brackets in the negative residue/Jacobian convention used by
# Route A.
brackets = {
    (u, v): -h_w,
    (v, w): -h_u,
    (u, w): h_v,
}
assert brackets[(u, v)] == -2 * w
assert brackets[(v, w)] == 1 + 2 * u * v
assert brackets[(u, w)] == -u**2


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """Negative Jacobian determinant -det(dh,dleft,dright)."""

    return sp.expand(
        -sp.det(
            sp.Matrix(
                [
                    [sp.diff(h, variable) for variable in (u, v, w)],
                    [sp.diff(left, variable) for variable in (u, v, w)],
                    [sp.diff(right, variable) for variable in (u, v, w)],
                ]
            )
        )
    )


assert bracket(u, v) == -2 * w
assert bracket(v, w) == 1 + 2 * u * v
assert bracket(u, w) == -u**2
assert bracket(h, u) == bracket(h, v) == bracket(h, w) == 0

# The displayed localization isomorphism B_u = C[u,u^{-1},w] eliminates v.
v_in_localization = (w**2 - u) / u**2
assert sp.cancel(h.subs(v, v_in_localization)) == 0

# The ideal (u,w) is proper and its quotient is C[v], so u is not a unit.
proper_ideal_basis = sp.groebner([h, u, w], w, u, v, order="lex")
assert list(proper_ideal_basis) != [1]
uw_basis = sp.groebner([u, w], u, w, v)
_, h_mod_uw = uw_basis.reduce(h)
assert h_mod_uw == 0

print("verified: h is primitive linear in v and irreducible")
print("verified: S is smooth and the Jacobian bracket is nondegenerate")
print("verified: B_u is obtained by v=(w^2-u)/u^2")
print("verified: (u,w) is proper, so u is not a unit")
print("all elementary Route A Galois-degree checks passed")
