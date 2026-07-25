#!/usr/bin/env python3
"""Exact symbolic checks for the Route C progress memo."""

import sympy as sp


x, y, z, lam = sp.symbols("x y z lam")
surface = x**2 * y - z**2 + 1


def tau(coords, parameter):
    """The Danielewski-surface automorphism exp(parameter * delta)."""
    X, Y, Z = coords
    return (
        X,
        sp.expand(Y + 2 * parameter * Z + parameter**2 * X**2),
        sp.expand(Z + parameter * X**2),
    )


def phi2(coords):
    """The degree-two Chebyshev etale endomorphism."""
    X, Y, Z = coords
    return (sp.expand(2 * X * Z), Y, sp.expand(2 * Z**2 - 1))


def reduce_on_surface(expression):
    """Reduce modulo x^2*y-z^2+1, using y as the leading variable."""
    return sp.rem(
        sp.Poly(sp.expand(expression), y, domain=sp.QQ.frac_field(x, z, lam)),
        sp.Poly(surface, y, domain=sp.QQ.frac_field(x, z, lam)),
    ).as_expr()


# Conjugate phi_2 by a non-equivariant shear tau_lam.
source = (x, y, z)
psi = tau(phi2(tau(source, lam)), -lam)
X, Y, Z = psi

# 1. It is a surface endomorphism.
assert sp.factor(X**2 * Y - Z**2 + 1) == sp.factor(
    4 * (z + lam * x**2) ** 2 * surface
)
assert reduce_on_surface(X**2 * Y - Z**2 + 1) == 0

# 2. Its canonical Jacobian is the constant 2:
#    omega=dx^dz/x^2 and Psi^*omega=H*omega.
canonical_jacobian = sp.factor(
    x**2 * sp.det(sp.Matrix([[sp.diff(X, x), sp.diff(X, z)],
                              [sp.diff(Z, x), sp.diff(Z, z)]])) / X**2
)
assert canonical_jacobian == 2

# 3. The Laurent-parametrized curve E_lam lies on the surface and maps to D_-.
s = sp.symbols("s", nonzero=True)
curve_substitution = {
    x: s,
    z: -lam * s**2,
    y: lam**2 * s**2 - s**-2,
}
assert sp.simplify(surface.subs(curve_substitution)) == 0
assert sp.simplify(X.subs(curve_substitution)) == 0
assert sp.simplify(Z.subs(curve_substitution)) == -1

# 4. The Chebyshev identities and canonical Jacobians hold exactly.
for degree in range(2, 9):
    R = sp.chebyshevt(degree, z)
    U = sp.chebyshevu(degree - 1, z)
    assert sp.expand(R**2 - 1 - (z**2 - 1) * U**2) == 0
    assert sp.expand(sp.diff(R, z) - degree * U) == 0
    assert sp.expand(R.subs(z, 1) - 1) == 0
    assert sp.expand(R.subs(z, -1) - (-1) ** degree) == 0
    # For even degree, -1 has only the interior critical preimages
    # cos(k*pi/d), k odd; for odd degree the endpoint z=-1 is a
    # noncritical preimage.  Hence the only omitted divisor in the even
    # case is L_-={y=0,z=-1}.
    if degree % 2 == 0:
        assert all((-1) ** k == -1 for k in range(1, degree, 2))
        assert sp.expand(R.subs(z, -1) - 1) == 0
    else:
        assert sp.expand(R.subs(z, -1) + 1) == 0
        assert sp.expand(U.subs(z, -1)) != 0

    # Every target sign has either another endpoint preimage or an interior
    # critical preimage.  This is the explicit inverse-image obstruction
    # used in the alternative-boundary theorem.
    for sign in (-1, 1):
        endpoint_extra = any(
            endpoint != sign
            and sp.expand(R.subs(z, endpoint) - sign) == 0
            for endpoint in (-1, 1)
        )
        critical_extra = False
        for k in range(1, degree):
            # T_d(cos(k*pi/d))=(-1)^k and U_{d-1} vanishes there.
            if (-1) ** k == sign:
                critical_extra = True
                break
        assert endpoint_extra or critical_extra

# 5. On the A^2 chart z=1+x^2*t, the conjugated restriction has a genuine
#    pole along 1+x^2*(t+lam)=0, precisely the curve mapped to D_-.
t = sp.symbols("t")
u = 1 + x**2 * (t + lam)
chart_X = 2 * x * u
chart_T = (u**2 - 1) / (2 * x**2 * u**2) - lam
chart_jacobian = sp.factor(
    sp.det(
        sp.Matrix(
            [
                [sp.diff(chart_X, x), sp.diff(chart_X, t)],
                [sp.diff(chart_T, x), sp.diff(chart_T, t)],
            ]
        )
    )
)
assert chart_jacobian == 2
assert sp.simplify((u**2 * chart_T).subs(u, 0)) != 0

# 6. The same obstruction holds for a kernel-polynomial shear.  A generic
#    quadratic is checked here; the proof is formal and degree-independent.
a0, a1, a2 = sp.symbols("a0 a1 a2")


def f_polynomial(value):
    return a0 + a1 * value + a2 * value**2


def tau_f(coords, sign=1):
    X0, Y0, Z0 = coords
    parameter = sign * f_polynomial(X0)
    return (
        X0,
        sp.expand(Y0 + 2 * parameter * Z0 + parameter**2 * X0**2),
        sp.expand(Z0 + parameter * X0**2),
    )


psi_f = tau_f(phi2(tau_f(source)), sign=-1)
Xf, Yf, Zf = psi_f
f_at_x = f_polynomial(x)
uf = z + f_at_x * x**2
assert sp.factor(Xf**2 * Yf - Zf**2 + 1) == sp.factor(
    4 * uf**2 * surface
)
canonical_jacobian_f = sp.factor(
    x**2
    * sp.det(
        sp.Matrix(
            [
                [sp.diff(Xf, x), sp.diff(Xf, z)],
                [sp.diff(Zf, x), sp.diff(Zf, z)],
            ]
        )
    )
    / Xf**2
)
assert canonical_jacobian_f == 2
f_at_s = f_polynomial(s)
curve_f_substitution = {
    x: s,
    z: -f_at_s * s**2,
    y: f_at_s**2 * s**2 - s**-2,
}
assert sp.simplify(surface.subs(curve_f_substitution)) == 0
assert sp.simplify(Xf.subs(curve_f_substitution)) == 0
assert sp.simplify(Zf.subs(curve_f_substitution)) == -1

print("Psi_lambda coordinates:")
print("X =", sp.factor(X))
print("Y =", sp.factor(Y))
print("Z =", sp.factor(Z))
print("canonical Jacobian =", canonical_jacobian)
print("exceptional curve: x=s, z=-lambda*s^2, y=lambda^2*s^2-s^-2")
print("chart Jacobian =", chart_jacobian)
print("generic quadratic f(x) shear conjugate: all checks passed")
print("all exact checks passed")
