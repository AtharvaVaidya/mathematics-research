#!/usr/bin/env python3
"""Independent literal audit using binary matrices and cut enumeration."""

from itertools import product

edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
    (0, 6), (2, 6), (4, 6), (1, 7), (3, 7), (5, 7),
]
support_low = [1, 0, 2, 0, 3, 0]
spoke_low = [1, 2, 3, 1, 2, 3]
low = support_low + spoke_low
first = [1] * 6 + [0] * 6


def apply(matrix, x):
    a, b = (x >> 1) & 1, x & 1
    return (
        (((matrix[0] * a + matrix[1] * b) & 1) << 1)
        | ((matrix[2] * a + matrix[3] * b) & 1)
    )


gl = []
for matrix in product(range(2), repeat=4):
    image = tuple(apply(matrix, x) for x in range(4))
    if set(image) == set(range(4)):
        gl.append(image)
assert len(gl) == 6

# Direct vertex xor, degree, and every edge-deletion connectivity check.
for vertex in range(8):
    incident = [i for i, edge in enumerate(edges) if vertex in edge]
    assert len(incident) == 3
    assert first[incident[0]] ^ first[incident[1]] ^ first[incident[2]] == 0
    assert low[incident[0]] ^ low[incident[1]] ^ low[incident[2]] == 0

for removed in range(-1, len(edges)):
    reachable = {0}
    changed = True
    while changed:
        changed = False
        for i, (u, v) in enumerate(edges):
            if i == removed:
                continue
            if u in reachable and v not in reachable:
                reachable.add(v)
                changed = True
            if v in reachable and u not in reachable:
                reachable.add(u)
                changed = True
    assert reachable == set(range(8))

# Cut and derivative calculations from the literal edge list.
shore = {1, 3, 5, 7}
cut = [
    i for i, (u, v) in enumerate(edges)
    if (u in shore) != (v in shore)
]
assert cut == list(range(6))
assert [sum(low[i] == c for i in cut) & 1 for c in range(4)] == [1, 1, 1, 1]

derivative = [
    support_low[i - 1] ^ support_low[i]
    for i in range(6)
]
assert derivative == [1, 1, 2, 2, 3, 3]
inside = [derivative[i] for i in (1, 3, 5)]
outside = [derivative[i] for i in (0, 2, 4)]
assert inside[0] ^ inside[1] ^ inside[2] == 0
assert outside[0] ^ outside[1] ^ outside[2] == 0
assert [inside.count(c) for c in (1, 2, 3)] == [1, 1, 1]
assert [outside.count(c) for c in (1, 2, 3)] == [1, 1, 1]
assert 2 <= 2 * (8 - 6)

# Independently integrate every matrix image on the selected star.
profiles = {}
for image in gl:
    changed = [
        image[derivative[i]] if i in (1, 3, 5) else derivative[i]
        for i in range(6)
    ]
    assert changed[0] ^ changed[1] ^ changed[2] ^ changed[3] ^ changed[4] ^ changed[5] == 0
    word = []
    value = 0
    for item in changed:
        value ^= item
        word.append(value)
    parity = tuple(word.count(c) & 1 for c in range(4))
    profiles["".join(map(str, image))] = parity

assert sorted(profiles.values()).count((0, 0, 0, 0)) == 4
assert sorted(profiles.values()).count((1, 1, 1, 1)) == 2

print(
    "PASS:",
    f"GL_matrices={len(gl)}",
    "literal_cut=rainbow",
    "inside_counts=111 outside_counts=111",
    "load=2 threshold=4",
    "clean_maps=4 dirty_maps=2",
)
