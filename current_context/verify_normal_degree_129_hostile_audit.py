#!/usr/bin/env python3
"""Exact checks for NORMAL_DEGREE_129_HOSTILE_AUDIT.md."""

import sympy as sp


X, t = sp.symbols("X t")


def pair(f_order, f_coeff, g_order, g_coeff):
    """Coefficient from a pair of scaled homogeneous z-orders."""
    return sp.expand(
        (f_order - 12) * f_coeff * sp.diff(g_coeff, X)
        + (9 - g_order) * sp.diff(f_coeff, X) * g_coeff
    )


# The finite-jet countermodel has a silent linearized coefficient,
# but its obstruction appears at the next order.
F_counter = X**4 + 4 * t * X
G_counter = X**3 + 3 * t
J_counter = sp.expand(
    sp.diff(F_counter, t) * sp.diff(G_counter, X)
    - sp.diff(F_counter, X) * sp.diff(G_counter, t)
)
assert J_counter == -12 * t

# It cannot be a polynomial common-component variation.
q = sp.Function("q")(X)
q_solution = sp.solve(
    [
        sp.Eq(4 * X**3 * q, 4 * X),
        sp.Eq(3 * X**2 * q, 3),
    ],
    [q],
    dict=True,
)
assert q_solution == [{q: X**-2}]
assert not q_solution[0][q].is_polynomial(X)


# Generic formulas for the eta=9 and eta=10 calculation.
P = sp.Function("P")(X)
S = sp.Function("S")(X)
T = sp.Function("T")(X)
H = sp.Function("H")(X)
K = sp.Function("K")(X)
k = sp.symbols("k")

E18 = (
    pair(18, sp.Rational(2, 9) * H, 0, P**3)
    + pair(9, sp.Rational(4, 3) * P * S, 9, S)
    + pair(9, k * P, 9, S)
)
R2 = S**2 - H * P**2
expected18 = -P * sp.diff(2 * R2 + 3 * k * S, X)
assert sp.simplify(E18 - expected18) == 0

E19 = (
    pair(19, sp.Rational(4, 9) * K, 0, P**3)
    + pair(9, sp.Rational(4, 3) * P * S, 10, T)
    + pair(10, sp.Rational(4, 3) * P * T, 9, S)
    + pair(9, k * P, 10, T)
)
RST = S * T - K * P**2
W = 4 * RST + 3 * k * T
expected19 = -sp.Rational(1, 3) * (
    3 * P * sp.diff(W, X) + sp.diff(P, X) * W
)
assert sp.simplify(E19 - expected19) == 0


# Exact nonconstant element of the eta=9 kernel.
Pc = X**3 - X
Sc = X**4 - 2 * X**2 + 1
kc = -sp.Rational(2, 3)
assert sp.rem(Sc**2 - Sc, Pc**2, X) == 0
Hc = sp.div(Sc**2, Pc**2, X)[0]
R2c = sp.expand(Sc**2 - Hc * Pc**2)
assert sp.diff(2 * R2c + 3 * kc * Sc, X) == 0


# For a monic depressed cubic and deg(W)<6, the order-19 operator
# can be constant only when W and that constant are zero.
A, B, constant = sp.symbols("A B constant")
w = sp.symbols("w0:6")
Pc_generic = X**3 + A * X + B
Wc = sum(w[i] * X**i for i in range(6))
operator = sp.Poly(
    sp.expand(
        3 * Pc_generic * sp.diff(Wc, X)
        + sp.diff(Pc_generic, X) * Wc
        - constant
    ),
    X,
)
solution = sp.solve(operator.all_coeffs(), list(w) + [constant], dict=True)
assert solution == [
    {
        constant: 0,
        w[0]: 0,
        w[1]: 0,
        w[2]: 0,
        w[3]: 0,
        w[4]: 0,
        w[5]: 0,
    }
]


# The all-jet convolution recurrence (10).  The identity is checked
# separately at every order so that all ordered cross-terms are present.
C = sp.symbols("C")
jets = {r: sp.Function(f"S{r}")(X) for r in range(7, 14)}
remainders = {n: sp.Function(f"R{n}")(X) for n in range(14, 20)}
quotients = {n: sp.Function(f"H{n}")(X) for n in range(14, 20)}

for total_order in range(14, 20):
    convolution = sum(
        (
            jets[i] * jets[total_order - i]
            for i in range(7, total_order - 6)
        ),
        sp.Integer(0),
    )
    Hn = quotients[total_order]
    Rn = remainders[total_order]

    quadratic_pairs = pair(
        total_order, sp.Rational(2, 9) * Hn, 0, P**3
    )
    quadratic_pairs += sum(
        (
            pair(
                i,
                sp.Rational(4, 3) * P * jets[i],
                total_order - i,
                jets[total_order - i],
            )
            for i in range(7, total_order - 6)
        ),
        sp.Integer(0),
    )

    symmetrized_pairs = (
        pair(total_order, sp.Rational(2, 9) * Hn, 0, P**3)
        - 2 * P * sp.diff(convolution, X)
        + sp.Rational(2 * (18 - total_order), 3)
        * sp.diff(P, X)
        * convolution
    )
    assert sp.simplify(quadratic_pairs - symmetrized_pairs) == 0

    # Now impose the defining convolution H_n P^2 + R_n.
    quadratic_reduced = sp.expand(
        pair(total_order, sp.Rational(2, 9) * Hn, 0, P**3)
        - 2 * P * sp.diff(Hn * P**2 + Rn, X)
        + sp.Rational(2 * (18 - total_order), 3)
        * sp.diff(P, X)
        * (Hn * P**2 + Rn)
    )
    expected_quadratic = (
        -2 * P * sp.diff(Rn, X)
        + sp.Rational(2 * (18 - total_order), 3)
        * sp.diff(P, X)
        * Rn
    )
    assert sp.simplify(quadratic_reduced - expected_quadratic) == 0

    if total_order >= 16:
        Sk = jets[total_order - 9]
        k_pair = pair(9, k * P, total_order - 9, Sk)
        expected_k_pair = (
            -3 * k * P * sp.diff(Sk, X)
            + (18 - total_order) * k * sp.diff(P, X) * Sk
        )
        assert sp.simplify(k_pair - expected_k_pair) == 0


# At order 17, classify every polynomial W of degree below six that
# can make (P'W - 3PW')/3 a scalar.
A17, B17, lambda17 = sp.symbols("A17 B17 lambda17")
w17 = sp.symbols("u0:6")
P17 = X**3 + A17 * X + B17
W17 = sum(w17[i] * X**i for i in range(6))
order17_equation = sp.Poly(
    sp.expand(
        (
            sp.diff(P17, X) * W17
            - 3 * P17 * sp.diff(W17, X)
        )
        / 3
        - lambda17
    ),
    X,
)
coeff17 = order17_equation.all_coeffs()
assert coeff17[0] == -4 * w17[5]
assert coeff17[1] == -3 * w17[4]
# After the forced high coefficients vanish, the only possible branch is
# W=u1*X, A*u1=0, lambda=-B*u1.
reduced17 = [
    sp.expand(eq.subs({w17[5]: 0, w17[4]: 0, w17[3]: 0, w17[2]: 0}))
    for eq in coeff17
]
assert set(reduced17) == {
    sp.Integer(0),
    w17[0],
    -sp.Rational(2, 3) * A17 * w17[1],
    A17 * w17[0] / 3 - B17 * w17[1] - lambda17,
}


# C != 0, order 16: the preceding jets force the displayed exact
# first-order factor with Y=2*C*B10+d*Q7.
d = sp.symbols("d")
B10 = sp.Function("B10")(X)
Q7 = sp.Function("Q7")(X)
Y16 = 2 * C * B10 + d * Q7
W16 = P * d * Q7
J16 = (
    -sp.Rational(2, 3)
    * C
    * P
    * (B10 * sp.diff(P, X) + 3 * P * sp.diff(B10, X))
    - P * sp.diff(W16, X)
    + sp.Rational(2, 3) * sp.diff(P, X) * W16
)
expected16 = -P * (
    3 * P * sp.diff(Y16, X) + sp.diff(P, X) * Y16
) / 3
assert sp.simplify(J16 - expected16) == 0


# C != 0, order 19: after W=P*V+D and
# P'*D+3*lambda=P*M, identity (25) is exact.
V = sp.Function("V")(X)
D0 = sp.Function("D0")(X)
Q7_delay = sp.Function("Q7_delay")(X)
c_background = sp.symbols("c_background")
D = D0 - sp.Rational(2, 3) * c_background * C * Q7_delay
B13 = sp.Function("B13")(X)
M = sp.Function("M")(X)
lambda19 = sp.symbols("lambda19")
Z = 2 * C * B13 + V
W19 = P * V + D0
J19 = (
    -sp.Rational(2, 3)
    * C
    * P
    * (4 * B13 * sp.diff(P, X) + 3 * P * sp.diff(B13, X))
    - P * sp.diff(W19, X)
    - sp.Rational(1, 3) * sp.diff(P, X) * W19
    + sp.Rational(2, 9)
    * c_background
    * C
    * (
        Q7_delay * sp.diff(P, X)
        + 3 * P * sp.diff(Q7_delay, X)
    )
)
expected19_all_jets = -P * (
    3 * P * sp.diff(Z, X)
    + 4 * sp.diff(P, X) * Z
    + 3 * sp.diff(D, X)
    + M
) / 3
relation19 = sp.diff(P, X) * D + 3 * lambda19 - P * M
assert sp.simplify(
    (J19 - lambda19) - expected19_all_jets + relation19 / 3
) == 0


# A deterministic full expansion checks every term in the all-jet
# formula, including the delayed order-19 background interaction.
z = sp.symbols("z")
P_test = X**3 + 2 * X + 1
c_test = sp.Integer(2)
j_test = -sp.Rational(1, 3)
k_test = sp.Rational(3, 2)
C_test = 2 * c_test + 3 * j_test
S_test = {
    r: sum(sp.Integer((r + 2 * i) % 7 - 3) * X**i for i in range(6))
    for r in range(7, 14)
}
Q_test = {r: sp.div(S_test[r], P_test, X)[0] for r in S_test}
B_test = {r: sp.rem(S_test[r], P_test, X) for r in S_test}
G_test = (
    P_test**3
    + c_test * z**6 * P_test
    + sum(z**r * S_test[r] for r in S_test)
)
F_test = (
    P_test**4
    + (sp.Rational(4, 3) * c_test + j_test) * z**6 * P_test**2
    + k_test * z**9 * P_test
    + sp.Rational(4, 3)
    * P_test
    * sum(z**r * S_test[r] for r in S_test)
    + (sp.Rational(4, 9) * c_test + sp.Rational(2, 3) * j_test)
    * sum(z ** (r + 6) * Q_test[r] for r in S_test)
)
R_test = {}
for total_order in range(14, 20):
    convolution = sum(
        (
            S_test.get(i, 0) * S_test.get(total_order - i, 0)
            for i in range(7, total_order - 6)
        ),
        sp.Integer(0),
    )
    quotient, remainder = sp.div(convolution, P_test**2, X)
    R_test[total_order] = remainder
    F_test += sp.Rational(2, 9) * z**total_order * quotient

full_bracket_test = sp.expand(
    z
    * (
        sp.diff(F_test, z) * sp.diff(G_test, X)
        - sp.diff(F_test, X) * sp.diff(G_test, z)
    )
    - 12 * F_test * sp.diff(G_test, X)
    + 9 * sp.diff(F_test, X) * G_test
)
for total_order in range(13, 20):
    W_test = (
        2 * R_test.get(total_order, 0)
        + 3 * k_test * S_test.get(total_order - 9, 0)
    )
    predicted = (
        -sp.Rational(2, 3)
        * C_test
        * P_test
        * (
            (total_order - 15)
            * B_test.get(total_order - 6, 0)
            * sp.diff(P_test, X)
            + 3
            * P_test
            * sp.diff(B_test.get(total_order - 6, 0), X)
        )
        - P_test * sp.diff(W_test, X)
        + sp.Rational(18 - total_order, 3)
        * sp.diff(P_test, X)
        * W_test
    )
    if total_order == 19:
        predicted += (
            sp.Rational(2, 9)
            * c_test
            * C_test
            * (
                Q_test[7] * sp.diff(P_test, X)
                + 3 * P_test * sp.diff(Q_test[7], X)
            )
        )
    assert sp.expand(full_bracket_test).coeff(z, total_order) == sp.expand(
        predicted
    )


print("verified hostile audit of local normal-degree (12,9) calculation")
