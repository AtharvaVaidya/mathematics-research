#!/usr/bin/env python3
"""Exact finite screen for the aligned marked-borrower nice skeleton.

The A-part is the minimum subcubic three-port star.  X1 and X2 are
singleton terminal rows.  B ranges over connected simple subcubic
graphs generated canonically by geng.  We label three B ports b1,b2,b3
and two degree-two terminals z3,z4, require an aligned 2+1+1 packet,
then check:

* the assembled graph is 2-connected and subcubic;
* every terminal triple lies on a circuit (T3);
* no terminal-covering binary cycle has even terminal count in every
  component (in particular, no all-four circuit);
* P4 holds after deletion of every nonterminal.

A printed survivor is only a countermodel to this fixed-A skeleton,
not automatically a rooted counterexample: the cap/Tait and marked-cut
hypotheses are not encoded here.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json

import networkx as nx

from search_aligned_nice_b_part import (
    cycle_vertex_sets_through,
    graph6_rows,
    path_vertex_sets,
)


def normalized_edge(edge):
    return tuple(sorted(edge))


def packet_witness(graph: nx.Graph, b1: int, b2: int, z3: int, z4: int):
    bit3 = 1 << z3
    bit4 = 1 << z4
    paths0 = [
        path
        for path in path_vertex_sets(graph, b1, b2)
        if not path & bit3 and not path & bit4
    ]
    if not paths0:
        return None
    cycles3 = cycle_vertex_sets_through(graph, z3)
    cycles4 = cycle_vertex_sets_through(graph, z4)
    for cycle3 in cycles3:
        for cycle4 in cycles4:
            if cycle3 & cycle4:
                continue
            for path0 in paths0:
                if not path0 & cycle3 and not path0 & cycle4:
                    return path0, cycle3, cycle4
    return None


def assemble(b_part: nx.Graph, b1: int, b2: int, b3: int):
    order = len(b_part)
    a1, center, a2, z1, z2 = range(order, order + 5)
    graph = nx.Graph()
    graph.add_nodes_from(range(order + 5))
    graph.add_edges_from(b_part.edges())
    graph.add_edges_from(
        [
            (a1, center),
            (center, a2),
            (center, b3),
            (a1, z1),
            (z1, b1),
            (a2, z2),
            (z2, b2),
        ]
    )
    return graph, (z1, z2), (a1, center, a2)


def binary_cycle_data(graph: nx.Graph, terminals):
    terminals = set(terminals)
    edges = sorted(normalized_edge(edge) for edge in graph.edges())
    edge_index = {edge: index for index, edge in enumerate(edges)}
    basis = []
    for cycle in nx.cycle_basis(graph):
        mask = 0
        for left, right in zip(cycle, cycle[1:] + cycle[:1]):
            mask ^= 1 << edge_index[normalized_edge((left, right))]
        basis.append(mask)

    triple_circuits = {triple: None for triple in itertools.combinations(terminals, 3)}
    certificate = None
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
        components = [
            set(component)
            for component in nx.connected_components(support.subgraph(active))
        ]
        if terminals <= active and all(
            len(component & terminals) % 2 == 0 for component in components
        ):
            certificate = mask
            break
        if len(components) == 1:
            component = components[0]
            for triple in triple_circuits:
                if triple_circuits[triple] is None and set(triple) <= component:
                    triple_circuits[triple] = mask
    return len(basis), triple_circuits, certificate


def path_through_all_after_deletion(graph: nx.Graph, terminals, deleted: int):
    target_mask = sum(1 << terminal for terminal in terminals)
    remaining = set(graph) - {deleted}
    for start in remaining:
        stack = [(start, 1 << start)]
        reached = {(start, 1 << start)}
        while stack:
            vertex, used = stack.pop()
            if used & target_mask == target_mask:
                return True
            for neighbour in graph[vertex]:
                bit = 1 << neighbour
                state = (neighbour, used | bit)
                if neighbour != deleted and not used & bit and state not in reached:
                    reached.add(state)
                    stack.append(state)
    return False


def full_p4_failures(graph: nx.Graph, terminals):
    return tuple(
        vertex
        for vertex in graph
        if vertex not in terminals
        and not path_through_all_after_deletion(graph, terminals, vertex)
    )


def mask_vertices(mask: int, order: int):
    return [vertex for vertex in range(order) if mask & (1 << vertex)]


def search_order(order: int, shard_count: int, shard_index: int):
    counts = collections.Counter()
    failure_profiles = collections.Counter()
    for graph_index, record in enumerate(graph6_rows(order)):
        if graph_index % shard_count != shard_index:
            continue
        counts["B_graphs"] += 1
        b_part = nx.from_graph6_bytes(record.encode("ascii"))
        possible_ports = [vertex for vertex in b_part if b_part.degree(vertex) <= 2]
        terminal_candidates = [
            vertex for vertex in b_part if b_part.degree(vertex) == 2
        ]
        for z3, z4 in itertools.combinations(terminal_candidates, 2):
            ports = [
                vertex
                for vertex in possible_ports
                if vertex not in {z3, z4}
            ]
            for b1, b2 in itertools.combinations(ports, 2):
                packet = packet_witness(b_part, b1, b2, z3, z4)
                if packet is None:
                    continue
                for b3 in ports:
                    if b3 in {b1, b2}:
                        continue
                    # Any degree-one vertex left in the B interior would
                    # remain degree one in the assembled graph.
                    if any(
                        b_part.degree(vertex) == 1
                        for vertex in b_part
                        if vertex not in {b1, b2,b3}
                    ):
                        continue
                    counts["labelings"] += 1
                    counts["packet"] += 1
                    graph, (z1, z2), a_ports = assemble(b_part, b1, b2, b3)
                    terminals = (z1, z2, z3, z4)
                    if max(dict(graph.degree()).values()) > 3:
                        continue
                    if nx.node_connectivity(graph) < 2:
                        continue
                    counts["two_connected"] += 1
                    rank, triples, certificate = binary_cycle_data(
                        graph, terminals
                    )
                    if any(mask is None for mask in triples.values()):
                        continue
                    counts["T3"] += 1
                    if certificate is not None:
                        continue
                    counts["T3_no_certificate"] += 1
                    failures = full_p4_failures(graph, terminals)
                    failure_profiles[failures] += 1
                    if failures:
                        continue
                    counts["full_P4"] += 1
                    path0, cycle3, cycle4 = packet
                    return {
                        "order_B": order,
                        "graph6_B": record,
                        "graph6_full": nx.to_graph6_bytes(
                            graph, header=False
                        ).decode("ascii").strip(),
                        "ports": {"b1": b1, "b2": b2, "b3": b3},
                        "terminals_B": [z3, z4],
                        "terminals_full": list(terminals),
                        "A_ports": list(a_ports),
                        "cycle_space_rank": rank,
                        "packet": {
                            "P0": mask_vertices(path0, order),
                            "R3": mask_vertices(cycle3, order),
                            "R4": mask_vertices(cycle4, order),
                        },
                    }, counts, failure_profiles
    return None, counts, failure_profiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-B-order", type=int, default=6)
    parser.add_argument("--maximum-B-order", type=int, default=12)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    arguments = parser.parse_args()
    if arguments.shard_count < 1:
        parser.error("--shard-count must be positive")
    if not 0 <= arguments.shard_index < arguments.shard_count:
        parser.error("--shard-index must lie in [0, shard-count)")

    total_counts = collections.Counter()
    total_profiles = collections.Counter()
    for order in range(
        arguments.minimum_B_order, arguments.maximum_B_order + 1
    ):
        survivor, counts, profiles = search_order(
            order, arguments.shard_count, arguments.shard_index
        )
        total_counts.update(counts)
        total_profiles.update(profiles)
        print(
            json.dumps(
                {
                    "order_B": order,
                    "shard": [
                        arguments.shard_index,
                        arguments.shard_count,
                    ],
                    "counts": dict(counts),
                    "P4_failure_profiles": {
                        ",".join(map(str, key)): value
                        for key, value in profiles.items()
                    },
                },
                sort_keys=True,
            )
        )
        if survivor is not None:
            print(json.dumps({"survivor": survivor}, sort_keys=True))
            return
    print(
        json.dumps(
            {
                "survivor": None,
                "shard": [
                    arguments.shard_index,
                    arguments.shard_count,
                ],
                "total_counts": dict(total_counts),
                "total_P4_failure_profiles": {
                    ",".join(map(str, key)): value
                    for key, value in total_profiles.items()
                },
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
