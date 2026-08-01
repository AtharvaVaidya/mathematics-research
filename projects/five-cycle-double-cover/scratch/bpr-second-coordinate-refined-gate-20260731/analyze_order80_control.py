#!/usr/bin/env python3
"""Exact reduced-gate analysis of the frozen girth-10 cyclically-4 control."""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
STATE = HERE.parent / "order80-girth10-binary-repair-state.txt"
TAIT_STATE = HERE.parent / "order80-girth10-tait-flow-state.txt"
JOIN = frozenset(
    (0, 2, 4, 8, 13, 17, 21, 28, 32, 39, 45, 47, 48, 50, 52, 53,
     56, 57, 59, 67, 72, 73, 76, 77, 78, 82, 83, 90, 93, 98, 101,
     105, 113, 114)
)


def decode_graph6(record):
    assert record[0] == "~" and record[1] != "~"
    order = 0
    for character in record[1:4]:
        order = (order << 6) | (ord(character) - 63)
    payload = []
    for character in record[4:]:
        value = ord(character) - 63
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = tuple((u, v) for v in range(1, order) for u in range(v))
    assert not any(payload[len(pairs):])
    return order, tuple(pair for pair, bit in zip(pairs, payload) if bit)


def rows(order, edges):
    answer = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        answer[u].append(edge)
        answer[v].append(edge)
    return tuple(tuple(row) for row in answer)


def graph_girth(order, edges, graph_rows):
    best = order + 1
    for forbidden, (source, target) in enumerate(edges):
        distance = [-1] * order
        distance[source] = 0
        queue = deque((source,))
        while queue:
            vertex = queue.popleft()
            for edge in graph_rows[vertex]:
                if edge == forbidden:
                    continue
                u, v = edges[edge]
                other = u ^ v ^ vertex
                if distance[other] < 0:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        assert distance[target] >= 0
        best = min(best, distance[target] + 1)
    return best


def cyclic_component_count(order, edges, graph_rows, deleted):
    unseen = set(range(order))
    cyclic = 0
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        shore = {root}
        queue = [root]
        edge_ends = 0
        for vertex in queue:
            for edge in graph_rows[vertex]:
                if edge in deleted:
                    continue
                edge_ends += 1
                u, v = edges[edge]
                other = u ^ v ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    shore.add(other)
                    queue.append(other)
        cyclic += edge_ends // 2 >= len(shore)
    return cyclic


def cyclic_cut_counts(order, edges, graph_rows):
    result = {}
    for size in range(1, 4):
        result[size] = sum(
            cyclic_component_count(order, edges, graph_rows, frozenset(deleted)) >= 2
            for deleted in combinations(range(len(edges)), size)
        )
    return result


def components(order, edges, allowed):
    graph_rows = rows(order, edges)
    unseen = set(range(order))
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        shore = {root}
        queue = [root]
        for vertex in queue:
            for edge in graph_rows[vertex]:
                if edge not in allowed:
                    continue
                u, v = edges[edge]
                other = u ^ v ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    shore.add(other)
                    queue.append(other)
        answer.append(frozenset(shore))
    return tuple(answer)


def cut(edges, shore):
    return frozenset(
        edge for edge, (u, v) in enumerate(edges) if (u in shore) != (v in shore)
    )


def cycle_basis(order, edges, allowed):
    """Fundamental-cycle basis as global edge bitsets."""
    parent = list(range(order))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree_edges = []
    chords = []
    for edge in sorted(allowed):
        u, v = edges[edge]
        ru, rv = root(u), root(v)
        if ru != rv:
            parent[rv] = ru
            tree_edges.append(edge)
        else:
            chords.append(edge)

    tree_rows = [[] for _ in range(order)]
    for edge in tree_edges:
        u, v = edges[edge]
        tree_rows[u].append(edge)
        tree_rows[v].append(edge)

    basis = []
    for chord in chords:
        source, target = edges[chord]
        previous = {source: (-1, -1)}
        queue = deque((source,))
        while queue and target not in previous:
            vertex = queue.popleft()
            for edge in tree_rows[vertex]:
                u, v = edges[edge]
                other = u ^ v ^ vertex
                if other not in previous:
                    previous[other] = (vertex, edge)
                    queue.append(other)
        assert target in previous
        vector = 1 << chord
        vertex = target
        while vertex != source:
            vertex, edge = previous[vertex]
            vector ^= 1 << edge
        basis.append(vector)
    component_count = len(components(order, edges, allowed))
    assert len(basis) == len(allowed) - order + component_count
    return tuple(basis)


def row_on_basis(edge_set, basis):
    mask = sum(1 << edge for edge in edge_set)
    return sum(
        (((mask & cycle).bit_count() & 1) << position)
        for position, cycle in enumerate(basis)
    )


def span_cycle(coordinates, basis):
    answer = 0
    for position, cycle in enumerate(basis):
        if (coordinates >> position) & 1:
            answer ^= cycle
    return answer


def partner_free(values, b):
    support = set(values)
    return tuple(sorted(value for value in support if (value ^ b) not in support))


def dual_obstruction(selected_row, protected_rows):
    for subset in range(1 << len(protected_rows)):
        value = selected_row
        for index, row in enumerate(protected_rows):
            if (subset >> index) & 1:
                value ^= row
        if value == 0:
            return tuple(index for index in range(len(protected_rows)) if (subset >> index) & 1)
    return None


def potential(component_data, target_set):
    tight = second = 0
    for _shore, component_cut in component_data:
        q = len(component_cut & target_set)
        d = len(component_cut)
        if q & 1:
            tight += d == 4
            second += d - q
    return tight, second


def main():
    lines = STATE.read_text().splitlines()
    order, edges = decode_graph6(lines[0])
    flow = tuple(map(int, lines[1].split(",")))
    graph_rows = rows(order, edges)
    assert order == 80 and len(edges) == len(flow) == 120
    assert len(set(edges)) == len(edges)
    assert all(u != v for u, v in edges)
    assert all(len(row) == 3 for row in graph_rows)
    assert all(flow[row[0]] ^ flow[row[1]] ^ flow[row[2]] == 0 for row in graph_rows)
    assert graph_girth(order, edges, graph_rows) == 10
    cut_counts = cyclic_cut_counts(order, edges, graph_rows)
    assert cut_counts == {1: 0, 2: 0, 3: 0}

    tait_lines = TAIT_STATE.read_text().splitlines()
    tait_order, tait_edges = decode_graph6(tait_lines[0])
    tait_values = tuple(map(int, tait_lines[1].split(",")))
    assert (tait_order, tait_edges) == (order, edges)
    assert set(tait_values) == {1, 2, 3}
    assert all(
        {tait_values[edge] for edge in row} == {1, 2, 3}
        for row in graph_rows
    )

    b = 1
    matching = frozenset(edge for edge, value in enumerate(flow) if value == b)
    h_edges = frozenset(range(len(edges))) - matching
    residual_edges = h_edges - JOIN
    shores = components(order, edges, residual_edges)
    component_data = tuple((shore, cut(edges, shore)) for shore in shores)
    old_potential = potential(component_data, matching)
    assert old_potential == (0, 44)

    old_even_four = tuple(
        (shore, component_cut)
        for shore, component_cut in component_data
        if len(component_cut) == 4 and not (len(component_cut & matching) & 1)
    )
    odd_components = tuple(
        (shore, component_cut)
        for shore, component_cut in component_data
        if len(component_cut & matching) & 1
    )
    print(
        f"graph order={order} edges={len(edges)} simple=1 cubic=1 girth=10 "
        f"cyclic_cut_counts={cut_counts} tait=1 old_potential={old_potential} "
        f"residual_components={len(component_data)} protected_even_d4={len(old_even_four)}"
    )

    direction_rows = []
    for q_index, (shore, q_cut) in enumerate(odd_components):
        h_cut = q_cut & h_edges
        values = tuple(flow[edge] for edge in h_cut)
        k = len(h_cut)
        q = len(q_cut & matching)
        if k >= 9:
            continue
        directions = partner_free(values, b)
        assert directions
        for t in directions:
            forbidden = frozenset(
                edge
                for edge, value in enumerate(flow)
                if value == t or (value == (b ^ t) and edge not in JOIN)
            )
            allowed = frozenset(range(len(edges))) - forbidden
            basis = cycle_basis(order, edges, allowed)
            p_edges = frozenset(
                edge for edge, value in enumerate(flow) if value in (b, b ^ t)
            )
            selected_row = row_on_basis(p_edges & q_cut & allowed, basis)
            protected_rows = tuple(
                row_on_basis(p_edges & component_cut & allowed, basis)
                for _component, component_cut in old_even_four
            )
            dual = dual_obstruction(selected_row, protected_rows)
            selected_only = selected_row != 0
            feasible = best = None
            feasible_count = 0
            best_coordinates = None
            if selected_only:
                for coordinates in range(1 << len(basis)):
                    if not ((selected_row & coordinates).bit_count() & 1):
                        continue
                    if any((row & coordinates).bit_count() & 1 for row in protected_rows):
                        continue
                    feasible_count += 1
                    cycle = span_cycle(coordinates, basis)
                    target = set(matching)
                    for edge, value in enumerate(flow):
                        if not ((cycle >> edge) & 1):
                            continue
                        if value == b:
                            target.remove(edge)
                        elif value == (b ^ t):
                            target.add(edge)
                    candidate = potential(component_data, frozenset(target))
                    if best is None or candidate < best:
                        best = candidate
                        best_coordinates = coordinates
                feasible = feasible_count > 0
            assert feasible_count > 0 if dual is None else feasible_count == 0
            if feasible:
                assert best is not None and best_coordinates is not None
            direction_rows.append((q_index, k, q, t, len(basis), selected_only, feasible_count, best, dual))
            print(
                f"Q={q_index} profile=({k},{q}) t={t} dim={len(basis)} "
                f"selected_nonzero={int(selected_only)} protected_feasible={feasible_count} "
                f"dual={dual} best={best}"
            )

    assert direction_rows
    obstructed = sum(not row[5] for row in direction_rows)
    parity_feasible = sum(row[6] > 0 for row in direction_rows)
    descending = sum(row[7] is not None and row[7] < old_potential for row in direction_rows)
    print(
        f"directions={len(direction_rows)} selected_only_obstructed={obstructed} "
        f"reduced_parity_feasible={parity_feasible} descending={descending}"
    )


if __name__ == "__main__":
    main()
