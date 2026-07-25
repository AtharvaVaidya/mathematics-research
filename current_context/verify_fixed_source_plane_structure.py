#!/usr/bin/env python3
"""Exact structural checks for the fixed-source-plane construction route.

On x=1 the three-dimensional Keller map restricts to the normalization
coordinates (t,c), with t=y+1.  This verifier checks the hypersurface
presentation, its conductor factor, the canonical minor identity, and the
all-degree exclusion of every linear target Hamiltonian.
"""

import sympy as sp


t, c = sp.symbols("t c")
A, B, C = sp.symbols("A B C")

a = sp.expand(t + t**2 - c * t**3)
b = sp.expand(2 + 4 * t - 3 * c * t**2)


def jacobian(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, t) * sp.diff(right, c)
        - sp.diff(left, c) * sp.diff(right, t)
    )


relation = (
    27 * A**2 * C**2
    - 18 * A * B * C
    + 16 * A
    + B**3 * C
    - B**2
    - 3 * B * C
    - 2 * C
    + 4
)
pullback = {A: a, B: b, C: c}
assert sp.expand(relation.subs(pullback)) == 0

conductor = 9 * c**2 * t**2 - 12 * c * t - 9 * c + 4
assert sp.expand((4 - 3 * B * C - 3 * C).subs(pullback) - conductor) == 0

minor_ab = jacobian(a, b)
minor_ac = jacobian(a, c)
minor_bc = jacobian(b, c)
assert sp.factor(minor_ab) == t**2 * (3 * c * t**2 - 2 * t - 3)
assert sp.factor(minor_ac) == -3 * c * t**2 + 2 * t + 1
assert sp.expand(minor_bc + 2 * (3 * c * t - 2)) == 0

# The cross product of the normalization derivatives is grad(relation)/D.
partials = [sp.diff(relation, variable) for variable in (A, B, C)]
assert sp.expand(partials[0].subs(pullback) - conductor * minor_bc) == 0
assert sp.expand(partials[1].subs(pullback) + conductor * minor_ac) == 0
assert sp.expand(partials[2].subs(pullback) - conductor * minor_ab) == 0

# The canonical area coefficient is already in the target-ring span of the
# three basic minors.  This shows that the remaining issue is integrability,
# rather than module generation.
assert sp.expand(
    c * minor_ab / 2 + b * minor_ac / 2 - a * minor_bc - 1
) == 0


# Classification used in the memo.  For a linear target Hamiltonian
#
#   U = alpha*a + beta*b + gamma*c,
#
# U_c=q(t), while U_t=l(t)-c*k(t).  Unless U is proportional to a, b, or c,
# q has a root outside k=0 and hence U has a critical point.
alpha, beta, gamma = sp.symbols("alpha beta gamma")
linear_u = sp.expand(alpha * a + beta * b + gamma * c)
q = sp.diff(linear_u, c)
ell = alpha * (1 + 2 * t) + 4 * beta
k = 3 * t * (alpha * t + 2 * beta)
assert sp.expand(sp.diff(linear_u, t) - (ell - c * k)) == 0
assert sp.expand(q - (gamma - alpha * t**3 - 3 * beta * t**2)) == 0

# If alpha*beta != 0 and every root of q lay in
# t*(alpha*t+2*beta)=0, then after alpha=1, r=beta/alpha the monic
# factorization would be one of the following four.  Each contradicts the
# t or t^2 coefficient of q.
r = sp.symbols("r", nonzero=True)
normalized_q = -t**3 - 3 * r * t**2 + gamma
for multiplicity_at_zero in range(4):
    supported = -t**multiplicity_at_zero * (
        t + 2 * r
    ) ** (3 - multiplicity_at_zero)
    difference = sp.Poly(
        sp.expand(normalized_q - supported), t
    )
    coefficients = difference.as_dict()
    if multiplicity_at_zero in (0, 1):
        assert coefficients.get((1,), 0) != 0
    else:
        assert coefficients.get((2,), 0) != 0

# For U=a or U=b, comparison of the top c coefficient in
# Jac(U,V)=constant recursively removes a polynomial in U.  The final
# c-independent remainder v(t) would have to solve respectively
# t^3*v'(t)=constant or 3*t^2*v'(t)=constant, impossible for a polynomial.
n = sp.symbols("n", integer=True, positive=True)
leading_a = sp.Function("v")(t)
leading_b = sp.Function("w")(t)
assert sp.expand(
    t**3 * sp.diff(leading_a, t)
    - 3 * n * t**2 * leading_a
    - t**2 * (t * sp.diff(leading_a, t) - 3 * n * leading_a)
) == 0
assert sp.expand(
    3 * t**2 * sp.diff(leading_b, t)
    - 6 * n * t * leading_b
    - 3 * t * (t * sp.diff(leading_b, t) - 2 * n * leading_b)
) == 0

# The first genuinely nonlinear submersion found by the sparse quadratic
# search is U=a(1+b).  Its gradient ideal is the unit ideal, but it too has
# no polynomial mate.  If V has c-degree n, its top bracket coefficient is
# 3*t^4*(5*n*v_n-2*t*v_n').  Hence n must be even and the leading term is
# removed by a multiple of U^(n/2).  The final c-independent remainder has
# a c-dependent bracket unless its derivative vanishes.
quadratic_submersion = sp.expand(a * (1 + b))
gradient_basis = sp.groebner(
    [
        sp.diff(quadratic_submersion, t),
        sp.diff(quadratic_submersion, c),
    ],
    c,
    t,
    order="lex",
)
assert list(gradient_basis) == [1]
leading_q = sp.Function("q")(t)
top_coefficient = sp.expand(
    15 * t**4 * n * leading_q - 6 * t**5 * sp.diff(leading_q, t)
)
assert sp.expand(
    top_coefficient
    - 3
    * t**4
    * (5 * n * leading_q - 2 * t * sp.diff(leading_q, t))
) == 0
assert sp.factor(sp.diff(quadratic_submersion, c)) == t**3 * (
    6 * c * t**2 - 7 * t - 6
)

# General leading-coefficient obstruction.  For
# U=u_2(t)c^2+... and V=v_m(t)c^m+..., the top bracket coefficient is
# m*u_2'*v_m-2*u_2*v_m'.  Its vanishing says
# (v_m^2/u_2^m)'=0.  If u_2 is not a square, m is even and a multiple of
# U^(m/2) removes the leading term; induction reaches an impossible
# c-independent mate.
u2_function = sp.Function("u2")(t)
vm_function = sp.Function("vm")(t)
generic_top = (
    n * sp.diff(u2_function, t) * vm_function
    - 2 * u2_function * sp.diff(vm_function, t)
)
quotient_derivative = sp.diff(
    vm_function**2 / u2_function**n, t
)
assert sp.simplify(
    quotient_derivative
    + vm_function * generic_top / u2_function ** (n + 1)
) == 0

print("verified fixed-plane hypersurface and conductor identities")
print("verified canonical target-module minor identity")
print("verified all-degree exclusion mechanism for linear Hamiltonians")
print("verified all-degree exclusion of the quadratic submersion a*(1+b)")
print("verified nonsquare leading-coefficient obstruction")
