"""Verify the arbitrary-d collision conductor and pullback identities."""

from __future__ import annotations

import sympy as sp


x, t, U, V, y, z = sp.symbols("x t U V y z")


def reduce_zeta(expr: sp.Expr) -> sp.Expr:
    """Reduce an expression modulo z^2+z+1."""
    numerator, denominator = sp.fraction(sp.cancel(expr))
    numerator = sp.rem(sp.Poly(numerator, z), sp.Poly(z**2 + z + 1, z)).as_expr()
    denominator = sp.rem(
        sp.Poly(denominator, z), sp.Poly(z**2 + z + 1, z)
    ).as_expr()
    inverse = sp.invert(
        sp.Poly(denominator, z), sp.Poly(z**2 + z + 1, z)
    ).as_expr()
    return sp.rem(
        sp.Poly(sp.expand(numerator * inverse), z),
        sp.Poly(z**2 + z + 1, z),
    ).as_expr()


def collision_product(d: sp.Expr, u: sp.Rational) -> tuple[sp.Expr, sp.Expr]:
    phi = x + (1 - z**2) * d**2 / u
    numerator = reduce_zeta(sp.expand(d.subs(x, phi) - z * d))
    quotient = sp.cancel(numerator / d)
    assert sp.cancel(quotient * d - numerator) == 0

    conjugate = reduce_zeta(quotient.subs(z, z**2))
    product = sp.factor(reduce_zeta(quotient * conjugate))
    assert z not in product.free_symbols
    return sp.factor(quotient), product


def verify_example(d: sp.Expr, u: sp.Rational, pullback: bool) -> None:
    g = sp.degree(d, x)
    dt = d.subs(x, t)
    p = sp.expand(d**2 + u * x)
    q = sp.expand(d**3)

    H = sp.factor(sp.resultant(V - dt**3, U - dt**2 - u * t, t))
    assert sp.Poly(H, U, V).degree(U) == 3 * g
    assert sp.Poly(H, U, V).total_degree() == 3 * g
    assert sp.Poly(H, U, V).coeff_monomial(U ** (3 * g)) == 1
    assert sp.expand(H.subs({U: p, V: q})) == 0

    Hp = sp.factor(sp.diff(H, U).subs({U: p, V: q}))
    Hq = sp.factor(sp.diff(H, V).subs({U: p, V: q}))
    dp = sp.diff(p, x)
    dq = sp.diff(q, x)
    kappa = sp.factor(sp.cancel(Hp / dq))

    assert sp.cancel(Hp - kappa * dq) == 0
    assert sp.cancel(Hq + kappa * dp) == 0
    assert sp.gcd(sp.Poly(dp, x), sp.Poly(dq, x)).degree() == 0

    Kz, product = collision_product(d, u)
    expected = sp.factor(u ** (3 * g - 1) * product / 3)
    assert sp.cancel(kappa - expected) == 0
    assert sp.degree(Kz, x) == 2 * g**2 - g
    assert sp.degree(kappa, x) == 4 * g**2 - 2 * g
    assert sp.gcd(sp.Poly(kappa, x), sp.Poly(d, x)).degree() == 0

    if pullback:
        # The bounded polynomial Bezout normal field from the canonical
        # symplectic-extension note.
        p1 = -4 * sp.diff(d, x) / (3 * u**2)
        q1 = 1 / u - 2 * d * sp.diff(d, x) / u**2
        assert sp.cancel(dp * q1 - dq * p1) == 1

        P = p + y * p1
        Q = q + y * q1
        pulled = sp.Poly(sp.together(H.subs({U: P, V: Q})), y)
        assert pulled.coeff_monomial(1) == 0
        R_at_boundary = sp.factor(pulled.coeff_monomial(y))
        assert sp.cancel(R_at_boundary + kappa) == 0


def verify_surjective_nonfinite_etale_stress() -> None:
    s = sp.symbols("s")
    f = s**3 - 3 * s
    derivative = sp.diff(f, s)
    assert derivative == 3 * (s**2 - 1)

    # The only derivative zeros are the deleted points.  Their two
    # critical values retain an undeleted preimage, so the restriction
    # A1\\{+/-1} -> A1 remains surjective.
    assert sp.factor(f + 2) == (s - 1) ** 2 * (s + 2)
    assert sp.factor(f - 2) == (s + 1) ** 2 * (s - 2)
    assert f.subs(s, -2) == -2
    assert f.subs(s, 2) == 2


verify_example(x + 2, sp.Rational(3), pullback=True)
verify_example(x**2 + x + 1, sp.Rational(2), pullback=True)
verify_example(x**3 + x + 2, sp.Rational(2), pullback=False)
verify_surjective_nonfinite_etale_stress()

print("verified the resultant and primitive-gradient conductor identities")
print("verified the two cube-root factors give the full conductor divisor")
print("verified R(x,0)=-kappa for explicit polynomial normal fields")
print("verified the surjective quasi-finite etale nonfinite stress example")
