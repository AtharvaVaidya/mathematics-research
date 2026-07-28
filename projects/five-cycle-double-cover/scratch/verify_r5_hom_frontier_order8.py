#!/usr/bin/env python3
"""Independent checker for the R5 homomorphism frontier through order 8.

The checker does not call the search routine.  It regenerates nauty's
unlabeled graph stream, checks every literal positive/negative certificate,
and exhaustively verifies the two finite facts about the 16-vertex target
used to rule out the negative certificates.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess


EXPECTED_SHA256 = "11d76be8a401309849269c1889372459a7d79b52b0eb5c745d8a49ac8e79cc96"
EXPECTED_PER_ORDER = {
    1: (1, 1, 0, 0),
    2: (2, 2, 0, 0),
    3: (4, 4, 0, 0),
    4: (11, 11, 0, 0),
    5: (34, 34, 0, 0),
    6: (156, 155, 1, 0),
    7: (1044, 1037, 7, 0),
    8: (12346, 12257, 88, 1),
}


def graph6_edges(text: str) -> tuple[int, frozenset[frozenset[int]]]:
    """Decode the small-graph graph6 format independently of the producer."""
    if not text or text[0] == "~":
        raise ValueError("only graph6 records of order at most 62 are supported")
    order = ord(text[0]) - 63
    payload = []
    for character in text[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("bad graph6 character")
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(payload) < required or any(payload[required:]):
        raise ValueError("bad graph6 payload length or padding")
    result: set[frozenset[int]] = set()
    cursor = 0
    for upper in range(1, order):
        for lower in range(upper):
            if payload[cursor]:
                result.add(frozenset((lower, upper)))
            cursor += 1
    return order, frozenset(result)


def adjacent(edges: frozenset[frozenset[int]], left: int, right: int) -> bool:
    return frozenset((left, right)) in edges


def check_map(
    order: int,
    edges: frozenset[frozenset[int]],
    image: object,
) -> None:
    assert isinstance(image, list) and len(image) == order
    assert all(
        isinstance(word, int) and 0 <= word < 32 and word.bit_count() % 2 == 0
        for word in image
    )
    for edge in edges:
        left, right = tuple(edge)
        assert (image[left] ^ image[right]).bit_count() == 2


def check_k6(
    order: int,
    edges: frozenset[frozenset[int]],
    vertices: object,
) -> None:
    assert isinstance(vertices, list)
    assert len(vertices) == len(set(vertices)) == 6
    assert all(isinstance(vertex, int) and 0 <= vertex < order for vertex in vertices)
    assert all(adjacent(edges, left, right) for left, right in combinations(vertices, 2))


def check_k3_join_c5(
    order: int,
    edges: frozenset[frozenset[int]],
    triangle: object,
    cycle: object,
) -> None:
    assert order == 8
    assert isinstance(triangle, list) and isinstance(cycle, list)
    assert len(triangle) == len(set(triangle)) == 3
    assert len(cycle) == len(set(cycle)) == 5
    assert set(triangle).isdisjoint(cycle)
    assert set(triangle) | set(cycle) == set(range(8))

    claimed: set[frozenset[int]] = set()
    claimed.update(frozenset(pair) for pair in combinations(triangle, 2))
    claimed.update(
        frozenset((cycle[index], cycle[(index + 1) % 5]))
        for index in range(5)
    )
    claimed.update(
        frozenset((left, right)) for left in triangle for right in cycle
    )
    assert edges == frozenset(claimed)


def target_lemmas() -> dict[str, object]:
    """Brute-force the target facts behind both obstruction certificates."""
    target = tuple(word for word in range(32) if word.bit_count() % 2 == 0)
    edges = frozenset(
        frozenset((left, right))
        for left, right in combinations(range(16), 2)
        if (target[left] ^ target[right]).bit_count() == 2
    )

    maximum_clique = 0
    maximum_witness: tuple[int, ...] = ()
    for mask in range(1 << 16):
        size = mask.bit_count()
        if size <= maximum_clique:
            continue
        vertices = tuple(index for index in range(16) if (mask >> index) & 1)
        if all(adjacent(edges, left, right) for left, right in combinations(vertices, 2)):
            maximum_clique = size
            maximum_witness = vertices
    assert maximum_clique == 5

    triangles = tuple(
        triple
        for triple in combinations(range(16), 3)
        if all(adjacent(edges, left, right) for left, right in combinations(triple, 2))
    )
    assert len(triangles) == 160
    common_neighborhood_types = Counter()
    for triangle in triangles:
        common = tuple(
            vertex
            for vertex in range(16)
            if all(adjacent(edges, vertex, member) for member in triangle)
        )
        internal_edges = sum(
            adjacent(edges, left, right) for left, right in combinations(common, 2)
        )
        common_neighborhood_types[(len(common), internal_edges)] += 1
    # Every triangle has common neighborhood K2 disjoint-union K1.  An odd
    # cycle cannot map to this graph, proving K3 join C5 has no target map.
    assert common_neighborhood_types == Counter({(3, 1): 160})

    return {
        "target_vertices": len(target),
        "target_edges": len(edges),
        "maximum_clique": maximum_clique,
        "maximum_clique_words": [target[index] for index in maximum_witness],
        "triangles": len(triangles),
        "triangle_common_neighborhood_types": {
            f"{vertices}_vertices_{internal}_edges": count
            for (vertices, internal), count in common_neighborhood_types.items()
        },
    }


def find_geng(explicit: str | None) -> str:
    if explicit:
        return explicit
    candidates = ("/opt/homebrew/bin/geng", shutil.which("geng"))
    for candidate in candidates:
        if candidate is not None and Path(candidate).is_file():
            return str(candidate)
    raise FileNotFoundError("nauty geng not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "frontier",
        nargs="?",
        type=Path,
        default=Path("output/r5-hom-frontier-order8/frontier.jsonl"),
    )
    parser.add_argument("--geng")
    arguments = parser.parse_args()

    raw = arguments.frontier.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256, (digest, EXPECTED_SHA256)
    lines = raw.decode("utf-8").splitlines()
    assert len(lines) == 13_599
    rows = [json.loads(line) for line in lines]
    summary = rows.pop()
    assert summary["type"] == "SUMMARY"

    executable = find_geng(arguments.geng)
    cursor = 0
    observed: dict[int, Counter[str]] = {}
    for order in range(1, 9):
        generated = subprocess.run(
            (executable, "-q", str(order)),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        counts: Counter[str] = Counter()
        for graph6 in generated:
            row = rows[cursor]
            cursor += 1
            assert row["type"] == "GRAPH"
            assert row["order"] == order
            assert row["graph6"] == graph6
            decoded_order, edges = graph6_edges(graph6)
            assert decoded_order == order
            assert row["edges"] == len(edges)
            result = row["result"]
            counts[result] += 1
            if result == "MAP":
                check_map(order, edges, row["image"])
            elif result == "K6_OBSTRUCTION":
                check_k6(order, edges, row["vertices"])
            elif result == "K3_JOIN_C5_OBSTRUCTION":
                check_k3_join_c5(order, edges, row["triangle"], row["cycle"])
            else:
                raise AssertionError(f"unknown result {result!r}")
        observed[order] = counts
    assert cursor == len(rows) == 13_598

    for order, expected in EXPECTED_PER_ORDER.items():
        graphs, maps, k6, exceptional = expected
        assert sum(observed[order].values()) == graphs
        assert observed[order]["MAP"] == maps
        assert observed[order]["K6_OBSTRUCTION"] == k6
        assert observed[order]["K3_JOIN_C5_OBSTRUCTION"] == exceptional

    assert summary["graphs"] == 13_598
    assert summary["maps"] == 13_501
    assert summary["k6_obstructions"] == 96
    assert summary["k3_join_c5_obstructions"] == 1
    lemmas = target_lemmas()
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "frontier": str(arguments.frontier),
                "sha256": digest,
                "orders": EXPECTED_PER_ORDER,
                **lemmas,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
