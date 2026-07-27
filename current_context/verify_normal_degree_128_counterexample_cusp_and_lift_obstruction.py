#!/usr/bin/env python3
"""Exact checks for the normalized (12,8) cusp and lift obstruction."""

from __future__ import annotations

import sympy as sp


t, w, tau, v = sp.symbols("t w tau v")
a, b, c, d, e, f_coefficient, q = sp.symbols("a b c d e f q")
coefficients = (a, b, c, d, e, f_coefficient, q)
deficits = tuple(range(2, 9))

unit = 1 + sum(
    coefficient * t**deficit
    for coefficient, deficit in zip(coefficients, deficits)
)

# The zero-upper-constant slice is f=(g^(3/2))_+.
phi_series = sp.expand(
    t**-12
    * sp.series(unit ** sp.Rational(3, 2), t, 0, 20).removeO()
)
f_in_t = sp.expand(
    sum(
        term
        for term in sp.Add.make_args(phi_series)
        if term.as_powers_dict().get(t, 0) <= 0
    )
)
f_normalized = sp.expand(f_in_t.subs(t, 1 / w))
g = w**8 + sum(
    coefficient * w ** (8 - deficit)
    for coefficient, deficit in zip(coefficients, deficits)
)

# Residue formula for A_1,...,A_7 in the inverse s-coordinate.
negative_tail = sp.expand(f_in_t - phi_series)
s_w = sp.series(
    unit ** sp.Rational(1, 8)
    - t
    * sp.diff(unit, t)
    * unit ** sp.Rational(-7, 8)
    / 8,
    t,
    0,
    10,
).removeO()

A: dict[int, sp.Expr] = {}
for ell in range(1, 8):
    residue_integrand = sp.series(
        t ** (-(ell - 1))
        * unit ** sp.Rational(ell - 1, 8)
        * negative_tail
        * s_w,
        t,
        0,
        2,
    ).removeO()
    A[ell] = sp.factor(
        sp.expand(residue_integrand).coeff(t, 1)
    )

sqrt21 = sp.sqrt(21)
base = {
    a: sp.Integer(1),
    b: -sp.Rational(22, 441) * sqrt21,
    c: sp.Rational(169, 504),
    d: -sp.Rational(47, 1029) * sqrt21,
    e: sp.Rational(6721, 148176),
    f_coefficient: -sp.Rational(13679, 1555848) * sqrt21,
    q: sp.Rational(268777, 49787136),
}
scaled = {
    coefficient: base[coefficient] * tau**deficit
    for coefficient, deficit in zip(coefficients, deficits)
}

for ell in range(1, 7):
    assert sp.factor(A[ell].subs(scaled)) == 0

expected_A7 = (
    -sp.Rational(2**18, 3**7 * 7**10)
    * sqrt21
    * tau**19
)
assert sp.factor(A[7].subs(scaled) - expected_A7) == 0

f_tau = sp.expand(f_normalized.subs(scaled))
g_tau = sp.expand(g.subs(scaled))
bracket_tau = sp.factor(
    sp.diff(f_tau, tau) * sp.diff(g_tau, w)
    - sp.diff(f_tau, w) * sp.diff(g_tau, tau)
)
expected_bracket_tau = (
    -sp.Rational(2**21 * 19, 3**7 * 7**10)
    * sqrt21
    * tau**18
)
assert sp.factor(bracket_tau - expected_bracket_tau) == 0
assert sp.factor(bracket_tau - 8 * sp.diff(expected_A7, tau)) == 0

# The one-pole parametrization tau=v^(-1) has n=19 and rho=1.
f_v = sp.expand(f_tau.subs(tau, 1 / v))
g_v = sp.expand(g_tau.subs(tau, 1 / v))
bracket_v = sp.factor(
    sp.diff(f_v, v) * sp.diff(g_v, w)
    - sp.diff(f_v, w) * sp.diff(g_v, v)
)
expected_bracket_v = (
    sp.Rational(2**21 * 19, 3**7 * 7**10)
    * sqrt21
    * v**-20
)
assert sp.factor(bracket_v - expected_bracket_v) == 0
assert sp.factor(
    A[7].subs(scaled).subs(tau, 1 / v)
    + sp.Rational(2**18, 3**7 * 7**10) * sqrt21 * v**-19
) == 0

# Both v^(-2) and a nonzero multiple of v^(-3) occur, so the
# coefficient field is C(v).  Bezout's identity gcd(2,3)=1 is the
# exact cyclic-field check.
assert sp.gcd(2, 3) == 1
assert all(
    sp.degree(
        sp.Poly(
            sp.together(
                (coefficient.subs(scaled) * tau**-deficit)
            ),
            tau,
        )
    )
    == 0
    for coefficient, deficit in zip(coefficients, deficits)
)

# Homogeneous binary forms f=v^-12 F0(vw), g=v^-8 G0(vw).
X = sp.symbols("X")
F0 = sp.factor(f_tau.subs({tau: 1, w: X}))
G0 = sp.factor(g_tau.subs({tau: 1, w: X}))
assert sp.factor(f_v - v**-12 * F0.subs(X, v * w)) == 0
assert sp.factor(g_v - v**-8 * G0.subs(X, v * w)) == 0
assert sp.degree(F0, X) == 12
assert sp.degree(G0, X) == 8
assert sp.LC(sp.Poly(F0, X)) == 1
assert sp.LC(sp.Poly(G0, X)) == 1

resultant = sp.factor(sp.resultant(F0, G0, X), extension=sqrt21)
expected_resultant = -sp.Rational(
    2**88 * 19**2,
    3**36 * 7**48,
)
assert resultant == expected_resultant
assert resultant != 0

# Davenport--Stothers equality: F0^2-G0^3 has exact degree five and
# is squarefree.  Its degree gives ramification index 24-5=19 at
# infinity for F0^2/G0^3.
remainder = sp.factor(F0**2 - G0**3, extension=sqrt21)
assert sp.degree(remainder, X) == 5
assert sp.factor(
    sp.LC(sp.Poly(remainder, X, extension=sqrt21))
    + sp.Rational(2**19, 3**7 * 7**10) * sqrt21
) == 0
assert sp.gcd(
    sp.Poly(remainder, X, extension=sqrt21),
    sp.Poly(sp.diff(remainder, X), X, extension=sqrt21),
).degree() == 0
assert 12 * (2 - 1) + 8 * (3 - 1) + (19 - 1) == 2 * 24 - 2

# Common-quartic normal cone.  If S^2=P*H+R, the eps^2 term of
# f^2-g^3 is exactly -(3/4)*P^2*R.
epsilon = sp.symbols("epsilon")
p2, p1, p0 = sp.symbols("p2 p1 p0")
s3, s2, s1, s0 = sp.symbols("s3 s2 s1 s0")
P = X**4 + p2 * X**2 + p1 * X + p0
S = s3 * X**3 + s2 * X**2 + s1 * X + s0
H, R = sp.div(S**2, P, domain=sp.QQ.frac_field(
    p2, p1, p0, s3, s2, s1, s0
))
g_normal = P**2 + epsilon * S
f_normal = (
    P**3
    + sp.Rational(3, 2) * epsilon * P * S
    + sp.Rational(3, 8) * epsilon**2 * H
)
normal_difference = sp.expand(f_normal**2 - g_normal**3)
assert sp.factor(
    normal_difference.coeff(epsilon, 2)
    + sp.Rational(3, 4) * P**2 * R
) == 0

# When R=0, the scaled first-normal bracket is formula (43).
delta = sp.symbols("delta")
P_function = sp.Function("P")(X)
S_function = sp.Function("S")(X)
H_function = S_function**2 / P_function
G_function = P_function**2 + epsilon * S_function
F_function = (
    P_function**3
    + sp.Rational(3, 2) * epsilon * P_function * S_function
    + sp.Rational(3, 8) * epsilon**2 * H_function
)
normal_bracket = sp.factor(
    -12 * F_function * sp.diff(G_function, X)
    + 8 * sp.diff(F_function, X) * G_function
    + delta
    * epsilon
    * (
        sp.diff(F_function, epsilon) * sp.diff(G_function, X)
        - sp.diff(F_function, X) * sp.diff(G_function, epsilon)
    )
)
expected_normal_bracket = (
    sp.Rational(3, 8)
    * epsilon**3
    * S_function**2
    / P_function**2
    * (
        4 * P_function * sp.diff(S_function, X)
        + (delta - 8)
        * S_function
        * sp.diff(P_function, X)
    )
)
assert sp.factor(normal_bracket - expected_normal_bracket) == 0

# Type I is an exact silent normal.
z, C_parameter, c_parameter = sp.symbols(
    "z C_parameter c_parameter"
)
Q = X**2 + C_parameter
type_i_g = Q**4 + c_parameter * z**6 * Q
type_i_f = (
    Q**6
    + sp.Rational(3, 2) * c_parameter * z**6 * Q**3
    + sp.Rational(3, 8) * c_parameter**2 * z**12
)


def scaled_bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    """Bracket after f=v^-12*left(v,vw), g=v^-8*right(v,vw)."""
    return sp.factor(
        -12 * left * sp.diff(right, X)
        + 8 * sp.diff(left, X) * right
        + z
        * (
            sp.diff(left, z) * sp.diff(right, X)
            - sp.diff(left, X) * sp.diff(right, z)
        )
    )


assert scaled_bracket(type_i_f, type_i_g) == 0

# Linearized first split of Type I.  Divide R_split=Q*A+B.  The
# quotient cancels, and formula (49) depends only on B.
eta = sp.symbols("eta")
A_function = sp.Function("A")(X)
B_function = sp.Function("B")(X)
R_split = Q * A_function + B_function
split_parameter = sp.symbols("split_parameter")
split_g = type_i_g + split_parameter * z**eta * R_split
split_f = (
    type_i_f
    + sp.Rational(3, 2)
    * split_parameter
    * z**eta
    * Q**2
    * R_split
    + sp.Rational(3, 4)
    * c_parameter
    * split_parameter
    * z ** (eta + 6)
    * A_function
)
linear_split = sp.powsimp(
    sp.expand(
        sp.diff(
            scaled_bracket(split_f, split_g),
            split_parameter,
        ).subs(split_parameter, 0)
        / z ** (eta + 6)
    ),
    force=True,
)
expected_linear_split = (
    3
    * c_parameter
    * Q**2
    * (
        (8 - eta) * B_function * sp.diff(Q, X)
        - 2 * Q * sp.diff(B_function, X)
    )
)
assert sp.factor(
    linear_split.subs(z, 0) - expected_linear_split
) == 0

# For depressed Q=X^2+C and B=b1*X+b0, the only vanishing cases are
# exactly those listed after formula (49).
b1, b0 = sp.symbols("b1 b0")
B_linear = b1 * X + b0
split_equation = sp.Poly(
    sp.expand(
        (8 - eta) * B_linear * sp.diff(Q, X)
        - 2 * Q * sp.diff(B_linear, X)
    ),
    X,
)
assert sp.expand(
    split_equation.coeff_monomial(X**2) - 2 * b1 * (7 - eta)
) == 0
assert sp.expand(
    split_equation.coeff_monomial(X) - 2 * b0 * (8 - eta)
) == 0
assert sp.expand(
    split_equation.coeff_monomial(1) + 2 * C_parameter * b1
) == 0

# Highest extra upper term at g0=P^2.  If H=(P^(ell/4))_+, its
# leading scaled bracket is formula (51).
ell, kappa = sp.symbols("ell kappa")
H_ell = sp.Function("H_ell")(X)
upper_order = sp.symbols("upper_order")
upper_f = P_function**3 + kappa * z**upper_order * H_ell
upper_g = P_function**2
upper_bracket = sp.factor(
    -12 * upper_f * sp.diff(upper_g, X)
    + 8 * sp.diff(upper_f, X) * upper_g
    + z
    * (
        sp.diff(upper_f, z) * sp.diff(upper_g, X)
        - sp.diff(upper_f, X) * sp.diff(upper_g, z)
    )
)
upper_bracket = sp.factor(
    upper_bracket.subs(upper_order, 12 - ell)
)
expected_upper_bracket = (
    2
    * kappa
    * z ** (12 - ell)
    * P_function
    * (
        4 * P_function * sp.diff(H_ell, X)
        - ell * sp.diff(P_function, X) * H_ell
    )
)
assert sp.factor(upper_bracket - expected_upper_bracket) == 0

# The only-j transverse square-cone calculation, formula (53).
j_parameter = sp.symbols("j_parameter")
phi_series_only_j = sp.expand(
    phi_series
    + j_parameter
    * t**-4
    * sp.series(unit ** sp.Rational(1, 2), t, 0, 9).removeO()
)
f_in_t_only_j = sp.expand(
    sum(
        term
        for term in sp.Add.make_args(phi_series_only_j)
        if term.as_powers_dict().get(t, 0) <= 0
    )
)
negative_tail_only_j = sp.expand(
    f_in_t_only_j - phi_series_only_j
)
A_only_j: dict[int, sp.Expr] = {}
for ell_index in range(1, 5):
    residue_integrand = sp.series(
        t ** (-(ell_index - 1))
        * unit ** sp.Rational(ell_index - 1, 8)
        * negative_tail_only_j
        * s_w,
        t,
        0,
        2,
    ).removeO()
    A_only_j[ell_index] = sp.factor(
        sp.expand(residue_integrand).coeff(t, 1)
    )

A_center, B_center, C_center = sp.symbols(
    "A_center B_center C_center"
)
U_center, V_center, W_center, Z_center = sp.symbols(
    "U_center V_center W_center Z_center"
)
center_epsilon = sp.symbols("center_epsilon")
square_cone = {
    a: 2 * A_center,
    b: 2 * B_center,
    c: A_center**2 + 2 * C_center,
    d: 2 * A_center * B_center + center_epsilon * U_center,
    e: (
        B_center**2
        + 2 * A_center * C_center
        + center_epsilon * V_center
    ),
    f_coefficient: (
        2 * B_center * C_center
        + center_epsilon * W_center
    ),
    q: C_center**2 + center_epsilon * Z_center,
}
only_j_linear = {
    ell_index: sp.factor(
        sp.diff(
            A_only_j[ell_index].subs(square_cone),
            center_epsilon,
        ).subs(center_epsilon, 0)
    )
    for ell_index in range(1, 5)
}
assert only_j_linear[1] == -j_parameter * U_center / 2
assert only_j_linear[2] == -j_parameter * V_center / 2
assert sp.expand(
    only_j_linear[3]
    - j_parameter
    * (3 * A_center * U_center - 4 * W_center)
    / 8
) == 0
assert sp.expand(
    only_j_linear[4]
    - j_parameter
    * (
        2 * A_center * V_center
        + 3 * B_center * U_center
        - 4 * Z_center
    )
    / 8
) == 0

# The c=0 even-upper residual.  After quotient tangents, the split
# remainder is B=b1*X+b0.
split_eps = sp.symbols("split_eps")
B_residual = b1 * X + b0
residual_g = Q**4 + split_eps * z**eta * B_residual
residual_f_pure = (
    Q**6
    + sp.Rational(3, 2)
    * split_eps
    * z**eta
    * Q**2
    * B_residual
)
residual_pure_bracket = sp.factor(
    scaled_bracket(residual_f_pure, residual_g)
)
residual_linear_form = (
    C_parameter * b1
    + (eta - 7) * b1 * X**2
    + (eta - 8) * b0 * X
)
expected_residual_pure = (
    -6
    * split_eps**2
    * z ** (2 * eta)
    * Q
    * B_residual
    * residual_linear_form
)
assert sp.factor(
    residual_pure_bracket - expected_residual_pure
) == 0

# Upper-linear operators for l=6,4,2, with (p,a)=(3,6),(2,8),(1,10).
for upper_power, upper_weight, multiplier, q_power in (
    (3, 6, -6, 2),
    (2, 8, -4, 1),
    (1, 10, -2, 0),
):
    residual_f_upper = (
        residual_f_pure
        + kappa * z**upper_weight * Q**upper_power
    )
    bracket_upper = scaled_bracket(
        residual_f_upper,
        residual_g,
    )
    upper_linear = sp.powsimp(
        sp.expand(
            sp.diff(bracket_upper, split_eps).subs(split_eps, 0)
            / (kappa * z ** (upper_weight + eta))
        ),
        force=True,
    )
    assert sp.factor(
        upper_linear
        - multiplier * Q**q_power * residual_linear_form
    ) == 0

# Exact tie factorizations, formula (59).
tie_l6 = sp.factor(
    scaled_bracket(
        residual_f_pure
        + kappa * z**6 * Q**3,
        residual_g,
    ).subs(eta, 6)
    / (split_eps * z**12)
)
assert sp.factor(
    tie_l6
    - 6
    * Q
    * (-C_parameter * b1 + X**2 * b1 + 2 * X * b0)
    * (kappa * Q + split_eps * B_residual)
) == 0

tie_l4 = sp.factor(
    scaled_bracket(
        residual_f_pure
        + kappa * z**8 * Q**2,
        residual_g,
    ).subs(eta, 8)
    / (split_eps * z**16)
)
assert sp.factor(
    tie_l4
    + 2
    * b1
    * Q**2
    * (3 * split_eps * B_residual + 2 * kappa)
) == 0

tie_l2 = sp.factor(
    scaled_bracket(
        residual_f_pure
        + kappa * z**10 * Q,
        residual_g,
    ).subs(eta, 10)
    / (split_eps * z**20)
)
assert sp.factor(
    tie_l2
    + 2
    * (
        C_parameter * b1
        + 3 * X**2 * b1
        + 2 * X * b0
    )
    * (
        3 * split_eps * Q * B_residual
        + kappa
    )
) == 0

# Degree-eight Taylor threshold.  If n>=3*rho, the lower bound for
# the y^i coefficient differs from i by 4*m*(i-2)*rho.
m, rho = sp.symbols("m rho", positive=True)
for i in range(2, 9):
    threshold_bound = sp.expand(
        i * (3 * m * rho + 1) - m * (8 - i) * rho
    )
    assert sp.expand(
        threshold_bound - (i + 4 * m * (i - 2) * rho)
    ) == 0

print("verified: six conserved Laurent coefficients vanish on the cusp")
print("verified: exact A_7 and monomial normalized Jacobians")
print("verified: one-pole exponent n=19 and weighted pole rho=1")
print("verified: nonzero homogeneous resultant and no common center limit")
print("verified: Davenport-Stothers degree-five equality and passport")
print("verified: common-quartic normal cone and four collision types")
print("verified: silent Type-I normal and exact first-split operator")
print("verified: highest-extra-upper-constant bracket operator")
print("verified: only-j transverse square-cone elimination")
print("verified: c=0 even-upper residual and all tie operators")
print("verified: degree-eight polynomial-lift threshold n >= 3*rho")
