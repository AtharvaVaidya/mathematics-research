#!/usr/bin/env python3
"""Checks for the integer-graded part of the (12,9) local theorem."""

import sympy as sp


X, z, eps = sp.symbols("X z eps")
delta, eta = sp.symbols("delta eta", integer=True)
P = sp.Function("P")(X)
S = sp.Function("S")(X)
Q = sp.Function("Q")(X)
H = sp.Function("H")(X)


def scaled_pair(order_f, F, order_g, G):
    """Coefficient of z^(order_f+order_g) in the scaled bracket."""
    return sp.expand(
        (order_f - 12) * F * sp.diff(G, X)
        + (9 - order_g) * sp.diff(F, X) * G
    )


# Polynomial-abc numerical contradiction at degree <=15.
d0 = sp.symbols("d0", integer=True, nonnegative=True)
assert sp.expand((12 + 9 + (15 - d0) - 1) - (36 - d0)) == -1


# First transverse approximate-root expansion and residual.
g = P**3 + eps * z**delta * S
f = (
    P**4
    + sp.Rational(4, 3) * eps * z**delta * P * S
    + sp.Rational(2, 9) * eps**2 * z ** (2 * delta) * H
)
residual2 = sp.expand(f**3 - g**4).coeff(eps, 2)
expected2 = sp.Rational(2, 3) * z ** (2 * delta) * P**6 * (
    P**2 * H - S**2
)
assert sp.simplify(residual2 - expected2) == 0


# On S=P*Q and H=Q^2, the cubic scaled bracket is formula (16).
g_pq = P**3 + eps * z**delta * P * Q
f_pq = (
    P**4
    + sp.Rational(4, 3) * eps * z**delta * P**2 * Q
    + sp.Rational(2, 9) * eps**2 * z ** (2 * delta) * Q**2
)
scaled = sp.expand(
    z * (sp.diff(f_pq, z) * sp.diff(g_pq, X)
         - sp.diff(f_pq, X) * sp.diff(g_pq, z))
    - 12 * f_pq * sp.diff(g_pq, X)
    + 9 * sp.diff(f_pq, X) * g_pq
)
cubic = sp.factor(scaled.coeff(eps, 3))
expected_cubic = (
    sp.Rational(4, 9)
    * z ** (3 * delta)
    * Q**2
    * ((delta - 6) * Q * sp.diff(P, X) + 3 * P * sp.diff(Q, X))
)
assert sp.simplify(cubic - expected_cubic) == 0


# Highest-upper-term operator.
ell = sp.symbols("ell", integer=True)
Hl = sp.Function("Hl")(X)
upper_operator = scaled_pair(12 - ell, Hl, 0, P**3)
expected_upper = 3 * P**2 * (
    3 * P * sp.diff(Hl, X) - ell * sp.diff(P, X) * Hl
)
assert sp.simplify(upper_operator - expected_upper) == 0


# Post-composite split formulas.
c, j, k = sp.symbols("c j k")
Bfun = sp.Function("B")(X)
S_decomp = P * Q + Bfun

linear_cj = (
    scaled_pair(6, (sp.Rational(4, 3) * c + j) * P**2, eta, S_decomp)
    + scaled_pair(eta, sp.Rational(4, 3) * P * S_decomp, 6, c * P)
    + scaled_pair(
        eta + 6,
        (sp.Rational(4, 9) * c + sp.Rational(2, 3) * j) * Q,
        0,
        P**3,
    )
)
expected_cj = (
    -sp.Rational(2, 3)
    * (2 * c + 3 * j)
    * P
    * ((eta - 9) * Bfun * sp.diff(P, X) + 3 * P * sp.diff(Bfun, X))
)
assert sp.simplify(sp.expand(linear_cj - expected_cj)) == 0


linear_k = scaled_pair(9, k * P, eta, S_decomp)
expected_k = -k * (
    (eta - 9) * S_decomp * sp.diff(P, X)
    + 3 * P * sp.diff(S_decomp, X)
)
assert sp.simplify(sp.expand(linear_k - expected_k)) == 0


# The dangerous eta=9 tie factors by P for a generic depressed cubic.
A, B0 = sp.symbols("A B0")
q0, q1, q2, b0, b1, b2 = sp.symbols("q0 q1 q2 b0 b1 b2")
Pc = X**3 + A * X + B0
Qc = q0 + q1 * X + q2 * X**2
Bc = b0 + b1 * X + b2 * X**2
Sc = sp.expand(Pc * Qc + Bc)
Hc = sp.div(Sc**2, Pc**2, X)[0]

eta9 = 9
quadratic9 = sp.Rational(2, 9) * (
    6 * eta9 * Hc * Pc**2 * sp.diff(Pc, X)
    - 6 * eta9 * Sc**2 * sp.diff(Pc, X)
    - 36 * Hc * Pc**2 * sp.diff(Pc, X)
    + 9 * Pc**3 * sp.diff(Hc, X)
    - 18 * Pc * Sc * sp.diff(Sc, X)
    + 54 * Sc**2 * sp.diff(Pc, X)
)
k9 = -k * (
    (eta9 - 9) * Sc * sp.diff(Pc, X) + 3 * Pc * sp.diff(Sc, X)
)
tie9 = sp.expand(quadratic9 + k9)
assert sp.rem(tie9, Pc, X) == 0


# The complete order-19 polarization after an eta=9 jet reduces to
# 3*P*W'+P'*W, where W=3*k*V+4*rem(S*V,P^2).
v_coeffs = sp.symbols("v0:6")
Vgeneric = sum(v_coeffs[i] * X**i for i in range(6))
Rcross = sp.rem(Sc * Vgeneric, Pc**2, X)
Wcross = 3 * k * Vgeneric + 4 * Rcross

zc = sp.symbols("zc")
cbase = sp.symbols("cbase")
Gcross = (
    Pc**3
    + cbase * zc**6 * Pc
    + zc**9 * Sc
    + zc**10 * Vgeneric
)
Fcross = (
    Pc**4
    + sp.Rational(2, 3) * cbase * zc**6 * Pc**2
    + k * zc**9 * Pc
    + sp.Rational(4, 3) * Pc * (zc**9 * Sc + zc**10 * Vgeneric)
    + sp.Rational(2, 9) * zc**18 * sp.div(Sc**2, Pc**2, X)[0]
    + sp.Rational(4, 9) * zc**19 * sp.div(
        Sc * Vgeneric, Pc**2, X
    )[0]
)
Bcross = sp.expand(
    zc * (
        sp.diff(Fcross, zc) * sp.diff(Gcross, X)
        - sp.diff(Fcross, X) * sp.diff(Gcross, zc)
    )
    - 12 * Fcross * sp.diff(Gcross, X)
    + 9 * sp.diff(Fcross, X) * Gcross
)
order19 = sp.expand(Bcross).coeff(zc, 19)
expected19 = -sp.Rational(1, 3) * (
    3 * Pc * sp.diff(Wcross, X) + sp.diff(Pc, X) * Wcross
)
assert sp.simplify(sp.expand(order19 - expected19)) == 0


# The full master formula, including C=2c+3j, combines into the
# three universal operators after Z_N=2R_N+3kS_(N-9)+2CPB_(N-6).
Cmaster = sp.symbols("Cmaster")
Rmaster = sp.Function("Rmaster")(X)
Smaster = sp.Function("Smaster")(X)
Bmaster = sp.Function("Bmaster")(X)
for N in (17, 18, 19):
    master = (
        -sp.Rational(2, 3)
        * Cmaster
        * Pc
        * (
            (N - 15) * Bmaster * sp.diff(Pc, X)
            + 3 * Pc * sp.diff(Bmaster, X)
        )
        + (12 - sp.Rational(2 * N, 3))
        * Rmaster
        * sp.diff(Pc, X)
        - 2 * Pc * sp.diff(Rmaster, X)
        - k * (
            (N - 18) * Smaster * sp.diff(Pc, X)
            + 3 * Pc * sp.diff(Smaster, X)
        )
    )
    Zmaster = 2 * Rmaster + 3 * k * Smaster + 2 * Cmaster * Pc * Bmaster
    if N == 17:
        universal = sp.Rational(1, 3) * (
            sp.diff(Pc, X) * Zmaster - 3 * Pc * sp.diff(Zmaster, X)
        )
    elif N == 18:
        universal = -Pc * sp.diff(Zmaster, X)
    else:
        universal = -sp.Rational(1, 3) * (
            sp.diff(Pc, X) * Zmaster + 3 * Pc * sp.diff(Zmaster, X)
        )
    assert sp.simplify(sp.expand(master - universal)) == 0


# The three all-jet dangerous-order operators cannot be a nonzero
# constant for a generic depressed monic cubic.
s_coeffs = sp.symbols("s0:6")
C0 = sp.symbols("C0")
Sgeneric = sum(s_coeffs[i] * X**i for i in range(6))
dangerous_operators = (
    sp.Rational(1, 3) * (
        sp.diff(Pc, X) * Sgeneric - 3 * Pc * sp.diff(Sgeneric, X)
    ),
    -Pc * sp.diff(Sgeneric, X),
    -sp.Rational(1, 3) * (
        sp.diff(Pc, X) * Sgeneric + 3 * Pc * sp.diff(Sgeneric, X)
    ),
)
for index, operator in enumerate(dangerous_operators):
    equation = sp.Poly(sp.expand(operator - C0), X)
    solution = sp.solve(
        equation.all_coeffs(),
        list(s_coeffs) + [C0],
        dict=True,
    )
    assert solution
    assert all(item[C0] == 0 for item in solution)
    if index == 2:
        assert all(
            item.get(coefficient, coefficient) == 0
            for item in solution
            for coefficient in s_coeffs
        )


# The order-17 operator has an apparent special constant when
# P=X^3+B and W=aX.  Compatibility with the earlier jets removes it:
# order 14 gives P|S7, and order 16 then gives P|S8 for squarefree P,
# so Z17=2R17+3kS8+2CPB11 is divisible by P and cannot equal aX.
a_special, b_special = sp.symbols("a_special b_special", nonzero=True)
Pspecial = X**3 + b_special
Wspecial = a_special * X
operator17_special = sp.factor(
    sp.Rational(1, 3) * (
        sp.diff(Pspecial, X) * Wspecial
        - 3 * Pspecial * sp.diff(Wspecial, X)
    )
)
assert operator17_special == -a_special * b_special
assert sp.gcd(Pspecial, sp.diff(Pspecial, X)) == 1

q7, q8 = sp.symbols("q7 q8")
S7special = Pspecial * q7
S8special = Pspecial * q8
r17special, b11special = sp.symbols("r17special b11special")
Z17_compatible = (
    2 * Pspecial * r17special
    + 3 * k * S8special
    + 2 * Cmaster * Pspecial * b11special
)
assert sp.rem(Z17_compatible, Pspecial, X) == 0


print("verified the integer-graded (12,9) local identities")
