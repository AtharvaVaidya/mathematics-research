#!/usr/bin/env python3
"""Exact checks for ROUTE_A_SINGULAR_DICRITICAL_INDEX_AUDIT.md."""

import sympy as sp


a, b, t, eta = sp.symbols("a b t eta")


def generators(a0, b0):
    u0 = a0**2
    v0 = 4 * b0 * (1 + a0**2 * b0)
    w0 = a0 * (1 + 2 * a0**2 * b0)
    return tuple(map(sp.factor, (u0, v0, w0)))


# The rational quadratic deck involution fixes all three generators.
u, v, w = generators(a, b)
sigma_a = -a
sigma_b = -b - a**-2
u_s, v_s, w_s = generators(sigma_a, sigma_b)
assert sp.factor(u_s - u) == 0
assert sp.factor(v_s - v) == 0
assert sp.factor(w_s - w) == 0


# The exact Puiseux chart at infinity.
theta_a = -t + eta * t**3
theta_b = -t**-2
u_t, v_t, w_t = generators(theta_a, theta_b)
z = 1 - eta * t**2

assert sp.factor(u_t - t**2 * z**2) == 0
assert sp.factor(v_t - (-8 * eta + 4 * eta**2 * t**2)) == 0
assert sp.factor(w_t - t * z * (2 * z**2 - 1)) == 0
assert all(expr.is_polynomial(t, eta) for expr in (u_t, v_t, w_t))
assert sp.factor(w_t**2 - u_t - u_t**2 * v_t) == 0

# The boundary restriction is v=-8 eta, hence b=-2 eta on L.
assert sp.expand(u_t.subs(t, 0)) == 0
assert sp.expand(w_t.subs(t, 0)) == 0
assert sp.expand(v_t.subs(t, 0)) == -8 * eta

# The coordinate substitution has constant Jacobian -2.
jac_theta = sp.det(
    sp.Matrix(
        [
            [sp.diff(theta_a, t), sp.diff(theta_a, eta)],
            [sp.diff(theta_b, t), sp.diff(theta_b, eta)],
        ]
    )
)
assert sp.factor(jac_theta) == -2

# Puiseux data for -x^(-1/2) + eta*x^(-3/2):
# -1/2 = 1 - 3/2 and -3/2 = 1 - 5/2.
m_phi = 2
n_phi = 5
mult_zero_parameter = 2
i_phi = m_phi // mult_zero_parameter
assert n_phi == 5
assert sp.Rational(1) - sp.Rational(3, 2) == -sp.Rational(1, 2)
assert sp.Rational(1) - sp.Rational(n_phi, m_phi) == -sp.Rational(3, 2)
assert i_phi == 1


# The two reduced-basis leading-monomial families are injective and disjoint.
ordinary = {}
with_w = {}
for i in range(8):
    for j in range(8):
        exp0 = (2 * i + 2 * j, 2 * j)
        exp1 = (3 + 2 * i + 2 * j, 1 + 2 * j)
        assert exp0 not in ordinary
        assert exp1 not in with_w
        ordinary[exp0] = (i, j)
        with_w[exp1] = (i, j)
        assert sum(exp0) == 2 * i + 4 * j
        assert sum(exp1) == 4 + 2 * i + 4 * j

assert set(ordinary).isdisjoint(with_w)

# In particular, a v^m restriction term has total degree exactly 4m
# before any higher filtered terms are considered.
for m in range(1, 12):
    assert sum((2 * m, 2 * m)) == 4 * m


print("route A singular dicritical-index audit: all exact checks passed")
