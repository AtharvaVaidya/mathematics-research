#!/usr/bin/env python3
"""Exact Petersen no-go for a matroid-style D5 orbit-circuit axiom.

For a Kempe orbit O, let C(O) contain every circuit component of every
bichromatic factor Y_ij in every state of O.  This script verifies that
C(O) need not satisfy ordinary circuit elimination:

    A,B in C(O), f in A cap B
      does not always imply
    some C in C(O) with C subset (A union B) - {f}.

The witness is one explicit D5 flow on the Petersen graph.  The result
does not refute the weaker assertion that some orbit circuit (allowed to
leave A union B) contains any prescribed e in A and g in B.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import deque
from pathlib import Path


EDGES = (
    (0, 1),
    (0, 4),
    (0, 5),
    (1, 2),
    (1, 6),
    (2, 3),
    (2, 7),
    (3, 4),
    (3, 8),
    (4, 9),
    (5, 7),
    (5, 8),
    (6, 8),
    (6, 9),
    (7, 9),
)
PAIRS = tuple(itertools.combinations(range(5), 2))
PERMUTATIONS = tuple(itertools.permutations(range(5)))
LABELS = frozenset(
    (1 << first) | (1 << second) for first, second in PAIRS
)

# Edge order is EDGES.  Hex 03 means label {0,1}, etc.
INITIAL = (
    0x03,
    0x05,
    0x06,
    0x06,
    0x05,
    0x0C,
    0x0A,
    0x14,
    0x18,
    0x11,
    0x12,
    0x14,
    0x0C,
    0x09,
    0x18,
)

A_PAIR = (0, 3)
B_PAIR = (2, 4)
A_MASK = sum(1 << edge for edge in (0, 1, 4, 5, 6, 8, 9, 12, 14))
B_MASK = sum(1 << edge for edge in (3, 4, 5, 8, 12))
ELIMINATED_EDGE = 4


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(10)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def validate_state(state: tuple[int, ...]) -> None:
    assert len(state) == len(EDGES)
    assert all(label in LABELS for label in state)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for coordinate in range(5):
        if (label >> coordinate) & 1:
            answer |= 1 << permutation[coordinate]
    return answer


def canonical(state: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_label(label, permutation) for label in state)
        for permutation in PERMUTATIONS
    )


def active_mask(state: tuple[int, ...], pair: tuple[int, int]) -> int:
    first, second = pair
    return sum(
        1 << edge
        for edge, label in enumerate(state)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    )


def component_masks(mask: int) -> tuple[int, ...]:
    unseen = {edge for edge in range(len(EDGES)) if (mask >> edge) & 1}
    answer = []
    while unseen:
        initial = min(unseen)
        queue = [initial]
        component: set[int] = set()
        while queue:
            edge = queue.pop()
            if edge in component:
                continue
            component.add(edge)
            for vertex in EDGES[edge]:
                queue.extend(
                    other
                    for other in INCIDENCE[vertex]
                    if (mask >> other) & 1 and other not in component
                )
        unseen -= component
        answer.append(sum(1 << edge for edge in component))
    return tuple(sorted(answer))


def is_circuit(mask: int) -> bool:
    if not mask:
        return False
    degrees = [
        sum((mask >> edge) & 1 for edge in row)
        for row in INCIDENCE
    ]
    if any(degree not in (0, 2) for degree in degrees):
        return False
    return len(component_masks(mask)) == 1


def transpose_label(label: int, pair: tuple[int, int]) -> int:
    first, second = pair
    if ((label >> first) & 1) == ((label >> second) & 1):
        return label
    return label ^ (1 << first) ^ (1 << second)


def switch(
    state: tuple[int, ...], pair: tuple[int, int], component: int
) -> tuple[int, ...]:
    answer = tuple(
        transpose_label(label, pair) if (component >> edge) & 1 else label
        for edge, label in enumerate(state)
    )
    validate_state(answer)
    return canonical(answer)


def state_circuits(
    state: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], int], ...]:
    answer = []
    for pair in PAIRS:
        for component in component_masks(active_mask(state, pair)):
            assert is_circuit(component)
            answer.append((pair, component))
    return tuple(answer)


def orbit() -> tuple[set[tuple[int, ...]], set[int]]:
    initial = canonical(INITIAL)
    states = {initial}
    queue = deque([initial])
    circuits: set[int] = set()
    while queue:
        state = queue.popleft()
        for pair, component in state_circuits(state):
            circuits.add(component)
            neighbour = switch(state, pair, component)
            if neighbour not in states:
                states.add(neighbour)
                queue.append(neighbour)
    return states, circuits


def raw_orbit() -> tuple[set[tuple[int, ...]], set[int]]:
    """Replay the orbit without quotienting by global coordinate names."""
    states = {INITIAL}
    queue = deque([INITIAL])
    circuits: set[int] = set()
    while queue:
        state = queue.popleft()
        for pair, component in state_circuits(state):
            circuits.add(component)
            neighbour = tuple(
                transpose_label(label, pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            validate_state(neighbour)
            if neighbour not in states:
                states.add(neighbour)
                queue.append(neighbour)
    return states, circuits


def graph_circuits_within(mask: int) -> tuple[int, ...]:
    answer = []
    submask = mask
    while submask:
        if is_circuit(submask):
            answer.append(submask)
        submask = (submask - 1) & mask
    return tuple(sorted(answer))


def edge_list(mask: int) -> list[int]:
    return [
        edge for edge in range(len(EDGES)) if (mask >> edge) & 1
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    validate_state(INITIAL)
    assert component_masks(active_mask(INITIAL, A_PAIR)) == (A_MASK,)
    assert B_MASK in component_masks(active_mask(INITIAL, B_PAIR))
    assert set(A_PAIR).isdisjoint(B_PAIR)
    assert (A_MASK >> ELIMINATED_EDGE) & 1
    assert (B_MASK >> ELIMINATED_EDGE) & 1

    states, orbit_circuits = orbit()
    raw_states, raw_circuits = raw_orbit()
    assert raw_circuits == orbit_circuits
    allowed = (A_MASK | B_MASK) & ~(1 << ELIMINATED_EDGE)
    graph_circuits = graph_circuits_within(allowed)
    symmetric_difference = A_MASK ^ B_MASK

    # In this literal witness the ordinary graphic elimination circuit is
    # unique, but it never occurs as a bichromatic factor circuit in O.
    assert graph_circuits == (symmetric_difference,)
    assert symmetric_difference not in orbit_circuits
    contained_orbit_circuits = sorted(
        circuit
        for circuit in orbit_circuits
        if circuit & ~allowed == 0
    )
    assert contained_orbit_circuits == []

    # Scope check: despite failure of containment, every cross-pair from
    # A x B is already joined by some factor circuit in the initial state.
    initial_circuits = {
        component for _, component in state_circuits(INITIAL)
    }
    cross_pairs = {
        tuple(sorted((left, right)))
        for left in edge_list(A_MASK)
        for right in edge_list(B_MASK)
        if left != right
    }
    initially_joined = {
        pair
        for pair in cross_pairs
        if any(
            all((component >> edge) & 1 for edge in pair)
            for component in initial_circuits
        )
    }
    assert initially_joined == cross_pairs

    result = {
        "schema": "d5-orbit-circuit-elimination-no-go-v1",
        "status": "PASS",
        "graph": {
            "name": "Petersen",
            "graph6": "IheA@GUAo",
            "edges": [list(edge) for edge in EDGES],
        },
        "initial_labels_hex": [f"{label:02x}" for label in INITIAL],
        "witness": {
            "A_pair": list(A_PAIR),
            "A_edges": edge_list(A_MASK),
            "B_pair": list(B_PAIR),
            "B_edges": edge_list(B_MASK),
            "factor_pair_local_type": "disjoint",
            "eliminated_edge": ELIMINATED_EDGE,
            "allowed_union_minus_edge": edge_list(allowed),
            "unique_graph_circuit_in_allowed_set": edge_list(
                symmetric_difference
            ),
        },
        "orbit_mod_global_S5": {
            "states": len(states),
            "distinct_factor_circuit_masks": len(orbit_circuits),
            "factor_circuit_edge_lists": [
                edge_list(mask) for mask in sorted(orbit_circuits)
            ],
        },
        "unquotiented_orbit": {
            "states": len(raw_states),
            "distinct_factor_circuit_masks": len(raw_circuits),
            "same_circuit_family_as_quotient": True,
        },
        "checks": {
            "orbit_circuit_contained_in_allowed_set": False,
            "unique_graph_elimination_circuit_occurs_in_orbit": False,
            "all_A_by_B_edge_pairs_joined_in_initial_state": True,
        },
        "scope": (
            "Refutes matroid-style containment circuit elimination for "
            "C(O), not orbit-level rooted transitivity."
        ),
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
