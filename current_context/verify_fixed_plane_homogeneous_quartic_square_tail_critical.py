#!/usr/bin/env python3
"""Exclude K=M_2(a,H)^2+k0, including an arbitrary constant lower term."""

import sympy as sp


A, H = sp.symbols("A H")
r, s, q, k0, inverse = sp.symbols("r s q k0 inverse")
delta = H**2 - 12 * A
M = r * A**2 + s * A * H + q * H**2
K = M**2 + k0


def positive_coefficients_are_not_all_zero(residual, unit_parameter):
    equations = [
        coefficient
        for (exponent,), coefficient in sp.Poly(residual, A).terms()
        if exponent > 0
    ]
    basis = sp.groebner(
        equations + [inverse * unit_parameter - 1],
        inverse,
        r,
        s,
        q,
        k0,
        order="grevlex",
    )
    return list(basis) == [1]

# Main chart q!=0.
for base, name, a_power, scalar, q_power, residual_constant in (
    (A, "a", 12, -64, 6, -729 * q**6),
    (H, "b", 5, -32, 6, -q**4),
):
    F = sp.expand(base + A**2 * delta * K)
    F_A = sp.diff(F, A)
    F_H = sp.diff(F, H)
    assert sp.factor(sp.Poly(F_A, H).LC()) == 2 * A * q**2
    assert sp.factor(sp.Poly(F_H, H).LC()) == 6 * A**2 * q**2
    resultant = sp.factor(sp.resultant(F_A, F_H, H))
    residual = sp.cancel(
        resultant / (scalar * A**a_power * q**q_power)
    )
    residual_poly = sp.Poly(residual, A)
    assert sp.factor(residual_poly.coeff_monomial(1)) == residual_constant
    assert positive_coefficients_are_not_all_zero(residual, q)
    print(f"verified homogeneous quartic {name}-branch on q!=0")

# Boundary chart q=0, s!=0.
K_q0 = (r * A**2 + s * A * H) ** 2 + k0
for base, name, a_power, scalar, residual_constant in (
    (A, "a", 16, -128, -2 * s**4),
    (H, "b", 9, -64, -s**2),
):
    F = sp.expand(base + A**2 * delta * K_q0)
    F_A = sp.diff(F, A)
    F_H = sp.diff(F, H)
    assert sp.factor(sp.Poly(F_A, H).LC()) == 4 * A**3 * s**2
    assert sp.factor(sp.Poly(F_H, H).LC()) == 4 * A**4 * s**2
    resultant = sp.factor(sp.resultant(F_A, F_H, H))
    residual = sp.cancel(resultant / (scalar * A**a_power * s**4))
    residual_poly = sp.Poly(residual, A)
    assert sp.factor(residual_poly.coeff_monomial(1)) == residual_constant
    assert positive_coefficients_are_not_all_zero(residual, s)
    print(f"verified homogeneous quartic {name}-branch on q=0, s!=0")

# Last chart q=s=0 is K=r^2*A^4, covered by the all-degree K(A)
# theorem.  Check its two critical numerators directly.
K_last = r**2 * A**4 + k0
U_a_last = sp.expand(A + A**2 * delta * K_last)
critical_a = sp.Poly(sp.diff(U_a_last, A).subs(H, 0), A)
assert critical_a.coeff_monomial(1) == 1
assert critical_a.LC() == -84 * r**2

L = A**2 * K_last
N = sp.expand(sp.diff(L, A) - 48 * A * L**2 * sp.diff(L, A) - 48 * L**3)
assert sp.degree(N, A) == 18
assert sp.Poly(N, A).LC() == -336 * r**6

print("verified final q=s=0 chart by univariate K(a) critical equations")
print("RESULT: EVERY K=M_2^2+k0 TAIL HAS A CRITICAL POINT")
