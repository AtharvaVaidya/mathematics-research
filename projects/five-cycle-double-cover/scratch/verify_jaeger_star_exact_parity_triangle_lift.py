#!/usr/bin/env python3
"""Exhaust the local triangle-lift table for exact Jaeger parity.

Bit positions 0,1,2 represent triangle vertices a,b,c.  Triangle-edge
bit positions represent ab,bc,ca.  The script enumerates a superset of all
realizable odd-kernel traces, reduces it by vertex permutations and swapping
the two common-kernel coordinates, and checks the seven-row lift table.
"""

from __future__ import annotations

from itertools import permutations, product


ODD_MASKS = (1, 2, 4, 7)
TRIANGLE_EDGES = ((0, 1), (1, 2), (2, 0))
VERTEX_PERMUTATIONS = tuple(permutations(range(3)))
EXPECTED = {
    ((1, 1, 2), 2): ((0, 1, 2), (2, 5, 3), 1),
    ((1, 2, 1), 0): ((0, 1, 2), (2, 4, 2), 0),
    ((1, 2, 4), 0): ((0, 1, 2), (2, 4, 1), 0),
    ((1, 2, 7), 0): ((0, 1, 2), (2, 4, 0), 0),
    ((1, 2, 7), 3): ((1, 2, 0), (5, 3, 0), 0),
    ((1, 2, 7), 5): ((1, 0, 2), (5, 4, 0), 0),
    ((1, 7, 2), 2): ((0, 1, 2), (2, 0, 3), 1),
}


def boundary(edge_mask: int) -> int:
    answer = 0
    for edge, (left, right) in enumerate(TRIANGLE_EDGES):
        if edge_mask & (1 << edge):
            answer ^= 1 << left
            answer ^= 1 << right
    return answer


def local_kernel(external_trace: int, omitted_edge: int) -> int:
    """Unique local K subset of the two-edge expansion tree."""
    allowed = 7 ^ (1 << omitted_edge)
    answers = [
        mask
        for mask in range(8)
        if mask & ~allowed == 0
        and boundary(mask) == (7 ^ external_trace)
    ]
    assert len(answers) == 1
    return answers[0]


def permute_vertex_mask(mask: int, permutation: tuple[int, int, int]) -> int:
    answer = 0
    for vertex in range(3):
        if mask & (1 << vertex):
            answer |= 1 << permutation[vertex]
    return answer


def all_patterns() -> set[tuple[tuple[int, int, int], int]]:
    answer = set()
    for traces in product(ODD_MASKS, repeat=3):
        # No external edge lies in all three trees, hence none lies in all
        # three odd kernels.
        if traces[0] & traces[1] & traces[2]:
            continue
        for p_trace in range(8):
            if p_trace & ~traces[2]:
                continue
            # Downstairs Z=(K0 cap K1) xor P is even at the contracted
            # vertex.
            if ((traces[0] & traces[1]) ^ p_trace).bit_count() % 2:
                continue
            answer.add((traces, p_trace))
    return answer


def orbit(
    pattern: tuple[tuple[int, int, int], int],
    universe: set[tuple[tuple[int, int, int], int]],
) -> set[tuple[tuple[int, int, int], int]]:
    traces, p_trace = pattern
    answer = set()
    for permutation in VERTEX_PERMUTATIONS:
        for swap in (False, True):
            ordered = (
                (traces[1], traces[0], traces[2])
                if swap
                else traces
            )
            image = (
                tuple(
                    permute_vertex_mask(trace, permutation)
                    for trace in ordered
                ),
                permute_vertex_mask(p_trace, permutation),
            )
            if image in universe:
                answer.add(image)
    return answer


def lift_solutions(
    pattern: tuple[tuple[int, int, int], int]
) -> list[tuple[tuple[int, int, int], tuple[int, int, int], int]]:
    traces, p_trace = pattern
    external_z = (traces[0] & traces[1]) ^ p_trace
    answer = []
    for omitted in permutations(range(3)):
        local = tuple(
            local_kernel(traces[coordinate], omitted[coordinate])
            for coordinate in range(3)
        )
        local_common = local[0] & local[1]
        required_boundary = external_z ^ boundary(local_common)
        completions = [
            mask
            for mask in range(8)
            if mask & ~local[2] == 0
            and boundary(mask) == required_boundary
        ]
        if completions:
            # K2 is a forest, so this completion is unique.
            assert len(completions) == 1
            answer.append((omitted, local, completions[0]))
    return answer


def main() -> None:
    patterns = all_patterns()
    assert len(patterns) == 60
    unseen = set(patterns)
    representatives = []
    orbit_sizes = []
    while unseen:
        representative = min(unseen)
        current = orbit(representative, patterns)
        assert current
        unseen -= current
        representatives.append(representative)
        orbit_sizes.append(len(current))
    assert representatives == list(EXPECTED)
    assert orbit_sizes == [6, 12, 6, 6, 6, 12, 12]
    assert sum(orbit_sizes) == 60

    solution_histogram: dict[int, int] = {}
    for pattern in patterns:
        solutions = lift_solutions(pattern)
        assert solutions
        solution_histogram[len(solutions)] = (
            solution_histogram.get(len(solutions), 0) + 1
        )
    assert solution_histogram == {1: 18, 2: 12, 3: 6, 4: 24}

    for representative, expected in EXPECTED.items():
        assert expected in lift_solutions(representative)

    print("PASS")
    print(
        "admissible local trace patterns=60; symmetry orbits=7; "
        "patterns without a parity-preserving triangle lift=0"
    )
    print("orbit_sizes=6,12,6,6,6,12,12")
    print("number_of_good_lifts histogram: 1:18 2:12 3:6 4:24")


if __name__ == "__main__":
    main()
