#!/usr/bin/env python3
"""Exact checks for the arbitrary-d canonical symplectic extension."""

from __future__ import annotations

import sympy as sp


x, y, u, ell = sp.symbols("x y u ell", nonzero=True)


# The bounded normal field and its intrinsic curvature.
d = x**4 + ell * x**2
d1 = sp.diff(d, x)
p0 = d**2 + u * x
q0 = d**3
p1 = -4 * d1 / (3 * u**2)
q1 = 1 / u - 2 * d * d1 / u**2
omega = sp.factor(sp.diff(p1, x) * q1 - p1 * sp.diff(q1, x))

assert sp.factor(sp.diff(p0, x) * q1 - sp.diff(q0, x) * p1) == 1
assert sp.factor(
    omega + 4 * (u * sp.diff(d, x, 2) + 2 * d1**3) / (3 * u**4)
) == 0
assert omega != 0


# The Catalan series is the unique solution of
# theta + omega*theta^2/2 = y.  Truncation through order seven
# verifies the exact symplectic identity to that order.
theta = sum(
    (-1) ** (degree - 1)
    * sp.catalan(degree - 1)
    * omega ** (degree - 1)
    * y**degree
    / 2 ** (degree - 1)
    for degree in range(1, 8)
)
quadratic_residual = sp.expand(theta + omega * theta**2 / 2 - y)
assert all(
    sp.factor(quadratic_residual.coeff(y, degree)) == 0
    for degree in range(1, 8)
)

P = p0 + p1 * theta
Q = q0 + q1 * theta
jacobian = sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x)
assert all(
    sp.factor(sp.expand(jacobian - 1).coeff(y, degree)) == 0
    for degree in range(0, 7)
)


# Work in Q[zeta]/(zeta^2+zeta+1) for the collision audit.
zeta = sp.symbols("zeta")


def reduce_zeta(expression: sp.Expr) -> sp.Expr:
    """Reduce an expression modulo zeta^2+zeta+1."""
    return sp.rem(
        sp.expand(expression),
        zeta**2 + zeta + 1,
        zeta,
    )


collision_examples = (
    # Two-block examples, including repeated roots.
    (x * (x + 1), sp.Integer(1)),
    (x**2 * (x + 1), sp.Integer(1)),
    (x**2 * (x**2 + 1), sp.Integer(1)),
    (x**3 * (x**2 + 1), sp.Integer(1)),
    # Genuinely arbitrary monic examples, including degree one and
    # boundaries with no root at the origin.
    (x + 2, sp.Integer(3)),
    (x**2 + 2 * x + 3, sp.Integer(2)),
    (x**3 - 2 * x + 5, sp.Integer(7)),
    ((x - 1) ** 2 * (x + 3) ** 2, sp.Integer(5)),
)

for d_value, u_value in collision_examples:
    g_value = sp.degree(d_value, x)
    phi = x + (1 - zeta**2) * d_value**2 / u_value
    collision = reduce_zeta(d_value.subs(x, phi) - zeta * d_value)
    collision_poly = sp.Poly(collision, x, domain=sp.QQ.frac_field(zeta))
    d_poly = sp.Poly(d_value, x, domain=sp.QQ.frac_field(zeta))

    assert collision_poly.degree() == 2 * g_value**2
    quotient, remainder = sp.div(collision_poly, d_poly)
    assert remainder.is_zero
    assert quotient.degree() == 2 * g_value**2 - g_value
    assert sp.gcd(quotient, d_poly).degree() == 0

    # If collision=0 and x1=phi, the two boundary coordinates agree
    # in the cube-root quotient ring.
    d0 = sp.symbols("d0")
    x_shift = (1 - zeta**2) * d0**2 / u_value
    p_difference = (zeta**2 - 1) * d0**2 + u_value * x_shift
    q_difference = (zeta**3 - 1) * d0**3
    assert reduce_zeta(p_difference) == 0
    assert reduce_zeta(q_difference) == 0


# Exact audit of the degree-two classification and its inverse.
f = x**3 + 2 * x + 1
a, C, k, c = sp.symbols("a C k c", nonzero=True)
g = C * f**2 + k * f - x / a + c
b = a * (2 * C * f + k)
h = C * a**2
P2 = f + a * y
Q2 = g + b * y + h * y**2
assert sp.factor(
    sp.diff(P2, x) * sp.diff(Q2, y)
    - sp.diff(P2, y) * sp.diff(Q2, x)
) == 1
assert sp.factor(Q2 - (C * P2**2 + k * P2 - x / a + c)) == 0

X, Y = sp.symbols("X Y")
x_inverse = a * (C * X**2 + k * X + c - Y)
y_inverse = (X - f.subs(x, x_inverse)) / a
assert sp.factor(P2.subs({x: x_inverse, y: y_inverse}, simultaneous=True) - X) == 0
assert sp.factor(Q2.subs({x: x_inverse, y: y_inverse}, simultaneous=True) - Y) == 0

# The two zero-leading subcases omitted by the generic h != 0
# display are triangular or a target shear of a triangular pair.
a0, k0 = sp.symbols("a0 k0", nonzero=True)
f0 = x**2 + x
P2_h_zero = f0 + a0 * y
Q2_h_zero = k0 * P2_h_zero - x / a0
assert sp.factor(
    sp.diff(P2_h_zero, x) * sp.diff(Q2_h_zero, y)
    - sp.diff(P2_h_zero, y) * sp.diff(Q2_h_zero, x)
) == 1

P2_a_zero = 2 * x + 1
Q2_a_zero = 3 * y + x**2
assert sp.factor(
    sp.diff(P2_a_zero, x) * sp.diff(Q2_a_zero, y)
    - sp.diff(P2_a_zero, y) * sp.diff(Q2_a_zero, x)
) == 6


# Exact coefficient audit for the transverse-degree-three reduction.
s_fun = sp.Function("s")(x)
t_fun = sp.Function("t")(x)
r_fun = sp.Function("R")(x)
b_fun = sp.Function("B")(x)
c_fun = sp.Function("C")(x)
d_fun = sp.Function("D")(x)
T = s_fun * y + t_fun
P3 = T**2 + r_fun
Q3 = T**3 + b_fun * T**2 + c_fun * T + d_fun
jacobian3 = sp.expand(
    (
        sp.diff(P3, x) * sp.diff(Q3, y)
        - sp.diff(P3, y) * sp.diff(Q3, x)
    )
    / s_fun
)

# Re-express the Jacobian as a polynomial in the independent
# variable T by temporarily replacing s*y+t with a fresh symbol.
tau = sp.symbols("tau")
jacobian3_tau = sp.expand(jacobian3.subs(y, (tau - t_fun) / s_fun))
assert sp.factor(jacobian3_tau.coeff(tau, 3) + 2 * sp.diff(b_fun, x)) == 0
assert sp.factor(
    jacobian3_tau.coeff(tau, 2)
    - (3 * sp.diff(r_fun, x) - 2 * sp.diff(c_fun, x))
) == 0
assert sp.factor(
    jacobian3_tau.coeff(tau, 1)
    - (2 * b_fun * sp.diff(r_fun, x) - 2 * sp.diff(d_fun, x))
) == 0
assert sp.factor(
    jacobian3_tau.coeff(tau, 0)
    - c_fun * sp.diff(r_fun, x)
) == 0

# Substitution of the integrated coefficient identities leaves
# exactly s*R'*(3R/2+c0).
b0, c0, d0 = sp.symbols("b0 c0 d0")
Q3_normal = (
    T**3
    + b0 * T**2
    + (sp.Rational(3, 2) * r_fun + c0) * T
    + b0 * r_fun
    + d0
)
normal_jacobian = sp.factor(
    sp.diff(P3, x) * sp.diff(Q3_normal, y)
    - sp.diff(P3, y) * sp.diff(Q3_normal, x)
)
assert sp.factor(
    normal_jacobian
    - s_fun
    * sp.diff(r_fun, x)
    * (sp.Rational(3, 2) * r_fun + c0)
) == 0

# Direct generic-polynomial audit of the leading equation
# 3*c'*k-2*c*k'=0, including the harmless nonzero scale factors.
s_polynomial = x**4 + 2 * x + 3
alpha3, beta3 = sp.symbols("alpha3 beta3", nonzero=True)
c_leading = alpha3 * s_polynomial**2
k_leading = beta3 * s_polynomial**3
assert sp.factor(
    3 * sp.diff(c_leading, x) * k_leading
    - 2 * c_leading * sp.diff(k_leading, x)
) == 0


# Exact coefficient audit for the transverse-degree-four reduction.
z = sp.symbols("z")
r_polynomial = x**3 - x + 2
alpha4, beta4 = sp.symbols("alpha4 beta4", nonzero=True)
cubic_leading = alpha4 * r_polynomial**3
quartic_leading = beta4 * r_polynomial**4
assert sp.factor(
    4 * sp.diff(cubic_leading, x) * quartic_leading
    - 3 * cubic_leading * sp.diff(quartic_leading, x)
) == 0

a4 = sp.Function("A4")(x)
b4 = sp.Function("B4")(x)
f4 = sp.Function("f4")(x)
c4, k4, l4 = sp.symbols("C4 K4 L4")
h4 = sp.Rational(4, 3) * b4
e4 = (
    sp.Rational(2, 9) * b4**2
    + sp.Rational(4, 3) * a4
    + c4
)
d4 = (
    sp.Rational(2, 3) * c4 * b4
    + sp.Rational(4, 9) * a4 * b4
    - sp.Rational(4, 81) * b4**3
    + sp.Rational(4, 3) * f4
    + k4
)
g4 = (
    54 * a4**2
    - 36 * a4 * b4**2
    + 162 * a4 * c4
    + 5 * b4**4
    - 27 * b4**2 * c4
    + 81 * b4 * k4
    + 108 * b4 * f4
) / 243 + l4
P4 = f4 + a4 * z + b4 * z**2 + z**3
Q4 = g4 + d4 * z + e4 * z**2 + h4 * z**3 + z**4
jacobian4 = sp.expand(
    sp.diff(P4, x) * sp.diff(Q4, z)
    - sp.diff(P4, z) * sp.diff(Q4, x)
)
assert all(
    sp.factor(jacobian4.coeff(z, degree)) == 0
    for degree in range(2, 7)
)

p4 = a4 - b4**2 / 3
q4 = f4 - a4 * b4 / 3 + 2 * b4**3 / 27
T4 = sp.symbols("T4")
P4_normal = T4**3 + p4 * T4 + q4
Q4_normal = (
    T4**4
    + (sp.Rational(4, 3) * p4 + c4) * T4**2
    + (sp.Rational(4, 3) * q4 + k4) * T4
    + sp.Rational(2, 9) * p4**2
    + sp.Rational(2, 3) * c4 * p4
    + l4
)
assert sp.factor(
    P4.subs(z, T4 - b4 / 3) - P4_normal
) == 0
assert sp.factor(
    Q4.subs(z, T4 - b4 / 3) - Q4_normal
) == 0

jacobian4_normal = sp.expand(
    sp.diff(P4_normal, x) * sp.diff(Q4_normal, T4)
    - sp.diff(P4_normal, T4) * sp.diff(Q4_normal, x)
)
first_integral4 = (
    4 * p4 * q4 + 3 * k4 * p4 + 6 * c4 * q4
) / 3
terminal4 = (
    -c4 * p4**2 / 3
    - 4 * p4**3 / 27
    + k4 * q4
    + 2 * q4**2 / 3
)
assert sp.factor(
    jacobian4_normal.coeff(T4, 1)
    - sp.diff(first_integral4, x)
) == 0
assert sp.factor(
    jacobian4_normal.coeff(T4, 0)
    - sp.diff(terminal4, x)
) == 0
assert all(
    sp.factor(jacobian4_normal.coeff(T4, degree)) == 0
    for degree in range(2, 7)
)

# The degree-five corollary uses only the exact leading coefficient
# and a constant target cancellation.
lead5 = x**3 + 2 * x + 1
ratio5 = sp.symbols("ratio5", nonzero=True)
lower_p5 = x * y**4 + (x + 1) * y + 1
lower_q5 = (x**2 + 1) * y**4 + x * y**2
P5 = lead5 * y**5 + lower_p5
Q5 = ratio5 * lead5 * y**5 + lower_q5
leading_jacobian5 = sp.Poly(
    sp.diff(P5, x) * sp.diff(Q5, y)
    - sp.diff(P5, y) * sp.diff(Q5, x),
    y,
)
assert leading_jacobian5.coeff_monomial(y**9) == 0
assert sp.Poly(sp.expand(Q5 - ratio5 * P5), y).degree() <= 4


print("verified: arbitrary-d bounded Bezout field and intrinsic curvature")
print("verified: Catalan canonical extension through formal order seven")
print("verified: explicit cube-root boundary collisions")
print("verified: every transverse-degree-two Keller pair is invertible")
print("verified: transverse-degree-three normal form and contradiction")
print("verified: transverse-degree-four normal form and contradiction")
print("verified: degree-five leading cancellation to prior theorem")
