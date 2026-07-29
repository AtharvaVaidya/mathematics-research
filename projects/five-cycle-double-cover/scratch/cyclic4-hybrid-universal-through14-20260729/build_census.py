#!/usr/bin/env python3
"""Build the canonical cyclically-4 cubic macro census through order 14."""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORDERS = (6, 8, 10, 12, 14)


def decode_graph6(record):
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


def incidence(vertices, edges):
    rows = [[] for _ in range(vertices)]
    masks = [0] * vertices
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
        masks[left] |= 1 << right
        masks[right] |= 1 << left
    return tuple(tuple(row) for row in rows), tuple(masks)


def connected(vertices, masks):
    seen = 1
    queue = [0]
    for vertex in queue:
        unseen = masks[vertex] & ~seen
        while unseen:
            bit = unseen & -unseen
            unseen ^= bit
            seen |= bit
            queue.append(bit.bit_length() - 1)
    return seen == (1 << vertices) - 1


def cyclically_four(vertices, edges, masks):
    """No cut of size at most three has a cycle on both shores."""

    count = 1 << (vertices - 1)
    internal = [0] * count
    total_edges = len(edges)
    for reduced in range(count):
        if reduced:
            bit = reduced & -reduced
            previous = reduced ^ bit
            vertex = bit.bit_length()
            shore_previous = (previous << 1) | 1
            internal[reduced] = (
                internal[previous]
                + (masks[vertex] & shore_previous).bit_count()
            )
        shore = (reduced << 1) | 1
        shore_vertices = shore.bit_count()
        if shore_vertices == vertices:
            continue
        shore_edges = internal[reduced]
        cut = 3 * shore_vertices - 2 * shore_edges
        if cut > 3:
            continue
        other_vertices = vertices - shore_vertices
        other_edges = total_edges - shore_edges - cut
        if shore_edges >= shore_vertices and other_edges >= other_vertices:
            return False
    return True


def graph_girth(vertices, masks):
    best = vertices + 1
    for source in range(vertices):
        distance = [-1] * vertices
        parent = [-1] * vertices
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            neighbours = masks[vertex]
            while neighbours:
                bit = neighbours & -neighbours
                neighbours ^= bit
                other = bit.bit_length() - 1
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    best = min(
                        best,
                        distance[vertex] + distance[other] + 1,
                    )
    return best


def automorphisms(vertices, edges):
    neighbours = [set() for _ in range(vertices)]
    for left, right in edges:
        neighbours[left].add(right)
        neighbours[right].add(left)
    mapping = {}
    used = set()
    result = []

    def choose():
        return max(
            (v for v in range(vertices) if v not in mapping),
            key=lambda v: sum(w in mapping for w in neighbours[v]),
        )

    def visit():
        if len(mapping) == vertices:
            result.append(tuple(mapping[v] for v in range(vertices)))
            return
        vertex = choose()
        for image in range(vertices):
            if image in used:
                continue
            if all(
                (other in neighbours[vertex])
                == (mapping[other] in neighbours[image])
                for other in mapping
            ):
                mapping[vertex] = image
                used.add(image)
                visit()
                used.remove(image)
                del mapping[vertex]

    visit()
    return tuple(result)


def junction_orbits(vertices, edges, actions):
    edge_set = set(edges)
    representatives = {}
    raw = 0
    for size in range(2, vertices + 1, 2):
        for junctions in combinations(range(vertices), size):
            if any(
                tuple(sorted(pair)) in edge_set
                for pair in combinations(junctions, 2)
            ):
                continue
            raw += 1
            key = min(
                tuple(sorted(action[v] for v in junctions))
                for action in actions
            )
            representatives.setdefault(key, junctions)
    return representatives, raw


def main() -> int:
    by_order = {}
    total_graphs = 0
    total_cyclic4 = 0
    total_raw = 0
    total_orbits = 0
    total_girth5_graphs = 0
    total_girth5_orbits = 0
    for order in ORDERS:
        records = [
            line
            for line in (HERE / f"order{order}-connected-cubic.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line
        ]
        graphs = []
        raw_order = 0
        orbits_order = 0
        girth5_graphs = 0
        girth5_orbits = 0
        for graph_index, graph6 in enumerate(records):
            vertices, edges = decode_graph6(graph6)
            rows, masks = incidence(vertices, edges)
            if (
                vertices != order
                or len(edges) != 3 * order // 2
                or any(len(row) != 3 for row in rows)
                or not connected(vertices, masks)
            ):
                raise AssertionError("bad connected cubic graph6 input")
            if not cyclically_four(vertices, edges, masks):
                continue
            actions = automorphisms(vertices, edges)
            representatives, raw = junction_orbits(
                vertices, edges, actions
            )
            girth = graph_girth(vertices, masks)
            graph = {
                "graph_index": graph_index,
                "graph6": graph6,
                "girth": girth,
                "automorphisms": len(actions),
                "raw_independent_positive_even_junction_sets": raw,
                "canonical_junction_orbits": len(representatives),
                "junction_representatives": [
                    list(row) for row in representatives.values()
                ],
            }
            graphs.append(graph)
            raw_order += raw
            orbits_order += len(representatives)
            if girth >= 5:
                girth5_graphs += 1
                girth5_orbits += len(representatives)
        by_order[str(order)] = {
            "connected_cubic_graphs": len(records),
            "cyclically_4_edge_connected_graphs": len(graphs),
            "girth_at_least_5_graphs": girth5_graphs,
            "raw_independent_positive_even_junction_sets": raw_order,
            "canonical_junction_orbits": orbits_order,
            "girth_at_least_5_junction_orbits": girth5_orbits,
            "graphs": graphs,
        }
        total_graphs += len(records)
        total_cyclic4 += len(graphs)
        total_raw += raw_order
        total_orbits += orbits_order
        total_girth5_graphs += girth5_graphs
        total_girth5_orbits += girth5_orbits
    report = {
        "schema": "cyclic4-cubic-hybrid-macro-census-through14-v1",
        "generator": "nauty geng -cq -d3 -D3 n",
        "cyclically_4_definition": (
            "no edge cut of size at most 3 has a cycle on both shores"
        ),
        "junction_scope": (
            "independent positive-even sets, quotiented by full graph "
            "automorphism group"
        ),
        "orders": by_order,
        "totals": {
            "connected_cubic_graphs": total_graphs,
            "cyclically_4_edge_connected_graphs": total_cyclic4,
            "girth_at_least_5_graphs": total_girth5_graphs,
            "raw_independent_positive_even_junction_sets": total_raw,
            "canonical_junction_orbits": total_orbits,
            "girth_at_least_5_junction_orbits": total_girth5_orbits,
        },
    }
    (HERE / "census-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(report["totals"], sort_keys=True))
    for order in ORDERS:
        row = by_order[str(order)]
        print(
            f"n={order} connected={row['connected_cubic_graphs']} "
            f"cyclic4={row['cyclically_4_edge_connected_graphs']} "
            f"girth5={row['girth_at_least_5_graphs']} "
            f"junction_orbits={row['canonical_junction_orbits']} "
            f"girth5_orbits={row['girth_at_least_5_junction_orbits']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
