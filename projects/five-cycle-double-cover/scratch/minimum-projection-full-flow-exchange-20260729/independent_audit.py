#!/usr/bin/env python3
"""Independent audit of the master triple and relative edge conditions."""

from itertools import product

edges = (
    [(i, (i + 1) % 7) for i in range(7)]
    + [(7 + i, 7 + (i + 1) % 7) for i in range(7)]
    + [
        (0, 11), (1, 9), (2, 12), (3, 10),
        (14, 4), (14, 5), (14, 15), (15, 6), (15, 16),
        (16, 13), (16, 17), (17, 7), (17, 8),
    ]
)
old_low = [int(x) for x in "323132013203203112213212312"]
old_h = [1] * 14 + [0] * 13
new_values = [
    3, 1, 3, 7, 5, 1, 5, 6, 4, 6, 2, 4, 6, 2,
    6, 2, 2, 4, 2, 4, 6, 4, 2, 4, 6, 4, 2,
]
old_values = [bit | (value << 1) for bit, value in zip(old_h, old_low)]


def parity(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


for values in (old_values, new_values):
    for vertex in range(18):
        incident = [edge for edge, pair in enumerate(edges) if vertex in pair]
        assert len(incident) == 3
        assert parity(values[edge] for edge in incident) == 0
    assert all(values)

new_h = [value & 1 for value in new_values]
new_low = [value >> 1 for value in new_values]
d_first = [old_h[e] ^ new_h[e] for e in range(27)]
d_low = [old_low[e] ^ new_low[e] for e in range(27)]

# Independently check that both coordinates of the difference are flows.
for vertex in range(18):
    incident = [edge for edge, pair in enumerate(edges) if vertex in pair]
    assert parity(d_first[edge] for edge in incident) == 0
    assert parity(d_low[edge] for edge in incident) == 0

# Edgewise admissibility in the theorem's exact form.
for edge in range(27):
    if d_first[edge] == old_h[edge]:
        assert d_low[edge] != old_low[edge]

gain = sum(
    1 if d_first[edge] and old_h[edge] else -1
    if d_first[edge] else 0
    for edge in range(27)
)
assert gain == 7

M = {edge for edge, value in enumerate(new_low) if value == 0}
J = {0, 2, 3, 4, 6}
assert M == {1, 5}
assert not M & J

degree_m = [0] * 18
degree_j = [0] * 18
for edge in M:
    for vertex in edges[edge]:
        degree_m[vertex] ^= 1
for edge in J:
    for vertex in edges[edge]:
        degree_j[vertex] ^= 1
assert degree_m == degree_j
assert sum(len([edge for edge in M if vertex in edges[edge]]) > 1 for vertex in range(18)) == 0
assert len(M) + len(J) == 7

# Exhaustively audit the local Boolean equivalence behind the master
# encoding: m iff p=q=0, disjoint m/j, and equal local parity make m+j
# an even first-coordinate incidence.
local_rows = 0
for low_bits in product(range(4), repeat=3):
    if parity(low_bits):
        continue
    m = tuple(value == 0 for value in low_bits)
    for j in product(range(2), repeat=3):
        if any(m[i] and j[i] for i in range(3)):
            continue
        if parity(m) != parity(j):
            continue
        h = tuple(int(m[i] or j[i]) for i in range(3))
        assert parity(h) == 0
        assert all(h[i] or low_bits[i] for i in range(3))
        local_rows += 1


# Reconstruct the literal inflation independently.  A local pole is
# described by its incidence/value table rather than by the primary
# checker's construction routine.
def expanded_instance(base_values):
    expanded_edges = list(edges[:14])
    expanded_values = list(base_values[:14])
    order = 18
    local_pattern = (
        (2, 3, 0),  # r-s has the terminal colour
        (0, 2, 1),  # a-r and b-s have the first other colour
        (1, 3, 1),
        (0, 3, 2),  # a-s and b-r have the second other colour
        (1, 2, 2),
    )
    for base_edge in range(14, 27):
        left, right = edges[base_edge]
        terminal_full = base_values[base_edge]
        assert terminal_full in (2, 4, 6)
        terminal = terminal_full >> 1
        other = tuple(value for value in (1, 2, 3) if value != terminal)
        colours = (terminal, other[0], other[1])
        previous = left
        for _copy in range(5):
            vertices = tuple(range(order, order + 4))
            order += 4
            expanded_edges.append((previous, vertices[0]))
            expanded_values.append(terminal_full)
            for first, second, colour_class in local_pattern:
                expanded_edges.append((vertices[first], vertices[second]))
                expanded_values.append(colours[colour_class] << 1)
            previous = vertices[1]
        expanded_edges.append((previous, right))
        expanded_values.append(terminal_full)
    return order, tuple(expanded_edges), tuple(expanded_values)


def audit_expanded_flow(order, expanded_edges, values):
    assert len(expanded_edges) == len(values)
    assert all(values)
    incident = [[] for _ in range(order)]
    for edge, (first, second) in enumerate(expanded_edges):
        assert first != second
        incident[first].append(edge)
        incident[second].append(edge)
    assert {len(row) for row in incident} == {3}
    assert all(parity(values[edge] for edge in row) == 0 for row in incident)


old_order, old_expanded_edges, old_expanded_values = expanded_instance(
    old_values
)
new_order, new_expanded_edges, new_expanded_values = expanded_instance(
    new_values
)
assert old_order == new_order == 278
assert old_expanded_edges == new_expanded_edges
assert len(old_expanded_edges) == 417
assert len({tuple(sorted(edge)) for edge in old_expanded_edges}) == 417
audit_expanded_flow(old_order, old_expanded_edges, old_expanded_values)
audit_expanded_flow(new_order, new_expanded_edges, new_expanded_values)
assert sum(value & 1 for value in old_expanded_values) == 14
assert sum(value & 1 for value in new_expanded_values) == 7
expanded_difference = tuple(
    old ^ new
    for old, new in zip(old_expanded_values, new_expanded_values)
)
assert all(
    difference_value != old_value
    for difference_value, old_value
    in zip(expanded_difference, old_expanded_values)
)

# Check connectedness and bridgelessness without importing the primary
# graph checker.
expanded_adjacency = [[] for _ in range(old_order)]
for edge, (first, second) in enumerate(old_expanded_edges):
    expanded_adjacency[first].append((second, edge))
    expanded_adjacency[second].append((first, edge))


def reaches_all(omitted):
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour, edge in expanded_adjacency[vertex]:
            if edge == omitted or neighbour in seen:
                continue
            seen.add(neighbour)
            stack.append(neighbour)
    return len(seen) == old_order


assert reaches_all(None)
assert all(reaches_all(edge) for edge in range(len(old_expanded_edges)))

print(
    "PASS:",
    "relative_gain=7",
    "M=1,5 J=0,2,3,4,6",
    "difference_coordinates_are_flows=1",
    f"master_local_rows={local_rows}",
    "inflated_vertices=278 inflated_edges=417",
    "inflated_supports=14,7 bridgeless=1",
)
