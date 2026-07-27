"""Verify the fixed-plane Laurent residue-exponent classification model.

This is an exact symbolic verifier, not a search.  It checks:

* the smooth quartic G_m parametrization and its inverse Laurent unit;
* the Liouville residue 2/3 and Poincare exponent j=-1;
* the conormal unit k(s) and conductor residual exponent m=1;
* the (2,5) and (2,3) target-resolution valuation triples;
* both source endpoint lift ledgers; and
* two exact Green rows compatible with final type-1 defects.
"""

from fractions import Fraction

import sympy as sp


s, X, Y, Z = sp.symbols("s X Y Z", nonzero=True)

x_of_s = s**2
y_of_s = -(s ** -1 + s ** -2) / 3
F = (3 * X * Y + 1) ** 2 - X

assert sp.simplify(F.subs({X: x_of_s, Y: y_of_s})) == 0

# T=-(3XY+1) is the Laurent coordinate and its inverse is polynomial
# in T and Y on the curve.
T_of_s = sp.simplify(-(3 * x_of_s * y_of_s + 1))
Tinv_of_s = sp.simplify(-3 * T_of_s * y_of_s - 1)
assert T_of_s == s
assert Tinv_of_s == 1 / s
assert sp.expand(T_of_s**2 - x_of_s) == 0

# The boundary values are restrictions of honest elements of the
# fixed-source target ring.
t, c_source = sp.symbols("t c_source", nonzero=True)
B0 = 2 + 4 * t - 3 * c_source * t**2
A0 = t + t**2 - c_source * t**3
D0 = 9 * c_source**2 * t**2 - 12 * c_source * t - 9 * c_source + 4
v0_source = 3 * c_source * t - 2
U0 = c_source**2
V0 = -(B0 + 1) / 4 - sp.Rational(3, 16) * (B0 + 1) ** 2
v_source = sp.symbols("v_source", nonzero=True)
conductor_substitution = {
    c_source: v_source**2 / 9,
    t: 3 * (v_source + 2) / v_source**2,
}
c_on_conductor = v_source**2 / 9
assert sp.factor((B0 + 1).subs(conductor_substitution)) == 12 / v_source**2
assert sp.factor(U0.subs(conductor_substitution)) == c_on_conductor**2
assert sp.simplify(
    V0.subs(conductor_substitution)
    + (c_on_conductor ** -1 + c_on_conductor ** -2) / 3
) == 0
assert sp.expand(D0 * v0_source - (9 * B0 * c_source - 27 * A0 * c_source**2 - 8)) == 0

# The parametrized curve is smooth: F_Y=-6s^3 never vanishes on G_m.
Fx = sp.diff(F, X)
Fy = sp.diff(F, Y)
fx_s = sp.factor(Fx.subs({X: x_of_s, Y: y_of_s}))
fy_s = sp.factor(Fy.subs({X: x_of_s, Y: y_of_s}))
assert fx_s == (s + 2) / s
assert fy_s == -6 * s**3

# Liouville residue and Poincare residue.
dy_ds = sp.diff(y_of_s, s)
liouville_coefficient = sp.expand(x_of_s * dy_ds)
assert liouville_coefficient == sp.Rational(1, 3) + sp.Rational(2, 3) / s
assert sp.residue(liouville_coefficient, s, 0) == sp.Rational(2, 3)

omega_coefficient = sp.factor(sp.diff(x_of_s, s) / fy_s)
assert omega_coefficient == -sp.Rational(1, 3) / s**2
j = -1  # omega=(-1/3) s^j ds/s
assert omega_coefficient == -sp.Rational(1, 3) * s**j / s

# dF=k(-sY_s,sX_s), with k=-3s.  Hence h=-k/(6v)=v/18 for
# s=c=v^2/9.
k = -3 * s
tau_conormal = (-s * dy_ds, s * sp.diff(x_of_s, s))
assert sp.simplify(fx_s - k * tau_conormal[0]) == 0
assert sp.simplify(fy_s - k * tau_conormal[1]) == 0

v = sp.symbols("v", nonzero=True)
c = v**2 / 9
h = sp.factor(-k.subs(s, c) / (6 * v))
assert h == v / 18
m = 1
delta = 1
epsilon = 1
assert m == -1 - 2 * epsilon * delta * j

# Homogeneous quartic and its two exact projective parametrizations.
Fh = (3 * X * Y + Z**2) ** 2 - X * Z**3
assert sp.Poly(Fh, X, Y, Z).total_degree() == 4

# At s=0 use Y=1.
x0 = sp.factor(x_of_s / y_of_s)
z0 = sp.factor(1 / y_of_s)
assert x0 == -3 * s**4 / (s + 1)
assert z0 == -3 * s**2 / (s + 1)
assert sp.factor(3 * x0 + z0**2) == -9 * s**5 / (s + 1) ** 2
assert sp.simplify(((3 * X + Z**2) ** 2 - X * Z**3).subs({X: x0, Z: z0})) == 0

# At s=infinity use X=1 and tau=1/s.
tau = sp.symbols("tau")
y_inf = sp.factor((y_of_s / x_of_s).subs(s, 1 / tau))
z_inf = sp.factor((1 / x_of_s).subs(s, 1 / tau))
assert y_inf == -tau**3 * (tau + 1) / 3
assert z_inf == tau**2
assert sp.factor(3 * y_inf + z_inf**2) == -tau**3
assert sp.simplify(((3 * Y + Z**2) ** 2 - Z**3).subs({Y: y_inf, Z: z_inf})) == 0

# Resolution valuation tables.  The final entries are (M,N,c_rel).
M_25 = [1, 1, 1, 2]
N_25 = [2, 4, 5, 10]
C_25 = [1, 2, 3, 6]
assert N_25[1] == N_25[0] + 2
assert N_25[2] == N_25[1] + 1
assert N_25[3] == N_25[1] + N_25[2] + 1
assert M_25[3] == M_25[1] + M_25[2]
assert C_25[3] == C_25[1] + C_25[2] + 1

M_23 = [1, 1, 2]
N_23 = [2, 3, 6]
C_23 = [1, 2, 4]
assert N_23[1] == N_23[0] + 1
assert N_23[2] == N_23[0] + N_23[1] + 1
assert M_23[2] == M_23[0] + M_23[1]
assert C_23[2] == C_23[0] + C_23[1] + 1

d_curve = 4
triple_0 = (M_25[-1], N_25[-1], C_25[-1])
triple_inf = (M_23[-1], N_23[-1], C_23[-1])
assert triple_0 == (2, 10, 6)
assert triple_inf == (2, 6, 4)

mu_0 = Fraction(triple_0[2] + 1 - triple_0[1], triple_0[0])
mu_inf = Fraction(triple_inf[2] + 1 - triple_inf[1], triple_inf[0])
assert (mu_0, mu_inf) == (Fraction(-3, 2), Fraction(-1, 2))
assert (Fraction(d_curve - 3) + mu_0, Fraction(d_curve - 3) + mu_inf) == (
    Fraction(-1, 2),
    Fraction(1, 2),
)

# Degree-two conductor cover: exact endpoint charges.
beta = 2
b0 = beta * triple_0[0]
b_inf = beta * triple_inf[0]
kappa0 = (Fraction(d_curve - 3) + mu_0) * b0
kappa_inf = (Fraction(d_curve - 3) + mu_inf) * b_inf
assert (b0, b_inf) == (4, 4)
assert (kappa0, kappa_inf) == (-2, 2)
assert kappa0 == 2 * delta * j
assert kappa_inf == -2 * delta * j

# Source endpoint lift data:
# (a,b,kappa,sigma,eta,theta,r).
endpoint_0 = (2, 4, -2, -4, 20, 0, 13)
endpoint_inf = (-1, 4, 2, 3, 13, 1, 10)
for endpoint, triple, mu in (
    (endpoint_0, triple_0, mu_0),
    (endpoint_inf, triple_inf, mu_inf),
):
    a, b, kappa, sigma, eta, theta, ram = endpoint
    M, N, c_rel = triple
    assert kappa == a + sigma
    assert sigma == d_curve * b - eta
    assert b == M * beta
    assert eta == N * beta + theta
    assert ram == a - 1 + 3 * b
    assert ram == c_rel * beta + beta + theta - 1
    assert ram == eta + mu * b - 1
    assert ram >= 0

# One conductor-contact blowup was used at s=0.
q = 1
assert endpoint_0[3] + endpoint_inf[3] == -q
assert endpoint_0[4] + endpoint_inf[4] - q == 2 * delta * d_curve**2

# Exact point rows of Qb=0 and Qsigma=z with final type-1
# attachments b=1,7 (hence sigma=4,28).
final_b = (1, 7)
final_sigma = tuple(d_curve * b for b in final_b)
final_a = tuple(-2 * b for b in final_b)
assert final_sigma == (4, 28)
assert final_a == (-2, -14)
assert all(a - 1 + 3 * b >= 0 for a, b in zip(final_a, final_b))

for endpoint, expected_z in ((endpoint_0, 40), (endpoint_inf, 26)):
    a, b, kappa, sigma, eta, theta, ram = endpoint
    assert -2 * b + sum(final_b) == 0
    z_row = -2 * sigma + sum(final_sigma)
    assert z_row == expected_z
    assert z_row >= 0
    assert -2 * eta + z_row == 0  # Q eta + z = d y, with y=0.

# Label-level finality skeleton.
label_E4 = 1
contact_child = label_E4 + 1
type3_child_25 = contact_child + 1
label_F3 = -1
zero_child = label_F3 + 1
type3_child_23 = zero_child + 1
inserted_crossing = -2 + -1
type1_child = inserted_crossing + 1
assert (contact_child, type3_child_25) == (2, 3)
assert (zero_child, type3_child_23) == (0, 1)
assert (inserted_crossing, type1_child) == (-3, -2)

print("verified smooth quartic G_m with Liouville residue 2/3 and j=-1")
print("verified exact relation m=-1-2 epsilon delta j with m=1")
print("verified target triples (2,10,6) and (2,6,4)")
print("verified both source endpoint lift ledgers and conductor identities")
print("verified exact Green rows compatible with final type-1 defects")
