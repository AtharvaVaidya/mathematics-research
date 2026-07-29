#!/usr/bin/env python3
"""Primary literal verifier for full-flow exchange and the 278v witness."""

from collections import Counter

BASE_EDGES = (
    tuple((i, (i + 1) % 7) for i in range(7))
    + tuple((7 + i, 7 + (i + 1) % 7) for i in range(7))
    + (
        (0, 11), (1, 9), (2, 12), (3, 10),
        (14, 4), (14, 5), (14, 15), (15, 6), (15, 16),
        (16, 13), (16, 17), (17, 7), (17, 8),
    )
)
BASE_ORDER = 18
CHAIN = 5
DISPLAY_LOW = tuple(map(int, "3231320" "1320320" "3112213212312"))
DISPLAY_FIRST = (1,) * 14 + (0,) * 13
DISPLAY_FLOW = tuple(
    first | (low << 1)
    for first, low in zip(DISPLAY_FIRST, DISPLAY_LOW)
)
COMPETING_FLOW = (
    3, 1, 3, 7, 5, 1, 5,
    6, 4, 6, 2, 4, 6, 2,
    6, 2, 2, 4, 2, 4, 6, 4, 2, 4, 6, 4, 2,
)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def adjacency(order, edges):
    graph = [[] for _ in range(order)]
    for edge, (u, v) in enumerate(edges):
        graph[u].append((v, edge))
        graph[v].append((u, edge))
    return graph


def verify_flow(order, edges, values):
    assert len(values) == len(edges)
    assert all(value != 0 for value in values)
    graph = adjacency(order, edges)
    assert all(
        xor_all(values[edge] for _other, edge in row) == 0
        for row in graph
    )


assert DISPLAY_FLOW == (
    7, 5, 7, 3, 7, 5, 1,
    3, 7, 5, 1, 7, 5, 1,
    6, 2, 2, 4, 4, 2, 6, 4, 2, 4, 6, 2, 4,
)
verify_flow(BASE_ORDER, BASE_EDGES, DISPLAY_FLOW)
verify_flow(BASE_ORDER, BASE_EDGES, COMPETING_FLOW)

display_support = {edge for edge, value in enumerate(DISPLAY_FLOW) if value & 1}
competing_support = {edge for edge, value in enumerate(COMPETING_FLOW) if value & 1}
assert display_support == set(range(14))
assert competing_support == set(range(7))

difference = tuple(f ^ g for f, g in zip(DISPLAY_FLOW, COMPETING_FLOW))
assert difference == (
    4, 4, 4, 4, 2, 4, 4,
    5, 3, 3, 3, 3, 3, 3,
    0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 6, 6,
)
assert all(d != f for d, f in zip(difference, DISPLAY_FLOW))
assert set(difference) - {0} == {2, 3, 4, 5, 6}

a = tuple(value & 1 for value in difference)
b = tuple(value >> 1 for value in difference)
assert "".join(map(str, a)) == "000000011111110000000000000"
assert (
    "".join(map(str, b[:7])),
    "".join(map(str, b[7:14])),
    "".join(map(str, b[14:])),
) == ("2222122", "2111111", "0000330000033")
assert xor_all(a[edge] for edge in range(7)) == 0
assert sum(a[edge] for edge in display_support) == 7
assert sum(a[edge] for edge in range(14, 27)) == 0

competing_low = tuple(value >> 1 for value in COMPETING_FLOW)
zero_set = {edge for edge, value in enumerate(competing_low) if value == 0}
matching = {1, 5}
join = {0, 2, 3, 4, 6}
assert zero_set == matching
assert matching | join == competing_support
assert not matching & join


def boundary(edge_set):
    result = set()
    for edge in edge_set:
        for vertex in BASE_EDGES[edge]:
            if vertex in result:
                result.remove(vertex)
            else:
                result.add(vertex)
    return result


assert boundary(matching) == boundary(join)
assert len(matching) + len(join) == 7

# The new low flow is outside the four affine rebases s+c*h: it differs
# from DISPLAY_LOW on complement edges.
assert any(
    competing_low[edge] != DISPLAY_LOW[edge]
    for edge in range(14, 27)
)


def inflate(base_low, base_first):
    edges = list(BASE_EDGES[:14])
    values = [
        base_first[edge] | (base_low[edge] << 1)
        for edge in range(14)
    ]
    order = BASE_ORDER
    for base_edge in range(14, 27):
        u, v = BASE_EDGES[base_edge]
        terminal = base_low[base_edge]
        assert terminal in (1, 2, 3)
        other = [value for value in (1, 2, 3) if value != terminal]
        previous = u
        for _ in range(CHAIN):
            aa, bb, rr, ss = range(order, order + 4)
            order += 4
            edges.append((previous, aa))
            values.append(terminal << 1)
            edges.extend(((rr, ss), (aa, rr), (bb, ss), (aa, ss), (bb, rr)))
            values.extend(
                (
                    terminal << 1,
                    other[0] << 1, other[0] << 1,
                    other[1] << 1, other[1] << 1,
                )
            )
            previous = bb
        edges.append((previous, v))
        values.append(terminal << 1)
    return order, tuple(edges), tuple(values)


display_order, inflated_edges, inflated_f = inflate(
    DISPLAY_LOW, DISPLAY_FIRST
)
competing_order, competing_edges, inflated_g = inflate(
    competing_low, tuple(value & 1 for value in COMPETING_FLOW)
)
assert display_order == competing_order == 278
assert inflated_edges == competing_edges
assert len(inflated_edges) == 417
verify_flow(278, inflated_edges, inflated_f)
verify_flow(278, inflated_edges, inflated_g)

inflated_d = tuple(f ^ g for f, g in zip(inflated_f, inflated_g))
assert all(d != f for d, f in zip(inflated_d, inflated_f))
assert sum(value & 1 for value in inflated_f) == 14
assert sum(value & 1 for value in inflated_g) == 7

print(
    "PASS:",
    "base_vertices=18 base_edges=27",
    "inflated_vertices=278 inflated_edges=417",
    "display_support=14 competitor_support=7 gain=7",
    "zero_matching=1,5 join=0,2,3,4,6",
    f"difference_nonzero_values={sorted(set(difference)-{0})}",
)
