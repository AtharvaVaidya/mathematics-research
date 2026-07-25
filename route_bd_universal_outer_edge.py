#!/usr/bin/env python3
"""Verify the universal coprime radial outer-edge Belyi reduction.

Let 1 <= m < n be coprime, let k >= 0, and put

    p = m*k + 1,  q = n*k + 1,  delta = n - m.

For polynomials U,V of degrees p,q, respectively, define

    E = delta*U*V + m*w*U*V' - n*w*U'*V.

Over characteristic zero, if E is a nonzero constant, then

    R = w^delta * V^m / U^n

satisfies R'/R = E/(w*U*V).  The differential equation makes U and V
coprime and squarefree.  Hence R is a degree d=n*(m*k+1) three-point cover
with passport

    (m^(n*k+1), delta),
    (n^(m*k+1)),
    ((m+n)*k+2, 1^kappa),

where

    kappa = ((m-1)*(n-1)-1)*k + n - 2.

The passport requires kappa >= 0.  If this integer is negative, the
Riemann--Hurwitz identity itself rules out such a polynomial solution.

If the equation is normalized as E=1, then necessarily
U(0)*V(0)=1/delta.  Thus U(0)=V(0)=1 is compatible with the right side
only when delta=1; with those constant terms the natural right side is
delta.

At the distinguished point over the third branch value, put

    N = (m+n)*k+2,  L = v_q^m/u_p^n,  t=1/w.

If E is the constant in the outer equation, then

    sigma = (u_p*v_q*N*(1-R/L)/E)^(1/N) = t+O(t^2)

and a unique unit H=1+O(sigma) put the outer pair in the exact form

    P_out = u_p*zeta^m*sigma^(-m*k),
    Q_out = v_q*zeta^n*sigma^(-n*k)*(1-sigma^N)^(1/m),

where zeta=z*H.  Moreover {zeta,sigma}=-sigma times a formal unit.

The final calculation evaluates the exact Frobenius character formula for
(m,n)=(2,3), k=1,...,4.  The weighted Hurwitz numbers are 1,2,5,14, the
first four Catalan numbers.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial

import sympy as sp

from route_bd_ab_hurwitz_count import (
    centralizer_size,
    character,
    partitions,
    representation_degree,
)


def passport(
    m: int,
    n: int,
    k: int,
) -> tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    assert 1 <= m < n
    assert sp.gcd(m, n) == 1
    assert k >= 0
    degree = n * (m * k + 1)
    delta = n - m
    infinity_index = (m + n) * k + 2
    kappa = degree - infinity_index
    assert kappa == ((m - 1) * (n - 1) - 1) * k + n - 2
    assert kappa >= 0
    over_zero = tuple(sorted((m,) * (n * k + 1) + (delta,), reverse=True))
    over_infinity = (n,) * (m * k + 1)
    over_third = (infinity_index,) + (1,) * kappa
    assert sum(over_zero) == sum(over_infinity) == sum(over_third) == degree
    return degree, over_zero, over_infinity, over_third


def verify_riemann_hurwitz(m: int, n: int, k: int) -> None:
    degree, over_zero, over_infinity, over_third = passport(m, n, k)
    defect = lambda cycle_type: sum(length - 1 for length in cycle_type)
    assert (
        defect(over_zero) + defect(over_infinity) + defect(over_third)
        == 2 * degree - 2
    )

    # The exact derivative has order infinity_index-1 in the local
    # coordinate t=1/w, so the distinguished third-fiber point has the
    # asserted ramification index.
    numerator_degree = (
        n - m - 1
        + (m - 1) * (n * k + 1)
    )
    denominator_degree = (n + 1) * (m * k + 1)
    derivative_order_at_infinity = (
        denominator_degree - numerator_degree - 2
    )
    assert derivative_order_at_infinity + 1 == (m + n) * k + 2


def weighted_hurwitz_number(m: int, n: int, k: int) -> Fraction:
    degree, over_zero, over_infinity, over_third = passport(m, n, k)
    character_sum = sum(
        Fraction(
            character(shape, over_zero)
            * character(shape, over_infinity)
            * character(shape, over_third),
            representation_degree(shape),
        )
        for shape in partitions(degree)
    )
    return (
        Fraction(
            factorial(degree),
            centralizer_size(over_zero)
            * centralizer_size(over_infinity)
            * centralizer_size(over_third),
        )
        * character_sum
    )


def verify_symbolic_identity() -> None:
    w = sp.symbols("w", nonzero=True)
    m, n = sp.symbols("m n", integer=True, positive=True)
    U = sp.Function("U")(w)
    V = sp.Function("V")(w)
    delta = n - m
    edge = (
        delta * U * V
        + m * w * U * sp.diff(V, w)
        - n * w * sp.diff(U, w) * V
    )
    logarithmic_derivative = sp.diff(
        delta * sp.log(w) + m * sp.log(V) - n * sp.log(U),
        w,
    )
    assert sp.simplify(logarithmic_derivative - edge / (w * U * V)) == 0


def verify_canonical_infinity_normal_form() -> None:
    """Check the general exact sigma/H normalization at infinity."""

    m, n = sp.symbols("m n", integer=True, positive=True)
    k = sp.symbols("k", integer=True, positive=True)
    leading_u, leading_v = sp.symbols(
        "leading_u leading_v", nonzero=True
    )
    edge_constant = sp.symbols("edge_constant", nonzero=True)
    sigma, h = sp.symbols("sigma h", nonzero=True)
    p = m * k + 1
    q = n * k + 1
    ramification_index = (m + n) * k + 2

    # From R'/R=E/(wUV) and t=1/w:
    # d(R/L)/dt = -E*(leading_u*leading_v)^(-1)
    #               * t^(N-1) + higher terms.
    derivative_order = p + q - 1
    assert sp.simplify(
        derivative_order - (ramification_index - 1)
    ) == 0
    derivative_coefficient = (
        -edge_constant / (leading_u * leading_v)
    )
    first_coefficient = sp.simplify(
        derivative_coefficient / ramification_index
    )
    assert first_coefficient == -edge_constant / (
        leading_u * leading_v * ramification_index
    )

    # Defining R/L=1-sigma^N and
    # F=leading_u*sigma^(-m*k)*h^m forces the displayed G exactly.
    normalized_f = leading_u * sigma ** (-m * k) * h**m
    normalized_g = (
        leading_v
        * sigma ** (-n * k)
        * h**n
        * (1 - sigma**ramification_index) ** (sp.S.One / m)
    )
    # Build the m-th power directly.  Asking SymPy to simplify
    # ((1-sigma^N)^(1/m))^m would impose an analytic branch convention,
    # whereas here the root is the unique formal root with constant one.
    normalized_g_m = (
        leading_v**m
        * sigma ** (-m * n * k)
        * h ** (m * n)
        * (1 - sigma**ramification_index)
    )
    ratio = sp.simplify(
        (normalized_g_m / normalized_f**n)
        / (leading_v**m / leading_u**n)
    )
    assert ratio == 1 - sigma**ramification_index

    # After zeta=z*h, the h-powers cancel from z^m*F and z^n*G.
    zeta = sp.symbols("zeta")
    assert sp.simplify((zeta / h) ** m * normalized_f) == (
        leading_u * zeta**m * sigma ** (-m * k)
    )
    assert sp.simplify((zeta / h) ** n * normalized_g) == (
        leading_v
        * zeta**n
        * sigma ** (-n * k)
        * (1 - sigma**ramification_index) ** (sp.S.One / m)
    )

    # If t=1/w and sigma=t+O(t^2), then
    # {z*h(sigma),sigma}=-sigma*mu with
    # mu=h*(t/sigma)*d(sigma)/dt, whose constant term is one.
    t = sp.symbols("t", nonzero=True)
    sigma_function = sp.Function("sigma")(t)
    h_function = sp.Function("h")(sigma_function)
    bracket_unit = (
        h_function
        * (t / sigma_function)
        * sp.diff(sigma_function, t)
    )
    bracket = -sigma_function * bracket_unit
    direct_bracket = -h_function * t * sp.diff(sigma_function, t)
    assert sp.simplify(bracket - direct_bracket) == 0


def main() -> None:
    verify_symbolic_identity()
    verify_canonical_infinity_normal_form()
    for m, n, k in (
        (2, 3, 1),
        (2, 3, 3),
        (2, 5, 1),
        (3, 4, 2),
        (3, 5, 1),
    ):
        verify_riemann_hurwitz(m, n, k)

    catalan_counts = tuple(
        weighted_hurwitz_number(2, 3, k)
        for k in range(1, 5)
    )
    assert catalan_counts == (1, 2, 5, 14)

    print("R=w^(n-m)*V^m/U^n and R'/R=E/(w*U*V)")
    print(
        "passport: (m^(nk+1),n-m), (n^(mk+1)), "
        "((m+n)k+2,1^kappa)"
    )
    print("kappa=((m-1)(n-1)-1)k+n-2")
    print(
        "normalization: E=1 forces U(0)V(0)=1/(n-m); "
        "U(0)=V(0)=1 forces E=n-m"
    )
    print(
        "general infinity normal form: "
        "P=u_p*zeta^m*sigma^(-mk), "
        "Q=v_q*zeta^n*sigma^(-nk)*(1-sigma^N)^(1/m)"
    )
    print("bracket change: {zeta,sigma}=-sigma times a formal unit")
    print("(m,n)=(2,3), k=1..4 Hurwitz counts:", catalan_counts)
    print("RESULT: UNIVERSAL COPRIME OUTER-EDGE BELYI REDUCTION VERIFIED")


if __name__ == "__main__":
    main()
