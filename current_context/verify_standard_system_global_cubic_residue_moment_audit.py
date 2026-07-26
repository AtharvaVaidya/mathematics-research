#!/usr/bin/env python3
"""Exact checks for the cubic lifted-endpoint residue and deck orbit."""

from __future__ import annotations

import sympy as sp


x, y = sp.symbols("x y")


def coeff(poly: sp.Expr, variable: sp.Symbol, exponent: int) -> sp.Expr:
    return sp.Poly(sp.expand(poly), variable).coeff_monomial(variable**exponent)


def bounded_solve(
    A: sp.Expr,
    B: sp.Expr,
    h: sp.Expr,
    p_degree: int,
    q_degree: int,
) -> tuple[sp.Expr, sp.Expr] | None:
    p_symbols = sp.symbols(f"p0:{p_degree + 1}")
    q_symbols = sp.symbols(f"q0:{q_degree + 1}")
    p = sum(p_symbols[i] * x**i for i in range(p_degree + 1))
    q = sum(q_symbols[i] * x**i for i in range(q_degree + 1))
    equation = sp.Poly(sp.expand(A * q - B * p - h), x)
    equations = [
        equation.coeff_monomial(x**i)
        for i in range(max(0, equation.degree()) + 1)
    ]
    solutions = sp.solve(equations, (*p_symbols, *q_symbols), dict=True)
    if not solutions:
        return None
    solution = solutions[0]
    return sp.expand(p.subs(solution)), sp.expand(q.subs(solution))


def cubic_source(
    p1: sp.Expr, q1: sp.Expr, p2: sp.Expr, q2: sp.Expr
) -> sp.Expr:
    return sp.expand(
        2 * sp.diff(p1, x) * q2
        - p1 * sp.diff(q2, x)
        + sp.diff(p2, x) * q1
        - 2 * p2 * sp.diff(q1, x)
    )


def modular_residue_moment(
    A: sp.Expr, B: sp.Expr, h: sp.Expr
) -> sp.Expr:
    beta = sp.degree(B, x)
    q_h = sp.rem(sp.expand(sp.invert(A, B) * h), B, domain=sp.QQ)
    return sp.factor(
        coeff(q_h, x, beta - 1) / sp.LC(sp.Poly(B, x))
    )


# The coefficient of y^(r-1) has the asserted recurrence.  A generic
# finite jet is enough to verify the r=1,2,3 formulas symbolically.
p_coefficients = [
    sum(sp.symbols(f"a{i}_0:{5 - i}")[j] * x**j for j in range(5 - i))
    for i in range(4)
]
q_coefficients = [
    sum(sp.symbols(f"b{i}_0:{6 - i}")[j] * x**j for j in range(6 - i))
    for i in range(4)
]
F = sum(p_coefficients[i] * y**i for i in range(4))
G = sum(q_coefficients[i] * y**i for i in range(4))
jacobian = sp.expand(sp.diff(F, x) * sp.diff(G, y) - sp.diff(F, y) * sp.diff(G, x))
A_generic = sp.diff(p_coefficients[0], x)
B_generic = sp.diff(q_coefficients[0], x)

assert sp.expand(
    coeff(jacobian, y, 0)
    - (A_generic * q_coefficients[1] - B_generic * p_coefficients[1])
) == 0
assert sp.expand(
    coeff(jacobian, y, 1)
    - (
        2 * (A_generic * q_coefficients[2] - B_generic * p_coefficients[2])
        + sp.diff(p_coefficients[1], x) * q_coefficients[1]
        - p_coefficients[1] * sp.diff(q_coefficients[1], x)
    )
) == 0
assert sp.expand(
    coeff(jacobian, y, 2)
    - (
        3 * (A_generic * q_coefficients[3] - B_generic * p_coefficients[3])
        + cubic_source(
            p_coefficients[1],
            q_coefficients[1],
            p_coefficients[2],
            q_coefficients[2],
        )
    )
) == 0


# A full-degree (n,m)=(3,4) endpoint with a nonzero cubic obstruction.
# B has rational simple roots, so the modular coefficient and residue
# evaluation formulas can be compared without numerical algebraic roots.
A = x**2 + 1
B = (x - 1) * (x - 2) * (x - 3)
p1 = x / 10
q1 = x**2 / 10 - 3 * x / 5 + 1
assert sp.expand(A * q1 - B * p1) == 1

H2 = sp.expand(sp.diff(p1, x) * q1 - p1 * sp.diff(q1, x))
second_lift = bounded_solve(A, B, -H2 / 2, 1, 2)
assert second_lift is not None
p2, q2 = second_lift
H3 = cubic_source(p1, q1, p2, q2)
h3 = sp.expand(-H3 / 3)

moment_from_remainder = modular_residue_moment(A, B, h3)
moment_from_roots = sp.factor(
    sum(
        h3.subs(x, root)
        / (A.subs(x, root) * sp.diff(B, x).subs(x, root))
        for root in (1, 2, 3)
    )
)
assert moment_from_remainder == moment_from_roots
assert moment_from_remainder == sp.Rational(343, 600000)
assert bounded_solve(A, B, h3, 0, 1) is None


# A nonmonic, nonsquarefree denominator checks the local-residue
# interpretation beyond the simple-root evaluation formula.
A_multiple = x**2 + 1
B_multiple = 5 * (x - 1) ** 2 * (x + 2)
h_multiple = 7 * x**3 - 3 * x + 11
moment_multiple = modular_residue_moment(
    A_multiple, B_multiple, h_multiple
)
residues_multiple = sp.factor(
    sp.residue(
        h_multiple / (A_multiple * B_multiple),
        x,
        1,
    )
    + sp.residue(
        h_multiple / (A_multiple * B_multiple),
        x,
        -2,
    )
)
assert moment_multiple == residues_multiple == -sp.Rational(6, 25)


# The cubic moment is not universally nonzero.  This second full-degree
# endpoint passes order three exactly.
A_zero = x**2 + 1
B_zero = x**3 + x + 1
p1_zero = -1
q1_zero = -x
assert sp.expand(A_zero * q1_zero - B_zero * p1_zero) == 1
H2_zero = sp.expand(
    sp.diff(p1_zero, x) * q1_zero
    - p1_zero * sp.diff(q1_zero, x)
)
p2_zero, q2_zero = bounded_solve(
    A_zero, B_zero, -H2_zero / 2, 1, 2
)
H3_zero = cubic_source(p1_zero, q1_zero, p2_zero, q2_zero)
h3_zero = sp.expand(-H3_zero / 3)
assert modular_residue_moment(A_zero, B_zero, h3_zero) == 0
third_lift_zero = bounded_solve(A_zero, B_zero, h3_zero, 0, 1)
assert third_lift_zero == (sp.Rational(-1, 2), -x / 2)


# Scaling law.  Recompute the transformed one- and two-jets, derive
# the transformed cubic source from them, and compare its residue
# moment with mu^3/lambda^2 times the original.
lambda_scale = sp.Rational(2)
mu_scale = sp.Rational(3)
u_scale = sp.Rational(5)
v_scale = sp.Rational(7)

A_scaled = sp.expand(u_scale * lambda_scale * A.subs(x, lambda_scale * x))
B_scaled = sp.expand(v_scale * lambda_scale * B.subs(x, lambda_scale * x))
p1_scaled = sp.expand(
    u_scale * mu_scale * p1.subs(x, lambda_scale * x)
)
q1_scaled = sp.expand(
    v_scale * mu_scale * q1.subs(x, lambda_scale * x)
)
p2_scaled = sp.expand(
    u_scale * mu_scale**2 * p2.subs(x, lambda_scale * x)
)
q2_scaled = sp.expand(
    v_scale * mu_scale**2 * q2.subs(x, lambda_scale * x)
)
h3_scaled_from_jet = sp.expand(
    -cubic_source(
        p1_scaled,
        q1_scaled,
        p2_scaled,
        q2_scaled,
    )
    / 3
)
h3_scaled = sp.expand(
    u_scale
    * v_scale
    * lambda_scale
    * mu_scale**3
    * h3.subs(x, lambda_scale * x)
)
assert sp.expand(h3_scaled_from_jet - h3_scaled) == 0
scaled_moment = modular_residue_moment(A_scaled, B_scaled, h3_scaled)
assert sp.factor(
    scaled_moment
    - mu_scale**3 / lambda_scale**2 * moment_from_remainder
) == 0


# The exact Rees survivor has the claimed drifted scalar but is not a
# principal Bezout endpoint.
t, z = sp.symbols("t z")
p_local = z**2 + 2 * t
q_local = z**3 + 3 * t * z
rees_operator = sp.expand(
    t
    * (
        sp.diff(p_local, z) * sp.diff(q_local, t)
        - sp.diff(p_local, t) * sp.diff(q_local, z)
    )
    + 2 * p_local * sp.diff(q_local, z)
    - 3 * q_local * sp.diff(p_local, z)
)
ordinary_jacobian = sp.expand(
    sp.diff(p_local, z) * sp.diff(q_local, t)
    - sp.diff(p_local, t) * sp.diff(q_local, z)
)
assert rees_operator == 6 * t**2
assert ordinary_jacobian == -6 * t
assert sp.gcd(2 * z, 3 * z**2) == z
assert sp.expand((2 * z) * (3 * z) - (3 * z**2) * 2) == 0


# Deck arithmetic for (h,d)=(4,5).  The fixed-root character is
# nontrivial; the four-root trace vanishes and its norm is -Lambda^4.
omega = sp.I
deck_ratio = sp.simplify(omega ** (-(2 * 5 + 3)))
assert deck_ratio == -sp.I
Lambda = sp.symbols("Lambda")
orbit = [sp.expand(deck_ratio**j * Lambda) for j in range(4)]
assert sp.simplify(sum(orbit)) == 0
assert sp.simplify(sp.prod(orbit)) == -Lambda**4
assert (2 * 5 + 3) % 4 == 1
assert 5 % 4 == 1

c, K = sp.symbols("c K", nonzero=True)
beta = sp.symbols("beta", nonzero=True)
assert sp.simplify(
    sp.prod(K * omega ** (-j) * beta for j in range(4))
    .subs(beta**4, -c)
) == K**4 * c


print("verified: order-three source and codimension-one modular test")
print("verified: cubic obstruction equals the residue/leading-coefficient moment")
print("verified: the cubic moment can vanish or be nonzero on full-degree endpoints")
print("verified: deck scaling has character omega^(-(2d+3))")
print("verified: the (9,7,4,5,1,2,3) orbit has zero trace and unconstrained norm")
print("verified: the known local Rees survivor is pre-principal")
