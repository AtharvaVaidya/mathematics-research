#!/usr/bin/env python3
"""Independent Python replay of one distance-three order-20 target orbit.

The graph, edge-label tuple, and roots use the lexicographic edge order of
``tools.fixed_fano_merge_frontier.graph_from_graph6``.  The implementation is
independent of the C++ target-orbit driver, while reusing the previously
audited Python Kempe primitives.
"""

from __future__ import annotations

import sys
from collections import Counter, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "scratch"
for item in (str(PROJECT_ROOT), str(SCRATCH)):
    if item not in sys.path:
        sys.path.insert(0, item)

from audit_d5_root_component_chain_potential import (  # noqa: E402
    all_root_distances,
    component_masks,
)
from audit_d5_root_kempe_orbits import canonical, neighbours  # noqa: E402
from tools.fixed_fano_merge_frontier import graph_from_graph6  # noqa: E402


GRAPH6 = "S?AI???OWCKC?IGQ@_S_?CO?A?HO?c_?G"
LABEL_NAMES = (
    "12", "02", "01", "12", "02", "01", "12", "02", "01", "01",
    "12", "02", "01", "12", "02", "02", "01", "02", "12", "01",
    "02", "01", "02", "12", "02", "12", "01", "12", "01", "12",
)
ROOTS = (1, 22)


def mask(name: str) -> int:
    return sum(1 << int(coordinate) for coordinate in name)


def main() -> None:
    graph = graph_from_graph6(GRAPH6)
    initial = canonical(tuple(mask(name) for name in LABEL_NAMES))
    assert len(initial) == graph.edge_count

    incidence = [[] for _ in range(graph.vertices)]
    for edge, (left, right) in enumerate(graph.edges):
        incidence[left].append(edge)
        incidence[right].append(edge)
    for row in incidence:
        assert len(row) == 3
        assert initial[row[0]] ^ initial[row[1]] ^ initial[row[2]] == 0

    states = [initial]
    index = {initial: 0}
    adjacency: list[list[int]] = []
    for state in states:
        row = []
        for other in sorted(set(neighbours(graph, state)) - {state}):
            if other not in index:
                index[other] = len(states)
                states.append(other)
            row.append(index[other])
        adjacency.append(row)

    first_root, second_root = ROOTS
    levels = [
        all_root_distances(
            graph.edge_count,
            component_masks(graph, state),
        )[first_root][second_root]
        for state in states
    ]

    seen: set[int] = set()
    plateaus = 0
    failures = []
    for start, level in enumerate(levels):
        if level <= 1 or start in seen:
            continue
        plateaus += 1
        plateau = {start}
        queue = deque([start])
        descent = False
        while queue:
            current = queue.popleft()
            for other in adjacency[current]:
                if levels[other] < level:
                    descent = True
                elif levels[other] == level and other not in plateau:
                    plateau.add(other)
                    queue.append(other)
        seen.update(plateau)
        if not descent:
            failures.append((level, len(plateau), state))

    assert len(states) == 18_893
    assert Counter(levels) == Counter({1: 11_811, 2: 7_058, 3: 24})
    assert plateaus == 54
    assert not failures
    print(
        "PASS: order-20 target orbit has 18,893 normalized states, "
        "level counts {1: 11811, 2: 7058, 3: 24}, 54 plateaus, "
        "and zero nonincreasing-distance failures"
    )


if __name__ == "__main__":
    main()
