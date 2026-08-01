#!/usr/bin/env python3
"""Finite transcription audit for the canonical Fano cut certificates.

The input is the retained ten-vertex all-value-class-bad flow.  The human
proof in docs/fano-canonical-join-cut-certificates.md is independent of
this enumeration.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTANCE = (
    ROOT / "search" / "fano-value-class-flow-countermodel-20260726"
    / "instance.json"
)


def dot(functional: int, value: int) -> int:
    return (functional & value).bit_count() & 1


def boundary(edges: list[tuple[int, int]], mask: int, order: int) -> int:
    result = 0
    for edge_id, (u, v) in enumerate(edges):
        if (mask >> edge_id) & 1:
            result ^= 1 << u
            result ^= 1 << v
    return result & ((1 << order) - 1)


def components(
    order: int, edges: list[tuple[int, int]], selected: set[int]
) -> list[set[int]]:
    adjacency = [[] for _ in range(order)]
    for edge_id in selected:
        u, v = edges[edge_id]
        adjacency[u].append(v)
        adjacency[v].append(u)

    unseen = set(range(order))
    output: list[set[int]] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    queue.append(v)
        output.append(component)
    return output


def cut_edges(
    edges: list[tuple[int, int]], shore: set[int]
) -> set[int]:
    return {
        edge_id
        for edge_id, (u, v) in enumerate(edges)
        if (u in shore) != (v in shore)
    }


def connected_cycle(
    edges: list[tuple[int, int]], mask: int
) -> bool:
    selected = [
        edge_id
        for edge_id in range(len(edges))
        if (mask >> edge_id) & 1
    ]
    if not selected:
        return False
    adjacency: dict[int, list[int]] = {}
    for edge_id in selected:
        u, v = edges[edge_id]
        adjacency.setdefault(u, []).append(v)
        adjacency.setdefault(v, []).append(u)
    root = min(adjacency)
    seen = {root}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen == set(adjacency)


def packs_two_t_joins(
    edges: list[tuple[int, int]],
    order: int,
    matching: int,
) -> bool:
    edge_count = len(edges)
    allowed = ((1 << edge_count) - 1) ^ matching
    target = boundary(edges, matching, order)
    joins = [
        mask
        for mask in range(1 << edge_count)
        if mask & ~allowed == 0 and boundary(edges, mask, order) == target
    ]
    return any(first & second == 0 for first in joins for second in joins)


def main() -> int:
    data = json.loads(INSTANCE.read_text())
    edges = [tuple(edge) for edge in data["edges"]]
    values = data["flow_values_by_edge"]
    order = data["vertices"]
    edge_count = len(edges)

    for vertex in range(order):
        incident = [
            values[edge_id]
            for edge_id, edge in enumerate(edges)
            if vertex in edge
        ]
        assert len(incident) == 3
        assert incident[0] ^ incident[1] ^ incident[2] == 0
        assert len(set(incident)) == 3

    cycles = [
        mask
        for mask in range(1 << edge_count)
        if boundary(edges, mask, order) == 0
    ]
    connected_cycles = [
        mask for mask in cycles if connected_cycle(edges, mask)
    ]

    rainbow_counts: dict[int, int] = {}
    ordered_pair_checks = 0

    for functional in range(1, 8):
        line_edges = {
            edge_id
            for edge_id, value in enumerate(values)
            if dot(functional, value) == 0
        }
        affine_values = [
            value for value in range(1, 8) if dot(functional, value) == 1
        ]
        assert len(affine_values) == 4

        rainbow_components: list[set[int]] = []
        for component in components(order, edges, line_edges):
            cut = cut_edges(edges, component)
            parity = {
                value: sum(values[edge_id] == value for edge_id in cut) & 1
                for value in affine_values
            }
            assert len(set(parity.values())) == 1
            if next(iter(parity.values())) == 1:
                rainbow_components.append(component)
        assert len(rainbow_components) >= 2
        assert len(rainbow_components) % 2 == 0
        rainbow_counts[functional] = len(rainbow_components)

    for k in range(1, 8):
        lambdas = [functional for functional in range(1, 8) if dot(functional, k)]
        assert len(lambdas) == 4
        mk = {
            edge_id for edge_id, value in enumerate(values) if value == k
        }
        allowed_cycle_masks = [
            mask
            for mask in cycles
            if all(((mask >> edge_id) & 1) == 0 for edge_id in mk)
        ]

        for lam in lambdas:
            join_lam = {
                edge_id
                for edge_id, value in enumerate(values)
                if value != k and dot(lam, value)
            }
            for mu in lambdas:
                if mu == lam:
                    continue
                join_mu = {
                    edge_id
                    for edge_id, value in enumerate(values)
                    if value != k and dot(mu, value)
                }
                intersection = join_lam & join_mu
                intersection_values = {values[edge_id] for edge_id in intersection}
                assert len(intersection_values) == 1
                w = next(iter(intersection_values))
                assert intersection == {
                    edge_id
                    for edge_id, value in enumerate(values)
                    if value == w
                }

                # No binary cycle in G-M_k has trace M_w on J_mu.
                assert not any(
                    {
                        edge_id
                        for edge_id in join_mu
                        if (mask >> edge_id) & 1
                    }
                    == intersection
                    for mask in allowed_cycle_masks
                )

                # A rainbow component of F_mu is a literal odd cut witness.
                line_edges = {
                    edge_id
                    for edge_id, value in enumerate(values)
                    if dot(mu, value) == 0
                }
                found = False
                for component in components(order, edges, line_edges):
                    cut_in_k = cut_edges(edges, component) - mk
                    if cut_in_k <= join_mu and len(cut_in_k & intersection) % 2:
                        found = True
                        break
                assert found
                ordered_pair_checks += 1

    # The retained flow is bad for all seven value classes, but it is not
    # switch-local bad.  This direct subset audit finds a connected-circuit
    # repair and keeps that distinction explicit.
    for value in range(1, 8):
        matching = sum(
            1 << edge_id
            for edge_id, edge_value in enumerate(values)
            if edge_value == value
        )
        assert not packs_two_t_joins(edges, order, matching)

    connected_repair: tuple[int, int, tuple[int, ...]] | None = None
    for switch_value in range(1, 8):
        forbidden = sum(
            1 << edge_id
            for edge_id, edge_value in enumerate(values)
            if edge_value == switch_value
        )
        for cycle in connected_cycles:
            if cycle & forbidden:
                continue
            switched = [
                edge_value ^ switch_value
                if (cycle >> edge_id) & 1
                else edge_value
                for edge_id, edge_value in enumerate(values)
            ]
            assert all(switched)
            for vertex in range(order):
                incident = [
                    switched[edge_id]
                    for edge_id, edge in enumerate(edges)
                    if vertex in edge
                ]
                assert incident[0] ^ incident[1] ^ incident[2] == 0
            successful = tuple(
                value
                for value in range(1, 8)
                if packs_two_t_joins(
                    edges,
                    order,
                    sum(
                        1 << edge_id
                        for edge_id, edge_value in enumerate(switched)
                        if edge_value == value
                    ),
                )
            )
            if successful:
                connected_repair = (switch_value, cycle, successful)
                break
        if connected_repair is not None:
            break
    assert connected_repair is not None
    switch_value, repair_cycle, successful = connected_repair

    print("Fano canonical cut-certificate audit: PASS")
    print(f"binary_cycles={len(cycles)}")
    print(f"connected_circuits={len(connected_cycles)}")
    print(f"ordered_pair_checks={ordered_pair_checks}")
    print(
        "rainbow_component_counts="
        + ",".join(f"{key}:{rainbow_counts[key]}" for key in sorted(rainbow_counts))
    )
    print(
        "connected_repair="
        f"value:{switch_value},"
        "edges:"
        + ",".join(
            str(edge_id)
            for edge_id in range(edge_count)
            if (repair_cycle >> edge_id) & 1
        )
        + ",successful_values:"
        + ",".join(map(str, successful))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
