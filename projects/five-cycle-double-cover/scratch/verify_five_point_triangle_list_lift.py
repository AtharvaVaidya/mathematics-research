#!/usr/bin/env python3
"""Literal audit of the five-point restriction of Fano triangle labels.

The eight points are the integers 0,...,7 with bitwise xor.  A Fano line
is represented by its four-element vector subspace, including zero.  A
local coordinate triangle for that line is a three-element subset of one
of its two affine cosets.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json


POINTS = frozenset(range(8))


def xor_sum(values: frozenset[int] | set[int]) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def fano_planes() -> tuple[frozenset[int], ...]:
    planes = {
        frozenset((0, first, second, first ^ second))
        for first in range(1, 8)
        for second in range(first + 1, 8)
    }
    assert len(planes) == 7
    return tuple(sorted(planes, key=lambda plane: tuple(sorted(plane))))


def affine_triangles(plane: frozenset[int]) -> tuple[frozenset[int], ...]:
    translate = next(point for point in POINTS if point not in plane)
    cosets = (plane, frozenset(point ^ translate for point in plane))
    triangles = {
        frozenset(coset - {omitted})
        for coset in cosets
        for omitted in coset
    }
    assert len(triangles) == 8
    return tuple(sorted(triangles, key=lambda triangle: tuple(sorted(triangle))))


def pair_with_difference(
    triangle: frozenset[int], difference: int
) -> frozenset[int]:
    pairs = [
        frozenset((left, right))
        for left, right in combinations(sorted(triangle), 2)
        if left ^ right == difference
    ]
    assert len(pairs) == 1
    return pairs[0]


def main() -> int:
    planes = fano_planes()
    five_sets = tuple(frozenset(values) for values in combinations(range(8), 5))
    assert len(five_sets) == 56

    line_case_counts = Counter()
    total_allowed_triangles = 0
    for five_set in five_sets:
        forbidden = POINTS - five_set
        singleton = xor_sum(set(forbidden))
        assert singleton in five_set

        forbidden_plane = frozenset(forbidden | {singleton})
        special = frozenset(point ^ singleton for point in forbidden_plane)
        assert special in planes
        other_coset = five_set - {singleton}
        assert len(other_coset) == 4
        assert frozenset(point ^ singleton for point in other_coset) != special

        special_cases = 0
        for plane in planes:
            allowed = [
                triangle
                for triangle in affine_triangles(plane)
                if triangle <= five_set
            ]
            expected = 4 if plane == special else 1
            assert len(allowed) == expected
            line_case_counts[(plane == special, len(allowed))] += 1
            total_allowed_triangles += len(allowed)

            if plane == special:
                special_cases += 1
                assert all(triangle <= other_coset for triangle in allowed)
                for triangle in allowed:
                    for difference in plane - {0}:
                        assert pair_with_difference(
                            triangle, difference
                        ) <= other_coset
                continue

            triangle = allowed[0]
            assert singleton in triangle
            intersection = (plane & special) - {0}
            assert len(intersection) == 1
            common_value = next(iter(intersection))
            assert pair_with_difference(triangle, common_value) <= other_coset
            for difference in plane - {0, common_value}:
                pair = pair_with_difference(triangle, difference)
                assert singleton in pair
                assert len(pair & other_coset) == 1
        assert special_cases == 1

    result = {
        "schema": "five-cdc-five-point-triangle-list-v1",
        "five_point_sets": len(five_sets),
        "fano_lines": len(planes),
        "line_cases": len(five_sets) * len(planes),
        "special_line_cases": line_case_counts[(True, 4)],
        "nonspecial_line_cases": line_case_counts[(False, 1)],
        "allowed_local_triangles": total_allowed_triangles,
        "result": (
            "For every five-point subset of F2^3, exactly one Fano line "
            "has four admitted local coordinate triangles and each of the "
            "other six lines has exactly one."
        ),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
