#!/usr/bin/env python3
"""Focused exact audit of the twelve strict order-14 delimiters.

This reuses the frozen all-flow/Kempe engine from the typed-cap package, but
implements complement circuits, full fixed-coordinate cycle spaces, and the
depth-two search here.  Solver answers are not used.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TYPED = HERE.parent / "d5-typed-cap-orbit-external-frontier-20260731"
sys.path.insert(0, str(TYPED))
import verify as base  # noqa: E402


GRAPH_ROWS = (
    "M??CB?X[E_P_H_B_?",
    "M?AACGohBAJ?AgE_?",
)
METADATA = {
    "M??CB?X[E_P_H_B_?": (4, True, 3, True),
    "M?AACGohBAJ?AgE_?": (3, False, 2, True),
}


def simple_cycles(n, edges, allowed):
    adjacency = [[] for _ in range(n)]
    for edge in allowed:
        left, right = edges[edge]
        adjacency[left].append((right, edge))
        adjacency[right].append((left, edge))
    answer = set()
    for start in range(n):
        stack = [(start, -1, (start,), ())]
        while stack:
            vertex, parent_edge, vertices, path = stack.pop()
            for following, edge in adjacency[vertex]:
                if edge == parent_edge:
                    continue
                if following == start and len(path) >= 2:
                    answer.add(tuple(sorted(path + (edge,))))
                elif following > start and following not in vertices:
                    stack.append((following, edge, vertices + (following,), path + (edge,)))
    return tuple(sorted(answer, key=lambda row: (len(row), row)))


def cycle_space(n, edges, allowed):
    parent = list(range(n))
    tree = [[] for _ in range(n)]
    chords = []

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for edge in allowed:
        left, right = edges[edge]
        first, second = find(left), find(right)
        if first != second:
            parent[first] = second
            tree[left].append((right, edge))
            tree[right].append((left, edge))
        else:
            chords.append(edge)

    basis = []
    for chord in chords:
        left, right = edges[chord]
        stack = [(left, 0)]
        seen = {left}
        while stack:
            vertex, mask = stack.pop()
            if vertex == right:
                basis.append(mask | (1 << chord))
                break
            for following, edge in tree[vertex]:
                if following not in seen:
                    seen.add(following)
                    stack.append((following, mask | (1 << edge)))
        else:
            raise AssertionError("forest path absent")

    supports = [0]
    for vector in basis:
        supports += [mask ^ vector for mask in supports]
    assert len(supports) == 1 << len(basis)
    return tuple(supports)


def translated(state, missing, support):
    shift = 31 ^ (1 << missing)
    return base.canonical(tuple(
        label ^ shift if (support >> edge) & 1 else label
        for edge, label in enumerate(state)
    ))


def audit_graph(row):
    n, edges, incidence = base.decode_graph6(row)
    assert (
        base.graph_girth(n, edges),
        base.edge_connectivity_at_least_three(n, edges),
        base.cyclic_edge_connectivity(n, edges),
        base.tait_colouring_exists(edges, incidence),
    ) == METADATA[row]
    flows = base.enumerate_flows(edges, incidence)
    unseen = set(flows)
    orbits = []
    orbit_of = {}
    while unseen:
        seed = min(unseen)
        orbit = base.kempe_orbit(seed, edges, incidence)
        index = len(orbits)
        orbits.append(orbit)
        unseen -= orbit
        for state in orbit:
            orbit_of[state] = index
    assert len(orbit_of) == len(flows)

    @lru_cache(maxsize=None)
    def fixed_good(state, cap, root):
        return base.fixed_typed_data(state, cap, root, edges, incidence)[1].bit_count() >= 2

    @lru_cache(maxsize=None)
    def full_neighbours(state):
        answer = set()
        for missing in range(5):
            allowed = tuple(
                edge for edge, label in enumerate(state)
                if not ((label >> missing) & 1)
            )
            for support in cycle_space(n, edges, allowed)[1:]:
                other = translated(state, missing, support)
                assert other in flows
                answer.add(other)
        return frozenset(answer)

    @lru_cache(maxsize=None)
    def simple_transitions(orbit_index):
        answer = []
        for state in orbits[orbit_index]:
            for missing in range(5):
                allowed = tuple(
                    edge for edge, label in enumerate(state)
                    if not ((label >> missing) & 1)
                )
                for circuit in simple_cycles(n, edges, allowed):
                    support = sum(1 << edge for edge in circuit)
                    other = translated(state, missing, support)
                    assert other in flows
                    answer.append((state, missing, circuit, other, orbit_of[other]))
        return tuple(answer)

    bad = []
    for orbit_index, orbit in enumerate(orbits):
        for cap in range(n):
            for root, endpoints in enumerate(edges):
                if cap in endpoints:
                    continue
                if not any(fixed_good(state, cap, root) for state in orbit):
                    bad.append((orbit_index, cap, root))

    strict = []
    for orbit_index, cap, root in bad:
        transitions = simple_transitions(orbit_index)
        if not any(fixed_good(other, cap, root) for _, _, _, other, _ in transitions):
            strict.append((orbit_index, cap, root))

    full_immediate_failures = 0
    direct_depth_two_rescues = 0
    disjoint_good_orbit_escapes = 0
    first_depth_two = None
    first_orbit_escape = None
    for orbit_index, cap, root in strict:
        first_layer = frozenset(
            other
            for state in orbits[orbit_index]
            for other in full_neighbours(state)
        )
        assert first_layer
        if any(fixed_good(other, cap, root) for other in first_layer):
            raise AssertionError("full fixed-h immediate rescue contradicts delimiter")
        full_immediate_failures += 1

        forbidden = {root, *incidence[cap]}
        orbit_good = [
            any(fixed_good(state, cap, root) for state in orbit)
            for orbit in orbits
        ]
        escapes = [
            record for record in simple_transitions(orbit_index)
            if orbit_good[record[4]] and forbidden.isdisjoint(record[2])
        ]
        assert escapes
        disjoint_good_orbit_escapes += 1
        if first_orbit_escape is None:
            first_orbit_escape = min(escapes, key=lambda record: (len(record[2]), record[1], record[2]))

        found = None
        for middle in sorted(first_layer):
            for final in full_neighbours(middle):
                if fixed_good(final, cap, root):
                    found = (middle, final)
                    break
            if found:
                break
        assert found is not None
        direct_depth_two_rescues += 1
        if first_depth_two is None:
            first_depth_two = found

    print(
        f"GRAPH graph6={row} flows={len(flows)} orbits={len(orbits)} "
        f"bad_orbit_interfaces={len(bad)} strict_simple_failures={len(strict)} "
        f"full_cycle_space_immediate_failures={full_immediate_failures} "
        f"direct_depth_two_rescues={direct_depth_two_rescues} "
        f"disjoint_one_complement_good_orbit_escapes={disjoint_good_orbit_escapes} PASS"
    )
    return len(strict)


def main():
    strict = sum(audit_graph(row) for row in GRAPH_ROWS)
    assert strict == 12
    print("TOTAL strict_simple_failures=12 full_cycle_space_immediate_failures=12 "
          "direct_depth_two_rescues=12 disjoint_one_complement_good_orbit_escapes=12 PASS")


if __name__ == "__main__":
    main()
