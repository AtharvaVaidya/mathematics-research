#!/usr/bin/env python3
"""Independent finite audit of the Petersen adjacent-deletion four-pole.

The script checks the two possible relations between the deleted edge uv
and a perfect matching F, and then exhausts the direct four-block gluing
mechanism for nowhere-zero F_2^3-flows.
"""

from __future__ import annotations

import collections
import itertools
import json

import networkx as nx


GRAPH = nx.petersen_graph()
EDGES = tuple(sorted(tuple(sorted(edge)) for edge in GRAPH.edges()))
EDGE_ID = {edge: index for index, edge in enumerate(EDGES)}


def is_cycle(mask: int) -> bool:
    return all(
        sum(
            (mask >> EDGE_ID[tuple(sorted((vertex, neighbor)))]) & 1
            for neighbor in GRAPH[vertex]
        )
        % 2
        == 0
        for vertex in GRAPH
    )


CYCLES = tuple(mask for mask in range(1 << 15) if is_cycle(mask))
MATCHINGS = tuple(
    frozenset(choice)
    for choice in itertools.combinations(range(15), 5)
    if len({vertex for edge in choice for vertex in EDGES[edge]}) == 10
)
MATCHING_SET = set(MATCHINGS)


def component_defect(first: int, second: int, matching_edge: int) -> int:
    vertices = set(EDGES[matching_edge])
    cut = [
        edge
        for edge, (u, v) in enumerate(EDGES)
        if (u in vertices) != (v in vertices)
    ]
    return sum(
        ((first >> edge) & 1) & ((second >> edge) & 1)
        for edge in cut
    ) % 2


def ports(deleted_edge: int) -> tuple[int, ...]:
    u, v = EDGES[deleted_edge]
    return tuple(
        edge
        for edge, endpoints in enumerate(EDGES)
        if edge != deleted_edge
        and ((u in endpoints) != (v in endpoints))
    )


def boundary_word(mask: int, deleted_edge: int) -> tuple[int, ...]:
    return tuple((mask >> edge) & 1 for edge in ports(deleted_edge))


def local_inside_case() -> dict[str, int]:
    matching = MATCHINGS[0]
    deleted = min(matching)
    internal = matching - {deleted}
    valid = []
    for first in CYCLES:
        for second in CYCLES:
            if any(
                not (((first >> edge) & 1) or ((second >> edge) & 1))
                for edge in internal
            ):
                continue
            if any(
                component_defect(first, second, edge)
                for edge in internal
            ):
                continue
            valid.append((first, second))
    assert len(valid) == 48
    assert all(
        not (((first >> deleted) & 1) or ((second >> deleted) & 1))
        for first, second in valid
    )
    boundary_states = {
        (boundary_word(first, deleted), boundary_word(second, deleted))
        for first, second in valid
    }
    return {
        "ordered_cycle_pairs": len(valid),
        "boundary_states": len(boundary_states),
        "pairs_covering_deleted_matching_edge": 0,
    }


def local_outside_case() -> dict[str, int]:
    matching = MATCHINGS[0]
    deleted = min(set(range(15)) - matching)
    u, v = EDGES[deleted]
    boundary_matching = {
        edge
        for edge in matching
        if u in EDGES[edge] or v in EDGES[edge]
    }
    internal = matching - boundary_matching
    assert len(boundary_matching) == 2 and len(internal) == 3
    valid = []
    for first in CYCLES:
        for second in CYCLES:
            if any(
                not (((first >> edge) & 1) or ((second >> edge) & 1))
                for edge in matching
            ):
                continue
            if any(
                component_defect(first, second, edge)
                for edge in internal
            ):
                continue
            defects = tuple(
                component_defect(first, second, edge)
                for edge in sorted(boundary_matching)
            )
            valid.append((first, second, defects))
    assert len(valid) == 72
    assert all(defects == (1, 1) for _, _, defects in valid)
    boundary_states = {
        (boundary_word(first, deleted), boundary_word(second, deleted))
        for first, second, _ in valid
    }
    assert len(boundary_states) == 36
    return {
        "ordered_cycle_pairs": len(valid),
        "boundary_states": len(boundary_states),
        "boundary_matching_defects_11": len(valid),
    }


def direct_four_block_no_go() -> dict[str, int]:
    signatures = set()
    flow_count = 0
    all_edges = (1 << 15) - 1
    for first in CYCLES:
        for second in CYCLES:
            for third in CYCLES:
                if (first | second | third) != all_edges:
                    continue
                flow_count += 1
                values = tuple(
                    ((first >> edge) & 1)
                    | (((second >> edge) & 1) << 1)
                    | (((third >> edge) & 1) << 2)
                    for edge in range(15)
                )
                for deleted in range(15):
                    covered = []
                    for functional in range(1, 8):
                        factor = frozenset(
                            edge
                            for edge, value in enumerate(values)
                            if (functional & value).bit_count() % 2 == 0
                        )
                        if factor in MATCHING_SET and deleted in factor:
                            covered.append(functional)
                    if not covered:
                        continue
                    port_values = tuple(
                        sorted(values[edge] for edge in ports(deleted))
                    )
                    signatures.add((tuple(covered), port_values))
    assert flow_count == 28560
    assert len(signatures) == 70

    covering_combinations = 0
    parity_compatible = 0
    cross_block_compatible = 0
    rows = tuple(signatures)
    for choice in itertools.combinations_with_replacement(range(len(rows)), 4):
        selected = [rows[index] for index in choice]
        if set().union(*(set(row[0]) for row in selected)) != set(range(1, 8)):
            continue
        covering_combinations += 1
        counts = collections.Counter(
            value for row in selected for value in row[1]
        )
        if any(count % 2 for count in counts.values()):
            continue
        parity_compatible += 1
        # Every equal-value connector joins two distinct blocks.
        if any(
            sum(value in row[1] for row in selected) < 2
            for value in counts
        ):
            continue
        cross_block_compatible += 1
    assert cross_block_compatible == 0
    return {
        "nowhere_zero_labelled_flows": flow_count,
        "flow_deletion_signatures": len(signatures),
        "four_signature_combinations_covering_all_functionals":
            covering_combinations,
        "value_parity_compatible_combinations": parity_compatible,
        "direct_value_preserving_gluable_combinations":
            cross_block_compatible,
    }


def main() -> int:
    assert len(CYCLES) == 64
    assert len(MATCHINGS) == 6
    report = {
        "schema": "petersen-four-cut-local-no-go-v1",
        "cycles": len(CYCLES),
        "perfect_matchings": len(MATCHINGS),
        "deleted_edge_in_factor": local_inside_case(),
        "deleted_edge_outside_factor": local_outside_case(),
        "direct_four_block_gluing": direct_four_block_no_go(),
        "status": "PASS",
    }
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
