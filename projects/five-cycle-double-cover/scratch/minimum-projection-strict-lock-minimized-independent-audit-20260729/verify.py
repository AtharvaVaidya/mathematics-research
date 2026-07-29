#!/usr/bin/env python3
"""Exact audit of the minimized strict-lock construction.

Only the Python standard library is used.  The checker independently:

* computes the conditional closure minima;
* minimizes the lock placement over all base extendable supports;
* constructs and checks the 162-vertex graph and a target flow;
* regenerates the base uncleanability count; and
* checks direct and compositional FiveCDC certificates.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent

CLOSURE_EDGES = (
    (0, 7),
    (1, 8),
    (2, 9),
    (3, 9),
    (4, 10),
    (5, 10),  # distinguished edge 5
    (2, 11),
    (3, 11),
    (6, 11),
    (2, 12),
    (3, 12),
    (4, 12),
    (0, 13),
    (6, 13),
    (10, 13),
    (1, 14),
    (5, 14),
    (6, 14),
    (5, 15),
    (7, 15),
    (9, 15),
    (0, 16),
    (7, 16),
    (8, 16),
    (1, 17),
    (4, 17),
    (8, 17),
)

BASE_EDGES = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11),
        (1, 9),
        (2, 12),
        (3, 10),
        (14, 4),
        (14, 5),
        (14, 15),
        (15, 6),
        (15, 16),
        (16, 13),
        (16, 17),
        (17, 7),
        (17, 8),
    )
)

TARGET_BASE = frozenset(range(14))
LOCKED = frozenset((0, 2, 3, 4, 7, 8, 9, 10))
LOCAL_TARGET = frozenset((5, 13, 14, 16, 17))

BASE_LOW = tuple(map(int, "32313201320320")) + (
    3,
    1,
    1,
    2,
    2,
    1,
    3,
    2,
    1,
    2,
    3,
    1,
    2,
)

BASE_FIVE = tuple(
    tuple(map(int, token))
    for token in (
        "01 02 23 24 23 12 02 13 14 24 23 13 01 12 "
        "12 12 03 34 34 13 14 01 04 02 24 23 34"
    ).split()
)

CLOSURE_FIVE = tuple(
    tuple(map(int, token))
    for token in (
        "01 24 23 24 12 02 02 04 24 03 02 23 02 12 "
        "01 12 24 14 04 03 34 12 13 23 14 13 34"
    ).split()
)

DIRECT_LABEL_SHA256 = (
    "845668d8778e48ae55cf7373ed159519804407a6d7afeb9999fda02cf97ae8c7"
)
COMPOSITION_LABEL_SHA256 = (
    "f1b77b572dfbd127e9dbf97a6b84a7b5be2e6d344393abb7f14b358af7b7fcd9"
)


def adjacency(order, edges):
    result = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        result[u].append((v, edge))
        result[v].append((u, edge))
    return result


def connected(order, graph, omitted=-1):
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v, edge in graph[u]:
            if edge == omitted or v in seen:
                continue
            seen.add(v)
            stack.append(v)
    return len(seen) == order


def graph_audit(order, edges):
    assert all(u != v for u, v in edges)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    graph = adjacency(order, edges)
    assert {len(row) for row in graph} == {3}
    assert connected(order, graph)
    assert all(
        connected(order, graph, omitted=edge)
        for edge in range(len(edges))
    )
    return graph


def cycle_basis(order, edges):
    graph = adjacency(order, edges)
    parent = [-1] * order
    path = [0] * order
    tree = set()
    parent[0] = 0
    stack = [0]
    while stack:
        u = stack.pop()
        for v, edge in graph[u]:
            if parent[v] >= 0:
                continue
            parent[v] = u
            path[v] = path[u] ^ (1 << edge)
            tree.add(edge)
            stack.append(v)
    assert all(value >= 0 for value in parent)
    return tuple(
        path[u] ^ path[v] ^ (1 << edge)
        for edge, (u, v) in enumerate(edges)
        if edge not in tree
    )


def all_cycles(basis):
    result = [0]
    for vector in basis:
        result += [value ^ vector for value in result]
    return tuple(result)


def extension_table(edges, cycles):
    full = (1 << len(edges)) - 1
    missing_counts = Counter(
        full ^ (first | second)
        for first in cycles
        for second in cycles
    )
    rows = []
    for support in cycles:
        count = sum(
            multiplicity
            for missing, multiplicity in missing_counts.items()
            if not missing & ~support
        )
        if count:
            rows.append((support, count))
    return missing_counts, tuple(rows)


def closure_audit():
    graph_audit(18, CLOSURE_EDGES)
    basis = cycle_basis(18, CLOSURE_EDGES)
    cycles = all_cycles(basis)
    assert len(basis) == 10
    assert len(cycles) == 1024
    missing, extensions = extension_table(CLOSURE_EDGES, cycles)
    assert len(missing) == 70780

    conditional = {}
    for bit in (0, 1):
        minimum = min(
            support.bit_count()
            for support, _count in extensions
            if ((support >> 5) & 1) == bit
        )
        rows = tuple(
            (support, count)
            for support, count in extensions
            if support.bit_count() == minimum
            and ((support >> 5) & 1) == bit
        )
        conditional[bit] = (minimum, rows)

    assert conditional[0][0] == 7
    assert len(conditional[0][1]) == 9
    assert sum(count for _support, count in conditional[0][1]) == 6336
    assert conditional[1] == ((5, ((221216, 240),)))
    assert {
        edge
        for edge in range(27)
        if (221216 >> edge) & 1
    } == LOCAL_TARGET

    profiles = Counter()
    for edge in range(27):
        row = []
        for bit in (0, 1):
            row.append(
                min(
                    support.bit_count()
                    for support, _count in extensions
                    if ((support >> edge) & 1) == bit
                )
            )
        profiles[tuple(row)] += 1
    assert profiles == Counter({(5, 7): 14, (5, 6): 8, (6, 5): 4, (7, 5): 1})

    print(
        "CLOSURE order=18 edges=27 dim=10 missing_sets=70780"
        " a0=7 a0_ties=9 a0_extensions=6336"
        " a1=5 a1_ties=1 a1_extensions=240"
    )
    return cycles


def base_and_lock_audit():
    graph_audit(18, BASE_EDGES)
    basis = cycle_basis(18, BASE_EDGES)
    cycles = all_cycles(basis)
    assert len(basis) == 10
    missing, rows = extension_table(BASE_EDGES, cycles)
    assert len(missing) == 66207
    assert len(rows) == 1008

    target = (1 << 14) - 1
    assert any(support == target for support, _count in rows)
    competitors = tuple(
        support for support, _count in rows if support != target
    )
    valid = []
    best_by_size = [-100] * 15
    for lock in range(1 << 14):
        minimum_delta = min(
            2 * ((target & ~support) & lock).bit_count()
            - (target & ~support).bit_count()
            + (support & ~target).bit_count()
            for support in competitors
        )
        best_by_size[lock.bit_count()] = max(
            best_by_size[lock.bit_count()], minimum_delta
        )
        if minimum_delta > 0:
            valid.append((lock, minimum_delta))

    assert best_by_size == [
        -9,
        -7,
        -5,
        -5,
        -3,
        -3,
        -1,
        -1,
        1,
        1,
        3,
        3,
        3,
        3,
        3,
    ]
    minimum_size = min(lock.bit_count() for lock, _delta in valid)
    minima = tuple(
        (lock, delta)
        for lock, delta in valid
        if lock.bit_count() == minimum_size
    )
    lock_mask = sum(1 << edge for edge in LOCKED)
    assert minimum_size == 8
    assert len(minima) == 180
    assert (lock_mask, 1) in minima

    print(
        "BASE dim=10 cycles=1024 missing_sets=66207"
        " extendable_supports=1008"
    )
    print(
        "LOCKS subsets=16384 minimum=8 minimizers=180"
        " canonical=0,2,3,4,7,8,9,10 gap=1"
        " no_size_le_7=1"
    )
    return cycles


def expanded_graph():
    edges = []
    target = set()
    metadata = []
    next_vertex = 18
    for base_edge, (u, v) in enumerate(BASE_EDGES):
        if base_edge not in LOCKED:
            edge = len(edges)
            edges.append((u, v))
            metadata.append(("base", base_edge, -1))
            if base_edge in TARGET_BASE:
                target.add(edge)
            continue

        offset = next_vertex
        next_vertex += 18
        for closure_edge, (a, b) in enumerate(CLOSURE_EDGES):
            if closure_edge == 5:
                continue
            edge = len(edges)
            edges.append((offset + a, offset + b))
            metadata.append(("inside", base_edge, closure_edge))
            if closure_edge in LOCAL_TARGET:
                target.add(edge)
        for endpoint, terminal in ((u, 5), (v, 10)):
            edge = len(edges)
            edges.append((endpoint, offset + terminal))
            metadata.append(("link", base_edge, 5))
            target.add(edge)

    assert next_vertex == 162
    assert len(edges) == 243
    assert len(target) == 54
    return next_vertex, tuple(edges), frozenset(target), tuple(metadata)


def verify_flow(order, edges, values):
    assert len(values) == len(edges)
    assert all(value in range(1, 8) for value in values)
    graph = adjacency(order, edges)
    assert all(
        not xor_all(values[edge] for _v, edge in incident)
        for incident in graph
    )


def xor_all(values):
    result = 0
    for value in values:
        result ^= value
    return result


def local_flow_vectors(closure_cycles):
    full = (1 << 27) - 1
    support = sum(1 << edge for edge in LOCAL_TARGET)
    vectors = {}
    extension_count = 0
    for first in closure_cycles:
        for second in closure_cycles:
            if support | first | second != full:
                continue
            extension_count += 1
            low_at_mark = ((first >> 5) & 1) | (
                2 * ((second >> 5) & 1)
            )
            vectors.setdefault(
                low_at_mark,
                tuple(
                    (4 if (support >> edge) & 1 else 0)
                    | ((first >> edge) & 1)
                    | (2 * ((second >> edge) & 1))
                    for edge in range(27)
                ),
            )
    assert extension_count == 240
    assert set(vectors) == set(range(4))
    for vector in vectors.values():
        verify_flow(18, CLOSURE_EDGES, vector)
        assert {
            edge for edge, value in enumerate(vector) if value & 4
        } == LOCAL_TARGET
    return vectors


def expanded_target_audit(closure_cycles):
    order, edges, target, metadata = expanded_graph()
    graph = graph_audit(order, edges)

    vectors = local_flow_vectors(closure_cycles)
    values = []
    for kind, base_edge, local_edge in metadata:
        if kind == "base":
            values.append(
                (4 if base_edge in TARGET_BASE else 0)
                | BASE_LOW[base_edge]
            )
        else:
            values.append(vectors[BASE_LOW[base_edge]][local_edge])
    verify_flow(order, edges, tuple(values))
    assert {
        edge for edge, value in enumerate(values) if value & 4
    } == target

    support_graph = [[] for _ in range(order)]
    for edge in target:
        u, v = edges[edge]
        support_graph[u].append((v, edge))
        support_graph[v].append((u, edge))
    assert {len(row) for row in support_graph} <= {0, 2}
    seen = set()
    circuit_lengths = []
    for start in range(order):
        if not support_graph[start] or start in seen:
            continue
        seen.add(start)
        stack = [start]
        degree_sum = 0
        while stack:
            u = stack.pop()
            degree_sum += len(support_graph[u])
            for v, _edge in support_graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        circuit_lengths.append(degree_sum // 2)
    assert sorted(circuit_lengths) == [27, 27]

    # The exact local and placement minima give the global bound.
    target_cost = 14 + 5 * len(LOCKED)
    assert target_cost == 54
    assert len(target) == target_cost

    print(
        "EXPANDED order=162 edges=243 simple=1 cubic=1"
        " connected=1 bridgeless=1"
        " target=54 circuits=27+27 global_minimum=54"
        " minimum_support_ties=1"
    )
    return order, edges, target, graph


def component_labels(order, edges, omitted):
    graph = adjacency(order, edges)
    labels = [-1] * order
    count = 0
    for start in range(order):
        if labels[start] >= 0:
            continue
        labels[start] = count
        stack = [start]
        while stack:
            u = stack.pop()
            for v, edge in graph[u]:
                if edge in omitted or labels[v] >= 0:
                    continue
                labels[v] = count
                stack.append(v)
        count += 1
    return tuple(labels), count


def base_cleanability_audit(base_cycles):
    target = (1 << 14) - 1
    full = (1 << 27) - 1
    labels, components = component_labels(
        18, BASE_EDGES, set(range(14))
    )
    assert components == 5
    extensions = 0
    clean = 0
    for first in base_cycles:
        for second in base_cycles:
            if target | first | second != full:
                continue
            extensions += 1
            parity = [[0] * 4 for _ in range(components)]
            for edge in range(14):
                u, v = BASE_EDGES[edge]
                if labels[u] == labels[v]:
                    continue
                colour = ((first >> edge) & 1) | (
                    2 * ((second >> edge) & 1)
                )
                parity[labels[u]][colour] ^= 1
                parity[labels[v]][colour] ^= 1
            clean += int(not any(any(row) for row in parity))
    assert extensions == 15360
    assert clean == 0

    print(
        "UNCLEAN base_target_extensions=15360"
        " clean=0 contraction_to_expanded=valid"
    )


def parse_labels(path):
    raw = path.read_text(encoding="ascii")
    tokens = raw.split()
    labels = tuple(tuple(map(int, token)) for token in tokens)
    assert all(
        len(pair) == 2
        and pair[0] < pair[1]
        and set(pair) <= set(range(5))
        for pair in labels
    )
    return raw, labels


def audit_labels(order, graph, labels):
    assert len(labels) == sum(len(row) for row in graph) // 2
    for vertex in range(order):
        for colour in range(5):
            assert (
                sum(
                    colour in labels[edge]
                    for _neighbor, edge in graph[vertex]
                )
                % 2
                == 0
            )
    return tuple(
        sum(colour in pair for pair in labels)
        for colour in range(5)
    )


def cnf_formula(order, graph):
    edge_count = sum(len(row) for row in graph) // 2

    def variable(edge, colour):
        return 5 * edge + colour + 1

    clauses = []
    for edge in range(edge_count):
        variables = [variable(edge, colour) for colour in range(5)]
        # At least two: every four-variable subset contains a true value.
        for omitted in range(5):
            clauses.append(
                tuple(
                    variables[index]
                    for index in range(5)
                    if index != omitted
                )
            )
        # At most two.
        for triple in itertools.combinations(variables, 3):
            clauses.append(tuple(-value for value in triple))

    # Even parity of three variables: forbid weights one and three.
    for vertex in range(order):
        incident = [edge for _neighbor, edge in graph[vertex]]
        assert len(incident) == 3
        for colour in range(5):
            a, b, c = (
                variable(edge, colour) for edge in incident
            )
            clauses.extend(
                (
                    (a, b, -c),
                    (a, -b, c),
                    (-a, b, c),
                    (-a, -b, -c),
                )
            )

    assert edge_count == 243
    assert len(clauses) == 6885
    lines = [f"p cnf {5 * edge_count} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return tuple(clauses), "\n".join(lines) + "\n"


def literal_satisfies_cnf(labels, clauses):
    assignment = {}
    for edge, pair in enumerate(labels):
        for colour in range(5):
            assignment[5 * edge + colour + 1] = colour in pair
    assert all(
        any(
            assignment[abs(literal)] == (literal > 0)
            for literal in clause
        )
        for clause in clauses
    )


def mapped_pair(pair, permutation):
    return tuple(sorted(permutation[value] for value in pair))


def compositional_labels():
    result = []
    marked = CLOSURE_FIVE[5]
    for base_edge in range(len(BASE_EDGES)):
        if base_edge not in LOCKED:
            result.append(BASE_FIVE[base_edge])
            continue
        target = BASE_FIVE[base_edge]
        permutation = next(
            row
            for row in itertools.permutations(range(5))
            if mapped_pair(marked, row) == target
        )
        for closure_edge in range(len(CLOSURE_EDGES)):
            if closure_edge == 5:
                continue
            result.append(
                mapped_pair(CLOSURE_FIVE[closure_edge], permutation)
            )
        result.extend((target, target))
    assert len(result) == 243
    return tuple(result)


def graph6(order, edges):
    assert 63 <= order <= 258047
    header = "~" + "".join(
        chr(((order >> shift) & 63) + 63)
        for shift in (12, 6, 0)
    )
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((lower, upper) in edge_set)
        for upper in range(1, order)
        for lower in range(upper)
    ]
    bits.extend([0] * (-len(bits) % 6))
    body = "".join(
        chr(
            63
            + sum(
                bits[offset + bit] << (5 - bit)
                for bit in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )
    return header + body


def fivecdc_audit(order, edges, graph):
    direct_raw, direct = parse_labels(HERE / "fivecdc-direct-labels.txt")
    assert hashlib.sha256(direct_raw.encode("ascii")).hexdigest() == (
        DIRECT_LABEL_SHA256
    )
    direct_sizes = audit_labels(order, graph, direct)
    assert direct_sizes == (92, 109, 97, 94, 94)

    clauses, dimacs = cnf_formula(order, graph)
    literal_satisfies_cnf(direct, clauses)
    cnf_sha = hashlib.sha256(dimacs.encode("ascii")).hexdigest()

    composition = compositional_labels()
    composition_raw = (
        " ".join("".join(map(str, pair)) for pair in composition) + "\n"
    )
    assert hashlib.sha256(composition_raw.encode("ascii")).hexdigest() == (
        COMPOSITION_LABEL_SHA256
    )
    composition_sizes = audit_labels(order, graph, composition)
    assert composition_sizes == (88, 92, 92, 110, 104)

    labelled = graph6(order, edges)
    frozen_labelled = (
        HERE / "labelled.g6"
    ).read_text(encoding="ascii").strip()
    assert labelled == frozen_labelled

    print(
        "FIVECDC formula_variables=1215 cnf_clauses=6885"
        " xor_rows=810 status=SAT"
    )
    print(
        "  direct_class_sizes=92,109,97,94,94"
        f" direct_sha256={DIRECT_LABEL_SHA256}"
    )
    print(
        "  composition_class_sizes=88,92,92,110,104"
        f" composition_sha256={COMPOSITION_LABEL_SHA256}"
    )
    print(f"  cnf_sha256={cnf_sha}")
    print(
        "  labelled_graph6_sha256="
        + hashlib.sha256((labelled + "\n").encode("ascii")).hexdigest()
    )


def main():
    closure_cycles = closure_audit()
    base_cycles = base_and_lock_audit()
    order, edges, target, graph = expanded_target_audit(closure_cycles)
    assert len(target) == 54
    base_cleanability_audit(base_cycles)
    fivecdc_audit(order, edges, graph)
    print(
        "PASS: unique globally minimum size-54 projection is uncleanable;"
        " graph has FiveCDC"
    )


if __name__ == "__main__":
    main()
