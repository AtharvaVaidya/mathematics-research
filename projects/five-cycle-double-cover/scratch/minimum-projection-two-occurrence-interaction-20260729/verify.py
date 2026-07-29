#!/usr/bin/env python3
"""Exact verifier for the two-occurrence interaction model and Petersen no-go."""

from __future__ import annotations

import functools
import itertools
from collections import deque


K = range(4)
KSTAR = (1, 2, 3)
GL = tuple((0,) + row for row in itertools.permutations(KSTAR))
IDENTITY = (0, 1, 2, 3)
ORDER_A = (0, 1, 2, 3, 4)
ORDER_B = (0, 3, 1, 4, 2)
INITIAL_FLOW = (1, 1, 1, 2, 3)
EXPECTED_TABLE = (
    ("11123", "10130", 3, "13210", 4),
    ("11213", "10230", 4, "10120", 3),
    ("11231", "10210", 3, "12320", 4),
    ("12113", "13230", 4, "10210", 3),
    ("12131", "13210", 4, "12010", 3),
    ("12223", "13130", 3, "13120", 4),
    ("12232", "13120", 4, "12020", 3),
    ("12311", "13010", 3, "10230", 4),
    ("12322", "13020", 4, "13130", 3),
    ("12333", "13030", 3, "12030", 4),
)


def xor_all(values):
    return functools.reduce(int.__xor__, values, 0)


def flows(edge_count):
    return tuple(
        values
        for values in itertools.product(KSTAR, repeat=edge_count)
        if xor_all(values) == 0
    )


def traverse(values, order, start=0):
    current = start
    word = []
    lines = {}
    for edge in order:
        before = current
        current ^= values[edge]
        word.append(current)
        lines[edge] = frozenset((before, current))
    assert current == start
    return tuple(word), lines


def clean_shifts(values):
    _word_a, lines_a = traverse(values, ORDER_A, 0)
    result = []
    for shift in K:
        _word_b, lines_b = traverse(values, ORDER_B, shift)
        if lines_a == lines_b:
            result.append(shift)
    return tuple(result)


def global_gl_orbit(values):
    return {
        tuple(mapping[value] for value in values)
        for mapping in GL
    }


def table_and_boundary_census():
    all_flows = flows(5)
    assert len(all_flows) == 60
    unseen = set(all_flows)
    rows = []
    while unseen:
        representative = min(unseen)
        orbit = global_gl_orbit(representative)
        assert len(orbit) == 6
        unseen -= orbit
        word_a, _lines_a = traverse(representative, ORDER_A)
        word_b, _lines_b = traverse(representative, ORDER_B)
        rows.append(
            (
                "".join(map(str, representative)),
                "".join(map(str, word_a)),
                len(set(word_a)),
                "".join(map(str, word_b)),
                len(set(word_b)),
            )
        )
    rows.sort()
    assert tuple(rows) == EXPECTED_TABLE

    clean = deletable = 0
    for values in all_flows:
        clean += bool(clean_shifts(values))
        word_a, _ = traverse(values, ORDER_A)
        word_b, _ = traverse(values, ORDER_B)
        deletable += min(len(set(word_a)), len(set(word_b))) < 4
    assert clean == 0
    assert deletable == 60
    return tuple(rows), len(all_flows), clean, deletable


def normalized_map_census():
    feasible = clean = deletable = 0
    for tail in itertools.product(GL, repeat=4):
        maps = (IDENTITY,) + tail
        values = tuple(
            maps[edge][INITIAL_FLOW[edge]] for edge in range(5)
        )
        if xor_all(values):
            continue
        feasible += 1
        clean += bool(clean_shifts(values))
        word_a, _ = traverse(values, ORDER_A)
        word_b, _ = traverse(values, ORDER_B)
        deletable += min(len(set(word_a)), len(set(word_b))) < 4
    assert (feasible, clean, deletable) == (320, 0, 320)
    return feasible, clean, deletable


def perfect_matchings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def pairing_owner(pairing, order):
    owner = [-1] * order
    for edge, endpoints in enumerate(pairing):
        for endpoint in endpoints:
            owner[endpoint] = edge
    assert all(value >= 0 for value in owner)
    return tuple(owner)


def shape_circuits(shape):
    result = []
    offset = 0
    for length in shape:
        result.append(tuple(range(offset, offset + length)))
        offset += length
    return tuple(result)


def generic_clean(pairing, circuits, values):
    order = sum(map(len, circuits))
    owner = pairing_owner(pairing, order)
    occurrence = [[] for _ in pairing]
    line_at = {}
    for circuit_index, circuit in enumerate(circuits):
        current = 0
        for position in circuit:
            edge = owner[position]
            before = current
            current ^= values[edge]
            occurrence[edge].append((circuit_index, before))
        assert current == 0
    for shifts_tail in itertools.product(K, repeat=len(circuits) - 1):
        shifts = (0,) + shifts_tail
        okay = True
        for edge, rows in enumerate(occurrence):
            assert len(rows) == 2
            lines = []
            for circuit_index, before in rows:
                first = before ^ shifts[circuit_index]
                lines.append(frozenset((first, first ^ values[edge])))
            if lines[0] != lines[1]:
                okay = False
                break
        if okay:
            return True
    return False


def exhaustive_shape(shape):
    order = sum(shape)
    circuits = shape_circuits(shape)
    total = flowable = cleanable = 0
    for pairing in perfect_matchings(tuple(range(order))):
        total += 1
        owner = pairing_owner(pairing, order)
        candidates = []
        for values in itertools.product(KSTAR, repeat=order // 2):
            if all(
                xor_all(values[owner[position]] for position in circuit) == 0
                for circuit in circuits
            ):
                candidates.append(values)
        if not candidates:
            continue
        flowable += 1
        if any(generic_clean(pairing, circuits, values) for values in candidates):
            cleanable += 1
    return total, flowable, cleanable


def verify_smaller_shapes():
    rows = {
        (2, 2): (3, 3, 3),
        (2, 4): (15, 15, 15),
        (3, 3): (15, 6, 6),
        (2, 2, 2): (15, 15, 15),
        (2, 6): (105, 105, 105),
        (3, 5): (105, 60, 60),
        (4, 4): (105, 105, 105),
        (2, 2, 4): (105, 105, 105),
        (2, 3, 3): (105, 42, 42),
        (2, 2, 2, 2): (105, 105, 105),
    }
    for shape, expected in rows.items():
        assert exhaustive_shape(shape) == expected
    return rows


def add_edge(edges, first, second, low, support, component):
    assert first != second
    key = tuple(sorted((first, second)))
    assert all(tuple(sorted(row[:2])) != key for row in edges)
    edges.append((first, second, low, support, component))


def build_petersen():
    edges = []
    word_a = tuple(map(int, "10130"))
    word_b = tuple(map(int, "13210"))
    for index, low in enumerate(word_a):
        add_edge(edges, index, (index + 1) % 5, low, True, -1)
    for index, low in enumerate(word_b):
        add_edge(edges, 5 + index, 5 + (index + 1) % 5, low, True, -1)
    position_b = {edge: local for local, edge in enumerate(ORDER_B)}
    for component, low in enumerate(INITIAL_FLOW):
        add_edge(
            edges,
            component,
            5 + position_b[component],
            low,
            False,
            component,
        )
    assert len(edges) == 15
    return tuple(edges)


def adjacency(edges, deleted=None, keep=None):
    graph = [[] for _ in range(10)]
    for index, edge in enumerate(edges):
        if index == deleted or (keep is not None and not keep(edge)):
            continue
        first, second = edge[:2]
        graph[first].append((second, index))
        graph[second].append((first, index))
    return graph


def connected(edges, deleted=None, keep=None):
    graph = adjacency(edges, deleted, keep)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbour, _edge in graph[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    return len(seen) == 10


def shortest_cycle(edges):
    best = 100
    for deleted, (source, target, *_tail) in enumerate(edges):
        graph = adjacency(edges, deleted)
        distance = [-1] * 10
        distance[source] = 0
        queue = deque([source])
        while queue and distance[target] < 0:
            vertex = queue.popleft()
            for neighbour, _edge in graph[vertex]:
                if distance[neighbour] < 0:
                    distance[neighbour] = distance[vertex] + 1
                    queue.append(neighbour)
        assert distance[target] >= 0
        best = min(best, distance[target] + 1)
    return best


def tait_colouring(edges):
    incident = [[] for _ in range(10)]
    for edge_index, edge in enumerate(edges):
        for vertex in edge[:2]:
            incident[vertex].append(edge_index)
    assignment = [0] * len(edges)

    def search(remaining):
        if not remaining:
            return tuple(assignment)
        best = None
        domain = None
        for edge in remaining:
            first, second = edges[edge][:2]
            forbidden = {
                assignment[other]
                for vertex in (first, second)
                for other in incident[vertex]
                if assignment[other]
            }
            choices = tuple(colour for colour in KSTAR if colour not in forbidden)
            if not choices:
                return None
            if best is None or len(choices) < len(domain):
                best, domain = edge, choices
        assert best is not None and domain is not None
        tail = tuple(edge for edge in remaining if edge != best)
        for colour in domain:
            assignment[best] = colour
            result = search(tail)
            if result is not None:
                return result
            assignment[best] = 0
        return None

    return search(tuple(range(len(edges))))


def verify_petersen_and_descent():
    edges = build_petersen()
    degree = [0] * 10
    low_xor = [0] * 10
    for first, second, low, _support, _component in edges:
        degree[first] += 1
        degree[second] += 1
        low_xor[first] ^= low
        low_xor[second] ^= low
    assert degree == [3] * 10
    assert low_xor == [0] * 10
    assert connected(edges)
    assert all(connected(edges, deleted=edge) for edge in range(15))
    assert shortest_cycle(edges) == 5
    assert tait_colouring(edges) is None

    # Delete the first support circuit by adding (first,low)=(1,2) on it.
    new_support = []
    new_low = []
    for edge_index, edge in enumerate(edges):
        low = edge[2]
        support = edge[3]
        if edge_index < 5:
            low ^= 2
            support = False
        new_low.append(low)
        new_support.append(support)
    assert all(
        new_support[index] or new_low[index] != 0
        for index in range(len(edges))
    )
    for vertex in range(10):
        incident = [
            index for index, edge in enumerate(edges) if vertex in edge[:2]
        ]
        assert xor_all(new_low[index] for index in incident) == 0
        assert xor_all(int(new_support[index]) for index in incident) == 0
    assert sum(new_support) == 5
    complement = [
        edge for index, edge in enumerate(edges) if not new_support[index]
    ]
    assert connected(tuple(complement))
    return edges, "".join(map(str, new_low)), "".join(
        map(lambda bit: str(int(bit)), new_support)
    )


def main():
    table, flow_count, clean_count, deletion_count = (
        table_and_boundary_census()
    )
    maps = normalized_map_census()
    smaller = verify_smaller_shapes()
    edges, deleted_low, deleted_support = verify_petersen_and_descent()
    print("PASS: two-occurrence interaction counterstate")
    print("interaction=two_vertices_five_parallel_edges")
    print("orders=01234|03142 initial_flow=11123")
    print(
        f"flow_assignments={flow_count} gl_orbits={len(table)} "
        f"clean={clean_count} deletion={deletion_count}"
    )
    print(
        f"normalized_maps feasible={maps[0]} clean={maps[1]} "
        f"deletion={maps[2]}"
    )
    print(
        "smaller_shapes="
        + ",".join(
            "+".join(map(str, shape)) + ":" + "/".join(map(str, counts))
            for shape, counts in smaller.items()
        )
    )
    print("graph=Petersen order=10 size=15 girth=5 bridgeless=yes tait=no")
    print("displayed_support=10 uncleanable=yes")
    print(
        f"deleted_support=5 global_minimum=yes clean=yes "
        f"low={deleted_low} support={deleted_support}"
    )
    print("table:")
    for row in table:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
