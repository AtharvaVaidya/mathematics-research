#!/usr/bin/env python3
"""Exclude the constant K tails in the Q[a,b] boundary classification.

Up to nonzero scaling, these are

    U_a = a + k*a^2*Delta,
    U_b = b + k*a^2*Delta,

where Delta=(b+1)^2-12*a.  For k!=0 each has an explicit critical point
over the algebraic closure, so neither can be a Darboux Hamiltonian.
The k=0 cases a and b are already excluded by the all-degree recurrence.
"""

import sympy as sp


t, c, k, z = sp.symbols("t c k z")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
delta = (b + 1) ** 2 - 12 * a

u_a = sp.expand(a + k * a**2 * delta)
u_b = sp.expand(b + k * a**2 * delta)

resultant_a = sp.factor(
    sp.resultant(sp.diff(u_a, t), sp.diff(u_a, c), c)
)
resultant_b = sp.factor(
    sp.resultant(sp.diff(u_b, t), sp.diff(u_b, c), c)
)

assert resultant_a == 5832 * k**3 * t**39 * (4 * k * t**4 - 1)
assert resultant_b == (
    17496
    * k**3
    * t**35
    * (8 * k**2 * t**10 + 396 * k * t**5 + 27)
)

# For U_a choose t!=0 with k*t^4=1/4 and then
# c=(4t+3)/(3t^2).  Both partial derivatives vanish exactly.
c_a = (4 * t + 3) / (3 * t**2)
for derivative in (sp.diff(u_a, t), sp.diff(u_a, c)):
    assert sp.factor(
        derivative.subs({c: c_a, k: 1 / (4 * t**4)})
    ) == 0

# For U_b choose a root z of 8z^2+396z+27=0, set k*t^5=z, and use
# the linear penultimate subresultant to recover c.  The root is neither
# zero nor -1, so all displayed denominators are legitimate.
q = 8 * z**2 + 396 * z + 27
assert q.subs(z, 0) != 0
assert q.subs(z, -1) != 0
c_b = ((16 * z - 3) * t + 18 * (z + 1)) / (
    18 * t**2 * (z + 1)
)
for derivative in (sp.diff(u_b, t), sp.diff(u_b, c)):
    numerator = sp.together(
        derivative.subs({c: c_b, k: z / t**5})
    ).as_numer_denom()[0]
    assert sp.factor(sp.rem(numerator, q, z)) == 0

print("verified Res_c(dU_a)=5832*k^3*t^39*(4*k*t^4-1)")
print("verified explicit critical point for every nonzero a-tail parameter")
print("verified Res_c(dU_b)=17496*k^3*t^35*(8*(k*t^5)^2+396*k*t^5+27)")
print("verified explicit critical point for every nonzero b-tail parameter")
print("RESULT: CONSTANT K TAILS IN BOTH Q[a,b] BRANCHES ARE EXCLUDED")
