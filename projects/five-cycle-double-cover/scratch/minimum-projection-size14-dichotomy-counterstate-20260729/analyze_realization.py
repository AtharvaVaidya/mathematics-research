#!/usr/bin/env python3
"""Construct and exhaustively analyse a simple cubic realization."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
N = 18

# Vertices 0..6 and 7..13 are the two displayed 7-circuits.
# Vertices 14..17 form a cubic tree joining the six vertices in block 4.
EDGES = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11),
        (1, 9),
        (2, 12),
        (3, 10),
        (14, 4),
        (14, 5),
        (14, 15),
        (15, 6),
        (15, 16),
        (16, 13),
        (16, 17),
        (17, 7),
        (17, 8),
    )
)
M = len(EDGES)
ALL = (1 << M) - 1
TARGET_H = (1 << 14) - 1
TARGET_CIRCUITS = (tuple(range(7)), tuple(range(7, 14)))
TARGET_VALUES = (
    tuple(map(int, "0101023"))
    + tuple(map(int, "0101232"))
    + (3, 1, 1, 1, 1, 2, 3, 1, 2, 1, 3, 2, 1)
)


def adjacency(excluded_edge=None):
    result = [[] for _ in range(N)]
    for index, (first, second) in enumerate(EDGES):
        if index == excluded_edge:
            continue
        result[first].append((second, index))
        result[second].append((first, index))
    return result


ADJACENCY = adjacency()


def connected(excluded_edge=None):
    graph = adjacency(excluded_edge)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour, _edge in graph[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == N


def components_without(edge_mask):
    labels = [-1] * N
    component = 0
    for start in range(N):
        if labels[start] >= 0:
            continue
        labels[start] = component
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour, edge in ADJACENCY[vertex]:
                if (edge_mask >> edge) & 1:
                    continue
                if labels[neighbour] < 0:
                    labels[neighbour] = component
                    stack.append(neighbour)
        component += 1
    return tuple(labels), component


def cycle_basis():
    # Fundamental cycles of a rooted spanning tree.
    parent = [-1] * N
    parent_edge = [-1] * N
    parent[0] = 0
    stack = [0]
    tree_edges = set()
    while stack:
        vertex = stack.pop()
        for neighbour, edge in ADJACENCY[vertex]:
            if parent[neighbour] < 0:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge
                tree_edges.add(edge)
                stack.append(neighbour)
    assert all(value >= 0 for value in parent)

    basis = []
    for edge, (first, second) in enumerate(EDGES):
        if edge in tree_edges:
            continue
        first_path = {}
        vertex = first
        mask = 0
        while vertex != 0:
            first_path[vertex] = mask
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        first_path[0] = mask

        second_mask = 0
        vertex = second
        while vertex not in first_path:
            second_mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        basis.append((1 << edge) ^ second_mask ^ first_path[vertex])
    assert len(basis) == M - N + 1 == 10
    return tuple(basis)


def all_cycles(basis):
    result = [0]
    for vector in basis:
        result += [value ^ vector for value in result]
    assert len(result) == 1 << len(basis)
    assert len(set(result)) == len(result)
    return tuple(result)


def is_cycle(mask):
    parity = [0] * N
    for edge, (first, second) in enumerate(EDGES):
        if (mask >> edge) & 1:
            parity[first] ^= 1
            parity[second] ^= 1
    return not any(parity)


def is_clean(h, first_coordinate, second_coordinate, component_data=None):
    labels, count = (
        components_without(h) if component_data is None else component_data
    )
    parity = [[0] * 4 for _ in range(count)]
    for edge, (first, second) in enumerate(EDGES):
        if not ((h >> edge) & 1) or labels[first] == labels[second]:
            continue
        colour = (
            ((first_coordinate >> edge) & 1)
            | (2 * ((second_coordinate >> edge) & 1))
        )
        parity[labels[first]][colour] ^= 1
        parity[labels[second]][colour] ^= 1
    return not any(any(row) for row in parity)


def extension_statistics(h, cycles):
    outside = ALL ^ h
    component_data = components_without(h)
    extensions = 0
    clean = 0
    first_clean = None
    for first in cycles:
        for second in cycles:
            if outside & ~(first | second):
                continue
            extensions += 1
            if is_clean(h, first, second, component_data):
                clean += 1
                if first_clean is None:
                    first_clean = (first, second)
    return extensions, clean, first_clean


def target_deletion_statistics(cycles):
    outside = ALL ^ TARGET_H
    deletable = 0
    by_circuit = [0, 0]
    for first in cycles:
        for second in cycles:
            if outside & ~(first | second):
                continue
            flags = []
            for circuit in TARGET_CIRCUITS:
                colours = {
                    ((first >> edge) & 1)
                    | (2 * ((second >> edge) & 1))
                    for edge in circuit
                }
                flags.append(len(colours) < 4)
            if any(flags):
                deletable += 1
            for circuit_index, flag in enumerate(flags):
                by_circuit[circuit_index] += flag
    return deletable, tuple(by_circuit)


def graph6_bytes():
    # graph6 orders the strict lower triangle column by column:
    # (0,1),(0,2),(1,2),... .
    bits = []
    edge_set = {tuple(sorted(edge)) for edge in EDGES}
    for second in range(1, N):
        for first in range(second):
            bits.append(int((first, second) in edge_set))
    while len(bits) % 6:
        bits.append(0)
    payload = bytes(
        63 + sum(bits[index + bit] << (5 - bit) for bit in range(6))
        for index in range(0, len(bits), 6)
    )
    return bytes([N + 63]) + payload + b"\n"


def main():
    assert N == 18 and M == 27
    assert len(set(tuple(sorted(edge)) for edge in EDGES)) == M
    assert all(first != second for first, second in EDGES)
    assert all(len(neighbours) == 3 for neighbours in ADJACENCY)
    assert connected()
    assert all(connected(edge) for edge in range(M))
    assert len(TARGET_VALUES) == M
    assert all(value in range(4) for value in TARGET_VALUES)
    assert all(
        __import__("functools").reduce(
            int.__xor__,
            (TARGET_VALUES[edge] for _neighbour, edge in ADJACENCY[vertex]),
            0,
        )
        == 0
        for vertex in range(N)
    )
    assert all(TARGET_VALUES[edge] for edge in range(14, M))
    assert is_cycle(TARGET_H)

    labels, component_count = components_without(TARGET_H)
    target_partition = tuple(labels[index] for index in range(14))
    assert target_partition == tuple(map(int, "01234444413024"))
    assert component_count == 5

    basis = cycle_basis()
    cycles = all_cycles(basis)
    assert all(is_cycle(mask) for mask in cycles)
    assert TARGET_H in cycles

    zero_sets = {
        ALL ^ (first | second) for first in cycles for second in cycles
    }
    minimum_weight = min(
        h.bit_count()
        for h in cycles
        if any(zero & ~h == 0 for zero in zero_sets)
    )
    minimum_projections = tuple(
        sorted(
            h
            for h in cycles
            if h.bit_count() == minimum_weight
            and any(zero & ~h == 0 for zero in zero_sets)
        )
    )
    tait_colourable = 0 in zero_sets

    target_extensions, target_clean, first_target_clean = (
        extension_statistics(TARGET_H, cycles)
    )
    target_deletable, target_deletable_by_circuit = (
        target_deletion_statistics(cycles)
    )
    minimum_statistics = []
    for projection in minimum_projections:
        extensions, clean, first_clean = extension_statistics(
            projection, cycles
        )
        minimum_statistics.append(
            {
                "edges": [
                    edge
                    for edge in range(M)
                    if (projection >> edge) & 1
                ],
                "extensions": extensions,
                "clean_extensions": clean,
                "is_cleanable": first_clean is not None,
            }
        )
    assert all(
        row["extensions"] == row["clean_extensions"]
        for row in minimum_statistics
    )

    original_first = sum(
        ((value & 1) != 0) << edge
        for edge, value in enumerate(TARGET_VALUES)
    )
    original_second = sum(
        ((value & 2) != 0) << edge
        for edge, value in enumerate(TARGET_VALUES)
    )
    assert original_first in cycles and original_second in cycles
    assert (ALL ^ TARGET_H) & ~(original_first | original_second) == 0
    original_clean = is_clean(
        TARGET_H, original_first, original_second
    )

    report = {
        "vertices": N,
        "edges": M,
        "simple": True,
        "connected": True,
        "bridgeless": True,
        "cubic": True,
        "cycle_space_dimension": len(basis),
        "cycle_space_size": len(cycles),
        "unique_low_missing_edge_sets": len(zero_sets),
        "labelled_graph6": graph6_bytes().decode("ascii").strip(),
        "target_projection_size": TARGET_H.bit_count(),
        "target_components": component_count,
        "target_partition": "".join(map(str, target_partition)),
        "target_extensions": target_extensions,
        "target_clean_extensions": target_clean,
        "target_has_clean_extension": first_target_clean is not None,
        "target_extensions_with_a_deletable_circuit": target_deletable,
        "target_deletable_extensions_by_circuit": list(
            target_deletable_by_circuit
        ),
        "displayed_extension_is_clean": original_clean,
        "tait_colourable": tait_colourable,
        "minimum_extendable_projection_size": minimum_weight,
        "number_of_minimum_extendable_projections": len(minimum_projections),
        "minimum_projection_statistics": minimum_statistics,
    }
    encoded = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode(
        "ascii"
    )
    frozen = ROOT / "realization-analysis.json"
    if frozen.exists():
        assert frozen.read_bytes() == encoded
    else:
        frozen.write_bytes(encoded)
    (ROOT / "labelled-realization.g6").write_bytes(graph6_bytes())

    print("PASS: exact simple cubic realization analysis")
    for key, value in report.items():
        print(f"{key}={value}")
    print(f"report_sha256={hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
