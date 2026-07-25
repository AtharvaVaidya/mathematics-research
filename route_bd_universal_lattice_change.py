#!/usr/bin/env python3
"""Verify the formal Laurent-jet lattice determinant formulas.

Let sigma=a*t+O(t^2), H=h+O(sigma), with a and h units.  For a contiguous
integer interval I=[r,s], project

    H(sigma)^e * sum_{j in I} c_j*t(sigma)^(-j)

to the Laurent window spanned by sigma^(-j), j in I.  In bases ordered by
increasing j, its matrix is upper triangular with diagonal

    (a^j*h^e)_{j in I}.

Consequently its determinant is

    a^(sum_{j in I}j) * h^(e*|I|).

This is the exact local lattice change for a radial P-layer with e=d-m,
and for a radial Q-layer with e=d-n.  It applies to every coprime outer
degree pair (m,n), not only (2,3).

For the (2,3) weight-at-most-eight prefix and k>=2, the product of all
source-layer determinants is

    a^(52*k^2+113*k+7) * h^(76*k-32).

If the output bracket unit is absorbed as well, the product of the target
jet determinants is

    a^(100*k^2+125*k+28) * h^(-20*k-32).

In the canonical normalization sigma=t+O(t^2), H=1+O(sigma), both are one.
Thus these local changes introduce no discriminant or resultant divisor.

The verifier also records the obstruction to stopping at the associated
graded.  If one replaces the transformed lattices by their monomial
windows and keeps only the leading monomials sigma^(-2k), sigma^(-3k) of
the canonical (2,3) outer pair, the kernel profiles at d=1,...,8 are

    k=1: 5,5,4,3,2,1,0,0
    k=2: 7,7,6,5,4,3,2,1
    k=3: 9,9,8,7,6,5,4,3.

These differ from the exact profile 2,2,2,1,0,... .  Hence the obvious
valuation filtration is not strict; its extension data cannot be discarded.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class Interval:
    lower: sp.Expr
    upper: sp.Expr

    @property
    def length(self) -> sp.Expr:
        return sp.expand(self.upper - self.lower + 1)

    @property
    def exponent_sum(self) -> sp.Expr:
        return sp.expand(
            (self.lower + self.upper) * self.length / 2
        )


def radial_support_interval(
    outer_degree: int,
    vertical_bound: sp.Expr,
    deficit: int,
) -> Interval:
    """Return the w-exponent interval for the deficit-d coefficient."""

    radial_degree = outer_degree - deficit
    if radial_degree > 0:
        return Interval(
            sp.Integer(0),
            sp.expand(vertical_bound - radial_degree),
        )
    if radial_degree == 0:
        # The bracket-invisible additive constant is removed.
        return Interval(sp.Integer(1), vertical_bound)
    return Interval(sp.Integer(-radial_degree), vertical_bound)


def determinant_exponents(interval: Interval, h_power: int) -> tuple[sp.Expr, sp.Expr]:
    """Return exponents of (a,h) in the triangular jet determinant."""

    return interval.exponent_sum, sp.expand(h_power * interval.length)


def verify_symbolic_triangular_matrix() -> None:
    """Expand a generic example, including negative H powers."""

    sigma = sp.symbols("sigma")
    a, h = sp.symbols("a h", nonzero=True)
    c1, c2, h1, h2 = sp.symbols("c1 c2 h1 h2")
    t = sigma / a * (1 + c1 * sigma + c2 * sigma**2)
    unit = h * (1 + h1 * sigma + h2 * sigma**2)

    for lower, upper, power in ((-2, 3, -3), (0, 5, 2), (2, 7, 0)):
        indices = tuple(range(lower, upper + 1))
        matrix = sp.zeros(len(indices))
        for column, j in enumerate(indices):
            expression = sp.series(
                unit**power * t ** (-j),
                sigma,
                0,
                upper - lower + 3,
            ).removeO().expand()
            for row, row_j in enumerate(indices):
                matrix[row, column] = expression.coeff(
                    sigma, -row_j
                )
        assert all(
            matrix[row, column] == 0
            for row in range(len(indices))
            for column in range(len(indices))
            if row > column
        )
        expected_diagonal = [
            sp.simplify(a**j * h**power) for j in indices
        ]
        assert [
            sp.simplify(matrix[index, index])
            for index in range(len(indices))
        ] == expected_diagonal
        expected_determinant = (
            a ** sum(indices) * h ** (power * len(indices))
        )
        assert sp.simplify(matrix.det() - expected_determinant) == 0


def verify_kummer_connection_identity() -> None:
    """Check the exact logarithmic-connection presentation of L_d."""

    w = sp.symbols("w", nonzero=True)
    m, n, deficit = sp.symbols(
        "m n deficit", integer=True, positive=True
    )
    f = sp.Function("F")(w)
    g = sp.Function("G")(w)
    a = sp.Function("A")(w)
    b = sp.Function("B")(w)
    c = m + n - deficit
    original = (
        (m - deficit) * a * sp.diff(g, w)
        - n * sp.diff(a, w) * g
        + m * f * sp.diff(b, w)
        - (n - deficit) * sp.diff(f, w) * b
    )
    x = a * g
    y = b * f
    connection_form = (
        -n
        * (
            sp.diff(x, w)
            - (c / n) * x * sp.diff(g, w) / g
        )
        + m
        * (
            sp.diff(y, w)
            - (c / m) * y * sp.diff(f, w) / f
        )
    )
    assert sp.simplify(original - connection_form) == 0


def verify_general_support_formula() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    m, n = 3, 5
    p_bound = m * (k + 1)
    q_bound = n * (k + 1)

    expected_p = {
        1: Interval(0, m * k + 1),
        2: Interval(0, m * k + 2),
        3: Interval(1, m * (k + 1)),
        4: Interval(1, m * (k + 1)),
    }
    expected_q = {
        1: Interval(0, n * k + 1),
        4: Interval(0, n * k + 4),
        5: Interval(1, n * (k + 1)),
        6: Interval(1, n * (k + 1)),
    }
    for deficit, expected in expected_p.items():
        assert radial_support_interval(
            m, p_bound, deficit
        ) == expected
    for deficit, expected in expected_q.items():
        assert radial_support_interval(
            n, q_bound, deficit
        ) == expected


def verify_23_prefix_determinants() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    p_bound = 2 * (k + 1)
    q_bound = 3 * (k + 1)
    source_a = sp.Integer(0)
    source_h = sp.Integer(0)

    p_intervals: dict[int, Interval] = {}
    q_intervals: dict[int, Interval] = {}
    for deficit in range(1, 9):
        p_interval = radial_support_interval(2, p_bound, deficit)
        q_interval = radial_support_interval(3, q_bound, deficit)
        p_intervals[deficit] = p_interval
        q_intervals[deficit] = q_interval
        p_a, p_h = determinant_exponents(
            p_interval, deficit - 2
        )
        q_a, q_h = determinant_exponents(
            q_interval, deficit - 3
        )
        source_a += p_a + q_a
        source_h += p_h + q_h

    assert sp.expand(source_a) == 52 * k**2 + 113 * k + 7
    assert sp.expand(source_h) == 76 * k - 32

    # The ambient output interval is the hull of
    # J_P+[-1,3k] and J_Q+[-1,2k].  The output radial degree is 4-d.
    # Absorbing {zeta,sigma}=-sigma*mu multiplies the target change by
    # mu^(-1), whose constant term is h^(-1).
    target_a = sp.Integer(0)
    target_h = sp.Integer(0)
    for deficit in range(1, 9):
        p_interval = p_intervals[deficit]
        q_interval = q_intervals[deficit]
        output = Interval(
            sp.Min(p_interval.lower - 1, q_interval.lower - 1),
            sp.Max(
                p_interval.upper + 3 * k,
                q_interval.upper + 2 * k,
            ),
        )
        # SymPy does not simplify Min/Max from the piecewise support
        # formulas, so compare with the elementary closed intervals.
        expected_outputs = {
            1: Interval(-1, 5 * k + 1),
            2: Interval(-1, 5 * k + 2),
            3: Interval(0, 5 * k + 3),
            4: Interval(0, 5 * k + 3),
            5: Interval(1, 5 * k + 3),
            6: Interval(2, 5 * k + 3),
            7: Interval(3, 5 * k + 3),
            8: Interval(4, 5 * k + 3),
        }
        expected = expected_outputs[deficit]
        assert sp.simplify(output.lower - expected.lower) == 0
        assert sp.simplify(output.upper - expected.upper) == 0
        output_a, output_h = determinant_exponents(
            expected, deficit - 5
        )
        target_a += output_a
        target_h += output_h

    assert sp.expand(target_a) == 100 * k**2 + 125 * k + 28
    assert sp.expand(target_h) == -20 * k - 32


def naive_associated_graded_profile(k: int) -> tuple[int, ...]:
    """Kernel dimensions after the invalid monomial-window replacement."""

    p_bound = 2 * (k + 1)
    q_bound = 3 * (k + 1)
    kernels: list[int] = []
    for deficit in range(1, 9):
        p_interval = radial_support_interval(2, p_bound, deficit)
        q_interval = radial_support_interval(3, q_bound, deficit)
        columns: list[tuple[int, int]] = []
        p_degree = 2 - deficit
        q_degree = 3 - deficit
        for exponent in range(
            int(p_interval.lower), int(p_interval.upper) + 1
        ):
            columns.append(
                (
                    exponent + 3 * k,
                    3 * (exponent - p_degree * k),
                )
            )
        for exponent in range(
            int(q_interval.lower), int(q_interval.upper) + 1
        ):
            columns.append(
                (
                    exponent + 2 * k,
                    2 * (q_degree * k - exponent),
                )
            )
        rank = len(
            {
                row
                for row, coefficient in columns
                if coefficient != 0
            }
        )
        kernels.append(len(columns) - rank)
    return tuple(kernels)


def verify_non_strict_associated_graded() -> None:
    expected = {
        1: (5, 5, 4, 3, 2, 1, 0, 0),
        2: (7, 7, 6, 5, 4, 3, 2, 1),
        3: (9, 9, 8, 7, 6, 5, 4, 3),
    }
    for k, profile in expected.items():
        assert naive_associated_graded_profile(k) == profile
        assert profile[:4] != (2, 2, 2, 1)


def main() -> None:
    verify_symbolic_triangular_matrix()
    verify_kummer_connection_identity()
    verify_general_support_formula()
    verify_23_prefix_determinants()
    verify_non_strict_associated_graded()
    print(
        "general layer determinant: "
        "a^(sum_{j in I}j)*h^(layer_power*|I|)"
    )
    print(
        "(2,3), d<=8 source determinant: "
        "a^(52k^2+113k+7)*h^(76k-32)"
    )
    print(
        "(2,3), d<=8 target determinant: "
        "a^(100k^2+125k+28)*h^(-20k-32)"
    )
    print("linear layers are sums of two finite-monodromy Kummer connections")
    print("canonical normalization a=h=1: all jet changes are unipotent")
    print(
        "naive monomial associated graded has the wrong kernel profile: "
        "the valuation filtration is not strict"
    )
    print("RESULT: FORMAL LAURENT-JET LATTICE DETERMINANTS VERIFIED")


if __name__ == "__main__":
    main()
