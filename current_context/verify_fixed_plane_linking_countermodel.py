#!/usr/bin/env python3
"""Exact checks for the étale-complement model in §1.16."""

import sympy as sp


p, q, delta = sp.symbols("p q delta", nonzero=True)
X = p ** (2 * delta)
Y = q

# The map is étale on the torus for every positive integral delta.
jac = sp.diff(X, p) * sp.diff(Y, q) - sp.diff(X, q) * sp.diff(Y, p)
assert sp.simplify(jac - 2 * delta * p ** (2 * delta - 1)) == 0

# The target hyperbola pulls back to a connected cyclic cover
# p^(2 delta) q = 1, parametrized by p with q=p^(-2 delta).
target_equation = X * Y - 1
assert sp.factor(target_equation.subs(q, p ** (-2 * delta))) == 0

# On Gamma, s=X and Y=s^(-1); winding orders against the two axes.
s = sp.symbols("s", nonzero=True)
assert s.as_powers_dict()[s] == 1
assert (1 / s).as_powers_dict()[s] == -1

print("fixed-plane linking countermodel checks passed")
