#!/usr/bin/env python3
"""Independent standard-library replay of the focused theta census.

This checker does not execute or import the primary C++ classifier.
For every independent root pair it:

1. tests whether H=G-V(R) has a perfect matching, using a shared exact
   bitmask recurrence;
2. if not, enumerates perfect matchings after exposing two H-vertices;
3. accepts the first near-perfect matching for which G-(R union P) has no
   bridge.

By the proved deficiency-two and two-core lemmas, the three outcomes are
exactly def0, def2-with-theta, and def2-all-dumbbell.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parent.parent
CORPUS_ROOT = (
    ROOT / "search" / "focused-theta-choice-through28-20260727" / "artifacts"
)
CORPORA = {
    order: CORPUS_ROOT / f"cyclic4-nontait-order{order}.g6"
    for order in range(10, 29, 2)
}
EXPECTED_HASHES = {
    10: "7aec0fba73c081d7eebc551fc46b2484e73e58b2d36718dee105dbb6226e76aa",
    12: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    14: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    16: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    18: "2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd",
    20: "a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1",
    22: "2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223",
    24: "37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456",
    26: "1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760",
    28: "b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f",
}
EXPECTED = {
    10: {
        "graphs": 1,
        "pairs": 75,
        "def0": 60,
        "def2_theta": 15,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 15,
    },
    12: {
        "graphs": 0,
        "pairs": 0,
        "def0": 0,
        "def2_theta": 0,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 0,
    },
    14: {
        "graphs": 0,
        "pairs": 0,
        "def0": 0,
        "def2_theta": 0,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 0,
    },
    16: {
        "graphs": 0,
        "pairs": 0,
        "def0": 0,
        "def2_theta": 0,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 0,
    },
    18: {
        "graphs": 2,
        "pairs": 594,
        "def0": 569,
        "def2_theta": 25,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 25,
    },
    20: {
        "graphs": 6,
        "pairs": 2250,
        "def0": 2183,
        "def2_theta": 67,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 67,
    },
    22: {
        "graphs": 31,
        "pairs": 14322,
        "def0": 14047,
        "def2_theta": 275,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 275,
    },
    24: {
        "graphs": 155,
        "pairs": 86490,
        "def0": 85156,
        "def2_theta": 1334,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 1334,
    },
    26: {
        "graphs": 1297,
        "pairs": 859911,
        "def0": 848725,
        "def2_theta": 11186,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 11186,
    },
    28: {
        "graphs": 12517,
        "pairs": 9725709,
        "def0": 9617033,
        "def2_theta": 108676,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 108676,
    },
}


def parse_graph6(
    text: str, expected_order: int
) -> tuple[tuple[tuple[int, int], ...], list[list[tuple[int, int]]]]:
    if not text or ord(text[0]) >= 126:
        raise AssertionError("expected short graph6")
    order = ord(text[0]) - 63
    if order != expected_order:
        raise AssertionError("graph order changed")
    bits: list[int] = []
    for character in text[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise AssertionError("bad graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    if len(edges) * 2 != 3 * order or len(set(edges)) != len(edges):
        raise AssertionError("corpus row is not simple cubic-size")
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        adjacency[u].append((v, edge))
        adjacency[v].append((u, edge))
    if any(len(row) != 3 for row in adjacency):
        raise AssertionError("corpus row is not cubic")
    return tuple(edges), adjacency


class GraphAudit:
    def __init__(
        self,
        order: int,
        edges: tuple[tuple[int, int], ...],
        adjacency: list[list[tuple[int, int]]],
    ) -> None:
        self.order = order
        self.edges = edges
        self.adjacency = adjacency
        self.full_vertices = (1 << order) - 1
        self.near_matchings_checked = 0

    @lru_cache(maxsize=None)
    def has_perfect_matching(self, vertices: int) -> bool:
        if not vertices:
            return True
        if vertices.bit_count() % 2:
            return False
        chosen = -1
        chosen_degree = 4
        remaining_vertices = vertices
        while remaining_vertices:
            bit = remaining_vertices & -remaining_vertices
            vertex = bit.bit_length() - 1
            remaining_vertices ^= bit
            degree = sum(
                (vertices >> neighbour) & 1
                for neighbour, _ in self.adjacency[vertex]
            )
            if degree < chosen_degree:
                chosen = vertex
                chosen_degree = degree
        if chosen_degree == 0:
            return False
        without_chosen = vertices ^ (1 << chosen)
        for neighbour, _ in self.adjacency[chosen]:
            if not ((without_chosen >> neighbour) & 1):
                continue
            if self.has_perfect_matching(
                without_chosen ^ (1 << neighbour)
            ):
                return True
        return False

    def complement_is_bridgeless(self, matching_edges: int) -> bool:
        discovery = [-1] * self.order
        low = [0] * self.order
        timer = 0
        bridge = False

        def visit(vertex: int, parent_edge: int) -> None:
            nonlocal timer, bridge
            discovery[vertex] = timer
            low[vertex] = timer
            timer += 1
            for neighbour, edge in self.adjacency[vertex]:
                if (matching_edges >> edge) & 1 or edge == parent_edge:
                    continue
                if discovery[neighbour] < 0:
                    visit(neighbour, edge)
                    low[vertex] = min(low[vertex], low[neighbour])
                    if low[neighbour] > discovery[vertex]:
                        bridge = True
                else:
                    low[vertex] = min(
                        low[vertex], discovery[neighbour]
                    )

        for vertex in range(self.order):
            if discovery[vertex] < 0:
                visit(vertex, -1)
        return not bridge

    def find_theta_completion(
        self, vertices: int, matching_edges: int
    ) -> bool:
        if not vertices:
            self.near_matchings_checked += 1
            return self.complement_is_bridgeless(matching_edges)
        chosen = -1
        chosen_degree = 4
        remaining_vertices = vertices
        while remaining_vertices:
            bit = remaining_vertices & -remaining_vertices
            vertex = bit.bit_length() - 1
            remaining_vertices ^= bit
            degree = sum(
                (vertices >> neighbour) & 1
                for neighbour, _ in self.adjacency[vertex]
            )
            if degree < chosen_degree:
                chosen = vertex
                chosen_degree = degree
        if chosen_degree == 0:
            return False
        without_chosen = vertices ^ (1 << chosen)
        for neighbour, edge in self.adjacency[chosen]:
            if not ((without_chosen >> neighbour) & 1):
                continue
            reduced = without_chosen ^ (1 << neighbour)
            if not self.has_perfect_matching(reduced):
                continue
            if self.find_theta_completion(
                reduced, matching_edges | (1 << edge)
            ):
                return True
        return False

    def root_has_theta(
        self, h_vertices: int, root_edge_mask: int
    ) -> bool:
        exposed_candidates = [
            vertex
            for vertex in range(self.order)
            if (h_vertices >> vertex) & 1
        ]
        for first_index, first in enumerate(exposed_candidates):
            for second in exposed_candidates[first_index + 1 :]:
                remaining = (
                    h_vertices ^ (1 << first) ^ (1 << second)
                )
                if not self.has_perfect_matching(remaining):
                    continue
                if self.find_theta_completion(
                    remaining, root_edge_mask
                ):
                    return True
        return False

    def classify(self) -> dict[str, int]:
        counts = {
            "pairs": 0,
            "def0": 0,
            "def2_theta": 0,
            "def2_all_dumbbell": 0,
            "def2_boundary6": 0,
            "def2_boundary8": 0,
        }
        for first, (a, b) in enumerate(self.edges):
            for second in range(first + 1, len(self.edges)):
                c, d = self.edges[second]
                if len({a, b, c, d}) != 4:
                    continue
                counts["pairs"] += 1
                roots = (1 << a) | (1 << b) | (1 << c) | (1 << d)
                h_vertices = self.full_vertices ^ roots
                if self.has_perfect_matching(h_vertices):
                    counts["def0"] += 1
                    continue

                internal_u_edges = sum(
                    ((roots >> u) & 1) and ((roots >> v) & 1)
                    for u, v in self.edges
                )
                boundary = 12 - 2 * internal_u_edges
                if boundary == 6:
                    counts["def2_boundary6"] += 1
                elif boundary == 8:
                    counts["def2_boundary8"] += 1
                else:
                    raise AssertionError(
                        "deficiency-two U-boundary is not 6 or 8"
                    )

                if self.root_has_theta(
                    h_vertices, (1 << first) | (1 << second)
                ):
                    counts["def2_theta"] += 1
                else:
                    counts["def2_all_dumbbell"] += 1
        counts["near_matchings_checked"] = self.near_matchings_checked
        return counts


def audit_order(
    order: int,
    limit: int,
    corpus_override: Path | None = None,
    expected_hash_override: str = "",
    shard_index: int = 0,
    shard_count: int = 1,
) -> dict[str, object]:
    corpus = corpus_override if corpus_override is not None else CORPORA[order]
    corpus_bytes = corpus.read_bytes()
    digest = hashlib.sha256(corpus_bytes).hexdigest()
    expected_digest = (
        expected_hash_override
        if expected_hash_override
        else EXPECTED_HASHES.get(order, "")
    )
    if expected_digest and digest != expected_digest:
        raise AssertionError(f"order-{order} corpus hash changed")
    source_rows = corpus_bytes.decode("ascii").splitlines()
    rows = [
        row
        for index, row in enumerate(source_rows)
        if index % shard_count == shard_index
    ]
    if limit:
        rows = rows[:limit]
    totals = {
        "pairs": 0,
        "def0": 0,
        "def2_theta": 0,
        "def2_all_dumbbell": 0,
        "def2_boundary6": 0,
        "def2_boundary8": 0,
        "near_matchings_checked": 0,
    }
    for index, graph6 in enumerate(rows):
        edges, adjacency = parse_graph6(graph6, order)
        audit = GraphAudit(order, edges, adjacency)
        row = audit.classify()
        for key in totals:
            totals[key] += row[key]
        if (index + 1) % 100 == 0 or index + 1 == len(rows):
            print(
                f"PROGRESS order={order} graphs={index + 1} "
                f"pairs={totals['pairs']} def0={totals['def0']} "
                f"def2_theta={totals['def2_theta']} "
                f"all_dumbbell={totals['def2_all_dumbbell']}",
                file=sys.stderr,
                flush=True,
            )
    result: dict[str, object] = {
        "order": order,
        "graphs": len(rows),
        "source_graphs": len(source_rows),
        "corpus_sha256": digest,
        "shard_index": shard_index,
        "shard_count": shard_count,
        **totals,
    }
    if (
        not limit
        and corpus_override is None
        and shard_count == 1
        and order in EXPECTED
    ):
        for key, value in EXPECTED[order].items():
            if result[key] != value:
                raise AssertionError(
                    f"order-{order} {key}: {result[key]} != {value}"
                )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="audit only the first LIMIT graphs at each requested order",
    )
    parser.add_argument(
        "--orders",
        default="10,12,14,16,18,20,22,24,26,28",
        help="comma-separated even orders from 10 through 28",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        help="audit one explicit graph6 corpus instead of the retained defaults",
    )
    parser.add_argument(
        "--expected-sha256",
        default="",
        help="require this SHA-256 for --corpus",
    )
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    args = parser.parse_args()
    orders = [int(item) for item in args.orders.split(",")]
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise AssertionError("invalid shard index/count")
    if args.corpus is not None and len(orders) != 1:
        raise AssertionError("--corpus requires exactly one --orders value")
    if args.corpus is None and any(order not in CORPORA for order in orders):
        raise AssertionError("orders must be even and between 10 and 28")

    started = time.time()
    results = [
        audit_order(
            order,
            args.limit,
            args.corpus,
            args.expected_sha256,
            args.shard_index,
            args.shard_count,
        )
        for order in orders
    ]
    output = {
        "classification": "PASS",
        "warning": (
            "This is a finite exact result for the requested corpus "
            "scope, not a universal theta-choice theorem."
            if args.corpus is not None
            else
            "These are finite exact results for the ten retained "
            "corpora, not a universal theta-choice theorem."
        ),
        "results": results,
        "elapsed_seconds": round(time.time() - started, 3),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
