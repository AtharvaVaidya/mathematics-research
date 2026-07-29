#!/usr/bin/env python3
"""Independent audit using the separately written size-14 cycle model.

This checker uses the edge order and cycle-space implementation from the
frozen independent size-14 audit, then reconstructs the inflation and
shortest joins in that independent labeling.
"""

from __future__ import annotations

import itertools
import sys
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
INDEPENDENT = (
    HERE.parent / "minimum-projection-size14-independent-audit-20260729"
)
sys.path.insert(0, str(INDEPENDENT))
import verify_realization as source  # noqa: E402


WORD = tuple(map(int, "32313201320320"))
PARTITION = tuple(map(int, "01234444413024"))
Y = frozenset((0, 1, 3))
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
CHAIN = 5


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def derivative(word):
    return tuple(word[index - 1] ^ word[index] for index in range(len(word)))


def integrate(row):
    answer = []
    value = 0
    for increment in row:
        value ^= increment
        answer.append(value)
    assert value == 0
    return tuple(answer)


def defects(words):
    result = [[0] * 4 for _ in range(5)]
    offset = 0
    for word in words:
        for local, colour in enumerate(word):
            first = PARTITION[offset + local]
            second = PARTITION[offset + (local + 1) % len(word)]
            if first != second:
                result[first][colour] ^= 1
                result[second][colour] ^= 1
        offset += len(word)
    return tuple(tuple(row) for row in result)


def abstract_check():
    increments = derivative(WORD[:7]) + derivative(WORD[7:])
    for block in range(5):
        assert xor_all(
            increments[index]
            for index, owner in enumerate(PARTITION)
            if owner == block
        ) == 0
    for offset in (0, 7):
        assert xor_all(
            increments[index]
            for index in range(offset, offset + 7)
            if PARTITION[index] in Y
        ) == 0

    obstruction = []
    for matrix in GL:
        changed = tuple(
            matrix[value] if PARTITION[index] in Y else value
            for index, value in enumerate(increments)
        )
        circuits = (integrate(changed[:7]), integrate(changed[7:]))
        assert all(len(set(row)) == 4 for row in circuits)
        assert all(
            any(
                any(row)
                for row in defects(
                    (
                        circuits[0],
                        tuple(value ^ shift for value in circuits[1]),
                    )
                )
            )
            for shift in range(4)
        )
        shore_parities = []
        offset = 0
        counts = Counter()
        for circuit in circuits:
            for local, colour in enumerate(circuit):
                first = PARTITION[offset + local] in Y
                second = PARTITION[offset + (local + 1) % len(circuit)] in Y
                if first != second:
                    counts[colour] += 1
            offset += len(circuit)
        shore_parities = tuple(counts[colour] & 1 for colour in range(4))
        assert len(set(shore_parities)) == 1
        obstruction.append(shore_parities[0])
        inside = Counter(
            changed[index]
            for index, owner in enumerate(PARTITION)
            if owner in Y
        )
        outside = Counter(
            changed[index]
            for index, owner in enumerate(PARTITION)
            if owner not in Y
        )
        assert tuple(sorted(inside.values())) == (2, 2, 2)
        assert sorted(outside.values()) == [4, 4]
        assert max(inside.values()) + max(outside.values()) == 6 <= 8
    assert tuple(obstruction) == (1, 1, 0, 1, 0, 1)
    print(
        "ABSTRACT_INDEPENDENT maps=6 clean=0 delete=0"
        f" obstruction_bits={tuple(obstruction)} max_load=6 bound=8"
    )


def component_map_low():
    original = source.explicit_target_flow()
    components = source.components_without(source.TARGET)
    labels = {
        vertex: component
        for component, vertices in enumerate(components)
        for vertex in vertices
    }
    assert tuple(labels[vertex] for vertex in range(14)) == PARTITION
    maps = (
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 2, 1, 3),
    )
    low = list(WORD)
    for edge, (u, v) in enumerate(source.EDGES[14:], start=14):
        assert labels[u] == labels[v]
        low.append(maps[labels[u]][original[edge]])
    assert all(
        xor_all(
            low[edge]
            for edge, pair in enumerate(source.EDGES)
            if vertex in pair
        )
        == 0
        for vertex in range(source.ORDER)
    )
    return tuple(low)


def base_semantics():
    cycles, states, properties, minimum, minima = source.profile()
    assert len(cycles) == 1024 and len(states) == 384064
    ordered, clean = source.target_ordered_extension_counts(cycles)
    assert (ordered, clean, minimum, len(minima)) == (15360, 0, 5, 4)
    weights = (1,) * 14 + (2,) * 13
    liftable = tuple(mask for mask, row in properties.items() if row[0])
    values = tuple(
        sum(
            weights[edge]
            for edge in range(27)
            if (mask >> edge) & 1
        )
        for mask in liftable
    )
    assert min(values) == 7 and values.count(7) == 6
    print(
        "BASE_INDEPENDENT cycle_space=1024 semantic_states=384064"
        " target_extensions=15360 target_clean=0"
        " weighted_minimum=7 weighted_minima=6"
    )


def construct_inflation(low):
    edges = list(source.EDGES[:14])
    colours = list(low[:14])
    order = source.ORDER
    for edge in range(14, len(source.EDGES)):
        u, v = source.EDGES[edge]
        terminal = low[edge]
        other = tuple(value for value in (1, 2, 3) if value != terminal)
        previous = u
        for _ in range(CHAIN):
            a, b, r, s = range(order, order + 4)
            order += 4
            edges.append((previous, a))
            colours.append(terminal)
            edges.extend(((r, s), (a, r), (b, s), (a, s), (b, r)))
            colours.extend(
                (terminal, other[0], other[0], other[1], other[1])
            )
            previous = b
        edges.append((previous, v))
        colours.append(terminal)
    return order, tuple(edges), tuple(colours)


def distances(order, edges, deleted, root):
    graph = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        if edge in deleted:
            continue
        graph[u].append(v)
        graph[v].append(u)
    result = [-1] * order
    result[root] = 0
    queue = deque((root,))
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if result[v] < 0:
                result[v] = result[u] + 1
                queue.append(v)
    assert all(value >= 0 for value in result)
    return result


def t_join(order, edges, matching):
    terminals = tuple(vertex for edge in matching for vertex in edges[edge])
    metric = tuple(
        tuple(
            distances(order, edges, frozenset(matching), u)[v]
            for v in terminals
        )
        for u in terminals
    )

    @lru_cache(maxsize=None)
    def solve(mask):
        if mask == 0:
            return 0
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        return min(
            metric[first][second] + solve(rest ^ (1 << second))
            for second in range(len(terminals))
            if (rest >> second) & 1
        )

    return solve((1 << len(terminals)) - 1)


def inflation_audit():
    low = component_map_low()
    order, edges, colours = construct_inflation(low)
    assert (order, len(edges)) == (278, 417)
    assert len({tuple(sorted(edge)) for edge in edges}) == len(edges)
    degree = [0] * order
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    assert set(degree) == {3}
    assert all(
        xor_all(
            colours[edge]
            for edge, pair in enumerate(edges)
            if vertex in pair
        )
        == 0
        for vertex in range(order)
    )
    sizes = []
    joins = []
    for colour in range(4):
        matching = tuple(
            edge for edge in range(14) if WORD[edge] == colour
        )
        sizes.append(len(matching))
        joins.append(t_join(order, edges, matching))
    assert sizes == [3, 2, 4, 5]
    assert joins == [11, 12, 10, 9]
    print(
        "INFLATED_INDEPENDENT vertices=278 edges=417"
        f" class_sizes={tuple(sizes)} joins={tuple(joins)}"
        " containing_cycles=(14,14,14,14)"
    )


def main():
    abstract_check()
    base_semantics()
    inflation_audit()
    print("PASS independent rainbow/load survivor audit")


if __name__ == "__main__":
    main()
