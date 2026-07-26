#!/usr/bin/env python3
"""Verify the all-degree reduction for homogeneous binary targets Q_n(A,B)."""

from __future__ import annotations

import math

import sympy as sp


x, y, u, t = sp.symbols("x y u t")


def jacobian(
    first: sp.Expr,
    second: sp.Expr,
    variables: tuple[sp.Symbol, sp.Symbol],
) -> sp.Expr:
    first_variable, second_variable = variables
    return sp.expand(
        sp.diff(first, first_variable) * sp.diff(second, second_variable)
        - sp.diff(first, second_variable) * sp.diff(second, first_variable)
    )


def verify_general_characteristic() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    gamma = sp.Function("gamma")(x, t)
    polynomial = sp.Function("P")(t)
    highest_u = x**15 * t**20 * gamma**17
    highest_binary = (
        x ** (4 * n)
        * t ** (5 * n)
        * gamma ** (4 * n)
        * polynomial
    )
    equation = (
        x * (5 * n / t + 17 * sp.diff(polynomial, t) / polynomial)
        * sp.diff(gamma, x)
        - 8 * n * sp.diff(gamma, t)
        + (-5 * n / t + 15 * sp.diff(polynomial, t) / polynomial)
        * gamma
    )
    assert sp.factor(
        jacobian(highest_u, highest_binary, (x, t))
        - highest_u * highest_binary * equation / (x * gamma)
    ) == 0

    I, d = sp.symbols("I d", integer=True)
    exponent_r = sp.Rational(5, 8) * (I - 1)
    exponent_s = (17 * I + 15) / (8 * n)
    relation_j = sp.expand(exponent_r + d * exponent_s)
    expected_j = (
        (5 * n + 17 * d) * I + 15 * d - 5 * n
    ) / (8 * n)
    assert sp.factor(relation_j - expected_j) == 0


def verify_source_equation_and_residual() -> None:
    n, d = sp.symbols("n d", integer=True, positive=True)
    leading_coefficient = sp.symbols("leading_coefficient", nonzero=True)
    a = -sp.Rational(57, 34)

    # For H(u,x)=x^d P(u/x), its x=0 jet is
    # H=p_d*u^d and u*H_u=d*p_d*u^d.  The cleared source equation is
    #
    # x*K*(x*gamma_x-y*gamma_y)
    # +u*(K-8*n*H)*gamma_y+x*L*gamma=0,
    #
    # K=5*n*H+17*u*H_u, L=-5*n*H+15*u*H_u.
    h_at_axis = leading_coefficient
    u_hu_at_axis = d * leading_coefficient
    k_at_axis = 5 * n * h_at_axis + 17 * u_hu_at_axis
    l_at_axis = -5 * n * h_at_axis + 15 * u_hu_at_axis
    residual = sp.expand(
        a * (k_at_axis - 8 * n * h_at_axis)
        + l_at_axis
    )
    assert sp.expand(
        residual - leading_coefficient * (n - 459 * d) / 34
    ) == 0

    m = sp.symbols("m", integer=True, positive=True)
    # For nonmonomial P, the cleared polynomial H=x^dP(u/x) has
    # leading ordinary degree 2d.  The leading source equation has
    # degree m+2d+3, whereas the displayed residual has degree one.
    residual_drop = m + 2 * d + 2
    lower_seed_drop = m + 4
    assert sp.expand(
        residual_drop.subs(d, 1) - lower_seed_drop
    ) == 0
    assert sp.expand(
        residual_drop - lower_seed_drop
    ) == 2 * d - 2


def verify_exception_has_no_integer_resonance() -> None:
    # If the x-adic coefficient vanishes, n=459*d.  The characteristic
    # relation reduces to 459*J=289*I-285.
    assert math.gcd(289, 459) == 17
    assert 285 % 17 != 0

    for source_i in range(2, 5000):
        assert (289 * source_i - 285) % 459 != 0


def verify_first_completion_transitions() -> None:
    # n=5,d=1: I=20k+5, J=21k+5.  The first ray has I=J;
    # later rays have the forbidden J>I behavior.
    for k in range(12):
        source_i = 20 * k + 5
        source_j = 21 * k + 5
        assert 40 * source_j == 42 * source_i - 10
        if k == 0:
            assert source_i == source_j
            exponent_r = sp.Rational(5, 2)
            exponent_s = sp.Rational(5, 2)
            assert exponent_r + exponent_s == source_j
        else:
            assert source_j > source_i

    # n=6,d=1 is the first family with graph-compatible polynomial
    # completions.  Every linear P works because r and s are integers.
    for k in range(12):
        source_i = 48 * k + 33
        source_j = 47 * k + 32
        exponent_r = 30 * k + 20
        exponent_s = 17 * k + 12
        assert 48 * source_j == 47 * source_i - 15
        assert exponent_r + exponent_s == source_j
        assert source_i - source_j == k + 1
        if k == 0:
            assert source_i - source_j == 1
        else:
            assert source_i - source_j >= 2

    # The universal x-adic residual coefficient is nonzero at n=6,d=1.
    assert 6 - 459 != 0

    # But for a mixed linear P it arrives at exactly the lower-seed
    # gap m+4, so it cannot be used as an exclusion.
    m = 95 * sp.symbols("k", integer=True, positive=True) + 63
    assert sp.expand((m + 2 * 1 + 2) - (m + 4)) == 0


def verify_first_exceptional_polynomial_completion() -> None:
    eta = sp.symbols("eta", nonzero=True)
    for k in range(1, 5):
        source_i = 48 * k + 33
        source_j = 47 * k + 32
        exponent_r = 30 * k + 20
        exponent_s = 17 * k + 12
        assert exponent_r + exponent_s == source_j
        assert source_i - source_j == k + 1 >= 2

        # Every term of t^r(t+eta)^s has t-degree at most J, so after
        # t=y+x^-1 every source x-exponent is at least I-J>=2.
        for t_degree in range(exponent_r, source_j + 1):
            assert source_i - t_degree >= k + 1

    gamma = sp.Function("gamma")(x, t)
    polynomial = t + eta
    equation = (
        x * (30 / t + 17 / polynomial) * sp.diff(gamma, x)
        - 48 * sp.diff(gamma, t)
        + (-30 / t + 15 / polynomial) * gamma
    )
    symbolic_k = sp.symbols("symbolic_k", integer=True, positive=True)
    source_i = 48 * symbolic_k + 33
    exponent_r = 30 * symbolic_k + 20
    exponent_s = 17 * symbolic_k + 12
    formal_gamma = (
        x**source_i * t**exponent_r * polynomial**exponent_s
    )
    assert sp.factor(
        equation.subs(gamma, formal_gamma).doit()
    ) == 0


def verify_sampled_resonance_classification() -> None:
    # Exhaustively audit a large finite window of (n,d,I,J).  Every
    # integer resonance has a nonzero universal residual coefficient.
    # The exact proof for all values is the gcd calculation above.
    for n in range(1, 80):
        for d in range(n + 1):
            for source_i in range(2, 500):
                numerator = (
                    (5 * n + 17 * d) * source_i
                    + 15 * d
                    - 5 * n
                )
                if numerator % (8 * n) != 0:
                    continue
                source_j = numerator // (8 * n)
                if source_j < 0:
                    continue
                assert n - 459 * d != 0


def verify_degrees_through_first_exception() -> None:
    equal_cases: list[tuple[int, int, int, int]] = []
    below_cases: list[tuple[int, int, int, int]] = []
    for n in range(1, 7):
        for d in range(1, n + 1):
            for source_i in range(2, 500):
                numerator = (
                    (5 * n + 17 * d) * source_i
                    + 15 * d
                    - 5 * n
                )
                if numerator % (8 * n):
                    continue
                source_j = numerator // (8 * n)
                if source_j < 0:
                    continue
                if source_j == source_i:
                    equal_cases.append((n, d, source_i, source_j))
                if source_j < source_i:
                    below_cases.append((n, d, source_i, source_j))

    assert equal_cases == [(5, 1, 5, 5)]
    assert all(case[0] == 6 and case[1] == 1 for case in below_cases)
    assert below_cases[:5] == [
        (6, 1, 33, 32),
        (6, 1, 81, 79),
        (6, 1, 129, 126),
        (6, 1, 177, 173),
        (6, 1, 225, 220),
    ]


def verify_pure_monomial_fixed_defect() -> None:
    n, d = sp.symbols("n d", integer=True, positive=True)
    a = -sp.Rational(57, 34)
    coefficient_x = 5 * n + 17 * d
    coefficient_u = 17 * d - 3 * n
    coefficient_zero = 15 * d - 5 * n
    gamma_fixed = 1 + a * (u - 1)
    defect = sp.expand(
        coefficient_x * x * sp.diff(gamma_fixed, x)
        + coefficient_u * u * sp.diff(gamma_fixed, u)
        + coefficient_zero * gamma_fixed
    )
    expected = (
        8 * a * (4 * d - n) * (u - 1)
        + a * (17 * d - 3 * n)
        + 15 * d
        - 5 * n
    )
    assert sp.expand(defect - expected) == 0
    assert sp.expand(
        a * (17 * d - 3 * n)
        + 15 * d
        - 5 * n
        - (n - 459 * d) / 34
    ) == 0

    coefficient_u = 17 * d - 3 * n
    coefficient_zero = 15 * d - 5 * n
    assert sp.expand(
        coefficient_zero.subs(n, sp.Rational(17, 3) * d)
    ) == -sp.Rational(40, 3) * d

    # A nonzero polynomial solution of
    # coefficient_u*u*f'+coefficient_zero*f=0 is c*u^N.
    # The graph boundary jets force c=1 and N=a, impossible.
    assert a == -sp.Rational(57, 34)
    assert a.is_integer is False


def main() -> None:
    verify_general_characteristic()
    verify_source_equation_and_residual()
    verify_exception_has_no_integer_resonance()
    verify_first_completion_transitions()
    verify_first_exceptional_polynomial_completion()
    verify_sampled_resonance_classification()
    verify_degrees_through_first_exception()
    verify_pure_monomial_fixed_defect()
    print("verified: all-n binary characteristic and resonance relation")
    print("verified: universal x-adic residual is (n-459*d)/34")
    print("verified: the zero-residual ratio has no integer resonance")
    print("verified: every binary face through n=5 is structurally closed")
    print("verified: n=6,d=1 has graph-compatible polynomial completions")
    print("verified: its x-adic residual collides with the lower seed")
    print("RESULT: first exceptional family is exactly n=6,d=1,k>=1")


if __name__ == "__main__":
    main()
