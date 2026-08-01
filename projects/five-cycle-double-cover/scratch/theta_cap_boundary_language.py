#!/usr/bin/env python3
"""Enumerate the D5 boundary languages of two five-terminal caps.

A D5 label is a two-subset of {0,1,2,3,4}.  At a cubic vertex the
three incident labels must be the three edges of a coordinate triangle.
The script compares

* the three-vertex path cap, with terminal multiplicities 2,1,2; and
* the seven-vertex theta cap used in the order-100 construction.

It also verifies a six-row, symmetry-reduced extension table proving
that every ordered simple coordinate 5-cycle extends through the theta
cap.  Only the Python standard library is used.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import json


COORDINATES = range(5)
LABELS = tuple(combinations(COORDINATES, 2))
LABEL_MASKS = tuple(sum(1 << coordinate for coordinate in label)
                    for label in LABELS)
CYCLE_EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))
COLOR_PERMUTATIONS = tuple(permutations(COORDINATES))


def mask(label: tuple[int, int]) -> int:
    return sum(1 << coordinate for coordinate in label)


def text(label: int) -> str:
    return "".join(str(coordinate) for coordinate in COORDINATES
                   if label >> coordinate & 1)


@lru_cache(maxsize=None)
def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[coordinate]
        for coordinate in COORDINATES
        if label >> coordinate & 1
    )


@lru_cache(maxsize=None)
def color_orbit_representative(
    word: tuple[int, ...],
) -> tuple[int, ...]:
    return min(
        tuple(permute_label(label, permutation) for label in word)
        for permutation in COLOR_PERMUTATIONS
    )


def local_states() -> tuple[tuple[int, int, int], ...]:
    result = []
    for triangle in combinations(COORDINATES, 3):
        triangle_edges = tuple(
            mask(edge) for edge in combinations(triangle, 2)
        )
        result.extend(permutations(triangle_edges))
    assert len(result) == 60
    return tuple(result)


STATES = local_states()
BY_SLOT_LABEL = {
    (slot, label): tuple(
        state for state in STATES if state[slot] == label
    )
    for slot in range(3)
    for label in LABEL_MASKS
}


def third_label(first: int, second: int) -> int | None:
    third = first ^ second
    if third not in LABEL_MASKS or len({first, second, third}) != 3:
        return None
    return third


def path_language() -> set[tuple[int, ...]]:
    """Ports are (a0,a1,b0,b1,v)."""
    result = set()
    # v slots are (av,bv,v); a and b slots begin with their path edge.
    for at_v in STATES:
        av, bv, terminal_v = at_v
        for at_a in BY_SLOT_LABEL[0, av]:
            for at_b in BY_SLOT_LABEL[0, bv]:
                result.add((
                    at_a[1], at_a[2], at_b[1], at_b[2], terminal_v
                ))
    return result


def theta_language() -> dict[tuple[int, ...], tuple[int, ...]]:
    """Return one internal-edge witness for every ordered boundary tuple.

    Internal-edge order is
    (w0w1,w2w3,w0z0,w2z0,w4z0,w1z1,w3z1,w4z1).
    """
    result = {}
    # z0 slots are (w0,w2,w4); z1 slots are (w1,w3,w4).
    # w0,w1,w2,w3 slots are (boundary,root,z); w4 slots are
    # (boundary,z0,z1).
    for at_z0 in STATES:
        w0z0, w2z0, w4z0 = at_z0
        for at_w0 in BY_SLOT_LABEL[2, w0z0]:
            for at_w2 in BY_SLOT_LABEL[2, w2z0]:
                for at_w4 in BY_SLOT_LABEL[1, w4z0]:
                    for at_z1 in BY_SLOT_LABEL[2, at_w4[2]]:
                        boundary_w1 = third_label(
                            at_w0[1], at_z1[0]
                        )
                        boundary_w3 = third_label(
                            at_w2[1], at_z1[1]
                        )
                        if boundary_w1 is None or boundary_w3 is None:
                            continue
                        boundary = (
                            at_w0[0],
                            boundary_w1,
                            at_w2[0],
                            boundary_w3,
                            at_w4[0],
                        )
                        internal = (
                            at_w0[1],
                            at_w2[1],
                            at_z0[0],
                            at_z0[1],
                            at_z0[2],
                            at_z1[0],
                            at_z1[1],
                            at_z1[2],
                        )
                        result.setdefault(boundary, internal)
    return result


def is_simple_five_cycle(boundary: tuple[int, ...]) -> bool:
    if len(set(boundary)) != 5:
        return False
    degrees = [0] * 5
    neighbours = [set() for _ in COORDINATES]
    for label in boundary:
        vertices = [coordinate for coordinate in COORDINATES
                    if label >> coordinate & 1]
        if len(vertices) != 2:
            return False
        left, right = vertices
        degrees[left] += 1
        degrees[right] += 1
        neighbours[left].add(right)
        neighbours[right].add(left)
    return degrees == [2] * 5 and all(len(row) == 2 for row in neighbours)


def cap_automorphisms() -> tuple[tuple[int, ...], ...]:
    # Vertices 0..4 are w0..w4; 5,6 are z0,z1.
    internal_edges = {
        tuple(sorted(edge)) for edge in (
            (0, 1), (2, 3), (0, 5), (2, 5), (4, 5),
            (1, 6), (3, 6), (4, 6),
        )
    }
    result = set()
    for image in permutations(range(7)):
        if set(image[:5]) != set(range(5)):
            continue
        transformed = {
            tuple(sorted((image[left], image[right])))
            for left, right in internal_edges
        }
        if transformed == internal_edges:
            result.add(tuple(image[index] for index in range(5)))
    return tuple(sorted(result))


def dihedral_edge_actions() -> tuple[tuple[int, ...], ...]:
    edge_index = {
        tuple(sorted(edge)): index
        for index, edge in enumerate(CYCLE_EDGES)
    }
    result = []
    for image in permutations(COORDINATES):
        action = []
        for edge in CYCLE_EDGES:
            transformed = tuple(sorted((
                image[edge[0]], image[edge[1]]
            )))
            if transformed not in edge_index:
                break
            action.append(edge_index[transformed])
        else:
            result.append(tuple(action))
    return tuple(result)


def five_cycle_orbits() -> tuple[tuple[tuple[int, ...], set[tuple[int, ...]]], ...]:
    cap_actions = cap_automorphisms()
    coordinate_actions = dihedral_edge_actions()
    unseen = set(permutations(range(5)))
    result = []
    while unseen:
        representative = min(unseen)
        orbit = set()
        stack = [representative]
        while stack:
            assignment = stack.pop()
            if assignment in orbit:
                continue
            orbit.add(assignment)
            for cap_action in cap_actions:
                for coordinate_action in coordinate_actions:
                    transformed = [None] * 5
                    for old_position in range(5):
                        transformed[cap_action[old_position]] = (
                            coordinate_action[assignment[old_position]]
                        )
                    value = tuple(transformed)
                    if value not in orbit:
                        stack.append(value)
        unseen -= orbit
        result.append((representative, orbit))
    return tuple(result)


def boundary_orbit_representatives() -> tuple[tuple[int, ...], ...]:
    result = set()
    for prefix in product(LABEL_MASKS, repeat=4):
        last = prefix[0] ^ prefix[1] ^ prefix[2] ^ prefix[3]
        if last in LABEL_MASKS:
            result.add(color_orbit_representative((*prefix, last)))
    if len(result) != 62:
        raise AssertionError("five-boundary orbit count changed")
    return tuple(sorted(result))


def toggle_pair(
    word: tuple[int, ...],
    positions: tuple[int, int] | list[int],
    color_pair: int,
) -> tuple[int, ...]:
    result = list(word)
    for position in positions:
        result[position] ^= color_pair
    answer = tuple(result)
    if not all(label in LABEL_MASKS for label in answer):
        raise AssertionError("bichromatic switch left D5")
    return answer


def switching_escape(
    word: tuple[int, ...],
    theta: dict[tuple[int, ...], tuple[int, ...]],
) -> dict[str, object]:
    """Find a pair whose every possible path pairing reaches the cap."""
    theta_orbits = {
        color_orbit_representative(boundary)
        for boundary in theta
    }
    for left, right in combinations(COORDINATES, 2):
        pair = (1 << left) | (1 << right)
        positions = [
            index for index, label in enumerate(word)
            if bool(label & (1 << left)) ^ bool(label & (1 << right))
        ]
        if len(positions) != 4:
            continue
        pairings = (
            ((positions[0], positions[1]), (positions[2], positions[3])),
            ((positions[0], positions[2]), (positions[1], positions[3])),
            ((positions[0], positions[3]), (positions[1], positions[2])),
        )
        rows = []
        works = True
        for pairing in pairings:
            outputs = tuple(
                color_orbit_representative(
                    toggle_pair(word, path, pair)
                )
                for path in pairing
            )
            works &= all(output in theta_orbits for output in outputs)
            rows.append({
                "path_pairing": pairing,
                "switched_outputs": [
                    {
                        "boundary_orbit": [
                            text(label) for label in output
                        ],
                        "theta_internal_witness": (
                            [text(label) for label in theta[output]]
                            if output in theta else None
                        ),
                    }
                    for output in outputs
                ],
            })
        if works:
            return {
                "color_pair": (left, right),
                "boundary_positions": positions,
                "all_three_pairings_escape": True,
                "pairings": rows,
            }
    raise AssertionError("missing theta state has no switching escape")


def main() -> int:
    path = path_language()
    theta = theta_language()
    simple_cycles = {
        boundary for boundary in permutations(
            tuple(mask(edge) for edge in CYCLE_EDGES)
        )
    }
    assert len(path) == 2160
    assert len(theta) == 6000
    assert len(simple_cycles) == 120

    # Enumerate all ordered simple coordinate 5-cycles independently of
    # the cap language, rather than merely testing the fixed canonical
    # cycle used in the symmetry table below.
    all_simple_cycles = {
        boundary
        for boundary in permutations(LABEL_MASKS, 5)
        if is_simple_five_cycle(boundary)
    }
    assert len(all_simple_cycles) == 1440
    assert all_simple_cycles <= set(theta)
    assert len(path - set(theta)) == 120

    boundary_orbits = set(boundary_orbit_representatives())
    theta_orbits = {
        color_orbit_representative(boundary)
        for boundary in theta
    }
    missing_orbits = tuple(sorted(boundary_orbits - theta_orbits))
    if len(theta_orbits) != 58 or len(missing_orbits) != 4:
        raise AssertionError("theta-cap color-orbit profile changed")
    switching_certificate = [
        {
            "missing_boundary_orbit": [text(label) for label in word],
            **switching_escape(word, theta),
        }
        for word in missing_orbits
    ]

    orbits = five_cycle_orbits()
    assert len(orbits) == 6
    assert Counter(len(orbit) for _, orbit in orbits) == {20: 6}
    cycle_masks = tuple(mask(edge) for edge in CYCLE_EDGES)
    table = []
    for representative, _ in orbits:
        boundary = tuple(cycle_masks[index] for index in representative)
        internal = theta[boundary]
        table.append({
            "edge_order_at_ports": representative,
            "boundary_labels": [text(label) for label in boundary],
            "internal_labels": [text(label) for label in internal],
        })

    report = {
        "status": "PASS",
        "local_states": len(STATES),
        "path_boundary_states": len(path),
        "theta_boundary_states": len(theta),
        "path_states_not_accepted_by_theta": len(path - set(theta)),
        "ordered_simple_five_cycles": len(all_simple_cycles),
        "all_simple_five_cycles_accepted_by_theta": True,
        "cap_automorphisms": len(cap_automorphisms()),
        "coordinate_cycle_automorphisms": len(dihedral_edge_actions()),
        "symmetry_reduced_cases": len(orbits),
        "extension_table": table,
        "all_even_boundary_color_orbits": len(boundary_orbits),
        "theta_boundary_color_orbits": len(theta_orbits),
        "missing_boundary_color_orbits": len(missing_orbits),
        "switching_attractor": True,
        "switching_certificate": switching_certificate,
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
