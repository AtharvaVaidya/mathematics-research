#!/usr/bin/env python3
"""Exact checks for FACTORIZATION_PLANE_NO_GO.md."""

import sympy as sp


p, q, r, s, t = sp.symbols("p q r s t")
u = sp.symbols("u0:4")
v = sp.symbols("v0:4")

A = p * r
B = p * s + q * r
C = p * t + q * s
D = q * t
resultant = p**2 * t - p * q * s + q**2 * r

M = sp.Matrix(
    [
        [q**2, -p * q, p**2],
        [u[0] * p + u[1] * q, u[1] * p + u[2] * q, u[2] * p + u[3] * q],
        [v[0] * p + v[1] * q, v[1] * p + v[2] * q, v[2] * p + v[3] * q],
    ]
)

plucker = {
    (i, j): sp.expand(u[i] * v[j] - u[j] * v[i])
    for i in range(4)
    for j in range(i + 1, 4)
}
expected_delta = (
    plucker[0, 1] * p**4
    + 2 * plucker[0, 2] * p**3 * q
    + (plucker[0, 3] + 3 * plucker[1, 2]) * p**2 * q**2
    + 2 * plucker[1, 3] * p * q**3
    + plucker[2, 3] * q**4
)
assert sp.expand(M.det() - expected_delta) == 0
print("verified: binary-quartic projection determinant")

plucker_relation = (
    plucker[0, 1] * plucker[2, 3]
    - plucker[0, 2] * plucker[1, 3]
    + plucker[0, 3] * plucker[1, 2]
)
assert sp.expand(plucker_relation) == 0
print("verified: Plucker relation")

rho, sigma = sp.symbols("rho sigma", nonzero=True)
r_nonzero = rho / p
s_nonzero = (sigma * p - q * rho) / p**2
t_nonzero = sp.solve(
    sp.Eq(resultant.subs({r: r_nonzero, s: s_nonzero}), 1), t
)[0]
assert sp.factor(A.subs(r, r_nonzero) - rho) == 0
assert sp.factor(B.subs({r: r_nonzero, s: s_nonzero}) - sigma) == 0
assert sp.factor(
    resultant.subs({r: r_nonzero, s: s_nonzero, t: t_nonzero}) - 1
) == 0
print("verified: rho-nonzero Laurent parametrization")

# rho=0, sigma nonzero: flat p=0 component.
flat = {p: 0, q: 1 / sigma, r: sigma**2}
assert sp.factor(A.subs(flat)) == 0
assert sp.factor(B.subs(flat) - sigma) == 0
assert sp.factor(resultant.subs(flat) - 1) == 0
assert sp.factor(C.subs(flat) - s / sigma) == 0
assert sp.factor(D.subs(flat) - t / sigma) == 0

laurent = {r: 0, s: sigma / p, t: (1 + q * sigma) / p**2}
assert sp.factor(A.subs(laurent)) == 0
assert sp.factor(B.subs(laurent) - sigma) == 0
assert sp.factor(resultant.subs(laurent) - 1) == 0
print("verified: exceptional flat and Laurent components")

zero_level = {r: 0, s: 0, t: p**-2}
assert sp.factor(A.subs(zero_level)) == 0
assert sp.factor(B.subs(zero_level)) == 0
assert sp.factor(resultant.subs(zero_level) - 1) == 0
print("verified: zero-level Laurent component")

print("all factorization-plane checks passed")
