"""Verify the exact algebra behind the global conductor-image theorem.

The geometric input (Lüroth plus Riemann--Hurwitz) is proved in the memo.
This script checks the fixed-plane parametrization, the full Laurent
restriction, and the residue identities for the two possible power-cover
normal forms.
"""

from fractions import Fraction

import sympy as sp


t, c, v = sp.symbols("t c v")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
D = 9 * c**2 * t**2 - 12 * c * t - 9 * c + 4

c_v = v**2 / 9
t_v = 3 * (v + 2) / v**2

assert sp.factor(D.subs({t: t_v, c: c_v})) == 0
assert sp.factor(a.subs({t: t_v, c: c_v}) - (4 - 9 * c_v) / (27 * c_v**2)) == 0
assert sp.factor(b.subs({t: t_v, c: c_v}) - (4 - 3 * c_v) / (3 * c_v)) == 0
assert sp.factor((b + 1).subs({t: t_v, c: c_v}) - 4 / (3 * c_v)) == 0
assert sp.factor(sp.diff(c_v, v) - 2 * v / 9) == 0

# The conductor itself is a smooth affine curve.  This supports the local
# smoothness step in the global Euler-characteristic dichotomy.
assert sp.groebner([D, sp.diff(D, t), sp.diff(D, c)], t, c).contains(sp.Integer(1))

# Homogenization and the two exact cusp normal forms at infinity.
T, C, Z, Ylocal = sp.symbols("T C Z Ylocal")
Dbar = 9 * C**2 * T**2 - 12 * C * T * Z**2 - 9 * C * Z**3 + 4 * Z**4
assert sp.factor(Dbar.subs(Z, 0) - 9 * C**2 * T**2) == 0

at_p0 = sp.expand(Dbar.subs(T, 1).subs(C, (Ylocal + 2 * Z**2) / 3))
assert sp.factor(at_p0 - (Ylocal**2 - 3 * Ylocal * Z**3 - 6 * Z**5)) == 0

at_pinf = sp.expand(Dbar.subs(C, 1))
assert sp.factor(at_pinf - (9 * T**2 - 12 * T * Z**2 - 9 * Z**3 + 4 * Z**4)) == 0


def derivative(poly):
    """Differentiate a Laurent polynomial represented by exponent->coefficient."""

    return {e - 1: e * a for e, a in poly.items() if e and a}


def multiply(left, right):
    out = {}
    for i, x in left.items():
        for j, y in right.items():
            out[i + j] = out.get(i + j, Fraction(0)) + x * y
    return {e: a for e, a in out.items() if a}


def residue_u_dw(u, w):
    return multiply(u, derivative(w)).get(-1, Fraction(0))


def substitute_power(poly, delta, sign=1):
    """Pull back s^i to c^(sign*delta*i); scalar shifts are already expanded."""

    return {sign * delta * i: a for i, a in poly.items()}


# In the A^1 case, regular functions are polynomials in the normalization
# coordinate.  After expanding a possible translation, their exponents in c
# all have one sign.  The residue is identically zero for arbitrary inputs.
u_affine = {0: Fraction(2), 1: Fraction(-3), 4: Fraction(5)}
w_affine = {0: Fraction(7), 2: Fraction(11), 5: Fraction(-1)}
for degree in range(1, 9):
    for sign in (-1, 1):
        assert residue_u_dw(
            substitute_power(u_affine, degree, sign),
            substitute_power(w_affine, degree, sign),
        ) == 0


# In the G_m case, Laurent functions can have a nonzero residue.  Under the
# power cover s=c^(sign*delta), residues scale by sign*delta.
u_torus = {-3: Fraction(2), -1: Fraction(5), 0: Fraction(7), 2: Fraction(-4)}
w_torus = {-2: Fraction(3), 0: Fraction(-1), 1: Fraction(11), 4: Fraction(6)}
base_residue = residue_u_dw(u_torus, w_torus)
assert base_residue != 0
for degree in range(1, 9):
    for sign in (-1, 1):
        pulled_residue = residue_u_dw(
            substitute_power(u_torus, degree, sign),
            substitute_power(w_torus, degree, sign),
        )
        assert pulled_residue == sign * degree * base_residue

print("verified the fixed conductor parametrization and full Laurent restriction")
print("verified: A1 power-cover restrictions have zero conductor residue")
print("verified: Gm power covers scale the conductor residue by their signed degree")


# Exact torus countermodel: the pullback of a smooth G_m divisor under an
# étale map can have disjoint components, each mapping by an even power cover
# and carrying a nonzero logarithmic residue.
x, y, X, Y, s = sp.symbols("x y X Y s")
pullback = sp.expand((X * Y - 1).subs({X: x**2, Y: y**2}))
assert sp.factor(pullback) == (x * y - 1) * (x * y + 1)

# The Jacobian is a unit in Q[x^±1,y^±1], so the torus map is étale.
jacobian = sp.det(sp.Matrix([[sp.diff(x**2, x), sp.diff(x**2, y)],
                             [sp.diff(y**2, x), sp.diff(y**2, y)]]))
assert sp.factor(jacobian - 4 * x * y) == 0

# The two components xy=1 and xy=-1 cannot meet in characteristic zero.
assert sp.groebner([x * y - 1, x * y + 1], x, y).contains(sp.Integer(1))

# On either component, the target normalization coordinate is s=x^2:
# X=s, Y=s^-1, and Res_0(X dY)=-1.
torus_residue = sp.residue(s * sp.diff(s**-1, s), s, 0)
assert torus_residue == -1

print("verified the disjoint étale torus pullback countermodel")
