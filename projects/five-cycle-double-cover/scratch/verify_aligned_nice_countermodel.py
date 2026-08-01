#!/usr/bin/env python3
"""Verify the smallest frozen countermodel to the local aligned-N closure.

This is not a rooted counterexample.  It shows that a 2-connected
subcubic nice decomposition, T3, Z-acyclicity, the aligned 2+1+1
packet, and even P4 at b3 do not close residual N.  Full P4 is absent.
"""

from __future__ import annotations

import itertools
import json

import networkx as nx


GRAPH6 = "O?AA@qoPaW??C@??o?_OA"
TERMINALS = {14, 15, 2, 6}
PARTS = {
    "X1": {(11, 14), (14, 0)},
    "X2": {(13, 15), (15, 4)},
    "A": {(11, 12), (13, 12), (3, 12)},
    "B": {
        (0, 5),
        (0, 8),
        (1, 6),
        (1, 9),
        (1, 10),
        (2, 7),
        (2, 8),
        (3, 7),
        (3, 8),
        (4, 7),
        (4, 10),
        (5, 9),
        (5, 10),
        (6, 9),
    },
}
PACKET = {
    "D12": [0, 14, 11, 12, 13, 15, 4, 10, 5, 0],
    "R3": [2, 7, 3, 8, 2],
    "R4": [6, 1, 9, 6],
}
TRIPLE_CIRCUITS = {
    "2,6,14": [11, 14, 0, 5, 9, 6, 1, 10, 4, 7, 2, 8, 3, 12, 11],
    "2,6,15": [13, 15, 4, 10, 1, 6, 9, 5, 0, 8, 2, 7, 3, 12, 13],
    "2,14,15": [11, 14, 0, 8, 2, 7, 4, 15, 13, 12, 11],
    "6,14,15": [11, 14, 0, 5, 9, 6, 1, 10, 4, 15, 13, 12, 11],
}
LOCAL_PATHS = {
    "P0": [0, 5, 10, 4],
    "P3": [0, 8, 2, 7, 4],
    "P4": [0, 5, 9, 6, 1, 10, 4],
    "Q31": [3, 8, 2, 7, 4, 10, 1, 6, 9, 5, 0],
    "Q32": [3, 7, 2, 8, 0, 5, 9, 6, 1, 10, 4],
}


def normalized_edge(edge):
    return tuple(sorted(edge))


def assert_path(graph: nx.Graph, vertices, closed=False):
    if closed:
        assert vertices[0] == vertices[-1]
        assert len(set(vertices[:-1])) == len(vertices) - 1
    else:
        assert len(set(vertices)) == len(vertices)
    for left, right in zip(vertices, vertices[1:]):
        assert graph.has_edge(left, right), (left, right)


def cycle_mask(graph: nx.Graph, vertices, edge_index):
    assert_path(graph, vertices, closed=True)
    mask = 0
    for left, right in zip(vertices, vertices[1:]):
        mask ^= 1 << edge_index[normalized_edge((left, right))]
    return mask


def cycle_space_certificate_count(graph: nx.Graph):
    edges = sorted(normalized_edge(edge) for edge in graph.edges())
    edge_index = {edge: index for index, edge in enumerate(edges)}
    basis = []
    for vertices in nx.cycle_basis(graph):
        vertices = vertices + vertices[:1]
        basis.append(cycle_mask(graph, vertices, edge_index))

    certificate_count = 0
    terminal_cover_count = 0
    for coefficients in range(1, 1 << len(basis)):
        mask = 0
        for index, vector in enumerate(basis):
            if coefficients & (1 << index):
                mask ^= vector
        support = nx.Graph()
        support.add_nodes_from(graph)
        support.add_edges_from(
            edge for index, edge in enumerate(edges) if mask & (1 << index)
        )
        active = {vertex for vertex in graph if support.degree(vertex)}
        if not TERMINALS <= active:
            continue
        terminal_cover_count += 1
        components = nx.connected_components(support.subgraph(active))
        if all(len(set(component) & TERMINALS) % 2 == 0 for component in components):
            certificate_count += 1
    return len(basis), terminal_cover_count, certificate_count


def path_through_all_after_deletion(graph: nx.Graph, deleted: int):
    reduced = graph.copy()
    reduced.remove_node(deleted)
    target_mask = sum(1 << terminal for terminal in TERMINALS)
    for start in reduced:
        stack = [(start, 1 << start, [start])]
        while stack:
            vertex, used, path = stack.pop()
            if used & target_mask == target_mask:
                return path
            for neighbour in reduced[vertex]:
                bit = 1 << neighbour
                if not used & bit:
                    stack.append((neighbour, used | bit, path + [neighbour]))
    return None


def b_part_has_path_through_both(graph: nx.Graph):
    b_part = graph.subgraph(range(11))
    return any(
        {2, 6} <= set(path)
        for path in nx.all_simple_paths(b_part, source=0, target=4)
    )


def b_part_has_pair_cycle_disjoint_from_p0(graph: nx.Graph):
    b_part = graph.subgraph(range(11)).copy()
    b_part.remove_nodes_from(set(LOCAL_PATHS["P0"]))
    if 2 not in b_part or 6 not in b_part:
        return False
    for cycle in nx.simple_cycles(nx.DiGraph(b_part)):
        if len(cycle) >= 3 and {2, 6} <= set(cycle):
            return True
    return False


def main():
    graph = nx.from_graph6_bytes(GRAPH6.encode("ascii"))
    expected_edges = {
        normalized_edge(edge)
        for part_edges in PARTS.values()
        for edge in part_edges
    }
    assert {normalized_edge(edge) for edge in graph.edges()} == expected_edges
    assert nx.node_connectivity(graph) == 2
    assert max(dict(graph.degree()).values()) == 3
    assert all(graph.degree(terminal) == 2 for terminal in TERMINALS)

    packet_sets = []
    for vertices in PACKET.values():
        assert_path(graph, vertices, closed=True)
        packet_sets.append(set(vertices[:-1]))
    assert all(
        not (left & right)
        for left, right in itertools.combinations(packet_sets, 2)
    )
    assert [vertices & TERMINALS for vertices in packet_sets] == [
        {14, 15},
        {2},
        {6},
    ]

    for label, vertices in TRIPLE_CIRCUITS.items():
        assert_path(graph, vertices, closed=True)
        expected = {int(value) for value in label.split(",")}
        assert set(vertices) & TERMINALS == expected
    for vertices in LOCAL_PATHS.values():
        assert_path(graph, vertices)

    rank, terminal_covers, certificates = cycle_space_certificate_count(graph)
    assert rank == 6
    assert certificates == 0
    assert not b_part_has_path_through_both(graph)
    assert not b_part_has_pair_cycle_disjoint_from_p0(graph)

    p4_witnesses = {
        vertex: path_through_all_after_deletion(graph, vertex)
        for vertex in sorted(set(graph) - TERMINALS)
    }
    failures = [
        vertex for vertex, witness in p4_witnesses.items() if witness is None
    ]
    assert failures == [0, 4, 12]
    assert p4_witnesses[3] is not None

    print(
        json.dumps(
            {
                "graph6": GRAPH6,
                "order": len(graph),
                "size": graph.number_of_edges(),
                "node_connectivity": nx.node_connectivity(graph),
                "terminals": sorted(TERMINALS),
                "cycle_space_rank": rank,
                "terminal_covering_binary_cycles": terminal_covers,
                "admissible_certificates": certificates,
                "p4_failures": failures,
                "p4_at_b3": p4_witnesses[3],
                "no_B_b1_b2_path_through_both": True,
                "no_B_pair_cycle_disjoint_from_P0": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
