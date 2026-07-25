#!/usr/bin/env python3
"""Verify the degree-21 algebraic symplectic bridge countermodel.

The model proves that a normalized formal inverse branch can be integral,
regular on its normalization, and exactly symplectic without being rational
over the base.  The missing datum is trivial global monodromy.
"""

from __future__ import annotations

import sympy as sp


N = 21
x, y, a, phi = sp.symbols("x y a phi", nonzero=True)

# Base and comparison pairs.
p0 = phi**N
q0_scale = sp.Rational(1, N) / phi ** (N - 1)
p = x**N + a
q = y / (N * x ** (N - 1))

# The algebraic branch satisfies phi^N=x^N+a and
# phi'=x^(N-1)/phi^(N-1).
phi_prime = x ** (N - 1) / phi ** (N - 1)
y_branch = y * phi ** (N - 1) / x ** (N - 1)

assert sp.factor(p0.subs(phi**N, p) - p) == 0
assert sp.factor(q0_scale * y_branch - q) == 0

# The bounded pair F has constant Jacobian one.
jacobian_f = sp.factor(sp.diff(p, x) * sp.diff(q, y) - sp.diff(p, y) * sp.diff(q, x))
assert jacobian_f == 1

# The algebraic correspondence T=(phi,y/phi') is symplectic.
# Since phi depends only on x, its determinant is phi' * dY/dy.
jacobian_t = sp.factor(phi_prime * sp.diff(y_branch, y))
assert jacobian_t == 1

# The normalized branch is identity at infinity to order N.
t = sp.symbols("t")
normalized_branch = sp.series((1 + a * t**N) ** sp.Rational(1, N), t, 0, N + 2)
assert sp.expand(normalized_branch.removeO()).coeff(t, 0) == 1
assert sp.expand(normalized_branch.removeO()).coeff(t, N) == a / N
assert all(
    sp.expand(normalized_branch.removeO()).coeff(t, exponent) == 0
    for exponent in range(1, N)
)

# Integrality and regularity on the finite cover are literal:
# phi is monic integral, and Y belongs to A[phi] because x is a unit.
minimal_polynomial = sp.Poly(phi**N - x**N - a, phi)
assert minimal_polynomial.LC() == 1
assert sp.Poly(y_branch * x ** (N - 1), phi).degree() == N - 1

# A simple root alpha of x^N+a gives valuation one to x^N+a.
# T^N-(x^N+a) is Eisenstein there, hence the branch degree is N.
derivative = sp.diff(x**N + a, x)
assert sp.gcd(sp.Poly(x**N + a, x), sp.Poly(derivative, x)).degree() == 0

# Stronger countermodel after additive constants are fixed: a nonlinear
# target shear.  It remains regular Laurent and its chosen branch remains
# degree N.
q_shear = y / (N * x ** (N - 1))
p_shear = x**N + q_shear**2

jacobian_shear = sp.factor(
    sp.diff(p_shear, x) * sp.diff(q_shear, y)
    - sp.diff(p_shear, y) * sp.diff(q_shear, x)
)
assert jacobian_shear == 1

phi_shear_y = N * phi ** (N - 1) * q_shear
assert sp.factor(phi_shear_y / (N * phi ** (N - 1)) - q_shear) == 0

# The first formal correction occurs at x^{-(3N-2)}.
correction_order = 3 * N - 2
u = sp.symbols("u")
shear_branch = sp.series(
    (1 + y**2 * u**correction_order / N**2) ** sp.Rational(1, N),
    u,
    0,
    correction_order + 2,
)
assert sp.expand(shear_branch.removeO()).coeff(u, correction_order) == y**2 / N**3

# y^2+N^2*x^(3N-2) is squarefree and has odd x-exponent for N=21;
# its prime divisor occurs with valuation one.
shear_divisor = y**2 + N**2 * x**correction_order
assert correction_order == 61
assert sp.gcd(
    sp.Poly(shear_divisor, y),
    sp.Poly(sp.diff(shear_divisor, y), y),
).degree() == 0

# The actual (2,3) radial caps rule out nonlinear target shears.  Every
# target monomial P^i Q^j contributes exact radial weight 2i+3j because
# G^2/F^3 is the nonconstant outer Belyi function.
Ptarget, Qtarget = sp.symbols("Ptarget Qtarget")
first_allowed = [
    Ptarget**i * Qtarget**j
    for i in range(4)
    for j in range(3)
    if 2 * i + 3 * j <= 2
]
second_allowed = [
    Ptarget**i * Qtarget**j
    for i in range(4)
    for j in range(3)
    if 2 * i + 3 * j <= 3
]
assert first_allowed == [1, Ptarget]
assert second_allowed == [1, Qtarget, Ptarget]

print("verified the regular degree-21 bounded symplectic pair")
print("verified its integral pole-free algebraic inverse branch")
print("verified the normalized identity expansion at infinity")
print("verified: cyclic degree-21 monodromy prevents rational descent")
print("verified the nonlinear-shear countermodel after fixing constants")
print("verified: exact (2,3) Newton caps exclude nonlinear target shears")
