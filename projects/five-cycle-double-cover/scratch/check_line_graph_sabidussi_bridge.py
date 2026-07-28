#!/usr/bin/env python3
"""Independent finite checks for the line-graph/Sabidussi bridge.

The script uses only the Python standard library.  It:

* constructs the Petersen graph and its edge-labelled line graph;
* enumerates D_4 and D_5 flows by direct propagation of the vertex XOR
  equations;
* maps a D_5 flow to a five-colouring of the line graph and back;
* checks the prescribed two triangle transitions at every line-graph vertex;
* independently enumerates Hamiltonian cycles, perfect matchings, and Tait
  colourings of the Petersen graph; and
* exhausts the local "recolour some edges with a fifth colour" repair at a
  switched degree-four vertex.

This is a checker for the claims in line-graph-sabidussi-bridge.md.  It is not
a Five-Cycle Double Cover solver.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


VERTICES = tuple(range(10))

# Outer 5-cycle 0--1--2--3--4--0, spokes i--(5+i), and inner pentagram.
PETERSEN_EDGES = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 4),
    (0, 5),
    (1, 6),
    (2, 7),
    (3, 8),
    (4, 9),
    (5, 7),
    (7, 9),
    (6, 9),
    (6, 8),
    (5, 8),
)


def incidence(edges: tuple[tuple[int, int], ...]) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in VERTICES]
    for edge, (left, right) in enumerate(edges):
        assert left != right
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence(PETERSEN_EDGES)


def label_text(label: int, coordinates: int) -> str:
    return "".join(str(i) for i in range(coordinates) if (label >> i) & 1)


def enumerate_d_flows(coordinates: int) -> tuple[tuple[int, ...], ...]:
    labels = tuple(
        (1 << first) | (1 << second)
        for first, second in combinations(range(coordinates), 2)
    )
    label_set = frozenset(labels)
    state = [0] * len(PETERSEN_EDGES)
    answers: list[tuple[int, ...]] = []

    def assign(edge: int, label: int, changed: list[int]) -> bool:
        if state[edge]:
            return state[edge] == label
        if label not in label_set:
            return False
        state[edge] = label
        changed.append(edge)
        pending = list(PETERSEN_EDGES[edge])
        while pending:
            vertex = pending.pop()
            row = INCIDENCE[vertex]
            assigned = [item for item in row if state[item]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[row[0]] ^ state[row[1]] ^ state[row[2]]:
                    return False
                continue
            missing = next(item for item in row if not state[item])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in label_set:
                return False
            state[missing] = forced
            changed.append(missing)
            pending.extend(PETERSEN_EDGES[missing])
        return True

    def visit() -> None:
        try:
            edge = next(index for index, label in enumerate(state) if not label)
        except StopIteration:
            answers.append(tuple(state))
            return
        for label in labels:
            changed: list[int] = []
            if assign(edge, label, changed):
                visit()
            for changed_edge in reversed(changed):
                state[changed_edge] = 0

    visit()
    return tuple(answers)


def validate_d_flow(state: tuple[int, ...], coordinates: int) -> None:
    labels = {
        (1 << first) | (1 << second)
        for first, second in combinations(range(coordinates), 2)
    }
    assert len(state) == len(PETERSEN_EDGES)
    assert all(label in labels for label in state)
    for row in INCIDENCE:
        assert state[row[0]] ^ state[row[1]] ^ state[row[2]] == 0


def line_graph():
    # A line edge is (first original edge, second original edge, triangle owner).
    line_edges: list[tuple[int, int, int]] = []
    for vertex, row in enumerate(INCIDENCE):
        for first, second in combinations(row, 2):
            line_edges.append((min(first, second), max(first, second), vertex))
    assert len(line_edges) == 30
    return tuple(line_edges)


LINE_EDGES = line_graph()


def d_flow_to_line_colouring(
    state: tuple[int, ...], coordinates: int
) -> tuple[int, ...]:
    validate_d_flow(state, coordinates)
    colours = []
    for first, second, _owner in LINE_EDGES:
        common = state[first] & state[second]
        assert common and common & (common - 1) == 0
        colours.append(common.bit_length() - 1)
    return tuple(colours)


def validate_line_colouring(
    colours: tuple[int, ...], coordinates: int
) -> None:
    assert len(colours) == len(LINE_EDGES)
    assert all(0 <= colour < coordinates for colour in colours)

    line_incidence: list[list[int]] = [[] for _ in PETERSEN_EDGES]
    owner_incidence: dict[tuple[int, int], list[int]] = {}
    for line_edge, (first, second, owner) in enumerate(LINE_EDGES):
        line_incidence[first].append(line_edge)
        line_incidence[second].append(line_edge)
        owner_incidence.setdefault((first, owner), []).append(line_edge)
        owner_incidence.setdefault((second, owner), []).append(line_edge)

    for original_edge, (left, right) in enumerate(PETERSEN_EDGES):
        assert len(line_incidence[original_edge]) == 4
        counts = Counter(colours[item] for item in line_incidence[original_edge])
        assert all(count % 2 == 0 for count in counts.values())
        for owner in (left, right):
            transition = owner_incidence[(original_edge, owner)]
            assert len(transition) == 2
            assert colours[transition[0]] != colours[transition[1]]


def line_colouring_to_d_flow(
    colours: tuple[int, ...], coordinates: int
) -> tuple[int, ...]:
    validate_line_colouring(colours, coordinates)
    line_incidence: list[list[int]] = [[] for _ in PETERSEN_EDGES]
    for line_edge, (first, second, _owner) in enumerate(LINE_EDGES):
        line_incidence[first].append(line_edge)
        line_incidence[second].append(line_edge)
    state = []
    for row in line_incidence:
        used = sorted(set(colours[item] for item in row))
        assert len(used) == 2
        state.append((1 << used[0]) | (1 << used[1]))
    answer = tuple(state)
    validate_d_flow(answer, coordinates)
    return answer


def enumerate_perfect_matchings() -> tuple[tuple[int, ...], ...]:
    answers: list[tuple[int, ...]] = []

    def visit(unmatched: frozenset[int], chosen: tuple[int, ...]) -> None:
        if not unmatched:
            answers.append(chosen)
            return
        vertex = min(unmatched)
        for edge in INCIDENCE[vertex]:
            left, right = PETERSEN_EDGES[edge]
            neighbour = right if left == vertex else left
            if neighbour in unmatched:
                visit(unmatched - {vertex, neighbour}, chosen + (edge,))

    visit(frozenset(VERTICES), ())
    return tuple(answers)


def cycle_lengths(edge_set: frozenset[int]) -> tuple[int, ...]:
    remaining = set(edge_set)
    lengths = []
    while remaining:
        first = next(iter(remaining))
        component_edges = {first}
        component_vertices = set(PETERSEN_EDGES[first])
        changed = True
        while changed:
            changed = False
            for edge in tuple(remaining - component_edges):
                if component_vertices.intersection(PETERSEN_EDGES[edge]):
                    component_edges.add(edge)
                    component_vertices.update(PETERSEN_EDGES[edge])
                    changed = True
        remaining -= component_edges
        lengths.append(len(component_edges))
    return tuple(sorted(lengths))


def count_hamiltonian_cycles() -> int:
    # Enumerate vertex cycles starting at 0, quotienting reversal at the end.
    adjacency = {
        vertex: {
            right if left == vertex else left
            for edge in INCIDENCE[vertex]
            for left, right in (PETERSEN_EDGES[edge],)
        }
        for vertex in VERTICES
    }
    cycles = set()

    def visit(path: tuple[int, ...]) -> None:
        if len(path) == len(VERTICES):
            if path[0] in adjacency[path[-1]]:
                forward = path
                reverse = (path[0],) + tuple(reversed(path[1:]))
                cycles.add(min(forward, reverse))
            return
        for neighbour in adjacency[path[-1]]:
            if neighbour not in path:
                visit(path + (neighbour,))

    visit((0,))
    return len(cycles)


def count_tait_colourings() -> int:
    colours = [-1] * len(PETERSEN_EDGES)
    count = 0

    def visit(edge: int) -> None:
        nonlocal count
        if edge == len(PETERSEN_EDGES):
            count += 1
            return
        left, right = PETERSEN_EDGES[edge]
        forbidden = {
            colours[item]
            for vertex in (left, right)
            for item in INCIDENCE[vertex]
            if colours[item] >= 0
        }
        for colour in range(3):
            if colour not in forbidden:
                colours[edge] = colour
                visit(edge + 1)
                colours[edge] = -1

    visit(0)
    return count


def local_fifth_recolour_audit() -> tuple[int, int]:
    # Half-edge positions 0,1 form one prescribed triangle transition, and
    # 2,3 the other.  A switched Euler-tour pairing is 0,2 and 1,3.
    prescribed = ((0, 1), (2, 3))
    switched = ((0, 2), (1, 3))
    bad_old_states = []
    repair_count = 0
    for old in product(range(4), repeat=4):
        if any(count % 2 for count in Counter(old).values()):
            continue
        if any(old[first] == old[second] for first, second in switched):
            continue
        if all(old[first] != old[second] for first, second in prescribed):
            continue
        bad_old_states.append(old)
        for mask in range(1 << 4):
            new = tuple(4 if (mask >> position) & 1 else old[position] for position in range(4))
            if any(count % 2 for count in Counter(new).values()):
                continue
            if all(new[first] != new[second] for first, second in prescribed):
                repair_count += 1
    return len(bad_old_states), repair_count


def main() -> None:
    assert all(len(row) == 3 for row in INCIDENCE)
    assert len(set(PETERSEN_EDGES)) == len(PETERSEN_EDGES)

    perfect_matchings = enumerate_perfect_matchings()
    complement_types = Counter(
        cycle_lengths(frozenset(range(len(PETERSEN_EDGES))) - frozenset(matching))
        for matching in perfect_matchings
    )
    hamiltonian_cycles = count_hamiltonian_cycles()
    tait_colourings = count_tait_colourings()

    d4_flows = enumerate_d_flows(4)
    d5_flows = enumerate_d_flows(5)
    assert not d4_flows
    assert d5_flows
    witness = d5_flows[0]
    validate_d_flow(witness, 5)
    line_colouring = d_flow_to_line_colouring(witness, 5)
    validate_line_colouring(line_colouring, 5)
    assert line_colouring_to_d_flow(line_colouring, 5) == witness

    bad_old_states, repair_count = local_fifth_recolour_audit()
    assert bad_old_states == 12
    assert repair_count == 0

    assert len(perfect_matchings) == 6
    assert complement_types == Counter({(5, 5): 6})
    assert hamiltonian_cycles == 0
    assert tait_colourings == 0

    print("Petersen graph: 10 vertices, 15 edges; line graph: 15 vertices, 30 edges")
    print(f"perfect matchings: {len(perfect_matchings)}")
    print(f"perfect-matching complement cycle types: {dict(complement_types)}")
    print(f"Hamiltonian cycles: {hamiltonian_cycles}")
    print(f"Tait colourings: {tait_colourings}")
    print(f"literal D4 flows: {len(d4_flows)}")
    print(f"literal D5 flows: {len(d5_flows)}")
    print(
        "D5 witness in PETERSEN_EDGES order:",
        [label_text(label, 5) for label in witness],
    )
    print("mapped line-graph colouring:", line_colouring)
    print(f"bad switched local four-colour states: {bad_old_states}")
    print(f"valid pure fifth-colour repairs: {repair_count}")
    print("PASS")


if __name__ == "__main__":
    main()
