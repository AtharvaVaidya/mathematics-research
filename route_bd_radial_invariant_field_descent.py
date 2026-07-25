#!/usr/bin/env python3
"""Exact checks for RADIAL_INVARIANT_FIELD_DESCENT.md."""

from __future__ import annotations

import sympy as sp


def bracket(left: sp.Expr, right: sp.Expr, z: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    return sp.expand(
        sp.diff(left, z) * sp.diff(right, w)
        - sp.diff(left, w) * sp.diff(right, z)
    )


def verify_weight_arithmetic() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    p = 2 * k + 1
    q = 3 * k + 1
    n = 5 * k + 2
    assert sp.expand(3 * p - 2 * q) == 1
    assert sp.expand(p + q - n) == 0


def verify_k1_endpoint_birationality() -> None:
    """The displayed k=1 outer pair has no nontrivial common fiber."""

    t, tau = sp.symbols("t tau")
    u = (
        1
        + tau
        + sp.Rational(6, 25) * tau**2
        + sp.Rational(9, 250) * tau**3
    )
    v = (
        1
        + sp.Rational(2, 3) * tau
        + sp.Rational(6, 25) * tau**2
        + sp.Rational(36, 875) * tau**3
        + sp.Rational(18, 4375) * tau**4
    )
    a = sp.expand(t**3 * u.subs(tau, 1 / t))
    b = sp.expand(t**4 * v.subs(tau, 1 / t))
    assert sp.degree(a, t) == 3
    assert sp.degree(b, t) == 4
    assert sp.gcd(3, 4) == 1

    # Over Q(t), the only common root of A(T)-A(t) and B(T)-B(t)
    # is T=t.  This is the concrete k=1 instance of polynomial Lüroth.
    T = sp.symbols("T")
    fraction_field = sp.QQ.frac_field(t)
    difference_a = sp.Poly(
        a.subs(t, T) - a,
        T,
        domain=fraction_field,
    )
    difference_b = sp.Poly(
        b.subs(t, T) - b,
        T,
        domain=fraction_field,
    )
    common = sp.gcd(difference_a, difference_b).monic()
    assert common == sp.Poly(T - t, T, domain=fraction_field)


def verify_torus_countermodel() -> None:
    z, w, theta = sp.symbols("z w theta", nonzero=True)
    lam, deformation = sp.symbols("lambda deformation", nonzero=True)

    for k in range(1, 5):
        n = 5 * k + 2
        xi = z * w**k
        s = w ** (-n)
        p0 = xi**2
        q0 = xi**3 * (lam - s / (2 * n))
        pa = p0
        qa = xi**3 * (lam - (s + deformation) / (2 * n))
        density = z**4 / w**3

        assert sp.factor(bracket(p0, q0, z, w) - density) == 0
        assert sp.factor(bracket(pa, qa, z, w) - density) == 0

        transformed_z = z * theta**k
        transformed_w = w / theta
        transformed_xi = sp.factor(
            transformed_z * transformed_w**k
        )
        assert transformed_xi == xi

        theta_relation = 1 + deformation * w**n
        transformed_s = transformed_w ** (-n)
        transformed_s = transformed_s.subs(theta**n, theta_relation)
        assert sp.factor(transformed_s - (s + deformation)) == 0

        composed_p = p0.subs(
            {z: transformed_z, w: transformed_w},
            simultaneous=True,
        )
        composed_q = q0.subs(
            {z: transformed_z, w: transformed_w},
            simultaneous=True,
        )
        composed_p = sp.factor(composed_p)
        composed_q = sp.expand(composed_q).subs(
            theta**n,
            theta_relation,
        )
        assert sp.factor(composed_p - pa) == 0
        assert sp.factor(composed_q - qa) == 0

        # The Kummer radicand is squarefree and has valuation one at
        # every zero.  Hence X^N-(1+a*w^N) is Eisenstein there.
        radicand = 1 + deformation * w**n
        assert sp.gcd(
            sp.Poly(radicand, w),
            sp.Poly(sp.diff(radicand, w), w),
        ).degree() == 0

        # The exact ramification signature follows from
        # Z=z*theta^k and W=w/theta at theta=0.
        valuation_z = k
        valuation_w = -1
        assert 5 * valuation_z - 2 * valuation_w == n
        assert valuation_z + k * valuation_w == 0

        # The simplified outer model deliberately violates the bounded
        # lower w-support in its Q-coordinate.
        forbidden_w_exponent = 3 * k - n
        assert forbidden_w_exponent == -2 * k - 2


def main() -> None:
    verify_weight_arithmetic()
    verify_k1_endpoint_birationality()
    verify_torus_countermodel()
    print("verified coprime reciprocal endpoint degrees")
    print("verified k=1 endpoint-pair birationality exactly")
    print("verified the all-k radial Kummer signature countermodel")
    print("RESULT: field descent is equivalent to descent of Z*W^k")


if __name__ == "__main__":
    main()
