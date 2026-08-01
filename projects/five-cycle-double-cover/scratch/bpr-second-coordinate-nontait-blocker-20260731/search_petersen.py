#!/usr/bin/env python3
"""Exhaust Petersen Fano flows and optimal first joins for refined blockers."""

from __future__ import annotations

from functools import lru_cache
from collections import Counter
from itertools import combinations, product


N = 10
EDGES = (
    (0, 1), (0, 4), (0, 5), (1, 2), (1, 6),
    (2, 3), (2, 7), (3, 4), (3, 8), (4, 9),
    (5, 7), (5, 8), (6, 8), (6, 9), (7, 9),
)
M = len(EDGES)


def incidence():
    answer = [[] for _ in range(N)]
    for edge, (u, v) in enumerate(EDGES):
        answer[u].append(edge)
        answer[v].append(edge)
    return tuple(tuple(row) for row in answer)


ROWS = incidence()


def components(allowed_mask):
    unseen = set(range(N))
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        shore = {root}
        queue = [root]
        for vertex in queue:
            for edge in ROWS[vertex]:
                if not ((allowed_mask >> edge) & 1):
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    shore.add(other)
                    queue.append(other)
        answer.append(frozenset(shore))
    return tuple(answer)


def cut_mask(shore):
    return sum(
        1 << edge
        for edge, (u, v) in enumerate(EDGES)
        if (u in shore) != (v in shore)
    )


def boundary(mask):
    return sum(
        (sum((mask >> edge) & 1 for edge in ROWS[vertex]) & 1) << vertex
        for vertex in range(N)
    )


def cycle_basis(allowed_mask):
    parent = list(range(N))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree, chords = [], []
    for edge in range(M):
        if not ((allowed_mask >> edge) & 1):
            continue
        u, v = EDGES[edge]
        ru, rv = root(u), root(v)
        if ru == rv:
            chords.append(edge)
        else:
            parent[rv] = ru
            tree.append(edge)
    tree_rows = [[] for _ in range(N)]
    for edge in tree:
        u, v = EDGES[edge]
        tree_rows[u].append(edge)
        tree_rows[v].append(edge)
    result = []
    for chord in chords:
        source, target = EDGES[chord]
        previous = {source: (-1, -1)}
        queue = [source]
        for vertex in queue:
            if target in previous:
                break
            for edge in tree_rows[vertex]:
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if other not in previous:
                    previous[other] = (vertex, edge)
                    queue.append(other)
        vector = 1 << chord
        vertex = target
        while vertex != source:
            vertex, edge = previous[vertex]
            vector ^= 1 << edge
        result.append(vector)
    assert len(result) == allowed_mask.bit_count() - N + len(components(allowed_mask))
    return tuple(result)


def span(basis):
    values = [0]
    for vector in basis:
        values += [old ^ vector for old in values]
    return tuple(values)


FULL_CYCLES = span(cycle_basis((1 << M) - 1))


@lru_cache(maxsize=None)
def joins_and_optimum(matching):
    allowed = ((1 << M) - 1) ^ matching
    target_boundary = boundary(matching)
    base = None
    sub = allowed
    while True:
        if boundary(sub) == target_boundary:
            base = sub
            break
        if sub == 0:
            break
        sub = (sub - 1) & allowed
    assert base is not None
    joins = tuple(base ^ cycle for cycle in span(cycle_basis(allowed)))
    assert len(set(joins)) == len(joins)
    records = []
    for join in joins:
        assert not (join & matching) and boundary(join) == target_boundary
        residual = ((1 << M) - 1) ^ (matching | join)
        data = tuple((shore, cut_mask(shore)) for shore in components(residual))
        value = potential(data, matching)
        records.append((value, join, data))
    optimum = min(record[0] for record in records)
    return optimum, tuple(record for record in records if record[0] == optimum)


def potential(component_data, target_mask):
    tight = second = 0
    for _shore, component_cut in component_data:
        q = (component_cut & target_mask).bit_count()
        d = component_cut.bit_count()
        if q & 1:
            tight += d == 4
            second += d - q
    return tight, second


def partner_free(values, b=1):
    support = set(values)
    return tuple(sorted(value for value in support if (value ^ b) not in support))


def analyze_direction(flow, matching, join, data, q_index, t):
    b = 1
    q_shore, q_cut = data[q_index]
    e4 = tuple(
        component_cut
        for _shore, component_cut in data
        if component_cut.bit_count() == 4
        and not ((component_cut & matching).bit_count() & 1)
    )
    forbidden = sum(
        1 << edge
        for edge, value in enumerate(flow)
        if value == t or (value == (b ^ t) and not ((join >> edge) & 1))
    )
    allowed = ((1 << M) - 1) ^ forbidden
    p_mask = sum(1 << edge for edge, value in enumerate(flow) if value in (b, b ^ t))
    basis = cycle_basis(allowed)
    cycles = span(basis)
    selected_functional_nonzero = any(((cycle & p_mask & q_cut).bit_count() & 1) for cycle in cycles)
    feasible = []
    for cycle in cycles:
        if not ((cycle & p_mask & q_cut).bit_count() & 1):
            continue
        if any((cycle & p_mask & component_cut).bit_count() & 1 for component_cut in e4):
            continue
        target = matching
        for edge, value in enumerate(flow):
            if not ((cycle >> edge) & 1):
                continue
            if value == b:
                target ^= 1 << edge
            elif value == (b ^ t):
                target ^= 1 << edge
        feasible.append((potential(data, target), cycle))
    best = min(feasible, default=None)
    return len(basis), selected_functional_nonzero, len(feasible), best


def flow_words():
    for first, second, third in product(FULL_CYCLES, repeat=3):
        values = tuple(
            ((first >> edge) & 1)
            | (((second >> edge) & 1) << 1)
            | (((third >> edge) & 1) << 2)
            for edge in range(M)
        )
        if all(values):
            yield values


def main():
    assert all(len(row) == 3 for row in ROWS)
    checked_flows = optimal_larger_states = 0
    distinct_flows = set()
    matching_optima = {}
    flow_optima = Counter()
    for flow in flow_words():
        if flow in distinct_flows:
            continue
        distinct_flows.add(flow)
        checked_flows += 1
        matching = sum(1 << edge for edge, value in enumerate(flow) if value == 1)
        optimum, records = joins_and_optimum(matching)
        matching_optima[matching] = optimum
        flow_optima[optimum] += 1
        if optimum[0] != 0 or optimum[1] == 0:
            continue
        for _value, join, data in records:
            optimal_larger_states += 1
            odd_indices = tuple(
                index
                for index, (_shore, component_cut) in enumerate(data)
                if (component_cut & matching).bit_count() & 1
            )
            for q_index in odd_indices:
                q_cut = data[q_index][1]
                h_cut = q_cut & ~matching
                k = h_cut.bit_count()
                q = (q_cut & matching).bit_count()
                if k >= 9:
                    continue
                values = tuple(flow[edge] for edge in range(M) if (h_cut >> edge) & 1)
                directions = partner_free(values)
                direction_data = tuple(
                    (t,) + analyze_direction(flow, matching, join, data, q_index, t)
                    for t in directions
                )
                if direction_data and all(row[3] == 0 or row[4][0] >= optimum for row in direction_data):
                    print("FOUND")
                    print(f"flows_checked={checked_flows} optimal_larger_states={optimal_larger_states}")
                    print("flow=" + ",".join(map(str, flow)))
                    print("matching=" + ",".join(map(str, [e for e in range(M) if (matching >> e) & 1])))
                    print("join=" + ",".join(map(str, [e for e in range(M) if (join >> e) & 1])))
                    print(f"optimum={optimum} Q={q_index} profile=({k},{q}) shore={sorted(data[q_index][0])}")
                    for row in direction_data:
                        print(f"direction t={row[0]} dim={row[1]} selected_nonzero={int(row[2])} feasible={row[3]} best={row[4]}")
                    return
    print(
        f"NO_BLOCKER flows={checked_flows} distinct_target_classes={len(matching_optima)} "
        f"optimal_larger_states={optimal_larger_states}"
    )
    print(f"flow_optima={dict(sorted(flow_optima.items()))}")
    print(
        "target_class_optima="
        + str(dict(sorted(Counter(matching_optima.values()).items())))
    )


if __name__ == "__main__":
    main()
