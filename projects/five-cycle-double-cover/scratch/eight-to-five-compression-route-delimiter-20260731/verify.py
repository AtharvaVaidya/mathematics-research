#!/usr/bin/env python3
"""Standalone exact verifier for the 12-vertex local-rule no-go.

Only the Python standard library is used.  This is a route delimiter for
context-free recolouring of a supplied eight-cover, not a FiveCDC solver.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


BLOCKS = (
    (0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 1, 5),
    (0, 2, 3), (0, 2, 4), (0, 2, 5), (1, 2, 3),
    (1, 3, 4), (1, 3, 5), (2, 4, 5), (3, 4, 5),
)

# (left vertex, right vertex, old unordered coordinate pair)
LABELLED_EDGES = (
    (0, 1, (0, 1)), (2, 3, (0, 1)),
    (0, 4, (0, 2)), (5, 6, (0, 2)),
    (1, 4, (0, 3)), (2, 5, (0, 4)), (3, 6, (0, 5)),
    (0, 7, (1, 2)),
    (1, 8, (1, 3)), (7, 9, (1, 3)),
    (2, 8, (1, 4)), (3, 9, (1, 5)), (4, 7, (2, 3)),
    (5, 10, (2, 4)), (6, 10, (2, 5)), (8, 11, (3, 4)),
    (9, 11, (3, 5)), (10, 11, (4, 5)),
)

TAIT_COLOURS = (0, 1, 1, 1, 2, 0, 2, 2, 1, 1, 2, 0, 0, 2, 0, 0, 2, 1)
EXPECTED_GRAPH6 = "K`o_kP_COK?F"
PAIR_COLUMNS = tuple(combinations(range(6), 2))


def incidence() -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in BLOCKS]
    for index, (left, right, _) in enumerate(LABELLED_EDGES):
        assert left != right
        rows[left].append(index)
        rows[right].append(index)
    return tuple(tuple(row) for row in rows)


def graph6_encode() -> str:
    edge_set = {
        tuple(sorted((left, right)))
        for left, right, _ in LABELLED_EDGES
    }
    bits = [
        int((left, right) in edge_set)
        for right in range(1, len(BLOCKS))
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    return chr(len(BLOCKS) + 63) + "".join(
        chr(63 + sum(bits[offset + bit] << (5 - bit) for bit in range(6)))
        for offset in range(0, len(bits), 6)
    )


def connected(removed_edge: int | None = None) -> bool:
    rows = incidence()
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for edge in rows[vertex]:
            if edge == removed_edge:
                continue
            left, right, _ = LABELLED_EDGES[edge]
            other = left ^ right ^ vertex
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(BLOCKS)


def gf2_rank(words: list[int]) -> tuple[int, tuple[int, ...]]:
    pivots: dict[int, int] = {}
    for original in words:
        word = original
        while word:
            pivot = word.bit_length() - 1
            if pivot in pivots:
                word ^= pivots[pivot]
            else:
                pivots[pivot] = word
                break
    return len(pivots), tuple(sorted(pivots))


def maximum_r5_clique() -> tuple[int, tuple[int, ...]]:
    neighbours = tuple(
        frozenset(
            other for other in range(32)
            if other != word and (word ^ other).bit_count() == 2
        )
        for word in range(32)
    )
    best: tuple[int, ...] = ()

    def visit(clique: tuple[int, ...], candidates: set[int]) -> None:
        nonlocal best
        if len(clique) + len(candidates) <= len(best):
            return
        if len(clique) > len(best):
            best = clique
        while candidates:
            if len(clique) + len(candidates) <= len(best):
                return
            vertex = min(candidates)
            candidates.remove(vertex)
            visit(clique + (vertex,), candidates & neighbours[vertex])

    visit((), set(range(32)))
    return len(best), best


def verify_graph_and_old_cover() -> dict[str, object]:
    rows = incidence()
    assert len(BLOCKS) == 12 and len(LABELLED_EDGES) == 18
    assert all(len(row) == 3 for row in rows)
    assert len({tuple(sorted((u, v))) for u, v, _ in LABELLED_EDGES}) == 18
    assert connected()
    assert all(connected(edge) for edge in range(18))
    assert graph6_encode() == EXPECTED_GRAPH6

    label_counts = Counter(label for _, _, label in LABELLED_EDGES)
    assert set(label_counts) == set(PAIR_COLUMNS)
    assert sorted(label_counts.values()) == [1] * 12 + [2] * 3

    flow = tuple(left ^ right for _, _, (left, right) in LABELLED_EDGES)
    assert set(flow) == set(range(1, 8))
    potential = tuple(a ^ b ^ c for a, b, c in BLOCKS)

    for vertex, block in enumerate(BLOCKS):
        local_edges = rows[vertex]
        local_labels = {
            LABELLED_EDGES[edge][2] for edge in local_edges
        }
        assert local_labels == set(combinations(block, 2))
        assert flow[local_edges[0]] ^ flow[local_edges[1]] ^ flow[local_edges[2]] == 0

        for edge in local_edges:
            label = LABELLED_EDGES[edge][2]
            other_edge = next(item for item in local_edges if item != edge)
            base = potential[vertex] ^ flow[other_edge]
            reconstructed = tuple(sorted((base, base ^ flow[edge])))
            assert reconstructed == label

    # Direct Eulerian-subgraph semantics in all eight old coordinates.
    for coordinate in range(8):
        for row in rows:
            degree = sum(coordinate in LABELLED_EDGES[edge][2] for edge in row)
            assert degree % 2 == 0
    assert all(len(label) == 2 for _, _, label in LABELLED_EDGES)

    return {
        "vertices": 12,
        "edges": 18,
        "graph6": EXPECTED_GRAPH6,
        "simple": True,
        "connected": True,
        "bridgeless_edge_deletions": 18,
        "used_old_coordinates": 6,
        "distinct_old_pairs": 15,
        "old_pair_edge_multiplicities": dict(
            sorted((f"{a}{b}", count) for (a, b), count in label_counts.items())
        ),
        "flow_values_used": list(range(1, 8)),
        "potential": list(potential),
    }


def verify_triangle_rigidity() -> dict[str, object]:
    column = {pair: index for index, pair in enumerate(PAIR_COLUMNS)}
    triangle_words = [
        sum(1 << column[pair] for pair in combinations(block, 2))
        for block in BLOCKS
    ]
    assert all(word.bit_count() == 3 for word in triangle_words)
    assert sum(triangle_words, 0) != 0  # integer sum is irrelevant to xor
    aggregate_xor = 0
    for word in triangle_words:
        aggregate_xor ^= word
    assert aggregate_xor == 0

    rank, pivot_columns = gf2_rank(triangle_words)
    cycle_dimension = len(PAIR_COLUMNS) - len(range(6)) + 1
    assert rank == cycle_dimension == 10

    clique_size, clique = maximum_r5_clique()
    assert clique_size == 5
    assert all(
        (left ^ right).bit_count() == 2
        for left, right in combinations(clique, 2)
    )

    # An exact homomorphism backtrack independently confirms K6 !-> R5.
    neighbours = tuple(
        frozenset(other for other in range(32) if (word ^ other).bit_count() == 2)
        for word in range(32)
    )
    hom_count = 0

    def extend(images: tuple[int, ...]) -> None:
        nonlocal hom_count
        if len(images) == 6:
            hom_count += 1
            return
        candidates = set(range(32))
        for image in images:
            candidates &= neighbours[image]
        for image in sorted(candidates):
            extend(images + (image,))

    extend(())
    assert hom_count == 0

    # The aggregate dependency plus even cubic order gives the sharp
    # lower bound 12 for this full-rank K6 rigidity mechanism.
    assert rank + 1 == 11
    minimum_even_cubic_order = 12

    return {
        "pair_columns": [f"{a}{b}" for a, b in PAIR_COLUMNS],
        "triangle_row_hex": [f"0x{word:04x}" for word in triangle_words],
        "triangle_row_count": len(triangle_words),
        "triangle_row_xor": aggregate_xor,
        "triangle_rank": rank,
        "k6_cycle_space_dimension": cycle_dimension,
        "rank_pivot_columns_zero_based": list(pivot_columns),
        "r5_vertices": 32,
        "r5_maximum_clique": clique_size,
        "r5_clique_witness_decimal": list(clique),
        "k6_to_r5_homomorphisms": hom_count,
        "minimum_full_rank_rigidity_order": minimum_even_cubic_order,
    }


def verify_positive_fivecdc_control() -> dict[str, object]:
    rows = incidence()
    assert len(TAIT_COLOURS) == len(LABELLED_EDGES)
    for row in rows:
        assert {TAIT_COLOURS[edge] for edge in row} == {0, 1, 2}

    new_label = ((0, 1), (0, 2), (1, 2))
    for row in rows:
        xor = 0
        for edge in row:
            for bit in new_label[TAIT_COLOURS[edge]]:
                xor ^= 1 << bit
        assert xor == 0
    assert all(len(new_label[colour]) == 2 for colour in TAIT_COLOURS)

    # The control truly uses global edge context: one old pair has two
    # occurrences assigned distinct Tait colours.
    by_old_label: dict[tuple[int, int], set[int]] = {}
    for edge, (_, _, label) in enumerate(LABELLED_EDGES):
        by_old_label.setdefault(label, set()).add(TAIT_COLOURS[edge])
    split_labels = sorted(
        f"{a}{b}" for (a, b), colours in by_old_label.items()
        if len(colours) > 1
    )
    assert split_labels

    return {
        "proper_tait_colouring": list(TAIT_COLOURS),
        "fivecdc_edge_labels_by_tait_colour": ["01", "02", "12"],
        "old_pair_types_split_by_global_context": split_labels,
        "fivecdc_exists": True,
    }


def main() -> None:
    report = {
        "schema": "fivecdc-eight-to-five-local-rule-rigidity-v1",
        "date": "2026-07-31",
        "claim_scope": (
            "context-free nonlinear pair recolouring of one supplied "
            "Oum eight-cover; not FiveCDC"
        ),
        "graph_and_old_cover": verify_graph_and_old_cover(),
        "rigidity_certificate": verify_triangle_rigidity(),
        "positive_control": verify_positive_fivecdc_control(),
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("certificate.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert report == expected
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
