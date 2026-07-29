#!/usr/bin/env python3
"""Exact checker for the smallest rainbow/load abstract survivor.

The checker also constructs a 278-vertex metric inflation, proves all
four static shortest-join inequalities, and proves that its displayed
14-edge projection is not globally minimum (the exact minimum is seven).
"""

from __future__ import annotations

import itertools
from collections import Counter, deque
from functools import lru_cache


K = range(4)
NZ = (1, 2, 3)
WORDS = ("3231320", "1320320")
PARTITION = tuple(map(int, "01234444413024"))
SELECTED_BLOCKS = frozenset((0, 1, 3))
CHAIN = 5

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
BASE_ORDER = 18
SUPPORT = frozenset(range(14))
SELECTED_LOW = tuple(map(int, "".join(WORDS))) + (
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
SIZE7_BASE_FLOW = (
    3,
    1,
    3,
    7,
    5,
    1,
    5,
    6,
    4,
    6,
    2,
    4,
    6,
    2,
    6,
    2,
    2,
    4,
    2,
    4,
    6,
    4,
    2,
    4,
    6,
    4,
    2,
)
GL = tuple((0,) + permutation for permutation in itertools.permutations(NZ))


def xor_all(values):
    result = 0
    for value in values:
        result ^= value
    return result


def derivatives(word):
    row = tuple(map(int, word))
    return tuple(row[index - 1] ^ row[index] for index in range(len(row)))


def integrate(row):
    previous = 0
    word = []
    for value in row:
        previous ^= value
        word.append(previous)
    assert previous == 0
    return tuple(word)


def translated(words, shifts):
    return tuple(
        tuple(value ^ shifts[circuit] for value in word)
        for circuit, word in enumerate(words)
    )


def clean(words):
    parity = [[0] * 4 for _ in range(max(PARTITION) + 1)]
    offset = 0
    for word in words:
        length = len(word)
        for index, colour in enumerate(word):
            first = PARTITION[offset + index]
            second = PARTITION[offset + (index + 1) % length]
            if first != second:
                parity[first][colour] ^= 1
                parity[second][colour] ^= 1
        offset += length
    return not any(any(row) for row in parity)


def cut_colour_counts(words, selected):
    result = Counter()
    offset = 0
    for word in words:
        length = len(word)
        for index, colour in enumerate(word):
            first = PARTITION[offset + index] in selected
            second = PARTITION[offset + (index + 1) % length] in selected
            if first != second:
                result[colour] += 1
        offset += length
    return tuple(result[colour] for colour in K)


def abstract_audit():
    original_derivatives = tuple(
        value
        for word in WORDS
        for value in derivatives(word)
    )
    assert all(value in NZ for value in original_derivatives)
    for block in range(max(PARTITION) + 1):
        assert xor_all(
            original_derivatives[index]
            for index, owner in enumerate(PARTITION)
            if owner == block
        ) == 0

    offset = 0
    for word in WORDS:
        length = len(word)
        assert xor_all(
            original_derivatives[offset + index]
            for index in range(length)
            if PARTITION[offset + index] in SELECTED_BLOCKS
        ) == 0
        offset += length

    rows = []
    for linear in GL:
        changed = tuple(
            linear[value] if PARTITION[index] in SELECTED_BLOCKS else value
            for index, value in enumerate(original_derivatives)
        )
        first = integrate(changed[:7])
        second = integrate(changed[7:])
        words = (first, second)
        clean_shifts = tuple(
            shift
            for shift in K
            if clean(translated(words, (0, shift)))
        )
        deletion = any(len(set(word)) < 4 for word in words)
        crossing = cut_colour_counts(words, SELECTED_BLOCKS)
        parities = tuple(value & 1 for value in crossing)
        assert len(set(parities)) == 1
        inside = Counter(
            changed[index]
            for index, owner in enumerate(PARTITION)
            if owner in SELECTED_BLOCKS
        )
        outside = Counter(
            changed[index]
            for index, owner in enumerate(PARTITION)
            if owner not in SELECTED_BLOCKS
        )
        inside_row = tuple(inside[value] for value in NZ)
        outside_row = tuple(outside[value] for value in NZ)
        max_load = max(inside_row) + max(outside_row)
        assert max_load == 6
        assert max_load <= 2 * 4
        assert not clean_shifts
        assert not deletion
        rows.append(
            (
                "".join(map(str, linear[1:])),
                "|".join("".join(map(str, word)) for word in words),
                crossing,
                inside_row,
                outside_row,
                max_load,
            )
        )

    assert cut_colour_counts(
        tuple(tuple(map(int, word)) for word in WORDS),
        SELECTED_BLOCKS,
    ) == (1, 1, 1, 3)
    obstruction_bits = tuple(row[2][0] & 1 for row in rows)
    assert obstruction_bits.count(1) == 4
    assert obstruction_bits.count(0) == 2

    print("ABSTRACT support=14 shape=7+7 partition=01234444413024")
    print(
        "  selected_blocks=013 initial_crossing=(1,1,1,3)"
        " rainbow_odd=1"
    )
    for row in rows:
        print(
            f"  map={row[0]} words={row[1]} crossing={row[2]}"
            f" inside={row[3]} outside={row[4]}"
            f" max_load={row[5]} clean=0 delete=0"
        )
    print(
        f"  six_map_obstruction_bits={obstruction_bits}"
        " load_bound_small_realization=8"
    )
    return rows


def adjacency(order, edges):
    result = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        result[u].append((v, edge))
        result[v].append((u, edge))
    return result


def graph_checks(order, edges):
    assert all(u != v for u, v in edges)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    graph = adjacency(order, edges)
    assert {len(row) for row in graph} == {3}

    def connected(omitted=None):
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

    assert connected()
    assert all(connected(edge) for edge in range(len(edges)))
    return graph


def verify_vector_flow(order, edges, values):
    assert len(values) == len(edges)
    assert all(value != 0 for value in values)
    graph = adjacency(order, edges)
    assert all(
        xor_all(values[edge] for _v, edge in incident) == 0
        for incident in graph
    )


def component_labels(order, edges, support):
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
                if edge in support or labels[v] >= 0:
                    continue
                labels[v] = count
                stack.append(v)
        count += 1
    return tuple(labels), count


def cycle_basis(order, edges):
    graph = adjacency(order, edges)
    parent = [-1] * order
    root_path = [0] * order
    tree = set()
    parent[0] = 0
    stack = [0]
    while stack:
        u = stack.pop()
        for v, edge in graph[u]:
            if parent[v] >= 0:
                continue
            parent[v] = u
            root_path[v] = root_path[u] ^ (1 << edge)
            tree.add(edge)
            stack.append(v)
    assert all(value >= 0 for value in parent)
    return tuple(
        root_path[u] ^ root_path[v] ^ (1 << edge)
        for edge, (u, v) in enumerate(edges)
        if edge not in tree
    )


def all_cycles(basis):
    result = [0]
    for vector in basis:
        result += [value ^ vector for value in result]
    return tuple(result)


def base_clean(h, p, q, labels, component_count):
    parity = [[0] * 4 for _ in range(component_count)]
    for edge, (u, v) in enumerate(BASE_EDGES):
        if not (h >> edge) & 1 or labels[u] == labels[v]:
            continue
        colour = ((p >> edge) & 1) | (2 * ((q >> edge) & 1))
        parity[labels[u]][colour] ^= 1
        parity[labels[v]][colour] ^= 1
    return not any(any(row) for row in parity)


def base_cycle_audit():
    graph_checks(BASE_ORDER, BASE_EDGES)
    verify_vector_flow(
        BASE_ORDER,
        BASE_EDGES,
        tuple(
            (1 if edge in SUPPORT else 0) | (SELECTED_LOW[edge] << 1)
            for edge in range(len(BASE_EDGES))
        ),
    )
    verify_vector_flow(BASE_ORDER, BASE_EDGES, SIZE7_BASE_FLOW)
    assert sum(value & 1 for value in SIZE7_BASE_FLOW) == 7

    labels, component_count = component_labels(
        BASE_ORDER, BASE_EDGES, SUPPORT
    )
    assert tuple(labels[vertex] for vertex in range(14)) == PARTITION
    assert component_count == 5

    basis = cycle_basis(BASE_ORDER, BASE_EDGES)
    assert len(basis) == 10
    cycles = all_cycles(basis)
    assert len(cycles) == 1024
    all_edges = (1 << len(BASE_EDGES)) - 1
    missing = {
        all_edges ^ (first | second)
        for first in cycles
        for second in cycles
    }
    assert len(missing) == 66207

    target = (1 << 14) - 1
    outside = all_edges ^ target
    extensions = 0
    clean_extensions = 0
    for first in cycles:
        for second in cycles:
            if outside & ~(first | second):
                continue
            extensions += 1
            clean_extensions += base_clean(
                target, first, second, labels, component_count
            )
    assert (extensions, clean_extensions) == (15360, 0)

    liftable = tuple(
        support
        for support in cycles
        if any(zero & ~support == 0 for zero in missing)
    )
    ordinary_minimum = min(value.bit_count() for value in liftable)
    ordinary_minima = tuple(
        value for value in liftable if value.bit_count() == ordinary_minimum
    )
    weight = (1,) * 14 + (2,) * (len(BASE_EDGES) - 14)
    weighted_value = {
        support: sum(
            weight[edge]
            for edge in range(len(BASE_EDGES))
            if (support >> edge) & 1
        )
        for support in liftable
    }
    weighted_minimum = min(weighted_value.values())
    weighted_minima = tuple(
        support
        for support, value in weighted_value.items()
        if value == weighted_minimum
    )
    assert ordinary_minimum == 5 and len(ordinary_minima) == 4
    assert weighted_minimum == 7 and len(weighted_minima) == 6
    assert sum(1 << edge for edge in range(7)) in weighted_minima
    print(
        "BASE vertices=18 edges=27 simple=1 cubic=1 bridgeless=1"
        " cycle_space=1024 missing_masks=66207"
    )
    print(
        "  target_extensions=15360 target_clean=0"
        " ordinary_minimum=5 ordinary_minima=4"
        " weighted_minimum=7 weighted_minima=6"
    )
    return weighted_minimum


def inflate(chain, low_values=None, full_values=None):
    assert (low_values is None) != (full_values is None)
    values = low_values if low_values is not None else full_values
    edges = list(BASE_EDGES[:14])
    result_values = list(values[:14])
    order = BASE_ORDER
    for edge in range(14, len(BASE_EDGES)):
        u, v = BASE_EDGES[edge]
        terminal = values[edge]
        if low_values is not None:
            candidates = tuple(value for value in NZ if value != terminal)
        elif terminal & 1:
            candidates = tuple(value for value in range(1, 8) if value != terminal)
        else:
            candidates = tuple(
                value for value in (2, 4, 6) if value != terminal
            )
        first_other = candidates[0]
        second_other = terminal ^ first_other
        assert first_other and second_other and first_other != second_other
        previous = u
        for _copy in range(chain):
            a, b, r, s = range(order, order + 4)
            order += 4
            edges.append((previous, a))
            result_values.append(terminal)
            edges.extend(((r, s), (a, r), (b, s), (a, s), (b, r)))
            result_values.extend(
                (
                    terminal,
                    first_other,
                    first_other,
                    second_other,
                    second_other,
                )
            )
            previous = b
        edges.append((previous, v))
        result_values.append(terminal)
    return order, tuple(edges), tuple(result_values)


def distances(order, graph, deleted, source):
    adjacency_rows = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(graph):
        if edge in deleted:
            continue
        adjacency_rows[u].append(v)
        adjacency_rows[v].append(u)
    answer = [-1] * order
    answer[source] = 0
    queue = deque((source,))
    while queue:
        u = queue.popleft()
        for v in adjacency_rows[u]:
            if answer[v] < 0:
                answer[v] = answer[u] + 1
                queue.append(v)
    assert all(value >= 0 for value in answer)
    return answer


def minimum_t_join(order, graph, matching):
    terminals = tuple(
        vertex for edge in matching for vertex in graph[edge]
    )
    assert len(terminals) == len(set(terminals))
    metric = tuple(
        tuple(
            distances(order, graph, frozenset(matching), source)[target]
            for target in terminals
        )
        for source in terminals
    )

    @lru_cache(maxsize=None)
    def solve(mask):
        if not mask:
            return 0
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        answer = 10**9
        candidates = remainder
        while candidates:
            second_bit = candidates & -candidates
            second = second_bit.bit_length() - 1
            answer = min(
                answer,
                metric[first][second] + solve(remainder ^ second_bit),
            )
            candidates ^= second_bit
        return answer

    return solve((1 << len(terminals)) - 1)


def inflated_audit(weighted_minimum):
    order, edges, low = inflate(CHAIN, low_values=SELECTED_LOW)
    graph_checks(order, edges)
    displayed = tuple(
        (1 if edge in SUPPORT else 0) | (low[edge] << 1)
        for edge in range(len(edges))
    )
    verify_vector_flow(order, edges, displayed)
    assert (order, len(edges), len(edges) - order + 1) == (278, 417, 140)
    labels, component_count = component_labels(order, edges, SUPPORT)
    assert tuple(labels[vertex] for vertex in range(14)) == PARTITION
    assert component_count == 5

    class_sizes = []
    joins = []
    totals = []
    for colour in K:
        matching = tuple(
            edge for edge in SUPPORT if SELECTED_LOW[edge] == colour
        )
        join = minimum_t_join(order, edges, matching)
        class_sizes.append(len(matching))
        joins.append(join)
        totals.append(len(matching) + join)
    assert class_sizes == [3, 2, 4, 5]
    assert joins == [11, 12, 10, 9]
    assert totals == [14, 14, 14, 14]

    witness_order, witness_edges, witness_flow = inflate(
        CHAIN, full_values=SIZE7_BASE_FLOW
    )
    assert (witness_order, witness_edges) == (order, edges)
    verify_vector_flow(order, edges, witness_flow)
    assert sum(value & 1 for value in witness_flow) == 7
    assert weighted_minimum == 7

    n = order - len(SUPPORT)
    changed = tuple(
        value
        for word in WORDS
        for value in derivatives(word)
    )
    inside = Counter(
        changed[index]
        for index, owner in enumerate(PARTITION)
        if owner in SELECTED_BLOCKS
    )
    outside = Counter(
        changed[index]
        for index, owner in enumerate(PARTITION)
        if owner not in SELECTED_BLOCKS
    )
    max_load = max(inside.values()) + max(outside.values())
    assert max_load == 6 and max_load <= 2 * n

    print(
        "INFLATED chain=5 vertices=278 edges=417 cycle_dimension=140"
        " simple=1 cubic=1 bridgeless=1"
    )
    print(
        f"  class_sizes={tuple(class_sizes)} shortest_t_joins={tuple(joins)}"
        f" containing_cycles={tuple(totals)}"
    )
    print(
        "  target_clean=0_by_two_pole_contraction"
        " exact_minimum_projection=7"
        f" load_max={max_load} load_bound={2*n}"
    )


def main():
    abstract_audit()
    weighted_minimum = base_cycle_audit()
    inflated_audit(weighted_minimum)
    print("PASS smallest support-14 abstract survivor and realized no-go")


if __name__ == "__main__":
    main()
