#!/usr/bin/env python3
"""Independent exact verifier for the order-18 non-Tait BPR-gate blocker.

This file deliberately imports neither search program nor Z3.  Every finite
claim is reconstructed from the graph6 record and the frozen edge data using
only the Python standard library.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


GRAPH6 = "Q???C@?GCoOoDO[?CcAO_?k?J??"
FLOW = (6, 6, 6, 2, 3, 1, 4, 5, 1, 5, 2, 7, 3, 5, 6, 3, 7, 4, 5, 4, 1, 5, 2, 7, 5, 4, 1)
MATCHING_EDGES = (5, 8, 20, 26)
JOIN_EDGES = (4, 7, 10, 11, 12, 14, 18, 21, 23, 24)
Q_SHORE = frozenset((0, 7, 10, 11))
TARGET_VALUE = 1


def decode_graph6(record):
    n = ord(record[0]) - 63
    assert 0 <= n <= 62
    bits = tuple(
        (ord(character) - 63 >> shift) & 1
        for character in record[1:]
        for shift in range(5, -1, -1)
    )
    pairs = tuple((u, v) for v in range(1, n) for u in range(v))
    return n, tuple(pair for pair, bit in zip(pairs, bits) if bit)


N, EDGES = decode_graph6(GRAPH6)
M = len(EDGES)
FULL = (1 << M) - 1
ROWS = tuple(
    tuple(edge for edge, endpoints in enumerate(EDGES) if vertex in endpoints)
    for vertex in range(N)
)


def mask(indices):
    return sum(1 << index for index in indices)


MATCHING = mask(MATCHING_EDGES)
JOIN = mask(JOIN_EDGES)
ALTERNATE_ESCAPE_CYCLE = mask((0, 2, 6, 8, 9, 11, 13, 14, 21, 23))


def indices(edge_mask):
    return tuple(edge for edge in range(M) if (edge_mask >> edge) & 1)


def boundary(edge_mask):
    answer = 0
    for vertex, row in enumerate(ROWS):
        answer |= (sum((edge_mask >> edge) & 1 for edge in row) & 1) << vertex
    return answer


def components(allowed):
    unseen = set(range(N))
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        shore = {root}
        queue = [root]
        for vertex in queue:
            for edge in ROWS[vertex]:
                if not ((allowed >> edge) & 1):
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if other in unseen:
                    unseen.remove(other)
                    shore.add(other)
                    queue.append(other)
        answer.append(frozenset(shore))
    return tuple(answer)


def cut(shore, allowed=FULL):
    return sum(
        1 << edge
        for edge, (u, v) in enumerate(EDGES)
        if ((allowed >> edge) & 1) and ((u in shore) != (v in shore))
    )


def cycle_basis(allowed):
    parent = list(range(N))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    tree = []
    chords = []
    for edge, (u, v) in enumerate(EDGES):
        if not ((allowed >> edge) & 1):
            continue
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
    basis = []
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
        basis.append(vector)
    rank = allowed.bit_count() - N + len(components(allowed))
    assert len(basis) == rank
    assert all(boundary(vector) == 0 and not (vector & ~allowed) for vector in basis)
    return tuple(basis)


def span(basis):
    answer = [0]
    for vector in basis:
        answer += [old ^ vector for old in answer]
    assert len(answer) == 1 << len(basis) and len(set(answer)) == len(answer)
    return tuple(answer)


def one_join(allowed, target):
    parent = [-1] * N
    parent_edge = [-1] * N
    roots = []
    order = []
    for root in range(N):
        if parent[root] != -1:
            continue
        parent[root] = root
        roots.append(root)
        queue = [root]
        for vertex in queue:
            order.append(vertex)
            for edge in ROWS[vertex]:
                if not ((allowed >> edge) & 1):
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if parent[other] == -1:
                    parent[other] = vertex
                    parent_edge[other] = edge
                    queue.append(other)
    need = [(target >> vertex) & 1 for vertex in range(N)]
    answer = 0
    for vertex in reversed(order):
        if vertex == parent[vertex]:
            continue
        if need[vertex]:
            answer |= 1 << parent_edge[vertex]
            need[parent[vertex]] ^= 1
    assert not any(need[root] for root in roots)
    assert not (answer & ~allowed) and boundary(answer) == target
    return answer


def residual_data(matching, join):
    residual = FULL ^ (matching | join)
    return tuple((shore, cut(shore)) for shore in components(residual))


def potential(data, matching):
    tight = second = 0
    for _shore, component_cut in data:
        d = component_cut.bit_count()
        q = (component_cut & matching).bit_count()
        if q & 1:
            tight += d == 4
            second += d - q
    return tight, second


def has_cycle(vertex_mask):
    parent = list(range(N))

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in EDGES:
        if not ((vertex_mask >> u) & 1 and (vertex_mask >> v) & 1):
            continue
        ru, rv = root(u), root(v)
        if ru == rv:
            return True
        parent[rv] = ru
    return False


def graph_girth():
    best = M + 1
    for removed, (source, target) in enumerate(EDGES):
        distance = [-1] * N
        distance[source] = 0
        queue = [source]
        for vertex in queue:
            if vertex == target:
                break
            for edge in ROWS[vertex]:
                if edge == removed:
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if distance[other] == -1:
                    distance[other] = distance[vertex] + 1
                    queue.append(other)
        if distance[target] != -1:
            best = min(best, distance[target] + 1)
    return best


def perfect_matchings():
    neighbours = [[] for _ in range(N)]
    edge_of = {}
    for edge, (u, v) in enumerate(EDGES):
        neighbours[u].append(v)
        neighbours[v].append(u)
        edge_of[u, v] = edge_of[v, u] = edge

    def recurse(unmatched, selected):
        if not unmatched:
            yield selected
            return
        vertex = (unmatched & -unmatched).bit_length() - 1
        rest = unmatched ^ (1 << vertex)
        for other in neighbours[vertex]:
            if (rest >> other) & 1:
                yield from recurse(
                    rest ^ (1 << other), selected | (1 << edge_of[vertex, other])
                )

    yield from recurse((1 << N) - 1, 0)


def cycle_lengths(two_factor):
    unseen = set(range(N))
    lengths = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        count = 1
        previous = -1
        vertex = root
        while True:
            candidates = []
            for edge in ROWS[vertex]:
                if not ((two_factor >> edge) & 1):
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                if other != previous:
                    candidates.append(other)
            assert candidates
            other = candidates[0]
            if other == root:
                break
            assert other in unseen
            unseen.remove(other)
            count += 1
            previous, vertex = vertex, other
        lengths.append(count)
    return tuple(sorted(lengths))


def cut_space_shore(row, allowed):
    """Return W with row=delta_allowed(W), or None if the row is not a cut."""
    if row & ~allowed:
        return None
    values = [None] * N
    for root in range(N):
        if values[root] is not None:
            continue
        values[root] = 0
        queue = [root]
        for vertex in queue:
            for edge in ROWS[vertex]:
                if not ((allowed >> edge) & 1):
                    continue
                u, v = EDGES[edge]
                other = u ^ v ^ vertex
                wanted = values[vertex] ^ ((row >> edge) & 1)
                if values[other] is None:
                    values[other] = wanted
                    queue.append(other)
                elif values[other] != wanted:
                    return None
    shore = frozenset(vertex for vertex, value in enumerate(values) if value)
    assert cut(shore, allowed) == row
    return shore


def verify_graph():
    assert N == 18 and M == 27
    assert len(set(EDGES)) == M and all(u < v for u, v in EDGES)
    assert all(len(row) == 3 for row in ROWS)
    assert len(components(FULL)) == 1
    bridges = tuple(edge for edge in range(M) if len(components(FULL ^ (1 << edge))) > 1)
    assert not bridges
    girth = graph_girth()
    assert girth == 5

    cyclic_cut_counts = Counter()
    minimum_cyclic_cut = M + 1
    # Fix vertex 0 in the shore to quotient by complementation.
    for subset in range(1 << (N - 1)):
        shore_vertices = (subset << 1) | 1
        if shore_vertices == (1 << N) - 1:
            continue
        complement = ((1 << N) - 1) ^ shore_vertices
        if has_cycle(shore_vertices) and has_cycle(complement):
            size = cut(frozenset(v for v in range(N) if (shore_vertices >> v) & 1)).bit_count()
            cyclic_cut_counts[size] += 1
            minimum_cyclic_cut = min(minimum_cyclic_cut, size)
    assert minimum_cyclic_cut == 4

    factors = Counter()
    factor_records = []
    for matching in perfect_matchings():
        assert matching.bit_count() == N // 2 and boundary(matching) == (1 << N) - 1
        lengths = cycle_lengths(FULL ^ matching)
        factors[lengths] += 1
        factor_records.append((indices(matching), lengths))
        assert any(length & 1 for length in lengths)
    assert factors
    return girth, minimum_cyclic_cut, cyclic_cut_counts, factors, tuple(factor_records)


def verify_state():
    assert len(FLOW) == M and all(1 <= value <= 7 for value in FLOW)
    assert all(FLOW[a] ^ FLOW[b] ^ FLOW[c] == 0 for a, b, c in ROWS)
    assert MATCHING == mask(edge for edge, value in enumerate(FLOW) if value == TARGET_VALUE)
    assert not (MATCHING & JOIN)
    h = FULL ^ MATCHING
    target = boundary(MATCHING)
    assert not (JOIN & ~h) and boundary(JOIN) == target
    assert boundary(MATCHING | JOIN) == 0

    data = residual_data(MATCHING, JOIN)
    assert potential(data, MATCHING) == (0, 8)
    q_candidates = tuple(i for i, (shore, _row) in enumerate(data) if shore == Q_SHORE)
    assert len(q_candidates) == 1
    q_index = q_candidates[0]
    q_cut = data[q_index][1]
    assert ((q_cut & ~MATCHING).bit_count(), (q_cut & MATCHING).bit_count()) == (3, 3)

    base = one_join(h, target)
    all_joins = tuple(base ^ cycle for cycle in span(cycle_basis(h)))
    assert len(all_joins) == len(set(all_joins))
    records = tuple(
        (join, residual_data(MATCHING, join), potential(residual_data(MATCHING, join), MATCHING))
        for join in all_joins
    )
    values = Counter(value for _join, _data, value in records)
    optimum = min(values)
    assert optimum == (0, 8) and JOIN in all_joins
    optimal_records = tuple((join, join_data) for join, join_data, value in records if value == optimum)
    assert {indices(join) for join, _join_data in optimal_records} == {
        JOIN_EDGES,
        (2, 4, 7, 9, 11, 15, 16, 19, 25),
        (2, 4, 7, 10, 11, 13, 14, 19, 25),
    }
    return data, q_index, values, optimal_records


def verify_alternate_optimal_escapes(optimal_records):
    direction = 3
    p = mask(
        edge
        for edge, value in enumerate(FLOW)
        if value in (TARGET_VALUE, TARGET_VALUE ^ direction)
    )
    summaries = []
    for join, data in optimal_records:
        if join == JOIN:
            continue
        forbidden = mask(
            edge
            for edge, value in enumerate(FLOW)
            if value == direction
            or (value == (TARGET_VALUE ^ direction) and not ((join >> edge) & 1))
        )
        allowed = FULL ^ forbidden
        cycle = ALTERNATE_ESCAPE_CYCLE
        assert not (cycle & ~allowed) and boundary(cycle) == 0
        e4_rows = tuple(
            p & component_cut
            for _shore, component_cut in data
            if component_cut.bit_count() == 4
            and not ((component_cut & MATCHING).bit_count() & 1)
        )
        assert all(not ((cycle & row).bit_count() & 1) for row in e4_rows)
        new_matching = MATCHING ^ (cycle & p)
        assert potential(data, new_matching) == (0, 0)
        summaries.append((join, direction, cycle, new_matching))
    assert len(summaries) == 2
    return tuple(summaries)


def verify_directions(data, q_index, expected_directions):
    q_cut = data[q_index][1]
    h_cut = q_cut & ~MATCHING
    cut_values = tuple(FLOW[edge] for edge in indices(h_cut))
    support = set(cut_values)
    directions = tuple(sorted(value for value in support if (value ^ TARGET_VALUE) not in support))
    assert directions == expected_directions
    e4 = tuple(
        (index, shore, component_cut)
        for index, (shore, component_cut) in enumerate(data)
        if component_cut.bit_count() == 4
        and not ((component_cut & MATCHING).bit_count() & 1)
    )
    assert e4
    summaries = []
    for direction in directions:
        forbidden = mask(
            edge
            for edge, value in enumerate(FLOW)
            if value == direction
            or (value == (TARGET_VALUE ^ direction) and not ((JOIN >> edge) & 1))
        )
        allowed = FULL ^ forbidden
        p = mask(
            edge
            for edge, value in enumerate(FLOW)
            if value in (TARGET_VALUE, TARGET_VALUE ^ direction)
        ) & allowed
        a_q = p & q_cut
        protected_rows = tuple(p & component_cut for _index, _shore, component_cut in e4)
        basis = cycle_basis(allowed)
        cycles = span(basis)
        selected = tuple(cycle for cycle in cycles if (cycle & a_q).bit_count() & 1)
        feasible = tuple(
            cycle
            for cycle in selected
            if all(not ((cycle & row).bit_count() & 1) for row in protected_rows)
        )
        assert not feasible

        dual = None
        for subset in range(1 << len(protected_rows)):
            row = a_q
            chosen = []
            for index, protected in enumerate(protected_rows):
                if (subset >> index) & 1:
                    row ^= protected
                    chosen.append(index)
            shore = cut_space_shore(row, allowed)
            if shore is not None:
                dual = (tuple(chosen), shore, row)
                break
        assert dual is not None
        chosen, shore, row = dual
        assert row == cut(shore, allowed)
        summaries.append(
            {
                "direction": direction,
                "allowed": allowed,
                "dimension": len(basis),
                "cycle_count": len(cycles),
                "selected_count": len(selected),
                "feasible_count": len(feasible),
                "chosen_e4_rows": chosen,
                "dual_shore": shore,
                "dual_row": row,
                "a_q": a_q,
                "protected_rows": protected_rows,
            }
        )
    return e4, summaries


def main():
    girth, minimum_cyclic_cut, cyclic_cut_counts, factors, factor_records = verify_graph()
    data, q_index, join_values, optimal_records = verify_state()
    alternate_escapes = verify_alternate_optimal_escapes(optimal_records)
    odd_indices = tuple(
        index
        for index, (_shore, component_cut) in enumerate(data)
        if (component_cut & MATCHING).bit_count() & 1
    )
    assert odd_indices == (0, 1)
    expected = {0: (3, 5, 7), 1: (2, 5, 6)}
    direction_audits = tuple(
        (index,) + verify_directions(data, index, expected[index])
        for index in odd_indices
    )

    print("CERTIFIED order-18 non-Tait reduced-gate blocker")
    print(
        f"graph: n={N} m={M} connected simple cubic bridgeless girth={girth} "
        f"cyclic_connectivity={minimum_cyclic_cut}"
    )
    print(f"perfect_matchings={sum(factors.values())} two_factor_types={dict(sorted(factors.items()))}")
    for matching_edges, lengths in factor_records:
        print(f"perfect_matching={matching_edges} complement_cycles={lengths}")
    print(f"join_count={sum(join_values.values())} join_potentials={dict(sorted(join_values.items()))}")
    print("edges=" + ";".join(f"{edge}:{u}-{v}/f{FLOW[edge]}" for edge, (u, v) in enumerate(EDGES)))
    for index, (shore, component_cut) in enumerate(data):
        d = component_cut.bit_count()
        q = (component_cut & MATCHING).bit_count()
        print(f"component={index} shore={sorted(shore)} cut={indices(component_cut)} profile=({d-q},{q})")
    e4_indices = [index for index, _shore, _row in direction_audits[0][1]]
    print(f"odd_components={list(odd_indices)} E4_components={e4_indices}")
    for blocker_index, _e4, summaries in direction_audits:
        for item in summaries:
            print(
                f"blocker_component={blocker_index} direction={item['direction']} "
                f"L_edges={indices(item['allowed'])} "
                f"dim={item['dimension']} cycles={item['cycle_count']} "
                f"q_flips={item['selected_count']} feasible={item['feasible_count']} "
                f"dual_E4={item['chosen_e4_rows']} dual_shore={sorted(item['dual_shore'])} "
                f"aQ={indices(item['a_q'])} "
                f"E4rows={tuple(indices(row) for row in item['protected_rows'])} "
                f"dual_cut={indices(item['dual_row'])}"
            )
    for join, direction, cycle, new_matching in alternate_escapes:
        print(
            f"alternate_optimal_join={indices(join)} escape_direction={direction} "
            f"escape_cycle={indices(cycle)} new_matching={indices(new_matching)} "
            "new_potential=(0, 0)"
        )


if __name__ == "__main__":
    main()
