#!/usr/bin/env python3
"""Primary exact verifier for the balanced rainbow/load counterstate."""

from functools import reduce
from itertools import permutations, product
from operator import xor
from pathlib import Path
from shutil import which
from subprocess import run

SUPPORT = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
SPOKES = [(0, 6), (2, 6), (4, 6), (1, 7), (3, 7), (5, 7)]
EDGES = SUPPORT + SPOKES
R = (1, 0, 2, 0, 3, 0)
G = (1, 1, 2, 2, 3, 3)
EPS = (0, 1, 0, 1, 0, 1)
SPOKE_VALUES = (1, 2, 3, 1, 2, 3)


def xor_all(values):
    return reduce(xor, values, 0)


assert tuple(R[i - 1] ^ R[i] for i in range(6)) == G
assert xor_all(G) == 0
assert xor_all(g for g, e in zip(G, EPS) if e) == 0
assert xor_all(g for g, e in zip(G, EPS) if not e) == 0
assert set(R) == set(range(4))
assert [R.count(c) & 1 for c in range(4)] == [1, 1, 1, 1]

# Graph premises and flow conservation.
inc = [[] for _ in range(8)]
for edge_id, (u, v) in enumerate(EDGES):
    assert u != v
    inc[u].append(edge_id)
    inc[v].append(edge_id)
assert len(set(tuple(sorted(e)) for e in EDGES)) == len(EDGES)
assert all(len(row) == 3 for row in inc)

first = (1,) * 6 + (0,) * 6
low = R + SPOKE_VALUES
for v in range(8):
    assert xor_all(first[e] for e in inc[v]) == 0
    assert xor_all(low[e] for e in inc[v]) == 0
assert all(first[e] or low[e] for e in range(12))


def connected_without(skip=None):
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for edge_id, (a, b) in enumerate(EDGES):
            if edge_id == skip:
                continue
            if a == u and b not in seen:
                seen.add(b)
                stack.append(b)
            elif b == u and a not in seen:
                seen.add(a)
                stack.append(a)
    return len(seen) == 8


assert connected_without()
assert all(connected_without(edge_id) for edge_id in range(12))


def graph6():
    bits = []
    edge_set = {tuple(sorted(edge)) for edge in EDGES}
    for upper in range(1, 8):
        for lower in range(upper):
            bits.append(int((lower, upper) in edge_set))
    while len(bits) % 6:
        bits.append(0)
    return chr(8 + 63) + "".join(
        chr(63 + sum(bits[offset + j] << (5 - j) for j in range(6)))
        for offset in range(0, len(bits), 6)
    )


here = Path(__file__).resolve().parent
assert graph6() == (here / "labelled.g6").read_text().strip() == "GhELQg"
if which("labelg"):
    canonical = run(
        ["labelg", "-q"],
        input=graph6() + "\n",
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    assert canonical == (here / "canonical.g6").read_text().strip() == "Gs@ipo"

# Explicit Tait colouring.
tait = (1, 2, 1, 3, 2, 3, 2, 3, 1, 3, 2, 1)
for v in range(8):
    assert sorted(tait[e] for e in inc[v]) == [1, 2, 3]

# All six selected-component maps and all four circuit translations.
maps = [(0,) + perm for perm in permutations((1, 2, 3))]
map_rows = []
clean_states = 0
dirty_states = 0
for mapping in maps:
    transformed = tuple(mapping[g] if e else g for g, e in zip(G, EPS))
    assert xor_all(transformed) == 0
    zero_word = []
    previous = 0
    for derivative in transformed:
        previous ^= derivative
        zero_word.append(previous)
    assert previous == 0
    row_parities = set()
    row_colour_counts = set()
    for translation in range(4):
        word = tuple(value ^ translation for value in zero_word)
        parity = tuple(word.count(c) & 1 for c in range(4))
        row_parities.add(parity)
        row_colour_counts.add(len(set(word)))
        if parity == (0, 0, 0, 0):
            clean_states += 1
        else:
            assert parity == (1, 1, 1, 1)
            dirty_states += 1
    assert len(row_parities) == len(row_colour_counts) == 1
    map_rows.append(
        ("".join(map(str, mapping)), "".join(map(str, zero_word)),
         next(iter(row_parities)), next(iter(row_colour_counts)))
    )
assert clean_states == 16 and dirty_states == 8

# Exhaust the minimally connected two-component, one-circuit subclass.
census = {}
for length in range(4, 7):
    total = safe = 0
    histogram = {}
    for derivative in product((1, 2, 3), repeat=length):
        if xor_all(derivative):
            continue
        support = []
        value = 0
        for item in derivative:
            value ^= item
            support.append(value)
        if len(set(support)) < 4:
            continue
        for shore in product((0, 1), repeat=length):
            inside_size = sum(shore)
            if inside_size < 2 or length - inside_size < 2:
                continue
            if xor_all(
                item for item, selected in zip(derivative, shore) if selected
            ):
                continue
            rainbow = sum(
                shore[i] != shore[(i + 1) % length] and support[i] == 3
                for i in range(length)
            ) & 1
            if not rainbow:
                continue
            inside = [
                sum(selected and item == colour
                    for selected, item in zip(shore, derivative))
                for colour in (1, 2, 3)
            ]
            outside = [
                sum((not selected) and item == colour
                    for selected, item in zip(shore, derivative))
                for colour in (1, 2, 3)
            ]
            load = max(inside) + max(outside)
            threshold = 2 * (length - 4)
            total += 1
            histogram[load] = histogram.get(load, 0) + 1
            safe += load <= threshold
    census[length] = (total, safe, histogram)

assert census == {
    4: (12, 0, {4: 12}),
    5: (120, 0, {3: 120}),
    6: (960, 888, {6: 72, 4: 576, 2: 312}),
}

print(
    "PASS:",
    "vertices=8 edges=12 bridges=0",
    f"clean_map_translation_states={clean_states}",
    f"dirty_map_translation_states={dirty_states}",
    f"census={census}",
)
