#!/usr/bin/env python3
"""Verify the compactified conductor endpoint and its log-symplectic model."""

import sympy as sp


tau, r, u, eta, zeta = sp.symbols(
    "tau r u eta zeta", nonzero=True
)

# First blowup of the endpoint (t,c)=(infinity,0):
#
#   t=1/tau, c=r*tau.
t = 1 / tau
c = r * tau
a = sp.factor(t + t**2 - c * t**3)
b = sp.factor(2 + 4 * t - 3 * c * t**2)
assert sp.factor(a - ((1 - r) / tau**2 + 1 / tau)) == 0
assert sp.factor(b - ((4 - 3 * r) / tau + 2)) == 0

# Coefficients of dt^dc and t*dc in the coordinate basis.
omega_tau_r = sp.factor(
    sp.diff(t, tau) * sp.diff(c, r)
    - sp.diff(t, r) * sp.diff(c, tau)
)
assert omega_tau_r == -1 / tau
liouville_tau = sp.factor(t * sp.diff(c, tau))
liouville_r = sp.factor(t * sp.diff(c, r))
assert liouville_tau == r / tau
assert liouville_r == 1

# The conductor equation after removing the exceptional factor tau^2.
D = 9 * c**2 * t**2 - 12 * c * t - 9 * c + 4
D_strict = sp.factor(D)
assert sp.expand(D_strict - ((3 * r - 2) ** 2 - 9 * r * tau)) == 0

# Its normalization at this endpoint is
#
#   r=(v+2)/3, tau=v^2/(3(v+2)).
v = sp.symbols("v", nonzero=True)
r_v = (v + 2) / 3
tau_v = v**2 / (3 * (v + 2))
assert sp.factor(D_strict.subs({r: r_v, tau: tau_v})) == 0
assert sp.limit(r_v, v, 0) == sp.Rational(2, 3)
assert sp.limit(tau_v / v**2, v, 0) == sp.Rational(1, 6)

# Two further point blowups separate the conductor, the first exceptional
# divisor, and the new exceptional divisor.  Put r=2/3+u, tau=u*eta,
# then eta=u*zeta.  The final strict conductor meets u=0 at zeta=3/2,
# away from the strict old exceptional divisor zeta=0.
D_second = sp.factor(
    D_strict.subs({r: sp.Rational(2, 3) + u, tau: u * eta}) / u
)
assert sp.expand(D_second - (9 * u - (6 + 9 * u) * eta)) == 0
D_third = sp.factor(D_second.subs(eta, u * zeta) / u)
assert sp.expand(D_third - (9 - (6 + 9 * u) * zeta)) == 0
assert sp.solve(D_third.subs(u, 0), zeta) == [sp.Rational(3, 2)]

# The divisor data alone is unobstructed.  For every nonzero integer m,
#
#   U=tau^m, V=-r/(m*tau^m)
#
# is a rational Darboux pair for the log-symplectic form and its Liouville
# difference from t*dc is rationally exact.
m = sp.symbols("m", nonzero=True)
U = tau**m
V = -r / (m * tau**m)
jac = sp.factor(
    sp.diff(U, tau) * sp.diff(V, r)
    - sp.diff(U, r) * sp.diff(V, tau)
)
assert jac == -1 / tau
beta_tau = sp.factor(U * sp.diff(V, tau) - liouville_tau)
beta_r = sp.factor(U * sp.diff(V, r) - liouville_r)
primitive = -(1 + 1 / m) * r
assert sp.factor(beta_tau - sp.diff(primitive, tau)) == 0
assert sp.factor(beta_r - sp.diff(primitive, r)) == 0

print("verified the cuspidal endpoint blowups and log-symplectic divisor")
print("verified a rational exact local chart with the same divisor data")
print("RESULT: COMPACTIFICATION DIVISORS ALONE DO NOT OBSTRUCT THE PAIR")
