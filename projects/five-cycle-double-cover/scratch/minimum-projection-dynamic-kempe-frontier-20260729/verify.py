#!/usr/bin/env python3
"""Exact local checker for the dynamic-Kempe frontier lemmas.

No third-party package or solver is used.  The checker exhausts every proper
three-edge-colouring of K_{3,3} and its edge-deleted two-pole, constructs the
literal Kempe graph, checks boundary-orbit reflection, verifies chain
distances, and audits the one-circuit/two-terminal cleaning construction on
every pairing through support size fourteen.
"""

from __future__ import annotations

import itertools
from collections import deque


COLOURS = (1, 2, 3)
PAIRS = ((1, 2), (1, 3), (2, 3))
PERMUTATIONS = tuple(
    (0,) + permutation for permutation in itertools.permutations(COLOURS)
)
LEFT = (0, 1, 2)
RIGHT = (3, 4, 5)
DELETED = (0, 3)
FULL_EDGES = tuple((u, v) for u in LEFT for v in RIGHT)
POLE_EDGES = (
    (6, 0),
    (3, 7),
) + tuple(edge for edge in FULL_EDGES if edge != DELETED)


def enumerate_proper(edges, constrained_vertices):
    incident = {vertex: [] for vertex in constrained_vertices}
    for edge_index, (u, v) in enumerate(edges):
        if u in incident:
            incident[u].append(edge_index)
        if v in incident:
            incident[v].append(edge_index)
    assert all(len(row) == 3 for row in incident.values())
    edge_vertices = tuple(
        tuple(vertex for vertex in edge if vertex in incident)
        for edge in edges
    )
    values = [0] * len(edges)
    used = {vertex: 0 for vertex in incident}
    result = []

    def recurse(done):
        if done == len(edges):
            result.append(tuple(values))
            return
        best = -1
        best_domain = None
        for edge_index, value in enumerate(values):
            if value:
                continue
            forbidden = 0
            for vertex in edge_vertices[edge_index]:
                forbidden |= used[vertex]
            domain = tuple(
                colour
                for colour in COLOURS
                if not forbidden & (1 << colour)
            )
            if not domain:
                return
            if best_domain is None or len(domain) < len(best_domain):
                best, best_domain = edge_index, domain
                if len(domain) == 1:
                    break
        for colour in best_domain:
            values[best] = colour
            for vertex in edge_vertices[best]:
                used[vertex] |= 1 << colour
            recurse(done + 1)
            for vertex in edge_vertices[best]:
                used[vertex] ^= 1 << colour
            values[best] = 0

    recurse(0)
    return tuple(result)


def extend_pole(colouring):
    assert colouring[0] == colouring[1]
    internal = iter(colouring[2:])
    return tuple(
        colouring[0] if edge == DELETED else next(internal)
        for edge in FULL_EDGES
    )


def colour_orbits(colourings):
    remaining = set(colourings)
    result = []
    while remaining:
        root = min(remaining)
        orbit = {
            tuple(permutation[value] for value in root)
            for permutation in PERMUTATIONS
        }
        assert orbit <= remaining
        remaining -= orbit
        result.append(frozenset(orbit))
    return tuple(result)


def bichromatic_components(edges, colouring, pair):
    adjacency = [[] for _ in range(8)]
    for edge_index, ((u, v), colour) in enumerate(zip(edges, colouring)):
        if colour not in pair:
            continue
        adjacency[u].append((v, edge_index))
        adjacency[v].append((u, edge_index))
    seen = set()
    result = []
    for edge_index, colour in enumerate(colouring):
        if colour not in pair or edge_index in seen:
            continue
        stack = [edge_index]
        seen.add(edge_index)
        row = []
        vertices = set()
        while stack:
            current = stack.pop()
            row.append(current)
            u, v = edges[current]
            vertices.update((u, v))
            for endpoint in (u, v):
                for _neighbour, following in adjacency[endpoint]:
                    if following not in seen:
                        seen.add(following)
                        stack.append(following)
        terminals = tuple(sorted(vertices & {6, 7}))
        result.append((terminals, tuple(sorted(row))))
    return tuple(result)


def switched(colouring, row, pair):
    first, second = pair
    result = list(colouring)
    for edge_index in row:
        assert result[edge_index] in pair
        result[edge_index] = (
            second if result[edge_index] == first else first
        )
    return tuple(result)


def connected_components(vertices, neighbours):
    unseen = set(vertices)
    result = []
    while unseen:
        root = min(unseen)
        reached = {root}
        queue = deque([root])
        while queue:
            current = queue.popleft()
            for following in neighbours[current]:
                if following not in reached:
                    reached.add(following)
                    queue.append(following)
        unseen -= reached
        result.append(frozenset(reached))
    return tuple(result)


def pole_audit():
    full = enumerate_proper(FULL_EDGES, range(6))
    pole = enumerate_proper(POLE_EDGES, range(6))
    assert len(full) == len(pole) == 12
    assert all(row[0] == row[1] for row in pole)
    assert {extend_pole(row) for row in pole} == set(full)

    full_orbits = colour_orbits(full)
    assert sorted(map(len, full_orbits)) == [6, 6]
    orbit_id = {
        colouring: index
        for index, orbit in enumerate(full_orbits)
        for colouring in orbit
    }

    pole_set = set(pole)
    neighbours = {row: set() for row in pole}
    terminal_moves = internal_moves = 0
    for colouring in pole:
        terminal_colour = colouring[0]
        source_orbit = orbit_id[extend_pole(colouring)]
        for pair in PAIRS:
            components = bichromatic_components(POLE_EDGES, colouring, pair)
            assert len(components) == 1
            terminals, edge_row = components[0]
            if terminal_colour in pair:
                assert terminals == (6, 7)
                terminal_moves += 1
            else:
                assert terminals == ()
                internal_moves += 1
            following = switched(colouring, edge_row, pair)
            assert following in pole_set
            assert orbit_id[extend_pole(following)] == source_orbit
            if terminals:
                assert following[0] == following[1]
                assert following[0] != terminal_colour
            else:
                assert following[:2] == colouring[:2]
            neighbours[colouring].add(following)
            neighbours[following].add(colouring)
    assert (terminal_moves, internal_moves) == (24, 12)
    kempe = connected_components(pole, neighbours)
    assert sorted(map(len, kempe)) == [6, 6]
    assert {
        frozenset(extend_pole(row) for row in component)
        for component in kempe
    } == set(full_orbits)
    return len(full), tuple(sorted(map(len, kempe)))


def shortest_distance(vertex_count, edges, source, target):
    adjacency = [[] for _ in range(vertex_count)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    distance = {source: 0}
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        if vertex == target:
            return distance[vertex]
        for following in adjacency[vertex]:
            if following not in distance:
                distance[following] = distance[vertex] + 1
                queue.append(following)
    return None


def chain_graph(copies):
    # Vertices 0,1 are the old endpoints.  Each copy uses six new vertices.
    edges = []
    blocks = []
    for copy in range(copies):
        offset = 2 + 6 * copy
        block = tuple(offset + local for local in range(6))
        blocks.append(block)
        edges.extend(
            (block[u], block[v])
            for u, v in FULL_EDGES
            if (u, v) != DELETED
        )
    edges.append((0, blocks[0][0]))
    for copy in range(copies - 1):
        edges.append((blocks[copy][3], blocks[copy + 1][0]))
    edges.append((blocks[-1][3], 1))
    return 2 + 6 * copies, tuple(edges)


def chain_audit():
    distances = []
    for copies in range(1, 9):
        order, edges = chain_graph(copies)
        distance = shortest_distance(order, edges, 0, 1)
        assert distance == 4 * copies + 1
        distances.append(distance)
    return tuple(distances)


def pairings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in pairings(rest):
            yield ((first, second),) + tail


def clean_alternating_pairing(order, matching):
    owner = [-1] * order
    for block, (first, second) in enumerate(matching):
        owner[first] = owner[second] = block
    # d_i=1 around the circuit.  Prefix integration alternates 1,0.
    support = []
    value = 0
    for _position in range(order):
        value ^= 1
        support.append(value)
    parity = [[0] * 4 for _ in matching]
    for edge in range(order):
        successor = (edge + 1) % order
        if owner[edge] == owner[successor]:
            continue
        colour = support[edge]
        parity[owner[edge]][colour] ^= 1
        parity[owner[successor]][colour] ^= 1
    return not any(bit for row in parity for bit in row)


def two_terminal_audit():
    counts = {}
    for order in range(2, 15, 2):
        count = 0
        for matching in pairings(tuple(range(order))):
            assert clean_alternating_pairing(order, matching)
            count += 1
        expected = 1
        for odd in range(1, order, 2):
            expected *= odd
        assert count == expected
        counts[order] = count
    return counts


def main():
    colourings, orbit_sizes = pole_audit()
    distances = chain_audit()
    counts = two_terminal_audit()
    print(
        "K33_EDGE_DELETED_POLE"
        f" proper_colourings={colourings}"
        " equal_terminal_colour=yes"
        f" kempe_orbits={len(orbit_sizes)}"
        " orbit_sizes=" + ",".join(map(str, orbit_sizes))
        + " boundary_orbit_reflecting=yes"
    )
    print(
        "CHAIN_DISTANCE copies=1..8 values="
        + ",".join(map(str, distances))
        + " formula=4r+1"
    )
    print(
        "TWO_TERMINAL_ONE_CIRCUIT"
        " pairing_counts="
        + ",".join(f"{order}:{count}" for order, count in counts.items())
        + " all_clean=yes"
    )
    print(
        "PASS: the orbit-reflecting pole and the universal direct-cleaning"
        " construction pass all finite local audits"
    )


if __name__ == "__main__":
    main()
