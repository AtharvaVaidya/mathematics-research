#!/usr/bin/env python3
"""Independent small-order and six-state replay for the typed-cap audit."""

from __future__ import annotations

import itertools
import subprocess


LABELS = tuple((1 << a) | (1 << b) for a, b in itertools.combinations(range(5), 2))
LABEL_SET = frozenset(LABELS)


def decode_graph6(row: str) -> tuple[int, list[tuple[int, int]], list[list[int]]]:
    assert row and row[0] != "~"
    n = ord(row[0]) - 63
    bits: list[int] = []
    for char in row[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    incidence = [[] for _ in range(n)]
    for edge, (left, right) in enumerate(edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    assert all(len(items) == 3 for items in incidence)
    return n, edges, incidence


def enumerate_representatives(
    edges: list[tuple[int, int]], incidence: list[list[int]]
):
    """Enumerate all flows after fixing the first edge to 01.

    This deliberately does not use the C++ producer's S5 canonicalizer.
    It retains duplicates under the stabilizer of 01; duplicates do not
    affect an exact union of typed states.
    """

    state = [0] * len(edges)

    def assign(edge: int, label: int, trail: list[int]) -> bool:
        if state[edge]:
            return state[edge] == label
        if label not in LABEL_SET:
            return False
        state[edge] = label
        trail.append(edge)
        queue = list(edges[edge])
        while queue:
            vertex = queue.pop()
            row = incidence[vertex]
            assigned = [item for item in row if state[item]]
            if len(assigned) < 2:
                continue
            if len(assigned) == 3:
                if state[row[0]] ^ state[row[1]] ^ state[row[2]]:
                    return False
                continue
            missing = next(item for item in row if not state[item])
            forced = state[assigned[0]] ^ state[assigned[1]]
            if forced not in LABEL_SET:
                return False
            state[missing] = forced
            trail.append(missing)
            queue.extend(edges[missing])
        return True

    def visit():
        try:
            edge = next(index for index, label in enumerate(state) if not label)
        except StopIteration:
            yield tuple(state)
            return
        choices = (3,) if not any(state) else LABELS
        for label in choices:
            trail: list[int] = []
            if assign(edge, label, trail):
                yield from visit()
            for changed in reversed(trail):
                state[changed] = 0

    yield from visit()


def active_components(
    labels: tuple[int, ...], pair: int, edges: list[tuple[int, int]], incidence: list[list[int]]
) -> list[list[int]]:
    active = [((label & pair).bit_count() == 1) for label in labels]
    unseen = {edge for edge, flag in enumerate(active) if flag}
    answer: list[list[int]] = []
    while unseen:
        start = unseen.pop()
        stack = [start]
        component: list[int] = []
        while stack:
            edge = stack.pop()
            component.append(edge)
            for vertex in edges[edge]:
                for other in incidence[vertex]:
                    if other in unseen:
                        unseen.remove(other)
                        stack.append(other)
        answer.append(component)
    return answer


def typed_masks(n: int, edges: list[tuple[int, int]], incidence: list[list[int]]) -> list[int]:
    masks = {
        (z, root): 0
        for z in range(n)
        for root, endpoints in enumerate(edges)
        if z not in endpoints
    }
    for labels in enumerate_representatives(edges, incidence):
        for pair in LABELS:
            for component in active_components(labels, pair, edges, incidence):
                component_set = set(component)
                for z in range(n):
                    slots = [i for i, edge in enumerate(incidence[z]) if edge in component_set]
                    if len(slots) != 2:
                        continue
                    inactive = next(i for i in range(3) if i not in slots)
                    physical = {(0, 1): 0, (0, 2): 1, (1, 2): 2}[tuple(slots)]
                    third_label = labels[incidence[z][inactive]]
                    assert pair == third_label or not (pair & third_label)
                    mode = int(pair != third_label)
                    for root in component:
                        if z not in edges[root]:
                            masks[z, root] |= 1 << (2 * physical + mode)
    return list(masks.values())


def covers_ports(mask: int) -> bool:
    pair01, pair02, pair12 = mask & 3, mask & 12, mask & 48
    return bool((pair01 or pair02) and (pair01 or pair12) and (pair02 or pair12))


def double_star(mask: int) -> bool:
    full01, full02, full12 = mask & 3 == 3, mask & 12 == 12, mask & 48 == 48
    return (full01 and full02) or (full01 and full12) or (full02 and full12)


def graph6_rows(order: int) -> list[str]:
    run = subprocess.run(
        ["/opt/homebrew/bin/geng", "-Cq", "-d3", "-D3", str(order)],
        check=True,
        text=True,
        capture_output=True,
    )
    return [row for row in run.stdout.splitlines() if row and not row.startswith(">")]


def replay_small_orders() -> None:
    expected = {
        4: (1, 12, {47, 59, 62}),
        6: (2, 72, {47, 59, 62, 63}),
        8: (5, 360, {47, 51, 59, 60, 62, 63}),
        10: (18, 2160, {15, 47, 51, 59, 60, 62, 63}),
    }
    for order, (graph_count, interface_count, expected_masks) in expected.items():
        rows = graph6_rows(order)
        assert len(rows) == graph_count
        masks: list[int] = []
        for row in rows:
            n, edges, incidence = decode_graph6(row)
            assert n == order and len(edges) == 3 * order // 2
            masks.extend(typed_masks(n, edges, incidence))
        assert len(masks) == interface_count
        assert set(masks) == expected_masks
        assert all(covers_ports(mask) and double_star(mask) for mask in masks)
        print(f"PYTHON_EXACT order={order} graphs={len(rows)} interfaces={len(masks)} PASS")


def replay_algebra() -> None:
    # Every ordered connector triangle and physical pair has one internal
    # and two external factor choices.
    ordered_triangles = []
    for names in itertools.combinations(range(5), 3):
        triangle = tuple((1 << a) | (1 << b) for a, b in itertools.combinations(names, 2))
        ordered_triangles.extend(itertools.permutations(triangle))
    assert len(ordered_triangles) == 60
    for triangle in ordered_triangles:
        assert triangle[0] ^ triangle[1] ^ triangle[2] == 0
        for active_slots in ((0, 1), (0, 2), (1, 2)):
            inactive = next(i for i in range(3) if i not in active_slots)
            choices = [
                pair
                for pair in LABELS
                if all((pair & triangle[i]).bit_count() == 1 for i in active_slots)
                and (pair & triangle[inactive]).bit_count() != 1
            ]
            internal = [pair for pair in choices if pair == triangle[inactive]]
            external = [pair for pair in choices if not (pair & triangle[inactive])]
            assert len(choices) == 3 and len(internal) == 1 and len(external) == 2

    masks = range(64)
    stars = [mask for mask in masks if double_star(mask)]
    covers = [mask for mask in masks if covers_ports(mask)]
    assert all(first & second for first in stars for second in stars)
    assert all(first & second for first in stars for second in covers)
    print("ALGEBRA ordered_triangles=60 double_star_gluing=PASS one_sided_gluing=PASS")


if __name__ == "__main__":
    replay_algebra()
    replay_small_orders()
    print("PASS")
