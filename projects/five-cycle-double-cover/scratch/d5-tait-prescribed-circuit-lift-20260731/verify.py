#!/usr/bin/env python3
"""Standard-library semantic replay of the Tait prescribed-circuit lift."""

from __future__ import annotations

from itertools import combinations


def prism(n: int) -> tuple[int, list[tuple[int, int]], dict[tuple[int, int], int]]:
    assert n >= 3
    edges: list[tuple[int, int]] = []
    colour: dict[tuple[int, int], int] = {}

    def add(u: int, v: int, c: int) -> None:
        edge = tuple(sorted((u, v)))
        assert edge not in colour
        edges.append(edge)
        colour[edge] = c

    # Even prisms have the immediate alternating colouring.  For odd n,
    # use the standard colouring in which both rims alternate except at
    # one edge and the spoke colours compensate.
    if n % 2 == 0:
        for layer in range(2):
            for i in range(n):
                add(layer * n + i, layer * n + (i + 1) % n, 2 + i % 2)
        for i in range(n):
            add(i, n + i, 4)
    else:
        # A triangular prism is Tait-colourable, but the general odd prism
        # is not cubic-bipartite in the same pattern.  Use only n=3 here.
        assert n == 3
        for i in range(3):
            add(i, (i + 1) % 3, 2 + i)
            add(3 + i, 3 + (i + 1) % 3, 2 + i)
            add(i, 3 + i, 2 + ((i + 1) % 3))
        # The preceding spoke assignment is not proper; replace it by the
        # colour missing at each corresponding rim vertex.
        for i in range(3):
            edge = (i, 3 + i)
            incident = {
                colour[tuple(sorted((i, (i - 1) % 3)))],
                colour[tuple(sorted((i, (i + 1) % 3)))],
            }
            colour[edge] = ({2, 3, 4} - incident).pop()
    edges = sorted(colour)
    return 2 * n, edges, colour


def incidence(order: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    rows = [[] for _ in range(order)]
    for eid, (u, v) in enumerate(edges):
        rows[u].append(eid)
        rows[v].append(eid)
    assert all(len(row) == 3 for row in rows)
    return rows


def common_cycle(
    order: int, edges: list[tuple[int, int]], first: int, second: int
) -> set[int]:
    rows = incidence(order, edges)
    target = (1 << first) | (1 << second)

    def dfs(start: int, vertex: int, used_v: int, path: list[int]) -> set[int] | None:
        for eid in rows[vertex]:
            if path and eid == path[-1]:
                continue
            u, v = edges[eid]
            other = u ^ v ^ vertex
            if other == start and len(path) >= 2:
                mask = sum(1 << item for item in path + [eid])
                if mask & target == target:
                    return set(path + [eid])
            if (used_v >> other) & 1:
                continue
            found = dfs(start, other, used_v | (1 << other), path + [eid])
            if found is not None:
                return found
        return None

    for start in range(order):
        found = dfs(start, start, 1 << start, [])
        if found is not None:
            return found
    raise AssertionError("no common circuit")


def lift_labels(
    edges: list[tuple[int, int]], colours: dict[tuple[int, int], int], cycle: set[int]
) -> list[int]:
    labels = []
    for eid, edge in enumerate(edges):
        c = colours[edge]
        if eid in cycle:
            labels.append((1 << 0) | (1 << c))
        else:
            labels.append(sum(1 << x for x in (2, 3, 4) if x != c))
    return labels


def check_flow(order: int, edges: list[tuple[int, int]], labels: list[int]) -> None:
    assert all(mask.bit_count() == 2 for mask in labels)
    for row in incidence(order, edges):
        assert labels[row[0]] ^ labels[row[1]] ^ labels[row[2]] == 0


def check_inserted(
    order: int,
    edges: list[tuple[int, int]],
    labels: list[int],
    cycle: set[int],
    roots: tuple[int, int],
) -> None:
    # Build the subdivided cycle and choose the arc by following cycle
    # adjacency from the first new vertex to the second.
    new_edges = list(edges)
    new_labels = list(labels)
    subdividers = []
    halves: list[tuple[int, int]] = []
    for root in roots:
        u, v = new_edges[root]
        w = order + len(subdividers)
        subdividers.append(w)
        new_edges[root] = (min(u, w), max(u, w))
        halves.append((root, len(new_edges)))
        new_edges.append((min(v, w), max(v, w)))
        new_labels.append(new_labels[root])
    central = len(new_edges)
    new_edges.append(tuple(subdividers))
    new_labels.append(0b00011)

    lifted_cycle = (cycle - set(roots)) | {eid for pair in halves for eid in pair}
    rows = incidence(order + 2, new_edges)
    start, finish = subdividers
    vertex = start
    previous = -1
    arc: list[int] = []
    while vertex != finish:
        choices = [eid for eid in rows[vertex] if eid in lifted_cycle and eid != previous]
        assert choices
        eid = min(choices)
        arc.append(eid)
        u, v = new_edges[eid]
        vertex = u ^ v ^ vertex
        previous = eid
        assert len(arc) <= len(lifted_cycle)
    for eid in arc:
        mask = new_labels[eid]
        b0, b1 = (mask >> 0) & 1, (mask >> 1) & 1
        assert b0 ^ b1
        new_labels[eid] = mask ^ 0b00011
    check_flow(order + 2, new_edges, new_labels)
    assert new_labels[central] == 0b00011


def main() -> None:
    graph_count = pair_count = insertion_count = 0
    for n in (3, 4, 6, 8, 10, 12):
        order, edges, colours = prism(n)
        rows = incidence(order, edges)
        for row in rows:
            assert {colours[edges[eid]] for eid in row} == {2, 3, 4}
        graph_count += 1
        for roots in combinations(range(len(edges)), 2):
            cycle = common_cycle(order, edges, *roots)
            labels = lift_labels(edges, colours, cycle)
            check_flow(order, edges, labels)
            active = {
                eid for eid, mask in enumerate(labels)
                if ((mask >> 0) & 1) ^ ((mask >> 1) & 1)
            }
            assert active == cycle
            assert set(roots) <= cycle
            check_inserted(order, edges, labels, cycle, roots)
            pair_count += 1
            insertion_count += 1
    print(
        "PASS: prescribed-circuit Tait lift; "
        f"graphs={graph_count}; edge_pairs={pair_count}; "
        f"inverse_insertions={insertion_count}"
    )


if __name__ == "__main__":
    main()
