#!/usr/bin/env python3
"""Standalone checker refuting local-maximum neutral connectivity.

This file deliberately uses only the Python standard library and contains
the graph and D5-flow state literally.  It verifies:

* the graph is finite, simple, connected, cubic, and bridgeless;
* every edge label is a 2-subset of {0,1,2,3,4} and the three labels at
  every vertex XOR to zero;
* all 24 nonempty single-factor-component transpositions have delta chi
  at most zero, so the state is a local maximum of the surface potential;
* the ten delta-zero factor components induce seven hypergraph components
  on E(G), including six isolated edges.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations


EDGES = (
    (0, 12), (0, 16), (0, 26),
    (1, 13), (1, 17), (1, 27),
    (2, 14), (2, 18), (2, 20),
    (3, 15), (3, 19), (3, 21),
    (4, 14), (4, 24), (4, 26),
    (5, 15), (5, 25), (5, 27),
    (6, 16), (6, 18), (6, 21),
    (7, 17), (7, 19), (7, 20),
    (8, 18), (8, 22), (8, 25),
    (9, 19), (9, 23), (9, 24),
    (10, 22), (10, 24), (10, 27),
    (11, 23), (11, 25), (11, 26),
    (12, 21), (12, 22),
    (13, 20), (13, 23),
    (14, 16), (15, 17),
)

STATE = (
    0x03, 0x09, 0x0A, 0x03, 0x09, 0x0A, 0x0C,
    0x14, 0x18, 0x0C, 0x14, 0x18, 0x14, 0x12,
    0x06, 0x14, 0x12, 0x06, 0x11, 0x18, 0x09,
    0x11, 0x18, 0x09, 0x0C, 0x18, 0x14, 0x0C,
    0x18, 0x14, 0x0A, 0x06, 0x0C, 0x0A, 0x06,
    0x0C, 0x11, 0x12, 0x11, 0x12, 0x18, 0x18,
)

VERTICES = 28
PAIRS = tuple(combinations(range(5), 2))
EXPECTED_ISOLATED_EDGES = (8, 11, 19, 22, 25, 28)


def incidence_rows() -> list[list[int]]:
    rows = [[] for _ in range(VERTICES)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


INCIDENCE = incidence_rows()


def vertex_reachable_without_edge(deleted: int | None) -> set[int]:
    adjacency = [[] for _ in range(VERTICES)]
    for edge, (left, right) in enumerate(EDGES):
        if edge == deleted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                queue.append(other)
    return reached


def active_edges(state: tuple[int, ...], pair: tuple[int, int]) -> set[int]:
    first, second = pair
    return {
        edge
        for edge, label in enumerate(state)
        if ((label >> first) & 1) ^ ((label >> second) & 1)
    }


def factor_components(
    state: tuple[int, ...], pair: tuple[int, int]
) -> list[frozenset[int]]:
    """Return the nonempty edge-components of the pair's active factor."""
    unseen = active_edges(state, pair)
    answer = []
    while unseen:
        seed = next(iter(unseen))
        component = {seed}
        unseen.remove(seed)
        queue = deque([seed])
        while queue:
            edge = queue.popleft()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        queue.append(other)
        answer.append(frozenset(component))
    return answer


def switch(
    state: tuple[int, ...],
    pair: tuple[int, int],
    component: frozenset[int],
) -> tuple[int, ...]:
    first, second = pair
    toggle = (1 << first) | (1 << second)
    answer = []
    for edge, label in enumerate(state):
        if edge in component:
            assert ((label >> first) & 1) ^ ((label >> second) & 1)
            label ^= toggle
        answer.append(label)
    return tuple(answer)


def coordinate_components(state: tuple[int, ...], coordinate: int) -> int:
    """Count nonempty components of the coordinate's even edge-subgraph."""
    unseen = {
        edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    }
    count = 0
    while unseen:
        count += 1
        seed = next(iter(unseen))
        unseen.remove(seed)
        queue = deque([seed])
        while queue:
            edge = queue.popleft()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        queue.append(other)
    return count


def chi(state: tuple[int, ...]) -> int:
    """The surface potential: sum of coordinate circuits - |E| + |V|."""
    return (
        sum(coordinate_components(state, coordinate) for coordinate in range(5))
        - len(EDGES)
        + VERTICES
    )


def validate_flow(state: tuple[int, ...]) -> None:
    assert len(state) == len(EDGES)
    assert all(label.bit_count() == 2 and label < (1 << 5) for label in state)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(
        state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0
        for row in INCIDENCE
    )


def neutral_hypergraph_blocks(
    components: list[frozenset[int]],
) -> list[frozenset[int]]:
    unseen = set(range(len(EDGES)))
    answer = []
    while unseen:
        seed = next(iter(unseen))
        block = {seed}
        unseen.remove(seed)
        queue = deque([seed])
        while queue:
            edge = queue.popleft()
            for component in components:
                if edge not in component:
                    continue
                new = set(component) & unseen
                unseen.difference_update(new)
                block.update(new)
                queue.extend(new)
        answer.append(frozenset(block))
    return answer


def main() -> int:
    assert len(EDGES) == 42
    assert all(left != right for left, right in EDGES)
    assert len({tuple(sorted(edge)) for edge in EDGES}) == len(EDGES)
    assert len(vertex_reachable_without_edge(None)) == VERTICES
    assert all(
        len(vertex_reachable_without_edge(edge)) == VERTICES
        for edge in range(len(EDGES))
    )
    validate_flow(STATE)

    old_chi = chi(STATE)
    moves = []
    for pair in PAIRS:
        for component in factor_components(STATE, pair):
            other = switch(STATE, pair, component)
            validate_flow(other)
            moves.append((pair, component, chi(other) - old_chi))

    delta_histogram = Counter(delta for _, _, delta in moves)
    assert old_chi == -4
    assert len(moves) == 24
    assert delta_histogram == {0: 10, -2: 14}
    assert max(delta_histogram) == 0

    neutral = [component for _, component, delta in moves if delta == 0]
    blocks = neutral_hypergraph_blocks(neutral)
    block_sizes = sorted(len(block) for block in blocks)
    isolated = tuple(
        sorted(next(iter(block)) for block in blocks if len(block) == 1)
    )
    assert block_sizes == [1, 1, 1, 1, 1, 1, 36]
    assert isolated == EXPECTED_ISOLATED_EDGES
    assert all(
        all(edge not in component for component in neutral)
        for edge in isolated
    )

    print("PASS")
    print("graph: 28 vertices, 42 edges, simple connected cubic bridgeless")
    print("D5 flow: verified")
    print(f"surface chi: {old_chi}")
    print(f"nonempty switch delta histogram: {dict(delta_histogram)}")
    print("local chi maximum: yes")
    print(f"neutral hypergraph block sizes: {block_sizes}")
    print(f"isolated edge indices: {list(isolated)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
