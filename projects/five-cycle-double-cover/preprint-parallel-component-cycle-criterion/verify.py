#!/usr/bin/env python3
"""Independent audit of the parallel six-point component criterion.

The script uses only the Python standard library.  It generates every
GL(3,2)-orbit of nowhere-zero F_2^3-flows on a fixed rigid 12-vertex
cubic graph, then compares two separately implemented decisions for
each of its 21 parallel flags:

1. the original vertex-potential affine system; and
2. the component/cycle defect-in-span criterion.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


DEFAULT_GRAPH6 = "K??FEaKR@oE_"
W = tuple(range(8))


def dot(left: int, right: int) -> int:
    return (left & right).bit_count() & 1


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not record or ord(record[0]) - 63 >= 63:
        raise ValueError("only short graph6 records are supported")
    order = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return order, tuple(edges)


def incidence_rows(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    incidence = tuple(
        tuple(index for index, ends in enumerate(edges) if vertex in ends)
        for vertex in range(order)
    )
    if not all(len(row) == 3 for row in incidence):
        raise ValueError("the graph is not cubic")
    return incidence


def is_connected(
    order: int, edges: tuple[tuple[int, int], ...], deleted: int | None = None
) -> bool:
    adjacency = [[] for _ in range(order)]
    for index, (left, right) in enumerate(edges):
        if index == deleted:
            continue
        adjacency[left].append(right)
        adjacency[right].append(left)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            if other not in reached:
                reached.add(other)
                stack.append(other)
    return len(reached) == order


def cycle_space(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Generate the binary cycle space from independently found cycles."""

    tree_edges: set[int] = set()
    parent = [-1] * order
    parent_edge = [-1] * order
    stack = [0]
    parent[0] = 0
    while stack:
        vertex = stack.pop()
        for edge in incidence[vertex]:
            left, right = edges[edge]
            other = right if left == vertex else left
            if parent[other] >= 0:
                continue
            parent[other] = vertex
            parent_edge[other] = edge
            tree_edges.add(edge)
            stack.append(other)
    assert len(tree_edges) == order - 1

    tree_adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree_edges:
        left, right = edges[edge]
        tree_adjacency[left].append((right, edge))
        tree_adjacency[right].append((left, edge))

    basis: list[int] = []
    for chord, (start, finish) in enumerate(edges):
        if chord in tree_edges:
            continue
        previous = {start: (-1, -1)}
        queue = [start]
        for vertex in queue:
            if vertex == finish:
                break
            for other, edge in tree_adjacency[vertex]:
                if other not in previous:
                    previous[other] = (vertex, edge)
                    queue.append(other)
        mask = 1 << chord
        vertex = finish
        while vertex != start:
            vertex, edge = previous[vertex]
            mask ^= 1 << edge
        basis.append(mask)

    vectors = {0}
    for basis_mask in basis:
        vectors |= {mask ^ basis_mask for mask in tuple(vectors)}
    answer = tuple(sorted(vectors))
    assert len(answer) == 1 << (len(edges) - order + 1)
    for mask in answer:
        assert all(
            sum((mask >> edge) & 1 for edge in row) % 2 == 0
            for row in incidence
        )
    return answer


def vector_subspaces(cycles: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Enumerate the 2- and 3-subspaces of the cycle space."""

    nonzero = cycles[1:]
    subspaces: set[tuple[int, ...]] = set()
    for first, second in itertools.combinations(nonzero, 2):
        subspaces.add(tuple(sorted((0, first, second, first ^ second))))
    for first, second, third in itertools.combinations(nonzero, 3):
        if third in (first ^ second,):
            continue
        subspaces.add(
            tuple(
                sorted(
                    (
                        0,
                        first,
                        second,
                        third,
                        first ^ second,
                        first ^ third,
                        second ^ third,
                        first ^ second ^ third,
                    )
                )
            )
        )
    return tuple(sorted(subspaces, key=lambda row: (len(row), row)))


def subspace_basis(subspace: tuple[int, ...]) -> tuple[int, ...]:
    basis: list[int] = []
    span = {0}
    for vector in subspace[1:]:
        if vector in span:
            continue
        basis.append(vector)
        span |= {value ^ vector for value in tuple(span)}
    assert len(span) == len(subspace)
    return tuple(basis)


def nowhere_zero_flow_orbits(
    edge_count: int, cycles: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    flows = []
    for subspace in vector_subspaces(cycles):
        basis = subspace_basis(subspace)
        flow = tuple(
            sum(((mask >> edge) & 1) << bit for bit, mask in enumerate(basis))
            for edge in range(edge_count)
        )
        if all(flow):
            flows.append(flow)
    return tuple(flows)


def planes() -> tuple[frozenset[int], ...]:
    result = {
        frozenset((0, first, second, first ^ second))
        for first in range(1, 8)
        for second in range(first + 1, 8)
        if first != second
    }
    return tuple(sorted(result, key=lambda plane: tuple(sorted(plane))))


PLANES = planes()
PARALLEL_FLAGS = tuple(
    (plane, direction)
    for plane in PLANES
    for direction in sorted(plane - {0})
)
assert len(PARALLEL_FLAGS) == 21


def consistent(rows: list[tuple[int, int]]) -> bool:
    basis: dict[int, tuple[int, int]] = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs)
                break
            other_mask, other_rhs = basis[pivot]
            mask ^= other_mask
            rhs ^= other_rhs
        if not mask and rhs:
            return False
    return True


def affine_hull_rows(
    vertex: int, allowed: tuple[int, ...]
) -> list[tuple[int, int]]:
    base = allowed[0]
    answer = []
    for functional in range(1, 8):
        values = {dot(functional, point) for point in allowed}
        if len(values) == 1:
            variable_mask = sum(
                1 << (3 * vertex + bit)
                for bit in range(3)
                if functional & (1 << bit)
            )
            answer.append((variable_mask, dot(functional, base)))
    return answer


def full_affine_decision(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    plane: frozenset[int],
    direction: int,
) -> bool:
    """Literal potential-system decision, without the component formula."""

    omitted = frozenset((0, direction))
    a = min(plane - omitted)
    missing = frozenset((a, a ^ direction))
    rows: list[tuple[int, int]] = []
    for vertex, incident in enumerate(incidence):
        local_plane = frozenset((0, *(flow[edge] for edge in incident)))
        allowed = []
        for potential in W:
            triangle = {
                potential ^ point
                for point in local_plane
                if point != 0
            }
            if triangle & omitted:
                continue
            if missing <= triangle:
                continue
            allowed.append(potential)
        assert allowed
        local_rows = affine_hull_rows(vertex, tuple(allowed))
        # The scalar rows must describe the literal allowed set exactly,
        # not merely be valid on it.
        for potential in W:
            assignment = sum(
                ((potential >> bit) & 1) << (3 * vertex + bit)
                for bit in range(3)
            )
            recovered = all(
                ((mask & assignment).bit_count() & 1) == rhs
                for mask, rhs in local_rows
            )
            assert recovered == (potential in allowed)
        rows.extend(local_rows)

    for edge, (left, right) in enumerate(edges):
        value = flow[edge]
        other_left = next(
            flow[candidate]
            for candidate in incidence[left]
            if candidate != edge
        )
        other_right = next(
            flow[candidate]
            for candidate in incidence[right]
            if candidate != edge
        )
        constant = other_left ^ other_right
        for functional in range(1, 8):
            if dot(functional, value):
                continue
            mask = 0
            for vertex in (left, right):
                for bit in range(3):
                    if functional & (1 << bit):
                        mask ^= 1 << (3 * vertex + bit)
            rows.append((mask, dot(functional, constant)))
    return consistent(rows)


def edge_components(
    order: int,
    edges: tuple[tuple[int, int], ...],
    selected_edges: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for edge in selected_edges:
        left, right = edges[edge]
        adjacency[left].append(right)
        adjacency[right].append(left)
    reached: set[int] = set()
    answer = []
    active = {vertex for edge in selected_edges for vertex in edges[edge]}
    for start in sorted(active):
        if start in reached:
            continue
        component = {start}
        stack = [start]
        reached.add(start)
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in reached:
                    reached.add(other)
                    component.add(other)
                    stack.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def component_span_decision(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incidence: tuple[tuple[int, ...], ...],
    flow: tuple[int, ...],
    plane: frozenset[int],
    direction: int,
) -> bool:
    """Decide beta_H in span{gamma_C^d} on E_H components."""

    h_edges = tuple(edge for edge, value in enumerate(flow) if value in plane)
    f_edges = tuple(edge for edge, value in enumerate(flow) if value not in plane)
    h_degree = [
        sum(edge in h_edges for edge in incident) for incident in incidence
    ]
    assert all(degree in (1, 3) for degree in h_degree)
    leaves = {vertex for vertex, degree in enumerate(h_degree) if degree == 1}
    assert all(
        sum(edge in f_edges for edge in incidence[vertex])
        == (2 if vertex in leaves else 0)
        for vertex in range(order)
    )

    h_components = edge_components(order, edges, h_edges)
    f_cycles = edge_components(order, edges, f_edges)
    assert set().union(*(set(component) for component in h_components)) == set(
        range(order)
    )
    assert set().union(
        *(set(component) for component in f_cycles), set()
    ) == leaves

    component_index = {
        vertex: index
        for index, component in enumerate(h_components)
        for vertex in component
    }
    cycle_index = {
        vertex: index
        for index, component in enumerate(f_cycles)
        for vertex in component
    }
    leaf_value = {}
    for vertex in leaves:
        edge = next(edge for edge in incidence[vertex] if edge in h_edges)
        leaf_value[vertex] = flow[edge]

    outside = tuple(sorted(set(W) - set(plane)))
    a = min(plane - {0, direction})
    b = outside[0]
    w = b ^ a
    beta = [0] * len(h_components)
    for edge in f_edges:
        if flow[edge] != w:
            continue
        left, right = edges[edge]
        if component_index[left] != component_index[right]:
            beta[component_index[left]] ^= 1
            beta[component_index[right]] ^= 1

    # Cut conservation makes the displayed defect independent of w outside H.
    for alternate in outside:
        check = [0] * len(h_components)
        for edge in f_edges:
            if flow[edge] != alternate:
                continue
            left, right = edges[edge]
            if component_index[left] != component_index[right]:
                check[component_index[left]] ^= 1
                check[component_index[right]] ^= 1
        assert check == beta

    row_masks = [0] * len(h_components)
    for vertex in leaves:
        if leaf_value[vertex] != direction:
            row_masks[component_index[vertex]] ^= 1 << cycle_index[vertex]

    # Equivalent boundary-vector form, checked literally for every cycle:
    # gamma_C^d = delta_C^w + delta_C^(w+d).
    beta_from_cycles = 0
    beta_mask = sum(value << index for index, value in enumerate(beta))
    for cycle, cycle_vertices in enumerate(f_cycles):
        cycle_set = set(cycle_vertices)
        gamma_mask = 0
        for vertex in cycle_vertices:
            if leaf_value[vertex] != direction:
                gamma_mask ^= 1 << component_index[vertex]
        delta_pair_mask = 0
        delta_w_mask = 0
        for edge in f_edges:
            left, right = edges[edge]
            if left not in cycle_set:
                continue
            assert right in cycle_set
            if flow[edge] in (w, w ^ direction):
                delta_pair_mask ^= 1 << component_index[left]
                delta_pair_mask ^= 1 << component_index[right]
            if flow[edge] == w:
                delta_w_mask ^= 1 << component_index[left]
                delta_w_mask ^= 1 << component_index[right]
        assert gamma_mask == delta_pair_mask

        # Literal whole-circuit flow switch: add d on every edge of C.
        switched = list(flow)
        for edge in f_edges:
            left, right = edges[edge]
            if left in cycle_set:
                assert right in cycle_set
                switched[edge] ^= direction
        assert all(switched)
        assert all(
            switched[row[0]] ^ switched[row[1]] ^ switched[row[2]] == 0
            for row in incidence
        )
        assert tuple(value in plane for value in switched) == tuple(
            value in plane for value in flow
        )
        switched_beta_mask = 0
        for edge in f_edges:
            if switched[edge] != w:
                continue
            left, right = edges[edge]
            if component_index[left] != component_index[right]:
                switched_beta_mask ^= 1 << component_index[left]
                switched_beta_mask ^= 1 << component_index[right]
        assert switched_beta_mask == (beta_mask ^ gamma_mask)

        beta_from_cycles ^= delta_w_mask
        assert gamma_mask == sum(
            ((row_masks[component] >> cycle) & 1) << component
            for component in range(len(h_components))
        )
    assert beta_from_cycles == beta_mask
    return consistent(list(zip(row_masks, beta)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", default=DEFAULT_GRAPH6)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    started = time.monotonic()
    order, edges = parse_graph6(arguments.graph6)
    incidence = incidence_rows(order, edges)
    assert is_connected(order, edges)
    assert all(is_connected(order, edges, edge) for edge in range(len(edges)))
    cycles = cycle_space(order, edges, incidence)
    flows = nowhere_zero_flow_orbits(len(edges), cycles)
    disagreements = []
    sat = 0
    for flow_index, flow in enumerate(flows):
        assert all(
            flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
            for row in incidence
        )
        for plane, direction in PARALLEL_FLAGS:
            full = full_affine_decision(
                order, edges, incidence, flow, plane, direction
            )
            reduced = component_span_decision(
                order, edges, incidence, flow, plane, direction
            )
            sat += full
            if full != reduced:
                disagreements.append(
                    {
                        "flow_index": flow_index,
                        "flow": list(flow),
                        "plane": sorted(plane),
                        "direction": direction,
                        "full_affine": full,
                        "component_span": reduced,
                    }
                )
    result = {
        "schema": "six-point-parallel-component-criterion-audit-v1",
        "status": "PASS" if not disagreements else "FAIL",
        "graph6": arguments.graph6,
        "vertices": order,
        "edges": len(edges),
        "cycle_space_dimension": len(edges) - order + 1,
        "flow_gl_orbits": len(flows),
        "parallel_flags_per_flow": len(PARALLEL_FLAGS),
        "systems_checked": len(flows) * len(PARALLEL_FLAGS),
        "soluble_systems": sat,
        "disagreements": disagreements,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "scope": (
            "Independent finite audit of a general theorem; it is not "
            "a FiveCDC resolution."
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is not None:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if disagreements:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
