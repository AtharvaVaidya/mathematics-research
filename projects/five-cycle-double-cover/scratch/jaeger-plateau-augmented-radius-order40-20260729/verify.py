#!/usr/bin/env python3
"""Re-audit the order-40 witness under three different orders.

The old audit orders states only by d_min.  A second order declares a
successful parallel component/circuit span flag terminal but still keeps
d_min as its only numeric level.  The current project order instead uses
lexicographic Psi=(d_min,S), where S is the sum of the three odd-kernel
sizes, and also declares span success terminal.  These orders have escape
distances four, three, and one, respectively, on this literal state.
"""

from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import sys


SCRATCH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRATCH))

import verify_jaeger_plateau_escape_radius4_order40 as base  # noqa: E402


def dot(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def in_binary_span(target: int, columns: list[int]) -> bool:
    basis: dict[int, int] = {}
    for vector in columns:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
    while target:
        pivot = target.bit_length() - 1
        if pivot not in basis:
            return False
        target ^= basis[pivot]
    return True


def fano_evaluation(
    order: int,
    edges: tuple[tuple[int, int], ...],
    kernels: tuple[frozenset[int], ...],
) -> tuple[tuple[int, ...], int]:
    """Reconstruct the seven defects and 21 span flags locally."""
    incidence: list[list[int]] = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    flow = tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(len(edges))
    )
    assert all(flow)
    normal = []
    for vertex in range(order):
        candidates = [
            functional
            for functional in range(1, 8)
            if all(
                dot(functional, flow[edge]) == 0
                for edge in incidence[vertex]
            )
        ]
        assert len(candidates) == 1
        normal.append(candidates[0])

    profile = []
    successful_flags = 0
    for functional in range(1, 8):
        zero_parent = list(range(order))

        def zero_find(vertex: int) -> int:
            while zero_parent[vertex] != vertex:
                zero_parent[vertex] = zero_parent[zero_parent[vertex]]
                vertex = zero_parent[vertex]
            return vertex

        def zero_unite(left: int, right: int) -> None:
            left = zero_find(left)
            right = zero_find(right)
            if left != right:
                zero_parent[left] = right

        zero_degree = [0] * order
        for edge, (left, right) in enumerate(edges):
            if dot(functional, flow[edge]):
                continue
            zero_degree[left] += 1
            zero_degree[right] += 1
            zero_unite(left, right)
        assert all(degree in (1, 3) for degree in zero_degree)

        transverse = functional & -functional
        parity = [0] * order
        for vertex in range(order):
            if zero_degree[vertex] == 1:
                parity[zero_find(vertex)] ^= dot(
                    normal[vertex] ^ functional, transverse
                )
        component_index: dict[int, int] = {}
        beta = 0
        for vertex in range(order):
            component = zero_find(vertex)
            if component not in component_index:
                component_index[component] = len(component_index)
            if component == vertex and parity[component]:
                beta |= 1 << component_index[component]
        profile.append(beta.bit_count())

        outside_parent = list(range(order))

        def outside_find(vertex: int) -> int:
            while outside_parent[vertex] != vertex:
                outside_parent[vertex] = outside_parent[
                    outside_parent[vertex]
                ]
                vertex = outside_parent[vertex]
            return vertex

        def outside_unite(left: int, right: int) -> None:
            left = outside_find(left)
            right = outside_find(right)
            if left != right:
                outside_parent[left] = right

        for edge, (left, right) in enumerate(edges):
            if dot(functional, flow[edge]):
                outside_unite(left, right)
        inside_value = [0] * order
        for vertex in range(order):
            if zero_degree[vertex] != 1:
                continue
            values = [
                flow[edge]
                for edge in incidence[vertex]
                if not dot(functional, flow[edge])
            ]
            assert len(values) == 1
            inside_value[vertex] = values[0]

        for direction in range(1, 8):
            if dot(functional, direction):
                continue
            gamma: dict[int, int] = {}
            for vertex in range(order):
                if (
                    zero_degree[vertex] != 1
                    or inside_value[vertex] == direction
                ):
                    continue
                outside = outside_find(vertex)
                gamma[outside] = gamma.get(outside, 0) ^ (
                    1 << component_index[zero_find(vertex)]
                )
            successful_flags += in_binary_span(
                beta, [value for value in gamma.values() if value]
            )
    return tuple(profile), successful_flags


def main() -> None:
    order, edges = base.decode_graph6(base.GRAPH6)
    incidence = base.incidence(order, edges)
    internal = tuple(
        edge for edge in range(len(edges)) if edge not in base.SPOKES
    )
    all_internal = (1 << len(internal)) - 1
    reconstruction_cache: dict[
        tuple[int, int, int],
        tuple[frozenset[int], ...] | None,
    ] = {}
    evaluation_cache: dict[
        tuple[int, int, int],
        tuple[tuple[int, ...], int],
    ] = {}

    def reconstruct(
        omitted: tuple[int, int, int],
    ) -> tuple[frozenset[int], ...] | None:
        if omitted in reconstruction_cache:
            return reconstruction_cache[omitted]
        if (
            omitted[0] ^ omitted[1] ^ omitted[2] != all_internal
            or omitted[0] & omitted[1]
            or omitted[0] & omitted[2]
            or omitted[1] & omitted[2]
            or tuple(mask.bit_count() for mask in omitted) != (19, 19, 19)
        ):
            reconstruction_cache[omitted] = None
            return None
        kernels = []
        for coordinate in range(3):
            tree = frozenset(
                [base.SPOKES[coordinate]]
                + [
                    edge
                    for local, edge in enumerate(internal)
                    if not ((omitted[coordinate] >> local) & 1)
                ]
            )
            if not base.is_tree(order, edges, incidence, tree):
                reconstruction_cache[omitted] = None
                return None
            kernels.append(
                base.odd_kernel(order, edges, incidence, tree)
            )
        answer = tuple(kernels)
        reconstruction_cache[omitted] = answer
        return answer

    def evaluate(
        omitted: tuple[int, int, int],
    ) -> tuple[tuple[int, ...], int]:
        if omitted not in evaluation_cache:
            kernels = reconstruct(omitted)
            if kernels is None:
                raise AssertionError("evaluation requested for illegal state")
            evaluation = fano_evaluation(order, edges, kernels)
            assert evaluation[0] == base.exact_profile(
                order, edges, incidence, kernels
            )
            evaluation_cache[omitted] = evaluation
        return evaluation_cache[omitted]

    def neighbours(
        omitted: tuple[int, int, int],
    ) -> list[tuple[int, int, int]]:
        answer = []
        for first in range(3):
            for second in range(first + 1, 3):
                first_bits = omitted[first]
                while first_bits:
                    first_bit = first_bits & -first_bits
                    first_bits ^= first_bit
                    second_bits = omitted[second]
                    while second_bits:
                        second_bit = second_bits & -second_bits
                        second_bits ^= second_bit
                        changed = list(omitted)
                        toggle = first_bit | second_bit
                        changed[first] ^= toggle
                        changed[second] ^= toggle
                        candidate = tuple(changed)
                        if reconstruct(candidate) is not None:
                            answer.append(candidate)
        assert len(answer) == len(set(answer))
        return answer

    start_profile, start_flags = evaluate(base.START)
    assert start_profile == base.EXPECTED_START_PROFILE
    assert start_flags == 0
    start_kernels = reconstruct(base.START)
    assert start_kernels is not None
    start_kernel_sizes = tuple(map(len, start_kernels))
    assert start_kernel_sizes == (26, 27, 25)
    start_psi = (min(start_profile), sum(start_kernel_sizes))
    assert start_psi == (2, 78)
    level = min(start_profile)
    assert level == 2

    parent: dict[
        tuple[int, int, int], tuple[int, int, int] | None
    ] = {base.START: None}
    distance = {base.START: 0}
    queue = deque([base.START])
    layer_histogram: Counter[int] = Counter()
    target_class_by_source_layer: Counter[tuple[int, str]] = Counter()
    legal_arcs = 0
    candidate_swaps = 0
    first_escape: tuple[int, int, int] | None = None
    first_escape_parent: tuple[int, int, int] | None = None
    maximum_internal_radius = 3

    while queue:
        current = queue.popleft()
        current_distance = distance[current]
        layer_histogram[current_distance] += 1
        candidate_swaps += 3 * 19 * 19
        for candidate in neighbours(current):
            legal_arcs += 1
            profile, flags = evaluate(candidate)
            score = min(profile)
            lower = score < level
            success = flags > 0
            if lower and success:
                target_class = "lower_and_success"
            elif lower:
                target_class = "lower_only"
            elif success:
                target_class = "success_only"
            elif score == level:
                target_class = "safe_plateau"
            else:
                target_class = f"higher_{score}"
            target_class_by_source_layer[
                (current_distance, target_class)
            ] += 1
            if lower or success:
                if first_escape is None:
                    first_escape = candidate
                    first_escape_parent = current
                continue
            if (
                score == level
                and current_distance < maximum_internal_radius
                and candidate not in distance
            ):
                distance[candidate] = current_distance + 1
                parent[candidate] = current
                queue.append(candidate)

    assert first_escape is not None and first_escape_parent is not None
    escape_distance = distance[first_escape_parent] + 1
    path = [first_escape]
    cursor: tuple[int, int, int] | None = first_escape_parent
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    path_evaluations = [
        {
            "omitted_internal_masks": list(state),
            "profile_h1_through_h7": list(evaluate(state)[0]),
            "parallel_successful_flags": evaluate(state)[1],
            "kernel_sizes": list(map(len, reconstruct(state) or ())),
            "lexicographic_psi": [
                min(evaluate(state)[0]),
                sum(map(len, reconstruct(state) or ())),
            ],
        }
        for state in path
    ]

    old_distance = {base.START: 0}
    old_queue = deque([base.START])
    while old_queue:
        current = old_queue.popleft()
        current_distance = old_distance[current]
        if current_distance >= maximum_internal_radius:
            continue
        for candidate in neighbours(current):
            profile, _ = evaluate(candidate)
            if min(profile) == level and candidate not in old_distance:
                old_distance[candidate] = current_distance + 1
                old_queue.append(candidate)
    assert len(old_distance) == 958
    assert set(distance) <= set(old_distance)
    assert escape_distance == 3
    assert layer_histogram == Counter({3: 836, 2: 108, 1: 13, 0: 1})
    assert len(distance) == 958
    assert set(distance) == set(old_distance)
    assert candidate_swaps == 1_037_514
    assert legal_arcs == 67_392
    assert target_class_by_source_layer == Counter(
        {
            (0, "higher_4"): 38,
            (0, "higher_6"): 14,
            (0, "safe_plateau"): 13,
            (1, "higher_4"): 508,
            (1, "higher_6"): 174,
            (1, "safe_plateau"): 197,
            (2, "higher_4"): 4275,
            (2, "higher_6"): 1317,
            (2, "higher_8"): 8,
            (2, "safe_plateau"): 1885,
            (2, "success_only"): 1,
            (3, "higher_4"): 32535,
            (3, "higher_6"): 8995,
            (3, "higher_8"): 103,
            (3, "lower_and_success"): 32,
            (3, "safe_plateau"): 17162,
            (3, "success_only"): 135,
        }
    )
    expected_path = (
        base.START,
        (
            95184251353315492,
            47576007214007363,
            1354929508533016,
        ),
        (
            95184251353315492,
            47576007482442817,
            1354929240097562,
        ),
        (
            95184251319761062,
            47576007482442817,
            1354929273651992,
        ),
    )
    assert tuple(path) == expected_path
    assert tuple(
        (
            tuple(state["profile_h1_through_h7"]),
            state["parallel_successful_flags"],
            tuple(state["kernel_sizes"]),
            tuple(state["lexicographic_psi"]),
        )
        for state in path_evaluations
    ) == (
        ((8, 2, 8, 8, 6, 10, 10), 0, (26, 27, 25), (2, 78)),
        ((6, 2, 6, 8, 8, 8, 10), 0, (26, 27, 24), (2, 77)),
        ((2, 6, 8, 12, 6, 4, 8), 0, (26, 25, 21), (2, 72)),
        ((4, 6, 6, 8, 6, 4, 6), 1, (24, 25, 21), (4, 70)),
    )
    escape_exchanges = []
    for source, target in zip(path, path[1:]):
        changed_coordinates = [
            coordinate
            for coordinate in range(3)
            if source[coordinate] != target[coordinate]
        ]
        assert len(changed_coordinates) == 2
        first, second = changed_coordinates
        toggle = source[first] ^ target[first]
        assert toggle == (source[second] ^ target[second])
        positions = tuple(
            position
            for position in range(len(internal))
            if (toggle >> position) & 1
        )
        assert len(positions) == 2
        escape_exchanges.append(
            {
                "coordinates": [first, second],
                "local_edge_positions": list(positions),
                "full_edge_ids": [
                    internal[position] for position in positions
                ],
                "edge_endpoints": [
                    list(edges[internal[position]]) for position in positions
                ],
            }
        )
    assert escape_exchanges == [
        {
            "coordinates": [0, 2],
            "local_edge_positions": [3, 21],
            "full_edge_ids": [6, 24],
            "edge_endpoints": [[5, 6], [6, 20]],
        },
        {
            "coordinates": [1, 2],
            "local_edge_positions": [1, 28],
            "full_edge_ids": [2, 31],
            "edge_endpoints": [[2, 3], [22, 23]],
        },
        {
            "coordinates": [0, 2],
            "local_edge_positions": [1, 25],
            "full_edge_ids": [2, 28],
            "edge_endpoints": [[2, 3], [3, 22]],
        },
    ]

    immediate_lex_histogram: Counter[tuple[int, int]] = Counter()
    immediate_lex_lower = 0
    immediate_lex_equal = 0
    immediate_lex_higher = 0
    immediate_success = 0
    for candidate in neighbours(base.START):
        profile, flags = evaluate(candidate)
        kernels = reconstruct(candidate)
        assert kernels is not None
        psi = (min(profile), sum(map(len, kernels)))
        immediate_lex_histogram[psi] += 1
        immediate_lex_lower += psi < start_psi
        immediate_lex_equal += psi == start_psi
        immediate_lex_higher += psi > start_psi
        immediate_success += flags > 0
    assert (
        immediate_lex_lower
        + immediate_lex_equal
        + immediate_lex_higher
        == len(neighbours(base.START))
        == 65
    )
    assert immediate_success == 0
    assert immediate_lex_lower > 0

    report = {
        "schema": "jaeger-order40-three-orderings-audit-v2",
        "graph6": base.GRAPH6,
        "order": order,
        "root": base.ROOT,
        "spokes_in_coordinate_order": list(base.SPOKES),
        "start_omitted_internal_masks": list(base.START),
        "start_profile_h1_through_h7": list(start_profile),
        "start_parallel_successful_flags": start_flags,
        "start_kernel_sizes": list(start_kernel_sizes),
        "start_lexicographic_psi": list(start_psi),
        "d_min_only_lower_escape_distance": 4,
        "d_min_only_with_terminal_span_success_escape_distance":
            escape_distance,
        "lexicographic_psi_with_terminal_span_success_escape_distance": 1,
        "d_min_only_complete_safe_plateau_ball_radius":
            maximum_internal_radius,
        "d_min_only_safe_plateau_layer_histogram": {
            str(key): value for key, value in sorted(layer_histogram.items())
        },
        "d_min_only_safe_plateau_states": len(distance),
        "old_d_min_only_plateau_states": len(old_distance),
        "old_states_excluded_by_terminal_success": len(
            set(old_distance) - set(distance)
        ),
        "candidate_swaps_checked": candidate_swaps,
        "legal_exchange_arcs_checked": legal_arcs,
        "d_min_only_target_class_by_source_layer": {
            f"{layer}:{target}": count
            for (layer, target), count
            in sorted(target_class_by_source_layer.items())
        },
        "d_min_only_terminal_success_escape_path": path_evaluations,
        "d_min_only_terminal_success_escape_exchanges": escape_exchanges,
        "lexicographic_psi_immediate_neighbours": {
            "legal": 65,
            "lower": immediate_lex_lower,
            "equal": immediate_lex_equal,
            "higher": immediate_lex_higher,
            "span_successful": immediate_success,
            "psi_histogram": {
                str(key): value
                for key, value in sorted(immediate_lex_histogram.items())
            },
        },
        "lexicographic_psi_shortest_escape_path":
            path_evaluations[:2],
        "lexicographic_psi_shortest_escape_exchange":
            escape_exchanges[0],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
