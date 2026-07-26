#!/usr/bin/env python3
"""Find a small bridgeless cubic Tait graph with no Hamiltonian circuit."""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = (
    ROOT
    / "berge-fulkerson/search/canonical/data/geng"
    / "connected-simple-cubic-n{order:02d}.g6"
)


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    vertices = ord(record[0]) - 63
    bits = [
        ((ord(char) - 63) >> shift) & 1
        for char in record[1:]
        for shift in range(5, -1, -1)
    ]
    edges = []
    cursor = 0
    for v in range(1, vertices):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return vertices, edges


def incidence(
    vertices: int, edges: list[tuple[int, int]]
) -> tuple[list[list[int]], list[list[int]]]:
    edge_rows = [[] for _ in range(vertices)]
    neighbours = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        edge_rows[u].append(edge)
        edge_rows[v].append(edge)
        neighbours[u].append(v)
        neighbours[v].append(u)
    return edge_rows, neighbours


def bridgeless(
    vertices: int,
    edges: list[tuple[int, int]],
    edge_rows: list[list[int]],
) -> bool:
    for skipped in range(len(edges)):
        seen = {0}
        stack = [0]
        while stack:
            vertex = stack.pop()
            for edge in edge_rows[vertex]:
                if edge == skipped:
                    continue
                u, v = edges[edge]
                other = v if u == vertex else u
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        if len(seen) < vertices:
            return False
    return True


def tait_coloring(
    vertices: int,
    edges: list[tuple[int, int]],
    edge_rows: list[list[int]],
) -> list[int] | None:
    colors = [-1] * len(edges)
    used = [0] * vertices

    def extend(colored: int) -> bool:
        if colored == len(edges):
            return True
        best_edge = -1
        best_allowed = 0
        best_count = 4
        for edge, (u, v) in enumerate(edges):
            if colors[edge] >= 0:
                continue
            allowed = 0b111 & ~(used[u] | used[v])
            count = allowed.bit_count()
            if count < best_count:
                best_edge, best_allowed, best_count = edge, allowed, count
                if count <= 1:
                    break
        if not best_allowed:
            return False
        u, v = edges[best_edge]
        for color in range(3):
            bit = 1 << color
            if not best_allowed & bit:
                continue
            colors[best_edge] = color
            used[u] |= bit
            used[v] |= bit
            if extend(colored + 1):
                return True
            used[u] ^= bit
            used[v] ^= bit
            colors[best_edge] = -1
        return False

    return colors if extend(0) else None


def hamiltonian_cycle(
    vertices: int, neighbours: list[list[int]]
) -> list[int] | None:
    full = (1 << vertices) - 1
    for first in sorted(neighbours[0]):
        path = [0, first]

        def extend(vertex: int, seen: int) -> bool:
            if seen == full:
                return 0 in neighbours[vertex]
            for other in sorted(neighbours[vertex]):
                bit = 1 << other
                if seen & bit:
                    continue
                path.append(other)
                if extend(other, seen | bit):
                    return True
                path.pop()
            return False

        if extend(first, 1 | (1 << first)):
            return path + [0]
    return None


def cycle_edge_masks(
    vertices: int,
    edges: list[tuple[int, int]],
    edge_rows: list[list[int]],
) -> set[int]:
    """Enumerate the edge sets of all connected circuits."""
    masks: set[int] = set()
    for start in range(vertices):
        path_vertices = [start]
        path_edges: list[int] = []

        def extend(vertex: int, seen: int) -> None:
            for edge in edge_rows[vertex]:
                u, v = edges[edge]
                other = v if u == vertex else u
                if other == start:
                    if len(path_vertices) >= 3:
                        masks.add(
                            sum(1 << item for item in path_edges)
                            | (1 << edge)
                        )
                    continue
                if other < start or seen & (1 << other):
                    continue
                path_vertices.append(other)
                path_edges.append(edge)
                extend(other, seen | (1 << other))
                path_edges.pop()
                path_vertices.pop()

        extend(start, 1 << start)
    return masks


def minimum_noncyclable_color_set(
    colors: list[int], cycle_masks: set[int]
) -> tuple[int, ...] | None:
    """Find a smallest monochromatic edge set in no connected circuit."""
    for size in range(1, len(colors) + 1):
        for color in range(3):
            color_class = [
                edge for edge, value in enumerate(colors) if value == color
            ]
            for selected in combinations(color_class, size):
                mask = sum(1 << edge for edge in selected)
                if all((cycle & mask) != mask for cycle in cycle_masks):
                    return selected
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=20)
    parser.add_argument("--optimize-composition-order", action="store_true")
    arguments = parser.parse_args()
    checked = 0
    best: dict[str, object] | None = None
    for order in range(4, arguments.max_order + 1, 2):
        path = Path(str(SOURCE).format(order=order))
        for index, graph6 in enumerate(path.read_text().splitlines()):
            vertices, edges = decode_graph6(graph6)
            edge_rows, neighbours = incidence(vertices, edges)
            if not bridgeless(vertices, edges, edge_rows):
                continue
            colors = tait_coloring(vertices, edges, edge_rows)
            if colors is None:
                continue
            checked += 1
            cycles = cycle_edge_masks(vertices, edges, edge_rows)
            noncyclable = minimum_noncyclable_color_set(colors, cycles)
            if noncyclable is None:
                continue
            hamiltonian = hamiltonian_cycle(vertices, neighbours)
            record = {
                "status": "FOUND",
                "order": order,
                "source_index": index,
                "graph6": graph6,
                "edges": edges,
                "three_edge_coloring_by_edge": colors,
                "connected_circuit_count": len(cycles),
                "minimum_noncyclable_monochromatic_set": noncyclable,
                "composition_order": order + 10 * len(noncyclable),
                "hamiltonian": hamiltonian is not None,
                "hamiltonian_cycle": hamiltonian,
                "bridgeless_tait_graphs_checked": checked,
            }
            if not arguments.optimize_composition_order:
                print(json.dumps(record, indent=2, sort_keys=True))
                return
            if best is None or int(record["composition_order"]) < int(
                best["composition_order"]
            ):
                best = record
        if (
            best is not None
            and len(best["minimum_noncyclable_monochromatic_set"]) == 3
            and int(best["order"]) <= order
        ):
            break
    print(
        json.dumps(
            best or {"status": "NOT_FOUND", "checked": checked},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
