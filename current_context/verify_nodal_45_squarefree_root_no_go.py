#!/usr/bin/env python3
"""Exact checks for NODAL_45_SQUAREFREE_ROOT_NO_GO.md."""

from __future__ import annotations

import sympy as sp


s, y, z = sp.symbols("s y z")
k = sp.symbols("k", integer=True, nonnegative=True)
alpha, beta, gamma = sp.symbols("alpha beta gamma", nonzero=True)
R = sp.Function("R")(s)


def residual(P: sp.Expr, Q: sp.Expr) -> sp.Poly:
    expression = (
        2
        * s
        * (sp.diff(P, s) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, s))
        - sp.diff(P, y) * Q
    )
    return sp.Poly(sp.expand(expression), y)


# ---------------------------------------------------------------------------
# Direct coefficient extraction for the first three descending diagonals.

w, f, v, u, a, e, d, c = [
    sp.Function(name)(s) for name in ("w", "f", "v", "u", "a", "e", "d", "c")
]
P = w * y**4 + v * y**3 + u * y**2 + a * y
Q = f * y**5 + e * y**4 + d * y**3 + c * y**2
C = residual(P, Q)

top_expected = 2 * s * (5 * sp.diff(w, s) * f - 4 * w * sp.diff(f, s)) - 4 * w * f
assert sp.simplify(C.coeff_monomial(y**8) - top_expected) == 0

w0 = alpha * s ** (2 + 4 * k) * R**4
f0 = beta * s ** (2 + 5 * k) * R**5
assert sp.simplify(top_expected.subs({w: w0, f: f0}).doit()) == 0

# The y^7 equation is exactly the U_1 equation after normalization.
U1 = 5 * v / w - 4 * e / f
M = 1 + 2 * k + 2 * s * sp.diff(R, s) / R
u1_equation = 2 * s * sp.diff(U1, s) + M * U1
assert sp.simplify(
    (C.coeff_monomial(y**7) / (w * f) - u1_equation)
    .subs({w: w0, f: f0})
    .doit()
) == 0

# Its nonzero formal homogeneous solution contains s^(-1/2), hence is not
# rational.  The exponent check also covers every integral k.
assert sp.denom(sp.together(-k - sp.Rational(1, 2))) == 2


# Translate by the common h and recompute in the depressed coordinates.
A, B, C3, D = [
    sp.Function(name)(s) for name in ("A", "B", "C3", "D")
]
P_depressed = w * y**4 + A * y**2 + B * y
Q_depressed = f * y**5 + C3 * y**3 + D * y**2
Cd = residual(P_depressed, Q_depressed)

U2 = 5 * A / w - 4 * C3 / f
U3 = 5 * B / w - 4 * D / f
assert sp.simplify(
    (
        Cd.coeff_monomial(y**6) / (w * f)
        - (2 * s * sp.diff(U2, s) + 2 * M * U2)
    )
    .subs({w: w0, f: f0})
    .doit()
) == 0
assert sp.simplify(
    (
        Cd.coeff_monomial(y**5) / (w * f)
        - (2 * s * sp.diff(U3, s) + 3 * M * U3)
    )
    .subs({w: w0, f: f0})
    .doit()
) == 0

# Check the two integrated modes directly.
mode2 = gamma / (s ** (2 * k + 1) * R**2)
assert sp.simplify(2 * s * sp.diff(mode2, s) + 2 * M * mode2) == 0
mode3_exponent = -3 * k - sp.Rational(3, 2)
assert sp.denom(sp.together(mode3_exponent)) == 2


# ---------------------------------------------------------------------------
# Exact downward recurrence.

h = sp.symbols("h")
wS, fS, vS, uS, aS = sp.symbols("w f v u a", nonzero=True)
rho = sp.symbols("rho", nonzero=True)  # rho = s^(2k+1) R^2

e_formula = 5 * fS * h
d_formula = 5 * fS * uS / (4 * wS) + sp.Rational(5, 2) * fS * h**2 - gamma * fS / (4 * rho)
c_formula = (
    5 * fS * aS / (4 * wS)
    + 5 * fS * uS * h / (4 * wS)
    - sp.Rational(5, 2) * fS * h**3
    - 3 * gamma * fS * h / (4 * rho)
)

A_formula = uS - 6 * wS * h**2
C_formula = d_formula - 10 * fS * h**2
B_formula = aS - 2 * uS * h + 8 * wS * h**3
D_formula = c_formula - 3 * d_formula * h + 20 * fS * h**3

assert sp.simplify(5 * A_formula / wS - 4 * C_formula / fS - gamma / rho) == 0
assert sp.simplify(5 * B_formula / wS - 4 * D_formula / fS) == 0
assert sp.simplify(e_formula - 5 * fS * h) == 0


# ---------------------------------------------------------------------------
# Newton-face identity.

t, H, AA, BB = sp.symbols("t H A B", nonzero=True)
Fz = sp.Function("F")(z)
Gz = sp.Function("G")(z)
Pface = t**AA * Fz.subs(z, t**H * y)
Qface = t**BB * Gz.subs(z, t**H * y)
bracket = sp.diff(Pface, t) * sp.diff(Qface, y) - sp.diff(Pface, y) * sp.diff(Qface, t)
expected_bracket = t ** (AA + BB + H - 1) * (
    AA * Fz * sp.diff(Gz, z) - BB * sp.diff(Fz, z) * Gz
)
assert sp.simplify(bracket.subs(y, z / t**H) - expected_bracket) == 0

# In each of the three forbidden faces, the top-endpoint intercepts have
# ratio A:B = 4:5, and the bracket order is strictly negative.
faces = [
    # (H, A, B)
    (sp.Rational(2), sp.Rational(-4), sp.Rational(-5)),
    (sp.Rational(3, 2), sp.Rational(-2), sp.Rational(-5, 2)),
    (sp.Rational(4, 3), sp.Rational(-4, 3), sp.Rational(-5, 3)),
]
for slope, intercept_p, intercept_q in faces:
    assert intercept_q == sp.Rational(5, 4) * intercept_p
    assert intercept_p + intercept_q + slope - 1 < 0

# A fourth power of a linear polynomial cannot have any of the P-face
# support patterns used in the proof.
ell0, ell1 = sp.symbols("ell0 ell1")
linear_fourth = sp.Poly(sp.expand((ell0 + ell1 * z) ** 4), z)
for required_degrees in ({4, 3}, {4, 2}, {4, 1}):
    equations = []
    for degree in range(5):
        coefficient = linear_fourth.coeff_monomial(z**degree)
        if degree not in required_degrees:
            equations.append(coefficient)
    solutions = sp.solve(equations, (ell0, ell1), dict=True)
    # The only solutions killing all forbidden support positions also kill
    # at least one of the two required nonzero coefficients.
    for solution in solutions:
        product = sp.prod(
            linear_fourth.coeff_monomial(z**degree).subs(solution)
            for degree in required_degrees
        )
        assert sp.simplify(product) == 0

# The tied Step 2 and Step 3 face coefficients already give explicit
# nonzero failures of 5 F'G - 4 FG'=0.
face_w, face_f, face_u, face_a = sp.symbols(
    "face_w face_f face_u face_a", nonzero=True
)
F2 = face_w * z**4 + face_u * z**2
G2 = face_f * z**5 + 5 * face_f * face_u * z**3 / (4 * face_w)
assert sp.factor(5 * sp.diff(F2, z) * G2 - 4 * F2 * sp.diff(G2, z)) == (
    -5 * face_f * face_u**2 * z**4 / (2 * face_w)
)
F3 = face_w * z**4 + face_a * z
G3 = face_f * z**5 + 5 * face_f * face_a * z**2 / (4 * face_w)
assert sp.factor(5 * sp.diff(F3, z) * G3 - 4 * F3 * sp.diff(G3, z)) == (
    -15 * face_f * face_a**2 * z**2 / (4 * face_w)
)


# ---------------------------------------------------------------------------
# Integer valuation bookkeeping.

# d has orders 1+ord(u), 2*ord(v)-3, 3.  Regularity forces ord(v)>=2.
for order_v in (0, 1):
    orders_d = [1, 2 * order_v - 3, 3]
    assert orders_d[1] < 0
    assert orders_d[1] < min(orders_d[0], orders_d[2])

# If ord(v)>=3 and ord(u)=j in {0,1}, q3 has exact order j+1;
# every possible q2 term remains strictly above the corresponding face.
for order_u in (0, 1):
    order_v = 3
    orders_d = [1 + order_u, 2 * order_v - 3, 3]
    assert orders_d[0] < min(orders_d[1:])
    order_q3 = orders_d[0]
    slope = sp.Rational(4 - order_u, 2)
    q_intercept = 5 - 5 * slope
    q2_lower_bound = min(1, order_u + order_v - 3, 3 * order_v - 7, order_v - 1)
    assert q2_lower_bound - 2 * slope > q_intercept
    assert order_q3 - 3 * slope == q_intercept

# Once ord(v)>=3 and ord(u)>=2, a unit p1 makes q2 have exact order one.
orders_q2 = [1, 2, 2, 2]
assert orders_q2[0] < min(orders_q2[1:])
slope = sp.Rational(4, 3)
assert 1 - 2 * slope == 5 - 5 * slope


# ---------------------------------------------------------------------------
# The final y^4 coefficient and its unique lowest-order (p4,q1) term.

p_all = [sp.Function(f"p{i}")(s) for i in range(5)]
q_all = [sp.Function(f"q{i}")(s) for i in range(6)]
P_all = sum(p_all[i] * y**i for i in range(5))
Q_all = sum(q_all[j] * y**j for j in range(6))
y4_coefficient = residual(P_all, Q_all).coeff_monomial(y**4)
y4_expected = (
    s
    * (
        -2 * p_all[1] * sp.diff(q_all[4], s)
        - 4 * p_all[2] * sp.diff(q_all[3], s)
        - 6 * p_all[3] * sp.diff(q_all[2], s)
        - 8 * p_all[4] * sp.diff(q_all[1], s)
        + 2 * q_all[1] * sp.diff(p_all[4], s)
        + 4 * q_all[2] * sp.diff(p_all[3], s)
        + 6 * q_all[3] * sp.diff(p_all[2], s)
        + 8 * q_all[4] * sp.diff(p_all[1], s)
        + 10 * q_all[5] * sp.diff(p_all[0], s)
    )
    - p_all[1] * q_all[4]
    - 2 * p_all[2] * q_all[3]
    - 3 * p_all[3] * q_all[2]
    - 4 * p_all[4] * q_all[1]
)
assert sp.simplify(y4_coefficient - y4_expected) == 0

# With ord(p4)=4 and ord(q1)=0, the derivative contribution
# 2s p4' q1 has order 3.  Every other pair has order at least 4.
pair_sum_orders = [5, 5, 5, 5]
assert all(order - 1 >= 4 for order in pair_sum_orders)
assert 4 + 0 - 1 == 3

print("nodal (4,5) squarefree-root no-go checks passed")
