#!/usr/bin/env python3
"""Literal realizations of the two surviving adverse matching systems."""

from __future__ import annotations

import itertools

from matching_game import COLOUR_PAIRS, DERIVATIVE, LENGTHS, WORD, classify


PARTITIONS = (
    "0001234000314200",
    "0123444444130244",
)

BAD_PATHS = {
    PARTITIONS[0]: {
        (1, 2): (
            (0, (1, 7)),
            (0, (2, 15)),
            (0, (8, 9)),
            (1, (3, 11)),
            (2, (4, 13)),
            (3, (5, 10)),
        ),
        (1, 3): (
            (0, (0, 1)),
            (0, (2, 7)),
            (0, (9, 14)),
            (1, (3, 11)),
            (2, (4, 13)),
            (3, (5, 10)),
            (4, (6, 12)),
        ),
        (2, 3): (
            (0, (0, 8)),
            (0, (14, 15)),
            (4, (6, 12)),
        ),
    },
    PARTITIONS[1]: {
        (1, 2): (
            (1, (1, 10)),
            (2, (2, 13)),
            (3, (3, 11)),
            (4, (4, 15)),
            (4, (5, 7)),
            (4, (8, 9)),
        ),
        (1, 3): (
            (0, (0, 12)),
            (1, (1, 10)),
            (2, (2, 13)),
            (3, (3, 11)),
            (4, (4, 7)),
            (4, (5, 6)),
            (4, (9, 14)),
        ),
        (2, 3): (
            (0, (0, 12)),
            (4, (6, 8)),
            (4, (14, 15)),
        ),
    },
}

# Local vertices 0,...,7 of the ten-vertex large multipole receive these
# boundary occurrences.  The first row is a colour-preserving reattachment
# of the second row's already known adverse transition system.
BIG_TERMINAL_ORDER = {
    PARTITIONS[0]: (2, 1, 0, 7, 8, 9, 14, 15),
    PARTITIONS[1]: (4, 5, 6, 7, 8, 9, 14, 15),
}

LARGE_INTERNAL_MATCHINGS = {
    1: ((2, 4), (6, 7), (8, 9)),
    2: ((0, 6), (1, 3), (2, 8), (5, 9)),
    3: ((0, 3), (1, 9), (4, 8), (5, 7)),
}

EXPECTED_REALIZATIONS = {
    PARTITIONS[0]: (
        "ihCGKC??G?_@?@??_?G@@C???C???W??[G????O???@_??F@????A"
        "??????W???F?_????A???????W????[_????O????C??????G???E?G"
        "???A?C??????C??C???_??B?????A_?????PG",
        "121212123212121233311223331122333112233311223333113321222131132",
    ),
    PARTITIONS[1]: (
        r"ihCGKC??G?_@?@??_?G@@_???A???W??\????A????@_??FG?????O"
        r"?????W???FC?????C???????W????[G????@?????C?????G???E?G?"
        r"??A?C??????C??C???_??B?????A_?????PG",
        "121212123121212133311223331122333112233311223333223312111232231",
    ),
}


def add_edge(edges, first, second, low, kind):
    assert first != second
    edges.append((min(first, second), max(first, second), low, kind))


def build_graph(partition_text: str):
    owner = tuple(map(int, partition_text))
    big = next(
        block
        for block in range(5)
        if sum(value == block for value in owner) == 8
    )
    edges = []
    offset = 0
    for length in LENGTHS:
        for local in range(length):
            add_edge(
                edges,
                offset + local,
                offset + (local + 1) % length,
                WORD[offset + local],
                "support",
            )
        offset += length

    block_vertices = {}
    next_vertex = 16
    for block in range(5):
        if block == big:
            continue
        occurrences = tuple(
            position
            for position, value in enumerate(owner)
            if value == block
        )
        assert len(occurrences) == 2
        terminal_colour = DERIVATIVE[occurrences[0]]
        assert DERIVATIVE[occurrences[1]] == terminal_colour
        vertices = tuple(range(next_vertex, next_vertex + 4))
        next_vertex += 4
        block_vertices[block] = set(vertices)
        add_edge(
            edges, occurrences[0], vertices[0], terminal_colour, "boundary"
        )
        add_edge(
            edges, occurrences[1], vertices[1], terminal_colour, "boundary"
        )
        other = tuple(
            colour for colour in (1, 2, 3) if colour != terminal_colour
        )
        add_edge(
            edges, vertices[2], vertices[3], terminal_colour, "internal"
        )
        add_edge(edges, vertices[0], vertices[2], other[0], "internal")
        add_edge(edges, vertices[1], vertices[3], other[0], "internal")
        add_edge(edges, vertices[0], vertices[3], other[1], "internal")
        add_edge(edges, vertices[1], vertices[2], other[1], "internal")

    vertices = tuple(range(next_vertex, next_vertex + 10))
    next_vertex += 10
    assert next_vertex == 42
    block_vertices[big] = set(vertices)
    terminals = BIG_TERMINAL_ORDER[partition_text]
    assert {position for position, value in enumerate(owner) if value == big} == (
        set(terminals)
    )
    assert tuple(DERIVATIVE[position] for position in terminals) == (
        1, 1, 3, 1, 2, 1, 3, 2
    )
    for local, occurrence in enumerate(terminals):
        add_edge(
            edges,
            occurrence,
            vertices[local],
            DERIVATIVE[occurrence],
            "boundary",
        )
    for low, matching in LARGE_INTERNAL_MATCHINGS.items():
        for first, second in matching:
            add_edge(
                edges,
                vertices[first],
                vertices[second],
                low,
                "internal",
            )
    return 42, tuple(edges), block_vertices


def adjacency(n, edges, selected=None):
    result = [[] for _ in range(n)]
    for index, (first, second, low, kind) in enumerate(edges):
        if selected is not None and not selected(index, low, kind):
            continue
        result[first].append((second, index))
        result[second].append((first, index))
    return result


def connected(n, edges) -> bool:
    graph = adjacency(n, edges)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour, _edge in graph[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == n


def bridges(n, edges):
    graph = adjacency(n, edges)
    discovery = [-1] * n
    lowlink = [0] * n
    timer = 0
    result = []

    def visit(vertex, parent_edge):
        nonlocal timer
        discovery[vertex] = lowlink[vertex] = timer
        timer += 1
        for neighbour, edge in graph[vertex]:
            if edge == parent_edge:
                continue
            if discovery[neighbour] < 0:
                visit(neighbour, edge)
                lowlink[vertex] = min(lowlink[vertex], lowlink[neighbour])
                if lowlink[neighbour] > discovery[vertex]:
                    result.append(edge)
            else:
                lowlink[vertex] = min(
                    lowlink[vertex], discovery[neighbour]
                )

    visit(0, -1)
    assert all(value >= 0 for value in discovery)
    return tuple(sorted(result))


def induced_pairs(
    n,
    edges,
    block_vertices,
    owner,
    block,
    colours,
):
    terminals = {
        position
        for position, value in enumerate(owner)
        if value == block and DERIVATIVE[position] in colours
    }
    allowed = set(block_vertices[block]) | terminals
    graph = adjacency(
        n,
        edges,
        lambda _index, low, kind: kind != "support" and low in colours,
    )
    seen = set()
    answer = []
    for terminal in sorted(terminals):
        if terminal in seen:
            continue
        endpoints = []
        stack = [terminal]
        seen.add(terminal)
        while stack:
            vertex = stack.pop()
            if vertex in terminals:
                endpoints.append(vertex)
            for neighbour, _edge in graph[vertex]:
                if neighbour in allowed and neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        assert len(endpoints) == 2
        answer.append(tuple(sorted(endpoints)))
    return tuple(sorted(answer))


def switched(transitions, paths, mask, delta):
    result = list(transitions)
    closure = [0, 0]
    for index, (_block, pair) in enumerate(paths):
        if not (mask >> index) & 1:
            continue
        for endpoint in pair:
            result[endpoint] ^= delta
            closure[int(endpoint >= 8)] ^= delta
    return tuple(result) if closure == [0, 0] else None


def find_tait_colouring(n, edges):
    incident = [[] for _ in range(n)]
    for edge, (first, second, _low, _kind) in enumerate(edges):
        incident[first].append(edge)
        incident[second].append(edge)
    colour = [0] * len(edges)
    used = [0] * n

    def recurse(done):
        if done == len(edges):
            return True
        best = None
        domain = None
        for edge, (first, second, _low, _kind) in enumerate(edges):
            if colour[edge]:
                continue
            choices = tuple(
                value
                for value in (1, 2, 3)
                if not used[first] & (1 << value)
                and not used[second] & (1 << value)
            )
            if not choices:
                return False
            if best is None or len(choices) < len(domain):
                best, domain = edge, choices
        first, second, _low, _kind = edges[best]
        for value in domain:
            colour[best] = value
            used[first] |= 1 << value
            used[second] |= 1 << value
            if recurse(done + 1):
                return True
            used[first] ^= 1 << value
            used[second] ^= 1 << value
            colour[best] = 0
        return False

    return tuple(colour) if recurse(0) else None


def graph6(n, edges):
    pairs = {(first, second) for first, second, _low, _kind in edges}
    bits = []
    for second in range(1, n):
        for first in range(second):
            bits.append(int((first, second) in pairs))
    while len(bits) % 6:
        bits.append(0)
    return chr(n + 63) + "".join(
        chr(
            63
            + sum(bits[offset + bit] << (5 - bit) for bit in range(6))
        )
        for offset in range(0, len(bits), 6)
    )


def audit(partition_text: str):
    owner = tuple(map(int, partition_text))
    n, edges, block_vertices = build_graph(partition_text)
    assert len(edges) == 63
    assert len({(first, second) for first, second, _low, _kind in edges}) == 63
    graph = adjacency(n, edges)
    assert all(len(row) == 3 for row in graph)
    assert connected(n, edges)
    assert bridges(n, edges) == ()

    for vertex in range(n):
        first_charge = low_charge = 0
        for _neighbour, edge in graph[vertex]:
            _first, _second, low, kind = edges[edge]
            first_charge ^= int(kind == "support")
            low_charge ^= low
        assert first_charge == low_charge == 0

    observed = {}
    for colours in COLOUR_PAIRS:
        paths = []
        for block in range(5):
            paths.extend(
                (block, pair)
                for pair in induced_pairs(
                    n,
                    edges,
                    block_vertices,
                    owner,
                    block,
                    colours,
                )
            )
        observed[colours] = tuple(paths)
        assert observed[colours] == BAD_PATHS[partition_text][colours]

        delta = colours[0] ^ colours[1]
        balanced = 0
        for mask in range(1, 1 << len(paths)):
            changed = switched(DERIVATIVE, paths, mask, delta)
            if changed is None:
                continue
            balanced += 1
            result = classify(changed, owner)
            assert result[0] == 320
            assert result[1] == result[2] == 0
        assert balanced == {6: 31, 7: 63, 3: 3}[len(paths)]

    tait = find_tait_colouring(n, edges)
    assert tait is not None
    for vertex in range(n):
        assert {
            tait[edge] for _neighbour, edge in graph[vertex]
        } == {1, 2, 3}
    encoded = graph6(n, edges)
    tait_text = "".join(map(str, tait))
    assert (encoded, tait_text) == EXPECTED_REALIZATIONS[partition_text]
    return n, len(edges), encoded, tait_text


def main():
    for partition in PARTITIONS:
        n, m, encoded, tait = audit(partition)
        print(
            f"REALIZATION partition={partition}"
            f" vertices={n} edges={m}"
            " simple=yes cubic=yes connected=yes bridgeless=yes"
            " simultaneous_bad_matchings=yes"
            " one_round_rescue=no"
            " tait=yes minimum_projection_size=0"
        )
        print(f" LABELLED_GRAPH6 {encoded}")
        print(f" TAIT_COLOURING {tait}")
    print("PASS literal realizations of both surviving matching systems")


if __name__ == "__main__":
    main()
