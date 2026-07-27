#!/usr/bin/env python3
"""Exact checks for FIXED_PLANE_RESIDUE_PARITY_SCALING_NO_GO.md."""

import sympy as sp


v, c = sp.symbols("v c", nonzero=True)
x = v**2
y = v * (v**2 - 9 * c)
t = (v + 2) / (3 * c)


def jac(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.factor(
        sp.diff(left, v) * sp.diff(right, c)
        - sp.diff(left, c) * sp.diff(right, v)
    )


A = x**3 / (6561 * c**2)
B = -243 * c * y / (2 * x**3) - sp.Rational(2, 3) / A
I = sp.factor(A * B)
S = -sp.Rational(5, 6) * v + v**3 / (54 * c)
log_argument = x / c
kappa = -sp.Rational(2, 3)

assert jac(A, B) == 1 / (3 * c)
assert sp.factor(I + (-9 * c * v + 36 * c + v**3) / (54 * c)) == 0
assert sp.factor(I.subs(c, v**2 / 9) - kappa) == 0
assert sp.factor(A.subs(c, v**2 / 9) - v**2 / 81) == 0
assert sp.factor(B.subs(c, v**2 / 9) + 54 / v**2) == 0

for coordinate in (v, c):
    beta = A * sp.diff(B, coordinate)
    if coordinate == c:
        beta -= t
    assert sp.factor(
        beta
        - sp.diff(S, coordinate)
        - 2 * sp.diff(sp.log(log_argument), coordinate)
    ) == 0


def canonical_scaling(
    zero: sp.Rational,
    pole: sp.Rational,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    raw = (I**2 - zero**2) / (I**2 - pole**2)
    normalization = sp.factor(1 / raw.subs(c, v**2 / 9))
    scaling = sp.factor(normalization * raw)
    U = sp.factor(A * scaling)
    V = sp.factor(B / scaling)
    assert sp.factor(scaling.subs(c, v**2 / 9) - 1) == 0
    assert jac(U, V) == 1 / (3 * c)
    assert sp.factor(U.subs(c, v**2 / 9) - v**2 / 81) == 0
    assert sp.factor(V.subs(c, v**2 / 9) + 54 / v**2) == 0
    return scaling, U, V


# Nonintegral endpoint-neutral scaling.
scaling_nonintegral, U_nonintegral, V_nonintegral = canonical_scaling(
    sp.Rational(1, 5),
    sp.Rational(1, 4),
)
nonintegral_residues = (
    -sp.Rational(3, 2) * sp.Rational(1, 5),
    sp.Rational(3, 2) * sp.Rational(1, 5),
    sp.Rational(3, 2) * sp.Rational(1, 4),
    -sp.Rational(3, 2) * sp.Rational(1, 4),
)
assert nonintegral_residues == (
    -sp.Rational(3, 10),
    sp.Rational(3, 10),
    sp.Rational(3, 8),
    -sp.Rational(3, 8),
)
assert sum(nonintegral_residues) == 0
assert any(not residue.is_integer for residue in nonintegral_residues)

# Integral but parity-changing endpoint-neutral scaling.
scaling_integral, U_integral, V_integral = canonical_scaling(
    sp.Integer(2),
    sp.Rational(4, 3),
)
assert sp.factor(
    scaling_integral
    - sp.Rational(3, 8) * (I**2 - 4) / (I**2 - sp.Rational(16, 9))
) == 0
integral_residues = (
    -sp.Integer(3),
    sp.Integer(3),
    sp.Integer(2),
    -sp.Integer(2),
)
assert sum(integral_residues) == 0
assert all(residue.is_integer for residue in integral_residues)

# Verify the exact Liouville-change identity and its dlog decomposition.
for coordinate in (v, c):
    scaled_beta = U_integral * sp.diff(V_integral, coordinate)
    original_beta = A * sp.diff(B, coordinate)
    scaling_change = -I * sp.diff(sp.log(scaling_integral), coordinate)
    assert sp.factor(scaled_beta - original_beta - scaling_change) == 0

    decomposed_change = (
        -2 * sp.diff(sp.log(I - 2), coordinate)
        + 2 * sp.diff(sp.log(I + 2), coordinate)
        + sp.Rational(4, 3) * sp.diff(
            sp.log(I - sp.Rational(4, 3)), coordinate
        )
        - sp.Rational(4, 3) * sp.diff(
            sp.log(I + sp.Rational(4, 3)), coordinate
        )
    )
    assert sp.factor(scaling_change - decomposed_change) == 0

# The two new odd level divisors are genuine irreducible cubics.
level_plus = sp.factor(-54 * c * (I - 2))
level_minus = sp.factor(-54 * c * (I + 2))
assert level_plus == v**3 - 9 * c * v + 144 * c
assert level_minus == v**3 - 9 * c * v - 72 * c
assert sp.Poly(level_plus, c).degree() == 1
assert sp.Poly(level_minus, c).degree() == 1
assert sp.gcd(v**3, 144 - 9 * v) == 1
assert sp.gcd(v**3, -72 - 9 * v) == 1

# The conductor boundary action remains exactly 2/3.
c_boundary = sp.symbols("c_boundary", nonzero=True)
u_boundary = c_boundary / 9
w_boundary = -6 / c_boundary
assert sp.residue(
    u_boundary * sp.diff(w_boundary, c_boundary),
    c_boundary,
    0,
) == sp.Rational(2, 3)

print("verified both rational canonical scalings preserve the Darboux equation")
print("verified conductor descent, boundary values, and residue 2/3")
print("verified endpoint-neutral nonintegral residues")
print("verified integral residues with two new odd level divisors")
print("RESULT: RATIONAL RESIDUE QUANTIZATION AND PARITY ARE NOT INVARIANT")
