#!/usr/bin/env python3
"""Finite algebra replay for the saturated disjoint-root normal form."""

from __future__ import annotations

import itertools


COORDINATES = frozenset(range(5))
LABELS = tuple(frozenset(pair) for pair in itertools.combinations(range(5), 2))


def active(label: frozenset[int], pair: frozenset[int]) -> bool:
    return len(label & pair) == 1


def transpose(
    label: frozenset[int], first: int, second: int
) -> frozenset[int]:
    if (first in label) == (second in label):
        return label
    if first in label:
        return (label - {first}) | {second}
    return (label - {second}) | {first}


def check_label_separation() -> int:
    cases = 0
    for root in LABELS:
        for target in LABELS:
            if not root & target:
                continue
            if root != target:
                common = next(iter(root & target))
                fresh = next(iter(COORDINATES - root - target))
                pair = frozenset((common, fresh))
                assert active(root, pair)
                assert active(target, pair)
                changed = transpose(root, common, fresh)
                assert not changed & target
            else:
                first, second = tuple(root)
                outside = tuple(COORDINATES - root)
                fresh_first, fresh_second = outside[:2]
                pair_first = frozenset((first, fresh_first))
                assert active(root, pair_first)
                assert active(target, pair_first)
                changed = transpose(root, first, fresh_first)
                pair_second = frozenset((second, fresh_second))
                assert active(changed, pair_second)
                assert active(target, pair_second)
                changed = transpose(changed, second, fresh_second)
                assert not changed & target
            cases += 1
    return cases


def check_d4_cross_switches() -> int:
    cases = 0
    for used_tuple in itertools.combinations(range(5), 4):
        used = frozenset(used_tuple)
        for root_tuple in itertools.combinations(used_tuple, 2):
            root = frozenset(root_tuple)
            target = used - root
            for chosen in root:
                other = next(iter(root - {chosen}))
                for target_coordinate in target:
                    pair = frozenset((chosen, target_coordinate))
                    assert active(root, pair)
                    assert active(target, pair)
                    changed = transpose(root, chosen, target_coordinate)
                    assert changed == frozenset((other, target_coordinate))
                    assert changed & target == {target_coordinate}
                    cases += 1
    return cases


def check_local_support_contradiction() -> int:
    """No cubic D4 triangle can have both a-edges labelled ab."""

    cases = 0
    for used_tuple in itertools.combinations(range(5), 4):
        used = frozenset(used_tuple)
        for root_tuple in itertools.combinations(used_tuple, 2):
            root = frozenset(root_tuple)
            target = used - root
            for chosen in root:
                other = next(iter(root - {chosen}))
                target_first, target_second = tuple(target)

                # A local xor-zero triple is the three sides of a
                # three-coordinate triangle.
                for triangle in itertools.combinations(used_tuple, 3):
                    if chosen not in triangle:
                        continue
                    chosen_edges = {
                        frozenset((chosen, coordinate))
                        for coordinate in triangle
                        if coordinate != chosen
                    }
                    assert len(chosen_edges) == 2
                    # If every C_chosen edge were active in both cross
                    # factors, both local chosen-edges would have to be
                    # the single label {chosen, other}; impossible.
                    active_in_both = {
                        label
                        for label in chosen_edges
                        if active(label, frozenset((chosen, target_first)))
                        and active(label, frozenset((chosen, target_second)))
                    }
                    assert active_in_both <= {
                        frozenset((chosen, other))
                    }
                    assert chosen_edges != {
                        frozenset((chosen, other))
                    }
                    cases += 1
    return cases


def check_disjoint_gate() -> int:
    cases = 0
    for root in LABELS:
        for target in LABELS:
            if root & target:
                continue
            active_on_both = {
                pair
                for pair in LABELS
                if active(root, pair) and active(target, pair)
            }
            expected = {
                frozenset((first, second))
                for first in root
                for second in target
            }
            assert active_on_both == expected
            assert len(active_on_both) == 4
            cases += 1
    return cases


def main() -> int:
    separation_cases = check_label_separation()
    cross_cases = check_d4_cross_switches()
    local_cases = check_local_support_contradiction()
    gate_cases = check_disjoint_gate()
    print("PASS")
    print(f"intersecting ordered root-label pairs: {separation_cases}")
    print(f"D4 cross-switch cases: {cross_cases}")
    print(f"D4 local triangle cases: {local_cases}")
    print(f"ordered disjoint-gate cases: {gate_cases}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
