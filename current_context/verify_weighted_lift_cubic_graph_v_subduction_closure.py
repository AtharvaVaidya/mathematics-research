#!/usr/bin/env python3
"""Verify the exceptional cubic projected subduction of V exactly."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_weighted_lift_sagbi_after_w_markov_and_next_generators as after_w


u = after_w.u
f_symbol = after_w.f
r = sp.symbols("r", nonzero=True)
d = sp.symbols("d")
a_fixed = -sp.Rational(57, 34)
e = a_fixed - 3 * r - 2 * d
s = 1 - a_fixed + 2 * r + d


def f_power_coefficient(power: int, drop: int) -> sp.Expr:
    """Return [u^(3*power-drop)](r*u^3+d*u^2+e*u+s)^power."""
    result = sp.Integer(0)
    for n3 in range(drop // 3 + 1):
        for n2 in range((drop - 3 * n3) // 2 + 1):
            n1 = drop - 3 * n3 - 2 * n2
            if n1 + n2 + n3 > power:
                continue
            n0 = power - n1 - n2 - n3
            result += (
                sp.factorial(power)
                / (
                    sp.factorial(n0)
                    * sp.factorial(n1)
                    * sp.factorial(n2)
                    * sp.factorial(n3)
                )
                * r**n0
                * d**n1
                * e**n2
                * s**n3
            )
    return sp.expand(result)


def specialized_coefficient(
    polynomial: sp.Poly,
    target_degree: int,
) -> sp.Expr:
    result = sp.Integer(0)
    for (u_degree, f_degree), coefficient in polynomial.terms():
        drop = u_degree + 3 * f_degree - target_degree
        if 0 <= drop <= 3 * f_degree:
            result += coefficient * f_power_coefficient(
                f_degree,
                drop,
            )
    return sp.factor(result)


def monomial(
    generators: list[sp.Poly],
    exponents: tuple[int, ...],
) -> sp.Poly:
    return after_w.monomial(generators, exponents)


def verify_fixed_jets() -> None:
    cubic = r * u**3 + d * u**2 + e * u + s
    assert sp.expand(cubic.subs(u, 1)) == 1
    assert sp.expand(sp.diff(cubic, u).subs(u, 1)) == a_fixed


def projected_factorizations(
    target_degree: int,
) -> list[tuple[int, ...]]:
    """Enumerate all old-generator monomials at (-11,target_degree)."""
    solutions: list[tuple[int, ...]] = []
    # Equation 5 bounds b<=8,a<=7,t<=1,v<=2,w<=1 in the range used.
    for b in range(9):
        for a in range(8):
            for t in range(2):
                for v in range(3):
                    for w in range(2):
                        c = -11 + b + 2 * a + 6 * t + 5 * v + 7 * w
                        if c < 0:
                            continue
                        degree = (
                            3 * c
                            + 17 * b
                            + 18 * a
                            + 82 * t
                            + 71 * v
                            + 85 * w
                        )
                        if degree == target_degree:
                            solutions.append((c, b, a, t, v, w))
    return solutions


def verify_semigroup_table() -> None:
    assert projected_factorizations(139) == [
        (1, 0, 3, 1, 0, 0),
        (0, 5, 3, 0, 0, 0),
    ]
    assert projected_factorizations(138) == []
    assert projected_factorizations(137) == [
        (0, 2, 1, 0, 0, 1),
    ]
    assert projected_factorizations(136) == []
    assert projected_factorizations(135) == [
        (3, 0, 7, 0, 0, 0),
        (0, 1, 2, 1, 0, 0),
    ]
    assert projected_factorizations(133) == []


def verify_symbolic_branching() -> tuple[
    list[sp.Poly],
    sp.Poly,
]:
    generators, coefficients = after_w.build_generators()
    polynomial_v = after_w.build_v(generators, coefficients)
    reducer_139_a = monomial(
        generators,
        (1, 0, 3, 1, 0, 0),
    )
    reducer_139_b = monomial(
        generators,
        (0, 5, 3, 0, 0, 0),
    )

    top_v = specialized_coefficient(polynomial_v, 139)
    coefficient_v = polynomial_v.coeff_monomial(
        u**40 * f_symbol**33
    )
    assert top_v == coefficient_v * r**33

    remainders: list[dict[int, sp.Expr]] = []
    for reducer in (reducer_139_a, reducer_139_b):
        ratio_139 = sp.factor(
            top_v / specialized_coefficient(reducer, 139)
        )
        remainder = {
            degree: sp.factor(
                specialized_coefficient(polynomial_v, degree)
                - ratio_139
                * specialized_coefficient(reducer, degree)
            )
            for degree in range(133, 139)
        }
        assert remainder[138] == coefficient_v * d * r**32
        remainders.append(remainder)

    # The two normalized degree-139 choices agree through degree 136.
    for degree in range(136, 139):
        assert sp.factor(
            remainders[0][degree] - remainders[1][degree]
        ) == 0
    normalized_difference_135 = sp.factor(
        specialized_coefficient(reducer_139_b, 135)
        / specialized_coefficient(reducer_139_b, 139)
        - specialized_coefficient(reducer_139_a, 135)
        / specialized_coefficient(reducer_139_a, 139)
    )
    assert normalized_difference_135 == sp.Rational(
        26245120625,
        33084609408,
    ) / r

    remainder_d0 = {
        degree: sp.factor(value.subs(d, 0))
        for degree, value in remainders[0].items()
    }
    k_137 = -sp.Rational(
        1723813088873291015625,
        129230026381362988475121198684461016956252545836408663083476189883762833805541376,
    )
    assert remainder_d0[137] == (
        k_137
        * r**32
        * (20234250 * r - 750661967)
    )

    reducer_137 = monomial(
        generators,
        (0, 2, 1, 0, 0, 1),
    )
    ratio_137 = sp.factor(
        remainder_d0[137]
        / specialized_coefficient(reducer_137, 137).subs(d, 0)
    )
    coefficient_136 = sp.factor(
        remainder_d0[136]
        - ratio_137
        * specialized_coefficient(reducer_137, 136).subs(d, 0)
    )
    k_136 = sp.Rational(
        646429908327484130859375,
        244291165182160658743140262163442376098776079085838682577459716226394770898944,
    )
    assert coefficient_136 == k_136 * r**32 * (68 * r + 91)
    return generators, polynomial_v


def specialized_polynomial(
    polynomial: sp.Poly,
    fixed_f: sp.Expr,
) -> sp.Poly:
    return sp.Poly(
        polynomial.as_expr().subs(f_symbol, fixed_f),
        u,
    )


def verify_last_stratum(
    generators: list[sp.Poly],
    polynomial_v: sp.Poly,
) -> None:
    fixed_r = -sp.Rational(91, 68)
    fixed_f = sp.expand(
        fixed_r * u**3
        + (a_fixed - 3 * fixed_r) * u
        + (1 - a_fixed + 2 * fixed_r)
    )
    assert fixed_f == (-91 * u**3 + 159 * u) / 68

    specialized_generators = [
        specialized_polynomial(generator, fixed_f)
        for generator in generators
    ]

    def fixed_monomial(exponents: tuple[int, ...]) -> sp.Poly:
        result = sp.Poly(1, u)
        for exponent, generator in zip(
            exponents,
            specialized_generators,
        ):
            if exponent:
                result *= generator**exponent
        return result

    reducers_139 = (
        (1, 0, 3, 1, 0, 0),
        (0, 5, 3, 0, 0, 0),
    )
    reducer_137 = (0, 2, 1, 0, 0, 1)
    reducers_135 = (
        (3, 0, 7, 0, 0, 0),
        (0, 1, 2, 1, 0, 0),
    )
    expected_133 = (
        sp.Integer(3) ** 25
        * sp.Integer(5) ** 8
        * sp.Integer(7) ** 31
        * sp.Integer(13) ** 31
        * 76444077740123
        / (
            sp.Integer(2) ** 127
            * sp.Integer(17) ** 32
            * sp.Integer(23) ** 44
        )
    )

    for reducer_139, reducer_135 in itertools.product(
        reducers_139,
        reducers_135,
    ):
        remainder = specialized_polynomial(polynomial_v, fixed_f)
        for target_degree, exponents in (
            (139, reducer_139),
            (137, reducer_137),
            (135, reducer_135),
        ):
            reducer = fixed_monomial(exponents)
            assert remainder.degree() == target_degree
            assert reducer.degree() == target_degree
            remainder -= remainder.LC() / reducer.LC() * reducer
        assert remainder.degree() == 133
        assert sp.factor(remainder.LC() - expected_133) == 0


def main() -> None:
    verify_fixed_jets()
    verify_semigroup_table()
    generators, polynomial_v = verify_symbolic_branching()
    verify_last_stratum(generators, polynomial_v)
    print("verified: exact fixed-jet cubic graph family")
    print("verified: complete projected semigroup table at the used degrees")
    print("verified: d!=0 stops at the degree-138 gap")
    print("verified: d=0 generically stops at the degree-136 gap")
    print("verified: the sole last stratum stops at the degree-133 gap")
    print("RESULT: V forces a new projected generator for every cubic graph")


if __name__ == "__main__":
    main()
