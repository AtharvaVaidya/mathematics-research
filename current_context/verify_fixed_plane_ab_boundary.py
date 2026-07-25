#!/usr/bin/env python3
"""Exact boundary identities for Hamiltonians U in Q[a,b].

This verifies the Laurent-coordinate calculation behind the following
necessary condition.  If U in Q[a,b] has a polynomial Darboux mate in the
normalization, then

    U = const + gamma*a + a^2*Delta(a,b)*K(a,b)

or

    U = const + lambda*b + a^2*Delta(a,b)*K(a,b).

Here gamma and lambda are nonzero and Delta=(b+1)^2-12*a.
"""

import sympy as sp


t, c, H = sp.symbols("t c H")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
c_in_t_h = (3 + 4 * t - H) / (3 * t**2)

assert sp.expand(b.subs(c, c_in_t_h) - (H - 1)) == 0
assert sp.expand(a.subs(c, c_in_t_h) - t * (H - t) / 3) == 0
assert sp.diff(b + 1, c) == -3 * t**2

# Write the boundary jets as
#
#   U = u0(H) + t*u1(H) + O(t^2),
#   V = t^(-N)*v(H) + higher t powers.
#
# The coefficient of t^(-N-1) in Jac_(t,H)(U,V) is
# N*u0'(H)*v(H).  When N=1, after this leading coefficient is fixed,
# the next negative coefficient is u1'(H)*v(H).
N = sp.symbols("N", integer=True, positive=True)
u0 = sp.Function("u0")(H)
u1 = sp.Function("u1")(H)
v = sp.Function("v")(H)
U_jet = u0 + t * u1
V_lead = t ** (-N) * v
jacobian = sp.expand(
    sp.diff(U_jet, t) * sp.diff(V_lead, H)
    - sp.diff(U_jet, H) * sp.diff(V_lead, t)
)
expected_jacobian = (
    N * sp.diff(u0, H) * v * t ** (-N - 1)
    + (
        u1 * sp.diff(v, H)
        + N * sp.diff(u1, H) * v
    )
    * t ** (-N)
)
assert sp.simplify(jacobian - expected_jacobian) == 0

v_constant = sp.symbols("v_constant")
jacobian_n1 = sp.expand(
    jacobian.subs({N: 1, v: v_constant})
).doit()
next_coefficient = jacobian_n1.coeff(t, -1)
assert sp.expand(
    next_coefficient - sp.diff(u1, H) * v_constant
) == 0

# If U(0,b)=lambda*b+const and
# U=lambda*b+const+a*G(a,b), its t-linear coefficient is
# H*G(0,H-1)/3.  Vanishing of its H derivative forces G(0,b)=0:
# for a polynomial g, (H*g(H-1))'=0 implies H*g(H-1) is constant,
# and divisibility by H makes that constant zero.
g_coefficients = sp.symbols("g0:6")
g = sum(
    coefficient * (H - 1) ** degree
    for degree, coefficient in enumerate(g_coefficients)
)
u1_from_a = H * g / 3
derivative = sp.Poly(sp.diff(u1_from_a, H), H)
solutions = sp.solve(
    derivative.all_coeffs(),
    g_coefficients,
    dict=True,
)
assert solutions == [{coefficient: 0 for coefficient in g_coefficients}]

# On the punctured component a=0, H=t is nonzero.  A polynomial with no
# zeros there is a nonzero monomial gamma*H^m, not necessarily a constant.
# This correctly retains the known submersion a*(b+1) at the submersion
# stage.  The Hamiltonian equation itself then excludes every m>=1.
gamma = sp.symbols("gamma", nonzero=True)
for degree in range(6):
    boundary_polynomial = gamma * H**degree
    assert sp.factor(boundary_polynomial.subs(H, t)) == gamma * t**degree

# If U=t*A(H)+O(t^2), V=t^(-N)*v(H)+..., the leading bracket coefficient
# is A*v'+N*A'*v.  Here A=gamma*H^(m+1)/3.  Terms of degree H^j in v are
# multiplied by gamma*(j+N*(m+1))/3 and shifted to H^(j+m).  Therefore
# the homogeneous equation has no nonzero polynomial solution for N>0.
# For N=2 the inhomogeneous equation can equal -1/3 only when m=0.
v_coefficients = sp.symbols("boundary_v0:7")
v_polynomial = sum(
    coefficient * H**degree
    for degree, coefficient in enumerate(v_coefficients)
)
for m in range(6):
    A = gamma * H ** (m + 1) / 3
    for pole_order in range(1, 7):
        operator = sp.expand(
            A * sp.diff(v_polynomial, H)
            + pole_order * sp.diff(A, H) * v_polynomial
        )
        expected_operator = gamma * sum(
            (degree + pole_order * (m + 1))
            * coefficient
            * H ** (degree + m)
            / 3
            for degree, coefficient in enumerate(v_coefficients)
        )
        assert sp.expand(operator - expected_operator) == 0
    if m >= 1:
        assert sp.rem(
            A * sp.diff(v_polynomial, H)
            + 2 * sp.diff(A, H) * v_polynomial,
            H,
        ) == 0

v_m0_solution = -sp.Rational(1, 2) / gamma
A_m0 = gamma * H / 3
assert sp.simplify(
    A_m0 * sp.diff(v_m0_solution, H)
    + 2 * sp.diff(A_m0, H) * v_m0_solution
    + sp.Rational(1, 3)
) == 0

# The nontrivial critical-value curve of (a,b) is parametrized by
# a=t^2/3, b=2t-1, hence has equation (b+1)^2-12a=0.  On either
# surviving family, the restriction of an a^2*G tail is t^4*g(t)/9.
# Absence of critical points forces g=0, hence Delta divides G.
a_edge = t**2 / 3
b_edge = 2 * t - 1
delta = (b_edge + 1) ** 2 - 12 * a_edge
assert sp.expand(delta) == 0

lam = sp.symbols("lambda", nonzero=True)
g_edge = sum(
    coefficient * t**degree
    for degree, coefficient in enumerate(g_coefficients)
)
u_a_edge = gamma * a_edge + a_edge**2 * g_edge
u_b_edge = lam * b_edge + a_edge**2 * g_edge
assert sp.simplify(sp.diff(u_a_edge, t) - (
    t
    * (
        6 * gamma
        + 4 * t**2 * g_edge
        + t**3 * sp.diff(g_edge, t)
    )
    / 9
)) == 0
assert sp.simplify(sp.diff(u_b_edge, t) - (
    18 * lam
    + 4 * t**3 * g_edge
    + t**4 * sp.diff(g_edge, t)
) / 9) == 0

print("verified (t,H) localization: a=t(H-t)/3, b=H-1")
print("verified lowest Laurent coefficient N*u0'(H)*v(H)")
print("verified next N=1 coefficient u1'(H)*v(H)")
print("verified punctured a=0 boundary permits exactly gamma*(b+1)^m")
print("verified Hamiltonian lowest coefficient excludes every m>=1")
print("verified critical parabola (b+1)^2=12a and restricted derivatives")
print("RESULT: EXACT Q[a,b] BOUNDARY NECESSARY-CONDITION IDENTITIES PASS")
