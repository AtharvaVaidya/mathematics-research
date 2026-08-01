#!/usr/bin/env python3
"""Semantic replay for the factor-splice lemmas and finite delimiters."""

from __future__ import annotations

import base64
from itertools import combinations
from pathlib import Path
import zlib


HERE = Path(__file__).resolve().parent
FIXED = HERE.parent / "d5-external-port-coverage-frontier-20260731"
PAIRS = tuple((1 << a) | (1 << b) for a, b in combinations(range(5), 2))
PETERSEN = (
    (0, 1), (1, 2), (2, 3), (0, 4), (3, 4),
    (0, 5), (1, 6), (2, 7), (5, 7), (3, 8),
    (5, 8), (6, 8), (4, 9), (6, 9), (7, 9),
)
LCF = (17, -9, 37, -37, 9, -17) * 15
FOSTER_PORTS = (1, 17, 89)


def graph6(word: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    n = ord(word[0]) - 63
    bits = []
    for char in word[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges, cursor = [], 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return n, tuple(edges)


def petersen_foster() -> tuple[int, tuple[tuple[int, int], ...]]:
    foster = set()
    for vertex in range(90):
        for other in ((vertex + 1) % 90, (vertex + LCF[vertex]) % 90):
            foster.add(tuple(sorted((vertex, other))))
    edges = []
    for copy in range(10):
        edges.extend((89 * copy + left - 1, 89 * copy + right - 1)
                     for left, right in foster if 0 not in (left, right))
    used = [0] * 10
    for left, right in PETERSEN:
        a = 89 * left + FOSTER_PORTS[used[left]] - 1
        b = 89 * right + FOSTER_PORTS[used[right]] - 1
        used[left] += 1
        used[right] += 1
        edges.append(tuple(sorted((a, b))))
    assert len(foster) == 135 and used == [3] * 10
    return 890, tuple(sorted(edges))


def incidence(n: int, edges: tuple[tuple[int, int], ...]) -> list[list[int]]:
    rows = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return rows


def check_flow(n: int, edges: tuple[tuple[int, int], ...], labels) -> list[list[int]]:
    rows = incidence(n, edges)
    assert len(labels) == len(edges)
    assert len(edges) == len(set(edges)) and all(left != right for left, right in edges)
    assert all(len(row) == 3 for row in rows)
    assert all(label in PAIRS for label in labels)
    assert all(labels[a] ^ labels[b] ^ labels[c] == 0 for a, b, c in rows)
    return rows


def components(edges, rows, labels, pair: int) -> list[frozenset[int]]:
    active = [((label & pair).bit_count() == 1) for label in labels]
    seen: set[int] = set()
    answer = []
    for start in range(len(edges)):
        if not active[start] or start in seen:
            continue
        found, todo = {start}, [start]
        while todo:
            edge = todo.pop()
            for vertex in edges[edge]:
                local = [other for other in rows[vertex] if active[other]]
                assert len(local) == 2
                for other in local:
                    if other not in found:
                        found.add(other)
                        todo.append(other)
        seen.update(found)
        answer.append(frozenset(found))
    return answer


def root_component(edges, rows, labels, pair: int, root: int) -> frozenset[int]:
    assert (labels[root] & pair).bit_count() == 1
    return next(found for found in components(edges, rows, labels, pair)
                if root in found)


def switch(labels, pair: int, component) -> tuple[int, ...]:
    answer = list(labels)
    for edge in component:
        assert (answer[edge] & pair).bit_count() == 1
        answer[edge] ^= pair
        assert answer[edge] in PAIRS
    return tuple(answer)


def active_set(labels, pair: int) -> frozenset[int]:
    return frozenset(edge for edge, label in enumerate(labels)
                     if (label & pair).bit_count() == 1)


def audit_splice_law(edges, rows, labels) -> int:
    moves = 0
    for switch_pair in PAIRS:
        for component in components(edges, rows, labels, switch_pair):
            changed = switch(labels, switch_pair, component)
            for factor in PAIRS:
                before, after = active_set(labels, factor), active_set(changed, factor)
                expected = (before ^ component
                            if (factor & switch_pair).bit_count() == 1
                            else before)
                assert after == expected
            moves += 1
    return moves


def typed_mask(edges, rows, labels, z: int, root: int) -> int:
    ports = rows[z]
    answer = 0
    for pair in PAIRS:
        if (labels[root] & pair).bit_count() != 1:
            continue
        found = root_component(edges, rows, labels, pair, root)
        slots = tuple(slot for slot, edge in enumerate(ports) if edge in found)
        if len(slots) != 2:
            assert not slots
            continue
        physical = {(0, 1): 0, (0, 2): 1, (1, 2): 2}[slots]
        inactive_slot = next(slot for slot in range(3) if slot not in slots)
        inactive = labels[ports[inactive_slot]]
        if inactive == pair:
            mode = 0
        else:
            assert inactive & pair == 0
            mode = 1
        answer |= 1 << (2 * physical + mode)
    return answer


def external_port_mask(edges, rows, labels, z: int, root: int):
    ports, answer, witnesses = rows[z], 0, []
    for pair in PAIRS:
        if (labels[root] & pair).bit_count() != 1:
            continue
        found = root_component(edges, rows, labels, pair, root)
        slots = tuple(slot for slot, edge in enumerate(ports) if edge in found)
        if len(slots) != 2:
            assert not slots
            continue
        inactive_slot = next(slot for slot in range(3) if slot not in slots)
        if labels[ports[inactive_slot]] & pair:
            continue
        for slot in slots:
            answer |= 1 << slot
        witnesses.append((pair, slots, len(found)))
    return answer, tuple(witnesses)


def audit_matching_characterization(edges, rows, labels) -> None:
    for pair in PAIRS:
        matching = {edge for edge, label in enumerate(labels) if label == pair}
        assert all(sum(edge in matching for edge in row) <= 1 for row in rows)
        outside = tuple(coordinate for coordinate in range(5)
                        if not (pair >> coordinate) & 1)
        factor = active_set(labels, pair)
        factor_components = components(edges, rows, labels, pair)
        endpoints = {vertex for edge in matching for vertex in edges[edge]}
        assert all(sum(edge in factor for edge in rows[vertex]) == 2
                   for vertex in endpoints)
        for component in factor_components:
            vertices = {vertex for edge in component for vertex in edges[edge]}
            assert len(vertices & endpoints) % 2 == 0
        for edge, label in enumerate(labels):
            if edge in matching:
                continue
            cover_count = int(edge in factor)
            cover_count += sum((label >> coordinate) & 1
                               for coordinate in outside)
            assert cover_count == 2


def audit_petersen_foster() -> None:
    n, edges = petersen_foster()
    encoded = (FIXED / "pf-fixed-flow-labels.b85").read_bytes().strip()
    labels = zlib.decompress(base64.b85decode(encoded))
    rows = check_flow(n, edges, labels)
    z, root = 0, 552
    assert tuple(rows[z]) == (0, 1, 2)
    assert typed_mask(edges, rows, labels, z, root) == 6
    assert external_port_mask(edges, rows, labels, z, root)[0] == 3
    audit_matching_characterization(edges, rows, labels)
    assert audit_splice_law(edges, rows, labels) == 124

    expected = (
        (10, 0, 46, False, (0, 1), 6, (1, 2), 517, 6),
        (10, 1, 463, True, (), 12, (1, 2), 455, 6),
        (20, 0, 275, False, (0, 1), 17, (1, 2), 549, 7),
        (20, 1, 265, False, (), 17, (0, 2), 601, 7),
        (20, 5, 46, True, (), 5, (1, 2), 444, 7),
        (24, 6, 48, True, (), 12, (1, 2), 408, 7),
    )
    repairs = []
    for pair in PAIRS:
        for index, component in enumerate(components(edges, rows, labels, pair)):
            changed = switch(labels, pair, component)
            check_flow(n, edges, changed)
            mask, witnesses = external_port_mask(edges, rows, changed, z, root)
            selected = [item for item in witnesses if 2 in item[1]]
            if not selected:
                continue
            assert len(selected) == 1
            factor, slots, size = selected[0]
            cap_slots = tuple(slot for slot, edge in enumerate(rows[z])
                              if edge in component)
            repairs.append((pair, index, len(component), root in component,
                            cap_slots, factor, slots, size, mask))
    assert tuple(repairs) == expected
    assert sum(item[-1] == 7 for item in repairs) == 4

    internal = root_component(edges, rows, labels, 6, root)
    def trace(start_vertex: int) -> tuple[int, ...]:
        sequence, previous, vertex = [root], root, start_vertex
        while vertex != z:
            following = next(edge for edge in rows[vertex]
                             if edge in internal and edge != previous)
            sequence.append(following)
            left, right = edges[following]
            vertex = right if vertex == left else left
            previous = following
        return tuple(sequence)
    arcs = tuple(trace(vertex) for vertex in edges[root])
    stabilizers = components(edges, rows, labels, 24)
    entangled = []
    for arc in arcs:
        count = 0
        for component in stabilizers:
            colours = {(labels[edge] & ~6).bit_length() - 1
                       for edge in component & frozenset(arc)}
            if colours == {3, 4}:
                count += 1
        entangled.append(count)
    assert tuple(entangled) == (6, 7)
    print("MATCHING_CHARACTERIZATION factors=10 PASS")
    print("PF_SPLICE moves=124 selected_port_repairs=6 simultaneous_all_ports=4 entangled_arcs=6,7 PASS")


def audit_depth_two_external() -> None:
    labels = (3, 5, 6, 5, 3, 6, 6, 5, 3, 6, 3, 5)
    n, edges = graph6("G?zTb_")
    rows = check_flow(n, edges, labels)
    z, root, selected = 0, 10, 1
    assert external_port_mask(edges, rows, labels, z, root)[0] == 5
    assert audit_splice_law(edges, rows, labels) == 12
    neighbours = []
    for pair in PAIRS:
        for component in components(edges, rows, labels, pair):
            changed = switch(labels, pair, component)
            assert not (external_port_mask(edges, rows, changed, z, root)[0]
                        & (1 << selected))
            neighbours.append(changed)
    assert len(neighbours) == 12
    first_component = frozenset((0, 1, 3, 4))
    assert first_component in components(edges, rows, labels, 9)
    first = switch(labels, 9, first_component)
    second_component = frozenset((0, 2, 6, 7))
    assert second_component in components(edges, rows, first, 3)
    final = switch(first, 3, second_component)
    assert final == (9, 12, 5, 12, 10, 6, 5, 6, 3, 6, 3, 5)
    mask, witnesses = external_port_mask(edges, rows, final, z, root)
    assert mask == 7 and (6, (1, 2), 8) in witnesses
    print("DEPTH2_SELECTED graph6=G?zTb_ zero_one_switch=UNREACHED two_switch=CHECKED final_all_ports=1 PASS")


def audit_depth_two_mode_flip() -> None:
    labels = (3, 5, 12, 10, 3, 9, 6, 20, 18, 9, 24, 17)
    n, edges = graph6("GCZJd_")
    rows = check_flow(n, edges, labels)
    z, root, physical = 0, 4, 1
    assert typed_mask(edges, rows, labels, z, root) == 7
    assert audit_splice_law(edges, rows, labels) == 12
    neighbours = []
    for pair in PAIRS:
        for component in components(edges, rows, labels, pair):
            changed = switch(labels, pair, component)
            assert not (typed_mask(edges, rows, changed, z, root)
                        & (1 << (2 * physical + 1)))
            neighbours.append(changed)
    assert len(neighbours) == 12
    first_component = frozenset((0, 9, 11))
    assert first_component in components(edges, rows, labels, 5)
    first = switch(labels, 5, first_component)
    second_component = frozenset((1, 4, 5))
    assert second_component in components(edges, rows, first, 17)
    final = switch(first, 17, second_component)
    assert final == (6, 20, 12, 10, 18, 24, 6, 20, 18, 12, 24, 20)
    assert typed_mask(edges, rows, final, z, root) == 62
    mask, witnesses = external_port_mask(edges, rows, final, z, root)
    assert mask == 7 and (20, (0, 2), 8) in witnesses
    print("DEPTH2_MODE graph6=GCZJd_ internal_pair=02 zero_one_external=UNREACHED two_switch=CHECKED final_all_ports=1 PASS")


def main() -> None:
    audit_petersen_foster()
    audit_depth_two_external()
    audit_depth_two_mode_flip()
    print("PASS")


if __name__ == "__main__":
    main()
