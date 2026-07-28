#!/usr/bin/env python3
"""Literal checker for the six lifts in the triangle-expansion note."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT / "scratch" / "verify_jaeger_star_parity_descent_countermodel.py"
)
SPEC = importlib.util.spec_from_file_location("fixed", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
FIXED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXED)

EXPANDED_VERTEX = 1
EXPECTED = {
    (0, 1, 2): (2, 4, 2, 2, 2, 8, 2),
    (0, 2, 1): (2, 4, 2, 2, 0, 8, 2),
    (1, 0, 2): (4, 4, 2, 2, 2, 6, 4),
    (1, 2, 0): (2, 4, 2, 2, 0, 8, 2),
    (2, 0, 1): (2, 4, 2, 2, 0, 8, 2),
    (2, 1, 0): (2, 4, 2, 2, 0, 6, 4),
}


def main() -> None:
    order, old_edges = FIXED.parse_graph6(FIXED.GRAPH6)
    spokes = tuple(
        edge
        for edge, endpoints in enumerate(old_edges)
        if FIXED.ROOT in endpoints
    )
    internal = tuple(
        edge for edge in range(len(old_edges)) if edge not in spokes
    )
    all_internal = (1 << len(internal)) - 1
    omitted = (
        FIXED.OMITTED_MASKS[0],
        FIXED.OMITTED_MASKS[1],
        all_internal
        ^ FIXED.OMITTED_MASKS[0]
        ^ FIXED.OMITTED_MASKS[1],
    )
    old_trees = tuple(
        frozenset(
            [spokes[coordinate]]
            + [
                edge
                for local, edge in enumerate(internal)
                if not ((omitted[coordinate] >> local) & 1)
            ]
        )
        for coordinate in range(3)
    )
    old_kernels = tuple(
        FIXED.odd_core(order, old_edges, tree) for tree in old_trees
    )
    assert FIXED.fano_profile(order, old_edges, old_kernels) == (
        2, 4, 2, 2, 0, 6, 2
    )

    neighbours = [
        right if left == EXPANDED_VERTEX else left
        for left, right in old_edges
        if EXPANDED_VERTEX in (left, right)
    ]
    triangle_old_labels = (14, 15, 16)
    expanded_edges = [
        edge
        for edge in old_edges
        if EXPANDED_VERTEX not in edge
    ]
    expanded_edges.extend(((14, 15), (15, 16), (16, 14)))
    expanded_edges.extend(zip(triangle_old_labels, neighbours))
    old_labels = sorted(
        {vertex for edge in expanded_edges for vertex in edge}
    )
    relabel = {old: new for new, old in enumerate(old_labels)}
    edges = tuple(
        sorted(
            (min(relabel[left], relabel[right]),
             max(relabel[left], relabel[right]))
            for left, right in expanded_edges
        )
    )
    edge_id = {
        frozenset(endpoints): edge
        for edge, endpoints in enumerate(edges)
    }
    triangle = tuple(
        edge_id[
            frozenset(
                (
                    relabel[triangle_old_labels[index]],
                    relabel[triangle_old_labels[(index + 1) % 3]],
                )
            )
        ]
        for index in range(3)
    )
    results = {}
    for permutation in itertools.permutations(range(3)):
        trees = []
        for coordinate in range(3):
            tree = set()
            for edge in old_trees[coordinate]:
                left, right = old_edges[edge]
                if EXPANDED_VERTEX not in (left, right):
                    lifted = (relabel[left], relabel[right])
                else:
                    other = right if left == EXPANDED_VERTEX else left
                    port = triangle_old_labels[neighbours.index(other)]
                    lifted = (relabel[port], relabel[other])
                tree.add(edge_id[frozenset(lifted)])
            tree.update(
                edge
                for index, edge in enumerate(triangle)
                if index != permutation[coordinate]
            )
            tree = frozenset(tree)
            assert FIXED.is_tree(16, edges, tree)
            trees.append(tree)
        root = relabel[FIXED.ROOT]
        root_star = {
            edge
            for edge, endpoints in enumerate(edges)
            if root in endpoints
        }
        for edge in range(len(edges)):
            assert sum(edge in tree for tree in trees) == (
                1 if edge in root_star else 2
            )
        kernels = tuple(
            FIXED.odd_core(16, edges, tree) for tree in trees
        )
        profile = FIXED.fano_profile(16, edges, kernels)
        assert profile == EXPECTED[permutation]
        # Contracting the triangle recovers the same external tree
        # memberships, which is the literal content needed here.
        for coordinate in range(3):
            for old_edge, (left, right) in enumerate(old_edges):
                if EXPANDED_VERTEX in (left, right):
                    continue
                lifted = edge_id[
                    frozenset((relabel[left], relabel[right]))
                ]
                assert (
                    (lifted in trees[coordinate])
                    == (old_edge in old_trees[coordinate])
                )
        results["".join(map(str, permutation))] = {
            "profile": list(profile),
            "d_min": min(profile),
        }
    assert sum(value["d_min"] == 0 for value in results.values()) == 4
    assert sum(value["d_min"] == 2 for value in results.values()) == 2
    print(
        json.dumps(
            {
                "base_graph6": FIXED.GRAPH6,
                "expanded_vertex": EXPANDED_VERTEX,
                "contracted_profile": [2, 4, 2, 2, 0, 6, 2],
                "six_lifts": results,
                "verified": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
