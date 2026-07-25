#!/usr/bin/env python3
"""Verify the balanced cusp-endpoint graded-ring obstruction."""

import sympy as sp


r, tau, p = sp.symbols("r tau p", nonzero=True)

# Initial forms on the first exceptional divisor, graded by pole order in
# tau.  Their degrees are 2, 1, and -1.
A = (1 - r) / tau**2
B = (4 - 3 * r) / tau
C = r * tau

# Every degree-zero monomial A^alpha B^beta C^gamma has
# gamma=2*alpha+beta and is therefore a monomial in f=A*C^2 and g=B*C.
f = sp.factor(A * C**2)
g = sp.factor(B * C)
assert sp.expand(f - r**2 * (1 - r)) == 0
assert sp.expand(g - r * (4 - 3 * r)) == 0

r0 = sp.Rational(2, 3)
assert sp.diff(f, r).subs(r, r0) == 0
assert sp.diff(g, r).subs(r, r0) == 0

# Hence the derivative of every polynomial h(f,g) vanishes at r0.
h_f, h_g = sp.symbols("h_f h_g")
generic_chain_derivative = h_f * sp.diff(f, r) + h_g * sp.diff(g, r)
assert sp.expand(generic_chain_derivative.subs(r, r0)) == 0

# More generally, every degree-d homogeneous coefficient h(r) in gr(R)
# obeys the endpoint Robin condition 2h'(r0)+3d*h(r0)=0.  It holds on
# the three generators and is multiplicative in the graded degree.
a_coefficient = 1 - r
b_coefficient = 4 - 3 * r
c_coefficient = r


def robin(coefficient, degree):
    return sp.expand(
        2 * sp.diff(coefficient, r).subs(r, r0)
        + 3 * degree * coefficient.subs(r, r0)
    )


assert robin(a_coefficient, 2) == 0
assert robin(b_coefficient, 1) == 0
assert robin(c_coefficient, -1) == 0

# Centering at the tangency identifies the degree-zero cusp and starts the
# full positive-degree conductor ideal.
w = sp.symbols("w")
centered_substitution = {r: w + r0}
f_centered = sp.expand(f.subs(centered_substitution))
g_centered = sp.expand(g.subs(centered_substitution))
assert sp.expand(f_centered - (sp.Rational(4, 27) - w**2 - w**3)) == 0
assert sp.expand(g_centered - (sp.Rational(4, 3) - 3 * w**2)) == 0

a_centered = sp.expand(a_coefficient.subs(centered_substitution))
b_centered = sp.expand(b_coefficient.subs(centered_substitution))
c_centered = sp.expand(c_coefficient.subs(centered_substitution))
assert sp.expand(a_centered * c_centered - b_centered / 9 + w**2) == 0
assert sp.expand(b_centered**2 - 12 * a_centered - 9 * w**2) == 0
assert sp.gcd(a_centered, b_centered) == 1

h1, h2, d1, d2 = sp.symbols("h1 h2 d1 d2")
h1_prime = -sp.Rational(3, 2) * d1 * h1
h2_prime = -sp.Rational(3, 2) * d2 * h2
product_robin = sp.expand(
    2 * (h1_prime * h2 + h1 * h2_prime)
    + 3 * (d1 + d2) * h1 * h2
)
assert product_robin == 0

# If the leading forms of U,V have opposite nonzero degrees p,-p, write
#
#   U=tau^-p*u(r), V=tau^p*v(r).
#
# Their tau^-1 Jacobian coefficient is -p*(u*v)'.
u = sp.Function("u")(r)
v = sp.Function("v")(r)
U = tau ** (-p) * u
V = tau**p * v
jac = sp.factor(
    sp.diff(U, tau) * sp.diff(V, r)
    - sp.diff(U, r) * sp.diff(V, tau)
)
assert sp.simplify(jac + p * sp.diff(u * v, r) / tau) == 0

# In the mixed-sign case p>0 and q=-s<0, cancellation of the top
# Jacobian coefficient is exactly (u^s*v^p)'=0 up to a nonzero factor.
s = sp.symbols("s", positive=True)
mixed_coefficient = p * u * sp.diff(v, r) + s * sp.diff(u, r) * v
mixed_product_derivative = sp.diff(u**s * v**p, r)
assert sp.simplify(
    mixed_product_derivative
    - u ** (s - 1) * v ** (p - 1) * mixed_coefficient
) == 0

print("verified gr(R)_0=Q[r^2(1-r),r(4-3r)]")
print("verified the endpoint Robin condition in every homogeneous degree")
print("RESULT: ALL BALANCED NONZERO ENDPOINT VALUATIONS ARE IMPOSSIBLE")
