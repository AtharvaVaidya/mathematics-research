#!/usr/bin/env python3
"""Audit neutral-component connectivity at local chi maxima in 2-lifts.

The base graph is the 14-vertex state used by the local-boundary audits.
We exhaust the 255 nontrivial gauge-normalized Z/2 voltage assignments.
Only nonempty factor components are counted as moves.
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

from audit_d5_local_neutral_two_lifts import cotree_edges  # noqa: E402
from audit_d5_root_euler_potential import euler_characteristic  # noqa: E402
from audit_d5_root_kempe_orbits import (  # noqa: E402
    PAIRS,
    active_mask,
    component_edge_masks,
    transpose_label,
)
from check_d5_local_boundary_degree_two_lift_no_go import (  # noqa: E402
    construct_lift,
    validate_flow,
)


def gf2_rank(rows: list[int]) -> int:
    """Return the rank of bit-vector rows over GF(2)."""
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def hypergraph_components(edge_count: int, hyperedges: list[int]) -> list[int]:
    """Return bit masks of connected components of a support hypergraph."""
    through: list[list[int]] = [[] for _ in range(edge_count)]
    for hyperedge in hyperedges:
        mask = hyperedge
        while mask:
            bit = mask & -mask
            edge = bit.bit_length() - 1
            through[edge].append(hyperedge)
            mask ^= bit

    unseen = (1 << edge_count) - 1
    answer: list[int] = []
    while unseen:
        seed = unseen & -unseen
        reached = seed
        queue = deque([seed.bit_length() - 1])
        unseen ^= seed
        while queue:
            edge = queue.popleft()
            for hyperedge in through[edge]:
                new = hyperedge & unseen
                reached |= new
                unseen ^= new
                while new:
                    bit = new & -new
                    queue.append(bit.bit_length() - 1)
                    new ^= bit
        answer.append(reached)
    return answer


def audit_state(graph, state):
    old_chi = euler_characteristic(graph, state)
    deltas: list[int] = []
    neutral: list[int] = []
    for pair in PAIRS:
        for component in component_edge_masks(
            graph, active_mask(state, *pair)
        ):
            if not component:
                continue
            other = tuple(
                transpose_label(label, *pair)
                if (component >> edge) & 1
                else label
                for edge, label in enumerate(state)
            )
            delta = euler_characteristic(graph, other) - old_chi
            deltas.append(delta)
            if delta == 0:
                neutral.append(component)
    return (
        Counter(deltas),
        neutral,
        hypergraph_components(graph.edge_count, neutral),
    )


def main() -> int:
    cotree = cotree_edges()
    local_maxima = 0
    disconnected = []
    local_max_delta_histograms = Counter()
    local_max_neutral_rank_histogram = Counter()
    local_max_hypergraph_block_histogram = Counter()

    for word in range(1, 1 << len(cotree)):
        voltages = {
            cotree[index]
            for index in range(len(cotree))
            if (word >> index) & 1
        }
        graph6, graph, state, _ = construct_lift(voltages)
        validate_flow(graph, state)
        delta_histogram, neutral, blocks = audit_state(graph, state)
        if max(delta_histogram) > 0:
            continue
        local_maxima += 1
        local_max_delta_histograms[tuple(sorted(delta_histogram.items()))] += 1
        local_max_neutral_rank_histogram[gf2_rank(neutral)] += 1
        local_max_hypergraph_block_histogram[len(blocks)] += 1
        if len(blocks) != 1:
            disconnected.append({
                "voltage_word": word,
                "voltage_one_edges": sorted(voltages),
                "graph6": graph6,
                "delta_histogram": dict(delta_histogram),
                "neutral_rank": gf2_rank(neutral),
                "block_sizes": sorted(mask.bit_count() for mask in blocks),
                "state_labels_hex": [
                    f"{label:02x}" for label in state
                ],
            })

    assert local_maxima > 0
    print("PASS" if not disconnected else "FAIL")
    print(f"cotree edges: {cotree}")
    print(f"connected gauge-normalized 2-lifts: {(1 << len(cotree)) - 1}")
    print(f"local chi maxima: {local_maxima}")
    print(
        "local-maximum delta histograms: "
        f"{dict(sorted(local_max_delta_histograms.items()))}"
    )
    print(
        "local-maximum neutral ranks: "
        f"{dict(sorted(local_max_neutral_rank_histogram.items()))}"
    )
    print(
        "local-maximum neutral hypergraph block counts: "
        f"{dict(sorted(local_max_hypergraph_block_histogram.items()))}"
    )
    print(f"disconnected local-maximum witnesses: {len(disconnected)}")
    if disconnected:
        print(f"first witness: {disconnected[0]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
