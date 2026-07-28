#!/usr/bin/env python3
"""Replay the D5 edge-contraction/Kempe audit on a Petersen contraction.

No external graph or SAT library is used.  The script checks:

* the displayed degree-four D5 flow and its bad 2+2 boundary split;
* invariance of the boundary-xor weight under every component Kempe switch;
* failure of every single generalized circuit switch to repair the witness;
* a displayed repair by two generalized circuit switches;
* the complete flow census on the contracted graph; and
* connectivity of that finite flow space under generalized circuit switches.

This audits a proof strategy.  It is not a FiveCDC counterexample checker.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations


LABELS = tuple(
    (1 << first) | (1 << second)
    for first, second in combinations(range(5), 2)
)
LABEL_SET = frozenset(LABELS)

# Petersen edge 01 has been contracted to vertex 0.  Original vertices
# 2,...,9 are relabelled 1,...,8.
EDGES = (
    (0, 1),  # h0: old 12, v-side
    (1, 2),  # h1: old 23
    (2, 3),  # h2: old 34
    (0, 3),  # h3: old 04, u-side
    (0, 4),  # h4: old 05, u-side
    (0, 5),  # h5: old 16, v-side
    (1, 6),  # h6: old 27
    (2, 7),  # h7: old 38
    (3, 8),  # h8: old 49
    (4, 6),  # h9: old 57
    (6, 8),  # h10: old 79
    (5, 8),  # h11: old 69
    (5, 7),  # h12: old 68
    (4, 7),  # h13: old 58
)
U_SIDE = (3, 4)
V_SIDE = (0, 5)
W = 0

WITNESS_TEXT = (
    "01",
    "02",
    "01",
    "03",
    "12",
    "23",
    "12",
    "12",
    "13",
    "02",
    "01",
    "03",
    "02",
    "01",
)


def parse_label(text: str) -> int:
    assert len(text) == 2 and text[0] != text[1]
    return (1 << int(text[0])) | (1 << int(text[1]))


WITNESS = tuple(parse_label(text) for text in WITNESS_TEXT)


def label_text(label: int) -> str:
    return "".join(str(i) for i in range(5) if (label >> i) & 1)


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(9)]
    for edge, (left, right) in enumerate(EDGES):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


INCIDENCE = incidence()


def validate_flow(state: tuple[int, ...]) -> None:
    assert len(state) == len(EDGES)
    assert all(label in LABEL_SET for label in state)
    for row in INCIDENCE:
        value = 0
        for edge in row:
            value ^= state[edge]
        assert value == 0


def boundary_xor(state: tuple[int, ...]) -> int:
    left = state[U_SIDE[0]] ^ state[U_SIDE[1]]
    right = state[V_SIDE[0]] ^ state[V_SIDE[1]]
    assert left == right
    return left


def active_edges(state: tuple[int, ...], pair: int) -> tuple[int, ...]:
    return tuple(
        edge
        for edge, label in enumerate(state)
        if (label & pair).bit_count() == 1
    )


def edge_components(edges: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    remaining = set(edges)
    answer = []
    while remaining:
        first = remaining.pop()
        component_edges = {first}
        component_vertices = set(EDGES[first])
        changed = True
        while changed:
            changed = False
            for edge in tuple(remaining):
                if component_vertices.intersection(EDGES[edge]):
                    remaining.remove(edge)
                    component_edges.add(edge)
                    component_vertices.update(EDGES[edge])
                    changed = True
        answer.append(tuple(sorted(component_edges)))
    return tuple(sorted(answer))


def even_edge_subsets(edges: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    answer = []
    for mask in range(1, 1 << len(edges)):
        parity = [0] * len(INCIDENCE)
        chosen = []
        for position, edge in enumerate(edges):
            if (mask >> position) & 1:
                chosen.append(edge)
                left, right = EDGES[edge]
                parity[left] ^= 1
                parity[right] ^= 1
        if not any(parity):
            answer.append(tuple(chosen))
    return tuple(answer)


EVEN_SUBSET_CACHE: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}


def switched(
    state: tuple[int, ...], pair: int, chosen: tuple[int, ...]
) -> tuple[int, ...]:
    active = frozenset(active_edges(state, pair))
    assert set(chosen) <= active
    answer = list(state)
    for edge in chosen:
        answer[edge] ^= pair
        assert answer[edge] in LABEL_SET
    result = tuple(answer)
    validate_flow(result)
    return result


def component_neighbours(state: tuple[int, ...]):
    for pair in LABELS:
        for component in edge_components(active_edges(state, pair)):
            yield switched(state, pair, component), pair, component


def circuit_neighbours(state: tuple[int, ...]):
    for pair in LABELS:
        active = active_edges(state, pair)
        if active not in EVEN_SUBSET_CACHE:
            EVEN_SUBSET_CACHE[active] = even_edge_subsets(active)
        for chosen in EVEN_SUBSET_CACHE[active]:
            yield switched(state, pair, chosen), pair, chosen


def enumerate_flows() -> tuple[tuple[int, ...], ...]:
    state = [0] * len(EDGES)
    answers: list[tuple[int, ...]] = []

    def assign(edge: int, label: int, changed: list[int]) -> bool:
        if state[edge]:
            return state[edge] == label
        if label not in LABEL_SET:
            return False
        state[edge] = label
        changed.append(edge)
        pending = list(EDGES[edge])
        while pending:
            vertex = pending.pop()
            row = INCIDENCE[vertex]
            unassigned = [item for item in row if not state[item]]
            if len(unassigned) > 1:
                continue
            total = 0
            for item in row:
                total ^= state[item]
            if not unassigned:
                if total:
                    return False
            else:
                if total not in LABEL_SET:
                    return False
                forced_edge = unassigned[0]
                state[forced_edge] = total
                changed.append(forced_edge)
                pending.extend(EDGES[forced_edge])
        return True

    def visit() -> None:
        try:
            edge = state.index(0)
        except ValueError:
            result = tuple(state)
            validate_flow(result)
            answers.append(result)
            return
        for label in LABELS:
            changed: list[int] = []
            if assign(edge, label, changed):
                visit()
            for changed_edge in reversed(changed):
                state[changed_edge] = 0

    visit()
    return tuple(answers)


def main() -> None:
    assert tuple(len(row) for row in INCIDENCE) == (4, 3, 3, 3, 3, 3, 3, 3, 3)
    validate_flow(WITNESS)
    initial_xor = boundary_xor(WITNESS)
    assert label_text(initial_xor) == "0123"
    assert initial_xor.bit_count() == 4

    component_moves = tuple(component_neighbours(WITNESS))
    assert component_moves
    assert all(
        boundary_xor(state).bit_count() == initial_xor.bit_count()
        for state, _pair, _component in component_moves
    )

    one_circuit_moves = tuple(circuit_neighbours(WITNESS))
    one_step_good = [
        (state, pair, chosen)
        for state, pair, chosen in one_circuit_moves
        if boundary_xor(state).bit_count() == 2
    ]
    assert not one_step_good

    # First switch: pair 04 on h0,h1,h2,h3.
    middle = switched(WITNESS, parse_label("04"), (0, 1, 2, 3))
    assert label_text(boundary_xor(middle)) == "1234"
    # Second switch: pair 24 on h0,h4,h6,h9.
    repaired = switched(middle, parse_label("24"), (0, 4, 6, 9))
    assert label_text(boundary_xor(repaired)) == "13"
    assert boundary_xor(repaired).bit_count() == 2

    flows = enumerate_flows()
    flow_set = set(flows)
    distribution = Counter(boundary_xor(state).bit_count() for state in flows)
    assert len(flow_set) == 14_700
    assert distribution == Counter({2: 6_000, 4: 5_400, 0: 3_300})

    # Full finite generalized-switch orbit census.
    seen = {WITNESS}
    queue = deque((WITNESS,))
    while queue:
        state = queue.popleft()
        for neighbour, _pair, _chosen in circuit_neighbours(state):
            assert neighbour in flow_set
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    assert seen == flow_set

    print("contracted Petersen graph: 9 vertices, 14 edges, degrees 4,3^8")
    print("witness labels:", list(WITNESS_TEXT))
    print(f"initial side xor: {label_text(initial_xor)} (weight {initial_xor.bit_count()})")
    print(f"component switches checked: {len(component_moves)}; all preserve weight")
    print(f"generalized one-circuit switches checked: {len(one_circuit_moves)}")
    print(f"one-circuit repairs: {len(one_step_good)}")
    print("two-switch route: 0123 --04--> 1234 --24--> 13")
    print(f"all literal D5 flows: {len(flow_set)}")
    print(f"side-xor weight distribution: {dict(sorted(distribution.items()))}")
    print(f"generalized circuit-switch orbit size: {len(seen)}")
    print("PASS")


if __name__ == "__main__":
    main()
