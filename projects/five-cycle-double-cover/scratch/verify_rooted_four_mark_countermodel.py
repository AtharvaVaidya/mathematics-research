#!/usr/bin/env python3
"""Independent finite check of the rooted four-mark countermodel.

This script uses only the Python standard library.  It verifies:

* the graph6 record and the connected simple cubic structure;
* every proper three-edge-colouring, modulo global colour permutation;
* universal bichromatic separation of the four marked edges;
* one colouring in which all marks have colour 2 and the root has colour 1;
* the displayed cyclic two-edge cut and its 3+1 mark split;
* all binary cycles containing the four marks, including the exact number
  with componentwise even marked parity and whether any avoids the root; and
* the marked-cut inequality failure and marked-subdivision girth.

The script is a finite checker, not a proof of any universal statement.
"""

from __future__ import annotations

from collections import deque
import json


GRAPH6 = (
    "[??????O@?R?d?EGGSAK?H_?HG?Ao@A_A"
    "?????????????C?G?C???M???B_???["
)
MARK_EDGES = ((3, 11), (6, 15), (7, 18), (22, 26))
ROOT_EDGE = (0, 20)
SECOND_CUT_EDGE = (8, 24)


def parse_graph6(row: str) -> tuple[int, list[tuple[int, int]]]:
    values = [ord(character) - 63 for character in row]
    assert values and all(0 <= value <= 63 for value in values)
    if values[0] <= 62:
        order = values[0]
        header = 1
    elif len(values) >= 4 and values[1] <= 62:
        order = (values[1] << 12) | (values[2] << 6) | values[3]
        header = 4
    else:
        raise AssertionError("unsupported or truncated graph6 header")

    edges: list[tuple[int, int]] = []
    bit = 0
    for right in range(1, order):
        for left in range(right):
            byte = header + bit // 6
            assert byte < len(values), "truncated graph6 record"
            if (values[byte] >> (5 - bit % 6)) & 1:
                edges.append((left, right))
            bit += 1
    return order, edges


def incidence(
    order: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    answer = [[] for _ in range(order)]
    for edge_id, (left, right) in enumerate(edges):
        answer[left].append(edge_id)
        answer[right].append(edge_id)
    return answer


def components_after_deleting(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    deleted: set[int],
) -> list[set[int]]:
    unseen = set(range(order))
    answer: list[set[int]] = []
    while unseen:
        root = min(unseen)
        component = {root}
        queue = deque([root])
        unseen.remove(root)
        while queue:
            vertex = queue.popleft()
            for edge_id in incident[vertex]:
                if edge_id in deleted:
                    continue
                left, right = edges[edge_id]
                neighbour = left ^ right ^ vertex
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    component.add(neighbour)
                    queue.append(neighbour)
        answer.append(component)
    return answer


def enumerate_tait_colourings(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    marks: set[int],
    root: int,
) -> tuple[int, bool]:
    colours = [-1] * len(edges)
    used = [0] * order
    count = 0
    all_mark_root_witness = False

    # Fix the ordered colours at vertex 0.  Every labelled Tait colouring
    # has exactly one global colour permutation satisfying this convention.
    assigned = 0
    for colour, edge_id in enumerate(incident[0]):
        left, right = edges[edge_id]
        bit = 1 << colour
        assert not (used[left] & bit or used[right] & bit)
        colours[edge_id] = colour
        used[left] |= bit
        used[right] |= bit
        assigned += 1

    def record() -> None:
        nonlocal count, all_mark_root_witness
        count += 1
        mark_colours = {colours[edge_id] for edge_id in marks}
        if len(mark_colours) == 1 and colours[root] not in mark_colours:
            all_mark_root_witness = True

        for omitted in range(3):
            seen_edges: set[int] = set()
            for start in range(len(edges)):
                if colours[start] == omitted or start in seen_edges:
                    continue
                component_edges = {start}
                stack = [start]
                seen_edges.add(start)
                while stack:
                    edge_id = stack.pop()
                    for vertex in edges[edge_id]:
                        for other in incident[vertex]:
                            if (
                                colours[other] != omitted
                                and other not in seen_edges
                            ):
                                seen_edges.add(other)
                                component_edges.add(other)
                                stack.append(other)
                assert len(component_edges & marks) <= 1, (
                    "marks are not universally separated",
                    omitted,
                    sorted(component_edges & marks),
                )

    def recurse(done: int) -> None:
        if done == len(edges):
            record()
            return
        best_edge = -1
        best_allowed = 0
        best_count = 4
        for edge_id, colour in enumerate(colours):
            if colour != -1:
                continue
            left, right = edges[edge_id]
            allowed = 7 & ~(used[left] | used[right])
            allowed_count = allowed.bit_count()
            if allowed_count == 0:
                return
            if allowed_count < best_count:
                best_edge = edge_id
                best_allowed = allowed
                best_count = allowed_count
                if allowed_count == 1:
                    break
        left, right = edges[best_edge]
        for colour in range(3):
            bit = 1 << colour
            if not (best_allowed & bit):
                continue
            colours[best_edge] = colour
            used[left] |= bit
            used[right] |= bit
            recurse(done + 1)
            used[left] ^= bit
            used[right] ^= bit
            colours[best_edge] = -1

    recurse(assigned)
    return count, all_mark_root_witness


def fundamental_cycle_basis(
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
) -> list[int]:
    parent = [-1] * order
    parent_edge = [-1] * order
    depth = [0] * order
    tree_edges: set[int] = set()
    parent[0] = 0
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge_id in incident[vertex]:
            left, right = edges[edge_id]
            neighbour = left ^ right ^ vertex
            if parent[neighbour] == -1:
                parent[neighbour] = vertex
                parent_edge[neighbour] = edge_id
                depth[neighbour] = depth[vertex] + 1
                tree_edges.add(edge_id)
                queue.append(neighbour)
    assert all(value != -1 for value in parent)

    basis: list[int] = []
    for edge_id, (left, right) in enumerate(edges):
        if edge_id in tree_edges:
            continue
        mask = 1 << edge_id
        while depth[left] > depth[right]:
            mask ^= 1 << parent_edge[left]
            left = parent[left]
        while depth[right] > depth[left]:
            mask ^= 1 << parent_edge[right]
            right = parent[right]
        while left != right:
            mask ^= 1 << parent_edge[left]
            mask ^= 1 << parent_edge[right]
            left = parent[left]
            right = parent[right]
        basis.append(mask)
    assert len(basis) == len(edges) - order + 1
    return basis


def even_marked_components(
    cycle: int,
    order: int,
    edges: list[tuple[int, int]],
    incident: list[list[int]],
    marks: set[int],
) -> bool:
    unseen_active = {
        vertex
        for vertex in range(order)
        if any((cycle >> edge_id) & 1 for edge_id in incident[vertex])
    }
    while unseen_active:
        root = min(unseen_active)
        vertices = {root}
        queue = deque([root])
        unseen_active.remove(root)
        while queue:
            vertex = queue.popleft()
            for edge_id in incident[vertex]:
                if not ((cycle >> edge_id) & 1):
                    continue
                left, right = edges[edge_id]
                neighbour = left ^ right ^ vertex
                if neighbour in unseen_active:
                    unseen_active.remove(neighbour)
                    vertices.add(neighbour)
                    queue.append(neighbour)
        mark_count = sum(
            1 for edge_id in marks if edges[edge_id][0] in vertices
        )
        if mark_count % 2:
            return False
    return True


def subdivided_girth(
    order: int, edges: list[tuple[int, int]], marks: set[int]
) -> int:
    adjacency = [[] for _ in range(order + len(marks))]
    mark_vertex = {
        edge_id: order + index
        for index, edge_id in enumerate(sorted(marks))
    }
    for edge_id, (left, right) in enumerate(edges):
        if edge_id not in marks:
            adjacency[left].append(right)
            adjacency[right].append(left)
            continue
        middle = mark_vertex[edge_id]
        adjacency[left].append(middle)
        adjacency[middle].append(left)
        adjacency[right].append(middle)
        adjacency[middle].append(right)

    answer = len(adjacency) + 1
    for root in range(len(adjacency)):
        distance = [-1] * len(adjacency)
        parent = [-1] * len(adjacency)
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if distance[neighbour] == -1:
                    distance[neighbour] = distance[vertex] + 1
                    parent[neighbour] = vertex
                    queue.append(neighbour)
                elif parent[vertex] != neighbour:
                    answer = min(
                        answer,
                        distance[vertex] + distance[neighbour] + 1,
                    )
    return answer


def main() -> None:
    order, edges = parse_graph6(GRAPH6)
    incident = incidence(order, edges)
    edge_id = {edge: index for index, edge in enumerate(edges)}
    marks = {edge_id[edge] for edge in MARK_EDGES}
    root = edge_id[ROOT_EDGE]
    second_cut = edge_id[SECOND_CUT_EDGE]

    assert order == 28
    assert len(edges) == 42
    assert len(set(edges)) == len(edges)
    assert all(left != right for left, right in edges)
    assert all(len(row) == 3 for row in incident)
    assert len(components_after_deleting(order, edges, incident, set())) == 1
    assert all(
        set(edges[left]).isdisjoint(edges[right])
        for left in marks
        for right in marks
        if left < right
    )

    colouring_count, colour_witness = enumerate_tait_colourings(
        order, edges, incident, marks, root
    )
    assert colouring_count == 162
    assert colour_witness

    cut_components = components_after_deleting(
        order, edges, incident, {root, second_cut}
    )
    assert len(cut_components) == 2
    cut_components.sort(key=lambda component: min(component))
    cut_mark_counts = [
        sum(1 for edge in MARK_EDGES if edge[0] in component)
        for component in cut_components
    ]
    assert cut_mark_counts == [3, 1]

    basis = fundamental_cycle_basis(order, edges, incident)
    mark_mask = sum(1 << edge for edge in marks)
    all_mark_cycles = 0
    even_component_cycles = 0
    even_component_root_avoiding = 0
    all_mark_root_avoiding = 0
    for coefficients in range(1 << len(basis)):
        cycle = 0
        for index, vector in enumerate(basis):
            if (coefficients >> index) & 1:
                cycle ^= vector
        if cycle & mark_mask != mark_mask:
            continue
        all_mark_cycles += 1
        if not ((cycle >> root) & 1):
            all_mark_root_avoiding += 1
        if even_marked_components(
            cycle, order, edges, incident, marks
        ):
            even_component_cycles += 1
            if not ((cycle >> root) & 1):
                even_component_root_avoiding += 1
            assert (cycle >> second_cut) & 1

    assert all_mark_cycles == 2048
    assert all_mark_root_avoiding > 0
    assert even_component_cycles == 360
    assert even_component_root_avoiding == 0

    small_shore = cut_components[1]
    assert len(small_shore) == 8
    marked_cut_left_side = 2 + cut_mark_counts[1]
    assert marked_cut_left_side == 3

    report = {
        "schema": "rooted-four-mark-countermodel-v1",
        "classification": (
            "EXACT_FINITE_COUNTERMODEL_WITHOUT_MARKED_CUT_HYPOTHESIS"
        ),
        "scope_warning": (
            "This refutes naive rooted avoidance, not the rooted theorem "
            "under the inherited marked-cut, marked-girth, paired-cut, "
            "and minimum-support hypotheses."
        ),
        "graph6": GRAPH6,
        "order": order,
        "edges": len(edges),
        "marks": [list(edge) for edge in MARK_EDGES],
        "root": list(ROOT_EDGE),
        "second_cut_edge": list(SECOND_CUT_EDGE),
        "tait_colourings_mod_s3": colouring_count,
        "universally_separated": True,
        "all_mark_one_colour_root_other_colour_exists": colour_witness,
        "two_cut_shore_orders": [len(row) for row in cut_components],
        "two_cut_mark_split": cut_mark_counts,
        "marked_cut_left_side_on_one_mark_shore": marked_cut_left_side,
        "marked_subdivision_girth": subdivided_girth(
            order, edges, marks
        ),
        "cycle_space_dimension": len(basis),
        "all_mark_binary_cycles": all_mark_cycles,
        "all_mark_root_avoiding_binary_cycles": all_mark_root_avoiding,
        "even_component_all_mark_binary_cycles": even_component_cycles,
        "even_component_root_avoiding_binary_cycles": (
            even_component_root_avoiding
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
