#!/usr/bin/env python3
"""Verify the all-k closure of both second-subduction Newton rays."""

from __future__ import annotations

import sympy as sp

from verify_weighted_lift_first_nonlinear_cusp_subduction import (
    build_maximal_subductions,
    build_seed,
)


x, y, u = sp.symbols("x y u")


def jacobian_xu(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, u)
        - sp.diff(first, u) * sp.diff(second, x)
    )


def verify_weighted_euler_identities() -> None:
    gamma = sp.Function("gamma")(x, u)
    highest_u = x**-5 * u**20 * gamma**17
    highest_b = x**-1 * u**5 * gamma**4
    highest_a = x**-2 * u**6 * gamma**4
    operator_b = (
        5 * x * sp.diff(gamma, x)
        - 3 * u * sp.diff(gamma, u)
        - 5 * gamma
    )
    operator_a = (
        11 * x * sp.diff(gamma, x)
        + 7 * u * sp.diff(gamma, u)
        + 5 * gamma
    )
    assert sp.expand(
        x * jacobian_xu(highest_u, highest_b)
        - highest_u * highest_b * operator_b / (u * gamma)
    ) == 0
    assert sp.expand(
        x * jacobian_xu(highest_u, highest_a)
        - 2
        * highest_u
        * highest_a
        * operator_a
        / (u * gamma)
    ) == 0

    I, J = sp.symbols("I J", integer=True, nonnegative=True)
    source_monomial = x**I * y**J
    # Source-coordinate forms of the two operators.
    expected_b = (
        (5 * I - 5 - 8 * J) * source_monomial
        - 3 * J * x ** (I - 1) * y ** (J - 1)
    )
    expected_a = (
        (11 * I + 5 - 4 * J) * source_monomial
        + 7 * J * x ** (I - 1) * y ** (J - 1)
    )
    # Verify through the substitution u=1+xy and the chain rule
    # x*d/dx|u = x*d/dx|y - xy*d/du.
    operator_b_source = (
        5 * x * sp.diff(source_monomial, x)
        + (5 - 8 * (1 + x * y))
        * sp.diff(source_monomial, y)
        / x
        - 5 * source_monomial
    )
    operator_a_source = (
        11 * x * sp.diff(source_monomial, x)
        + (11 - 4 * (1 + x * y))
        * sp.diff(source_monomial, y)
        / x
        + 5 * source_monomial
    )
    assert sp.simplify(operator_b_source - expected_b) == 0
    assert sp.simplify(operator_a_source - expected_a) == 0


def verify_b_ray() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    source_i = 8 * k + 9
    source_j = 5 * k + 5
    assert sp.expand(5 * source_i - 5 - 8 * source_j) == 0
    assert sp.expand(source_i - source_j) == 3 * k + 4

    # Exact binomial recurrence.
    for sample_k in range(6):
        I = 8 * sample_k + 9
        J = 5 * sample_k + 5
        coefficients = [sp.binomial(J, n) for n in range(J + 1)]
        for n in range(1, J + 1):
            diagonal = 3 * n * coefficients[n]
            inherited = 3 * (J - n + 1) * coefficients[n - 1]
            assert diagonal == inherited
        completed = sp.expand(
            sum(
                coefficients[n] * x ** (I - n) * y ** (J - n)
                for n in range(J + 1)
            )
        )
        expected = sp.expand(
            x ** (I - J) * (1 + x * y) ** J
        )
        assert completed == expected
        assert I - J >= 2

    a = -sp.Rational(57, 34)
    assert -8 * a == sp.Rational(228, 17)
    assert -(5 + 3 * a) == sp.Rational(1, 34)
    n = sp.symbols("n", integer=True, positive=True)
    assert sp.expand(5 * n - 5 - 8 * n) == -3 * n - 5

    m = 13 * k + 12
    defect_degree = 20 * m + 84
    linear_degree = 8 * m + 33
    assert sp.expand(defect_degree - linear_degree) == 12 * m + 51
    assert sp.expand((m + 4) - m) == 4


def verify_a_ray() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    source_i = 4 * k + 1
    source_j = 11 * k + 4
    assert sp.expand(11 * source_i + 5 - 4 * source_j) == 0

    for sample_k in range(1, 7):
        I = 4 * sample_k + 1
        J = 11 * sample_k + 4
        coefficients = [sp.binomial(J, n) for n in range(I)]
        for n in range(1, I):
            diagonal = 7 * n * coefficients[n]
            inherited = 7 * (J - n + 1) * coefficients[n - 1]
            assert diagonal == inherited
        assert coefficients[I - 1] != 0
        assert I - (I - 1) == 1
        assert J - (I - 1) == 7 * sample_k + 4

    m = 15 * k + 3
    assert sp.expand((m + 4) - 8 * k) == 7 * k + 7
    a_obstruction_degree = 21 * m + 85 - 8 * k
    linear_degree = 8 * m + 33
    assert sp.expand(
        a_obstruction_degree - linear_degree
    ) == 187 * k + 91


def verify_exact_seed_gap() -> None:
    p, q = build_seed()
    _, second_numerator, _, _ = build_maximal_subductions(p, q)
    poly = sp.Poly(second_numerator, sp.symbols("w"), sp.symbols("gamma"))
    # build_maximal_subductions uses symbols with these names, and SymPy
    # identifies them structurally.
    seed_w, seed_gamma = poly.gens
    assert poly.coeff_monomial(seed_w**20 * seed_gamma**2) != 0
    assert poly.coeff_monomial(seed_w**19 * seed_gamma**2) != 0

    m = sp.symbols("m", integer=True, positive=True)
    def graph_weight(monomial: tuple[int, int]) -> sp.Expr:
        w_power, gamma_power = monomial
        return sp.expand(
            w_power * (m + 4)
            + (gamma_power - 5) * (m + 2)
            - 5
        )

    top_monomial = (20, 2)
    next_monomial = (19, 2)
    top_weight = graph_weight(top_monomial)
    next_weight = graph_weight(next_monomial)
    assert sp.expand(top_weight - next_weight) == m + 4

    # Audit the full 77-term support, not only the two displayed terms:
    # for every m>=1 the two monomials above are uniquely first and second.
    support = [
        monomial
        for monomial, coefficient in poly.terms()
        if coefficient != 0
    ]
    for reference, excluded in (
        (top_monomial, {top_monomial}),
        (next_monomial, {top_monomial, next_monomial}),
    ):
        for monomial in support:
            if monomial in excluded:
                continue
            difference = sp.Poly(
                graph_weight(reference) - graph_weight(monomial),
                m,
            )
            assert difference.coeff_monomial(m) >= 0
            assert difference.eval(1) > 0


def main() -> None:
    verify_weighted_euler_identities()
    verify_b_ray()
    verify_a_ray()
    verify_exact_seed_gap()
    print("verified: exact legacy B- and A-pivot top-Euler operators")
    print("verified: B-ray top model (not the full boundary equation)")
    print("verified: A-ray requires a forbidden x^1 graph contribution")
    print("verified: the A-ray defect precedes every lower seed sector")
    print("RESULT: use the final binary verifier for the corrected B-ray proof")


if __name__ == "__main__":
    main()
