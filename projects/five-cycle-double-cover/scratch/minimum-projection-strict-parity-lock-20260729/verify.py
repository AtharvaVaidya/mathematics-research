#!/usr/bin/env python3
"""Exact verifier for the minimized strict parity-lock construction."""

from __future__ import annotations

import hashlib
import itertools
import shutil
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCKED = frozenset((0, 2, 3, 4, 7, 8, 9, 10))
CLOSURE_G6 = "Q???C@?K?WEOM?_aGo?I__W@G_?"
CUT_EDGE = 5

BASE_EDGES = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11), (1, 9), (2, 12), (3, 10),
        (14, 4), (14, 5), (14, 15), (15, 6), (15, 16),
        (16, 13), (16, 17), (17, 7), (17, 8),
    )
)
BASE_FLOW = (
    7, 5, 7, 3, 7, 5, 1,
    3, 7, 5, 1, 7, 5, 1,
    6, 2, 2, 4, 4, 2, 6, 4, 2, 4, 6, 2, 4,
)
CLOSURE_FLOW = (
    4, 6, 2, 6, 4, 5, 4, 2, 6,
    6, 4, 2, 2, 3, 1, 2, 7, 5,
    2, 6, 4, 6, 2, 4, 4, 6, 2,
)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def decode_graph6(text):
    assert text and text[0] != "~"
    order = ord(text[0]) - 63
    bits = []
    for character in text[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for second in range(1, order):
        for first in range(second):
            if bits[cursor]:
                edges.append((first, second))
            cursor += 1
    return order, tuple(edges)


CLOSURE_ORDER, CLOSURE_EDGES = decode_graph6(CLOSURE_G6)


def adjacency(order, edges):
    result = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        result[u].append((v, edge))
        result[v].append((u, edge))
    return result


def connected(order, edges, omitted=None):
    graph = adjacency(order, edges)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour, edge in graph[vertex]:
            if edge == omitted or neighbour in seen:
                continue
            seen.add(neighbour)
            stack.append(neighbour)
    return len(seen) == order


def graph_checks(order, edges):
    assert all(u != v for u, v in edges)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    graph = adjacency(order, edges)
    assert {len(row) for row in graph} == {3}
    assert connected(order, edges)
    assert all(connected(order, edges, edge) for edge in range(len(edges)))
    return graph


def nonplanar_base_certificate():
    left = (2, 10, 16)
    right = (3, 9, 12)
    paths = (
        (2, 3),
        (2, 1, 9),
        (2, 12),
        (10, 3),
        (10, 9),
        (10, 11, 12),
        (16, 15, 14, 4, 3),
        (16, 17, 8, 9),
        (16, 13, 12),
    )
    expected_pairs = {
        (first, second) for first in left for second in right
    }
    assert {
        (path[0], path[-1]) for path in paths
    } == expected_pairs
    base_pairs = {tuple(sorted(edge)) for edge in BASE_EDGES}
    used_edges = set()
    used_internal = set()
    branches = set(left) | set(right)
    for path in paths:
        assert not (set(path[1:-1]) & branches)
        assert not (set(path[1:-1]) & used_internal)
        used_internal.update(path[1:-1])
        for u, v in zip(path, path[1:]):
            edge = tuple(sorted((u, v)))
            assert edge in base_pairs and edge not in used_edges
            used_edges.add(edge)
    return paths


def verify_flow(order, edges, values):
    assert len(values) == len(edges)
    assert all(values)
    graph = adjacency(order, edges)
    assert all(
        xor_all(values[edge] for _neighbour, edge in row) == 0
        for row in graph
    )


def cycle_space(order, edges):
    graph = adjacency(order, edges)
    seen = {0}
    path = [0] * order
    tree = set()
    stack = [0]
    while stack:
        u = stack.pop()
        for v, edge in graph[u]:
            if v in seen:
                continue
            seen.add(v)
            tree.add(edge)
            path[v] = path[u] ^ (1 << edge)
            stack.append(v)
    assert len(seen) == order
    basis = tuple(
        path[u] ^ path[v] ^ (1 << edge)
        for edge, (u, v) in enumerate(edges)
        if edge not in tree
    )
    cycles = [0]
    for vector in basis:
        cycles += [cycle ^ vector for cycle in cycles]
    assert len(set(cycles)) == 1 << (len(edges) - order + 1)
    return tuple(cycles)


def liftable_supports(order, edges):
    cycles = cycle_space(order, edges)
    all_edges = (1 << len(edges)) - 1
    missing = {
        all_edges ^ (first | second)
        for first in cycles
        for second in cycles
    }
    liftable = tuple(
        support
        for support in cycles
        if any((zero & ~support) == 0 for zero in missing)
    )
    return cycles, missing, liftable


def components_without(order, edges, removed):
    graph = adjacency(order, edges)
    labels = [-1] * order
    components = []
    for root in range(order):
        if labels[root] >= 0:
            continue
        label = len(components)
        labels[root] = label
        vertices = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            for v, edge in graph[u]:
                if edge in removed or labels[v] >= 0:
                    continue
                labels[v] = label
                vertices.add(v)
                stack.append(v)
        components.append(frozenset(vertices))
    return tuple(labels), tuple(components)


def base_clean(first, second, labels):
    parity = [[0] * 4 for _ in range(max(labels) + 1)]
    for edge in range(14):
        u, v = BASE_EDGES[edge]
        if labels[u] == labels[v]:
            continue
        colour = ((first >> edge) & 1) | (2 * ((second >> edge) & 1))
        parity[labels[u]][colour] ^= 1
        parity[labels[v]][colour] ^= 1
    return not any(any(row) for row in parity)


def base_audit():
    graph_checks(18, BASE_EDGES)
    verify_flow(18, BASE_EDGES, BASE_FLOW)
    cycles, missing, liftable = liftable_supports(18, BASE_EDGES)
    assert (len(cycles), len(missing), len(liftable)) == (1024, 66207, 1008)
    target = (1 << 14) - 1
    outside = ((1 << 27) - 1) ^ target
    labels, _components = components_without(18, BASE_EDGES, set(range(14)))
    assert tuple(labels[:14]) == tuple(map(int, "01234444413024"))
    extensions = clean = 0
    for first in cycles:
        for second in cycles:
            if outside & ~(first | second):
                continue
            extensions += 1
            clean += base_clean(first, second, labels)
    assert (extensions, clean) == (15360, 0)
    return liftable


def closure_audit():
    assert (CLOSURE_ORDER, len(CLOSURE_EDGES), CLOSURE_EDGES[CUT_EDGE]) == (
        18, 27, (5, 10)
    )
    graph_checks(CLOSURE_ORDER, CLOSURE_EDGES)
    verify_flow(CLOSURE_ORDER, CLOSURE_EDGES, CLOSURE_FLOW)
    support = sum(
        (value & 1) << edge for edge, value in enumerate(CLOSURE_FLOW)
    )
    assert support == 0x36020
    assert CLOSURE_FLOW[CUT_EDGE] == 5
    cycles, missing, liftable = liftable_supports(
        CLOSURE_ORDER, CLOSURE_EDGES
    )
    assert (len(cycles), len(missing), len(liftable)) == (1024, 70780, 1008)
    avoid = min(
        value.bit_count()
        for value in liftable
        if not ((value >> CUT_EDGE) & 1)
    )
    use = min(
        value.bit_count()
        for value in liftable
        if (value >> CUT_EDGE) & 1
    )
    use_minima = tuple(
        value for value in liftable
        if value.bit_count() == use and ((value >> CUT_EDGE) & 1)
    )
    assert (avoid, use, use_minima) == (7, 5, (0x36020,))
    return avoid, use


def placement_audit(liftable):
    target = (1 << 14) - 1
    valid = []
    minimum_gap = {}
    for locked in range(1 << 14):
        gaps = []
        for support in liftable:
            if support == target:
                continue
            omitted = target & ~support
            added = support & ~target
            gap = (
                (locked & omitted).bit_count()
                - ((target ^ locked) & omitted).bit_count()
                + added.bit_count()
            )
            gaps.append(gap)
        if min(gaps) > 0:
            valid.append(locked)
            minimum_gap[locked] = min(gaps)
    minimum_size = min(value.bit_count() for value in valid)
    minima = tuple(
        value for value in valid if value.bit_count() == minimum_size
    )
    chosen = sum(1 << edge for edge in LOCKED)
    assert (len(valid), minimum_size, len(minima)) == (2280, 8, 180)
    assert chosen in minima and minimum_gap[chosen] == 1
    return len(valid), len(minima)


def transform_local(value, terminal):
    shift = 2 ^ (terminal >> 1)
    first = value & 1
    low = (value >> 1) ^ (shift if first else 0)
    return first | (low << 1)


def build_graph():
    edges = []
    values = []
    for edge, pair in enumerate(BASE_EDGES):
        if edge not in LOCKED:
            edges.append(pair)
            values.append(BASE_FLOW[edge])
    order = 18
    for base_edge in sorted(LOCKED):
        u, v = BASE_EDGES[base_edge]
        terminal = BASE_FLOW[base_edge]
        local_values = tuple(
            transform_local(value, terminal) for value in CLOSURE_FLOW
        )
        assert local_values[CUT_EDGE] == terminal
        offset = order
        order += CLOSURE_ORDER
        edges.append((u, offset + CLOSURE_EDGES[CUT_EDGE][0]))
        values.append(terminal)
        for edge, (a, b) in enumerate(CLOSURE_EDGES):
            if edge == CUT_EDGE:
                continue
            edges.append((offset + a, offset + b))
            values.append(local_values[edge])
        edges.append((offset + CLOSURE_EDGES[CUT_EDGE][1], v))
        values.append(terminal)
    return order, tuple(edges), tuple(values)


def read_edge_tsv():
    rows = []
    for line in (HERE / "graph-edges.tsv").read_text().splitlines():
        if not line or line.startswith("edge"):
            continue
        edge, u, v = map(int, line.split("\t"))
        assert edge == len(rows)
        rows.append((u, v))
    return tuple(rows)


def graph6(order, edges):
    if order <= 62:
        header = chr(order + 63)
    else:
        assert order <= 258047
        header = "~" + "".join(
            chr(((order >> shift) & 63) + 63) for shift in (12, 6, 0)
        )
    edge_set = {tuple(sorted(edge)) for edge in edges}
    bits = [
        int((first, second) in edge_set)
        for second in range(1, order)
        for first in range(second)
    ]
    while len(bits) % 6:
        bits.append(0)
    body = "".join(
        chr(
            sum(bits[start + offset] << (5 - offset) for offset in range(6))
            + 63
        )
        for start in range(0, len(bits), 6)
    )
    return header + body


def canonical_audit(order, edges):
    assert shutil.which("labelg"), "nauty labelg is required"
    encoded = graph6(order, edges) + "\n"
    sparse_result = subprocess.run(
        ("labelg", "-q", "-s"), input=encoded, text=True,
        capture_output=True, check=True,
    )
    graph6_result = subprocess.run(
        ("labelg", "-q", "-g"), input=encoded, text=True,
        capture_output=True, check=True,
    )
    expected_sparse = (HERE / "canonical.s6").read_text()
    expected_graph6 = (HERE / "canonical.g6").read_text()
    assert sparse_result.stdout == expected_sparse
    assert graph6_result.stdout == expected_graph6
    return (
        hashlib.sha256(expected_sparse.encode()).hexdigest(),
        hashlib.sha256(expected_graph6.encode()).hexdigest(),
    )


def support_audit(order, edges, values):
    support = frozenset(
        edge for edge, value in enumerate(values) if value & 1
    )
    assert len(support) == 54
    support_graph = adjacency(order, edges)
    active = {
        vertex for edge in support for vertex in edges[edge]
    }
    assert {
        sum(edge in support for _neighbour, edge in support_graph[vertex])
        for vertex in active
    } == {2}
    unseen = set(active)
    sizes = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            for v, edge in support_graph[u]:
                if edge in support and v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    stack.append(v)
        sizes.append(len(component))
    assert sorted(sizes) == [27, 27]

    labels, components = components_without(order, edges, support)
    assert len(components) == 13
    assert tuple(labels[:14]) == tuple(map(int, "01234444413024"))
    return support, tuple(sorted(map(len, components)))


def parse_certificates():
    answer = {}
    for line in (HERE / "fivecdc-certificates.txt").read_text().splitlines():
        key, value = line.split("=", 1)
        answer[key] = tuple(value[index:index + 2]
                            for index in range(0, len(value), 2))
    return answer


def check_fivecdc(order, edges, pairs):
    assert len(pairs) == len(edges)
    for pair in pairs:
        assert len(pair) == 2 and pair[0] < pair[1]
        assert set(pair) <= set("01234")
    graph = adjacency(order, edges)
    for row in graph:
        for colour in "01234":
            assert sum(colour in pairs[edge] for _v, edge in row) % 2 == 0
    return tuple(sum(colour in pair for pair in pairs) for colour in "01234")


def permuted_pair(pair, source, target):
    source_rest = [value for value in range(5) if str(value) not in source]
    target_rest = [value for value in range(5) if str(value) not in target]
    mapping = {
        int(source[0]): int(target[0]),
        int(source[1]): int(target[1]),
        **dict(zip(source_rest, target_rest)),
    }
    return "".join(map(str, sorted(mapping[int(value)] for value in pair)))


def fivecdc_audit(order, edges):
    rows = parse_certificates()
    assert set(rows) == {"BASE", "CLOSURE", "COMPOSITIONAL", "DIRECT_SAT"}
    assert check_fivecdc(18, BASE_EDGES, rows["BASE"]) == (7, 7, 13, 14, 13)
    assert check_fivecdc(
        CLOSURE_ORDER, CLOSURE_EDGES, rows["CLOSURE"]
    ) == (7, 10, 11, 13, 13)

    composed = [
        rows["BASE"][edge] for edge in range(27) if edge not in LOCKED
    ]
    marked = rows["CLOSURE"][CUT_EDGE]
    for base_edge in sorted(LOCKED):
        target = rows["BASE"][base_edge]
        composed.append(target)
        composed.extend(
            permuted_pair(pair, marked, target)
            for edge, pair in enumerate(rows["CLOSURE"])
            if edge != CUT_EDGE
        )
        composed.append(target)
    assert tuple(composed) == rows["COMPOSITIONAL"]
    compositional_sizes = check_fivecdc(order, edges, tuple(composed))
    direct_sizes = check_fivecdc(order, edges, rows["DIRECT_SAT"])
    assert compositional_sizes == (79, 90, 106, 106, 105)
    assert direct_sizes == (99, 93, 101, 95, 98)
    return compositional_sizes, direct_sizes


def main():
    avoid, use = closure_audit()
    liftable = base_audit()
    assert len(nonplanar_base_certificate()) == 9
    valid, minimizers = placement_audit(liftable)
    order, edges, values = build_graph()
    assert (order, len(edges)) == (162, 243)
    assert edges == read_edge_tsv()
    graph_checks(order, edges)
    verify_flow(order, edges, values)
    support, component_sizes = support_audit(order, edges, values)
    sparse_digest, graph6_digest = canonical_audit(order, edges)
    compositional_sizes, direct_sizes = fivecdc_audit(order, edges)
    assert (avoid, use, len(support)) == (7, 5, 54)

    print(
        "LOCK closure_order=18 closure_edges=27"
        " cut_edge=5 endpoints=5,10"
        " cycles=1024 missing=70780 liftable=1008"
        " a0=7 a1=5 odd_minimum_supports=1"
    )
    print(
        "BASE cycles=1024 missing=66207 liftable=1008"
        " target_extensions=15360 target_clean=0"
    )
    print(
        f"PLACEMENTS total=16384 uniquely_optimal={valid}"
        f" minimum_locks=8 minimizers={minimizers}"
        " chosen=0,2,3,4,7,8,9,10 gap=1"
    )
    print(
        "GRAPH vertices=162 edges=243 simple=1 cubic=1"
        " connected=1 bridgeless=1 nonplanar_by_base_minor=1"
        " target_support=54 support_circuits=27,27"
        f" complement_components={len(component_sizes)}"
    )
    print(
        "MINIMUM exact_mu=54 unique_projection=1"
        " all_minimum_extensions_clean=0"
    )
    print(
        f"FIVECDC compositional_sizes={compositional_sizes}"
        f" direct_sat_sizes={direct_sizes}"
        " exact_two=1 parity=1"
    )
    print(
        f"CANONICAL graph6_sha256={graph6_digest}"
        f" sparse6_sha256={sparse_digest}"
    )
    print(
        "PASS unique globally minimum uncleanable projection;"
        " graph has a FiveCDC"
    )


if __name__ == "__main__":
    main()
