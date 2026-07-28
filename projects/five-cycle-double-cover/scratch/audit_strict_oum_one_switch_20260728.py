#!/usr/bin/env python3
"""Replay the order-34 strict Oum one-switch sample.

This is an exact checker of the finite assertions stored in
``fixed-fano-pure-merge-strong34-sample500-20260728.json``.  The selection
of 500 flows per graph was random, so a successful replay is not a complete
flow census and not a universal theorem.

For the first merge-bad flow retained on each graph, the checker:

* independently checks the elementary graph properties relevant here;
* enumerates every gauged Oum-compatible potential;
* checks five-colourability and homomorphism to the distance-two graph R_5;
* identifies a K6 or K3 join C5 critical core when present; and
* verifies the displayed legal connected-circuit switch and the repaired
  compatible cover.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import deque
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.fixed_fano_cover_merge_audit import (  # noqa: E402
    PAIR_INDEX,
    direct_potential_merge_audit,
    five_coloring_of_used_pairs,
    fixed_flow_potential_rows,
    gf2_rref,
    graph_incidence,
    labels_from_potentials,
    potential_assignment,
)
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402
from tools.flow_switch_audit import is_flow, switch_flow  # noqa: E402


DEFAULT_SAMPLE = (
    ROOT / "scratch/fixed-fano-pure-merge-strong34-sample500-20260728.json"
)
DEFAULT_SOURCE = (
    ROOT / "search/strong_snarks/source/strongsnarks_34_5_cyc4.g6"
)
EXPECTED_SOURCE_SHA256 = (
    "2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f"
)


def adjacency(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    rows: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    for edge_id, (left, right) in enumerate(edges):
        rows[left].append((right, edge_id))
        rows[right].append((left, edge_id))
    return tuple(tuple(row) for row in rows)


def reached_without(
    rows: tuple[tuple[tuple[int, int], ...], ...],
    removed: frozenset[int],
    start: int,
) -> frozenset[int]:
    reached = {start}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for other, edge_id in rows[vertex]:
            if edge_id in removed or other in reached:
                continue
            reached.add(other)
            queue.append(other)
    return frozenset(reached)


def components_without(
    rows: tuple[tuple[tuple[int, int], ...], ...],
    removed: frozenset[int],
) -> tuple[frozenset[int], ...]:
    unseen = set(range(len(rows)))
    components = []
    while unseen:
        component = reached_without(rows, removed, next(iter(unseen)))
        components.append(component)
        unseen -= component
    return tuple(components)


def induced_has_cycle(
    shore: frozenset[int], edges: tuple[tuple[int, int], ...]
) -> bool:
    internal_edges = sum(
        left in shore and right in shore for left, right in edges
    )
    # Every connected component is a tree exactly when |E|=|V|-components.
    parent = {vertex: vertex for vertex in shore}

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    components = len(shore)
    for left, right in edges:
        if left not in shore or right not in shore:
            continue
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_left] = root_right
            components -= 1
    return internal_edges > len(shore) - components


def graph_audit(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> dict[str, Any]:
    if any(left == right for left, right in edges):
        raise AssertionError("loop in source graph")
    if len({tuple(sorted(edge)) for edge in edges}) != len(edges):
        raise AssertionError("parallel edge in source graph")
    incidence = graph_incidence(vertices, edges)
    rows = adjacency(vertices, edges)
    if len(reached_without(rows, frozenset(), 0)) != vertices:
        raise AssertionError("source graph is disconnected")

    girth = vertices + 1
    for root in range(vertices):
        distance = [-1] * vertices
        parent_edge = [-1] * vertices
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other, edge_id in rows[vertex]:
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    parent_edge[other] = edge_id
                    queue.append(other)
                elif parent_edge[vertex] != edge_id:
                    girth = min(
                        girth, distance[vertex] + distance[other] + 1
                    )

    first_small_cyclic_cut = None
    for cut_size in range(1, 4):
        for removed_tuple in combinations(range(len(edges)), cut_size):
            removed = frozenset(removed_tuple)
            components = components_without(rows, removed)
            if len(components) == 1:
                continue
            # A partition into two cyclic shores exists exactly when at
            # least two components of G-removed contain a cycle.
            cyclic_components = sum(
                induced_has_cycle(component, edges)
                for component in components
            )
            if cyclic_components >= 2:
                first_small_cyclic_cut = list(removed_tuple)
                break
        if first_small_cyclic_cut is not None:
            break
    if first_small_cyclic_cut is not None:
        raise AssertionError(
            f"source graph has cyclic cut below four: {first_small_cyclic_cut}"
        )
    return {
        "vertices": vertices,
        "edges": len(edges),
        "simple": True,
        "cubic": all(len(row) == 3 for row in incidence),
        "connected": True,
        "girth": girth,
        "no_cyclic_edge_cut_below_4": True,
    }


def used_pair_mask(labels: tuple[tuple[int, int], ...]) -> int:
    result = 0
    for pair in labels:
        result |= 1 << PAIR_INDEX[pair]
    return result


R5_NEIGHBORS = tuple(
    frozenset(
        other
        for other in range(32)
        if (word ^ other).bit_count() == 2
    )
    for word in range(32)
)


def r5_homomorphism(used_mask: int) -> tuple[int, ...] | None:
    """Return H -> R_5, where H is the eight-coordinate used-pair graph."""

    graph = [set() for _ in range(8)]
    for pair, index in PAIR_INDEX.items():
        if (used_mask >> index) & 1:
            left, right = pair
            graph[left].add(right)
            graph[right].add(left)
    image = [-1] * 8

    # Translation is an automorphism of R_5, so coordinate zero may map to 0.
    image[0] = 0

    def search() -> bool:
        if all(value >= 0 for value in image):
            return True
        vertex = max(
            (item for item in range(8) if image[item] < 0),
            key=lambda item: (
                sum(image[other] >= 0 for other in graph[item]),
                len(graph[item]),
                -item,
            ),
        )
        candidates = set(range(32))
        for other in graph[vertex]:
            if image[other] >= 0:
                candidates &= R5_NEIGHBORS[image[other]]
        for target in sorted(candidates):
            image[vertex] = target
            if search():
                return True
        image[vertex] = -1
        return False

    return tuple(image) if search() else None


def contains_clique(used_mask: int, vertices: tuple[int, ...]) -> bool:
    return all(
        (used_mask >> PAIR_INDEX[tuple(sorted((left, right)))]) & 1
        for left, right in combinations(vertices, 2)
    )


def critical_core(used_mask: int) -> dict[str, Any] | None:
    for six in combinations(range(8), 6):
        if contains_clique(used_mask, six):
            return {"type": "K6", "vertices": list(six)}
    # K3 join C5: a triangle complete to a chordless five-cycle.
    for triangle in combinations(range(8), 3):
        remaining = tuple(v for v in range(8) if v not in triangle)
        if not contains_clique(used_mask, triangle):
            continue
        if not all(
            (used_mask >> PAIR_INDEX[tuple(sorted((left, right)))]) & 1
            for left in triangle
            for right in remaining
        ):
            continue
        for cycle in permutations_fixing_start(remaining):
            cycle_edges = {
                tuple(sorted((cycle[index], cycle[(index + 1) % 5])))
                for index in range(5)
            }
            if all(
                (used_mask >> PAIR_INDEX[pair]) & 1
                for pair in cycle_edges
            ):
                return {
                    "type": "K3_join_C5",
                    "triangle": list(triangle),
                    "cycle": list(cycle),
                }
    return None


def permutations_fixing_start(
    vertices: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    from itertools import permutations

    first = min(vertices)
    return tuple(
        (first,) + rest
        for rest in permutations(v for v in vertices if v != first)
    )


def all_potential_masks(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
) -> tuple[int, ...]:
    rows = fixed_flow_potential_rows(
        vertices, edges, incidence, flow, fix_translation=True
    )
    pivots = gf2_rref(rows)
    free = tuple(
        variable for variable in range(3 * vertices) if variable not in pivots
    )
    masks = []
    for free_bits in range(1 << len(free)):
        assignment = potential_assignment(pivots, free, free_bits)
        labels = labels_from_potentials(
            vertices, edges, incidence, flow, assignment
        )
        masks.append(used_pair_mask(labels))
    return tuple(masks)


def small_r5_obstruction_audit() -> dict[str, Any]:
    k5_mask = 0
    for pair in combinations(range(5), 2):
        k5_mask |= 1 << PAIR_INDEX[pair]
    k6_mask = 0
    for pair in combinations(range(6), 2):
        k6_mask |= 1 << PAIR_INDEX[pair]
    triangle = (0, 1, 2)
    cycle = (3, 4, 5, 6, 7)
    join_mask = 0
    for pair in combinations(triangle, 2):
        join_mask |= 1 << PAIR_INDEX[pair]
    for left in triangle:
        for right in cycle:
            join_mask |= 1 << PAIR_INDEX[tuple(sorted((left, right)))]
    for index in range(5):
        pair = tuple(sorted((cycle[index], cycle[(index + 1) % 5])))
        join_mask |= 1 << PAIR_INDEX[pair]

    k5_witness = r5_homomorphism(k5_mask)
    if k5_witness is None:
        raise AssertionError("K5 did not map to R5")
    if r5_homomorphism(k6_mask) is not None:
        raise AssertionError("K6 unexpectedly mapped to R5")
    if r5_homomorphism(join_mask) is not None:
        raise AssertionError("K3 join C5 unexpectedly mapped to R5")

    normalized_triangle = (0, 0b00011, 0b00101)
    common_neighbors = sorted(
        set.intersection(
            *(set(R5_NEIGHBORS[word]) for word in normalized_triangle)
        )
    )
    common_edges = [
        [left, right]
        for left, right in combinations(common_neighbors, 2)
        if right in R5_NEIGHBORS[left]
    ]
    if common_neighbors != [0b00110, 0b01001, 0b10001]:
        raise AssertionError("normalized triangle has wrong common neighborhood")
    if common_edges != [[0b01001, 0b10001]]:
        raise AssertionError("normalized common neighborhood is not K1 plus K2")
    return {
        "K5_maps_to_R5": True,
        "K5_image": list(k5_witness),
        "K6_maps_to_R5": False,
        "K3_join_C5_maps_to_R5": False,
        "normalized_triangle": list(normalized_triangle),
        "common_neighbors": common_neighbors,
        "common_neighborhood_edges": common_edges,
    }


def circuit_check(
    vertices: int,
    edges: tuple[tuple[int, int], ...],
    circuit_edges: tuple[int, ...],
) -> None:
    degree = [0] * vertices
    local_rows: list[list[int]] = [[] for _ in range(vertices)]
    for edge_id in circuit_edges:
        left, right = edges[edge_id]
        degree[left] += 1
        degree[right] += 1
        local_rows[left].append(right)
        local_rows[right].append(left)
    support = {vertex for vertex, value in enumerate(degree) if value}
    if not support or any(degree[vertex] != 2 for vertex in support):
        raise AssertionError("displayed switch support is not a circuit")
    reached = {next(iter(support))}
    stack = list(reached)
    while stack:
        vertex = stack.pop()
        for other in local_rows[vertex]:
            if other not in reached:
                reached.add(other)
                stack.append(other)
    if reached != support:
        raise AssertionError("displayed switch support is disconnected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    source_hash = hashlib.sha256(arguments.source.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise AssertionError(f"unexpected source hash {source_hash}")
    source_rows = tuple(
        row.strip()
        for row in arguments.source.read_text(encoding="ascii").splitlines()
        if row.strip() and not row.startswith("#")
    )
    sample = json.loads(arguments.sample.read_text(encoding="utf-8"))
    if sample["status"] != "SAMPLED_PASS":
        raise AssertionError("sample did not record a pass")
    if sample["accepted_per_graph"] != 500:
        raise AssertionError("unexpected sample size")
    if tuple(row["graph6"] for row in sample["graph_rows"]) != source_rows:
        raise AssertionError("sample graph rows differ from frozen source")

    checked_rows = []
    for row in sample["graph_rows"]:
        graph = graph_from_graph6(row["graph6"])
        incidence = graph_incidence(graph.vertices, graph.edges)
        properties = graph_audit(graph.vertices, graph.edges)
        first_bad = row["first_pure_merge_bad_flow"]
        flow = tuple(first_bad["flow_values_by_edge"])
        if not is_flow(graph, flow):
            raise AssertionError("retained starting assignment is not a flow")

        initial_masks = all_potential_masks(
            graph.vertices, graph.edges, incidence, flow
        )
        if any(five_coloring_of_used_pairs(mask) is not None for mask in initial_masks):
            raise AssertionError("retained flow is not five-merge bad")
        initial_r5 = tuple(r5_homomorphism(mask) for mask in initial_masks)
        initial_cores = tuple(critical_core(mask) for mask in initial_masks)
        if any(witness is not None for witness in initial_r5):
            raise AssertionError("retained flow has an R5-compressible cover")
        if any(core is None for core in initial_cores):
            raise AssertionError("a retained cover lacks a K6/K3 join C5 core")

        repair = first_bad["repair"]
        switch_value = int(repair["switch_value"])
        circuit_edges = tuple(int(item) for item in repair["circuit_edges"])
        circuit_check(graph.vertices, graph.edges, circuit_edges)
        if any(flow[edge_id] == switch_value for edge_id in circuit_edges):
            raise AssertionError("displayed circuit switch creates a zero edge")
        circuit_mask = sum(1 << edge_id for edge_id in circuit_edges)
        if circuit_mask != int(repair["circuit_mask"]):
            raise AssertionError("displayed circuit list and mask differ")
        switched = switch_flow(graph, flow, switch_value, circuit_mask)
        if switched != tuple(repair["resulting_flow_values_by_edge"]):
            raise AssertionError("displayed switched flow differs on replay")
        if not is_flow(graph, switched):
            raise AssertionError("displayed switched assignment is not a flow")
        repaired_audit = direct_potential_merge_audit(
            graph.vertices,
            graph.edges,
            incidence,
            switched,
            exhaustive=True,
            criterion="five-color",
        )
        if not repaired_audit["five_color_merge_exists"]:
            raise AssertionError("displayed switch does not repair five merging")

        totals = row["totals"]
        if totals.get("one_circuit_local_bad", 0):
            raise AssertionError("sample contains a retained local bad flow")
        if (
            totals["pure_merge_bad"]
            != totals["one_circuit_repairable"]
        ):
            raise AssertionError("not every sampled bad flow was repaired")
        checked_rows.append(
            {
                "graph_index": row["graph_index"],
                "graph6": row["graph6"],
                "graph_properties": properties,
                "sampled_nowhere_zero_flows": totals[
                    "distinct_nowhere_zero_flows"
                ],
                "sampled_five_merge_bad": totals["pure_merge_bad"],
                "sampled_one_circuit_repairable": totals[
                    "one_circuit_repairable"
                ],
                "first_bad_flow_potential_covers": len(initial_masks),
                "first_bad_flow_all_R5_bad": True,
                "first_bad_flow_core_types": sorted(
                    {core["type"] for core in initial_cores if core is not None}
                ),
                "displayed_repair": {
                    "switch_value": switch_value,
                    "circuit_length": len(circuit_edges),
                    "repair_mechanism": repair["repair_mechanism"],
                    "five_color_witness": repaired_audit[
                        "first_five_color_witness"
                    ],
                },
            }
        )

    aggregate = {
        "sampled_nowhere_zero_flows": sum(
            row["sampled_nowhere_zero_flows"] for row in checked_rows
        ),
        "sampled_five_merge_bad": sum(
            row["sampled_five_merge_bad"] for row in checked_rows
        ),
        "sampled_one_circuit_repairable": sum(
            row["sampled_one_circuit_repairable"] for row in checked_rows
        ),
    }
    report = {
        "schema": "strict-oum-order34-one-switch-replay-v1",
        "status": "PASS",
        "scope_warning": (
            "Exact replay for retained finite witnesses, but the 500 flows "
            "per graph were randomly sampled. This is not a flow census or "
            "a universal one-switch theorem."
        ),
        "source": str(arguments.source),
        "source_sha256": source_hash,
        "graphs": len(checked_rows),
        "aggregate": aggregate,
        "small_R5_obstruction_audit": small_r5_obstruction_audit(),
        "graph_rows": checked_rows,
    }
    if aggregate != {
        "sampled_nowhere_zero_flows": 3500,
        "sampled_five_merge_bad": 1528,
        "sampled_one_circuit_repairable": 1528,
    }:
        raise AssertionError(f"unexpected aggregate {aggregate}")
    if arguments.output:
        arguments.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
