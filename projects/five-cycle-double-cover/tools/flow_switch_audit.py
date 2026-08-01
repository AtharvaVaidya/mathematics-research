#!/usr/bin/env python3
"""Exact finite checks for the F2^3 quotient/lift and flow-switch audit.

The code uses only the Python standard library.  Flow values are the integers
0,...,7 with bitwise XOR as addition in F2^3.  Graph edges are indexed, so
parallel edges remain distinct.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Iterator


FANO_LINES = tuple(
    sorted(
        {
            tuple(sorted((first, second, first ^ second)))
            for first, second in combinations(range(1, 8), 2)
        }
    )
)
D5 = tuple((1 << first) | (1 << second) for first, second in combinations(range(5), 2))
D5_SET = frozenset(D5)


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: tuple[tuple[int, int], ...]

    @property
    def edge_count(self) -> int:
        return len(self.edges)


FIXED_EIGHT_GRAPH = Graph(
    8,
    (
        (0, 1),
        (0, 3),
        (0, 2),
        (1, 2),
        (1, 5),
        (2, 6),
        (3, 7),
        (3, 5),
        (4, 6),
        (4, 5),
        (4, 7),
        (6, 7),
    ),
)
FIXED_EIGHT_FLOW = (4, 5, 1, 2, 6, 3, 7, 2, 1, 4, 5, 2)
FIXED_EIGHT_SWITCH_MASK = sum(1 << index for index in (0, 1, 4, 7))

ORDER_TEN_RESISTANT_FLOW = (2, 1, 3, 5, 6, 3, 6, 7, 1, 7, 5, 4, 1, 2, 4)
ORDER_TEN_FIRST_SWITCH = (1, 2589)
ORDER_TEN_SECOND_SWITCH = (2, 515)
K4_SURJECTIVE_CIRCUIT_FLOW = (3, 5, 6, 1, 2, 4)
K4_SURJECTIVE_CIRCUIT_LINE = (1, 6, 7)


def load_graph(path: Path) -> Graph:
    data = json.loads(path.read_text())
    edges = tuple(
        (int(edge["u"]), int(edge["v"]))
        for edge in sorted(data["edges"], key=lambda edge: int(edge["id"]))
    )
    return Graph(int(data["vertices"]), edges)


def connected_components(
    graph: Graph, edge_indices: Iterable[int] | None = None
) -> tuple[frozenset[int], ...]:
    adjacency = [set() for _ in range(graph.vertices)]
    indices = range(graph.edge_count) if edge_indices is None else edge_indices
    for index in indices:
        first, second = graph.edges[index]
        adjacency[first].add(second)
        adjacency[second].add(first)
    unseen = set(range(graph.vertices))
    result: list[frozenset[int]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        component = {start}
        queue = deque((start,))
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        result.append(frozenset(component))
    return tuple(result)


def is_bridgeless(graph: Graph) -> bool:
    if graph.vertices == 0:
        return True
    original_components = len(connected_components(graph))
    for omitted in range(graph.edge_count):
        remaining = (index for index in range(graph.edge_count) if index != omitted)
        if len(connected_components(graph, remaining)) > original_components:
            return False
    return True


def selected_degrees(graph: Graph, mask: int) -> tuple[int, ...]:
    degree = [0] * graph.vertices
    for index, (first, second) in enumerate(graph.edges):
        if (mask >> index) & 1:
            degree[first] += 1
            degree[second] += 1
    return tuple(degree)


def binary_cycles(graph: Graph) -> tuple[int, ...]:
    """All even edge sets, represented as edge-bit masks."""
    result = []
    for mask in range(1 << graph.edge_count):
        if all(value % 2 == 0 for value in selected_degrees(graph, mask)):
            result.append(mask)
    return tuple(result)


def elementary_circuits(graph: Graph, cycles: Iterable[int] | None = None) -> tuple[int, ...]:
    """All nonempty connected 2-regular edge sets."""
    candidates = binary_cycles(graph) if cycles is None else cycles
    result = []
    for mask in candidates:
        if mask == 0:
            continue
        degrees = selected_degrees(graph, mask)
        if any(value not in (0, 2) for value in degrees):
            continue
        active_vertices = frozenset(
            vertex for vertex, degree in enumerate(degrees) if degree != 0
        )
        selected = tuple(
            index for index in range(graph.edge_count) if (mask >> index) & 1
        )
        components = connected_components(graph, selected)
        nontrivial = tuple(
            component & active_vertices
            for component in components
            if component & active_vertices
        )
        if len(nontrivial) == 1 and nontrivial[0] == active_vertices:
            result.append(mask)
    return tuple(result)


def is_flow(graph: Graph, flow: tuple[int, ...], nowhere_zero: bool = True) -> bool:
    if len(flow) != graph.edge_count:
        return False
    if nowhere_zero and any(value == 0 for value in flow):
        return False
    boundary = [0] * graph.vertices
    for value, (first, second) in zip(flow, graph.edges):
        boundary[first] ^= value
        boundary[second] ^= value
    return not any(boundary)


def enumerate_nowhere_zero_flows(
    graph: Graph, cycles: tuple[int, ...] | None = None
) -> Iterator[tuple[int, ...]]:
    """Enumerate every F2^3-flow as three independently chosen binary cycles."""
    cycle_space = binary_cycles(graph) if cycles is None else cycles
    for first, second, third in product(cycle_space, repeat=3):
        flow = tuple(
            ((first >> edge) & 1)
            | (((second >> edge) & 1) << 1)
            | (((third >> edge) & 1) << 2)
            for edge in range(graph.edge_count)
        )
        if 0 not in flow:
            yield flow


def bad_components(
    graph: Graph, flow: tuple[int, ...], line: Iterable[int]
) -> tuple[frozenset[int], ...]:
    line_set = frozenset(line)
    line_edges = tuple(
        index for index, value in enumerate(flow) if value in line_set
    )
    components = connected_components(graph, line_edges)
    outside = frozenset(range(1, 8)) - line_set
    bad = []
    for component in components:
        boundary_values = Counter()
        for index, (first, second) in enumerate(graph.edges):
            if (first in component) ^ (second in component):
                boundary_values[flow[index]] += 1
        odd_support = frozenset(
            value for value, count in boundary_values.items() if count % 2
        )
        if odd_support == outside:
            bad.append(component)
    return tuple(bad)


def good_lines(graph: Graph, flow: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(line for line in FANO_LINES if not bad_components(graph, flow, line))


def line_edge_mask(flow: tuple[int, ...], line: Iterable[int]) -> int:
    line_set = frozenset(line)
    return sum(1 << edge for edge, value in enumerate(flow) if value in line_set)


def line_component_count(
    graph: Graph, flow: tuple[int, ...], line: Iterable[int]
) -> int:
    mask = line_edge_mask(flow, line)
    return len(
        connected_components(
            graph,
            (edge for edge in range(graph.edge_count) if (mask >> edge) & 1),
        )
    )


def connected_kernel_lines(
    graph: Graph, flow: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    """Fano lines whose value subgraph is connected and spanning."""
    return tuple(
        line for line in FANO_LINES if line_component_count(graph, flow, line) == 1
    )


def switch_flow(
    graph: Graph,
    flow: tuple[int, ...],
    value: int,
    cycle_mask: int,
    *,
    require_cycle: bool = True,
) -> tuple[int, ...]:
    if value not in range(1, 8):
        raise ValueError("switch value must be nonzero in F2^3")
    if require_cycle and any(
        degree % 2 for degree in selected_degrees(graph, cycle_mask)
    ):
        raise ValueError("switch support is not a binary cycle")
    if any(
        ((cycle_mask >> edge) & 1) and flow[edge] == value
        for edge in range(graph.edge_count)
    ):
        raise ValueError("switch would create a zero edge")
    switched = tuple(
        label ^ value if (cycle_mask >> edge) & 1 else label
        for edge, label in enumerate(flow)
    )
    assert is_flow(graph, switched)
    return switched


def switch_neighbours(
    graph: Graph,
    flow: tuple[int, ...],
    circuit_masks: Iterable[int],
) -> Iterator[tuple[int, ...]]:
    for value in range(1, 8):
        for mask in circuit_masks:
            if any(
                ((mask >> edge) & 1) and flow[edge] == value
                for edge in range(graph.edge_count)
            ):
                continue
            # `circuit_masks` has already been checked as a family of binary
            # cycles.  Avoid rechecking conservation for every neighbour in
            # the exhaustive census.
            yield tuple(
                label ^ value if (mask >> edge) & 1 else label
                for edge, label in enumerate(flow)
            )


def brute_lift_exists(
    graph: Graph,
    flow: tuple[int, ...],
    line: Iterable[int],
    cycles: Iterable[int],
) -> bool:
    """Brute-force the partial-cycle extension in the quotient-lift theorem.

    On the four outside values, use any fixed odd forced-bit function.  The
    existence result is independent of that choice.
    """
    line_set = frozenset(line)
    outside = sorted(frozenset(range(1, 8)) - line_set)
    forced_one = outside[0]
    for mask in cycles:
        if all(
            value in line_set
            or ((mask >> edge) & 1) == int(value == forced_one)
            for edge, value in enumerate(flow)
        ):
            return True
    return False


def linear_maps_gl3() -> tuple[tuple[int, ...], ...]:
    result = []
    for images in product(range(1, 8), repeat=3):
        mapping = tuple(
            (images[0] if value & 1 else 0)
            ^ (images[1] if value & 2 else 0)
            ^ (images[2] if value & 4 else 0)
            for value in range(8)
        )
        if len(set(mapping)) == 8:
            result.append(mapping)
    assert len(result) == 168
    return tuple(result)


def check_quotient_geometry() -> None:
    even_five = frozenset(value for value in range(32) if value.bit_count() % 2 == 0)
    caps = tuple(value for value in even_five if value.bit_count() == 4)
    assert len(even_five) == 16 and len(caps) == 5
    for kernel in caps:
        seen: set[frozenset[int]] = set()
        allowed_counts = []
        for value in even_five:
            coset = frozenset((value, value ^ kernel))
            if coset in seen:
                continue
            seen.add(coset)
            allowed_counts.append(len(coset & D5_SET))
        assert sorted(allowed_counts) == [0, 1, 1, 1, 1, 2, 2, 2]

    kernel = 0b01111
    basis_images = (0b00011, 0b00101, 0b10001)

    def section(value: int) -> int:
        return (
            (basis_images[0] if value & 1 else 0)
            ^ (basis_images[1] if value & 2 else 0)
            ^ (basis_images[2] if value & 4 else 0)
        )

    free = set()
    forced: dict[int, int] = {}
    for value in range(1, 8):
        lifts = (section(value), section(value) ^ kernel)
        bits = [bit for bit, lift in enumerate(lifts) if lift in D5_SET]
        if len(bits) == 2:
            free.add(value)
        else:
            assert len(bits) == 1
            forced[value] = bits[0]
    assert free == {1, 2, 3}
    assert forced == {4: 0, 5: 0, 6: 0, 7: 1}
    for functional in range(8):
        parity = 0
        for value, forced_bit in forced.items():
            parity ^= forced_bit ^ ((functional & value).bit_count() % 2)
        assert parity == 1


def toggle_vector(
    graph: Graph,
    flow: tuple[int, ...],
    line: Iterable[int],
    switch_value: int,
    cycle_mask: int,
) -> tuple[int, ...]:
    """Bad-component toggles for a fixed-line, fixed-value switch.

    This is defined when `switch_value` lies on `line`, the support is a
    binary cycle, and the support avoids all edges currently valued
    `switch_value`.
    """
    line_set = frozenset(line)
    if switch_value not in line_set:
        raise ValueError("the switch value must lie on the fixed line")
    switched = switch_flow(graph, flow, switch_value, cycle_mask)
    assert frozenset(
        edge for edge, value in enumerate(flow) if value in line_set
    ) == frozenset(
        edge for edge, value in enumerate(switched) if value in line_set
    )
    original_bad = frozenset(bad_components(graph, flow, line_set))
    switched_bad = frozenset(bad_components(graph, switched, line_set))
    components = connected_components(
        graph,
        tuple(edge for edge, value in enumerate(flow) if value in line_set),
    )
    return tuple(
        int((component in original_bad) ^ (component in switched_bad))
        for component in components
    )


def check_fixed_examples() -> None:
    graph = FIXED_EIGHT_GRAPH
    flow = FIXED_EIGHT_FLOW
    assert is_bridgeless(graph)
    assert is_flow(graph, flow)
    assert all(len(bad_components(graph, flow, line)) == 2 for line in FANO_LINES)

    cycles = binary_cycles(graph)
    assert len(cycles) == 32
    for line in FANO_LINES:
        assert brute_lift_exists(graph, flow, line, cycles) == bool(
            not bad_components(graph, flow, line)
        )
        assert len(bad_components(graph, flow, line)) % 2 == 0
        join_mask = line_edge_mask(flow, line)
        assert all(degree % 2 == 1 for degree in selected_degrees(graph, join_mask))

        # For a line value, translation preserves line membership.  For an
        # outside value it swaps the line subspace with its affine coset, so
        # the line-valued join changes by symmetric difference with the
        # switch cycle.
        for value in range(1, 8):
            for mask in cycles:
                if mask & line_edge_mask(flow, (value,)):
                    continue
                switched_flow = switch_flow(graph, flow, value, mask)
                expected_join = join_mask if value in line else join_mask ^ mask
                assert line_edge_mask(switched_flow, line) == expected_join

    switched = switch_flow(graph, flow, 1, FIXED_EIGHT_SWITCH_MASK)
    assert 6 not in switched
    assert good_lines(graph, switched) == (
        (1, 2, 3),
        (1, 4, 5),
        (2, 5, 7),
        (3, 4, 7),
    )

    for mapping in linear_maps_gl3():
        mapped_flow = tuple(mapping[value] for value in flow)
        for line in FANO_LINES:
            mapped_line = tuple(sorted(mapping[value] for value in line))
            assert len(bad_components(graph, flow, line)) == len(
                bad_components(graph, mapped_flow, mapped_line)
            )

    # Verify the exact fixed-line toggle law for every allowed line-valued
    # switch and every binary cycle on the eight-vertex example.
    for line in FANO_LINES:
        original_bad = frozenset(bad_components(graph, flow, line))
        components = connected_components(
            graph,
            tuple(edge for edge, value in enumerate(flow) if value in line),
        )
        original_vector = tuple(
            int(component in original_bad) for component in components
        )
        for value in line:
            for mask in cycles:
                if any(
                    ((mask >> edge) & 1) and flow[edge] == value
                    for edge in range(graph.edge_count)
                ):
                    continue
                switched_flow = switch_flow(graph, flow, value, mask)
                switched_bad = frozenset(bad_components(graph, switched_flow, line))
                switched_vector = tuple(
                    int(component in switched_bad) for component in components
                )
                toggles = toggle_vector(graph, flow, line, value, mask)
                assert tuple(
                    before ^ toggle
                    for before, toggle in zip(original_vector, toggles)
                ) == switched_vector


def analyze_graph(graph: Graph) -> dict[str, int]:
    cycles = binary_cycles(graph)
    circuits = elementary_circuits(graph, cycles)
    component_count = tuple(
        len(
            connected_components(
                graph,
                (
                    edge
                    for edge in range(graph.edge_count)
                    if (mask >> edge) & 1
                ),
            )
        )
        for mask in range(1 << graph.edge_count)
    )
    flows = frozenset(enumerate_nowhere_zero_flows(graph, cycles))
    good_builder = set()
    connected_kernel_flow_count = 0
    disconnected_line_pairs = 0
    one_switch_stable_disconnected_pairs = 0
    for flow in flows:
        assert is_flow(graph, flow)
        line_bad_counts = tuple(
            len(bad_components(graph, flow, line)) for line in FANO_LINES
        )
        assert all(count % 2 == 0 for count in line_bad_counts)
        if 0 in line_bad_counts:
            good_builder.add(flow)
        if len(set(flow)) < 7:
            assert 0 in line_bad_counts

        value_masks = [0] * 8
        for edge, value in enumerate(flow):
            value_masks[value] |= 1 << edge
        has_connected_kernel = False
        for line in FANO_LINES:
            join_mask = (
                value_masks[line[0]]
                | value_masks[line[1]]
                | value_masks[line[2]]
            )
            join_components = component_count[join_mask]
            if join_components == 1:
                has_connected_kernel = True
                continue
            disconnected_line_pairs += 1
            line_set = frozenset(line)
            reducible_in_one = any(
                not (circuit & value_masks[switch_value])
                and component_count[join_mask ^ circuit] < join_components
                for switch_value in range(1, 8)
                if switch_value not in line_set
                for circuit in circuits
            )
            if not reducible_in_one:
                one_switch_stable_disconnected_pairs += 1
        connected_kernel_flow_count += int(has_connected_kernel)
    good = frozenset(good_builder)

    bad = flows - good
    distance_one = frozenset(
        flow
        for flow in bad
        if any(
            neighbour in good
            for neighbour in switch_neighbours(graph, flow, circuits)
        )
    )
    after_one = bad - distance_one
    distance_two = frozenset(
        flow
        for flow in after_one
        if any(
            neighbour in distance_one
            for neighbour in switch_neighbours(graph, flow, circuits)
        )
    )
    unresolved = after_one - distance_two
    return {
        "binary_cycles": len(cycles),
        "elementary_circuits": len(circuits),
        "nowhere_zero_flows": len(flows),
        "already_good": len(good),
        "connected_kernel_flows": connected_kernel_flow_count,
        "disconnected_line_pairs": disconnected_line_pairs,
        "one_switch_stable_disconnected_pairs": one_switch_stable_disconnected_pairs,
        "distance_one": len(distance_one),
        "distance_two": len(distance_two),
        "unresolved_after_two": len(unresolved),
    }


def check_order_ten_witness(graph_path: Path) -> None:
    graph = load_graph(graph_path)
    flow = ORDER_TEN_RESISTANT_FLOW
    assert is_flow(graph, flow)
    assert not good_lines(graph, flow)
    cycles = binary_cycles(graph)
    circuits = elementary_circuits(graph, cycles)
    assert all(
        not good_lines(graph, neighbour)
        for neighbour in switch_neighbours(graph, flow, circuits)
    )
    first_value, first_mask = ORDER_TEN_FIRST_SWITCH
    second_value, second_mask = ORDER_TEN_SECOND_SWITCH
    assert first_mask in circuits and second_mask in circuits
    intermediate = switch_flow(graph, flow, first_value, first_mask)
    assert not good_lines(graph, intermediate)
    repaired = switch_flow(graph, intermediate, second_value, second_mask)
    assert (1, 4, 5) in good_lines(graph, repaired)


def check_k4_surjective_circuit_pattern(graph_path: Path) -> None:
    graph = load_graph(graph_path)
    flow = K4_SURJECTIVE_CIRCUIT_FLOW
    line = K4_SURJECTIVE_CIRCUIT_LINE
    assert graph.vertices == 4 and graph.edge_count == 6
    assert is_flow(graph, flow)
    assert line_component_count(graph, flow, line) == 2

    join_mask = line_edge_mask(flow, line)
    all_edges = (1 << graph.edge_count) - 1
    complement = all_edges ^ join_mask
    outside = frozenset(range(1, 8)) - frozenset(line)
    assert frozenset(
        flow[edge]
        for edge in range(graph.edge_count)
        if (complement >> edge) & 1
    ) == outside
    assert all(
        complement & line_edge_mask(flow, (switch_value,))
        for switch_value in outside
    )

    circuits = elementary_circuits(graph)
    assert any(
        not (circuit & line_edge_mask(flow, (switch_value,)))
        and line_component_count(
            graph,
            switch_flow(graph, flow, switch_value, circuit),
            line,
        )
        == 1
        for switch_value in outside
        for circuit in circuits
    )


def analyze_canonical_directory(root: Path) -> dict[str, object]:
    rows = []
    for path in sorted(root.glob("*/graph.json")):
        graph = load_graph(path)
        if not is_bridgeless(graph):
            rows.append({"graph": path.parent.name, "bridgeless": False})
            continue
        row: dict[str, object] = {
            "graph": path.parent.name,
            "bridgeless": True,
        }
        row.update(analyze_graph(graph))
        rows.append(row)

    bridgeless_rows = [row for row in rows if row["bridgeless"]]
    totals = {
        key: sum(int(row[key]) for row in bridgeless_rows)
        for key in (
            "nowhere_zero_flows",
            "already_good",
            "connected_kernel_flows",
            "disconnected_line_pairs",
            "one_switch_stable_disconnected_pairs",
            "distance_one",
            "distance_two",
            "unresolved_after_two",
        )
    }
    return {
        "generated_graphs": len(rows),
        "bridgeless_graphs": len(bridgeless_rows),
        "totals": totals,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--canonical-root",
        type=Path,
        help="optional directory containing canonical */graph.json fixtures",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    check_quotient_geometry()
    check_fixed_examples()
    result: dict[str, object] = {
        "classification": "PARTIAL STRUCTURAL PROGRESS / COMPUTATIONAL EVIDENCE",
        "quotient_geometry": "PASS",
        "fixed_examples": "PASS",
    }
    if args.canonical_root is not None:
        result["canonical_census"] = analyze_canonical_directory(args.canonical_root)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
