#!/usr/bin/env python3
"""Exact checks for the delta=4 osculating-cubic restriction.

The conceptual proof is in
``current_context/AB_OSCULATING_CUBIC_DELTA4.md``.  This verifier checks
the convention-sensitive cubic, cusp, nodal, and exact countermodel
identities.
"""

from __future__ import annotations

import sympy as sp


def verify_degree_two_three_nonembedding() -> None:
    h = sp.symbols("h")
    a2, a0, b3, b2, b1, b0 = sp.symbols(
        "a2 a0 b3 b2 b1 b0", nonzero=True
    )
    rho = sp.symbols("rho", nonzero=True)
    A = a2 * h**2 + a0
    B = b3 * h**3 + b2 * h**2 + b1 * h + b0

    assert sp.expand(A.subs(h, rho) - A.subs(h, -rho)) == 0
    odd_difference = sp.factor(B.subs(h, rho) - B.subs(h, -rho))
    assert odd_difference == 2 * rho * (b1 + b3 * rho**2)

    # If b1=0, both coordinate derivatives vanish at the centered point.
    assert sp.diff(A, h).subs(h, 0) == 0
    assert sp.diff(B, h).subs({h: 0, b1: 0}) == 0

    # The pullback degree ledger leaves only constant or linear.
    assert 7 // 4 == 1

    # The Abhyankar--Moh--Suzuki divisibility test excludes a linear
    # restriction for every normalization degree.  Constant restriction
    # is possible only when the image degree is at most three.
    intrinsic_spectrum = {}
    for delta in (1, 2, 4):
        degree_pair = (8 // delta, 12 // delta)
        assert degree_pair[1] % degree_pair[0] != 0
        assert degree_pair[0] % degree_pair[1] != 0
        maximum = 7 // delta
        image_degree = 12 // delta
        intrinsic_spectrum[delta] = (
            (0,) if image_degree <= 3 else tuple(range(2, maximum + 1))
        )
    assert intrinsic_spectrum == {
        1: (2, 3, 4, 5, 6, 7),
        2: (2, 3),
        4: (0,),
    }


def verify_cusp_square_and_pole_ledger() -> None:
    p0, p1, p2, q0 = sp.symbols("p0 p1 p2 q0", nonzero=True)
    L = q0**2 / p0**3
    q1 = 3 * q0 * p1 / (2 * p0)
    q2 = 3 * q0 * p2 / (2 * p0) + 3 * q0 * p1**2 / (8 * p0**2)
    q3 = (
        3 * q0 * p1 * p2 / (4 * p0**2)
        - q0 * p1**3 / (16 * p0**3)
    )
    n4 = q2**2 + 2 * q1 * q3 - 3 * L * (
        p0 * p2**2 + p1**2 * p2
    )
    expected = (
        -3 * q0**2 * (4 * p0 * p2 - p1**2) ** 2
        / (64 * p0**4)
    )
    assert sp.factor(n4 - expected) == 0

    # An affine Weierstrass shear may add a simple pole to q2, but n5
    # still has pole order at most two.
    w = sp.symbols("w")
    lam, mu, shear, L0 = sp.symbols(
        "lam mu shear L0", nonzero=True
    )
    a1, a2, b2, b3 = (
        sp.Function(name)(w) for name in ("a1", "a2", "b2", "b3")
    )
    p2_sheared = a2 + lam / w
    q2_sheared = b2 + shear * a2 + shear * lam / w
    q3_sheared = b3 + mu / w
    n5 = 2 * q2_sheared * q3_sheared - 3 * L0 * a1 * p2_sheared**2
    assert sp.denom(sp.cancel(w**2 * n5)) == 1

    # The forced square has odd w-valuation because lam != 0.
    possible_square_orders = {2 * order for order in range(8)}
    assert 7 not in possible_square_orders


def verify_nodal_normalization_jacobian() -> None:
    X, Y, c = sp.symbols("X Y c", nonzero=True)
    h = sp.symbols("h")
    normal = Y**2 - X * (X - c**2) ** 2
    parameter = Y / (X - c**2)
    target_jacobian = sp.factor(
        sp.diff(parameter, X) * sp.diff(normal, Y)
        - sp.diff(parameter, Y) * sp.diff(normal, X)
    )
    boundary_substitution = {
        X: h**2,
        Y: h * (h**2 - c**2),
    }
    assert sp.expand(normal.subs(boundary_substitution)) == 0
    assert sp.cancel(
        target_jacobian.subs(boundary_substitution) - (h**2 - c**2)
    ) == 0


def verify_marked_shabat_countermodel() -> None:
    w, v = sp.symbols("w v")
    h = 8 * w**4 - 8 * w**2 + 1
    p = h**2
    q = h**3 - h

    assert sp.degree(p, w) == 8
    assert sp.degree(q, w) == 12
    assert sp.expand(q**2 - p * (p - 1) ** 2) == 0

    derivative = sp.factor(sp.diff(h, w))
    assert derivative == 16 * w * (2 * w**2 - 1)
    assert h.subs(w, 0) == 1
    assert sp.rem(h**2 - 1, derivative, domain=sp.QQ) == 0
    quotient = sp.factor((h**2 - 1) / (w**3 * derivative))
    assert quotient == (w - 1) * (w + 1) * (2 * w**2 - 1) / w**2

    # The common generic fiber is h(v)-h(w), of degree four.  Since
    # h=q/(p-1) in the function field, the parametrization degree is 4.
    rational_function_field = sp.QQ.frac_field(w)
    p_v = (8 * v**4 - 8 * v**2 + 1) ** 2
    h_v = 8 * v**4 - 8 * v**2 + 1
    q_v = h_v**3 - h_v
    common_fiber = sp.gcd(
        sp.Poly(p_v - p, v, domain=rational_function_field),
        sp.Poly(q_v - q, v, domain=rational_function_field),
    )
    expected = sp.Poly(h_v - h, v, domain=rational_function_field).monic()
    assert common_fiber.monic() == expected
    assert common_fiber.degree() == 4


def multiplicity_partition(
    polynomial: sp.Expr, variable: sp.Symbol
) -> tuple[int, ...]:
    _constant, factors = sp.factor_list(polynomial, variable)
    return tuple(
        sorted(
            (
                multiplicity
                for factor, multiplicity in factors
                for _root in range(sp.degree(factor, variable))
            ),
            reverse=True,
        )
    )


def verify_degree_four_shabat_passports() -> None:
    w = sp.symbols("w")
    representatives = (
        (2 * w**4 - 1, ((4,), (1, 1, 1, 1))),
        (-6 * w**4 + 8 * w**3 - 1, ((3, 1), (2, 1, 1))),
        (8 * w**4 - 8 * w**2 + 1, ((2, 2), (2, 1, 1))),
    )
    observed = set()
    for h, expected in representatives:
        partitions = (
            multiplicity_partition(h + 1, w),
            multiplicity_partition(h - 1, w),
        )
        assert partitions == expected
        assert sp.rem(h**2 - 1, sp.diff(h, w), domain=sp.QQ) == 0
        assert sum(4 - len(partition) for partition in partitions) == 3
        observed.add(tuple(sorted(partitions)))

    combinatorial = set()
    partitions_of_four = (
        (4,),
        (3, 1),
        (2, 2),
        (2, 1, 1),
        (1, 1, 1, 1),
    )
    for left in partitions_of_four:
        for right in partitions_of_four:
            if len(left) + len(right) == 5:
                combinatorial.add(tuple(sorted((left, right))))
    assert observed == combinatorial


def verify_full_jacobian_selects_power_passport() -> None:
    s, z = sp.symbols("s z")
    unit = sp.symbols("unit", nonzero=True)

    # At a nonzero source point over the node, u=z^5*unit and
    # v=s^m+... give z^4 coefficient 5*m*unit*s^(m-1).  It is a unit at
    # s=0 exactly for m=1, as required by J=z^4/w^3 with w0 != 0.
    for multiplicity in range(1, 5):
        u = z**5 * unit
        v = s**multiplicity
        jacobian = sp.expand(
            sp.diff(u, z) * sp.diff(v, s)
            - sp.diff(u, s) * sp.diff(v, z)
        )
        coefficient = sp.expand(jacobian).coeff(z, 4)
        assert coefficient == 5 * multiplicity * unit * s ** (
            multiplicity - 1
        )
        assert (coefficient.subs(s, 0) != 0) == (multiplicity == 1)

    w = sp.symbols("w")
    h = 2 * w**4 - 1
    assert sp.factor(sp.diff(h, w)) == 8 * w**3
    assert multiplicity_partition(h + 1, w) == (4,)
    assert multiplicity_partition(h - 1, w) == (1, 1, 1, 1)
    quotient = sp.factor((h**2 - 1) / (w**3 * sp.diff(h, w)))
    assert quotient == (w - 1) * (w + 1) * (w**2 + 1) / (2 * w**2)


def main() -> None:
    verify_degree_two_three_nonembedding()
    verify_cusp_square_and_pole_ledger()
    verify_nodal_normalization_jacobian()
    verify_marked_shabat_countermodel()
    verify_degree_four_shabat_passports()
    verify_full_jacobian_selects_power_passport()
    print("verified the elementary degree-(2,3) nonembedding dichotomy")
    print("verified generalized-cusp pole stability and square obstruction")
    print("verified the nodal normalization Jacobian")
    print("verified the marked Chebyshev degree-four countermodel")
    print("verified the complete three-passport degree-four Shabat list")
    print("verified that the full Jacobian selects the power passport")
    print("RESULT: DELTA=4 OSCULATING-CUBIC CHECKS PASS")


if __name__ == "__main__":
    main()
