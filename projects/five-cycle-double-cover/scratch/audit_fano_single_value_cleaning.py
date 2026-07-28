#!/usr/bin/env python3
"""Exact fixed-line, single-value cleaning audit for F_2^3 flows.

For every nonzero functional mu and every nonzero t in ker(mu), this module
computes the rainbow vector r_mu and the image of

    tau_t : Z_1(G-M_t; F_2) -> F_2^{components(F_mu)}.

The implementation uses a cycle basis of the possibly disconnected graph
G-M_t and Gaussian elimination with source tracking.  A positive row
therefore includes an explicit binary-cycle preimage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.fixed_fano_cover_merge_audit import (  # noqa: E402
    direct_potential_merge_audit,
    graph_incidence,
)
from tools.flow_switch_audit import Graph, connected_components, is_flow  # noqa: E402


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def kernel_line(mu: int) -> tuple[int, int, int]:
    line = tuple(value for value in range(1, 8) if dot(mu, value) == 0)
    if len(line) != 3:
        raise AssertionError("nonzero functional has malformed kernel")
    return line


def cut_mask(graph: Graph, shore: frozenset[int]) -> int:
    return sum(
        1 << edge
        for edge, (left, right) in enumerate(graph.edges)
        if (left in shore) != (right in shore)
    )


def subgraph_cycle_basis(
    graph: Graph, allowed_edges: Iterable[int]
) -> tuple[int, ...]:
    allowed = tuple(sorted(allowed_edges))
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(graph.vertices)
    ]
    for edge in allowed:
        left, right = graph.edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    for row in adjacency:
        row.sort()

    seen: set[int] = set()
    basis: list[int] = []
    for root in range(graph.vertices):
        if root in seen:
            continue
        seen.add(root)
        parent = {root: root}
        parent_edge = {root: -1}
        depth = {root: 0}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other, edge in adjacency[vertex]:
                if other in seen:
                    continue
                seen.add(other)
                parent[other] = vertex
                parent_edge[other] = edge
                depth[other] = depth[vertex] + 1
                stack.append(other)
        component = frozenset(parent)
        tree_edges = frozenset(
            edge for edge in parent_edge.values() if edge >= 0
        )
        for edge in allowed:
            left, right = graph.edges[edge]
            if left not in component or edge in tree_edges:
                continue
            cycle = 1 << edge
            first, second = left, right
            while depth[first] > depth[second]:
                cycle ^= 1 << parent_edge[first]
                first = parent[first]
            while depth[second] > depth[first]:
                cycle ^= 1 << parent_edge[second]
                second = parent[second]
            while first != second:
                cycle ^= 1 << parent_edge[first]
                first = parent[first]
                cycle ^= 1 << parent_edge[second]
                second = parent[second]
            basis.append(cycle)
    return tuple(basis)


def defect_mask(
    graph: Graph,
    flow: tuple[int, ...],
    mu: int,
    components: tuple[frozenset[int], ...],
) -> int:
    affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
    base = min(affine)
    result = 0
    for index, component in enumerate(components):
        boundary = cut_mask(graph, component)
        parities = {
            sum(
                flow[edge] == value
                for edge in range(graph.edge_count)
                if (boundary >> edge) & 1
            )
            & 1
            for value in affine
        }
        if len(parities) != 1:
            raise AssertionError("affine boundary parities disagree")
        if next(iter(parities)):
            result |= 1 << index
        # The selected base gives the same bit by the preceding check.
        if bool((result >> index) & 1) != bool(
            sum(
                flow[edge] == base
                for edge in range(graph.edge_count)
                if (boundary >> edge) & 1
            )
            & 1
        ):
            raise AssertionError("defect base-color mismatch")
    return result


def tau_image(
    graph: Graph,
    flow: tuple[int, ...],
    mu: int,
    switch_value: int,
    components: tuple[frozenset[int], ...],
    cycle: int,
) -> int:
    affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
    base = min(affine)
    pair = frozenset((base, base ^ switch_value))
    result = 0
    for index, component in enumerate(components):
        boundary = cut_mask(graph, component)
        parity = sum(
            1
            for edge in range(graph.edge_count)
            if (cycle >> edge) & 1
            and (boundary >> edge) & 1
            and flow[edge] in pair
        ) & 1
        result |= parity << index
    return result


def solve_image(
    target: int,
    image_source_rows: Iterable[tuple[int, int]],
) -> tuple[bool, int, int]:
    """Return membership, source XOR, and image rank."""

    pivots: dict[int, tuple[int, int]] = {}
    for original_image, original_source in image_source_rows:
        image, source = original_image, original_source
        while image:
            pivot = image.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (image, source)
                break
            old_image, old_source = pivots[pivot]
            image ^= old_image
            source ^= old_source
    source = 0
    remainder = target
    while remainder:
        pivot = remainder.bit_length() - 1
        if pivot not in pivots:
            return False, 0, len(pivots)
        image, pivot_source = pivots[pivot]
        remainder ^= image
        source ^= pivot_source
    return True, source, len(pivots)


def independent_basis(vectors: Iterable[int]) -> tuple[int, ...]:
    pivots: dict[int, int] = {}
    for original in vectors:
        vector = original
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def separating_dual(
    target: int, generators: Iterable[int], dimension: int
) -> int | None:
    rows = tuple(generators)
    for functional in range(1, 1 << dimension):
        if (functional & target).bit_count() & 1 and all(
            (functional & row).bit_count() % 2 == 0 for row in rows
        ):
            return functional
    return None


def cleaning_pair_exists_fast(
    graph: Graph, flow: tuple[int, ...]
) -> bool:
    """Decision-only variant, stopping at the first successful pair."""

    if not is_flow(graph, flow):
        raise ValueError("input is not a nowhere-zero F_2^3-flow")
    cycle_bases: dict[int, tuple[int, ...]] = {}
    for mu in range(1, 8):
        line = kernel_line(mu)
        factor_edges = tuple(
            edge for edge, value in enumerate(flow) if value in line
        )
        components = connected_components(graph, factor_edges)
        owner = [0] * graph.vertices
        for index, component in enumerate(components):
            for vertex in component:
                owner[vertex] = index
        affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
        base = min(affine)
        defect = 0
        for edge, (left, right) in enumerate(graph.edges):
            first, second = owner[left], owner[right]
            if first != second and flow[edge] == base:
                defect ^= (1 << first) ^ (1 << second)
        if defect == 0:
            return True
        for switch_value in line:
            if switch_value not in cycle_bases:
                cycle_bases[switch_value] = subgraph_cycle_basis(
                    graph,
                    (
                        edge
                        for edge, value in enumerate(flow)
                        if value != switch_value
                    ),
                )
            pair = frozenset((base, base ^ switch_value))
            image_source_rows = []
            for cycle in cycle_bases[switch_value]:
                image = 0
                remaining = cycle
                while remaining:
                    bit = remaining & -remaining
                    edge = bit.bit_length() - 1
                    left, right = graph.edges[edge]
                    first, second = owner[left], owner[right]
                    if first != second and flow[edge] in pair:
                        image ^= (1 << first) ^ (1 << second)
                    remaining ^= bit
                image_source_rows.append((image, cycle))
            if solve_image(defect, image_source_rows)[0]:
                return True
    return False


def cleaning_rows(
    graph: Graph, flow: tuple[int, ...]
) -> tuple[dict[str, Any], ...]:
    if not is_flow(graph, flow):
        raise ValueError("input is not a nowhere-zero F_2^3-flow")
    cycle_bases = {
        switch_value: subgraph_cycle_basis(
            graph,
            (
                edge
                for edge, value in enumerate(flow)
                if value != switch_value
            ),
        )
        for switch_value in range(1, 8)
    }
    rows = []
    for mu in range(1, 8):
        line = kernel_line(mu)
        factor_edges = tuple(
            edge for edge, value in enumerate(flow) if value in line
        )
        components = connected_components(graph, factor_edges)
        owner = [0] * graph.vertices
        for index, component in enumerate(components):
            for vertex in component:
                owner[vertex] = index
        affine = tuple(value for value in range(1, 8) if dot(mu, value) == 1)
        base = min(affine)

        # Every crossing edge contributes to the boundary of its two factor
        # components.  This direct endpoint accumulation is equivalent to
        # constructing every cut mask separately, and is materially faster
        # in a complete flow census.
        defect = 0
        for edge, (left, right) in enumerate(graph.edges):
            first, second = owner[left], owner[right]
            if first != second and flow[edge] == base:
                defect ^= (1 << first) ^ (1 << second)

        # Conservation says all four affine colors have the same boundary
        # parity on each factor component.  Retain this semantic assertion.
        for alternate in affine[1:]:
            check = 0
            for edge, (left, right) in enumerate(graph.edges):
                first, second = owner[left], owner[right]
                if first != second and flow[edge] == alternate:
                    check ^= (1 << first) ^ (1 << second)
            if check != defect:
                raise AssertionError("affine boundary parities disagree")

        for switch_value in line:
            basis = cycle_bases[switch_value]
            pair = frozenset((base, base ^ switch_value))
            edge_images = [0] * graph.edge_count
            for edge, (left, right) in enumerate(graph.edges):
                first, second = owner[left], owner[right]
                if first != second and flow[edge] in pair:
                    edge_images[edge] = (1 << first) ^ (1 << second)
            image_rows = []
            for cycle in basis:
                image = 0
                remaining = cycle
                while remaining:
                    bit = remaining & -remaining
                    image ^= edge_images[bit.bit_length() - 1]
                    remaining ^= bit
                image_rows.append((image, cycle))
            cleanable, witness, rank = solve_image(defect, image_rows)
            image_basis = independent_basis(image for image, _ in image_rows)
            dual = (
                None
                if cleanable
                else separating_dual(defect, image_basis, len(components))
            )
            if not cleanable and dual is None:
                raise AssertionError("failed membership has no dual separator")
            if cleanable:
                if witness & sum(
                    1 << edge
                    for edge, value in enumerate(flow)
                    if value == switch_value
                ):
                    raise AssertionError("witness intersects M_t")
                if tau_image(
                    graph,
                    flow,
                    mu,
                    switch_value,
                    components,
                    witness,
                ) != defect:
                    raise AssertionError("reported preimage has wrong image")
            rows.append(
                {
                    "mu": mu,
                    "line": list(line),
                    "switch_value": switch_value,
                    "factor_components": len(components),
                    "rainbow_defect_mask": defect,
                    "cycle_basis_dimension_G_minus_M_t": len(basis),
                    "tau_image_rank": rank,
                    "tau_image_basis_masks": list(image_basis),
                    "separating_dual_mask": dual,
                    "r_mu_in_image_tau_t": cleanable,
                    "witness_binary_cycle_mask": witness if cleanable else None,
                    "witness_edge_ids": (
                        [
                            edge
                            for edge in range(graph.edge_count)
                            if (witness >> edge) & 1
                        ]
                        if cleanable
                        else None
                    ),
                }
            )
    return tuple(rows)


def load_flow(path: Path) -> tuple[Graph, tuple[int, ...]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    order = int(value.get("order", value.get("vertices")))
    edge_rows = value["edges"]
    edges = tuple(
        (
            int(row["u"]) if isinstance(row, dict) else int(row[0]),
            int(row["v"]) if isinstance(row, dict) else int(row[1]),
        )
        for row in edge_rows
    )
    flow = tuple(
        int(item)
        for item in value.get("flow_values_by_edge", value.get("flow"))
    )
    return Graph(order, edges), flow


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("construction", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-oum-potentials", action="store_true")
    arguments = parser.parse_args()
    graph, flow = load_flow(arguments.construction)
    rows = cleaning_rows(graph, flow)
    report: dict[str, Any] = {
        "schema": "fano-single-value-line-cleaning-audit-v1",
        "construction": str(arguments.construction),
        "vertices": graph.vertices,
        "edges": graph.edge_count,
        "flow_values_by_edge": list(flow),
        "functional_value_rows": list(rows),
        "cleaning_pair_exists": any(
            row["r_mu_in_image_tau_t"] for row in rows
        ),
    }
    if arguments.audit_oum_potentials:
        incidence = graph_incidence(graph.vertices, graph.edges)
        report["Oum_potential_audit"] = direct_potential_merge_audit(
            graph.vertices,
            graph.edges,
            incidence,
            flow,
            exhaustive=True,
            criterion="five-color",
        )
    if arguments.output:
        arguments.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps({
        "vertices": graph.vertices,
        "cleaning_pair_exists": report["cleaning_pair_exists"],
        "positive_pairs": sum(
            row["r_mu_in_image_tau_t"] for row in rows
        ),
        "Oum_five_color_merge_exists": (
            report.get("Oum_potential_audit", {}).get(
                "five_color_merge_exists"
            )
        ),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
