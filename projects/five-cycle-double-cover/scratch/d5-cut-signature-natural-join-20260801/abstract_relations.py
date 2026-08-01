#!/usr/bin/env python3
"""Enumerate the complete parity/S5-local abstract cut-state frontier."""

from __future__ import annotations

import hashlib
from itertools import combinations, permutations, product
import json


D5 = tuple((1 << i) | (1 << j) for i, j in combinations(range(5), 2))
INDEX = {label: index for index, label in enumerate(D5)}
NAMES = tuple(f"{i}{j}" for i, j in combinations(range(5), 2))
PHYSICAL = {(0, 1): 0, (0, 2): 1, (1, 2): 2}


def active(label: int, factor: int) -> bool:
    return (label & factor).bit_count() == 1


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[i] for i in range(5) if label & (1 << i))


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << INDEX[permute_label(label, permutation)]
        for index, label in enumerate(D5)
        if mask & (1 << index)
    )


def state_orbit(mask: int, group: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sorted({permute_mask(mask, permutation) for permutation in group}))


def cap_orbit(
    state: tuple[int, int, int],
    group: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(sorted({
        tuple(permute_mask(mask, permutation) for mask in state)
        for permutation in group
    }))


def mask_names(mask: int) -> tuple[str, ...]:
    return tuple(NAMES[index] for index in range(10) if mask & (1 << index))


def local_universe(boundary: tuple[int, ...]):
    boundary_active = tuple(
        factor for factor in D5
        if sum(active(label, factor) for label in boundary) == 2
    )
    boundary_mask = sum(1 << INDEX[factor] for factor in boundary_active)
    group = tuple(
        permutation for permutation in permutations(range(5))
        if tuple(permute_label(label, permutation) for label in boundary) == boundary
    )

    # A root state may use only factors active both on the root label and on
    # the boundary.  Local parity imposes no connectivity relation among
    # those eligible factors, so take every subset.
    root_states: set[int] = set()
    for root_label in D5:
        eligible = tuple(
            INDEX[factor] for factor in boundary_active
            if active(root_label, factor)
        )
        for subset in range(1 << len(eligible)):
            root_states.add(sum(
                1 << eligible[position]
                for position in range(len(eligible))
                if subset & (1 << position)
            ))

    # At the cap, choose an arbitrary ordered coordinate triangle.  A factor
    # is locally eligible for one physical pair precisely when it is active
    # on that pair, disjoint from the inactive cap label, and boundary-active.
    # Connectivity may independently retain or omit each eligible factor at
    # the purely local abstraction level.
    cap_states: set[tuple[int, int, int]] = set()
    triangles = tuple(
        labels for labels in product(D5, repeat=3)
        if labels[0] ^ labels[1] ^ labels[2] == 0
    )
    assert len(triangles) == 60
    for triangle in triangles:
        eligible: list[list[int]] = [[], [], []]
        for factor in boundary_active:
            slots = tuple(
                slot for slot, label in enumerate(triangle)
                if active(label, factor)
            )
            if len(slots) != 2:
                continue
            inactive = next(slot for slot in range(3) if slot not in slots)
            if triangle[inactive] & factor:
                assert triangle[inactive] == factor
                continue
            eligible[PHYSICAL[slots]].append(INDEX[factor])
        for selections in product(*(range(1 << len(row)) for row in eligible)):
            cap_states.add(tuple(
                sum(1 << row[position] for position in range(len(row))
                    if selection & (1 << position))
                for row, selection in zip(eligible, selections)
            ))

    root_orbits = tuple(sorted({state_orbit(state, group) for state in root_states}))
    cap_orbits = tuple(sorted({cap_orbit(state, group) for state in cap_states}))
    return (
        boundary_mask,
        group,
        tuple(sorted(root_states)),
        tuple(sorted(cap_states)),
        root_orbits,
        cap_orbits,
    )


def external_mask(root: int, cap: tuple[int, int, int]) -> int:
    return sum(1 << physical for physical in range(3) if root & cap[physical])


def good_orbit_pair(
    root_orbit: tuple[int, ...],
    cap_state_orbit: tuple[tuple[int, int, int], ...],
) -> bool:
    return any(
        external_mask(root, cap).bit_count() >= 2
        for root in root_orbit
        for cap in cap_state_orbit
    )


def nondegenerate(
    root_orbit: tuple[int, ...],
    cap_state_orbit: tuple[tuple[int, int, int], ...],
) -> bool:
    return (
        all(root for root in root_orbit)
        and all(sum(bool(mask) for mask in cap) >= 2 for cap in cap_state_orbit)
    )


def orbit_json(orbit) -> object:
    first = orbit[0]
    if isinstance(first, int):
        return [[*mask_names(mask)] for mask in orbit]
    return [[list(mask_names(mask)) for mask in state] for state in orbit]


def main() -> None:
    expected = {
        2: {
            "boundary": (3, 3),
            "group": 12,
            "boundary_factors": 6,
            "root_states": 64,
            "root_orbits": 13,
            "cap_states": 478,
            "cap_orbits": 51,
            "bad_edges": 281,
            "good_edges": 382,
            "nondegenerate_bad_edges": 110,
            "minimal_root": ((1 << 1), (1 << 2), (1 << 3),
                             (1 << 4), (1 << 5), (1 << 6)),
            "minimal_cap": (
                (0, 1 << 1, 1 << 4), (0, 1 << 2, 1 << 5),
                (0, 1 << 3, 1 << 6), (0, 1 << 4, 1 << 1),
                (0, 1 << 5, 1 << 2), (0, 1 << 6, 1 << 3),
            ),
            "join_histogram": {0: 24, 2: 6, 4: 6},
        },
        3: {
            "boundary": (3, 5, 6),
            "group": 2,
            "boundary_factors": 9,
            "root_states": 238,
            "root_orbits": 138,
            "cap_states": 1774,
            "cap_orbits": 922,
            "bad_edges": 74985,
            "good_edges": 52251,
            "nondegenerate_bad_edges": 65295,
            "minimal_root": (1 << 0,),
            "minimal_cap": ((0, 1 << 0, 1 << 1),),
            "join_histogram": {2: 1},
        },
    }

    for size in (2, 3):
        row = expected[size]
        boundary_mask, group, root_states, cap_states, root_orbits, cap_orbits = (
            local_universe(row["boundary"])
        )
        assert len(group) == row["group"]
        assert boundary_mask.bit_count() == row["boundary_factors"]
        assert len(root_states) == row["root_states"]
        assert len(root_orbits) == row["root_orbits"]
        assert len(cap_states) == row["cap_states"]
        assert len(cap_orbits) == row["cap_orbits"]

        bad_edges = []
        nondegenerate_bad = []
        for root_index, root_orbit in enumerate(root_orbits):
            for cap_index, cap_state_orbit in enumerate(cap_orbits):
                if not good_orbit_pair(root_orbit, cap_state_orbit):
                    bad_edges.append((root_index, cap_index))
                    if nondegenerate(root_orbit, cap_state_orbit):
                        nondegenerate_bad.append((root_index, cap_index))
        total = len(root_orbits) * len(cap_orbits)
        assert len(bad_edges) == row["bad_edges"]
        assert total - len(bad_edges) == row["good_edges"]
        assert len(nondegenerate_bad) == row["nondegenerate_bad_edges"]

        # Lexicographic minimality excludes the vacuous empty root/cap states
        # and then minimizes maximum root support, maximum total cap support,
        # orbit product, and orbit sum.
        scored = []
        for root_index, cap_index in nondegenerate_bad:
            root_orbit = root_orbits[root_index]
            cap_state_orbit = cap_orbits[cap_index]
            score = (
                max(mask.bit_count() for mask in root_orbit),
                max(sum(mask.bit_count() for mask in state)
                    for state in cap_state_orbit),
                len(root_orbit) * len(cap_state_orbit),
                len(root_orbit) + len(cap_state_orbit),
            )
            scored.append((score, root_orbit, cap_state_orbit))
        score, minimal_root, minimal_cap = min(scored)
        assert minimal_root == row["minimal_root"]
        assert minimal_cap == row["minimal_cap"]
        histogram: dict[int, int] = {}
        for root in minimal_root:
            for cap in minimal_cap:
                mask = external_mask(root, cap)
                histogram[mask] = histogram.get(mask, 0) + 1
        assert histogram == row["join_histogram"]
        assert max(mask.bit_count() for mask in histogram) <= 1

        canonical = json.dumps({
            "boundary": row["boundary"],
            "root_orbits": [orbit_json(orbit) for orbit in root_orbits],
            "cap_orbits": [orbit_json(orbit) for orbit in cap_orbits],
            "bad_edges": bad_edges,
        }, sort_keys=True, separators=(",", ":")).encode("ascii")
        digest = hashlib.sha256(canonical).hexdigest()
        print(
            f"ABSTRACT size={size} stabilizer={len(group)} "
            f"boundary_factors={boundary_mask.bit_count()} "
            f"root_states={len(root_states)} root_orbits={len(root_orbits)} "
            f"root_relations=2^{len(root_orbits)}-1 "
            f"cap_states={len(cap_states)} cap_orbits={len(cap_orbits)} "
            f"cap_relations=2^{len(cap_orbits)}-1 "
            f"bad_orbit_edges={len(bad_edges)} good_orbit_edges={total-len(bad_edges)} "
            f"nondegenerate_bad={len(nondegenerate_bad)} sha256={digest} PASS"
        )
        print(
            f"MINIMAL size={size} score={','.join(map(str, score))} "
            f"root={json.dumps(orbit_json(minimal_root), separators=(',', ':'))} "
            f"cap={json.dumps(orbit_json(minimal_cap), separators=(',', ':'))} "
            f"join_hist={json.dumps(histogram, sort_keys=True, separators=(',', ':'))} "
            "unsafe=1 PASS"
        )
    print("ABSTRACT_LOCAL_AXIOMS finite_closure_theorem=FALSE PASS")


if __name__ == "__main__":
    main()
