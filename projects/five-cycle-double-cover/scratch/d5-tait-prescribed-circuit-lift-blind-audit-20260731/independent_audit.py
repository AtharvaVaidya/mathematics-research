#!/usr/bin/env python3
"""Edge-ID audit of the prescribed-circuit Tait construction."""

from __future__ import annotations

from itertools import combinations


Edge = tuple[int, int]


def incidence(order: int, edges: list[Edge]) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    for eid, (u, v) in enumerate(edges):
        assert u != v, "the audited theorem is loopless"
        rows[u].append(eid)
        rows[v].append(eid)
    assert all(len(row) == 3 for row in rows)
    return rows


def is_circuit(order: int, edges: list[Edge], chosen: frozenset[int]) -> bool:
    if not chosen:
        return False
    degree = [0] * order
    adjacency = [[] for _ in range(order)]
    for eid in chosen:
        u, v = edges[eid]
        degree[u] += 1
        degree[v] += 1
        adjacency[u].append(v)
        adjacency[v].append(u)
    support = {v for v, d in enumerate(degree) if d}
    if any(degree[v] != 2 for v in support):
        return False
    seen = set()
    stack = [next(iter(support))]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(w for w in adjacency[v] if w not in seen)
    return seen == support


def circuits(order: int, edges: list[Edge]) -> list[frozenset[int]]:
    return [
        frozenset(eid for eid in range(len(edges)) if mask >> eid & 1)
        for mask in range(1, 1 << len(edges))
        if is_circuit(
            order,
            edges,
            frozenset(eid for eid in range(len(edges)) if mask >> eid & 1),
        )
    ]


def prescribed_labels(colours: list[int], circuit: frozenset[int]) -> list[int]:
    universe = sum(1 << c for c in (2, 3, 4))
    return [
        (1 << 0) | (1 << colour) if eid in circuit else universe ^ (1 << colour)
        for eid, colour in enumerate(colours)
    ]


def check_colouring(order: int, edges: list[Edge], colours: list[int]) -> None:
    assert len(edges) == len(colours)
    for row in incidence(order, edges):
        assert {colours[eid] for eid in row} == {2, 3, 4}


def check_flow(
    order: int,
    edges: list[Edge],
    labels: list[int],
    expected_factor: frozenset[int] | None = None,
) -> None:
    assert len(edges) == len(labels)
    assert all(label.bit_count() == 2 for label in labels)
    rows = incidence(order, edges)
    for row in rows:
        value = 0
        for eid in row:
            value ^= labels[eid]
        assert value == 0

    coordinate_sets = [
        {eid for eid, label in enumerate(labels) if label >> coordinate & 1}
        for coordinate in range(5)
    ]
    for chosen in coordinate_sets:
        for row in rows:
            assert sum(eid in chosen for eid in row) % 2 == 0
    for eid in range(len(edges)):
        assert sum(eid in chosen for chosen in coordinate_sets) == 2

    if expected_factor is not None:
        active = frozenset(
            eid
            for eid, label in enumerate(labels)
            if ((label >> 0) & 1) ^ ((label >> 1) & 1)
        )
        assert active == expected_factor


def insert_and_check(
    order: int,
    edges: list[Edge],
    labels: list[int],
    circuit: frozenset[int],
    roots: tuple[int, int],
) -> None:
    assert roots[0] != roots[1]
    assert set(roots) <= circuit
    new_edges = list(edges)
    new_labels = list(labels)
    new_circuit = set(circuit) - set(roots)
    subdividers: list[int] = []

    for root in roots:
        u, v = new_edges[root]
        w = order + len(subdividers)
        subdividers.append(w)
        new_edges[root] = (u, w)
        second_half = len(new_edges)
        new_edges.append((w, v))
        new_labels.append(new_labels[root])
        new_circuit.update((root, second_half))

    central = len(new_edges)
    new_edges.append((subdividers[0], subdividers[1]))
    new_labels.append(0b00011)

    rows = incidence(order + 2, new_edges)
    start, finish = subdividers
    previous = None
    vertex = start
    arc: list[int] = []
    while vertex != finish:
        choices = [eid for eid in rows[vertex] if eid in new_circuit and eid != previous]
        assert len(choices) == (2 if previous is None else 1)
        eid = min(choices)
        arc.append(eid)
        u, v = new_edges[eid]
        vertex = v if vertex == u else u
        previous = eid
        assert len(arc) <= len(new_circuit)

    for eid in arc:
        assert ((new_labels[eid] >> 0) & 1) ^ ((new_labels[eid] >> 1) & 1)
        new_labels[eid] ^= 0b00011

    check_flow(order + 2, new_edges, new_labels, frozenset(new_circuit))
    assert new_labels[central] == 0b00011


def audit_graph(
    order: int, edges: list[Edge], colours: list[int], require_all_pairs: bool
) -> tuple[int, int]:
    check_colouring(order, edges, colours)
    graph_circuits = circuits(order, edges)
    formula_checks = insertion_checks = 0
    for circuit in graph_circuits:
        labels = prescribed_labels(colours, circuit)
        check_flow(order, edges, labels, circuit)
        formula_checks += 1
        for roots in combinations(sorted(circuit), 2):
            insert_and_check(order, edges, labels, circuit, roots)
            insertion_checks += 1

    if require_all_pairs:
        for roots in combinations(range(len(edges)), 2):
            witnesses = [circuit for circuit in graph_circuits if set(roots) <= circuit]
            assert witnesses, roots
            labels = prescribed_labels(colours, witnesses[0])
            check_flow(order, edges, labels, witnesses[0])
            insert_and_check(order, edges, labels, witnesses[0], roots)
            insertion_checks += 1
    return formula_checks, insertion_checks


def main() -> None:
    # K4 with its standard 1-factorization.
    k4_edges = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]
    k4_colours = [2, 2, 3, 3, 4, 4]

    # The cubic two-vertex multigraph.  Every pair of edges is a 2-circuit.
    theta_edges = [(0, 1), (0, 1), (0, 1)]
    theta_colours = [2, 3, 4]

    formula = insertion = 0
    for graph in (
        (4, k4_edges, k4_colours, True),
        (2, theta_edges, theta_colours, True),
    ):
        f_count, i_count = audit_graph(*graph)
        formula += f_count
        insertion += i_count

    # Disconnected control: the theorem is local and does not need H connected.
    disconnected_edges = theta_edges + [(2, 3), (2, 3), (2, 3)]
    disconnected_colours = theta_colours + theta_colours
    chosen = frozenset((0, 1))
    check_colouring(4, disconnected_edges, disconnected_colours)
    labels = prescribed_labels(disconnected_colours, chosen)
    check_flow(4, disconnected_edges, labels, chosen)
    formula += 1

    print(
        "PASS: blind edge-ID audit; "
        f"formula_circuits={formula}; insertions={insertion}; "
        "parallel_digons=checked; disconnected_control=checked"
    )


if __name__ == "__main__":
    main()
