#!/usr/bin/env python3
"""Build a 40-vertex countermodel to one-circuit Fano-flow domination.

This is not a counterexample to the five-cycle double cover conjecture.
It replaces three edges of a ten-vertex Tait graph by aligned two-sums
with the certified ten-vertex bad-flow block.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BAD_BLOCK = (
    ROOT
    / "search/fano-value-class-flow-countermodel-20260726/instance.json"
)

BASE_GRAPH6 = "It?GYDKKO"
BASE_VERTICES = 10
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
NONCYCLABLE = (1, 6, 7)
COLOR_VALUES = (1, 2, 3)
COLOR_LABELS = ((0, 1), (0, 2), (1, 2))


def edges_of(records: list[object]) -> list[tuple[int, int]]:
    edges = []
    for record in records:
        if isinstance(record, dict):
            edges.append((int(record["u"]), int(record["v"])))
        else:
            u, v = record
            edges.append((int(u), int(v)))
    return edges


def graph6(vertices: int, edges: list[tuple[int, int]]) -> str:
    assert 0 <= vertices <= 62
    present = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((u, v) in present)
        for v in range(1, vertices)
        for u in range(v)
    ]
    bits.extend([0] * (-len(bits) % 6))
    return chr(vertices + 63) + "".join(
        chr(
            63
            + sum(
                bits[cursor + shift] << (5 - shift)
                for shift in range(6)
            )
        )
        for cursor in range(0, len(bits), 6)
    )


def pair_permutation(
    source: tuple[int, int], target: tuple[int, int]
) -> tuple[int, ...]:
    for permutation in permutations(range(5)):
        image = tuple(sorted((permutation[source[0]], permutation[source[1]])))
        if image == target:
            return permutation
    raise AssertionError("S5 is not transitive on two-subsets")


def permute_pair(
    pair: tuple[int, int], permutation: tuple[int, ...]
) -> tuple[int, int]:
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))


def graph_checks(
    vertices: int, edges: list[tuple[int, int]], values: list[int]
) -> dict[str, object]:
    incidence: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    for edge, (u, v) in enumerate(edges):
        assert 0 <= u < vertices and 0 <= v < vertices and u != v
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
    parity = [[0] * 5 for _ in range(vertices)]
    sizes = [0] * 5
    for edge, (u, v) in enumerate(edges):
        left, right = labels[edge]
        assert 0 <= left < right < 5
        for coordinate in (left, right):
            parity[u][coordinate] ^= 1
            parity[v][coordinate] ^= 1
            sizes[coordinate] += 1
    return {
        "exact_two": len(edges) == len(labels),
        "even_incidence": all(
            value == 0 for row in parity for value in row
        ),
        "coordinate_edge_counts": sizes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()

    block = json.loads(BAD_BLOCK.read_text(encoding="utf-8"))
    block_edges = edges_of(block["edges"])
    block_values = list(map(int, block["flow_values_by_edge"]))
    block_colors = list(map(int, block["three_edge_coloring_by_edge"]))
    block_labels = [COLOR_LABELS[color] for color in block_colors]
    base_edges = list(BASE_EDGES)
    base_values = [COLOR_VALUES[color] for color in BASE_COLORS]
    base_labels = [COLOR_LABELS[color] for color in BASE_COLORS]
    target = base_values[NONCYCLABLE[0]]
    assert all(base_values[edge] == target for edge in NONCYCLABLE)
    block_port = next(
        edge for edge, value in enumerate(block_values) if value == target
    )

    expanded_edges: list[tuple[int, int]] = []
    expanded_values: list[int] = []
    expanded_labels: list[tuple[int, int]] = []
    origins: list[dict[str, int | str]] = []
    blocks: list[dict[str, object]] = []
    next_vertex = BASE_VERTICES
    selected = set(NONCYCLABLE)
    for edge, endpoints in enumerate(base_edges):
        if edge not in selected:
            expanded_edges.append(endpoints)
            expanded_values.append(base_values[edge])
            expanded_labels.append(base_labels[edge])
            origins.append({"kind": "base", "edge": edge})
            continue

        offset = next_vertex
        next_vertex += int(block["vertices"])
        permutation = pair_permutation(
            block_labels[block_port], base_labels[edge]
        )
        retained: dict[str, int] = {}
        for local, (x, y) in enumerate(block_edges):
            if local == block_port:
                continue
            retained[str(local)] = len(expanded_edges)
            expanded_edges.append((offset + x, offset + y))
            expanded_values.append(block_values[local])
            expanded_labels.append(
                permute_pair(block_labels[local], permutation)
            )
            origins.append(
                {"kind": "bad-block", "base_edge": edge, "edge": local}
            )
        u, v = endpoints
        x, y = block_edges[block_port]
        connectors = (len(expanded_edges), len(expanded_edges) + 1)
        expanded_edges.extend(((u, offset + x), (v, offset + y)))
        expanded_values.extend((target, target))
        expanded_labels.extend((base_labels[edge], base_labels[edge]))
        origins.extend(
            (
                {
                    "kind": "bad-block-connector",
                    "base_edge": edge,
                    "side": 0,
                },
                {
                    "kind": "bad-block-connector",
                    "base_edge": edge,
                    "side": 1,
                },
            )
        )
        blocks.append(
            {
                "replaced_base_edge": edge,
                "block_port_edge": block_port,
                "vertex_offset": offset,
                "cover_coordinate_permutation": list(permutation),
                "connector_edges": list(connectors),
                "retained_edge_map": retained,
            }
        )

    base_checks = graph_checks(BASE_VERTICES, base_edges, base_values)
    base_cover = cover_checks(
        BASE_VERTICES, base_edges, base_labels
    )
    expanded_checks = graph_checks(
        next_vertex, expanded_edges, expanded_values
    )
    expanded_cover = cover_checks(
        next_vertex, expanded_edges, expanded_labels
    )
    required = (
        "simple",
        "cubic",
        "connected",
        "bridgeless",
        "nowhere_zero",
        "flow_conservation",
    )
    assert all(base_checks[key] for key in required)
    assert all(expanded_checks[key] for key in required)
    assert base_cover["exact_two"] and base_cover["even_incidence"]
    assert expanded_cover["exact_two"] and expanded_cover["even_incidence"]

    report = {
        "schema": "small-connected-one-switch-countermodel-v1",
        "status": "EXPLICIT_CONNECTED_SWITCH_LOCAL_COUNTERMODEL",
        "claim_scope": (
            "countermodel to connected one-circuit Fano-flow domination; "
            "not a five-cycle-double-cover counterexample"
        ),
        "five_cdc_counterexample": False,
        "sources": {
            "bad_block": str(BAD_BLOCK.relative_to(ROOT)),
            "base_graph6": BASE_GRAPH6,
        },
        "base": {
            "vertices": BASE_VERTICES,
            "edges": [list(edge) for edge in base_edges],
            "three_edge_coloring_by_edge": list(BASE_COLORS),
            "flow_values_by_edge": base_values,
            "five_cdc_labels_by_edge": [
                f"{left}{right}" for left, right in base_labels
            ],
            "noncyclable_monochromatic_edges": list(NONCYCLABLE),
            "checks": base_checks,
            "five_cdc_checks": base_cover,
        },
        "expanded_graph": {
            "vertices": next_vertex,
            "graph6": graph6(next_vertex, expanded_edges),
            "edges": [list(edge) for edge in expanded_edges],
            "flow_values_by_edge": expanded_values,
            "five_cdc_labels_by_edge": [
                f"{left}{right}" for left, right in expanded_labels
            ],
            "edge_origins": origins,
            "embedded_bad_blocks": blocks,
            "checks": expanded_checks,
            "five_cdc_checks": expanded_cover,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
