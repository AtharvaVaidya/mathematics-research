#!/usr/bin/env python3
"""Exact root-component distances in a recurring capped-ladder family."""

from __future__ import annotations

import argparse
import itertools
from collections import deque


A, B, C = 0x03, 0x05, 0x06
PAIRS = tuple(itertools.combinations(range(5), 2))

# One selected cross-cap root pair for each length.  Literal BFS proves the
# listed distance, so this is a lower bound for the graph's maximum radius.
SELECTED = {
    1: ((0, 13), 3),
    2: ((0, 17), 4),
    3: ((0, 20), 5),
    4: ((0, 22), 6),
    5: ((1, 25), 8),
    6: ((1, 28), 9),
}


def capped_ladder(length: int):
    """Return edges and a Tait-supported D5 state for L_length."""
    assert length >= 1
    edges = []
    state = []

    def add(left: int, right: int, label: int) -> int:
        edges.append((left, right))
        state.append(label)
        return len(edges) - 1

    # Left cap: K4 minus the edge between the two attachment vertices.
    add(0, 2, B)
    add(1, 2, C)
    add(0, 3, C)
    add(1, 3, B)
    add(2, 3, A)
    add(0, 4, A)
    add(1, 5, A)

    rung = B
    add(4, 5, rung)
    incoming = A
    for index in range(length):
        upper, lower = 4 + 2 * index, 5 + 2 * index
        next_upper, next_lower = upper + 2, lower + 2
        side = incoming ^ rung
        add(upper, next_upper, side)
        add(lower, next_lower, side)
        rung ^= side
        add(next_upper, next_lower, rung)
        incoming = side

    outgoing = incoming ^ rung
    upper, lower = 4 + 2 * length, 5 + 2 * length
    cap = 6 + 2 * length
    outer_upper, outer_lower, inner_upper, inner_lower = range(cap, cap + 4)
    add(upper, outer_upper, outgoing)
    add(lower, outer_lower, outgoing)
    other = [label for label in (A, B, C) if label != outgoing]
    first, second = other
    add(outer_upper, inner_upper, first)
    add(outer_lower, inner_upper, second)
    add(outer_upper, inner_lower, second)
    add(outer_lower, inner_lower, first)
    add(inner_upper, inner_lower, outgoing)
    return tuple(edges), tuple(state)


def short_graph6(vertices: int, edges: tuple[tuple[int, int], ...]) -> str:
    assert vertices < 63
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = []
    for right in range(1, vertices):
        for left in range(right):
            bits.append(int((left, right) in edge_set))
    while len(bits) % 6:
        bits.append(0)
    return chr(vertices + 63) + "".join(
        chr(63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6)))
        for offset in range(0, len(bits), 6)
    )


def shortest_distance(
    edges: tuple[tuple[int, int], ...],
    initial: tuple[int, ...],
    roots: tuple[int, int],
    length: int,
) -> tuple[int, int]:
    vertices = 1 + max(max(edge) for edge in edges)
    incidence = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    cuts = (
        ((5, 6),)
        + tuple((8 + 3 * index, 9 + 3 * index) for index in range(length))
        + ((8 + 3 * length, 9 + 3 * length),)
    )

    def components(selected):
        unseen = set(selected)
        answer = []
        while unseen:
            first = unseen.pop()
            component = {first}
            queue = [first]
            while queue:
                edge = queue.pop()
                for vertex in edges[edge]:
                    for other in incidence[vertex]:
                        if other in unseen:
                            unseen.remove(other)
                            component.add(other)
                            queue.append(other)
            answer.append(tuple(sorted(component)))
        return answer

    def factor_components(state, pair):
        mask = (1 << pair[0]) | (1 << pair[1])
        return components(
            edge
            for edge, label in enumerate(state)
            if (label & mask).bit_count() == 1
        )

    def root_good(state):
        return any(
            roots[0] in component and roots[1] in component
            for pair in PAIRS
            for component in factor_components(state, pair)
        )

    seen = {initial}
    queue = deque([(initial, 0)])
    while queue:
        state, distance = queue.popleft()
        assert all(state[left] == state[right] for left, right in cuts)
        if root_good(state):
            return distance, len(seen)
        for pair in PAIRS:
            mask = (1 << pair[0]) | (1 << pair[1])
            for component in factor_components(state, pair):
                if sum(root in component for root in roots) != 1:
                    continue
                # This checks the structural prefix/suffix assertion used
                # in the human lower-bound proof on every move reached by
                # the literal BFS.
                crossed = []
                for cut, (left, right) in enumerate(cuts):
                    assert (left in component) == (right in component)
                    if left in component:
                        crossed.append(cut)
                if roots[0] in component:
                    assert crossed == list(range(len(crossed)))
                else:
                    assert roots[1] in component
                    assert crossed == list(
                        range(len(cuts) - len(crossed), len(cuts))
                    )
                other = list(state)
                for edge in component:
                    other[edge] ^= mask
                    assert other[edge].bit_count() == 2
                other = tuple(other)
                for cut, (left, right) in enumerate(cuts):
                    expected = (
                        state[left] ^ mask
                        if cut in crossed
                        else state[left]
                    )
                    assert other[left] == other[right] == expected
                if other not in seen:
                    seen.add(other)
                    queue.append((other, distance + 1))
    raise AssertionError("root-component orbit has no rescue")


def validate_graph_and_flow(edges, state, length):
    vertices = 2 * length + 10
    incidence = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        assert left != right
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert len(edges) == 3 * vertices // 2
    assert len(set(tuple(sorted(edge)) for edge in edges)) == len(edges)
    assert all(len(row) == 3 for row in incidence)
    assert all(label in (A, B, C) for label in state)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in incidence
    )
    # Every edge lies on a cycle iff deleting it keeps this connected graph
    # connected.  Check that directly.
    for removed in range(len(edges)):
        seen = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for edge in incidence[vertex]:
                if edge == removed:
                    continue
                other = edges[edge][0] ^ edges[edge][1] ^ vertex
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        assert len(seen) == vertices


def validate_cut_word_hypotheses(edges, state, length, roots):
    """Check the finite graph hypotheses used in the written theorem."""
    vertices = 2 * length + 10
    cuts = (
        ((5, 6),)
        + tuple((8 + 3 * index, 9 + 3 * index) for index in range(length))
        + ((8 + 3 * length, 9 + 3 * length),)
    )
    word = tuple(state[left] for left, right in cuts)
    assert all(state[left] == state[right] for left, right in cuts)
    assert word == tuple((A, C, B)[index % 3] for index in range(length + 2))
    for start in range(0, 3 * ((length + 2) // 3), 3):
        assert word[start] ^ word[start + 1] ^ word[start + 2] == 0

    # Each displayed pair is an actual nested two-edge cut separating the
    # left root edge from the right root edge.
    for cut in cuts:
        removed = set(cut)
        incidence = [[] for _ in range(vertices)]
        for edge, (left, right) in enumerate(edges):
            if edge not in removed:
                incidence[left].append(right)
                incidence[right].append(left)
        component = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for other in incidence[vertex]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        assert 0 < len(component) < vertices
        assert all(vertex in component for vertex in edges[roots[0]])
        assert all(vertex not in component for vertex in edges[roots[1]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=4, choices=range(1, 7))
    args = parser.parse_args()
    for length in range(1, args.through + 1):
        edges, state = capped_ladder(length)
        validate_graph_and_flow(edges, state, length)
        roots, expected = SELECTED[length]
        validate_cut_word_hypotheses(edges, state, length, roots)
        distance, discovered = shortest_distance(
            edges, state, roots, length
        )
        assert distance == expected
        theoretical_lower_bound = (length + 2) // 3
        assert distance >= theoretical_lower_bound
        print(
            f"L_{length}: n={2 * length + 10}, graph6="
            f"{short_graph6(2 * length + 10, edges)}, roots={roots}, "
            f"distance={distance}, word_bound={theoretical_lower_bound}, "
            f"discovered={discovered}"
        )
    print("PASS: every displayed distance is an exact literal-BFS distance")


if __name__ == "__main__":
    main()
