#!/usr/bin/env python3
"""Independent replay for the sharp multipole macro-network frontier.

The script reconstructs the exact D5 boundary relations of the C5,
graph6 C], and graph6 ECxo atoms without using the pole census.  It then
compiles the C++ search and exhausts every labelled terminal pairing for
two C5 atoms with zero or one four-pole atom.
"""

from __future__ import annotations

from functools import lru_cache, reduce
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_d5_multipole_macronetwork.cpp"
COLORS = tuple(range(5))
D = tuple(sum(1 << color for color in pair) for pair in combinations(COLORS, 2))
COLOR_PERMUTATIONS = tuple(permutations(COLORS))


def parse_graph6(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    vertices = ord(record[0]) - 63
    bits = []
    for character in record[1:]:
        value = ord(character) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    cursor = 0
    for right in range(1, vertices):
        for left in range(right):
            if bits[cursor]:
                edges.append((left, right))
            cursor += 1
    return vertices, tuple(edges)


@lru_cache(maxsize=None)
def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[color]
        for color in COLORS
        if (mask >> color) & 1
    )


@lru_cache(maxsize=None)
def color_representative(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(permute_mask(label, permutation) for label in word)
        for permutation in COLOR_PERMUTATIONS
    )


@lru_cache(maxsize=None)
def orbit_representatives(arity: int) -> tuple[tuple[int, ...], ...]:
    answer = {
        color_representative(word)
        for word in product(D, repeat=arity)
        if reduce(int.__xor__, word, 0) == 0
    }
    return tuple(sorted(answer))


def incidence(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows = [[] for _ in range(vertices)]
    for edge, (left, right) in enumerate(edges):
        rows[left].append(edge)
        rows[right].append(edge)
    return tuple(tuple(row) for row in rows)


def boundary_relation(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> tuple[int, tuple[int, ...]]:
    rows = incidence(vertices, edges)
    terminals = tuple(
        vertex for vertex, row in enumerate(rows) if len(row) == 2
    )
    assert all(len(row) in (2, 3) for row in rows)
    representatives = orbit_representatives(len(terminals))
    orbit_index = {word: index for index, word in enumerate(representatives)}
    relation_mask = 0
    admitted_words = 0

    def extends(boundary: tuple[int, ...]) -> bool:
        terminal_label = dict(zip(terminals, boundary))

        def search(values: list[int | None]) -> bool:
            while True:
                changed = False
                for vertex, row in enumerate(rows):
                    known = [
                        values[edge]
                        for edge in row
                        if values[edge] is not None
                    ]
                    if vertex in terminal_label:
                        known.append(terminal_label[vertex])
                    unknown = [
                        edge for edge in row if values[edge] is None
                    ]
                    xor = reduce(int.__xor__, known, 0)
                    if not unknown:
                        if xor:
                            return False
                    elif len(unknown) == 1:
                        if xor not in D:
                            return False
                        values[unknown[0]] = xor
                        changed = True
                if not changed:
                    break
            try:
                edge = values.index(None)
            except ValueError:
                return True
            for label in D:
                branch = values.copy()
                branch[edge] = label
                if search(branch):
                    return True
            return False

        return search([None] * len(edges))

    for word in product(D, repeat=len(terminals)):
        if reduce(int.__xor__, word, 0):
            continue
        if extends(word):
            admitted_words += 1
            relation_mask |= (
                1 << orbit_index[color_representative(word)]
            )
    return relation_mask, tuple(terminals), admitted_words


def transform_relation(mask: int, permutation: tuple[int, ...]) -> int:
    representatives = orbit_representatives(len(permutation))
    index = {word: position for position, word in enumerate(representatives)}
    answer = 0
    for position, word in enumerate(representatives):
        if (mask >> position) & 1:
            transformed = tuple(word[index_] for index_ in permutation)
            answer |= 1 << index[color_representative(transformed)]
    return answer


def compile_search(directory: Path) -> Path:
    binary = directory / "macro-search"
    subprocess.run(
        [
            "c++",
            "-std=c++17",
            "-O3",
            "-I/opt/homebrew/include",
            str(SOURCE),
            "/opt/homebrew/lib/libcadical.a",
            "-lpthread",
            "-o",
            str(binary),
        ],
        check=True,
    )
    return binary


def run_row(binary: Path, four_count: int, mode: str) -> dict[str, object]:
    completed = subprocess.run(
        [
            str(binary),
            "-1",
            str(four_count),
            str(four_count),
            "2",
            "0",
            mode,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random", action="store_true")
    arguments = parser.parse_args()

    c5_edges = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))
    c5_mask, c5_terminals, c5_words = boundary_relation(5, c5_edges)
    assert c5_terminals == (0, 1, 2, 3, 4)
    assert c5_mask.bit_count() == 46 and c5_words == 4620

    a_vertices, a_edges = parse_graph6("C]")
    b_vertices, b_edges = parse_graph6("ECxo")
    a_mask, a_terminals, a_words = boundary_relation(a_vertices, a_edges)
    b_mask, b_terminals, b_words = boundary_relation(b_vertices, b_edges)
    assert a_terminals == (0, 1, 2, 3)
    assert b_terminals == (0, 1, 2, 3)
    assert a_mask == 0x3FD and a_words == 580
    assert b_mask == 0x3FE and b_words == 630
    a_variants = {
        transform_relation(a_mask, permutation)
        for permutation in permutations(range(4))
    }
    assert a_variants == {0x3EF, 0x3F7, 0x3FD}
    assert {
        transform_relation(b_mask, permutation)
        for permutation in permutations(range(4))
    } == {0x3FE}

    with tempfile.TemporaryDirectory(prefix="d5-macro-replay-") as raw:
        binary = compile_search(Path(raw))
        exact_rows = [
            run_row(binary, 0, "A"),
            run_row(binary, 1, "A"),
            run_row(binary, 1, "B"),
        ]
        assert exact_rows == [
            {
                "classification": "NO_UNSAT_IN_EXACT_LABELLED_PAIRINGS",
                "five_atoms": 2,
                "four_atoms": 0,
                "four_mode": "A",
                "pairing_leaves": 120,
                "accepted": 120,
                "non_tait": 10,
            },
            {
                "classification": "NO_UNSAT_IN_EXACT_LABELLED_PAIRINGS",
                "five_atoms": 2,
                "four_atoms": 1,
                "four_mode": "A",
                "pairing_leaves": 14400,
                "accepted": 14400,
                "non_tait": 0,
            },
            {
                "classification": "NO_UNSAT_IN_EXACT_LABELLED_PAIRINGS",
                "five_atoms": 2,
                "four_atoms": 1,
                "four_mode": "B",
                "pairing_leaves": 14400,
                "accepted": 14400,
                "non_tait": 0,
            },
        ]
        random_rows = []
        if arguments.random:
            for trials, lower, upper, five, seed, mode in (
                (50000, 0, 30, 2, 20260730, "mixed"),
                (50000, 0, 30, 4, 20260731, "mixed"),
                (50000, 1, 40, 2, 20260732, "B"),
            ):
                completed = subprocess.run(
                    [
                        str(binary),
                        str(trials),
                        str(lower),
                        str(upper),
                        str(five),
                        str(seed),
                        mode,
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                row = json.loads(completed.stdout)
                assert row["classification"] == "NO_UNSAT_IN_RANDOM_SAMPLE"
                random_rows.append(row)

    print(
        json.dumps(
            {
                "classification": (
                    "EXACT SMALL MACRO-NETWORK NO-GO / FRONTIER OPEN"
                ),
                "relations": {
                    "c5_orbits": c5_mask.bit_count(),
                    "c5_words": c5_words,
                    "proper_four_pole_masks": [
                        "0x3ef", "0x3f7", "0x3fd", "0x3fe"
                    ],
                },
                "exact_rows": exact_rows,
                "random_rows": random_rows,
                "fivecdc_unsat_found": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
