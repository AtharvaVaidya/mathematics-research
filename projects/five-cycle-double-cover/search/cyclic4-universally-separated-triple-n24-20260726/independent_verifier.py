#!/usr/bin/env python3
"""Clean-room verifier for the order-24 separated-triple witness.

This standard-library checker does not import the search program or the
four-sum generator.  It decodes the literal graph6 row, checks the graph
directly, enumerates every proper three-edge-colouring modulo global colour
permutation, and enumerates all edge deletions of size at most three to
verify cyclic 4-edge-connectivity.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


GRAPH6 = "W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E"
MARK_ENDPOINTS = ((0, 1), (2, 3), (20, 23))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(row: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    require(row and not row.startswith((":", ">>")), "unsupported graph6 row")
    order = ord(row[0]) - 63
    require(0 <= order <= 62, "only short graph6 rows are supported")
    edges: list[tuple[int, int]] = []
    bit = 0
    for second in range(1, order):
        for first in range(second):
            byte_index = 1 + bit // 6
            require(byte_index < len(row), "truncated graph6 row")
            value = ord(row[byte_index]) - 63
            require(0 <= value <= 63, "invalid graph6 byte")
            if (value >> (5 - bit % 6)) & 1:
                edges.append((first, second))
            bit += 1
    expected_length = 1 + (order * (order - 1) // 2 + 5) // 6
    require(len(row) == expected_length, "noncanonical short graph6 length")
    return order, tuple(edges)


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    result: list[list[int]] = [[] for _ in range(order)]
    for edge_index, (first, second) in enumerate(edges):
        require(0 <= first < second < order, "edge endpoint out of range")
        result[first].append(edge_index)
        result[second].append(edge_index)
    return tuple(tuple(row) for row in result)


def component_data(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
    removed: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    component = [-1] * order
    component_count = 0
    for root in range(order):
        if component[root] != -1:
            continue
        component[root] = component_count
        stack = [root]
        while stack:
            vertex = stack.pop()
            for edge_index in incident[vertex]:
                if edge_index in removed:
                    continue
                first, second = edges[edge_index]
                other = first ^ second ^ vertex
                if component[other] == -1:
                    component[other] = component_count
                    stack.append(other)
        component_count += 1
    vertices = [0] * component_count
    internal_edges = [0] * component_count
    for vertex in range(order):
        vertices[component[vertex]] += 1
    for edge_index, (first, second) in enumerate(edges):
        if edge_index in removed:
            continue
        if component[first] == component[second]:
            internal_edges[component[first]] += 1
    return tuple(component), tuple(vertices), tuple(internal_edges)


def cyclic_cut(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
    removed: tuple[int, ...],
) -> bool:
    _, vertices, internal_edges = component_data(
        order, edges, incident, frozenset(removed)
    )
    if len(vertices) == 1:
        return False
    cyclic_components = sum(
        edge_count >= vertex_count
        for edge_count, vertex_count in zip(
            internal_edges, vertices, strict=True
        )
    )
    return cyclic_components >= 2


def verify_cyclic_connectivity(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    cuts_tested: dict[str, int] = {}
    for size in range(1, 4):
        tested = 0
        for removed in itertools.combinations(range(len(edges)), size):
            tested += 1
            require(
                not cyclic_cut(order, edges, incident, removed),
                f"cyclic edge cut below four: {removed}",
            )
        cuts_tested[str(size)] = tested
    cyclic_four_witness: tuple[int, ...] | None = None
    tested_four = 0
    for removed in itertools.combinations(range(len(edges)), 4):
        tested_four += 1
        if cyclic_cut(order, edges, incident, removed):
            cyclic_four_witness = removed
            break
    require(cyclic_four_witness is not None, "no cyclic four-edge cut found")
    return {
        "cuts_tested_below_four": cuts_tested,
        "four_edge_subsets_until_witness": tested_four,
        "cyclic_four_cut_edge_indices": list(cyclic_four_witness),
        "cyclic_four_cut_edges": [
            list(edges[index]) for index in cyclic_four_witness
        ],
    }


def connected(
    order: int,
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> bool:
    component, _, _ = component_data(
        order, edges, incident, frozenset()
    )
    return len(set(component)) == 1


def shortest_cycle_length(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> int:
    adjacency: list[list[int]] = [[] for _ in range(order)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    answer = order + 1
    for root in range(order):
        distance = [-1] * order
        parent = [-1] * order
        distance[root] = 0
        queue = [root]
        for vertex in queue:
            for other in adjacency[vertex]:
                if distance[other] == -1:
                    distance[other] = distance[vertex] + 1
                    parent[other] = vertex
                    queue.append(other)
                elif parent[vertex] != other:
                    answer = min(
                        answer,
                        distance[vertex] + distance[other] + 1,
                    )
    require(answer <= order, "graph has no circuit")
    return answer


def marked_subdivision_girth(
    order: int,
    edges: tuple[tuple[int, int], ...],
    mark_indices: tuple[int, ...],
) -> int:
    marks = set(mark_indices)
    subdivided: list[tuple[int, int]] = []
    next_vertex = order
    for edge_index, (first, second) in enumerate(edges):
        if edge_index not in marks:
            subdivided.append((first, second))
            continue
        subdivided.append((first, next_vertex))
        subdivided.append((second, next_vertex))
        next_vertex += 1
    return shortest_cycle_length(next_vertex, tuple(subdivided))


def enumerate_tait_colourings(
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    edge_count = len(edges)
    colours = [-1] * edge_count
    used = [0] * len(incident)

    def assign(edge_index: int, colour: int) -> bool:
        first, second = edges[edge_index]
        flag = 1 << colour
        if used[first] & flag or used[second] & flag:
            return False
        colours[edge_index] = colour
        used[first] |= flag
        used[second] |= flag
        return True

    def unassign(edge_index: int, colour: int) -> None:
        first, second = edges[edge_index]
        colours[edge_index] = -1
        used[first] &= ~(1 << colour)
        used[second] &= ~(1 << colour)

    colourings: list[tuple[int, ...]] = []

    def recurse(assigned: int) -> None:
        if assigned == edge_count:
            require(
                all(mask == 0b111 for mask in used),
                "complete colouring misses a vertex colour",
            )
            colourings.append(tuple(colours))
            return
        best_edge = -1
        best_allowed = 0
        best_count = 4
        for edge_index, colour in enumerate(colours):
            if colour != -1:
                continue
            first, second = edges[edge_index]
            allowed = 0b111 & ~(used[first] | used[second])
            count = allowed.bit_count()
            if count == 0:
                return
            if count < best_count:
                best_edge = edge_index
                best_allowed = allowed
                best_count = count
                if count == 1:
                    break
        require(best_edge >= 0, "failed to choose an uncoloured edge")
        for colour in range(3):
            if best_allowed & (1 << colour):
                require(assign(best_edge, colour), "inconsistent assignment")
                recurse(assigned + 1)
                unassign(best_edge, colour)

    require(len(incident[0]) == 3, "normalization vertex is not cubic")
    assigned = 0
    for colour, edge_index in enumerate(incident[0]):
        require(assign(edge_index, colour), "normalization failed")
        assigned += 1
    recurse(assigned)
    return tuple(colourings)


def bichromatic_components(
    colouring: tuple[int, ...],
    omitted_colour: int,
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> tuple[frozenset[int], ...]:
    seen: set[int] = set()
    result: list[frozenset[int]] = []
    for root in range(len(edges)):
        if colouring[root] == omitted_colour or root in seen:
            continue
        component: set[int] = {root}
        seen.add(root)
        stack = [root]
        while stack:
            edge_index = stack.pop()
            for vertex in edges[edge_index]:
                for other in incident[vertex]:
                    if (
                        colouring[other] != omitted_colour
                        and other not in seen
                    ):
                        seen.add(other)
                        component.add(other)
                        stack.append(other)
        result.append(frozenset(component))
    return tuple(result)


def verify_universal_separation(
    colourings: Iterable[tuple[int, ...]],
    mark_indices: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    incident: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    maximum_marks_on_component = 0
    component_profiles: dict[str, int] = {}
    for colouring in colourings:
        for omitted in range(3):
            profile = []
            for component in bichromatic_components(
                colouring, omitted, edges, incident
            ):
                count = sum(mark in component for mark in mark_indices)
                maximum_marks_on_component = max(
                    maximum_marks_on_component, count
                )
                profile.append(count)
            key = ",".join(map(str, sorted(profile, reverse=True)))
            component_profiles[key] = component_profiles.get(key, 0) + 1
    require(
        maximum_marks_on_component <= 1,
        "two marks share a bichromatic circuit",
    )
    return {
        "maximum_marks_on_one_bichromatic_component":
            maximum_marks_on_component,
        "bichromatic_mark_profile_counts": component_profiles,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    order, edges = decode_graph6(GRAPH6)
    require(len(edges) == 3 * order // 2, "wrong cubic edge count")
    require(len(set(edges)) == len(edges), "parallel edge in simple graph")
    incident = incidence(order, edges)
    require(all(len(row) == 3 for row in incident), "graph is not cubic")
    require(connected(order, edges, incident), "graph is disconnected")

    endpoint_to_index = {item: index for index, item in enumerate(edges)}
    require(
        all(mark in endpoint_to_index for mark in MARK_ENDPOINTS),
        "marked edge is absent",
    )
    mark_indices = tuple(endpoint_to_index[mark] for mark in MARK_ENDPOINTS)
    require(
        len(set(itertools.chain.from_iterable(MARK_ENDPOINTS))) == 6,
        "marks are not a matching",
    )

    cyclic = verify_cyclic_connectivity(order, edges, incident)
    colourings = enumerate_tait_colourings(edges, incident)
    require(colourings, "graph is not Tait-colourable")
    require(
        len(set(colourings)) == len(colourings),
        "duplicate normalized Tait colouring",
    )
    separation = verify_universal_separation(
        colourings, mark_indices, edges, incident
    )
    colouring_payload = "\n".join(
        "".join(map(str, colouring)) for colouring in colourings
    ).encode("ascii")

    report = {
        "status": "VERIFIED",
        "scope": (
            "order-24 simple connected cubic Tait-colourable graph with "
            "cyclic edge connectivity exactly four and a universally "
            "separated three-edge matching"
        ),
        "graph6": GRAPH6,
        "order": order,
        "edges": len(edges),
        "mark_edge_indices": list(mark_indices),
        "mark_edges": [list(item) for item in MARK_ENDPOINTS],
        "girth": shortest_cycle_length(order, edges),
        "marked_subdivision_girth": marked_subdivision_girth(
            order, edges, mark_indices
        ),
        "satisfies_every_circuit_length_plus_marks_at_least_10":
            marked_subdivision_girth(order, edges, mark_indices) >= 10,
        "tait_colourings_mod_global_s3": len(colourings),
        "normalized_tait_colourings_sha256": hashlib.sha256(
            colouring_payload
        ).hexdigest(),
        **cyclic,
        **separation,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
