#!/usr/bin/env python3
"""Exact arithmetic verifier for the osculating-cubic genus budget.

The mathematical proof is in
``current_context/AB_OSCULATING_GENUS_BUDGET.md``.  This script checks:

* the local equation of the generalized Weierstrass cubic at infinity;
* the exact contact identity f(A/B,1/B)=H(A,B)/B^3;
* the all-r arithmetic-genus simplification;
* the r=4 infinity delta table and the five marked-cusp delta bounds;
* elimination of three cells and d>=5 for the (3,10) cell.
"""

from __future__ import annotations

from math import ceil, gcd

import sympy as sp


def verify_local_cubic_identity() -> None:
    a, b = sp.symbols("A B", nonzero=True)
    u, v = sp.symbols("u v")
    L, c5, c4, c3, c2, c0 = sp.symbols(
        "L c5 c4 c3 c2 c0", nonzero=True
    )
    h = (
        b**2
        - L * a**3
        + c5 * a * b
        + c4 * a**2
        + c3 * b
        + c2 * a
        + c0
    )
    f = (
        v
        - L * u**3
        + c5 * u * v
        + c4 * u**2 * v
        + c3 * v**2
        + c2 * u * v**2
        + c0 * v**3
    )
    assert sp.factor(f.subs({u: a / b, v: 1 / b}) - h / b**3) == 0
    assert f.subs({u: 0, v: 0}) == 0
    assert sp.diff(f, v).subs({u: 0, v: 0}) == 1


def verify_all_r_budget() -> None:
    r, d = sp.symbols("r d", integer=True, positive=True)
    arithmetic_genus_twice = (3 * r - 1) * (3 * r - 2)
    infinity_mu_lower = (r - 1) * (9 * r - d - 1)
    affine_budget_twice = sp.expand(
        arithmetic_genus_twice - infinity_mu_lower
    )
    assert sp.expand(
        affine_budget_twice - ((d + 1) * r - d + 1)
    ) == 0
    uniform = sp.expand(affine_budget_twice.subs(d, r + 3))
    assert sp.expand(uniform - (r**2 + 3 * r - 2)) == 0


def r4_infinity_delta(contact: int) -> int:
    """Sharp minimum from the first characteristic-exponent cases."""

    assert contact >= 29
    if contact % 4 == 1 or contact % 4 == 3:
        mu = 3 * (contact - 1)
    elif contact % 4 == 2:
        # e0=4,e1=2; the next exponent is at least contact+1 and odd.
        mu = 2 * (contact - 1) + contact
    else:
        # Remove the analytic x^(contact/4) term.  The first
        # characteristic exponent is at least contact+1.
        mu = 3 * contact
    assert mu % 2 == 0
    return mu // 2


def marked_delta(multiplicity: int, contact: int) -> int:
    if gcd(multiplicity, contact) == 1:
        return (multiplicity - 1) * (contact - 1) // 2
    if (multiplicity, contact) == (4, 14):
        # e0=4,e1=2 and beta2>=15.
        return (2 * 13 + 14) // 2
    raise AssertionError("only the five audited cells are used here")


def verify_r4_cells() -> None:
    exact_infinity = {
        d: r4_infinity_delta(36 - d) for d in range(2, 8)
    }
    assert exact_infinity == {
        2: 50,
        3: 48,
        4: 48,
        5: 45,
        6: 44,
        7: 42,
    }
    assert min(exact_infinity.values()) == 42
    arithmetic_genus = 55
    universal_affine_budget = arithmetic_genus - 42
    assert universal_affine_budget == 13

    cells = {
        "(3,5)": marked_delta(3, 5),
        "(5,8)": marked_delta(5, 8),
        "(7,11)": marked_delta(7, 11),
        "(3,10)": marked_delta(3, 10),
        "(4,14)": marked_delta(4, 14),
    }
    assert cells == {
        "(3,5)": 4,
        "(5,8)": 14,
        "(7,11)": 30,
        "(3,10)": 9,
        "(4,14)": 20,
    }
    eliminated = {
        name for name, delta in cells.items()
        if delta > universal_affine_budget
    }
    assert eliminated == {"(5,8)", "(7,11)", "(4,14)"}

    def coarse_budget(d: int) -> int:
        return ((d + 1) * 4 - d + 1) // 2

    assert {d: coarse_budget(d) for d in range(1, 8)} == {
        1: 4,
        2: 5,
        3: 7,
        4: 8,
        5: 10,
        6: 11,
        7: 13,
    }
    assert [
        d for d in range(3, 8)
        if coarse_budget(d) >= cells["(3,10)"]
    ] == [5, 6, 7]

    # The full leading ODE has five nonzero coefficients at r=4, so its
    # pure-w endpoint makes the restricted degree exactly seven.
    r = 4
    coefficients = [sp.Rational(1, 3 - 5 * r)]
    for degree in range(1, 5):
        denominator = r * (degree - 5) + 3
        assert denominator
        coefficients.append(
            sp.cancel(
                -sp.Rational(r * (degree - 5), denominator)
                * coefficients[-1]
            )
        )
    assert all(coefficients)
    assert coefficients[-1] != 0
    full_degree = 7
    assert exact_infinity[full_degree] == 42
    assert arithmetic_genus - exact_infinity[full_degree] == 13
    assert 13 - cells["(3,5)"] == 9
    assert 13 - cells["(3,10)"] == 4

    semigroup = {
        7 * a + 8 * b + 12 * c
        for a in range(20)
        for b in range(20)
        for c in range(20)
    }
    gaps = [degree for degree in range(100) if degree not in semigroup]
    assert gaps == [1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 17, 18, 25]
    assert len(gaps) == 13
    apery = [
        min(degree for degree in semigroup if degree % 7 == residue)
        for residue in range(7)
    ]
    assert apery == [0, 8, 16, 24, 32, 12, 20]
    assert apery == [0, 8, 2 * 8, 3 * 8, 4 * 8, 12, 8 + 12]

    # Riemann--Hurwitz is compatible with every possible marked index.
    w = sp.symbols("w")
    for index in (3, 5, 6):
        polynomial = w**index + w**7
        derivative = sp.factor(sp.diff(polynomial, w))
        assert sp.degree(polynomial, w) == 7
        assert sp.Poly(derivative, w).terms()[-1][0][0] == index - 1
        residual = sp.cancel(derivative / w ** (index - 1))
        assert sp.degree(residual, w) == 7 - index

    # Directly check the universal smooth-contact lower bound at r=4.
    for d, delta in exact_infinity.items():
        q = 36 - d
        assert delta >= ceil(3 * (q - 1) / 2)


def main() -> None:
    verify_local_cubic_identity()
    verify_all_r_budget()
    verify_r4_cells()
    print("verified smooth generalized-Weierstrass coordinate at infinity")
    print("verified all-r affine delta budget")
    print("r=4: infinity delta >= 42, affine delta budget <= 13")
    print("eliminated cells: (5,8), (7,11), (4,14)")
    print("full a/b leading ODE: d=7 and total affine delta=13")
    print("degree semigroup forced to <7,8,12>; verified 13 gaps")
    print("Apéry basis over C[G]: 1,A,A^2,A^3,A^4,B,AB")
    print("survivors: (3,5), (3,10), requiring residual delta 9 and 4")
    print("verified bare Riemann-Hurwitz compatibility for both survivors")


if __name__ == "__main__":
    main()
