#!/usr/bin/env python3
"""Check the capped-ladder H=0 family and its unbounded-delay hypotheses."""

from __future__ import annotations

import argparse
import functools
import itertools
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
for item in (str(PROJECT_ROOT), str(PROJECT_ROOT / "scratch")):
    if item not in sys.path:
        sys.path.insert(0, item)

from check_d5_capped_ladder_delay_family import (  # noqa: E402
    B,
    capped_ladder,
    shortest_distance,
    validate_graph_and_flow,
)


PAIRS = tuple(itertools.combinations(range(5), 2))
P = (0, 3, 4, 5, 6, 7)
Q = (0, 1, 2, 3)
LINE = ((1, 3), (3, 4), (1, 4))
EXACT = {
    2: (2, 2),
    3: (3, 3),
    4: (3, 3),
    5: (6, 6),
    6: (8, 8),
}


def machinery(edges):
    vertices = 1 + max(max(edge) for edge in edges)
    incidence = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)

    def components(state, pair):
        mask = (1 << pair[0]) | (1 << pair[1])
        unseen = {
            edge
            for edge, label in enumerate(state)
            if (label & mask).bit_count() == 1
        }
        answer = []
        while unseen:
            first = min(unseen)
            unseen.remove(first)
            component = {first}
            stack = [first]
            while stack:
                edge = stack.pop()
                for vertex in edges[edge]:
                    for other in incidence[vertex]:
                        if other in unseen:
                            unseen.remove(other)
                            component.add(other)
                            stack.append(other)
            answer.append(tuple(sorted(component)))
        return tuple(answer)

    def switch(state, pair, component):
        mask = (1 << pair[0]) | (1 << pair[1])
        answer = list(state)
        for edge in component:
            answer[edge] ^= mask
            assert answer[edge].bit_count() == 2
        return tuple(answer)

    return components, switch


def construct(length):
    edges, tait = capped_ladder(length)
    components, switch = machinery(edges)
    first = next(
        component
        for component in components(tait, (0, 3))
        if 0 in component
    )
    assert first == P
    state = switch(tait, (0, 3), first)
    second = next(
        component
        for component in components(state, (2, 4))
        if 0 in component
    )
    assert second == Q
    state = switch(state, (2, 4), second)

    # The right cap occupies these five final internal-edge positions.
    right_cap = range(10 + 3 * length, 15 + 3 * length)
    second_root = next(edge for edge in right_cap if state[edge] == B)
    roots = (0, second_root)
    return edges, tait, state, roots


def root_good(components, state, roots):
    return any(
        all(root in component for root in roots)
        for pair in PAIRS
        for component in components(state, pair)
    )


def audit_length(length, do_bfs):
    edges, tait, state, roots = construct(length)
    validate_graph_and_flow(edges, tait, length)
    vertices = 2 * length + 10
    incidence = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in incidence
    )
    components, switch = machinery(edges)
    assert state[roots[0]] == 0b11000  # 34
    assert state[roots[1]] == 0b00101  # 02
    assert not (state[roots[0]] & state[roots[1]])
    assert functools.reduce(int.__or__, state, 0) == 0b11111

    cuts = (
        ((5, 6),)
        + tuple((8 + 3 * index, 9 + 3 * index) for index in range(length))
        + ((8 + 3 * length, 9 + 3 * length),)
    )
    initial_word = tuple(state[left] for left, right in cuts)
    assert all(state[left] == state[right] for left, right in cuts)
    assert initial_word[0] == 0b01010  # 13
    assert initial_word[1:] == tuple(
        (0b00110, 0b00101, 0b00011)[index % 3]
        for index in range(length + 1)
    )

    assert not root_good(components, state, roots)
    endpoint = state
    circuits = []
    words = [initial_word]
    for pair, expected in zip(LINE, (Q, P, Q)):
        component = next(
            component
            for component in components(endpoint, pair)
            if roots[0] in component
        )
        assert component == expected
        assert roots[1] not in component
        circuits.append(component)
        endpoint = switch(endpoint, pair, component)
        assert not root_good(components, endpoint, roots)
        assert all(endpoint[left] == endpoint[right] for left, right in cuts)
        words.append(tuple(endpoint[left] for left, right in cuts))

    assert circuits[0] == circuits[2] == Q
    assert tuple(sorted(set(circuits[0]) ^ set(circuits[1]))) == (
        1, 2, 4, 5, 6, 7
    )
    assert words[0] == words[1]
    assert words[2] == words[3]
    assert words[2][0] == 0b10010  # 14
    assert words[2][1:] == words[0][1:]

    # The human lower bound uses disjoint zero-xor triples in this tail.
    triples = [
        initial_word[start : start + 3]
        for start in range(1, 1 + 3 * ((length + 1) // 3), 3)
    ]
    assert len(triples) == (length + 1) // 3
    assert all(left ^ middle ^ right == 0 for left, middle, right in triples)

    distances = None
    if do_bfs:
        distances = (
            shortest_distance(edges, state, roots, length)[0],
            shortest_distance(edges, endpoint, roots, length)[0],
        )
        assert distances == EXACT[length]
    return roots, distances, (length + 1) // 3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=5)
    args = parser.parse_args()
    assert args.through >= 2
    for length in range(2, args.through + 1):
        roots, distances, bound = audit_length(
            length, do_bfs=length in EXACT and length <= args.through
        )
        print(
            f"L_{length}: n={2 * length + 10}, roots={roots}, "
            f"H=0, Z=(1,2,4,5,6,7), word_bound={bound}, "
            f"exact_distances={distances}"
        )
    print(
        "PASS: uniform H=0 capped-ladder construction and "
        "unbounded cut-word lower-bound hypotheses"
    )


if __name__ == "__main__":
    main()
