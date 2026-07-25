#!/usr/bin/env python3
"""Exact Hurwitz count for the outer a/b differential equation.

For

    U*V + 2*w*U*V' - 3*w*U'*V = 1,
    deg(U)=7, deg(V)=10, U(0)=V(0)=1,

the rational function R=w*V**2/U**3 satisfies R'=V/U**4.  Coprimality
and the differential equation make the roots of U and V simple.  If
lambda is the ratio of the leading coefficients, then

    w*V**2-lambda*U**3

has degree four: a smaller degree would violate Riemann--Hurwitz.  Thus
the three branch partitions are

    (2**10, 1), (3**7), (17, 1**4).

This verifier evaluates the Frobenius character formula by the
Murnaghan--Nakayama rule.  It gives weighted Hurwitz number five.
Every triple is transitive, and its automorphism group is trivial, for
the elementary reasons printed by ``main``.  Hence there are exactly five
normalized complex outer maps, before imposing any lower a/b equations.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from math import factorial


Partition = tuple[int, ...]


def partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    maximum = total if maximum is None else min(total, maximum)
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            yield (first, *tail)


@cache
def subpartitions_of_size(shape: Partition, total: int) -> tuple[Partition, ...]:
    answers: list[Partition] = []

    def visit(row: int, previous: int, remaining: int, parts: list[int]) -> None:
        if row == len(shape):
            if remaining == 0:
                while parts and parts[-1] == 0:
                    parts = parts[:-1]
                answers.append(tuple(parts))
            return
        for length in range(min(previous, shape[row], remaining), -1, -1):
            visit(row + 1, length, remaining - length, [*parts, length])

    visit(0, sum(shape), total, [])
    return tuple(answers)


@cache
def rim_hooks(shape: Partition, size: int) -> tuple[tuple[Partition, int], ...]:
    """Return removable border strips and their Murnaghan--Nakayama signs."""

    if size > sum(shape):
        return ()
    answers: list[tuple[Partition, int]] = []
    for remainder in subpartitions_of_size(shape, sum(shape) - size):
        cells: set[tuple[int, int]] = set()
        for row, length in enumerate(shape, start=1):
            retained = remainder[row - 1] if row <= len(remainder) else 0
            cells.update((row, column) for column in range(retained + 1, length + 1))
        if not cells:
            continue

        seen = {next(iter(cells))}
        frontier = list(seen)
        while frontier:
            row, column = frontier.pop()
            for neighbor in (
                (row - 1, column),
                (row + 1, column),
                (row, column - 1),
                (row, column + 1),
            ):
                if neighbor in cells and neighbor not in seen:
                    seen.add(neighbor)
                    frontier.append(neighbor)
        if seen != cells:
            continue

        has_square = any(
            (row + 1, column) in cells
            and (row, column + 1) in cells
            and (row + 1, column + 1) in cells
            for row, column in cells
        )
        if has_square:
            continue

        occupied_rows = {row for row, _column in cells}
        height = max(occupied_rows) - min(occupied_rows) + 1
        answers.append((remainder, (-1) ** (height - 1)))
    return tuple(answers)


@cache
def character(shape: Partition, cycle_type: Partition) -> int:
    if not cycle_type:
        return int(not shape)
    return sum(
        sign * character(remainder, cycle_type[1:])
        for remainder, sign in rim_hooks(shape, cycle_type[0])
    )


def representation_degree(shape: Partition) -> int:
    hook_product = 1
    for row, length in enumerate(shape):
        for column in range(length):
            below = sum(other_length > column for other_length in shape[row + 1 :])
            hook_product *= length - column + below
    return factorial(sum(shape)) // hook_product


def centralizer_size(cycle_type: Partition) -> int:
    answer = 1
    for length, multiplicity in Counter(cycle_type).items():
        answer *= length**multiplicity * factorial(multiplicity)
    return answer


def hurwitz_number() -> tuple[Fraction, Fraction, int]:
    degree = 21
    over_zero = (2,) * 10 + (1,)
    over_infinity = (3,) * 7
    over_third_value = (17,) + (1,) * 4

    character_sum = sum(
        Fraction(
            character(shape, over_zero)
            * character(shape, over_infinity)
            * character(shape, over_third_value),
            representation_degree(shape),
        )
        for shape in partitions(degree)
    )
    weighted_count = (
        Fraction(
            factorial(degree),
            centralizer_size(over_zero)
            * centralizer_size(over_infinity)
            * centralizer_size(over_third_value),
        )
        * character_sum
    )
    nonzero_terms = sum(
        character(shape, over_zero)
        * character(shape, over_infinity)
        * character(shape, over_third_value)
        != 0
        for shape in partitions(degree)
    )
    return character_sum, weighted_count, nonzero_terms


def verify_character_table_checks() -> None:
    """Independent orthogonality and hook-dimension checks for the recursion."""

    degree = 21
    shapes = tuple(partitions(degree))
    identity = (1,) * degree
    cycle_types = (
        (2,) * 10 + (1,),
        (3,) * 7,
        (17,) + (1,) * 4,
    )
    for shape in shapes:
        assert character(shape, identity) == representation_degree(shape)
    for cycle_type in cycle_types:
        assert sum(character(shape, cycle_type) ** 2 for shape in shapes) == (
            centralizer_size(cycle_type)
        )


def main() -> None:
    verify_character_table_checks()
    character_sum, weighted_count, nonzero_terms = hurwitz_number()
    assert character_sum == Fraction(31104, 19019)
    assert weighted_count == 5
    assert nonzero_terms == 19

    # Ramification from the ten double zeros and seven triple poles is
    # 10+14.  If d<=4 is the degree of R-lambda's numerator, infinity
    # contributes 20-d; Riemann--Hurwitz on P1 forces d=4.
    assert 10 + 14 + (20 - 4) == 2 * 21 - 2

    print("passport: (2^10,1), (3^7), (17,1^4)")
    print("character sum:", character_sum)
    print("nonzero character terms:", nonzero_terms)
    print("weighted Hurwitz count:", weighted_count)
    print(
        "transitivity: automatic, since a component on the four fixed "
        "third-value sheets would make a 3-cycle equal an involution"
    )
    print(
        "automorphisms: trivial, since the distinguished simple zero and "
        "17-fold point are fixed and R(w)=w+... rules out nontrivial scaling"
    )
    print("RESULT: EXACT a/b OUTER HURWITZ COUNT IS FIVE")


if __name__ == "__main__":
    main()
