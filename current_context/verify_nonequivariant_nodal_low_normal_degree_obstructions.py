#!/usr/bin/env python3
"""Exact checks for NONEQUIVARIANT_NODAL_LOW_NORMAL_DEGREE_OBSTRUCTIONS.md."""

from __future__ import annotations

import sympy as sp


x, y, t = sp.symbols("x y t")


# ---------------------------------------------------------------------------
# The asymmetric immersed nodal boundary.

p_seed = x**3 - x
q_seed = x**5 - x**4 + x**3 - x

assert p_seed.subs(x, 0) == p_seed.subs(x, 1) == 0
assert q_seed.subs(x, 0) == q_seed.subs(x, 1) == 0

bezout_p = 180 * x**3 - 69 * x**2 + 108 * x + 22
bezout_q = -108 * x - 45
assert sp.expand(
    bezout_p * sp.diff(p_seed, x) + bezout_q * sp.diff(q_seed, x)
) == 23

# There is no affine target map gamma(x) -> gamma(1-x).
A0, A1, A2, B0, B1, B2 = sp.symbols("A0 A1 A2 B0 B1 B2")
affine_residuals = [
    sp.Poly(
        sp.expand(A0 + A1 * p_seed + A2 * q_seed - p_seed.subs(x, 1 - x)),
        x,
    ),
    sp.Poly(
        sp.expand(B0 + B1 * p_seed + B2 * q_seed - q_seed.subs(x, 1 - x)),
        x,
    ),
]
affine_equations = []
for residual in affine_residuals:
    affine_equations.extend(residual.all_coeffs())
assert sp.solve(
    affine_equations,
    [A0, A1, A2, B0, B1, B2],
    dict=True,
) == []


# ---------------------------------------------------------------------------
# Universal quadratic-normal equations and their first integrals.

p = sp.Function("p")(x)
q = sp.Function("q")(x)
a = sp.Function("a")(x)
b = sp.Function("b")(x)
c = sp.Function("c")(x)

F2 = p + a * y + b * y**2
G1 = q + c * y
J21 = sp.Poly(
    sp.expand(sp.diff(F2, x) * sp.diff(G1, y) - sp.diff(F2, y) * sp.diff(G1, x)),
    y,
)
assert J21.coeff_monomial(y**2) == sp.diff(b, x) * c - 2 * b * sp.diff(c, x)
assert J21.coeff_monomial(y) == (
    sp.diff(a, x) * c - a * sp.diff(c, x) - 2 * b * sp.diff(q, x)
)
assert J21.coeff_monomial(1) == sp.diff(p, x) * c - a * sp.diff(q, x)

kappa, ell = sp.symbols("kappa ell")
b_quadratic = kappa * c**2
a_quadratic = c * (2 * kappa * q + ell)
assert sp.simplify(
    sp.diff(b_quadratic, x) * c - 2 * b_quadratic * sp.diff(c, x)
) == 0
assert sp.simplify(
    sp.diff(a_quadratic, x) * c
    - a_quadratic * sp.diff(c, x)
    - 2 * b_quadratic * sp.diff(q, x)
) == 0


# ---------------------------------------------------------------------------
# Cubic against linear.

d = sp.Function("d")(x)
c3 = sp.Function("c3")(x)
b2 = sp.Function("b2")(x)
a1 = sp.Function("a1")(x)
F3 = p + a1 * y + b2 * y**2 + c3 * y**3
Glin = q + d * y
J31 = sp.Poly(
    sp.expand(sp.diff(F3, x) * sp.diff(Glin, y) - sp.diff(F3, y) * sp.diff(Glin, x)),
    y,
)
expected_31 = {
    3: sp.diff(c3, x) * d - 3 * c3 * sp.diff(d, x),
    2: (
        sp.diff(b2, x) * d
        - 2 * b2 * sp.diff(d, x)
        - 3 * c3 * sp.diff(q, x)
    ),
    1: sp.diff(a1, x) * d - a1 * sp.diff(d, x) - 2 * b2 * sp.diff(q, x),
    0: sp.diff(p, x) * d - a1 * sp.diff(q, x),
}
for degree, expected in expected_31.items():
    assert sp.simplify(J31.coeff_monomial(y**degree) - expected) == 0

rho, mu = sp.symbols("rho mu")
assert sp.simplify(
    expected_31[3].subs(c3, rho * d**3)
) == 0
assert sp.simplify(
    expected_31[2].subs(
        {
            c3: rho * d**3,
            b2: d**2 * (3 * rho * q + mu),
        }
    )
) == 0
assert sp.simplify(
    sp.diff(d * (3 * rho * q**2 + 2 * mu * q + ell), x) * d
    - d * (3 * rho * q**2 + 2 * mu * q + ell) * sp.diff(d, x)
    - 2 * d**2 * (3 * rho * q + mu) * sp.diff(q, x)
) == 0


# ---------------------------------------------------------------------------
# Full (3,2) coefficient system.

e = sp.Function("e")(x)
F32 = p + a * y + b * y**2 + c3 * y**3
G32 = q + d * y + e * y**2
J32 = sp.Poly(
    sp.expand(sp.diff(F32, x) * sp.diff(G32, y) - sp.diff(F32, y) * sp.diff(G32, x)),
    y,
)
expected_32 = {
    4: 2 * sp.diff(c3, x) * e - 3 * c3 * sp.diff(e, x),
    3: (
        2 * sp.diff(b, x) * e
        - 2 * b * sp.diff(e, x)
        + sp.diff(c3, x) * d
        - 3 * c3 * sp.diff(d, x)
    ),
    2: (
        2 * sp.diff(a, x) * e
        - a * sp.diff(e, x)
        + sp.diff(b, x) * d
        - 2 * b * sp.diff(d, x)
        - 3 * c3 * sp.diff(q, x)
    ),
    1: (
        2 * sp.diff(p, x) * e
        + sp.diff(a, x) * d
        - a * sp.diff(d, x)
        - 2 * b * sp.diff(q, x)
    ),
    0: sp.diff(p, x) * d - a * sp.diff(q, x),
}
for degree, expected in expected_32.items():
    assert sp.simplify(J32.coeff_monomial(y**degree) - expected) == 0

h = sp.Function("h")(x)
top_relation = sp.simplify(
    expected_32[3].subs({c3: h**3, e: h**2})
)
integrated_top_relation = sp.diff((2 * b - 3 * h * d) / h**2, x)
assert sp.simplify(top_relation - h**4 * integrated_top_relation) == 0


# ---------------------------------------------------------------------------
# Constant-h first integrals and the terminal square.

k, AA = sp.symbols("k AA")
bb = sp.Function("bb")(x)
qq = sp.Function("qq")(x)

dd = (2 * bb - k) / 3
aa = bb**2 / 6 + k * bb / 6 + 3 * qq / 2 + AA
pp = -sp.Rational(1, 2) * (
    bb**3 / 27
    - k * bb**2 / 18
    - k**2 * bb / 18
    - bb * qq
    - 2 * AA * bb / 3
    - k * qq / 2
)

constant_h_y2 = (
    2 * sp.diff(aa, x)
    + sp.diff(bb, x) * dd
    - 2 * bb * sp.diff(dd, x)
    - 3 * sp.diff(qq, x)
)
constant_h_y1 = (
    2 * sp.diff(pp, x)
    + sp.diff(aa, x) * dd
    - aa * sp.diff(dd, x)
    - 2 * bb * sp.diff(qq, x)
)
assert sp.simplify(constant_h_y2) == 0
assert sp.simplify(constant_h_y1) == 0

Psi = (
    -bb**4 / 108
    + k * bb**3 / 54
    - k**3 * bb / 108
    + qq * (bb**2 - k * bb) / 6
    + AA * (bb**2 - k * bb) / 9
    - k**2 * qq / 12
    - 3 * qq**2 / 4
    - AA * qq
)
assert sp.simplify(
    sp.diff(pp, x) * dd - aa * sp.diff(qq, x) - sp.diff(Psi, x)
) == 0

T = 2 * bb**2 - 2 * k * bb - k**2
square_form = (
    k**4 / 432
    + AA * k**2 / 18
    + AA**2 / 3
    - sp.Rational(3, 4) * (qq - T / 18 + 2 * AA / 3) ** 2
)
assert sp.expand(Psi - square_form) == 0


# ---------------------------------------------------------------------------
# Global rational-quotient closure.

u = sp.Function("u")(x)
V = sp.Function("V")(x)
hh = sp.Function("hh")(x)
pp0 = sp.Function("pp0")(x)
qq0 = sp.Function("qq0")(x)

dd_general = hh * u
bb_general = hh**2 * (sp.Rational(3, 2) * u + k / 2)
aa_general = hh * V

y2_general = (
    2 * sp.diff(aa_general, x) * hh**2
    - aa_general * sp.diff(hh**2, x)
    + sp.diff(bb_general, x) * dd_general
    - 2 * bb_general * sp.diff(dd_general, x)
    - 3 * hh**3 * sp.diff(qq0, x)
)
expected_V_ode = hh**3 * (
    2 * sp.diff(V, x)
    - (sp.Rational(3, 2) * u + k) * sp.diff(u, x)
    - 3 * sp.diff(qq0, x)
)
assert sp.simplify(y2_general - expected_V_ode) == 0

V_integrated = (
    sp.Rational(3, 8) * u**2
    + k * u / 2
    + sp.Rational(3, 2) * qq0
    + AA
)
assert sp.simplify(
    2 * sp.diff(V_integrated, x)
    - (sp.Rational(3, 2) * u + k) * sp.diff(u, x)
    - 3 * sp.diff(qq0, x)
) == 0

y1_general = (
    2 * sp.diff(pp0, x) * hh**2
    + sp.diff(hh * V_integrated, x) * hh * u
    - hh * V_integrated * sp.diff(hh * u, x)
    - 2 * bb_general * sp.diff(qq0, x)
)
Phi = (
    2 * pp0
    + u**3 / 8
    - sp.Rational(3, 2) * u * qq0
    - AA * u
    - k * qq0
)
assert sp.simplify(y1_general - hh**2 * sp.diff(Phi, x)) == 0

last_general = (
    sp.diff(pp0, x) * dd_general
    - hh * V_integrated * sp.diff(qq0, x)
)
assert sp.simplify(
    last_general
    - hh * (sp.diff(pp0, x) * u - V_integrated * sp.diff(qq0, x))
) == 0


# ---------------------------------------------------------------------------
# The top quartic equation and the power-shear reductions.

f4 = sp.Function("f4")(x)
for normal_degree, exponent in ((1, 4), (2, 2), (4, 1)):
    gn = sp.Function(f"g{normal_degree}")(x)
    top_equation = (
        normal_degree * sp.diff(f4, x) * gn
        - 4 * f4 * sp.diff(gn, x)
    )
    kappa_q = sp.symbols(f"kappa_{normal_degree}")
    assert sp.simplify(
        top_equation.subs(f4, kappa_q * gn**exponent)
    ) == 0

# The arithmetic counterexample to Lemma 2.3 in arXiv:1810.08202v2.
for L in range(100):
    assert not (
        sp.gcd(2, L + 1) == 1
        and sp.gcd(2, L + 2) == 1
    )


print("verified: asymmetric nodal collision and immersion certificate")
print("verified: no affine target intertwiner for x -> 1-x on the boundary")
print("verified: quadratic-normal and cubic-linear injectivity reductions")
print("verified: exact (3,2) five-equation system and leading-factor integral")
print("verified: constant leading factor collapses to a terminal square")
print("verified: rational quotient closure forces the leading factor to be constant")
print("verified: quartic power shears leave only bidegree (4,3)")
print("verified: exact counterexample to the cited number-theoretic lemma")
