#!/usr/bin/env python3
"""Check the fixed-pair circuit-nullity reduction and its smallest cage.

The script is standalone and uses only the Python standard library.  It:

* verifies an explicit simple bridgeless cubic D5 state;
* constructs the auxiliary 4-regular graph for the coordinate pair 02;
* verifies the extended Cohn--Lempel circuit-nullity equality for all eight
  choices of 02-factor-component switches;
* exhausts loopless symmetric binary matrices of orders at most three and
  checks that order three is the first order at which the maximizers of
      nu(A + D_S) + nu(A + D_S + I)
  can fail symmetric exchange;
* verifies that the fixed-02 cage occurs at a state in a terminal
  equal-chi plateau, but a neutral 04 switch supplies the marked-root exit.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


GRAPH6 = "K??FEagT@WB_"
VERTICES = 12
EDGES = (
    (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9),
    (2, 6), (2, 8), (2, 10), (3, 7), (3, 9), (3, 11),
    (4, 8), (4, 10), (4, 11), (5, 9), (5, 10), (5, 11),
)
STATE = tuple(
    int(label, 16)
    for label in (
        "03", "05", "06", "05", "09", "0c",
        "06", "03", "05", "0c", "09", "05",
        "05", "03", "06", "05", "06", "03",
    )
)
PAIR = (0, 2)
PAIR_MASK = (1 << PAIR[0]) | (1 << PAIR[1])
ROOTS = (0, 10)


def decode_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    vertices = ord(record[0]) - 63
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    position = 0
    edges = []
    for right in range(1, vertices):
        for left in range(right):
            if bits[position]:
                edges.append((left, right))
            position += 1
    return vertices, tuple(sorted(edges))


INCIDENCE: list[list[int]] = [[] for _ in range(VERTICES)]
for edge, (left, right) in enumerate(EDGES):
    INCIDENCE[left].append(edge)
    INCIDENCE[right].append(edge)


def edge_components(selected: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    unseen = set(selected)
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        queue = [first]
        while queue:
            edge = queue.pop()
            for vertex in EDGES[edge]:
                for other in INCIDENCE[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        component.add(other)
                        queue.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def coordinate_components(
    state: tuple[int, ...], coordinate: int
) -> tuple[tuple[int, ...], ...]:
    return edge_components(tuple(
        edge
        for edge, label in enumerate(state)
        if (label >> coordinate) & 1
    ))


def factor_components(
    state: tuple[int, ...], pair: tuple[int, int]
) -> tuple[tuple[int, ...], ...]:
    mask = (1 << pair[0]) | (1 << pair[1])
    return edge_components(tuple(
        edge
        for edge, label in enumerate(state)
        if (label & mask).bit_count() == 1
    ))


def switched_component(
    state: tuple[int, ...],
    pair: tuple[int, int],
    component: tuple[int, ...],
) -> tuple[int, ...]:
    mask = (1 << pair[0]) | (1 << pair[1])
    answer = list(state)
    for edge in component:
        answer[edge] ^= mask
        assert answer[edge].bit_count() == 2
    return tuple(answer)


def chi(state: tuple[int, ...]) -> int:
    return (
        sum(
            len(coordinate_components(state, coordinate))
            for coordinate in range(5)
        )
        - len(EDGES)
        + VERTICES
    )


def gf2_rank(rows: list[int], columns: int) -> int:
    rows = rows[:]
    pivot = 0
    for column in range(columns):
        found = next(
            (
                row
                for row in range(pivot, len(rows))
                if (rows[row] >> column) & 1
            ),
            None,
        )
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        for row in range(len(rows)):
            if row != pivot and ((rows[row] >> column) & 1):
                rows[row] ^= rows[pivot]
        pivot += 1
    return pivot


def gf2_nullity(rows: list[int], columns: int) -> int:
    return columns - gf2_rank(rows, columns)


def validate_graph_and_state() -> None:
    assert decode_graph6(GRAPH6) == (VERTICES, EDGES)
    assert len(set(EDGES)) == len(EDGES)
    assert all(left != right for left, right in EDGES)
    assert all(len(row) == 3 for row in INCIDENCE)
    assert all(label.bit_count() == 2 for label in STATE)
    for row in INCIDENCE:
        assert STATE[row[0]] ^ STATE[row[1]] ^ STATE[row[2]] == 0

    for removed in range(len(EDGES)):
        seen = {0}
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            for edge in INCIDENCE[vertex]:
                if edge == removed:
                    continue
                left, right = EDGES[edge]
                other = left ^ right ^ vertex
                if other not in seen:
                    seen.add(other)
                    queue.append(other)
        assert len(seen) == VERTICES


def auxiliary_four_regular_graph() -> tuple[
    tuple[int, ...],
    tuple[tuple[int, int], ...],
    dict[int, int],
]:
    """Contract the 02-labelled matching and retain the Y_02 edges."""
    common = tuple(
        edge for edge, label in enumerate(STATE) if label == PAIR_MASK
    )
    common_index = {edge: index for index, edge in enumerate(common)}
    common_at_vertex: dict[int, int] = {}
    for edge in common:
        for vertex in EDGES[edge]:
            assert vertex not in common_at_vertex
            common_at_vertex[vertex] = common_index[edge]
    assert set(common_at_vertex) == set(range(VERTICES))

    y_edges = tuple(
        edge
        for edge, label in enumerate(STATE)
        if (label & PAIR_MASK).bit_count() == 1
    )
    assert set(common) | set(y_edges) == set(range(len(EDGES)))
    auxiliary_edges = tuple(
        (common_at_vertex[left], common_at_vertex[right])
        for edge in y_edges
        for left, right in (EDGES[edge],)
    )
    degrees = [0] * len(common)
    for left, right in auxiliary_edges:
        degrees[left] += 1
        degrees[right] += 1
    assert degrees == [4] * len(common)
    return y_edges, auxiliary_edges, common_index


def auxiliary_components(
    vertex_count: int, auxiliary_edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    adjacency = [[] for _ in range(vertex_count)]
    for edge, (left, right) in enumerate(auxiliary_edges):
        adjacency[left].append((edge, right))
        adjacency[right].append((edge, left))
    unseen = set(range(vertex_count))
    answer = []
    while unseen:
        first = unseen.pop()
        component = {first}
        queue = [first]
        while queue:
            vertex = queue.pop()
            for _, other in adjacency[vertex]:
                if other in unseen:
                    unseen.remove(other)
                    component.add(other)
                    queue.append(other)
        answer.append(tuple(sorted(component)))
    return tuple(answer)


def euler_system(
    vertex_count: int, auxiliary_edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Return one (vertex sequence, edge sequence) Euler circuit per component."""
    adjacency: list[list[tuple[int, int]]] = [
        [] for _ in range(vertex_count)
    ]
    for edge, (left, right) in enumerate(auxiliary_edges):
        adjacency[left].append((edge, right))
        adjacency[right].append((edge, left))

    used: set[int] = set()
    circuits = []
    for component in auxiliary_components(vertex_count, auxiliary_edges):
        if all(edge in used for vertex in component for edge, _ in adjacency[vertex]):
            continue
        stack_vertices = [component[0]]
        stack_edges: list[int] = []
        reverse_vertices: list[int] = []
        reverse_edges: list[int] = []
        while stack_vertices:
            vertex = stack_vertices[-1]
            next_step = next(
                (
                    (edge, other)
                    for edge, other in adjacency[vertex]
                    if edge not in used
                ),
                None,
            )
            if next_step is None:
                reverse_vertices.append(stack_vertices.pop())
                if stack_edges:
                    reverse_edges.append(stack_edges.pop())
                continue
            edge, other = next_step
            used.add(edge)
            stack_edges.append(edge)
            stack_vertices.append(other)
        vertices = tuple(reversed(reverse_vertices))
        edges = tuple(reversed(reverse_edges))
        assert len(vertices) == len(edges) + 1
        assert vertices[0] == vertices[-1]
        for index, edge in enumerate(edges):
            assert set(auxiliary_edges[edge]) == {
                vertices[index], vertices[index + 1]
            }
        circuits.append((vertices, edges))
    assert used == set(range(len(auxiliary_edges)))
    return tuple(circuits)


def euler_interlace_data(
    vertex_count: int,
    auxiliary_edges: tuple[tuple[int, int], ...],
    circuits: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> tuple[list[int], dict[int, frozenset[frozenset[int]]], dict[tuple[int, int], int]]:
    """Interlace rows, Euler transitions, and half-edge directions."""
    interlace_rows = [0] * vertex_count
    phi: dict[int, frozenset[frozenset[int]]] = {}
    direction: dict[tuple[int, int], int] = {}

    for vertices, edges in circuits:
        length = len(edges)
        positions: dict[int, list[int]] = {}
        for position, vertex in enumerate(vertices[:-1]):
            positions.setdefault(vertex, []).append(position)
            outgoing = edges[position]
            incoming = edges[(position - 1) % length]
            direction[(vertex, outgoing)] = 1
            direction[(vertex, incoming)] = 0
            phi.setdefault(vertex, set()).add(frozenset((incoming, outgoing)))

        for vertex, occurrences in positions.items():
            assert len(occurrences) == 2
            phi[vertex] = frozenset(phi[vertex])
            assert len(phi[vertex]) == 2
        for left, right in combinations(sorted(positions), 2):
            left_0, left_1 = sorted(positions[left])
            right_between = sum(
                left_0 < position < left_1 for position in positions[right]
            )
            if right_between == 1:
                interlace_rows[left] |= 1 << right
                interlace_rows[right] |= 1 << left

    assert set(phi) == set(range(vertex_count))
    for edge, (left, right) in enumerate(auxiliary_edges):
        assert direction[(left, edge)] != direction[(right, edge)]
    return interlace_rows, phi, direction


def coordinate_transition(
    state: tuple[int, ...],
    common_edge: int,
    y_edge_to_auxiliary: dict[int, int],
) -> frozenset[frozenset[int]]:
    left, right = EDGES[common_edge]
    pairs = []
    for coordinate in PAIR:
        coordinate_half_edges = []
        for vertex in (left, right):
            candidates = [
                edge
                for edge in INCIDENCE[vertex]
                if edge != common_edge
                and ((state[edge] >> coordinate) & 1)
            ]
            assert len(candidates) == 1
            coordinate_half_edges.append(
                y_edge_to_auxiliary[candidates[0]]
            )
        pairs.append(frozenset(coordinate_half_edges))
    answer = frozenset(pairs)
    assert len(answer) == 2
    return answer


def circuit_partition_count(
    vertex_count: int,
    auxiliary_edges: tuple[tuple[int, int], ...],
    transitions: dict[int, frozenset[frozenset[int]]],
) -> int:
    """Count circuits by connected components of the half-edge port graph."""
    nodes = {
        (vertex, edge)
        for edge, endpoints in enumerate(auxiliary_edges)
        for vertex in endpoints
    }
    adjacency: dict[tuple[int, int], set[tuple[int, int]]] = {
        node: set() for node in nodes
    }
    for edge, (left, right) in enumerate(auxiliary_edges):
        adjacency[(left, edge)].add((right, edge))
        adjacency[(right, edge)].add((left, edge))
    for vertex in range(vertex_count):
        for pair in transitions[vertex]:
            first, second = tuple(pair)
            adjacency[(vertex, first)].add((vertex, second))
            adjacency[(vertex, second)].add((vertex, first))
    assert all(len(neighbours) == 2 for neighbours in adjacency.values())

    unseen = set(nodes)
    circuits = 0
    while unseen:
        circuits += 1
        first = unseen.pop()
        queue = [first]
        while queue:
            node = queue.pop()
            for other in adjacency[node]:
                if other in unseen:
                    unseen.remove(other)
                    queue.append(other)
    return circuits


def modified_interlace_nullity(
    interlace_rows: list[int],
    phi: dict[int, frozenset[frozenset[int]]],
    direction: dict[tuple[int, int], int],
    transitions: dict[int, frozenset[frozenset[int]]],
) -> int:
    retained = [
        vertex
        for vertex in range(len(interlace_rows))
        if transitions[vertex] != phi[vertex]
    ]
    rows = []
    for row_index, vertex in enumerate(retained):
        row = 0
        for column_index, other in enumerate(retained):
            if vertex != other and ((interlace_rows[vertex] >> other) & 1):
                row |= 1 << column_index
        if vertex == retained[row_index]:
            # The non-Euler transition is orientation-inconsistent exactly
            # when each paired pair has equal Euler orientation.
            inconsistent = all(
                direction[(vertex, first)] == direction[(vertex, second)]
                for pair in transitions[vertex]
                for first, second in (tuple(pair),)
            )
            if inconsistent:
                row |= 1 << row_index
            else:
                assert all(
                    direction[(vertex, first)] != direction[(vertex, second)]
                    for pair in transitions[vertex]
                    for first, second in (tuple(pair),)
                )
        rows.append(row)
    return gf2_nullity(rows, len(retained))


def validate_extended_cohn_lempel_cube() -> None:
    y_edges, auxiliary_edges, common_index = auxiliary_four_regular_graph()
    vertex_count = len(common_index)
    circuits = euler_system(vertex_count, auxiliary_edges)
    interlace_rows, phi, direction = euler_interlace_data(
        vertex_count, auxiliary_edges, circuits
    )
    component_count = len(
        auxiliary_components(vertex_count, auxiliary_edges)
    )
    y_edge_to_auxiliary = {
        original_edge: auxiliary_edge
        for auxiliary_edge, original_edge in enumerate(y_edges)
    }
    switch_components = factor_components(STATE, PAIR)
    assert switch_components == (
        (0, 2, 6, 7),
        (4, 5, 9, 10),
        (13, 14, 16, 17),
    )

    observed_cycle_sums = []
    observed_nullities = []
    for mask in range(1 << len(switch_components)):
        state = STATE
        for component_index, component in enumerate(switch_components):
            if (mask >> component_index) & 1:
                state = switched_component(state, PAIR, component)
        transitions = {
            common_index[common_edge]: coordinate_transition(
                state, common_edge, y_edge_to_auxiliary
            )
            for common_edge in common_index
        }
        partition_circuits = circuit_partition_count(
            vertex_count, auxiliary_edges, transitions
        )
        pair_cycle_sum = sum(
            len(coordinate_components(state, coordinate))
            for coordinate in PAIR
        )
        nullity = modified_interlace_nullity(
            interlace_rows, phi, direction, transitions
        )
        assert pair_cycle_sum == partition_circuits
        assert partition_circuits == component_count + nullity
        observed_cycle_sums.append(pair_cycle_sum)
        observed_nullities.append(nullity)

    assert observed_cycle_sums == [5, 3, 3, 3, 3, 3, 3, 5]
    assert observed_nullities == [4, 2, 2, 2, 2, 2, 2, 4]


def diagonal_nullity_sum(rows: list[int], size: int, subset: int) -> int:
    full = (1 << size) - 1
    answer = 0
    for complement in (0, full):
        matrix = [
            rows[row] ^ ((((subset ^ complement) >> row) & 1) << row)
            for row in range(size)
        ]
        answer += gf2_nullity(matrix, size)
    return answer


def satisfies_symmetric_exchange(feasible: set[int], size: int) -> bool:
    for left in feasible:
        for right in feasible:
            difference = left ^ right
            for first in range(size):
                if not ((difference >> first) & 1):
                    continue
                if not any(
                    ((difference >> second) & 1)
                    and (
                        left
                        ^ (1 << first)
                        ^ (0 if second == first else (1 << second))
                    )
                    in feasible
                    for second in range(size)
                ):
                    return False
    return True


def loopless_symmetric_matrices(size: int):
    positions = list(combinations(range(size), 2))
    for mask in range(1 << len(positions)):
        rows = [0] * size
        for bit, (left, right) in enumerate(positions):
            if (mask >> bit) & 1:
                rows[left] |= 1 << right
                rows[right] |= 1 << left
        yield rows


def validate_smallest_binary_cage() -> None:
    failure_counts = {}
    for size in range(1, 4):
        failures = 0
        for rows in loopless_symmetric_matrices(size):
            values = [
                diagonal_nullity_sum(rows, size, subset)
                for subset in range(1 << size)
            ]
            maximum = max(values)
            feasible = {
                subset
                for subset, value in enumerate(values)
                if value == maximum
            }
            if not satisfies_symmetric_exchange(feasible, size):
                failures += 1
        failure_counts[size] = failures
    assert failure_counts == {1: 0, 2: 0, 3: 4}

    triangle = [0b110, 0b101, 0b011]
    values = [
        diagonal_nullity_sum(triangle, 3, subset)
        for subset in range(8)
    ]
    assert values == [3, 1, 1, 1, 1, 1, 1, 3]
    feasible = {
        subset for subset, value in enumerate(values) if value == 3
    }
    assert feasible == {0b000, 0b111}
    assert not satisfies_symmetric_exchange(feasible, 3)


def factor_chain_distance(
    state: tuple[int, ...], root_left: int, root_right: int
) -> int:
    nodes = [
        frozenset(component)
        for pair in combinations(range(5), 2)
        for component in factor_components(state, pair)
    ]
    starts = [index for index, node in enumerate(nodes) if root_left in node]
    targets = {
        index for index, node in enumerate(nodes) if root_right in node
    }
    distances = {index: 1 for index in starts}
    queue = deque(starts)
    while queue:
        index = queue.popleft()
        if index in targets:
            return distances[index]
        for other, node in enumerate(nodes):
            if other not in distances and nodes[index] & node:
                distances[other] = distances[index] + 1
                queue.append(other)
    raise AssertionError("factor-component graph is disconnected")


def circuit_edge_order(
    component: tuple[int, ...], root_edge: int, start_vertex: int
) -> tuple[int, ...]:
    selected = set(component)
    answer = [root_edge]
    left, right = EDGES[root_edge]
    vertex = left ^ right ^ start_vertex
    previous = root_edge
    while True:
        candidates = [
            edge
            for edge in INCIDENCE[vertex]
            if edge in selected and edge != previous
        ]
        assert len(candidates) == 1
        edge = candidates[0]
        if edge == root_edge:
            break
        answer.append(edge)
        left, right = EDGES[edge]
        vertex = left ^ right ^ vertex
        previous = edge
    return tuple(answer)


def validate_marked_corner_and_cross_pair_exit() -> None:
    old_chi = chi(STATE)
    assert old_chi == 2
    assert factor_chain_distance(STATE, *ROOTS) == 2

    p_component = (0, 1, 3, 5, 9, 11, 15, 17)
    root_q_component = (0, 2, 6, 7)
    target_q_component = (4, 5, 9, 10)
    assert p_component in factor_components(STATE, (0, 3))
    assert root_q_component in factor_components(STATE, PAIR)
    assert target_q_component in factor_components(STATE, PAIR)
    assert ROOTS[0] in p_component and ROOTS[0] in root_q_component
    assert ROOTS[1] in target_q_component
    assert set(p_component) & set(target_q_component)

    # Starting at root edge 0 in this orientation, the first edge on the
    # P-circuit belonging to a non-root Q-component is edge 5 in D.
    edge_order = circuit_edge_order(p_component, ROOTS[0], 0)
    assert edge_order == (0, 3, 5, 15, 17, 11, 9, 1)
    q_components = factor_components(STATE, PAIR)
    first_foreign = next(
        edge
        for edge in edge_order[1:]
        if any(
            edge in component and component != root_q_component
            for component in q_components
        )
    )
    assert first_foreign == 5
    assert first_foreign in target_q_component

    # The first-foreign switch is topologically legal but loses chi.
    q_switched = switched_component(STATE, PAIR, root_q_component)
    assert chi(q_switched) - old_chi == -2
    assert factor_chain_distance(q_switched, *ROOTS) == 2

    # A different coordinate pair supplies the actual neutral rooted exit.
    cross_component = (0, 1, 3, 4)
    assert cross_component in factor_components(STATE, (0, 4))
    cross_switched = switched_component(
        STATE, (0, 4), cross_component
    )
    assert chi(cross_switched) == old_chi
    assert factor_chain_distance(cross_switched, *ROOTS) == 1

    # Exact cross-pair coupling: a switch on R toggles precisely the six
    # factors meeting R in one coordinate.  In particular it changes Y_02
    # by symmetric difference with K and creates two direct root factors.
    pairs = tuple(combinations(range(5), 2))
    changed_pairs = []
    for pair in pairs:
        mask = (1 << pair[0]) | (1 << pair[1])
        before = {
            edge
            for edge, label in enumerate(STATE)
            if (label & mask).bit_count() == 1
        }
        after = {
            edge
            for edge, label in enumerate(cross_switched)
            if (label & mask).bit_count() == 1
        }
        if before != after:
            assert after == before ^ set(cross_component)
            changed_pairs.append(pair)
        else:
            assert len(set(pair) & {0, 4}) in (0, 2)
    assert tuple(changed_pairs) == (
        (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)
    )
    direct_root_factors = {
        pair
        for pair in pairs
        if any(
            ROOTS[0] in component and ROOTS[1] in component
            for component in factor_components(cross_switched, pair)
        )
    }
    assert direct_root_factors == {(0, 1), (3, 4)}


def validate_terminal_plateau() -> None:
    """Exhaust the literal equal-chi component and all its boundary moves."""
    target_chi = chi(STATE)
    pairs = tuple(combinations(range(5), 2))
    seen = {STATE}
    queue = deque([STATE])
    directed_neutral_moves = 0
    while queue:
        state = queue.popleft()
        for pair in pairs:
            for component in factor_components(state, pair):
                other = switched_component(state, pair, component)
                delta = chi(other) - target_chi
                assert delta <= 0
                if delta == 0:
                    directed_neutral_moves += 1
                    if other not in seen:
                        seen.add(other)
                        queue.append(other)
    assert len(seen) == 4980
    assert directed_neutral_moves == 70800


def main() -> None:
    validate_graph_and_state()
    validate_extended_cohn_lempel_cube()
    validate_smallest_binary_cage()
    validate_marked_corner_and_cross_pair_exit()
    validate_terminal_plateau()
    print(
        "PASS: exact 4-regular circuit-nullity cube; smallest loopless "
        "binary cage at order 3; 4,980-state terminal plateau; marked "
        "02 corner exits neutrally only through the checked 04 move"
    )


if __name__ == "__main__":
    main()
