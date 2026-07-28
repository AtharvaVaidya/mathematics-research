#!/usr/bin/env python3
"""Exact finite algebra for the three-root global-entry reduction.

The checker has three independent finite parts:

* all suppressed cubic multigraph kernels on two and four branch vertices;
* all D/O/E subdivision signatures of the flowable kernels; and
* every three-edge matching and every relevant maximum matching in the
  Petersen graph.

No external graph library is used.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product, permutations
import argparse
import json
from pathlib import Path


PETERSEN_EDGES = (
    (0, 1), (0, 4), (0, 5), (1, 2), (1, 6),
    (2, 3), (2, 7), (3, 4), (3, 8), (4, 9),
    (5, 7), (5, 8), (6, 8), (6, 9), (7, 9),
)


def edge_key(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def is_matching(edges: tuple[tuple[int, int], ...]) -> bool:
    return len({vertex for edge in edges for vertex in edge}) == 2 * len(edges)


def maximum_matchings(
    vertices: set[int], edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    candidates = []
    optimum = -1
    for size in range(len(vertices) // 2 + 1):
        rows = tuple(
            selected
            for selected in combinations(edges, size)
            if is_matching(selected)
        )
        if rows:
            optimum = size
            candidates = list(rows)
    assert optimum >= 0
    return tuple(candidates)


def adjacency(
    vertices: set[int], edges: tuple[tuple[int, int], ...]
) -> dict[int, list[tuple[int, int]]]:
    answer = {vertex: [] for vertex in vertices}
    for edge_id, (left, right) in enumerate(edges):
        answer[left].append((right, edge_id))
        answer[right].append((left, edge_id))
    return answer


def binary_cycles(
    vertices: set[int], edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    incident = adjacency(vertices, edges)
    result = []
    for mask in range(1 << len(edges)):
        if all(
            sum(bool(mask >> edge_id & 1) for _, edge_id in incident[vertex])
            % 2
            == 0
            for vertex in vertices
        ):
            result.append(mask)
    return tuple(result)


def nowhere_zero_f2_square(
    vertices: set[int], edges: tuple[tuple[int, int], ...]
) -> bool:
    cycles = binary_cycles(vertices, edges)
    full = (1 << len(edges)) - 1
    return any((left | right) == full for left in cycles for right in cycles)


def component_parity_good(
    vertices: set[int],
    edges: tuple[tuple[int, int], ...],
    covered: set[int],
) -> bool:
    incident = adjacency(vertices, edges)
    for mask in range(1 << len(edges)):
        degrees = {
            vertex: sum(
                bool(mask >> edge_id & 1)
                for _, edge_id in incident[vertex]
            )
            for vertex in vertices
        }
        if any(degree % 2 == 0 for degree in degrees.values()):
            continue
        selected_adjacency = {vertex: set() for vertex in vertices}
        for edge_id, (left, right) in enumerate(edges):
            if mask >> edge_id & 1:
                selected_adjacency[left].add(right)
                selected_adjacency[right].add(left)
        unseen = set(vertices)
        valid = True
        while unseen:
            start = next(iter(unseen))
            component = {start}
            stack = [start]
            unseen.remove(start)
            while stack:
                vertex = stack.pop()
                for other in selected_adjacency[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        stack.append(other)
            if len(component & covered) % 2:
                valid = False
                break
        if valid:
            return True
    return False


def canonical_kernel(
    branch_count: int,
    loops: tuple[int, ...],
    multiplicities: tuple[int, ...],
) -> tuple[int, ...]:
    pairs = tuple(combinations(range(branch_count), 2))
    answer = []
    for permutation in permutations(range(branch_count)):
        new_loops = [0] * branch_count
        matrix = [[0] * branch_count for _ in range(branch_count)]
        for vertex in range(branch_count):
            new_loops[permutation[vertex]] = loops[vertex]
        for value, (left, right) in zip(multiplicities, pairs):
            image_left = permutation[left]
            image_right = permutation[right]
            matrix[image_left][image_right] = value
            matrix[image_right][image_left] = value
        answer.append(
            tuple(new_loops)
            + tuple(matrix[left][right] for left, right in pairs)
        )
    return min(answer)


def kernel_from_edges(
    branch_count: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    loops = [0] * branch_count
    pairs = tuple(combinations(range(branch_count), 2))
    index = {pair: position for position, pair in enumerate(pairs)}
    multiplicities = [0] * len(pairs)
    for left, right in edges:
        if left == right:
            loops[left] += 1
        else:
            multiplicities[index[edge_key(left, right)]] += 1
    return canonical_kernel(
        branch_count, tuple(loops), tuple(multiplicities)
    )


def kernel_connected(
    branch_count: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    graph = {vertex: set() for vertex in range(branch_count)}
    for left, right in edges:
        if left != right:
            graph[left].add(right)
            graph[right].add(left)
    reached = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in graph[vertex] - reached:
            reached.add(other)
            stack.append(other)
    return len(reached) == branch_count


def kernel_flowable(
    branch_count: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    nonloops = tuple(edge for edge in edges if edge[0] != edge[1])
    for values in product((1, 2, 3), repeat=len(nonloops)):
        total = [0] * branch_count
        for value, (left, right) in zip(values, nonloops):
            total[left] ^= value
            total[right] ^= value
        if not any(total):
            return True
    return False


def enumerate_four_branch_kernels() -> dict[tuple[int, ...], dict[str, object]]:
    branch_count = 4
    pairs = tuple(combinations(range(branch_count), 2))
    kernels: dict[tuple[int, ...], dict[str, object]] = {}
    for loops in product(range(2), repeat=branch_count):
        remaining = tuple(3 - 2 * value for value in loops)
        for multiplicities in product(range(4), repeat=len(pairs)):
            degree = [0] * branch_count
            for value, (left, right) in zip(multiplicities, pairs):
                degree[left] += value
                degree[right] += value
            if tuple(degree) != remaining:
                continue
            edges = tuple(
                (vertex, vertex)
                for vertex, count in enumerate(loops)
                for _ in range(count)
            ) + tuple(
                pair
                for pair, count in zip(pairs, multiplicities)
                for _ in range(count)
            )
            key = kernel_from_edges(branch_count, edges)
            kernels.setdefault(
                key,
                {
                    "edges": edges,
                    "connected": kernel_connected(branch_count, edges),
                    "nowhere_zero_f2_square_flow": kernel_flowable(
                        branch_count, edges
                    ),
                },
            )
    assert len(kernels) == 8
    return kernels


THETA_EDGES = ((0, 1), (0, 1), (0, 1))
DUMBBELL_EDGES = ((0, 0), (0, 1), (1, 1))
THETA_THETA_EDGES = (
    (0, 1), (0, 1), (0, 1),
    (2, 3), (2, 3), (2, 3),
)
K4_EDGES = tuple(combinations(range(4), 2))
DOUBLE_C4_EDGES = (
    (0, 2), (0, 3), (0, 3),
    (1, 2), (1, 2), (1, 3),
)


def named_kernel_keys() -> dict[tuple[int, ...], str]:
    prototypes = {
        "theta+theta": THETA_THETA_EDGES,
        "theta+dumbbell": THETA_EDGES
        + tuple((left + 2, right + 2) for left, right in DUMBBELL_EDGES),
        "dumbbell+dumbbell": DUMBBELL_EDGES
        + tuple((left + 2, right + 2) for left, right in DUMBBELL_EDGES),
        "K4": K4_EDGES,
        "doubled-four-cycle": DOUBLE_C4_EDGES,
        "connected-one-loop": (
            (0, 1), (0, 2), (0, 3), (1, 2), (1, 2), (3, 3)
        ),
        "connected-two-loops": (
            (0, 1), (0, 1), (0, 3), (1, 2), (2, 2), (3, 3)
        ),
        "connected-three-loops": (
            (0, 1), (0, 2), (0, 3), (1, 1), (2, 2), (3, 3)
        ),
    }
    result = {
        kernel_from_edges(4, edges): name for name, edges in prototypes.items()
    }
    assert len(result) == 8
    return result


def signature_good(
    branch_count: int,
    kernel_edges: tuple[tuple[int, int], ...],
    signature: tuple[str, ...],
) -> bool:
    """Does a D/O/E subdivision admit a component-parity-good odd factor?"""
    choices = tuple(
        ((0, 0), (1, 1)) if edge_type in ("D", "O")
        else ((0, 1), (1, 0))
        for edge_type in signature
    )
    for incidence_bits in product(*choices):
        parity = [0] * branch_count
        direct_selected = []
        for (left, right), edge_type, (at_left, at_right) in zip(
            kernel_edges, signature, incidence_bits
        ):
            parity[left] ^= at_left
            parity[right] ^= at_right
            if edge_type == "D" and at_left == at_right == 1:
                direct_selected.append((left, right))
        if parity != [1] * branch_count:
            continue
        graph = {vertex: set() for vertex in range(branch_count)}
        for left, right in direct_selected:
            graph[left].add(right)
            graph[right].add(left)
        unseen = set(range(branch_count))
        valid = True
        while unseen:
            start = next(iter(unseen))
            component = {start}
            stack = [start]
            unseen.remove(start)
            while stack:
                vertex = stack.pop()
                for other in graph[vertex] & unseen:
                    unseen.remove(other)
                    component.add(other)
                    stack.append(other)
            if len(component) % 2:
                valid = False
                break
        if valid:
            return True
    return False


def available_direct_components_even(
    branch_count: int,
    kernel_edges: tuple[tuple[int, int], ...],
    signature: tuple[str, ...],
) -> bool:
    graph = {vertex: set() for vertex in range(branch_count)}
    for (left, right), edge_type in zip(kernel_edges, signature):
        if edge_type == "D":
            graph[left].add(right)
            graph[right].add(left)
    unseen = set(range(branch_count))
    while unseen:
        start = next(iter(unseen))
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            vertex = stack.pop()
            for other in graph[vertex] & unseen:
                unseen.remove(other)
                component.add(other)
                stack.append(other)
        if len(component) % 2:
            return False
    return True


def double_c4_exception(signature: tuple[str, ...]) -> bool:
    # Edge order:
    # 02, 03a, 03b, 12a, 12b, 13.
    if signature[0] != "D" or signature[5] != "D":
        return False
    first_pair = signature[1:3]
    second_pair = signature[3:5]
    if first_pair.count("E") != 1 or second_pair.count("E") != 1:
        return False
    first_other = next(value for value in first_pair if value != "E")
    second_other = next(value for value in second_pair if value != "E")
    return "O" in (first_other, second_other)


def signature_tables() -> dict[str, dict[str, object]]:
    kernels = {
        "theta": (2, THETA_EDGES),
        "theta+theta": (4, THETA_THETA_EDGES),
        "K4": (4, K4_EDGES),
        "doubled-four-cycle": (4, DOUBLE_C4_EDGES),
    }
    report = {}
    for name, (branch_count, edges) in kernels.items():
        passing = 0
        for signature in product("DOE", repeat=len(edges)):
            actual = signature_good(branch_count, edges, signature)
            if name == "theta":
                predicted = (
                    signature.count("E") % 2 == 0 and "D" in signature
                )
            elif name == "theta+theta":
                predicted = all(
                    part.count("E") % 2 == 0 and "D" in part
                    for part in (signature[:3], signature[3:])
                )
            elif name == "K4":
                predicted = (
                    signature.count("E") % 2 == 0
                    and available_direct_components_even(
                        branch_count, edges, signature
                    )
                )
            else:
                predicted = (
                    signature.count("E") % 2 == 0
                    and available_direct_components_even(
                        branch_count, edges, signature
                    )
                    and not double_c4_exception(signature)
                )
            if actual != predicted:
                raise AssertionError((name, signature, actual, predicted))
            passing += actual
        report[name] = {
            "edge_objects": len(edges),
            "signatures": 3 ** len(edges),
            "component_parity_good_signatures": passing,
        }
    assert {
        name: row["component_parity_good_signatures"]
        for name, row in report.items()
    } == {
        "theta": 10,
        "theta+theta": 100,
        "K4": 125,
        "doubled-four-cycle": 129,
    }
    return report


def suppress_complement(
    vertices: set[int],
    edges: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    graph = adjacency(vertices, edges)
    branches = tuple(sorted(vertex for vertex in vertices if len(graph[vertex]) == 3))
    branch_index = {vertex: index for index, vertex in enumerate(branches)}
    used: set[int] = set()
    paths = []
    for branch in branches:
        for other, edge_id in graph[branch]:
            if edge_id in used:
                continue
            used.add(edge_id)
            previous = branch
            current = other
            length = 1
            literal = [branch, other]
            while current not in branch_index:
                options = [
                    (next_vertex, next_edge)
                    for next_vertex, next_edge in graph[current]
                    if next_edge not in used
                ]
                if len(options) != 1:
                    raise AssertionError("degree-two path did not continue")
                next_vertex, next_edge = options[0]
                used.add(next_edge)
                previous, current = current, next_vertex
                length += 1
                literal.append(current)
            paths.append({
                "ends": (branch_index[branch], branch_index[current]),
                "length": length,
                "vertices": tuple(literal),
            })

    circuits = []
    for first_edge, (left, right) in enumerate(edges):
        if first_edge in used:
            continue
        used.add(first_edge)
        start = left
        previous = left
        current = right
        length = 1
        while current != start:
            options = [
                (next_vertex, edge_id)
                for next_vertex, edge_id in graph[current]
                if edge_id not in used
            ]
            if len(options) != 1:
                raise AssertionError("circuit did not continue")
            next_vertex, edge_id = options[0]
            used.add(edge_id)
            previous, current = current, next_vertex
            length += 1
        circuits.append(length)
    assert len(used) == len(edges)
    kernel_edges = tuple(row["ends"] for row in paths)
    return {
        "branches": branches,
        "paths": tuple(paths),
        "circuits": tuple(sorted(circuits)),
        "kernel_edges": kernel_edges,
        "kernel_key": kernel_from_edges(len(branches), kernel_edges),
        "signature": tuple(
            "D" if row["length"] == 1
            else "O" if row["length"] % 2
            else "E"
            for row in paths
        ),
    }


def verify_cycle(edge_set: tuple[tuple[int, int], ...]) -> None:
    degree = Counter(vertex for edge in edge_set for vertex in edge)
    assert degree and all(value == 2 for value in degree.values())
    graph = {vertex: set() for vertex in degree}
    for left, right in edge_set:
        graph[left].add(right)
        graph[right].add(left)
    reached = {next(iter(graph))}
    stack = list(reached)
    while stack:
        vertex = stack.pop()
        for other in graph[vertex] - reached:
            reached.add(other)
            stack.append(other)
    assert reached == set(graph)


PETERSEN_FIVE_CDC = (
    ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4)),
    ((0, 1), (0, 5), (1, 6), (5, 8), (6, 8)),
    ((0, 4), (0, 5), (4, 9), (5, 7), (7, 9)),
    ((2, 3), (2, 7), (3, 8), (6, 8), (6, 9), (7, 9)),
    (
        (1, 2), (1, 6), (2, 7), (3, 4), (3, 8),
        (4, 9), (5, 7), (5, 8), (6, 9),
    ),
)


def petersen_audit(named_keys: dict[tuple[int, ...], str]) -> dict[str, object]:
    vertices = set(range(10))
    roots_profile: Counter[int] = Counter()
    maximum_profile: Counter[tuple[int, str, bool, bool, tuple[str, ...]]] = Counter()
    first_by_deficiency = {}
    total_matchings = 0
    nonextendable = 0
    flowable_maxima = 0
    component_good_maxima = 0

    for roots in combinations(PETERSEN_EDGES, 3):
        if not is_matching(roots):
            continue
        total_matchings += 1
        root_vertices = {vertex for edge in roots for vertex in edge}
        h_vertices = vertices - root_vertices
        h_edges = tuple(
            edge
            for edge in PETERSEN_EDGES
            if edge[0] in h_vertices and edge[1] in h_vertices
        )
        maxima = maximum_matchings(h_vertices, h_edges)
        deficiency = len(h_vertices) - 2 * len(maxima[0])
        roots_profile[deficiency] += 1
        if deficiency == 0:
            continue
        nonextendable += 1
        for matching in maxima:
            zero_edges = {
                edge_key(*edge) for edge in roots + matching
            }
            complement_edges = tuple(
                edge for edge in PETERSEN_EDGES if edge not in zero_edges
            )
            flowable = nowhere_zero_f2_square(vertices, complement_edges)
            covered = {vertex for edge in zero_edges for vertex in edge}
            component_good = (
                component_parity_good(vertices, complement_edges, covered)
                if flowable else False
            )
            suppressed = suppress_complement(vertices, complement_edges)
            if deficiency == 2:
                kernel_name = (
                    "theta"
                    if suppressed["kernel_key"]
                    == kernel_from_edges(2, THETA_EDGES)
                    else "dumbbell"
                )
            else:
                kernel_name = named_keys[suppressed["kernel_key"]]
            signature = tuple(sorted(suppressed["signature"]))
            maximum_profile[(
                deficiency,
                kernel_name,
                flowable,
                component_good,
                signature,
            )] += 1
            flowable_maxima += flowable
            component_good_maxima += component_good
            expected_component = (
                not any(length % 2 for length in suppressed["circuits"])
                and signature_good(
                    deficiency,
                    suppressed["kernel_edges"],
                    suppressed["signature"],
                )
            )
            if component_good != expected_component:
                raise AssertionError("signature criterion disagrees with graph")
            first_by_deficiency.setdefault(deficiency, {
                "roots": roots,
                "H_vertices": tuple(sorted(h_vertices)),
                "H_edges": h_edges,
                "maximum_matching": matching,
                "kernel": kernel_name,
                "path_lengths": tuple(
                    row["length"] for row in suppressed["paths"]
                ),
                "signature": suppressed["signature"],
                "flowable": flowable,
                "component_parity_good": component_good,
            })

    assert total_matchings == 145
    assert roots_profile == Counter({0: 60, 2: 80, 4: 5})
    assert nonextendable == 85
    assert flowable_maxima == 185
    assert component_good_maxima == 0

    cover_count = Counter()
    for cycle in PETERSEN_FIVE_CDC:
        verify_cycle(cycle)
        for edge in cycle:
            assert edge in PETERSEN_EDGES
            cover_count[edge] += 1
    assert cover_count == Counter({edge: 2 for edge in PETERSEN_EDGES})

    return {
        "three_edge_matchings": total_matchings,
        "deficiency_profile": dict(sorted(roots_profile.items())),
        "nonextendable_root_matchings": nonextendable,
        "maximum_near_perfect_matchings": sum(maximum_profile.values()),
        "flowable_maximum_complements": flowable_maxima,
        "component_parity_good_maximum_complements": component_good_maxima,
        "maximum_profile": [
            {
                "deficiency": key[0],
                "kernel": key[1],
                "flowable": key[2],
                "component_parity_good": key[3],
                "sorted_signature": list(key[4]),
                "instances": count,
            }
            for key, count in sorted(maximum_profile.items())
        ],
        "first_by_deficiency": {
            str(deficiency): row
            for deficiency, row in sorted(first_by_deficiency.items())
        },
        "explicit_five_cdc": PETERSEN_FIVE_CDC,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    four_kernels = enumerate_four_branch_kernels()
    names = named_kernel_keys()
    kernel_rows = []
    for key, row in sorted(four_kernels.items()):
        name = names[key]
        kernel_rows.append({
            "name": name,
            "canonical_key": key,
            "connected": row["connected"],
            "nowhere_zero_f2_square_flow":
                row["nowhere_zero_f2_square_flow"],
        })
    flowable_names = {
        row["name"] for row in kernel_rows
        if row["nowhere_zero_f2_square_flow"]
    }
    assert flowable_names == {"theta+theta", "K4", "doubled-four-cycle"}

    report = {
        "schema": "three-root-global-entry-finite-algebra-v1",
        "classification": "EXACT FINITE KERNEL/SIGNATURE/PETERSEN AUDIT",
        "two_branch_kernels": [
            {
                "name": "theta",
                "nowhere_zero_f2_square_flow": True,
            },
            {
                "name": "dumbbell",
                "nowhere_zero_f2_square_flow": False,
            },
        ],
        "four_branch_kernels": kernel_rows,
        "signature_tables": signature_tables(),
        "status_alphabet": {
            "D": "suppressed path has length one (direct branch edge)",
            "O": "suppressed path has odd length at least three",
            "E": "suppressed path has even length",
        },
        "petersen": petersen_audit(names),
        "scope_warning": (
            "The kernel and status tables are universal finite algebra. "
            "The graph census is only the Petersen control. Failure of the "
            "three-root certificate route is not failure of FiveCDC; the "
            "report includes and checks an explicit Petersen 5CDC."
        ),
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="ascii")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
