#!/usr/bin/env python3
"""Exact audit of generalized cycle-space switches for F2^3 flows.

Values are integers 0,...,7 with XOR addition.  The fixed Fano line is
L={1,2,3}; its affine complement is B={4,5,6,7}.  This file distinguishes:

* a constant-value switch on an arbitrary binary cycle;
* a sequence mixing different switch values; and
* an unrestricted choice of another nowhere-zero flow on the same graph.

The order-12 witness is stable only under the first notion.  It escapes in
two elementary circuit switches and its graph has a connected-kernel flow.
"""

from __future__ import annotations

import argparse
from collections import deque
import json
from pathlib import Path
import subprocess
import sys
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from search.canonical.canonical_search import (
    SimpleGraph,
    parse_graph6,
    validate_simple_cubic,
)
from tools.flow_switch_audit import (
    Graph,
    binary_cycles,
    connected_components,
    elementary_circuits,
    is_bridgeless,
    is_flow,
    line_edge_mask,
    switch_flow,
)


LINE = frozenset((1, 2, 3))
OUTSIDE = frozenset((4, 5, 6, 7))

WITNESS_GRAPH6 = "K?ABAfCi?wF?"
WITNESS_GRAPH = Graph(
    12,
    (
        (0, 5),
        (0, 8),
        (0, 9),
        (1, 6),
        (1, 7),
        (1, 8),
        (2, 6),
        (2, 9),
        (2, 11),
        (3, 7),
        (3, 10),
        (3, 11),
        (4, 9),
        (4, 10),
        (4, 11),
        (5, 8),
        (5, 10),
        (6, 7),
    ),
)
WITNESS_FLOW = (7, 3, 4, 1, 3, 2, 5, 6, 3, 7, 5, 2, 2, 3, 1, 1, 6, 4)
PREPARATION_SWITCH = (1, 2998)
CONNECTING_SWITCH = (4, 67293)


def component_count(graph: Graph, edge_mask: int) -> int:
    return len(
        connected_components(
            graph,
            (
                edge
                for edge in range(graph.edge_count)
                if (edge_mask >> edge) & 1
            ),
        )
    )


def component_reducing_cycles(
    graph: Graph,
    join_mask: int,
    cycles: Iterable[int],
) -> tuple[int, ...]:
    initial = component_count(graph, join_mask)
    return tuple(
        cycle
        for cycle in cycles
        if component_count(graph, join_mask ^ cycle) < initial
    )


def outside_color_masks(
    flow: tuple[int, ...],
) -> dict[int, int]:
    return {
        value: line_edge_mask(flow, (value,))
        for value in sorted(OUTSIDE)
    }


def is_cycle_space_stable(
    graph: Graph,
    flow: tuple[int, ...],
    cycles: Iterable[int],
) -> bool:
    """No single constant-value binary-cycle switch lowers join components."""
    join = line_edge_mask(flow, LINE)
    reducing = component_reducing_cycles(graph, join, cycles)
    masks = outside_color_masks(flow)
    return all(
        cycle & masks[value]
        for value in OUTSIDE
        for cycle in reducing
    )


def fundamental_cycle_space(graph: Graph) -> tuple[int, ...]:
    """Enumerate the binary cycle space from a deterministic spanning tree."""
    if graph.vertices == 0:
        return (0,)
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(graph.vertices)
    ]
    for edge, (first, second) in enumerate(graph.edges):
        adjacency[first].append((second, edge))
        adjacency[second].append((first, edge))
    for row in adjacency:
        row.sort()

    parent = [-1] * graph.vertices
    parent_edge = [-1] * graph.vertices
    depth = [0] * graph.vertices
    parent[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other, edge in adjacency[vertex]:
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            depth[other] = depth[vertex] + 1
            stack.append(other)
    if any(value < 0 for value in parent):
        raise ValueError("fundamental_cycle_space requires a connected graph")

    tree_edges = frozenset(parent_edge[1:])
    basis: list[int] = []
    for edge, (first, second) in enumerate(graph.edges):
        if edge in tree_edges:
            continue
        cycle = 1 << edge
        left, right = first, second
        while depth[left] > depth[right]:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            cycle ^= 1 << parent_edge[left]
            left = parent[left]
            cycle ^= 1 << parent_edge[right]
            right = parent[right]
        basis.append(cycle)

    cycles = [0]
    for basis_cycle in basis:
        cycles.extend(cycle ^ basis_cycle for cycle in tuple(cycles))
    return tuple(sorted(cycles))


def low_assignment_states(
    cycles: Iterable[int],
    join_mask: int,
) -> frozenset[tuple[int, int]]:
    """Pairs of low-coordinate cycles that cover every line-valued edge."""
    cycle_tuple = tuple(cycles)
    return frozenset(
        (first, second)
        for first in cycle_tuple
        for second in cycle_tuple
        if not (join_mask & ~(first | second))
    )


def low_color_masks(
    all_edges: int,
    join_mask: int,
    first: int,
    second: int,
) -> tuple[int, int, int]:
    """Masks of values 1,2,3 on the line-valued join."""
    return (
        join_mask & first & ~second & all_edges,
        join_mask & ~first & second & all_edges,
        join_mask & first & second,
    )


def line_switch_neighbours(
    cycles: Iterable[int],
    all_edges: int,
    join_mask: int,
    state: tuple[int, int],
) -> Iterable[tuple[int, int]]:
    """All states reached by one switch with value in the fixed line."""
    first, second = state
    color_one, color_two, color_three = low_color_masks(
        all_edges, join_mask, first, second
    )
    for cycle in cycles:
        if not (cycle & color_one):
            yield (first ^ cycle, second)
        if not (cycle & color_two):
            yield (first, second ^ cycle)
        if not (cycle & color_three):
            yield (first ^ cycle, second ^ cycle)


def fixed_join_reconfiguration_components(
    cycles: Iterable[int],
    all_edges: int,
    join_mask: int,
) -> tuple[frozenset[tuple[int, int]], ...]:
    """Components under all line-valued switches, which preserve the join."""
    cycle_tuple = tuple(cycles)
    unseen = set(low_assignment_states(cycle_tuple, join_mask))
    components: list[frozenset[tuple[int, int]]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        component = {start}
        queue = deque((start,))
        while queue:
            state = queue.popleft()
            for neighbour in line_switch_neighbours(
                cycle_tuple, all_edges, join_mask, state
            ):
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        components.append(frozenset(component))
    return tuple(components)


def flow_from_coordinates(
    edge_count: int,
    first: int,
    second: int,
    high: int,
) -> tuple[int, ...]:
    return tuple(
        ((first >> edge) & 1)
        | (((second >> edge) & 1) << 1)
        | (((high >> edge) & 1) << 2)
        for edge in range(edge_count)
    )


def canonical_cubic_graphs(
    executable: str,
    order: int,
    project_root: Path,
) -> tuple[tuple[int, str, SimpleGraph], ...]:
    """Materialize quiet geng output and close both subprocess pipes."""
    edge_count = 3 * order // 2
    completed = subprocess.run(
        [
            executable,
            "-cq",
            "-d3",
            "-D3",
            str(order),
            f"{edge_count}:{edge_count}",
        ],
        cwd=project_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    if completed.stderr:
        raise RuntimeError("quiet geng unexpectedly wrote stderr")
    return tuple(
        (index, graph6, parse_graph6(graph6))
        for index, graph6 in enumerate(completed.stdout.splitlines(), 1)
    )


def check_witness() -> dict[str, object]:
    parsed = parse_graph6(WITNESS_GRAPH6)
    assert parsed.vertices == WITNESS_GRAPH.vertices
    assert parsed.edges == WITNESS_GRAPH.edges
    assert is_bridgeless(WITNESS_GRAPH)
    assert is_flow(WITNESS_GRAPH, WITNESS_FLOW)

    cycles = binary_cycles(WITNESS_GRAPH)
    assert cycles == fundamental_cycle_space(WITNESS_GRAPH)
    assert len(cycles) == 128
    circuits = elementary_circuits(WITNESS_GRAPH, cycles)
    assert len(circuits) == 89

    join = line_edge_mask(WITNESS_FLOW, LINE)
    all_edges = (1 << WITNESS_GRAPH.edge_count) - 1
    high = all_edges ^ join
    assert join == 63802
    assert high == 198341
    assert component_count(WITNESS_GRAPH, join) == 2
    reducing = component_reducing_cycles(WITNESS_GRAPH, join, cycles)
    assert reducing == (
        67293,
        68997,
        145088,
        164085,
        198187,
        198341,
        218949,
        223941,
        231110,
    )

    color_masks = outside_color_masks(WITNESS_FLOW)
    assert color_masks == {
        4: 131076,
        5: 1088,
        6: 65664,
        7: 513,
    }
    assert all(mask.bit_count() == 2 for mask in color_masks.values())
    assert all(
        cycle & color_masks[value]
        for value in OUTSIDE
        for cycle in reducing
    )
    assert is_cycle_space_stable(WITNESS_GRAPH, WITNESS_FLOW, cycles)

    switch_histogram: dict[int, int] = {}
    for value in sorted(OUTSIDE):
        for cycle in cycles:
            if cycle & color_masks[value]:
                continue
            switched_join = join ^ cycle
            count = component_count(WITNESS_GRAPH, switched_join)
            switch_histogram[count] = switch_histogram.get(count, 0) + 1
    assert switch_histogram == {2: 14, 3: 26, 4: 36, 5: 38, 6: 14}

    first_value, first_cycle = PREPARATION_SWITCH
    second_value, second_cycle = CONNECTING_SWITCH
    assert first_cycle in circuits and second_cycle in circuits
    prepared = switch_flow(
        WITNESS_GRAPH, WITNESS_FLOW, first_value, first_cycle
    )
    assert line_edge_mask(prepared, LINE) == join
    assert component_count(WITNESS_GRAPH, join) == 2
    connected = switch_flow(
        WITNESS_GRAPH, prepared, second_value, second_cycle
    )
    assert component_count(
        WITNESS_GRAPH, line_edge_mask(connected, LINE)
    ) == 1

    states = low_assignment_states(cycles, join)
    assert len(states) == 576
    stable_states = 0
    reducible_states = 0
    for first, second in states:
        flow = flow_from_coordinates(
            WITNESS_GRAPH.edge_count, first, second, high
        )
        assert is_flow(WITNESS_GRAPH, flow)
        if is_cycle_space_stable(WITNESS_GRAPH, flow, cycles):
            stable_states += 1
        else:
            reducible_states += 1
    assert (stable_states, reducible_states) == (72, 504)

    fixed_join_components = fixed_join_reconfiguration_components(
        cycles, all_edges, join
    )
    assert tuple(map(len, fixed_join_components)) == (576,)

    return {
        "schema": "cycle-space-switch-obstruction-witness-v1",
        "classification": "LOCAL SWITCH OBSTRUCTION / NOT GRAPH-LEVEL",
        "graph6": WITNESS_GRAPH6,
        "vertices": WITNESS_GRAPH.vertices,
        "edges": [
            {"id": edge, "u": first, "v": second}
            for edge, (first, second) in enumerate(WITNESS_GRAPH.edges)
        ],
        "flow": list(WITNESS_FLOW),
        "line": sorted(LINE),
        "join_mask": join,
        "join_components": 2,
        "cycle_space_size": len(cycles),
        "elementary_circuits": len(circuits),
        "component_reducing_cycles": list(reducing),
        "outside_color_masks": {
            str(value): mask for value, mask in color_masks.items()
        },
        "valid_outside_switch_component_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(switch_histogram.items())
        },
        "fixed_join_low_assignments": len(states),
        "fixed_join_locally_stable_assignments": stable_states,
        "fixed_join_reducible_assignments": reducible_states,
        "fixed_join_line_switch_components": [
            len(component) for component in fixed_join_components
        ],
        "escape": {
            "preparation_switch": {
                "value": first_value,
                "cycle_mask": first_cycle,
            },
            "connecting_switch": {
                "value": second_value,
                "cycle_mask": second_cycle,
            },
            "prepared_flow": list(prepared),
            "connected_flow": list(connected),
        },
        "warning": (
            "The witness is stable under one constant-value switch on any "
            "binary cycle, and under every sequence using one fixed outside "
            "value. It escapes after mixing switch values and is not a "
            "counterexample to connected-kernel flow or five-CDC."
        ),
    }


def fixed_join_order_twelve_census(
    geng: str = "geng",
    project_root: Path | None = None,
) -> dict[str, object]:
    """Exact existential recoloring/reduction census at order 12.

    For every complement J of a binary cycle, enumerate all pairs of low
    coordinate cycles until finding a nowhere-zero flow and a color/cycle
    switch that lowers the number of J-components.  A failure is exhausted
    over all low-coordinate pairs.
    """
    root = Path(__file__).resolve().parent.parent if project_root is None else project_root
    totals = {
        "generated_graphs": 0,
        "bridgeless_graphs": 0,
        "nonbridgeless_graphs": 0,
        "cycle_masks": 0,
        "connected_joins": 0,
        "disconnected_joins": 0,
        "realizable_disconnected_joins": 0,
        "unrealizable_disconnected_joins": 0,
        "recolorable_then_reducible_joins": 0,
        "fixed_join_traps": 0,
    }
    for _, _, simple in canonical_cubic_graphs(geng, 12, root):
        totals["generated_graphs"] += 1
        premise = validate_simple_cubic(simple)
        if not premise["bridgeless"]:
            totals["nonbridgeless_graphs"] += 1
            continue
        totals["bridgeless_graphs"] += 1
        graph = Graph(simple.vertices, simple.edges)
        cycles = fundamental_cycle_space(graph)
        assert len(cycles) == 128
        totals["cycle_masks"] += len(cycles)
        all_edges = (1 << graph.edge_count) - 1
        count_cache: dict[int, int] = {}

        def cached_count(mask: int) -> int:
            if mask not in count_cache:
                count_cache[mask] = component_count(graph, mask)
            return count_cache[mask]

        for high in cycles:
            join = all_edges ^ high
            initial = cached_count(join)
            if initial == 1:
                totals["connected_joins"] += 1
                continue
            totals["disconnected_joins"] += 1
            reducing = tuple(
                cycle
                for cycle in cycles
                if cached_count(join ^ cycle) < initial
            )
            realizable = False
            reducible = False
            for first in cycles:
                for second in cycles:
                    if join & ~(first | second):
                        continue
                    realizable = True
                    low_classes = (
                        ~first & ~second,
                        first & ~second,
                        ~first & second,
                        first & second,
                    )
                    if any(
                        not (cycle & high & low_classes[color])
                        for color in range(4)
                        for cycle in reducing
                    ):
                        reducible = True
                        break
                if reducible:
                    break
            if realizable:
                totals["realizable_disconnected_joins"] += 1
            else:
                totals["unrealizable_disconnected_joins"] += 1
            if reducible:
                totals["recolorable_then_reducible_joins"] += 1
            elif realizable:
                totals["fixed_join_traps"] += 1

    assert totals == {
        "generated_graphs": 85,
        "bridgeless_graphs": 81,
        "nonbridgeless_graphs": 4,
        "cycle_masks": 10368,
        "connected_joins": 1236,
        "disconnected_joins": 9132,
        "realizable_disconnected_joins": 9132,
        "unrealizable_disconnected_joins": 0,
        "recolorable_then_reducible_joins": 9132,
        "fixed_join_traps": 0,
    }
    return {
        "schema": "fixed-join-order-12-census-v1",
        "classification": "FINITE STRUCTURAL CENSUS",
        "order": 12,
        "totals": totals,
        "warning": (
            "Recoloring is existential over all low-coordinate assignments; "
            "the census does not assert universal line-switch reachability."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geng", default="geng")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-order-12", action="store_true")
    args = parser.parse_args()

    report: dict[str, object] = {"witness": check_witness()}
    if not args.skip_order_12:
        report["order_12_census"] = fixed_join_order_twelve_census(args.geng)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
