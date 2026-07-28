#!/usr/bin/env python3
"""Search four-coordinate traps against the cubic rooted Kempe-orbit lemma.

Random seeds are built from a missing-coordinate map m:V->{0,1,2,3}.
For each of the three complementary-pair classes of K4, vertices are
perfect-matched inside the two corresponding blocks.  This gives a Tait
colouring and a canonical D4 lift.  The script retains simple connected
cubic graphs whose four coordinate classes are initially single circuits,
then explores the complete standard component-Kempe orbit.

A reported failure is a counterexample to the rooted reconfiguration lemma,
not automatically a FiveCDC counterexample.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import deque
from itertools import combinations, permutations


LABELS = tuple(
    (1 << first) | (1 << second)
    for first, second in combinations(range(5), 2)
)
LABEL_SET = frozenset(LABELS)
PAIRS = tuple(combinations(range(5), 2))
PERMUTATIONS = tuple(permutations(range(5)))
PERMUTATIONS4 = tuple(
    permutation + (4,)
    for permutation in permutations(range(4))
)

# A Tait colour is a partition of the four used coordinates into two
# complementary two-subsets.
TAIT_PARTITIONS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def permute_label(label: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for coordinate in range(5):
        if (label >> coordinate) & 1:
            answer |= 1 << permutation[coordinate]
    return answer


PERMUTED = {
    permutation: {
        label: permute_label(label, permutation)
        for label in LABELS
    }
    for permutation in PERMUTATIONS
}


def canonical(state: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(PERMUTED[permutation][label] for label in state)
        for permutation in PERMUTATIONS
    )


def canonical4(state: tuple[int, ...]) -> tuple[int, ...]:
    assert all(label < 16 for label in state)
    return min(
        tuple(PERMUTED[permutation][label] for label in state)
        for permutation in PERMUTATIONS4
    )


def components(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    selected: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    selected_set = set(selected)
    for edge in selected:
        left, right = edges[edge]
        incidence[left].append(edge)
        incidence[right].append(edge)
    unseen = set(selected)
    answer = []
    while unseen:
        first = unseen.pop()
        seen_edges = {first}
        queue = deque((first,))
        while queue:
            edge = queue.popleft()
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if other in selected_set and other not in seen_edges:
                        seen_edges.add(other)
                        unseen.discard(other)
                        queue.append(other)
        answer.append(tuple(sorted(seen_edges)))
    return tuple(sorted(answer))


def connected_graph(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    adjacency = [[] for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {0}
    queue = deque((0,))
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == vertices


def validate_flow(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, ...],
) -> None:
    assert len(state) == len(edges)
    assert all(label in LABEL_SET for label in state)
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(row) == 3 for row in incidence)
    for row in incidence:
        assert state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0


def coordinate_classes_are_circuits(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, ...],
) -> bool:
    used = {
        coordinate
        for label in state
        for coordinate in range(5)
        if (label >> coordinate) & 1
    }
    if len(used) != 4:
        return False
    for coordinate in used:
        selected = tuple(
            edge
            for edge, label in enumerate(state)
            if (label >> coordinate) & 1
        )
        if len(components(vertices, edges, selected)) != 1:
            return False
    return True


def kempe_neighbours(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    answer = set()
    for first, second in PAIRS:
        pair = (1 << first) | (1 << second)
        active = tuple(
            edge
            for edge, label in enumerate(state)
            if (label & pair).bit_count() == 1
        )
        for component in components(vertices, edges, active):
            switched = list(state)
            for edge in component:
                switched[edge] ^= pair
                assert switched[edge] in LABEL_SET
            answer.add(canonical(tuple(switched)))
    return frozenset(answer)


def orbit_audit(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    initial: tuple[int, ...],
):
    initial = canonical4(initial)
    seen = {initial}
    queue = deque((initial,))
    successful_roots: set[tuple[int, int]] = set()
    trapped = True
    while queue:
        state = queue.popleft()
        trapped = trapped and coordinate_classes_are_circuits(
            vertices, edges, state
        )
        for first, second in PAIRS:
            pair = (1 << first) | (1 << second)
            active = tuple(
                edge
                for edge, label in enumerate(state)
                if (label & pair).bit_count() == 1
            )
            for component in components(vertices, edges, active):
                successful_roots.update(combinations(component, 2))
        # Only the six pairs among the used coordinates need exploration.
        # If every coordinate class remains one circuit, the four switches
        # against missing coordinate 4 are global renamings.
        for first, second in combinations(range(4), 2):
            pair = (1 << first) | (1 << second)
            active = tuple(
                edge
                for edge, label in enumerate(state)
                if (label & pair).bit_count() == 1
            )
            for component in components(vertices, edges, active):
                switched = list(state)
                for edge in component:
                    switched[edge] ^= pair
                other = canonical4(tuple(switched))
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
    all_roots = set(combinations(range(len(edges)), 2))
    return {
        "states": seen,
        "trapped": trapped,
        "failed_roots": sorted(all_roots - successful_roots),
    }


def static_failed_roots(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    successful_roots: set[tuple[int, int]] = set()
    for first, second in PAIRS:
        pair = (1 << first) | (1 << second)
        active = tuple(
            edge
            for edge, label in enumerate(state)
            if (label & pair).bit_count() == 1
        )
        for component in components(vertices, edges, active):
            successful_roots.update(combinations(component, 2))
    return tuple(sorted(
        set(combinations(range(len(edges)), 2)) - successful_roots
    ))


def random_matching(
    rng: random.Random,
    vertices: list[int],
) -> list[tuple[int, int]]:
    shuffled = vertices[:]
    rng.shuffle(shuffled)
    return [
        tuple(sorted((shuffled[index], shuffled[index + 1])))
        for index in range(0, len(shuffled), 2)
    ]


def random_seed(
    rng: random.Random,
    vertices: int,
):
    assert vertices % 4 == 0
    missing = [
        coordinate
        for coordinate in range(4)
        for _ in range(vertices // 4)
    ]
    rng.shuffle(missing)
    edges = []
    labels = []
    for first_block, second_block in TAIT_PARTITIONS:
        first_vertices = [
            vertex
            for vertex, coordinate in enumerate(missing)
            if coordinate in first_block
        ]
        second_vertices = [
            vertex
            for vertex, coordinate in enumerate(missing)
            if coordinate in second_block
        ]
        for block_vertices, opposite_label in (
            (first_vertices, second_block),
            (second_vertices, first_block),
        ):
            for edge in random_matching(rng, block_vertices):
                edges.append(edge)
                labels.append(
                    (1 << opposite_label[0]) | (1 << opposite_label[1])
                )
    if len(set(edges)) != len(edges):
        return None
    ordered = sorted(zip(edges, labels))
    graph_edges = tuple(edge for edge, _label in ordered)
    state = tuple(label for _edge, label in ordered)
    if not connected_graph(vertices, graph_edges):
        return None
    validate_flow(vertices, graph_edges, state)
    if not coordinate_classes_are_circuits(vertices, graph_edges, state):
        return None
    return graph_edges, state, tuple(missing)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vertices", type=int, default=16)
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260728)
    args = parser.parse_args()
    if args.vertices % 4:
        raise SystemExit("--vertices must be divisible by four")
    rng = random.Random(args.seed)

    retained = 0
    trapped = 0
    maximum_orbit = 0
    static_failures = 0
    for trial in range(args.trials):
        seed = random_seed(rng, args.vertices)
        if seed is None:
            continue
        retained += 1
        edges, state, missing = seed
        if static_failed_roots(args.vertices, edges, state):
            static_failures += 1
        audit = orbit_audit(args.vertices, edges, state)
        maximum_orbit = max(maximum_orbit, len(audit["states"]))
        if audit["trapped"]:
            trapped += 1
            if audit["failed_roots"]:
                root = audit["failed_roots"][0]
                print(json.dumps({
                    "classification": "D4_TRAPPED_ROOT_ORBIT_COUNTEREXAMPLE",
                    "vertices": args.vertices,
                    "trial": trial,
                    "seed": args.seed,
                    "edges": edges,
                    "labels": state,
                    "missing_coordinates": missing,
                    "orbit_states": len(audit["states"]),
                    "failed_root": root,
                }, sort_keys=True))
                return
    print(json.dumps({
        "classification": "NO_COUNTEREXAMPLE_IN_RANDOM_SAMPLE",
        "vertices": args.vertices,
        "trials": args.trials,
        "retained_single_circuit_seeds": retained,
        "fully_D4_trapped_orbits": trapped,
        "seeds_with_static_root_failures": static_failures,
        "maximum_orbit": maximum_orbit,
        "seed": args.seed,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
