#!/usr/bin/env python3
"""Exclude every quadratic square-top K tail by critical points.

The primitive-leading obstruction reduces degree-two tails to

    K=(r*a+s*H)^2+k0+k1*a+k2*H,   (r,s)!=(0,0),

where H=b+1 and Delta=H^2-12a.  This verifier proves that both

    a+a^2*Delta*K,   H+a^2*Delta*K

have a critical point over the algebraic closure for every parameter
choice.  Additive constants and nonzero scaling do not matter.

Every target point (a,H) with a!=0 lifts to the normalization: its
t-coordinates solve t*(H-t)=3a and are nonzero, after which
c=(3+4t-H)/(3t^2).  Thus a target-coordinate critical point with a!=0
is a genuine finite critical point of the normalization Hamiltonian.
"""

import sympy as sp


A, H = sp.symbols("A H")
r, s = sp.symbols("r s")
k0, k1, k2, inverse = sp.symbols("k0 k1 k2 inverse")
delta = H**2 - 12 * A
K = (r * A + s * H) ** 2 + k0 + k1 * A + k2 * H


def positive_coefficient_ideal_is_unit(polynomial):
    coefficients = [
        coefficient
        for (exponent,), coefficient in sp.Poly(polynomial, A).terms()
        if exponent > 0
    ]
    saturated = sp.groebner(
        coefficients + [inverse * s - 1],
        inverse,
        r,
        s,
        k0,
        k1,
        k2,
        order="grevlex",
    )
    return list(saturated) == [1]


# Chart s!=0.  The target-coordinate derivative resultants have a power
# of A and s^2 as their only systematic factors.  Their residual constant
# terms are nonzero, while the saturated positive-coefficient ideals are
# units, so each residual is nonconstant for every parameter choice.
for base, name, a_power, residual_degree, residual_constant in (
    (A, "a", 8, 13, 128 * s**6),
    (H, "b", 3, 18, 4 * s**4),
):
    F = sp.expand(base + A**2 * delta * K)
    F_A = sp.diff(F, A)
    F_H = sp.diff(F, H)
    assert sp.factor(sp.Poly(F_A, H).LC()) == 2 * A * s**2
    assert sp.factor(sp.Poly(F_H, H).LC()) == 4 * A**2 * s**2

    resultant = sp.factor(sp.resultant(F_A, F_H, H))
    residual = sp.cancel(resultant / (2 * A**a_power * s**2))
    residual_poly = sp.Poly(residual, A)
    assert residual_poly.degree() == residual_degree
    assert sp.factor(residual_poly.coeff_monomial(1)) == residual_constant
    assert positive_coefficient_ideal_is_unit(residual)

    # A nonconstant polynomial with nonzero constant has a nonzero A-root.
    # At A*s!=0 both H-leading coefficients above remain nonzero, so the
    # resultant root is a finite common zero, not a degree-drop artifact.
    print(
        f"verified {name}-branch s!=0 resultant: nonconstant residual "
        f"of A-degree {residual_degree} with nonzero constant"
    )


# Chart s=0, so r!=0.
K_s0 = r**2 * A**2 + k0 + k1 * A + k2 * H

# If k2!=0, the lower-H-degree resultants again have nonconstant residuals
# with nonzero constants and leading coefficients controlled by r.
for base, name, a_power, residual_constant in (
    (A, "a", 6, -27 * k2**2),
    (H, "b", 2, -4 * k2),
):
    F = sp.expand(base + A**2 * delta * K_s0)
    F_A = sp.diff(F, A)
    F_H = sp.diff(F, H)
    assert sp.factor(sp.Poly(F_A, H).LC()) == 2 * A * k2
    assert sp.factor(sp.Poly(F_H, H).LC()) == 3 * A**2 * k2
    resultant = sp.factor(sp.resultant(F_A, F_H, H))
    residual = sp.cancel(resultant / (-A**a_power * k2))
    residual_poly = sp.Poly(residual, A)
    assert sp.factor(residual_poly.coeff_monomial(1)) == residual_constant
    assert sp.factor(residual_poly.LC() / r**8).is_number
    assert residual_poly.degree() > 0
    print(f"verified {name}-branch s=0, k2!=0 resultant")


# Final chart s=k2=0.  Put K0=r^2*A^2+k1*A+k0.
K0 = r**2 * A**2 + k1 * A + k0

# In the a-branch, H=0 makes F_H=0.  The remaining derivative is a
# degree-four polynomial with constant 1 and leading coefficient -60r^2,
# so it has a nonzero algebraic root.
F_a_final = sp.expand(A + A**2 * delta * K0)
critical_a_at_h0 = sp.factor(sp.diff(F_a_final, A).subs(H, 0))
assert critical_a_at_h0.subs(A, 0) == 1
assert sp.degree(critical_a_at_h0, A) == 4
assert sp.Poly(critical_a_at_h0, A).LC() == -60 * r**2
assert sp.diff(F_a_final, H).subs(H, 0) == 0

# In the b-branch write L=A^2*K0.  F_H=0 gives H=-1/(2L).
# After clearing 4L^2 from F_A, the numerator
#
#   N=L' - 48*A*L^2*L' - 48*L^3
#
# has degree 12.  At a root of L of multiplicity m it has multiplicity
# exactly m-1, so at most deg(L)-1=3 of its roots (with multiplicity) lie
# on L=0.  Hence at least one root has A*L!=0 and yields a critical point.
L = sp.expand(A**2 * K0)
L_prime = sp.diff(L, A)
N = sp.factor(L_prime - 48 * A * L**2 * L_prime - 48 * L**3)
assert sp.factor(N / A).is_polynomial(A)
assert sp.degree(N, A) == 12
assert sp.Poly(N, A).LC() == -240 * r**6

H_critical = -1 / (2 * L)
F_b_final = sp.expand(H + A**2 * delta * K0)
cleared_F_A = sp.factor(
    sp.diff(F_b_final, A).subs(H, H_critical) * 4 * L**2
)
assert sp.expand(cleared_F_A - N) == 0
assert sp.simplify(sp.diff(F_b_final, H).subs(H, H_critical)) == 0

print("verified final s=k2=0 a-branch degree-four critical equation")
print("verified final s=k2=0 b-branch degree-12 numerator and root count")
print("all constructed target critical points have A!=0 and lift finitely")
print("RESULT: EVERY QUADRATIC SQUARE-TOP K TAIL HAS A CRITICAL POINT")
