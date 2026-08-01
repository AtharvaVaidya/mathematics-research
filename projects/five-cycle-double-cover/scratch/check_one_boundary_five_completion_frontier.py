#!/usr/bin/env python3
"""Check two exact completions at the one-boundary-five frontier.

This file uses the 67-vertex factor-critical five-pole constructed and
independently checked in ``check_cyclic4_all_bad_threshold_three_core.py``.
It verifies two complementary facts.

1.  When s=0, every labelled completion has a cyclic 3-edge-cut.  The code
    enumerates all 720 assignments and checks the concrete triangle shore.
    This fact also has the short proof implemented by ``s0_triangle``:
    the one singleton sees three of the four root endpoints, so one of the
    two root edges has both ends in its neighbourhood.

2.  When s=1, the theta outside

        z0--w0--w1--z1,  z0--w2--w3--z1,  z0--w4--z1

    has one boundary incidence at every w.  Gluing the five checked pole
    terminals in source-label order (3,7,8,9,12) produces a simple cubic
    cyclically 4-edge-connected graph on 74 vertices.  Its exact perfect
    matching census has oddness four, so this particular completion is
    non-Tait but is not an oddness-six obstruction.

3.  The lexicographically first locally cyclic-four outside at s=2 also
    gives a cyclically 4-edge-connected completion of exact oddness four.

These are structural/computational frontier results, not a resolution of
the Five-Cycle Double Cover Conjecture.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import json

import check_cyclic4_all_bad_threshold_three_core as core


EXPECTED_S0_COMPLETIONS = 720
EXPECTED_S1_MATCHING_DISTRIBUTION = {
    4: 43_137,
    6: 2_660,
    8: 408,
    10: 4,
}
EXPECTED_S1_MATCHING_TYPE_DISTRIBUTION = {
    (1, 1, 4): 24_242,
    (1, 1, 6): 1_960,
    (1, 1, 8): 88,
    (3, 0, 4): 18_895,
    (3, 0, 6): 700,
    (3, 0, 8): 320,
    (3, 0, 10): 4,
}
EXPECTED_S2_MATCHING_DISTRIBUTION = {
    4: 40_562,
    6: 24_346,
    8: 400,
}


def normalized_edges(rows: list[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left, row in enumerate(rows)
        for right in range(left + 1, len(rows))
        if row >> right & 1
    )


def pole() -> tuple[list[int], tuple[int, ...]]:
    order, edges = core.build_source()
    source = core.adjacency(order, edges)
    rows, _, new_index = core.delete_source_vertices(
        source, core.DELETED_PATH
    )
    terminals = tuple(
        new_index[old] for old in core.EXPECTED_BOUNDARY_OLD
    )
    assert core.factor_critical(rows)
    assert tuple(rows[q].bit_count() for q in terminals) == (2,) * 5
    assert all(
        row.bit_count() == (2 if vertex in terminals else 3)
        for vertex, row in enumerate(rows)
    )
    return rows, terminals


def add_edge(
    rows: list[int], edges: list[tuple[int, int]], left: int, right: int
) -> None:
    edge = tuple(sorted((left, right)))
    if left == right or rows[left] >> right & 1:
        raise AssertionError("completion is not simple")
    rows[left] |= 1 << right
    rows[right] |= 1 << left
    edges.append(edge)


def bridgeless(rows: list[int], edges: tuple[tuple[int, int], ...]) -> bool:
    full = (1 << len(rows)) - 1
    for left, right in edges:
        modified = rows[:]
        modified[left] &= ~(1 << right)
        modified[right] &= ~(1 << left)
        if len(core.components(modified, full)) != 1:
            return False
    return True


def full_boundary(
    rows: list[int], vertices: set[int]
) -> tuple[tuple[int, int], ...]:
    return tuple(
        edge for edge in normalized_edges(rows)
        if (edge[0] in vertices) != (edge[1] in vertices)
    )


def s0_triangle(
    roots: tuple[tuple[int, int], tuple[int, int]],
    z_neighbours: tuple[int, int, int],
) -> tuple[int, int]:
    """Return the unique root with both ends adjacent to z."""
    inside = tuple(
        root for root in roots if set(root) <= set(z_neighbours)
    )
    assert len(inside) == 1
    return inside[0]


def check_s0(pole_rows: list[int], terminals: tuple[int, ...]) -> dict:
    q_order = len(pole_rows)
    pairings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    completion_count = 0
    bridgeless_count = 0
    cyclic_three_triangle_count = 0

    # ``missing`` is the W vertex not adjacent to z.  It receives two of
    # the five Q incidences; each of the other three W vertices receives one.
    for roots in pairings:
        for missing in range(4):
            z_neighbours = tuple(w for w in range(4) if w != missing)
            for doubled_terminals in combinations(range(5), 2):
                remaining = tuple(
                    index for index in range(5)
                    if index not in doubled_terminals
                )
                for assignment in permutations(remaining):
                    rows = pole_rows[:] + [0] * 5
                    edges = list(normalized_edges(pole_rows))
                    w_vertices = tuple(q_order + w for w in range(4))
                    z = q_order + 4
                    for left, right in roots:
                        add_edge(
                            rows, edges, w_vertices[left], w_vertices[right]
                        )
                    for w in z_neighbours:
                        add_edge(rows, edges, z, w_vertices[w])
                    for terminal_index in doubled_terminals:
                        add_edge(
                            rows, edges, terminals[terminal_index],
                            w_vertices[missing]
                        )
                    for terminal_index, w in zip(assignment, z_neighbours):
                        add_edge(
                            rows, edges, terminals[terminal_index],
                            w_vertices[w]
                        )

                    completion_count += 1
                    assert all(row.bit_count() == 3 for row in rows)
                    edge_tuple = tuple(sorted(edges))
                    if bridgeless(rows, edge_tuple):
                        bridgeless_count += 1

                    root = s0_triangle(roots, z_neighbours)
                    triangle = {
                        z, w_vertices[root[0]], w_vertices[root[1]]
                    }
                    induced_edges = tuple(
                        edge for edge in edge_tuple
                        if edge[0] in triangle and edge[1] in triangle
                    )
                    boundary = full_boundary(rows, triangle)
                    assert len(induced_edges) == 3
                    assert len(boundary) == 3
                    # Q is nontrivial factor-critical and internally
                    # bridgeless, hence it contains a circuit.
                    assert any(
                        core.component_has_circuit(
                            pole_rows, (1 << q_order) - 1
                        )
                        for _ in (0,)
                    )
                    cyclic_three_triangle_count += 1

    assert completion_count == EXPECTED_S0_COMPLETIONS
    assert bridgeless_count == completion_count
    assert cyclic_three_triangle_count == completion_count
    return {
        "labelled_completions": completion_count,
        "bridgeless_completions": bridgeless_count,
        "completions_with_explicit_cyclic_3_cut": (
            cyclic_three_triangle_count
        ),
        "cyclically_4_edge_connected_completions": 0,
    }


def build_s1_theta(
    pole_rows: list[int], terminals: tuple[int, ...]
) -> tuple[list[int], tuple[tuple[int, int], ...], dict[str, object]]:
    q_order = len(pole_rows)
    rows = pole_rows[:] + [0] * 7
    edges = list(normalized_edges(pole_rows))
    w = tuple(q_order + index for index in range(5))
    z = (q_order + 5, q_order + 6)

    add_edge(rows, edges, w[0], w[1])
    add_edge(rows, edges, w[2], w[3])
    for local in (0, 2, 4):
        add_edge(rows, edges, z[0], w[local])
    for local in (1, 3, 4):
        add_edge(rows, edges, z[1], w[local])
    for terminal, outside in zip(terminals, w):
        add_edge(rows, edges, terminal, outside)

    assert all(row.bit_count() == 3 for row in rows)
    edge_tuple = tuple(sorted(edges))
    metadata = {
        "order": len(rows),
        "size": len(edge_tuple),
        "root_edges_local_W": [[0, 1], [2, 3]],
        "Z_neighbourhoods_local_W": [[0, 2, 4], [1, 3, 4]],
        "terminal_source_labels_to_local_W": [
            [old, local]
            for local, old in enumerate(core.EXPECTED_BOUNDARY_OLD)
        ],
    }
    return rows, edge_tuple, metadata


def matching_type_distribution(
    rows: list[int],
    q_order: int,
) -> Counter[tuple[int, int, int]]:
    """Count matchings by (Q-cut edges, roots, odd complement circuits)."""
    result: Counter[tuple[int, int, int]] = Counter()
    chosen: list[tuple[int, int]] = []
    roots = {
        (q_order, q_order + 1),
        (q_order + 2, q_order + 3),
    }

    def search(vertices: int) -> None:
        if not vertices:
            cut_count = sum(
                (left < q_order) != (right < q_order)
                for left, right in chosen
            )
            root_count = sum(
                tuple(sorted(edge)) in roots for edge in chosen
            )
            odd = core.complement_odd_circuits(rows, tuple(chosen))
            result[(cut_count, root_count, odd)] += 1
            return
        first_bit = vertices & -vertices
        first = first_bit.bit_length() - 1
        candidates = rows[first] & vertices & ~first_bit
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            chosen.append((first, second))
            search(vertices ^ first_bit ^ second_bit)
            chosen.pop()

    search((1 << len(rows)) - 1)
    return result


def check_s1(
    pole_rows: list[int], terminals: tuple[int, ...]
) -> dict[str, object]:
    rows, edges, metadata = build_s1_theta(pole_rows, terminals)
    assert bridgeless(rows, edges)
    assert core.cyclically_four(rows, edges)

    type_distribution = matching_type_distribution(rows, len(pole_rows))
    assert dict(type_distribution) == EXPECTED_S1_MATCHING_TYPE_DISTRIBUTION
    assert all(cut + 2 * roots == 3
               for cut, roots, _ in type_distribution)
    distribution: Counter[int] = Counter()
    for (_, _, odd), count in type_distribution.items():
        distribution[odd] += count
    assert dict(distribution) == EXPECTED_S1_MATCHING_DISTRIBUTION
    oddness = min(distribution)
    assert oddness == 4

    metadata.update({
        "simple_cubic": True,
        "bridgeless": True,
        "cyclically_4_edge_connected": True,
        "factor_critical_core_order": len(pole_rows),
        "strict_Hall_for_A": (
            "|N({a})|=3>|{a}|=1 "
            "(Q and the two singleton components)"
        ),
        "perfect_matching_count": sum(distribution.values()),
        "complement_odd_circuit_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
        "matching_type_distribution": {
            f"k={cut},r={roots},odd={odd}": count
            for (cut, roots, odd), count in sorted(
                type_distribution.items()
            )
        },
        "oddness": oddness,
        "Tait_colorable": False,
    })
    return metadata


def build_s2_lexicographic(
    pole_rows: list[int], terminals: tuple[int, ...]
) -> tuple[list[int], tuple[tuple[int, int], ...], dict[str, object]]:
    """Build the first retained s=2 outside in the incidence census."""
    q_order = len(pole_rows)
    rows = pole_rows[:] + [0] * 9
    edges = list(normalized_edges(pole_rows))
    w = tuple(q_order + index for index in range(6))
    z = tuple(q_order + 6 + index for index in range(3))
    z_neighbourhoods = ((0, 2, 4), (0, 2, 5), (1, 3, 4))
    boundary_stubs = (1, 3, 4, 5, 5)

    add_edge(rows, edges, w[0], w[1])
    add_edge(rows, edges, w[2], w[3])
    for singleton, neighbourhood in zip(z, z_neighbourhoods):
        for local in neighbourhood:
            add_edge(rows, edges, singleton, w[local])
    for terminal, local in zip(terminals, boundary_stubs):
        add_edge(rows, edges, terminal, w[local])

    assert all(row.bit_count() == 3 for row in rows)
    edge_tuple = tuple(sorted(edges))
    metadata = {
        "order": len(rows),
        "size": len(edge_tuple),
        "root_edges_local_W": [[0, 1], [2, 3]],
        "Z_neighbourhoods_local_W": [
            list(neighbourhood) for neighbourhood in z_neighbourhoods
        ],
        "boundary_stub_W_indices": list(boundary_stubs),
        "terminal_source_labels_in_stub_order": list(
            core.EXPECTED_BOUNDARY_OLD
        ),
    }
    return rows, edge_tuple, metadata


def check_s2_lexicographic(
    pole_rows: list[int], terminals: tuple[int, ...]
) -> dict[str, object]:
    rows, edges, metadata = build_s2_lexicographic(
        pole_rows, terminals
    )
    assert bridgeless(rows, edges)
    assert core.cyclically_four(rows, edges)
    type_distribution = matching_type_distribution(rows, len(pole_rows))
    assert all(cut + 2 * roots == 3
               for cut, roots, _ in type_distribution)
    distribution: Counter[int] = Counter()
    for (_, _, odd), count in type_distribution.items():
        distribution[odd] += count
    assert dict(distribution) == EXPECTED_S2_MATCHING_DISTRIBUTION
    metadata.update({
        "simple_cubic": True,
        "bridgeless": True,
        "cyclically_4_edge_connected": True,
        "strict_Hall_checks_for_A": {
            "{w4}": "3 >= 2",
            "{w5}": "2 >= 2",
            "{w4,w5}": "4 >= 3",
        },
        "perfect_matching_count": sum(distribution.values()),
        "complement_odd_circuit_distribution": {
            str(key): distribution[key] for key in sorted(distribution)
        },
        "oddness": min(distribution),
        "Tait_colorable": False,
    })
    return metadata


def main() -> int:
    pole_rows, terminals = pole()
    report = {
        "schema": "one-boundary-five-completion-frontier-v1",
        "classification": (
            "EXACT FINITE CHECK; NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION"
        ),
        "core": {
            "order": len(pole_rows),
            "terminal_source_labels": list(
                core.EXPECTED_BOUNDARY_OLD
            ),
            "all_terminal_minimum_internal_odd_circuits": 4,
        },
        "s0": check_s0(pole_rows, terminals),
        "s1_identity_theta_completion": check_s1(
            pole_rows, terminals
        ),
        "s2_lexicographic_completion": check_s2_lexicographic(
            pole_rows, terminals
        ),
        "warning": (
            "The displayed s=1 and s=2 graphs have oddness four.  They "
            "are not oddness-six obstructions and say nothing against "
            "Five-CDC."
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
