#!/usr/bin/env python3
"""Exact checks for RESIDUAL_FACTOR_HAMILTONIAN.md."""

import sympy as sp


t, c = sp.symbols("t c")
lam = sp.symbols("lam", nonzero=True)
vv = sp.symbols("vv")
v = 3 * c * t - 2
D = v**2 - 9 * c
U0 = sp.expand(D * v)
W = sp.expand(c * U0)

# The descended identity in the fixed-source ring.
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
assert sp.expand(U0 - (9 * b * c - 27 * a * c**2 - 8)) == 0

# U0 has the stated unique critical point.
U0_t = sp.factor(sp.diff(U0, t))
U0_c = sp.factor(sp.diff(U0, c))
assert sp.expand(U0_t - 9 * c * (v**2 - 3 * c)) == 0
assert sp.expand(U0_c - 9 * (t * (v**2 - 3 * c) - v)) == 0
p = {t: sp.Rational(-1, 2), c: 0}
assert U0_t.subs(p) == 0
assert U0_c.subs(p) == 0
assert U0.subs(p) == -8
Hessian = sp.hessian(U0, (t, c)).subs(p)
assert Hessian == sp.Matrix([[0, 36], [36, 0]])
assert Hessian.det() == -1296

# W=c*U0 is a submersion.  The displayed formulas prove this by splitting
# c=0 from c!=0 and then imposing v^2=3c.
W_t = sp.factor(sp.diff(W, t))
W_c = sp.factor(sp.diff(W, c))
assert sp.expand(W_t - 9 * c**2 * (v**2 - 3 * c)) == 0
assert sp.expand(W_c.subs(c, 0) + 8) == 0
Wc_in_v = sp.cancel(W_c.subs(t, (vv + 2) / (3 * c)))
Wc_on_stationary_stratum = sp.rem(
    sp.Poly(Wc_in_v, vv, domain=sp.QQ.frac_field(c)),
    sp.Poly(vv**2 - 3 * c, vv, domain=sp.QQ.frac_field(c)),
).as_expr()
assert sp.expand(Wc_on_stationary_stratum + 15 * c * vv) == 0

# The leading t-degree calculation behind the descent modulo k[W].
n = sp.symbols("n", integer=True, positive=True)
fn, fn_prime = sp.symbols("fn fn_prime")
W_poly = sp.Poly(W, t)
Wt_poly = sp.Poly(sp.diff(W, t), t)
Wc_poly = sp.Poly(sp.diff(W, c), t)
assert W_poly.degree() == 3
assert W_poly.LC() == 27 * c**4
assert Wt_poly.LC() == 81 * c**4
assert Wc_poly.LC() == 108 * c**3
top_bracket = 81 * c**4 * fn_prime - 108 * n * c**3 * fn
assert sp.factor(top_bracket) == 27 * c**3 * (
    3 * c * fn_prime - 4 * n * fn
)

# Check the final t-degree-zero bracket.
q_prime = sp.symbols("q_prime")
assert sp.expand(W_t * q_prime - 9 * c**2 * (v**2 - 3 * c) * q_prime) == 0

# The classification step: on v^2=3c, U=f(c)+g(c)Dv has
# U_c=f'-v(6cg'+9g).
f0, fp, g0, gp = sp.symbols("f0 fp g0 gp")
U_formal_c = fp + gp * U0 + g0 * U0_c
U_formal_c_in_v = sp.cancel(U_formal_c.subs(t, (vv + 2) / (3 * c)))
remainder = sp.rem(
    sp.Poly(
        U_formal_c_in_v,
        vv,
        domain=sp.QQ.frac_field(c, fp, g0, gp),
    ),
    sp.Poly(
        vv**2 - 3 * c,
        vv,
        domain=sp.QQ.frac_field(c, fp, g0, gp),
    ),
).as_expr()
assert sp.expand(remainder - (fp - vv * (6 * c * gp + 9 * g0))) == 0

# For g=lambda*c^q, the operator B=6cg'+9g preserves the monomial and
# has a nonzero eigenvalue in characteristic zero.
q = sp.symbols("q", integer=True, nonnegative=True)
B_monomial = 6 * c * sp.diff(lam * c**q, c) + 9 * lam * c**q
assert sp.factor(B_monomial) == 3 * lam * c**q * (2 * q + 3)

print("fixed-plane residual Hamiltonian checks passed")
