#!/usr/bin/env python3
"""Standard-library verification of the order-22 minimum-support example.

This file deliberately does not import NetworkX, NumPy, a SAT solver, or any
code from the main FiveCDC repository.
"""

from collections import deque
from itertools import combinations
import json


N = 22
GRAPH6 = "U??????_A?E?I?B@A_Os?GoBA?A@_C@O?D_??U??"
EDGES = [
    (0, 9), (1, 10), (2, 11), (3, 11), (2, 12), (4, 12),
    (4, 13), (5, 13), (11, 13), (3, 14), (5, 14), (12, 14),
    (3, 15), (4, 15), (6, 15), (2, 16), (6, 16), (7, 16),
    (0, 17), (1, 17), (6, 17), (1, 18), (8, 18), (9, 18),
    (0, 19), (8, 19), (10, 19), (5, 20), (7, 20), (8, 20),
    (7, 21), (9, 21), (10, 21),
]

SOURCE_P = 516851579
SOURCE_Q = 7175781286
SOURCE_VALUES = [
    5, 3, 6, 5, 1, 3, 1, 2, 3, 3, 1,
    2, 6, 2, 4, 7, 2, 5, 7, 1, 6, 2,
    1, 3, 2, 3, 1, 3, 1, 2, 4, 6, 2,
]
SOURCE_M = {14, 30}

SWITCH_EDGES = {2, 3, 12, 14, 15, 16}
SWITCH_MASK = sum(1 << e for e in SWITCH_EDGES)

TARGET_P = 516904823
TARGET_Q = SOURCE_Q
TARGET_VALUES = [
    5, 3, 7, 4, 1, 3, 1, 2, 3, 3, 1,
    2, 7, 2, 5, 6, 3, 5, 7, 1, 6, 2,
    1, 3, 2, 3, 1, 3, 1, 2, 4, 6, 2,
]
TARGET_M = {3, 30}

PACKING_CIRCUIT = {
    0, 1, 2, 7, 8, 9, 10, 12, 14, 15, 17, 18, 20,
    21, 22, 28, 29, 31, 32,
}
TARGET_JOIN_1 = {1, 7, 8, 9, 10, 21, 22, 28, 29, 32}
TARGET_JOIN_2 = {0, 2, 12, 14, 15, 17, 18, 20, 31}


def decode_graph6(text):
    """Decode the one-byte-order graph6 format used by this example."""
    data = [ord(c) - 63 for c in text.strip()]
    assert 0 <= data[0] <= 62
    n = data[0]
    bits = []
    for word in data[1:]:
        bits.extend((word >> shift) & 1 for shift in range(5, -1, -1))
    answer = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                answer.append((i, j))
            k += 1
    return n, answer


def adjacency(removed=frozenset(), only_vertices=None):
    allowed = set(range(N)) if only_vertices is None else set(only_vertices)
    adj = [[] for _ in range(N)]
    for i, (u, v) in enumerate(EDGES):
        if i not in removed and u in allowed and v in allowed:
            adj[u].append((v, i))
            adj[v].append((u, i))
    return adj


def connected_after_removing(removed):
    adj = adjacency(removed)
    seen = {0}
    todo = [0]
    while todo:
        u = todo.pop()
        for v, _ in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == N


def contains_cycle(vertices):
    vertices = set(vertices)
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in EDGES:
        if u not in vertices or v not in vertices:
            continue
        ru, rv = find(u), find(v)
        if ru == rv:
            return True
        parent[ru] = rv
    return False


def cut_edges(vertices, removed=frozenset()):
    vertices = set(vertices)
    return {
        i for i, (u, v) in enumerate(EDGES)
        if i not in removed and ((u in vertices) != (v in vertices))
    }


def girth():
    best = N + 1
    for forbidden, (start, goal) in enumerate(EDGES):
        adj = adjacency({forbidden})
        dist = [-1] * N
        dist[start] = 0
        todo = deque([start])
        while todo:
            u = todo.popleft()
            for v, _ in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    todo.append(v)
        assert dist[goal] >= 0
        best = min(best, dist[goal] + 1)
    return best


def is_even_mask(mask):
    parity = [0] * N
    for e, (u, v) in enumerate(EDGES):
        if (mask >> e) & 1:
            parity[u] ^= 1
            parity[v] ^= 1
    return not any(parity)


def cycle_space():
    """Construct all binary cycles from a fundamental cycle basis."""
    adj = adjacency()
    parent = [-1] * N
    parent_edge = [-1] * N
    tree_edges = set()
    todo = [0]
    parent[0] = 0
    while todo:
        u = todo.pop()
        for v, e in adj[u]:
            if parent[v] < 0:
                parent[v] = u
                parent_edge[v] = e
                tree_edges.add(e)
                todo.append(v)
    assert all(x >= 0 for x in parent)

    tree_adj = [[] for _ in range(N)]
    for e in tree_edges:
        u, v = EDGES[e]
        tree_adj[u].append((v, e))
        tree_adj[v].append((u, e))

    basis = []
    for chord, (start, goal) in enumerate(EDGES):
        if chord in tree_edges:
            continue
        prev = {start: (start, -1)}
        todo = deque([start])
        while goal not in prev:
            u = todo.popleft()
            for v, e in tree_adj[u]:
                if v not in prev:
                    prev[v] = (u, e)
                    todo.append(v)
        mask = 1 << chord
        v = goal
        while v != start:
            u, e = prev[v]
            mask ^= 1 << e
            v = u
        assert is_even_mask(mask)
        basis.append(mask)

    assert len(basis) == len(EDGES) - N + 1 == 12
    cycles = [0]
    for b in basis:
        cycles += [x ^ b for x in cycles]
    assert len(cycles) == 4096
    assert len(set(cycles)) == 4096
    assert all(is_even_mask(x) for x in cycles)
    return cycles


def exact_zero_mask(p, q):
    full = (1 << len(EDGES)) - 1
    return full ^ (p | q)


def flow_values_are_valid(values):
    if len(values) != len(EDGES) or not all(1 <= x <= 7 for x in values):
        return False
    sums = [0] * N
    for value, (u, v) in zip(values, EDGES):
        sums[u] ^= value
        sums[v] ^= value
    return not any(sums)


def exact_value_edges(values, value):
    return {e for e, x in enumerate(values) if x == value}


def terminals(matching):
    answer = set()
    for e in matching:
        u, v = EDGES[e]
        assert u not in answer and v not in answer
        answer.update((u, v))
    return answer


def odd_vertices(edge_set):
    parity = [0] * N
    for e in edge_set:
        u, v = EDGES[e]
        parity[u] ^= 1
        parity[v] ^= 1
    return {v for v, x in enumerate(parity) if x}


def component_terminal_counts(mask, terminal_set):
    active = set()
    adj = [[] for _ in range(N)]
    for e, (u, v) in enumerate(EDGES):
        if (mask >> e) & 1:
            active.update((u, v))
            adj[u].append(v)
            adj[v].append(u)
    assert all(len(adj[v]) == 2 for v in active)
    counts = []
    while active:
        start = next(iter(active))
        seen = {start}
        todo = [start]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        active -= seen
        counts.append(len(seen & terminal_set))
    return sorted(counts)


def packing_cycle_statistics(cycles, matching):
    t = terminals(matching)
    forbidden = sum(1 << e for e in matching)
    required = set()
    for v in t:
        required.update(
            e for e, (u, w) in enumerate(EDGES)
            if e not in matching and v in (u, w)
        )
    required_mask = sum(1 << e for e in required)
    candidates = 0
    good = 0
    profiles = {}
    for c in cycles:
        if c & forbidden:
            continue
        if c & required_mask != required_mask:
            continue
        candidates += 1
        profile = tuple(component_terminal_counts(c, t))
        profiles[profile] = profiles.get(profile, 0) + 1
        if all(x % 2 == 0 for x in profile):
            good += 1
    return candidates, good, profiles


def main():
    # Literal graph identity and basic premises.
    decoded_n, decoded_edges = decode_graph6(GRAPH6)
    assert decoded_n == N and decoded_edges == EDGES
    assert len(EDGES) == 33 and len(set(EDGES)) == 33
    assert all(u != v and 0 <= u < v < N for u, v in EDGES)
    degrees = [0] * N
    for u, v in EDGES:
        degrees[u] += 1
        degrees[v] += 1
    assert degrees == [3] * N
    assert connected_after_removing(set())
    assert all(connected_after_removing({e}) for e in range(33))
    assert all(
        connected_after_removing(set(pair))
        for pair in combinations(range(33), 2)
    )
    cyclic_shore = {2, 3, 4, 5, 11, 12, 13, 14, 15}
    assert cut_edges(cyclic_shore) == {14, 15, 27}
    assert contains_cycle(cyclic_shore)
    assert contains_cycle(set(range(N)) - cyclic_shore)
    assert girth() == 5

    cycles = cycle_space()
    cycle_set = set(cycles)
    assert SOURCE_P in cycle_set and SOURCE_Q in cycle_set
    assert TARGET_P in cycle_set and TARGET_Q in cycle_set

    # Exhaust every ordered F_2^2 flow: 4096^2 exact cases.
    full = (1 << len(EDGES)) - 1
    minimum = len(EDGES) + 1
    minimum_states = 0
    minimum_supports = set()
    for p in cycles:
        for q in cycles:
            z = full ^ (p | q)
            size = z.bit_count()
            if size < minimum:
                minimum = size
                minimum_states = 1
                minimum_supports = {z}
            elif size == minimum:
                minimum_states += 1
                minimum_supports.add(z)
    assert minimum == 2
    assert minimum_states == 19440
    assert len(minimum_supports) == 222
    assert sum(1 << e for e in SOURCE_M) in minimum_supports
    assert sum(1 << e for e in TARGET_M) in minimum_supports
    nonpacking_minimum_supports = 0
    for support_mask in minimum_supports:
        support = {
            e for e in range(len(EDGES)) if (support_mask >> e) & 1
        }
        _, packing_witnesses, _ = packing_cycle_statistics(cycles, support)
        nonpacking_minimum_supports += int(packing_witnesses == 0)
    assert nonpacking_minimum_supports == 11

    # Explicit nowhere-zero F_2^3 lifts and the neutral value-1 switch.
    assert flow_values_are_valid(SOURCE_VALUES)
    assert flow_values_are_valid(TARGET_VALUES)
    assert exact_value_edges(SOURCE_VALUES, 4) == SOURCE_M
    assert exact_value_edges(TARGET_VALUES, 4) == TARGET_M
    assert sum(((x & 1) << e) for e, x in enumerate(SOURCE_VALUES)) == SOURCE_P
    assert sum((((x >> 1) & 1) << e) for e, x in enumerate(SOURCE_VALUES)) == SOURCE_Q
    assert sum(((x & 1) << e) for e, x in enumerate(TARGET_VALUES)) == TARGET_P
    assert sum((((x >> 1) & 1) << e) for e, x in enumerate(TARGET_VALUES)) == TARGET_Q
    assert SWITCH_MASK in cycle_set
    assert SOURCE_P ^ SWITCH_MASK == TARGET_P
    assert SOURCE_Q == TARGET_Q
    assert all(
        TARGET_VALUES[e] == (SOURCE_VALUES[e] ^ (1 if e in SWITCH_EDGES else 0))
        for e in range(33)
    )

    # Direct, non-enumerative obstruction for SOURCE_M.
    source_t = terminals(SOURCE_M)
    assert source_t == {6, 7, 15, 21}
    k_removed = SOURCE_M
    # Any union C of two disjoint T-joins must contain both K-edges at
    # every degree-two terminal.  In particular it contains 16,17,20,28.
    for v, incident in {
        6: {16, 20}, 7: {17, 28}, 15: {12, 13}, 21: {31, 32}
    }.items():
        assert {
            e for e, edge in enumerate(EDGES)
            if e not in k_removed and v in edge
        } == incident
    # Evenness at vertex 16 then excludes edge 15.
    assert {
        e for e, edge in enumerate(EDGES) if 16 in edge
    } == {15, 16, 17}
    # Even cut parity on this shore, with 17 and 20 present, excludes 27.
    parity_shore = {2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16}
    assert cut_edges(parity_shore, k_removed) == {17, 20, 27}
    # But this is a T-cut of size two.  Each of two disjoint T-joins must
    # use one of its edges, forcing both 15 and 27 into their union.
    obstruction_shore = {2, 3, 4, 5, 11, 12, 13, 14, 15}
    assert len(obstruction_shore & source_t) == 1
    assert cut_edges(obstruction_shore, k_removed) == {15, 27}

    # Independently scan the complete cycle space using the equivalent
    # even-marked-circuit packing criterion.
    source_candidates, source_good, source_profiles = (
        packing_cycle_statistics(cycles, SOURCE_M)
    )
    assert source_candidates == 64
    assert source_good == 0
    assert source_profiles == {(1, 3): 48, (1, 1, 2): 16}

    # Literal positive co-minimizer: two disjoint T-joins.
    target_t = terminals(TARGET_M)
    assert target_t == {3, 7, 11, 21}
    assert TARGET_JOIN_1.isdisjoint(TARGET_JOIN_2)
    assert not ((TARGET_JOIN_1 | TARGET_JOIN_2) & TARGET_M)
    assert odd_vertices(TARGET_JOIN_1) == target_t
    assert odd_vertices(TARGET_JOIN_2) == target_t
    assert TARGET_JOIN_1 | TARGET_JOIN_2 == PACKING_CIRCUIT
    packing_mask = sum(1 << e for e in PACKING_CIRCUIT)
    assert packing_mask in cycle_set
    assert component_terminal_counts(packing_mask, target_t) == [4]

    report = {
        "status": "PASS",
        "classification": (
            "EVERY GLOBAL MINIMIZER PACKS IS FALSE; "
            "A PACKING GLOBAL CO-MINIMIZER EXISTS"
        ),
        "graph": {
            "graph6": GRAPH6,
            "vertices": N,
            "edges": len(EDGES),
            "simple": True,
            "cubic": True,
            "bridgeless": True,
            "edge_connectivity": 3,
            "cyclic_edge_connectivity": 3,
            "girth": 5,
        },
        "global_minimum": {
            "exact_zero_size": minimum,
            "ordered_F2_2_states": minimum_states,
            "distinct_supports": len(minimum_supports),
            "nonpacking_supports": nonpacking_minimum_supports,
        },
        "nonpacking_minimizer": {
            "support": sorted(SOURCE_M),
            "terminals": sorted(source_t),
            "complete_candidate_cycle_count": source_candidates,
            "packing_candidate_count": source_good,
            "component_terminal_profiles": {
                ",".join(map(str, key)): value
                for key, value in sorted(source_profiles.items())
            },
        },
        "neutral_switch": {
            "value": 1,
            "edges": sorted(SWITCH_EDGES),
            "target_support": sorted(TARGET_M),
        },
        "packing_cominimizer": {
            "support": sorted(TARGET_M),
            "terminals": sorted(target_t),
            "join_1": sorted(TARGET_JOIN_1),
            "join_2": sorted(TARGET_JOIN_2),
        },
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
