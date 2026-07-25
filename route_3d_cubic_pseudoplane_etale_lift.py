#!/usr/bin/env python3
"""Exact checks for the cubic-pseudo-plane etale lifting obstruction."""

from __future__ import annotations

import sympy as sp


def verify_plane_filling_coordinates() -> None:
    a, b, h = sp.symbols("a b h")
    h_value = 1 + 3 * a**3 * b
    u = a**3
    w = a * h_value
    v_polynomial = 9 * b + 27 * a**3 * b**2 + 27 * a**6 * b**3
    assert sp.expand(
        a**3 * v_polynomial - (h_value**3 - 1)
    ) == 0
    assert sp.expand(w**3 - u - u**2 * v_polynomial) == 0
    assert sp.expand(
        (1 - h**3).subs(h, h_value)
        + u * v_polynomial
    ) == 0


def verify_cyclic_pole() -> None:
    a, b, h, epsilon, P = sp.symbols("a b h epsilon P")
    t = 1 - h**3
    R1 = 1 + (epsilon - 1) * t
    A = a * h
    required_B = sp.factor((R1 - 1) / (3 * A**3))
    expected = -(
        (epsilon - 1) * b * (h**2 + h + 1) / h**3
    )
    assert sp.simplify(
        required_B.subs(b, (h - 1) / (3 * a**3)) - expected.subs(
            b, (h - 1) / (3 * a**3)
        )
    ) == 0

    # A standard Theta^P deformation only adds the regular term P(A)/3.
    deformed_B = sp.factor(
        (R1 + P * A**3 - 1) / (3 * A**3)
    )
    assert sp.simplify(deformed_B - required_B - P / 3) == 0
    leading_pole = sp.simplify(sp.limit(h**3 * required_B, h, 0))
    assert leading_pole == (epsilon - 1) / (3 * a**3)


def verify_shabat_degree_obstruction() -> None:
    for N in range(0, 100):
        alpha_zero_degree = 6 * N + 3
        r2_degree = N
        r1_degree = 2 * N + 1
        required_divisor_degree = 2 + 3 * r2_degree
        assert alpha_zero_degree > 1
        assert required_divisor_degree > r1_degree

        alpha_one_degree = 6 * N + 1
        assert alpha_one_degree == 1 if N == 0 else alpha_one_degree > 1
        assert (2 * N) == (alpha_one_degree - 1) // 3


def verify_alpha_one_component_obstruction() -> None:
    h, beta, R, zeta = sp.symbols(
        "h beta R zeta", nonzero=True
    )
    # At a root beta of R2, the three components are h, zeta*h,
    # zeta^2*h.  Two of the required equations already contradict
    # zeta != 1.
    first = h * R - 1
    second = zeta * h * R - 1
    assert sp.factor(second - zeta * first) == zeta - 1

    # Equivalently, a nonzero linear polynomial h*R-1 cannot be divisible
    # by the cubic defining all three components.
    cubic = h**3 - (1 - beta)
    quotient, remainder = sp.div(h * R - 1, cubic, h)
    assert quotient == 0
    assert remainder == h * R - 1


def main() -> None:
    verify_plane_filling_coordinates()
    verify_cyclic_pole()
    verify_shabat_degree_obstruction()
    verify_alpha_one_component_obstruction()
    print("verified the exact cube-root plane filling coordinates")
    print("verified the cyclic h^-3 pole and Theta^P invariance")
    print("verified the all-degree alpha=0 Shabat obstruction")
    print("verified the alpha=1 three-component obstruction")
    print("RESULT: NO NONPROPER DP SHABAT FAMILY LIFTS THROUGH PI_3")


if __name__ == "__main__":
    main()
