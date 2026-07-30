#!/usr/bin/env python3
"""Independent exact replay of an augmented radius-two counterexample.

This is a counterexample to an auxiliary Jaeger-star descent statement,
not to the Five-Cycle Double Cover Conjecture.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEMANTICS = (
    HERE.parent
    / "jaeger-lift13-girth10-augmented-trap-20260729"
    / "independent_verify.py"
)
SPEC = importlib.util.spec_from_file_location("semantics", SEMANTICS)
assert SPEC and SPEC.loader
semantics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(semantics)

GRAPH6 = (
    "ghe?GC@@G??@?@??_@I??A?C_?G??G@?CA?@?C?G_??_@?@???@?@??_?"
    "C?G??C@?O??C?A??G????G????C????@??O??G?????_????H????_@?????"
    "G_????@G??_?C@"
)
ROOT = 0
OMITTED_MASKS = (
    74750917167123596,
    60249003513889361,
    9115267394842914,
)
ESCAPE_PATH = ((10, 9), (40, 43), (15, 17))
SEED_PROFILE = (4, 6, 2, 6, 6, 6, 2)
SEED_PSI = (2, 60)
FIVECDC_LABELS = (
    20, 24, 9, 5, 3, 17, 24, 18, 10, 9,
    3, 5, 20, 5, 6, 12, 12, 6, 20, 17,
    18, 3, 9, 10, 10, 3, 10, 9, 10, 3,
    3, 9, 10, 17, 3, 10, 18, 9, 24, 24,
    17, 17, 9, 24, 10, 18, 9, 17, 24, 24,
    20, 9, 12, 3, 5, 12, 6, 24, 18, 10,
)


def components(
    order: int,
    edges: tuple[tuple[int, int], ...],
    deleted: frozenset[int],
) -> list[tuple[frozenset[int], int]]:
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(order)
    ]
    for edge, (left, right) in enumerate(edges):
        if edge in deleted:
            continue
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    seen: set[int] = set()
    answer = []
    for source in range(order):
        if source in seen:
            continue
        vertices = {source}
        component_edges: set[int] = set()
        seen.add(source)
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for other, edge in adjacency[vertex]:
                component_edges.add(edge)
                if other not in seen:
                    seen.add(other)
                    vertices.add(other)
                    queue.append(other)
        answer.append((frozenset(vertices), len(component_edges)))
    return answer


def structural_audit(
    order: int,
    edges: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    assert order == 40 and len(edges) == 60
    assert all(left != right for left, right in edges)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    degrees = [0] * order
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    assert set(degrees) == {3}

    disconnecting = {}
    for cut_size in range(4):
        count = 0
        cyclic = 0
        for deleted_tuple in combinations(range(len(edges)), cut_size):
            pieces = components(
                order, edges, frozenset(deleted_tuple)
            )
            if len(pieces) == 1:
                continue
            count += 1
            cyclic_pieces = sum(
                edge_count >= len(vertices)
                for vertices, edge_count in pieces
            )
            cyclic += cyclic_pieces >= 2
        disconnecting[cut_size] = count
        assert cyclic == 0
    assert disconnecting == {0: 0, 1: 0, 2: 0, 3: 40}
    girth = semantics.graph_girth(order, edges)
    assert girth == 5
    return {
        "order": order,
        "edges": len(edges),
        "simple_cubic": True,
        "disconnecting_cut_counts_through_three":
            disconnecting,
        "cyclic_three_edge_cuts": 0,
        "three_edge_connected": True,
        "cyclically_four_edge_connected": True,
        "girth": girth,
    }


def labels_from_masks(length: int) -> tuple[int, ...]:
    assert all(mask >> length == 0 for mask in OMITTED_MASKS)
    labels = []
    for local in range(length):
        present = [
            coordinate
            for coordinate, mask in enumerate(OMITTED_MASKS)
            if mask >> local & 1
        ]
        assert len(present) == 1
        labels.append(present[0])
    class_size = length // 3
    assert Counter(labels) == {
        0: class_size, 1: class_size, 2: class_size
    }
    return tuple(labels)


def main() -> None:
    order, edges = semantics.graph6(GRAPH6)
    structure = structural_audit(order, edges)
    spokes = tuple(
        edge for edge, endpoints in enumerate(edges)
        if ROOT in endpoints
    )
    internal = tuple(
        edge for edge, endpoints in enumerate(edges)
        if ROOT not in endpoints
    )
    assert spokes == (0, 3, 5)
    assert len(internal) == 57
    seed = labels_from_masks(len(internal))
    incidence = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)

    assert len(FIVECDC_LABELS) == len(edges)
    assert all(label.bit_count() == 2 for label in FIVECDC_LABELS)
    assert all(
        FIVECDC_LABELS[row[0]]
        ^ FIVECDC_LABELS[row[1]]
        ^ FIVECDC_LABELS[row[2]]
        == 0
        for row in incidence
    )
    fivecdc_sizes = tuple(
        sum(label >> coordinate & 1 for label in FIVECDC_LABELS)
        for coordinate in range(5)
    )
    assert fivecdc_sizes == (27, 25, 15, 30, 23)

    state_cache: dict[
        tuple[int, ...],
        tuple[
            tuple[int, ...],
            int,
            tuple[int, int],
            tuple[frozenset[int], ...],
        ]
        | None,
    ] = {}

    def theorem_316_defects(kernels):
        """Direct Hušek--Šámal component-parity defects.

        For every nonzero functional a and every value m with a(m)=1,
        count components of E\\F containing an odd number of vertices
        incident with an m-edge.
        """
        flow = tuple(
            sum(
                1 << coordinate
                for coordinate in range(3)
                if edge not in kernels[coordinate]
            )
            for edge in range(len(edges))
        )
        rows = []
        for functional in range(1, 8):
            zero = semantics.DSU(order)
            for edge, (left, right) in enumerate(edges):
                if not semantics.scalar(functional, flow[edge]):
                    zero.union(left, right)
            defects = []
            for matching_value in range(1, 8):
                if not semantics.scalar(functional, matching_value):
                    continue
                parity = {
                    zero.find(vertex): 0 for vertex in range(order)
                }
                for vertex in range(order):
                    if any(
                        flow[edge] == matching_value
                        for edge in incidence[vertex]
                    ):
                        parity[zero.find(vertex)] ^= 1
                defects.append(sum(parity.values()))
            assert len(defects) == 4
            rows.append(tuple(defects))
        return tuple(rows)

    def state_data(labels: tuple[int, ...]):
        if labels in state_cache:
            return state_cache[labels]
        trees = tuple(
            frozenset(
                [spokes[coordinate]]
                + [
                    internal[local]
                    for local, label in enumerate(labels)
                    if label != coordinate
                ]
            )
            for coordinate in range(3)
        )
        if not all(
            semantics.is_tree(order, edges, tree)
            for tree in trees
        ):
            state_cache[labels] = None
            return None
        kernels, profile, flags = semantics.evaluate(
            order, edges, trees
        )
        direct_defects = theorem_316_defects(kernels)
        assert all(
            len(set(row)) == 1 and row[0] == profile[index]
            for index, row in enumerate(direct_defects)
        )
        result = (
            tuple(profile),
            flags,
            (min(profile), sum(map(len, kernels))),
            tuple(kernels),
        )
        state_cache[labels] = result
        return result

    def neighbours(labels: tuple[int, ...]):
        answer = []
        for first_coordinate, second_coordinate in combinations(
            range(3), 2
        ):
            for first, label in enumerate(labels):
                if label != first_coordinate:
                    continue
                for second, other_label in enumerate(labels):
                    if other_label != second_coordinate:
                        continue
                    changed = list(labels)
                    changed[first], changed[second] = (
                        changed[second], changed[first]
                    )
                    candidate = tuple(changed)
                    data = state_data(candidate)
                    if data is not None:
                        answer.append(
                            (candidate, (first, second), data)
                        )
        return answer

    seed_data = state_data(seed)
    assert seed_data is not None
    seed_profile, seed_flags, seed_psi, seed_kernels = seed_data
    assert seed_profile == SEED_PROFILE
    assert seed_flags == 0 and seed_psi == SEED_PSI
    assert tuple(map(len, seed_kernels)) == (20, 20, 20)

    first = neighbours(seed)
    assert len(first) == 93
    assert not any(
        data[2] < SEED_PSI or data[1] > 0
        for _, _, data in first
    )
    safe_first = [
        candidate
        for candidate, _, data in first
        if data[2] == SEED_PSI and data[1] == 0
    ]
    assert len(safe_first) == 24

    first_histogram = Counter(
        (data[2], data[1]) for _, _, data in first
    )
    second_histogram = Counter()
    second_legal_arcs = 0
    second_targets: set[tuple[int, ...]] = set()
    for first_state in safe_first:
        second = neighbours(first_state)
        second_legal_arcs += len(second)
        for candidate, _, data in second:
            second_targets.add(candidate)
            second_histogram[(data[2], data[1])] += 1
            assert not (data[2] < SEED_PSI or data[1] > 0)
    assert second_legal_arcs == 2196
    assert len(second_targets) == 1895
    first_states = {candidate for candidate, _, _ in first}
    assert len(second_targets - first_states - {seed}) == 1852

    path_states = [seed]
    current = seed
    path_rows = []
    for local_exchange in ESCAPE_PATH:
        first_local, second_local = local_exchange
        first_coordinate = current[first_local]
        second_coordinate = current[second_local]
        assert first_coordinate != second_coordinate
        changed = list(current)
        changed[first_local], changed[second_local] = (
            changed[second_local], changed[first_local]
        )
        current = tuple(changed)
        data = state_data(current)
        assert data is not None
        profile, flags, psi, kernels = data
        path_rows.append(
            {
                "local_exchange": local_exchange,
                "full_edge_exchange": (
                    internal[first_local], internal[second_local]
                ),
                "coordinates": (
                    first_coordinate, second_coordinate
                ),
                "profile": profile,
                "kernel_sizes": tuple(map(len, kernels)),
                "psi": psi,
                "parallel_successful_flags": flags,
                "theorem_3_16_component_parity_success":
                    min(profile) == 0,
            }
        )
        path_states.append(current)
    assert path_rows[0]["psi"] == SEED_PSI
    assert path_rows[0]["parallel_successful_flags"] == 0
    assert not path_rows[0][
        "theorem_3_16_component_parity_success"
    ]
    assert path_rows[1]["psi"] == SEED_PSI
    assert path_rows[1]["parallel_successful_flags"] == 0
    assert not path_rows[1][
        "theorem_3_16_component_parity_success"
    ]
    assert (
        path_rows[2]["psi"] < SEED_PSI
        or path_rows[2]["parallel_successful_flags"] > 0
    )
    assert path_rows[2]["profile"] == (6, 6, 6, 6, 4, 4, 0)
    assert path_rows[2]["kernel_sizes"] == (20, 20, 21)
    assert path_rows[2]["psi"] == (0, 61)
    assert path_rows[2]["parallel_successful_flags"] == 3
    assert path_rows[2][
        "theorem_3_16_component_parity_success"
    ]

    def histogram_rows(histogram):
        return [
            {
                "psi": psi,
                "parallel_successful_flags": flags,
                "arcs": count,
            }
            for (psi, flags), count in sorted(histogram.items())
        ]

    output = {
        "schema":
            "jaeger-augmented-radius-two-counterexample-v1",
        "scope":
            "auxiliary_descent_statement_not_fivecdc",
        "graph6": GRAPH6,
        "root": ROOT,
        "structure": structure,
        "omitted_masks": OMITTED_MASKS,
        "seed_profile": seed_profile,
        "seed_kernel_sizes": tuple(map(len, seed_kernels)),
        "seed_psi": seed_psi,
        "seed_parallel_successful_flags": seed_flags,
        "seed_theorem_3_16_component_parity_success": False,
        "seed_theorem_3_16_defects_for_four_matching_values":
            theorem_316_defects(seed_kernels),
        "candidate_swaps": 3 * 19 * 19,
        "legal_first_neighbours": len(first),
        "safe_equal_first_neighbours": len(safe_first),
        "first_neighbour_histogram": histogram_rows(
            first_histogram
        ),
        "legal_second_arcs_from_safe_equal_first_neighbours":
            second_legal_arcs,
        "unique_second_targets": len(second_targets),
        "new_unique_distance_two_targets":
            len(second_targets - first_states - {seed}),
        "second_arc_histogram": histogram_rows(second_histogram),
        "lower_or_successful_endpoint_through_radius_two": False,
        "literal_escape_path": path_rows,
        "exact_augmented_escape_distance": 3,
        "standard_fivecdc_edge_labels": FIVECDC_LABELS,
        "standard_fivecdc_coordinate_sizes": fivecdc_sizes,
        "standard_fivecdc_checked": True,
        "semantic_dependency": str(SEMANTICS.relative_to(HERE.parent)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
