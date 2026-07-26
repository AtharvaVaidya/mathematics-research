#!/usr/bin/env python3
"""Independent semantic checker for the 40-vertex countermodel.

This file deliberately does not import the producer.  It reconstructs the
two-sums, enumerates every circuit of the ten-vertex base and the expanded
graph, checks the explicit five-CDC, and literally enumerates the T-joins
of the bad block.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BAD_BLOCK = (
    ROOT
    / "search/fano-value-class-flow-countermodel-20260726/instance.json"
)
BASE_GRAPH6 = "It?GYDKKO"
BASE_EDGES = (
    (0, 1),
    (0, 2),
    (0, 3),
    (2, 3),
    (4, 5),
    (4, 6),
    (5, 6),
    (1, 7),
    (6, 7),
    (1, 8),
    (4, 8),
    (5, 8),
    (2, 9),
    (3, 9),
    (7, 9),
)
BASE_COLORS = (0, 1, 2, 0, 2, 0, 1, 1, 2, 2, 1, 0, 2, 1, 0)
P = (1, 6, 7)
COLOR_VALUES = (1, 2, 3)
COLOR_LABELS = ((0, 1), (0, 2), (1, 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def edges_of(records: list[object]) -> list[tuple[int, int]]:
    edges = []
    for record in records:
        if isinstance(record, dict):
            edges.append((int(record["u"]), int(record["v"])))
        else:
            u, v = record
            edges.append((int(u), int(v)))
    return edges


def decode_graph6(record: str) -> tuple[int, list[tuple[int, int]]]:
    require(1 <= ord(record[0]) - 63 <= 62, "unsupported graph6 order")
    vertices = ord(record[0]) - 63
    bits = [
        ((ord(character) - 63) >> shift) & 1
        for character in record[1:]
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


def graph_checks(
    vertices: int, edges: list[tuple[int, int]], values: list[int]
) -> dict[str, object]:
    require(len(edges) == len(values), "edge/value length mismatch")
    incidence: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        require(0 <= u < vertices and 0 <= v < vertices, "bad endpoint")
        require(u != v, "loop")
        incidence[u].append((v, edge))
        incidence[v].append((u, edge))

    def reached(skipped: int | None = None) -> int:
        seen = 1
        stack = [0]
        while stack:
            vertex = stack.pop()
            for other, edge in incidence[vertex]:
                if edge == skipped or (seen >> other) & 1:
                    continue
                seen |= 1 << other
                stack.append(other)
        return seen

    full = (1 << vertices) - 1
    connected = reached() == full
    return {
        "simple": len({tuple(sorted(edge)) for edge in edges}) == len(edges),
        "cubic": all(len(row) == 3 for row in incidence),
        "connected": connected,
        "bridgeless": connected
        and all(reached(edge) == full for edge in range(len(edges))),
        "nowhere_zero": all(1 <= value <= 7 for value in values),
        "flow_conservation": all(
            values[row[0][1]] ^ values[row[1][1]] ^ values[row[2][1]]
            == 0
            for row in incidence
        ),
        "value_class_sizes": {
            str(key): value for key, value in sorted(Counter(values).items())
        },
    }


def cover_checks(
    vertices: int,
    edges: list[tuple[int, int]],
    labels: list[tuple[int, int]],
) -> dict[str, object]:
    require(len(edges) == len(labels), "edge/label length mismatch")
    parity = [[0] * 5 for _ in range(vertices)]
    sizes = [0] * 5
    for edge, (u, v) in enumerate(edges):
        left, right = labels[edge]
        require(0 <= left < right < 5, "label is not a two-subset")
        for coordinate in (left, right):
            parity[u][coordinate] ^= 1
            parity[v][coordinate] ^= 1
            sizes[coordinate] += 1
    return {
        "exact_two": True,
        "even_incidence": all(
            value == 0 for row in parity for value in row
        ),
        "coordinate_edge_counts": sizes,
    }


def parse_label(label: str) -> tuple[int, int]:
    result = tuple(sorted(map(int, label)))
    require(len(result) == 2 and result[0] < result[1], "bad label")
    return result


def permute_pair(
    pair: tuple[int, int], permutation: tuple[int, ...]
) -> tuple[int, int]:
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))


def cycle_masks(
    vertices: int, edges: list[tuple[int, int]]
) -> set[int]:
    incidence: list[list[int]] = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        incidence[u].append(edge)
        incidence[v].append(edge)
    cycles: set[int] = set()
    for start in range(vertices):
        path_vertices = [start]
        path_edges: list[int] = []

        def extend(vertex: int, seen: int) -> None:
            for edge in incidence[vertex]:
                u, v = edges[edge]
                other = v if u == vertex else u
                if other == start:
                    if len(path_vertices) >= 3:
                        cycles.add(
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
    return cycles


def bad_graft_table(
    vertices: int,
    edges: list[tuple[int, int]],
    values: list[int],
) -> dict[str, dict[str, int]]:
    result = {}
    for target in range(1, 8):
        removed = {edge for edge, value in enumerate(values) if value == target}
        terminals = 0
        for edge in removed:
            u, v = edges[edge]
            terminals ^= (1 << u) ^ (1 << v)
        available = [edge for edge in range(len(edges)) if edge not in removed]
        joins: list[int] = []
        for selected in range(1 << len(available)):
            boundary = 0
            mask = 0
            for bit, edge in enumerate(available):
                if not (selected >> bit) & 1:
                    continue
                mask |= 1 << edge
                u, v = edges[edge]
                boundary ^= (1 << u) ^ (1 << v)
            if boundary == terminals:
                joins.append(mask)
        disjoint_pairs = sum(
            1
            for left in range(len(joins))
            for right in range(left + 1, len(joins))
            if joins[left] & joins[right] == 0
        )
        require(disjoint_pairs == 0, f"bad block packs for value {target}")
        result[str(target)] = {
            "matching_edges": len(removed),
            "t_joins": len(joins),
            "disjoint_pairs": disjoint_pairs,
        }
    return result


def reconstruct(
    report: dict[str, object],
    block_edges: list[tuple[int, int]],
    block_values: list[int],
    block_labels: list[tuple[int, int]],
) -> tuple[
    list[tuple[int, int]],
    list[int],
    list[tuple[int, int]],
    list[set[int]],
]:
    expanded = report["expanded_graph"]
    records = {
        int(record["replaced_base_edge"]): record
        for record in expanded["embedded_bad_blocks"]
    }
    require(set(records) == set(P), "wrong replaced base edges")
    edges: list[tuple[int, int]] = []
    values: list[int] = []
    labels: list[tuple[int, int]] = []
    footprints: list[set[int]] = []
    base_values = [COLOR_VALUES[color] for color in BASE_COLORS]
    base_labels = [COLOR_LABELS[color] for color in BASE_COLORS]
    for edge, endpoints in enumerate(BASE_EDGES):
        if edge not in records:
            edges.append(endpoints)
            values.append(base_values[edge])
            labels.append(base_labels[edge])
            continue
        record = records[edge]
        port = int(record["block_port_edge"])
        offset = int(record["vertex_offset"])
        permutation = tuple(
            map(int, record["cover_coordinate_permutation"])
        )
        require(
            sorted(permutation) == list(range(5)),
            "bad coordinate permutation",
        )
        require(
            block_values[port] == base_values[edge],
            "flow ports not aligned",
        )
        require(
            permute_pair(block_labels[port], permutation)
            == base_labels[edge],
            "cover ports not aligned",
        )
        footprint: set[int] = set()
        retained: dict[str, int] = {}
        for local, (x, y) in enumerate(block_edges):
            if local == port:
                continue
            retained[str(local)] = len(edges)
            footprint.add(len(edges))
            edges.append((offset + x, offset + y))
            values.append(block_values[local])
            labels.append(permute_pair(block_labels[local], permutation))
        u, v = endpoints
        x, y = block_edges[port]
        connectors = [len(edges), len(edges) + 1]
        footprint.update(connectors)
        edges.extend(((u, offset + x), (v, offset + y)))
        values.extend((base_values[edge], base_values[edge]))
        labels.extend((base_labels[edge], base_labels[edge]))
        require(
            retained == record["retained_edge_map"],
            "retained edge map differs",
        )
        require(
            connectors == list(map(int, record["connector_edges"])),
            "connector ids differ",
        )
        footprints.append(footprint)
    require(edges == edges_of(expanded["edges"]), "expanded edges differ")
    require(
        values == list(map(int, expanded["flow_values_by_edge"])),
        "expanded values differ",
    )
    require(
        labels
        == [parse_label(label) for label in expanded["five_cdc_labels_by_edge"]],
        "expanded labels differ",
    )
    return edges, values, labels, footprints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    report = json.loads((HERE / "construction.json").read_text(encoding="utf-8"))
    block = json.loads(BAD_BLOCK.read_text(encoding="utf-8"))
    block_edges = edges_of(block["edges"])
    block_values = list(map(int, block["flow_values_by_edge"]))
    block_labels = [
        COLOR_LABELS[int(color)]
        for color in block["three_edge_coloring_by_edge"]
    ]

    decoded_vertices, decoded_edges = decode_graph6(BASE_GRAPH6)
    require(decoded_vertices == 10, "base graph6 order differs")
    require(decoded_edges == list(BASE_EDGES), "base graph6 edges differ")
    base = report["base"]
    require(int(base["vertices"]) == 10, "base order differs")
    require(edges_of(base["edges"]) == list(BASE_EDGES), "base edges differ")
    require(
        tuple(map(int, base["three_edge_coloring_by_edge"])) == BASE_COLORS,
        "base coloring differs",
    )
    require(
        tuple(map(int, base["noncyclable_monochromatic_edges"])) == P,
        "base P differs",
    )
    base_values = [COLOR_VALUES[color] for color in BASE_COLORS]
    base_labels = [COLOR_LABELS[color] for color in BASE_COLORS]
    base_checks = graph_checks(10, list(BASE_EDGES), base_values)
    require(base_checks == base["checks"], "base graph checks differ")
    base_cover = cover_checks(10, list(BASE_EDGES), base_labels)
    require(base_cover == base["five_cdc_checks"], "base cover differs")
    incidence_colors = [[] for _ in range(10)]
    for edge, (u, v) in enumerate(BASE_EDGES):
        incidence_colors[u].append(BASE_COLORS[edge])
        incidence_colors[v].append(BASE_COLORS[edge])
    require(
        all(sorted(row) == [0, 1, 2] for row in incidence_colors),
        "base is not Tait colored",
    )
    require(
        len({BASE_COLORS[edge] for edge in P}) == 1,
        "P is not monochromatic",
    )
    base_cycles = cycle_masks(10, list(BASE_EDGES))
    p_mask = sum(1 << edge for edge in P)
    require(
        all(cycle & p_mask != p_mask for cycle in base_cycles),
        "P lies on a base circuit",
    )

    bad_grafts = bad_graft_table(
        int(block["vertices"]), block_edges, block_values
    )
    edges, values, labels, footprints = reconstruct(
        report, block_edges, block_values, block_labels
    )
    expanded = report["expanded_graph"]
    vertices = int(expanded["vertices"])
    expanded_graph6_vertices, expanded_graph6_edges = decode_graph6(
        str(expanded["graph6"])
    )
    require(
        expanded_graph6_vertices == vertices
        and set(expanded_graph6_edges) == {
            tuple(sorted(edge)) for edge in edges
        },
        "expanded graph6 differs",
    )
    labelg = shutil.which("labelg")
    canonical = (HERE / "canonical.g6").read_text(encoding="ascii").strip()
    if labelg is not None:
        canonicalized = subprocess.run(
            [labelg, "-q"],
            input=str(expanded["graph6"]) + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        require(canonicalized.returncode == 0, "nauty labelg failed")
        require(
            canonicalized.stdout.strip() == canonical,
            "canonical graph6 differs",
        )
    expanded_checks = graph_checks(vertices, edges, values)
    require(expanded_checks == expanded["checks"], "expanded checks differ")
    expanded_cover = cover_checks(vertices, edges, labels)
    require(
        expanded_cover == expanded["five_cdc_checks"],
        "expanded cover differs",
    )
    expanded_cycles = cycle_masks(vertices, edges)
    require(footprints and len(footprints) == 3, "wrong block count")
    require(
        all(
            any(
                cycle & sum(1 << edge for edge in footprint) == 0
                for footprint in footprints
            )
            for cycle in expanded_cycles
        ),
        "an expanded circuit touches every bad block",
    )

    result = {
        "status": "ACCEPTED",
        "scope": (
            "40-vertex connected one-switch domination countermodel; "
            "not a five-CDC counterexample"
        ),
        "base_graph6": BASE_GRAPH6,
        "base_checks": base_checks,
        "base_connected_circuits": len(base_cycles),
        "base_noncyclable_edges": list(P),
        "bad_grafts": bad_grafts,
        "expanded_checks": expanded_checks,
        "expanded_graph6": expanded["graph6"],
        "nauty_canonical_graph6": canonical,
        "nauty_canonicalization_checked": labelg is not None,
        "expanded_five_cdc_checks": expanded_cover,
        "expanded_connected_circuits": len(expanded_cycles),
        "every_expanded_circuit_misses_a_bad_block": True,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
