#!/usr/bin/env python3
"""Standard-library verification of the flow and reconfiguration certificate.

This checker is independent of the C++ randomized Jaeger-state producer and
of the Z3 search that first found the five-move path.  It reconstructs the
seed flow from the frozen three-tree state, checks the H--S profiles, proves
the absence of legal paths of length at most four by finite exhaustive
arguments, validates the five-move path literally, and independently replays
the complete reciprocal-exchange neighbourhood.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

import verify as graph_certificate


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "reconfiguration-certificate.json"


class DSU:
    def __init__(self, order: int) -> None:
        self.parent = list(range(order))
        self.size = [1] * order

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, first: int, second: int) -> None:
        first, second = self.find(first), self.find(second)
        if first == second:
            return
        if self.size[first] < self.size[second]:
            first, second = second, first
        self.parent[second] = first
        self.size[first] += self.size[second]


def incidence(
    order: int, edges: tuple[tuple[int, int], ...]
) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def scalar(first: int, second: int) -> int:
    return (first & second).bit_count() & 1


def is_tree(
    order: int,
    edges: tuple[tuple[int, int], ...],
    chosen: set[int] | frozenset[int],
) -> bool:
    if len(chosen) != order - 1:
        return False
    dsu = DSU(order)
    for edge in chosen:
        left, right = edges[edge]
        if dsu.find(left) == dsu.find(right):
            return False
        dsu.union(left, right)
    return True


def odd_kernel(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: set[int] | frozenset[int],
) -> frozenset[int]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * order
    parent_edge = [-1] * order
    parent[0] = 0
    traversal = [0]
    for vertex in traversal:
        for other, edge in adjacency[vertex]:
            if parent[other] < 0:
                parent[other] = vertex
                parent_edge[other] = edge
                traversal.append(other)
    assert len(traversal) == order
    subtree_size = [1] * order
    answer: set[int] = set()
    for vertex in reversed(traversal[1:]):
        if subtree_size[vertex] & 1:
            answer.add(parent_edge[vertex])
        subtree_size[parent[vertex]] += subtree_size[vertex]
    degree = [0] * order
    for edge in answer:
        left, right = edges[edge]
        degree[left] += 1
        degree[right] += 1
    assert all(value & 1 for value in degree)
    return frozenset(answer)


def flow_from_kernels(
    edge_count: int,
    kernels: tuple[frozenset[int], frozenset[int], frozenset[int]]
    | list[frozenset[int]],
) -> tuple[int, ...]:
    return tuple(
        sum(
            1 << coordinate
            for coordinate in range(3)
            if edge not in kernels[coordinate]
        )
        for edge in range(edge_count)
    )


def check_flow(flow: tuple[int, ...], rows: list[list[int]]) -> None:
    assert all(1 <= value <= 7 for value in flow)
    assert all(
        flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0
        for row in rows
    )


def hs_profile(
    order: int,
    edges: tuple[tuple[int, int], ...],
    flow: tuple[int, ...],
) -> tuple[int, ...]:
    answer = []
    for functional in range(1, 8):
        components = DSU(order)
        for edge, (left, right) in enumerate(edges):
            if not scalar(functional, flow[edge]):
                components.union(left, right)
        transverse_value = next(
            value
            for value in range(1, 8)
            if scalar(functional, value)
        )
        parity: dict[int, int] = {}
        for edge, (left, right) in enumerate(edges):
            if flow[edge] != transverse_value:
                continue
            for vertex in (left, right):
                root = components.find(vertex)
                parity[root] = parity.get(root, 0) ^ 1
        answer.append(sum(parity.values()))
    return tuple(answer)


def span_contains(target: int, columns: list[int]) -> bool:
    pivots: dict[int, int] = {}
    for column in columns:
        while column:
            pivot = column.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = column
                break
            column ^= pivots[pivot]
    while target:
        pivot = target.bit_length() - 1
        if pivot not in pivots:
            return False
        target ^= pivots[pivot]
    return True


def parallel_successful_flags(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: list[list[int]],
    flow: tuple[int, ...],
) -> int:
    normals = []
    for row in rows:
        choices = [
            functional
            for functional in range(1, 8)
            if all(not scalar(functional, flow[edge]) for edge in row)
        ]
        assert len(choices) == 1
        normals.append(choices[0])

    flags = 0
    for functional in range(1, 8):
        zero = DSU(order)
        zero_degree = [0] * order
        for edge, (left, right) in enumerate(edges):
            if scalar(functional, flow[edge]):
                continue
            zero.union(left, right)
            zero_degree[left] += 1
            zero_degree[right] += 1
        assert all(value in (1, 3) for value in zero_degree)
        roots = sorted({zero.find(vertex) for vertex in range(order)})
        root_index = {root: index for index, root in enumerate(roots)}
        transverse = functional & -functional
        beta = 0
        for vertex in range(order):
            if (
                zero_degree[vertex] == 1
                and scalar(normals[vertex] ^ functional, transverse)
            ):
                beta ^= 1 << root_index[zero.find(vertex)]

        outside = DSU(order)
        for edge, (left, right) in enumerate(edges):
            if scalar(functional, flow[edge]):
                outside.union(left, right)
        inside_value = [0] * order
        for vertex in range(order):
            if zero_degree[vertex] != 1:
                continue
            values = [
                flow[edge]
                for edge in rows[vertex]
                if not scalar(functional, flow[edge])
            ]
            assert len(values) == 1
            inside_value[vertex] = values[0]

        for direction in range(1, 8):
            if scalar(functional, direction):
                continue
            columns: dict[int, int] = {}
            for vertex in range(order):
                if (
                    zero_degree[vertex] != 1
                    or inside_value[vertex] == direction
                ):
                    continue
                outside_root = outside.find(vertex)
                columns[outside_root] = columns.get(outside_root, 0) ^ (
                    1 << root_index[zero.find(vertex)]
                )
            flags += span_contains(
                beta, [column for column in columns.values() if column]
            )
    return flags


def binary_rank(values: tuple[int, ...] | list[int] | set[int]) -> int:
    basis = [0, 0, 0]
    answer = 0
    for value in values:
        for bit in range(2, -1, -1):
            if not ((value >> bit) & 1):
                continue
            if basis[bit]:
                value ^= basis[bit]
            else:
                basis[bit] = value
                answer += 1
                break
    return answer


def membership_map(
    constants: tuple[int, ...], pivot_positions: tuple[int, int, int]
) -> dict[int, int]:
    answer: dict[int, int] = {}
    for subset in range(8):
        value = 0
        mask = 0
        for local, position in enumerate(pivot_positions):
            if (subset >> local) & 1:
                value ^= constants[position]
                mask |= 1 << position
        answer[value] = mask
    assert len(answer) == 8
    return answer


def legal_prefixes(
    start: int, constants: tuple[int, ...], membership: int
) -> bool:
    current = start
    for position, constant in enumerate(constants):
        if (membership >> position) & 1:
            current ^= constant
        if current == 0:
            return False
    return True


def support_is_eulerian(
    support: set[int] | frozenset[int],
    rows: list[list[int]],
) -> bool:
    return all(
        sum(edge in support for edge in row) % 2 == 0
        for row in rows
    )


def simple_cycle_components(
    support: set[int] | frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> list[frozenset[int]]:
    vertex_edges: dict[int, list[int]] = {}
    for edge in support:
        left, right = edges[edge]
        vertex_edges.setdefault(left, []).append(edge)
        vertex_edges.setdefault(right, []).append(edge)
    assert all(len(row) == 2 for row in vertex_edges.values())
    unseen = set(support)
    answer = []
    while unseen:
        first = min(unseen)
        seen_edges = {first}
        left, right = edges[first]
        seen_vertices = {left, right}
        stack = [left, right]
        while stack:
            vertex = stack.pop()
            for edge in vertex_edges[vertex]:
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    u, v = edges[edge]
                    other = u ^ v ^ vertex
                    if other not in seen_vertices:
                        seen_vertices.add(other)
                        stack.append(other)
        assert len(seen_edges) == len(seen_vertices)
        answer.append(frozenset(seen_edges))
        unseen -= seen_edges
    return answer


def forced_free_eulerian_feasible(
    order: int,
    edges: tuple[tuple[int, int], ...],
    allowed: list[int],
) -> bool:
    """Whether t_e in allowed[e] can form an Eulerian edge-subset.

    Bit 0 of ``allowed[e]`` permits t_e=0 and bit 1 permits t_e=1.
    Forced-one edges prescribe a boundary.  A subset of the free edges
    realizes that boundary exactly when every free-edge component contains
    an even number of prescribed odd vertices.
    """
    required = [0] * order
    free_adjacency = [[] for _ in range(order)]
    for edge, choices in enumerate(allowed):
        if choices == 0:
            return False
        left, right = edges[edge]
        if choices == 2:
            required[left] ^= 1
            required[right] ^= 1
        elif choices == 3:
            free_adjacency[left].append(right)
            free_adjacency[right].append(left)
    unseen = set(range(order))
    while unseen:
        root = min(unseen)
        seen = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in free_adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        if sum(required[vertex] for vertex in seen) & 1:
            return False
        unseen -= seen
    return True


def audit_short_paths(
    order: int,
    edges: tuple[tuple[int, int], ...],
    rows: list[list[int]],
    start: tuple[int, ...],
    target: tuple[int, ...],
) -> dict[str, int]:
    difference = tuple(
        first ^ second for first, second in zip(start, target)
    )
    assert binary_rank(set(difference)) == 3

    length_three = 0
    legal_three = 0
    for constants in permutations(range(1, 8), 3):
        if binary_rank(constants) != 3:
            continue
        length_three += 1
        coordinates = membership_map(constants, (0, 1, 2))
        memberships = [coordinates[value] for value in difference]
        supports = [
            {
                edge
                for edge, membership in enumerate(memberships)
                if (membership >> move) & 1
            }
            for move in range(3)
        ]
        assert all(support_is_eulerian(support, rows) for support in supports)
        if all(
            legal_prefixes(start[edge], constants, memberships[edge])
            for edge in range(len(edges))
        ):
            legal_three += 1

    length_four = 0
    local_blocked_four = 0
    parity_blocked_four = 0
    legal_four = 0
    for constants in product(range(1, 8), repeat=4):
        if binary_rank(constants) != 3:
            continue
        length_four += 1
        pivots = next(
            positions
            for positions in combinations(range(4), 3)
            if binary_rank(tuple(constants[index] for index in positions))
            == 3
        )
        coordinates = membership_map(constants, pivots)
        dependencies = []
        for mask in range(1, 16):
            value = 0
            for position in range(4):
                if (mask >> position) & 1:
                    value ^= constants[position]
            if value == 0:
                dependencies.append(mask)
        assert len(dependencies) == 1
        dependency = dependencies[0]

        allowed = []
        for edge, difference_value in enumerate(difference):
            base = coordinates[difference_value]
            choices = 0
            for toggle in (0, 1):
                membership = base ^ (dependency if toggle else 0)
                if legal_prefixes(start[edge], constants, membership):
                    choices |= 1 << toggle
            allowed.append(choices)
        if 0 in allowed:
            local_blocked_four += 1
        elif not forced_free_eulerian_feasible(order, edges, allowed):
            parity_blocked_four += 1
        else:
            legal_four += 1

    assert length_three == 168 and legal_three == 0
    assert length_four == 1848 and legal_four == 0
    assert local_blocked_four + parity_blocked_four == length_four
    return {
        "rank_three_ordered_bases": length_three,
        "legal_three_move_paths": legal_three,
        "rank_three_ordered_four_tuples": length_four,
        "four_tuples_with_local_blocker": local_blocked_four,
        "four_tuples_with_global_parity_blocker": parity_blocked_four,
        "legal_four_move_paths": legal_four,
    }


def tree_cut_data(
    order: int,
    edges: tuple[tuple[int, int], ...],
    tree: set[int],
) -> tuple[list[int], list[int], dict[int, int]]:
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(order)]
    for edge in tree:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    parent = [-1] * order
    parent[0] = 0
    child_by_edge: dict[int, int] = {}
    tin = [-1] * order
    tout = [-1] * order
    clock = 0
    stack = [(0, -1, 0)]
    while stack:
        vertex, parent_edge, phase = stack.pop()
        if phase == 0:
            tin[vertex] = clock
            clock += 1
            stack.append((vertex, parent_edge, 1))
            for other, edge in reversed(adjacency[vertex]):
                if edge == parent_edge or parent[other] >= 0:
                    continue
                parent[other] = vertex
                child_by_edge[edge] = other
                stack.append((other, edge, 0))
        else:
            tout[vertex] = clock
    assert clock == order
    return tin, tout, child_by_edge


def separated_by_tree_edge(
    data: tuple[list[int], list[int], dict[int, int]],
    tree_edge: int,
    other_edge: int,
    edges: tuple[tuple[int, int], ...],
) -> bool:
    tin, tout, child_by_edge = data
    child = child_by_edge[tree_edge]
    left, right = edges[other_edge]
    left_inside = tin[child] <= tin[left] < tout[child]
    right_inside = tin[child] <= tin[right] < tout[child]
    return left_inside != right_inside


def audit_jaeger_neighbourhood(
    order: int,
    edges: tuple[tuple[int, int], ...],
    state: tuple[int, ...],
    internal: tuple[int, ...],
    trees: tuple[set[int], set[int], set[int]],
    kernels: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> dict[str, object]:
    cut_data = [
        tree_cut_data(order, edges, trees[coordinate])
        for coordinate in range(3)
    ]
    positions = [
        [local for local, label in enumerate(state) if label == coordinate]
        for coordinate in range(3)
    ]
    candidate_pairs = 0
    legal: list[tuple[int, int, int, int]] = []
    for first_coordinate in range(3):
        for second_coordinate in range(first_coordinate + 1, 3):
            candidate_pairs += (
                len(positions[first_coordinate])
                * len(positions[second_coordinate])
            )
            for first in positions[first_coordinate]:
                first_edge = internal[first]
                for second in positions[second_coordinate]:
                    second_edge = internal[second]
                    if (
                        separated_by_tree_edge(
                            cut_data[first_coordinate],
                            second_edge,
                            first_edge,
                            edges,
                        )
                        and separated_by_tree_edge(
                            cut_data[second_coordinate],
                            first_edge,
                            second_edge,
                            edges,
                        )
                    ):
                        legal.append((
                            first,
                            second,
                            first_coordinate,
                            second_coordinate,
                        ))
    assert candidate_pairs == 591408
    assert len(legal) == 2640

    initial_profile = hs_profile(
        order, edges, flow_from_kernels(len(edges), kernels)
    )
    initial_potential = (min(initial_profile), sum(map(len, kernels)))
    lower = 0
    minimum = (order + 1, 3 * len(edges))
    first_minimum: tuple[int, int, tuple[int, ...]] | None = None
    potential_histogram: Counter[tuple[int, int]] = Counter()
    for first, second, first_coordinate, second_coordinate in legal:
        first_edge = internal[first]
        second_edge = internal[second]
        changed_first = set(trees[first_coordinate])
        changed_second = set(trees[second_coordinate])
        changed_first.remove(second_edge)
        changed_first.add(first_edge)
        changed_second.remove(first_edge)
        changed_second.add(second_edge)
        candidate_kernels = list(kernels)
        candidate_kernels[first_coordinate] = odd_kernel(
            order, edges, changed_first
        )
        candidate_kernels[second_coordinate] = odd_kernel(
            order, edges, changed_second
        )
        candidate_flow = flow_from_kernels(len(edges), candidate_kernels)
        candidate_profile = hs_profile(order, edges, candidate_flow)
        candidate_potential = (
            min(candidate_profile),
            sum(map(len, candidate_kernels)),
        )
        potential_histogram[candidate_potential] += 1
        if candidate_potential < initial_potential:
            lower += 1
        if candidate_potential < minimum:
            minimum = candidate_potential
            first_minimum = (first, second, candidate_profile)

    assert lower == 822
    assert minimum == (92, 1533)
    assert first_minimum == (
        545,
        1194,
        (180, 184, 114, 184, 130, 146, 92),
    )
    return {
        "candidate_reciprocal_pairs": candidate_pairs,
        "legal_reciprocal_neighbours": len(legal),
        "strictly_lower_neighbours": lower,
        "distinct_neighbour_potentials": len(potential_histogram),
        "minimum_neighbour_potential": list(minimum),
        "first_minimum_swap_local_positions": [
            first_minimum[0],
            first_minimum[1],
        ],
        "first_minimum_profile": list(first_minimum[2]),
        "augmented_escape_distance": 1,
    }


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text())
    assert payload["schema"] == "petersen-foster-flow-reconfiguration-v1"
    order = 890
    edge_set = graph_certificate.petersen_foster_edges()
    edges = tuple(graph_certificate.graph6_edge_order(order, edge_set))
    rows = incidence(order, edges)
    assert all(len(row) == 3 for row in rows)

    state = tuple(int(value) for value in payload["jaeger_state_digits"])
    internal = tuple(
        edge
        for edge, (left, right) in enumerate(edges)
        if left != payload["jaeger_root"]
        and right != payload["jaeger_root"]
    )
    spokes = tuple(rows[payload["jaeger_root"]])
    assert len(state) == len(internal) == 1332
    assert Counter(state) == {0: 444, 1: 444, 2: 444}
    trees = tuple(
        set([spokes[coordinate]] + [
            internal[local]
            for local, label in enumerate(state)
            if label != coordinate
        ])
        for coordinate in range(3)
    )
    assert all(is_tree(order, edges, tree) for tree in trees)
    kernels = tuple(odd_kernel(order, edges, tree) for tree in trees)
    assert tuple(map(len, kernels)) == (506, 507, 526)
    bad_flow = flow_from_kernels(len(edges), kernels)
    frozen_bad_flow = tuple(int(value) for value in payload["bad_flow_digits"])
    assert bad_flow == frozen_bad_flow
    check_flow(bad_flow, rows)
    bad_profile = hs_profile(order, edges, bad_flow)
    assert bad_profile == (174, 192, 138, 184, 130, 140, 110)
    assert parallel_successful_flags(
        order, edges, rows, bad_flow
    ) == 0

    fivecdc_masks = [
        int(value)
        for value in (HERE / "fivecdc-labels.txt").read_text().split()
    ]
    points = tuple(payload["good_point_assignment"])
    assert len(points) == len(set(points)) == 5
    good_flow = []
    for mask in fivecdc_masks:
        coordinates = [
            coordinate for coordinate in range(5)
            if (mask >> coordinate) & 1
        ]
        assert len(coordinates) == 2
        good_flow.append(
            points[coordinates[0]] ^ points[coordinates[1]]
        )
    good_flow = tuple(good_flow)
    check_flow(good_flow, rows)
    good_profile = hs_profile(order, edges, good_flow)
    assert good_profile == (142, 160, 132, 0, 148, 130, 150)

    short_path_audit = audit_short_paths(
        order, edges, rows, bad_flow, good_flow
    )
    difference_rank = binary_rank({
        first ^ second
        for first, second in zip(bad_flow, good_flow)
    })
    assert difference_rank == 3

    constants = tuple(payload["legal_path_constants"])
    support_masks = [
        int(text, 16) for text in payload["legal_path_support_masks_hex"]
    ]
    assert len(constants) == len(support_masks) == 5
    assert all(mask >> len(edges) == 0 for mask in support_masks)
    supports = [
        {
            edge for edge in range(len(edges))
            if (mask >> edge) & 1
        }
        for mask in support_masks
    ]
    assert all(support_is_eulerian(support, rows) for support in supports)
    cycle_components = [
        simple_cycle_components(support, edges) for support in supports
    ]
    cycle_lengths = [
        sorted(map(len, components)) for components in cycle_components
    ]
    assert list(map(len, cycle_components)) == [14, 11, 10, 14, 14]
    assert cycle_lengths == [
        [10, 12, 14, 18, 20, 24, 26, 28, 28, 30, 32, 34, 52, 238],
        [10, 10, 10, 12, 14, 16, 26, 26, 34, 179, 271],
        [10, 10, 10, 10, 16, 28, 32, 46, 46, 357],
        [10, 10, 10, 12, 14, 18, 18, 20, 26, 28, 34, 42, 46, 322],
        [10, 10, 10, 10, 12, 12, 18, 20, 20, 24, 32, 62, 64, 300],
    ]
    current = list(bad_flow)
    connected_cycle_current = list(bad_flow)
    intermediate_profiles = []
    for constant, support, components in zip(
        constants, supports, cycle_components
    ):
        assert all(current[edge] != constant for edge in support)
        for edge in support:
            current[edge] ^= constant
        check_flow(tuple(current), rows)
        intermediate_profiles.append(hs_profile(order, edges, tuple(current)))
        for component in components:
            assert all(
                connected_cycle_current[edge] != constant
                for edge in component
            )
            for edge in component:
                connected_cycle_current[edge] ^= constant
            check_flow(tuple(connected_cycle_current), rows)
        assert connected_cycle_current == current
    assert tuple(current) == good_flow
    assert tuple(map(len, supports)) == (566, 608, 565, 610, 604)
    assert intermediate_profiles == [
        (140, 186, 144, 156, 114, 180, 112),
        (148, 172, 112, 158, 114, 182, 136),
        (170, 132, 124, 132, 180, 178, 152),
        (136, 106, 186, 132, 180, 164, 128),
        (142, 160, 132, 0, 148, 130, 150),
    ]

    neighbourhood = audit_jaeger_neighbourhood(
        order, edges, state, internal, trees, kernels
    )
    report = {
        "classification": "EXACT_FLOW_RECONFIGURATION_AND_JAEGER_AUDIT",
        "bad_flow_nowhere_zero": True,
        "bad_flow_value_counts": dict(sorted(Counter(bad_flow).items())),
        "bad_flow_hs_profile": list(bad_profile),
        "bad_flow_hs_good": False,
        "bad_flow_parallel_successful_flags": 0,
        "jaeger_kernel_sizes": list(map(len, kernels)),
        "good_flow_point_assignment": list(points),
        "good_flow_hs_profile": list(good_profile),
        "good_flow_hs_good": True,
        "difference_value_rank": difference_rank,
        "zero_allowing_fixed_value_distance": 3,
        "legal_eulerian_support_fixed_value_distance": 5,
        "connected_simple_cycle_distance_lower_bound": 5,
        "connected_simple_cycle_distance_upper_bound": sum(
            map(len, cycle_components)
        ),
        "legal_path_constants": list(constants),
        "legal_path_support_sizes": list(map(len, supports)),
        "legal_path_support_cycle_component_counts": list(
            map(len, cycle_components)
        ),
        "legal_path_support_cycle_lengths": cycle_lengths,
        "legal_path_intermediate_profiles": [
            list(profile) for profile in intermediate_profiles
        ],
        "short_path_exhaustion": short_path_audit,
        "jaeger_neighbourhood": neighbourhood,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
