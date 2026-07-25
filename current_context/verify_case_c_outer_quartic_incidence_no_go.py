#!/usr/bin/env python3
"""Exact checks for the outer-quartic incidence no-go and conditional route."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from current_context.verify_case_c_cap_resonant_star_no_go import (  # noqa: E402
    linear_map_matrix,
    truncated_formal_lift,
)
from route_bd_fbar_obstruction import (  # noqa: E402
    K,
    PRIME,
    outer_coefficients,
)


def symbolic_outer_identities() -> None:
    h = sp.symbols("h", nonzero=True)
    u = sp.Function("U")(h)
    v = sp.Function("V")(h)
    leading = sp.symbols("L", nonzero=True)
    outer = u * v + 2 * h * u * sp.diff(v, h) - 3 * h * sp.diff(u, h) * v
    rational_map = h * v**2 / u**3
    incidence = h * v**2 - leading * u**3

    assert sp.simplify(
        sp.diff(rational_map, h) - v * outer / u**4
    ) == 0
    assert sp.simplify(
        u * sp.diff(incidence, h)
        - 3 * sp.diff(u, h) * incidence
        - v * outer
    ) == 0
    assert sp.simplify(rational_map - leading - incidence / u**3) == 0


def passport_and_conditional_monodromy() -> None:
    degree = 21
    ramification = 10 + 7 * 2 + (17 - 1)
    assert ramification == 2 * degree - 2

    # If deg(E)=d, infinity has ramification index 21-d.
    d = sp.symbols("d", integer=True)
    equation = sp.Eq(10 + 14 + (21 - d - 1), 40)
    assert sp.solve(equation, d) == [4]

    invariant_sizes = {
        fixed + include_long * 17
        for fixed in range(5)
        for include_long in (0, 1)
    }
    assert invariant_sizes == {
        0, 1, 2, 3, 4, 17, 18, 19, 20, 21
    }
    assert 8 not in invariant_sizes
    assert 12 not in invariant_sizes


def signed(value: K) -> int:
    assert not value.c1 and not value.c2
    return value.c0 if value.c0 <= PRIME // 2 else value.c0 - PRIME


def exact_outer_quartic() -> None:
    h = sp.symbols("h")
    primitive = K(26839)
    u, v = outer_coefficients(primitive)
    polynomial_u = sp.Poly(
        sum(signed(coefficient) * h**index for index, coefficient in enumerate(u)),
        h,
        modulus=PRIME,
    )
    polynomial_v = sp.Poly(
        sum(signed(coefficient) * h**index for index, coefficient in enumerate(v)),
        h,
        modulus=PRIME,
    )
    leading = v[-1] ** 2 / u[-1] ** 3
    incidence = sp.Poly(
        h * polynomial_v.as_expr() ** 2
        - signed(leading) * polynomial_u.as_expr() ** 3,
        h,
        modulus=PRIME,
    )
    assert incidence.as_expr() == (
        15441 * h**4
        + 14388 * h**3
        + 3553 * h**2
        - 6746 * h
        - 2249
    )
    assert incidence.degree() == 4
    assert incidence.nth(0) != 0
    assert sp.gcd(incidence, incidence.diff()).degree() == 0
    assert sp.gcd(incidence, polynomial_u).degree() == 0
    assert sp.gcd(incidence, polynomial_v).degree() == 0

    factors = (
        sp.Poly(h + 1900, h, modulus=PRIME),
        sp.Poly(h - 10636, h, modulus=PRIME),
        sp.Poly(h**2 - 8219 * h - 9921, h, modulus=PRIME),
    )
    product = factors[0] * factors[1] * factors[2]
    assert incidence.monic() == product.monic()
    for left_index, left in enumerate(factors):
        for right in factors[left_index + 1 :]:
            assert sp.gcd(left, right).degree() == 0

    # The first-thickening incidence algebra has the expected CRT dimension.
    assert sum(2 * factor.degree() for factor in factors) == 8
    assert (incidence * incidence).degree() == 8


def formal_cap_over_incidence_algebra() -> None:
    u, v, t = sp.symbols("u v t")
    f = v**8 - 1
    g = v**12 + 2 * v
    assert sp.gcd(f, g) == 1
    assert sp.degree(sp.gcd(sp.diff(f, v), sp.diff(g, v)), v) == 0
    assert linear_map_matrix(f, g, v, 8, 12).rank() == 20

    # The calculation is over Q[t], so it remains valid after every
    # characteristic-zero base change, in particular Q[t]/(E).
    x, y = truncated_formal_lift(
        f,
        g,
        u**2 * (t + u * v) ** 2,
        u,
        v,
        8,
        12,
        through_order=5,
    )
    residual = sp.expand(
        sp.diff(x, u) * sp.diff(y, v)
        - sp.diff(x, v) * sp.diff(y, u)
        - u**2 * (t + u * v) ** 2
    )
    for order in range(6):
        assert residual.coeff(u, order) == 0


def main() -> None:
    symbolic_outer_identities()
    passport_and_conditional_monodromy()
    exact_outer_quartic()
    formal_cap_over_incidence_algebra()
    print("verified E is the squarefree residual divisor in R^(-1)(L)")
    print("verified Riemann-Hurwitz forces passport (17,1^4)")
    print("verified no invariant outer-sheet subset has size 8 or 12")
    print("verified the (8,12) formal cap after base change to the incidence algebra")
    print("RESULT: OUTER-QUARTIC VALUATIONS ALONE DO NOT EXCLUDE CASE C")


if __name__ == "__main__":
    main()
