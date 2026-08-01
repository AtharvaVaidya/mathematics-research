#!/usr/bin/env python3
"""Exact small-order search for a Fano flow with seven bad projections.

For a connected cubic graph G, a nowhere-zero F_2^3-flow is equivalently
a 3-dimensional subspace S of the binary cycle space whose supports cover
E(G).  Its seven nonzero functional projections are the seven nonzero
members of S.

For a binary cycle h, exact line cleanability depends only on h.  With
F=E\\h it asks for binary cycles p,q such that

  F subset support(p) union support(q), and
  |delta(W) intersect support(p) intersect support(q)| is even

for every component W of F.  This script checks that definition directly,
classifies all h, and then searches the bad cycles for a covering
3-dimensional subspace.

The default run canonically generates every connected cubic graph through
order 12 with nauty-geng and filters to bridgeless graphs.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


def decode_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    value = text.strip()
    if value.startswith(">>graph6<<"):
        value = value[len(">>graph6<<") :]
    if not value or ord(value[0]) >= 126:
        raise ValueError("only graph6 orders below 63 are supported")
    order = ord(value[0]) - 63
    bits = []
    for character in value[1:]:
        number = ord(character) - 63
        bits.extend((number >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [
        (first, second)
        for second in range(1, order)
        for first in range(second)
    ]
    if len(bits) < len(pairs):
        raise ValueError("truncated graph6 row")
    edges = tuple(pair for pair, bit in zip(pairs, bits) if bit)
    return order, edges


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        rows[first].append(edge)
        rows[second].append(edge)
    return tuple(tuple(row) for row in rows)


def connected_without_edge(
    order: int,
    edges: tuple[tuple[int, int], ...],
    omitted: int,
) -> bool:
    adjacency = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if edge == omitted:
            continue
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == order


def cycle_basis(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    adjacency = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        adjacency[first].append((second, edge))
        adjacency[second].append((first, edge))

    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    queue = deque([0])
    tree_edges = set()
    while queue:
        vertex = queue.popleft()
        for neighbor, edge in adjacency[vertex]:
            if parent[neighbor] < 0:
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge
                tree_edges.add(edge)
                queue.append(neighbor)
    assert all(value >= 0 for value in parent)

    def tree_path(first: int, second: int) -> int:
        first_path: dict[int, int] = {}
        mask = 0
        vertex = first
        while True:
            first_path[vertex] = mask
            if vertex == 0:
                break
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        mask = 0
        vertex = second
        while vertex not in first_path:
            mask ^= 1 << parent_edge[vertex]
            vertex = parent[vertex]
        return mask ^ first_path[vertex]

    basis = []
    for edge, (first, second) in enumerate(edges):
        if edge not in tree_edges:
            basis.append((1 << edge) ^ tree_path(first, second))
    assert len(basis) == len(edges) - order + 1
    return tuple(basis)


def is_tait_colorable(
    order: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    rows = incidence(order, edges)
    colors = [-1] * len(edges)
    used = [0] * order

    # Fix the global S_3 symmetry at vertex zero.
    for color, edge in enumerate(rows[0]):
        first, second = edges[edge]
        colors[edge] = color
        used[first] |= 1 << color
        used[second] |= 1 << color

    def recurse(colored: int) -> bool:
        if colored == len(edges):
            return True
        best_edge = -1
        best_allowed = 0
        for edge, color in enumerate(colors):
            if color >= 0:
                continue
            first, second = edges[edge]
            allowed = 0b111 & ~used[first] & ~used[second]
            if allowed == 0:
                return False
            if best_edge < 0 or allowed.bit_count() < best_allowed.bit_count():
                best_edge = edge
                best_allowed = allowed
                if allowed.bit_count() == 1:
                    break
        first, second = edges[best_edge]
        choices = best_allowed
        while choices:
            bit = choices & -choices
            choices ^= bit
            colors[best_edge] = bit.bit_length() - 1
            used[first] |= bit
            used[second] |= bit
            if recurse(colored + 1):
                return True
            used[first] ^= bit
            used[second] ^= bit
            colors[best_edge] = -1
        return False

    return recurse(3)


def enumerate_cycles(basis: tuple[int, ...]) -> tuple[int, ...]:
    cycles = [0]
    for vector in basis:
        cycles += [cycle ^ vector for cycle in cycles]
    return tuple(sorted(cycles))


def factor_cut_masks(
    order: int,
    edges: tuple[tuple[int, int], ...],
    factor: int,
) -> tuple[int, ...]:
    adjacency = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(edges):
        if (factor >> edge) & 1:
            adjacency[first].append(second)
            adjacency[second].append(first)
    unseen = set(range(order))
    components = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)

    cuts = []
    for component in components:
        cut = 0
        for edge, (first, second) in enumerate(edges):
            if (first in component) != (second in component):
                cut |= 1 << edge
        cuts.append(cut)
    return tuple(cuts)


def classify_projections(
    order: int,
    edges: tuple[tuple[int, int], ...],
    cycles: tuple[int, ...],
) -> tuple[set[int], set[int], dict[int, tuple[int, int]]]:
    all_edges = (1 << len(edges)) - 1
    if is_tait_colorable(order, edges):
        # Fixed 4-flow lemma: one nowhere-zero pair p,q cleans every
        # binary projection, not merely the zero projection.
        return set(cycles), set(cycles), {}

    # p,q are symmetric.  Equal union/intersection pairs have identical
    # semantics, so retain one and try the largest unions first.
    pair_states = {
        (first | second, first & second)
        for position, first in enumerate(cycles)
        for second in cycles[position:]
    }
    ordered_pairs = sorted(
        pair_states,
        key=lambda row: (row[0].bit_count(), -row[1].bit_count()),
        reverse=True,
    )

    clean = set()
    liftable = set()
    witnesses: dict[int, tuple[int, int]] = {}
    # Recover one actual p,q pair for each semantic pair only when needed.
    semantic_witness = {}
    for position, first in enumerate(cycles):
        for second in cycles[position:]:
            semantic_witness.setdefault(
                (first | second, first & second), (first, second)
            )

    for projection in cycles:
        if projection == 0:
            # We already excluded the Tait case.  A lift of the zero
            # projection is exactly a nowhere-zero F_2^2-flow.
            continue
        factor = all_edges ^ projection
        cuts = factor_cut_masks(order, edges, factor)
        for union, product in ordered_pairs:
            if factor & ~union:
                continue
            liftable.add(projection)
            if any((product & cut).bit_count() & 1 for cut in cuts):
                continue
            clean.add(projection)
            witnesses[projection] = semantic_witness[(union, product)]
            break
    return clean, liftable, witnesses


def binary_rank(vectors: tuple[int, ...] | list[int]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)


def find_all_bad_subspace(
    bad: set[int], all_edges: int
) -> tuple[int, ...] | None:
    nonzero = sorted(bad - {0})
    seen: set[frozenset[int]] = set()
    for first, second, third in combinations(nonzero, 3):
        if binary_rank([first, second, third]) != 3:
            continue
        span = frozenset(
            (
                first,
                second,
                third,
                first ^ second,
                first ^ third,
                second ^ third,
                first ^ second ^ third,
            )
        )
        if len(span) != 7 or span in seen:
            continue
        seen.add(span)
        if not span <= bad:
            continue
        if (first | second | third) != all_edges:
            continue
        return tuple(sorted(span))
    return None


def rows_from_geng(order: int, geng: str) -> list[str]:
    process = subprocess.run(
        [geng, "-cq", "-d3", "-D3", str(order)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [row for row in process.stdout.splitlines() if row]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=4)
    parser.add_argument("--max-order", type=int, default=12)
    parser.add_argument("--geng", default=shutil.which("geng"))
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if not arguments.geng:
        raise SystemExit("nauty-geng not found; pass --geng PATH")

    summaries = []
    obstruction = None
    for order in range(arguments.min_order, arguments.max_order + 1, 2):
        generated = bridgeless = 0
        bad_histogram: Counter[int] = Counter()
        for graph_index, row in enumerate(rows_from_geng(order, arguments.geng)):
            generated += 1
            decoded_order, edges = decode_graph6(row)
            assert decoded_order == order
            rows = incidence(order, edges)
            assert len(edges) * 2 == 3 * order
            assert all(len(vertex_row) == 3 for vertex_row in rows)
            if not all(
                connected_without_edge(order, edges, edge)
                for edge in range(len(edges))
            ):
                continue
            bridgeless += 1
            basis = cycle_basis(order, edges)
            cycles = enumerate_cycles(basis)
            clean, liftable, _ = classify_projections(order, edges, cycles)
            bad = set(cycles) - clean
            liftable_bad = liftable - clean
            bad_histogram[(len(bad), len(liftable_bad))] += 1
            candidate = find_all_bad_subspace(
                bad, (1 << len(edges)) - 1
            )
            if candidate is not None:
                obstruction = {
                    "bad_projection_count": len(bad),
                    "graph6": row,
                    "graph_index": graph_index,
                    "order": order,
                    "subspace_nonzero_cycles_hex": [
                        hex(value) for value in candidate
                    ],
                }
                break
        summary = {
            "bad_projection_count_histogram": {
                f"{key[0]}_total/{key[1]}_liftable": value
                for key, value in sorted(bad_histogram.items())
            },
            "bridgeless_graphs": bridgeless,
            "connected_cubic_graphs": generated,
            "order": order,
        }
        summaries.append(summary)
        print(json.dumps(summary, sort_keys=True))
        if obstruction is not None:
            print(json.dumps({"obstruction": obstruction}, sort_keys=True))
            break

    result = {
        "obstruction": obstruction,
        "schema": "fano-all-bad-projection-subspace-small-census-v1",
        "summaries": summaries,
    }
    if arguments.output:
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 2 if obstruction is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
