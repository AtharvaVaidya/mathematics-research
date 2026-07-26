#!/usr/bin/env python3
"""Exact checks for the repeated-root normal-form bridge countermodel."""

from __future__ import annotations

import sympy as sp


X, tau, x, y, z = sp.symbols("X tau x y z")
u, v, w = sp.symbols("u v w", nonzero=True)


def homogeneous_piece(poly: sp.Expr, total_degree: int) -> sp.Expr:
    """Extract one ordinary homogeneous piece in X,tau."""
    output = 0
    for powers, coefficient in sp.Poly(poly, X, tau).terms():
        if sum(powers) == total_degree:
            output += coefficient * X ** powers[0] * tau ** powers[1]
    return sp.expand(output)


def reciprocal_bracket(P: sp.Expr, Q: sp.Expr, g: int) -> sp.Expr:
    """The (2g,3g) homogenized Keller operator."""
    return sp.expand(
        tau * (sp.diff(P, X) * sp.diff(Q, tau) - sp.diff(P, tau) * sp.diff(Q, X))
        + 2 * g * P * sp.diff(Q, X)
        - 3 * g * Q * sp.diff(P, X)
    )


def root_order(poly: sp.Expr, root: sp.Expr) -> int:
    """Return the multiplicity of one exact polynomial root."""
    order = 0
    quotient = sp.Poly(poly, X)
    divisor = sp.Poly(X - root, X)
    while True:
        next_quotient, remainder = sp.div(quotient, divisor)
        if remainder.as_expr() != 0:
            return order
        order += 1
        quotient = next_quotient


for E in range(2, 6):
    r = E + 1
    g = 2 * r
    roots = tuple(range(1, r + 1))
    R = sp.prod((X - alpha) ** 2 for alpha in roots)
    L0 = sp.prod(X - alpha for alpha in roots)
    H = X - (r + 1)
    L = sp.expand(L0 * H)
    D = sp.expand(R + tau**E * L)

    assert sp.degree(R, X) == g
    assert sp.degree(L, X) == g - E
    for alpha in roots:
        assert root_order(R, alpha) == 2
        assert root_order(L, alpha) == 1
    assert g - 2 * E == 2
    assert E < sp.Rational(g, 2)

    P = sp.expand(D**2 + tau ** (2 * g - 1) * (u * X + v))
    Q = sp.expand(D**3 + w * tau ** (3 * g - 1))

    # Every coefficient obeys deg_X coefficient <= normal_degree-order.
    for power, coefficient in sp.Poly(P, tau).terms():
        order = power[0]
        assert sp.degree(coefficient, X) <= 2 * g - order
    for power, coefficient in sp.Poly(Q, tau).terms():
        order = power[0]
        assert sp.degree(coefficient, X) <= 3 * g - order

    d_E = x**g + x ** (g - E)
    P_top = homogeneous_piece(P, 2 * g)
    Q_top = homogeneous_piece(Q, 3 * g)
    assert sp.expand(P_top.subs({X: x, tau: 1}) - (d_E**2 + u * x)) == 0
    assert sp.expand(Q_top.subs({X: x, tau: 1}) - d_E**3) == 0

    # Cross terms cannot reach the terminal order; direct extraction
    # checks the exact endpoint scalar for several arbitrary E.
    bracket = reciprocal_bracket(P, Q, g)
    terminal = sp.Poly(bracket, tau).coeff_monomial(tau ** (5 * g - 2))
    assert sp.expand(terminal + u * w) == 0

    # The common-root partitions distinguish E>=2 from E=1.
    partition_E = sorted(
        (
            multiplicity
            for factor, multiplicity in sp.sqf_list(d_E, x)[1]
            for _ in range(sp.degree(factor, x))
        ),
        reverse=True,
    )
    d_one = x ** (g - 1) * (x + 1)
    partition_one = sorted(
        (
            multiplicity
            for factor, multiplicity in sp.sqf_list(d_one, x)[1]
            for _ in range(sp.degree(factor, x))
        ),
        reverse=True,
    )
    assert partition_E == [g - E, *([1] * E)]
    assert partition_one == [g - 1, 1]
    assert partition_E != partition_one


# The derivative and Bezout identities hold for an arbitrary common root.
c0, c1, c2, c3 = sp.symbols("c0 c1 c2 c3")
d = x**4 + c3 * x**3 + c2 * x**2 + c1 * x + c0
d_prime = sp.diff(d, x)
p0 = d**2 + u * x
q0 = d**3
A = sp.diff(p0, x)
B = sp.diff(q0, x)
p1 = -4 * d_prime / (3 * u**2)
q1 = 1 / u - 2 * d * d_prime / u**2
assert sp.factor(A * q1 - B * p1 - 1) == 0
assert sp.degree(p1, x) <= 7
assert sp.degree(q1, x) <= 11

# An independent gcd check on several exact common roots.
for exact_d in (
    x**5 + x**3 + 2,
    x**6 + 2 * x**4 - x + 1,
    x**7 - 3 * x**2 + 4,
):
    exact_A = sp.diff(exact_d**2 + 5 * x, x)
    exact_B = sp.diff(exact_d**3, x)
    assert sp.gcd(exact_A, exact_B) == 1


# Verify the formal lift through a nontrivial finite jet.  Keep the
# universal Catalan identity separate from the (larger) arbitrary-d
# expression so polynomial expansion remains fast.
W = sp.factor(sp.diff(p1, x) * q1 - p1 * sp.diff(q1, x))
base_F = p0 + p1 * z
base_G = q0 + q1 * z
base_jacobian = (
    sp.diff(base_F, x) * sp.diff(base_G, z)
    - sp.diff(base_F, z) * sp.diff(base_G, x)
)
assert sp.factor(base_jacobian - (1 + W * z)) == 0

W_scalar = sp.symbols("W")
phi = (
    y
    - W_scalar * y**2 / 2
    + W_scalar**2 * y**3 / 2
    - 5 * W_scalar**3 * y**4 / 8
    + 7 * W_scalar**4 * y**5 / 8
)
formal_equation = sp.expand(phi + W_scalar * phi**2 / 2 - y)
assert all(
    sp.expand(formal_equation).coeff(y, degree) == 0
    for degree in range(1, 6)
)
chain_factor = sp.expand((1 + W_scalar * phi) * sp.diff(phi, y) - 1)
assert all(
    sp.expand(chain_factor).coeff(y, degree) == 0
    for degree in range(0, 5)
)

# Verify the arbitrary-d root evaluation in differential symbols, rather
# than only through concrete polynomial specializations below.  Here
# Djet,d1jet,d2jet,d3jet,rjet,r1jet stand for d,d',d'',d''',r,r'.
Djet, d1jet, d2jet, d3jet, rjet, r1jet = sp.symbols(
    "Djet d1jet d2jet d3jet rjet r1jet",
    nonzero=True,
)


def differential_jet(value: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(value, Djet) * d1jet
        + sp.diff(value, d1jet) * d2jet
        + sp.diff(value, d2jet) * d3jet
        + sp.diff(value, rjet) * r1jet
    )


p1_jet = -4 * d1jet / (3 * u**2)
q1_jet = 1 / u - 2 * Djet * d1jet / u**2
p2_jet = sp.Rational(8, 9) / u**5 * (
    (d1jet**3 - rjet) / Djet
    - d1jet * d2jet
    - 2 * d1jet * rjet / u
)
q2_jet = (
    2 * d2jet / (3 * u**4)
    + 4 * d1jet**3 / (3 * u**5)
    - 4 * Djet * d1jet * d2jet / (3 * u**5)
    - 8 * Djet * d1jet * rjet / (3 * u**6)
)
h3_jet = -sp.Rational(1, 3) * (
    2 * differential_jet(p1_jet) * q2_jet
    - p1_jet * differential_jet(q2_jet)
    + differential_jet(p2_jet) * q1_jet
    - 2 * p2_jet * differential_jet(q1_jet)
)
psi_jet = (
    u**5
    - 6 * u**3 * Djet**3 * d2jet
    + 2 * u**2 * Djet**3 * rjet
    + 12 * u * Djet**6 * d2jet**2
    + 4 * u * Djet**5 * r1jet
    + 24 * Djet**6 * rjet * d2jet
)
assert sp.factor(
    h3_jet.subs(d1jet, -u / (2 * Djet))
    - 2 * psi_jet / (27 * u**7 * Djet**6)
) == 0


def arbitrary_d_first_obstruction(d_value: sp.Expr, u_value: sp.Expr) -> sp.Expr:
    """Compute the universal modular defect-three scalar."""
    u_value = sp.sympify(u_value)
    g_value = sp.degree(d_value, x)
    d1 = sp.diff(d_value, x)
    d2 = sp.diff(d1, x)
    remainder_d = sp.rem(d1**3, d_value, x, domain=sp.QQ)
    A_value = u_value + 2 * d_value * d1
    B_value = 3 * d_value**2 * d1
    p1_value = -4 * d1 / (3 * u_value**2)
    q1_value = 1 / u_value - 2 * d_value * d1 / u_value**2
    p2_value = sp.Rational(8, 9) / u_value**5 * (
        (d1**3 - remainder_d) / d_value
        - d1 * d2
        - 2 * d1 * remainder_d / u_value
    )
    q2_value = (
        2 * d2 / (3 * u_value**4)
        + 4 * d1**3 / (3 * u_value**5)
        - 4 * d_value * d1 * d2 / (3 * u_value**5)
        - 8 * d_value * d1 * remainder_d / (3 * u_value**6)
    )
    assert sp.cancel(A_value * q1_value - B_value * p1_value - 1) == 0
    H3_value = (
        2 * sp.diff(p1_value, x) * q2_value
        - p1_value * sp.diff(q2_value, x)
        + sp.diff(p2_value, x) * q1_value
        - 2 * p2_value * sp.diff(q1_value, x)
    )
    h3_value = sp.cancel(-H3_value / 3)
    inverse_A = sp.invert(A_value, B_value, domain=sp.QQ)
    modular_remainder = sp.rem(
        sp.cancel(inverse_A * h3_value),
        B_value,
        x,
        domain=sp.QQ,
    )
    return sp.factor(
        sp.Poly(modular_remainder, x).coeff_monomial(x ** (3 * g_value - 2))
    )


def quotient_trace(value: sp.Expr, modulus: sp.Expr) -> sp.Expr:
    """Trace of multiplication by value in QQ[x]/(modulus)."""
    dimension = sp.degree(modulus, x)
    diagonal = []
    for column in range(dimension):
        reduced = sp.rem(
            sp.expand(value * x**column),
            modulus,
            x,
            domain=sp.QQ,
        )
        diagonal.append(sp.Poly(reduced, x).coeff_monomial(x**column))
    return sp.factor(sum(diagonal))


def arbitrary_d_trace_obstruction(d_value: sp.Expr, u_value: int) -> sp.Expr:
    """Compute the exact trace form of the defect-three scalar."""
    u_value = sp.sympify(u_value)
    g_value = sp.degree(d_value, x)
    d1 = sp.diff(d_value, x)
    d2 = sp.diff(d1, x)
    remainder_d = sp.rem(d1**3, d_value, x, domain=sp.QQ)
    A_value = u_value + 2 * d_value * d1
    psi = (
        u_value**5
        - 6 * u_value**3 * d_value**3 * d2
        + 2 * u_value**2 * d_value**3 * remainder_d
        + 12 * u_value * d_value**6 * d2**2
        + 4 * u_value * d_value**5 * sp.diff(remainder_d, x)
        + 24 * d_value**6 * remainder_d * d2
    )
    denominator = d_value**5 * (u_value**2 + 4 * d_value**3 * d2)
    squarefree_gcd = sp.gcd(A_value, sp.diff(A_value, x))
    assert sp.degree(squarefree_gcd, x) == 0, (
        d_value,
        u_value,
        squarefree_gcd,
    )
    inverse_denominator = sp.invert(denominator, A_value, domain=sp.QQ)
    quotient_value = sp.rem(
        sp.expand(psi * inverse_denominator),
        A_value,
        x,
        domain=sp.QQ,
    )
    return sp.factor(
        sp.Rational(8 * g_value, 27 * u_value**8)
        * quotient_trace(quotient_value, A_value)
    )


# Independent exact checks of the arbitrary-d residue/trace theorem.
trace_examples = (
    (x**4 * (x + 1), 1),
    (x**4 + x + 1, 2),
    (x**5 + 2 * x**3 - x + 1, 3),
)
for trace_d, trace_u in trace_examples:
    modular_value = arbitrary_d_first_obstruction(trace_d, trace_u)
    trace_value = arbitrary_d_trace_obstruction(trace_d, trace_u)
    assert modular_value == trace_value, (trace_d, modular_value, trace_value)
assert arbitrary_d_first_obstruction(x**4 * (x + 1), 1) == -sp.Rational(
    8000, 9
)
assert arbitrary_d_first_obstruction(x**5, 1) == 0

# Exact regression for the arbitrary two-block remainder chamber.
ell_symbol = sp.symbols("ell", nonzero=True)
for g_value in range(5, 13):
    for E_value in range(1, g_value - 1):
        s_value = g_value - E_value
        quotient_value, j_value = divmod(2 * s_value - 3, E_value)
        two_block_d = x**s_value * (x**E_value + ell_symbol)
        actual_remainder = sp.rem(
            sp.diff(two_block_d, x) ** 3,
            two_block_d,
            x,
            domain=sp.QQ.frac_field(ell_symbol),
        )
        expected_remainder = (
            (-1) ** (quotient_value + 1)
            * E_value**3
            * ell_symbol ** (quotient_value + 3)
            * x ** (s_value + j_value)
        )
        assert sp.expand(actual_remainder - expected_remainder) == 0

print("verified: saturated strict repeated-root support families for E=2,...,5")
print("verified: affine endpoint scalar and generalized top forms")
print("verified: E>=2 root partitions are not the [g-1,1] partition")
print("verified: arbitrary-d Bezout jets and formal Keller lift")
print("verified: universal differential-symbol root evaluation for the residue formula")
print("verified: arbitrary-d modular obstruction equals its exact trace formula")
print("verified: arbitrary two-block remainder chamber formula")
