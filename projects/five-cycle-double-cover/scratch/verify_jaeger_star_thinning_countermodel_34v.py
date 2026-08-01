#!/usr/bin/env python3
"""Independent semantic and proof-certificate check of the 34v obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

import networkx as nx


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "output" / "jaeger-star-thinning-countermodel-34v"
GRAPH6 = (
    "as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?"
    "o??????_C??CGO??B@????a????__??C@O??A?_"
)
EXPECTED = {
    "star-thin.cnf": "5154202a28948a2b013ffaa4fa1b7bae2e8bad7eddc74885a5ed10603c633f0c",
    "star-thin-any.cnf": "8c96bd3d02685c12dca1eee78047459c65a60b0defdf87b68c000274dee9e6c0",
    "star-good.cnf": "6690acbd7c9ad93d976fd80fa638977d0d1b310e5b9a7a82b1162bff89a30ecc",
    "star-good-witness.json": "15160e5b5bd0915335b0b123475122a36d2092f6e5c7067e6bb79cdcc56bd84b",
    "star-good-six.cnf": "c85c1607d533d198796f2a89c0226fa553114bc6edbfe611b1e45f1701610103",
    "star-good-six-witness.json": "e3160e5f6b2985823a3421e9f3b1a4582c9c8be4b9abfd1f0e2312d311eb8358",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def even_degrees(
    order: int,
    edges: tuple[tuple[int, int], ...],
    mask: int,
) -> bool:
    degrees = [0] * order
    for edge, (left, right) in enumerate(edges):
        if mask & (1 << edge):
            degrees[left] ^= 1
            degrees[right] ^= 1
    return not any(degrees)


def main() -> None:
    for name, expected in EXPECTED.items():
        assert digest(PACKAGE / name) == expected

    graph = nx.from_graph6_bytes(GRAPH6.encode("ascii"))
    edges = tuple(
        (left, right)
        for right in range(1, len(graph))
        for left in range(right)
        if graph.has_edge(left, right)
    )
    assert len(graph) == 34 and len(edges) == 51
    assert edges[:3] == ((0, 1), (0, 2), (0, 3))
    assert all(degree == 3 for _, degree in graph.degree())
    assert nx.is_connected(graph)
    assert nx.edge_connectivity(graph) == 3
    assert nx.node_connectivity(graph) == 3

    thin_cnf = PACKAGE / "star-thin-any.cnf"
    thin_lrat = PACKAGE / "star-thin-any.lrat"
    lrat_check = (
        ROOT / ".tools" / "cert-checkers" / "drat-trim" / "lrat-check"
    )
    cake_lpr = (
        ROOT / ".tools" / "cert-checkers" / "cake_lpr" / "cake_lpr"
    )
    checked = subprocess.run(
        [str(lrat_check), str(thin_cnf), str(thin_lrat)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "c VERIFIED" in checked.stdout
    checked_cake = subprocess.run(
        [str(cake_lpr), str(thin_cnf), str(thin_lrat)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "s VERIFIED UNSAT" in checked_cake.stdout

    witness = json.loads(
        (PACKAGE / "star-good-six-witness.json").read_text(
            encoding="utf-8"
        )
    )
    assert witness["graph6"] == GRAPH6
    assert tuple(map(tuple, witness["edges"])) == edges
    assert witness["star_vertex"] == 0
    assert witness["star_edges"] == [0, 1, 2]

    trees = list(map(int, witness["tree_masks"]))
    completions = list(map(int, witness["completion_masks"]))
    assert len(trees) == len(completions) == 3
    for tree_mask, completion in zip(trees, completions):
        selected = [
            edges[edge]
            for edge in range(len(edges))
            if tree_mask & (1 << edge)
        ]
        tree = nx.Graph()
        tree.add_nodes_from(graph)
        tree.add_edges_from(selected)
        assert nx.is_tree(tree)
        # This verifies the defining characterization of the fundamental
        # completion without copying the producer's path-xor algorithm.
        assert even_degrees(len(graph), edges, completion)
        cotree = ((1 << len(edges)) - 1) ^ tree_mask
        assert completion & cotree == cotree
    for edge in range(len(edges)):
        expected = 1 if edge < 3 else 2
        assert sum(bool(tree & (1 << edge)) for tree in trees) == expected

    flow = [
        sum(
            bool(completion & (1 << edge)) << coordinate
            for coordinate, completion in enumerate(completions)
        )
        for edge in range(len(edges))
    ]
    assert flow == witness["flow"]
    assert all(flow)
    counts = [flow.count(value) for value in range(1, 8)]
    assert counts == witness["flow_value_counts"]
    # The exhibited good representative is genuinely outside the failed
    # sufficient criterion.
    assert min(counts) > 1

    labels = tuple(map(tuple, witness["point_labels"]))
    assert len(labels) == len(edges)
    assert all(
        len(pair) == 2
        and pair[0] < pair[1]
        and pair[0] ^ pair[1] == flow[edge]
        for edge, pair in enumerate(labels)
    )
    used_points = {point for pair in labels for point in pair}
    assert len(used_points) == 6
    incidence = [[] for _ in graph]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    for vertex in graph:
        for point in range(8):
            assert (
                sum(point in labels[edge] for edge in incidence[vertex]) % 2
                == 0
            )

    colours = list(map(int, witness["point_five_colouring"]))
    assert len(colours) == 8
    assert all(0 <= colour < 5 for colour in colours)
    five_labels = tuple(map(tuple, witness["five_labels"]))
    assert five_labels == tuple(
        tuple(sorted((colours[first], colours[second])))
        for first, second in labels
    )
    assert all(first != second for first, second in five_labels)
    for vertex in graph:
        for colour in range(5):
            assert (
                sum(
                    colour in five_labels[edge]
                    for edge in incidence[vertex]
                )
                % 2
                == 0
            )

    print(
        "PASS: graph premises; star multiplicities; LRAT accepted by "
        "lrat-check and CakeML cake_lpr; independent good five-cover "
        "witness verified."
    )


if __name__ == "__main__":
    main()
