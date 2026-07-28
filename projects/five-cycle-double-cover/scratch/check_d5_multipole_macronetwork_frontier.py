#!/usr/bin/env python3
"""Independent replay for the sharp multipole macro-network frontier.

The script reconstructs the exact D5 boundary relations of the C5,
graph6 C], and graph6 ECxo atoms without using the pole census.  It then
compiles the C++ search and exhausts every labelled terminal pairing for
two C5 atoms with zero or one four-pole atom.  With ``--frontier2`` it
also generates all loopless pairings with exactly two four-poles, removes
expanded-graph isomorphs with nauty ``shortg``, independently checks the
canonical streams, and semantically checks both Tait and FiveCDC models.
"""

from __future__ import annotations

from functools import lru_cache, reduce
from itertools import combinations, permutations, product
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_d5_multipole_macronetwork.cpp"
FRONTIER2_GENERATOR = HERE / "generate_d5_frontier2_graphs.cpp"
FRONTIER2_CHECKER = HERE / "check_d5_frontier2_graphs.cpp"
FRONTIER2_WITNESSES = (
    HERE / "d5-multipole-macronetwork-frontier2-nontait-witnesses.json"
)
FRONTIER3_SOURCE = HERE / "search_d5_frontier3_boundary.cpp"
FRONTIER4_SOURCE = HERE / "search_d5_frontier4_boundary.cpp"
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


def compile_frontier2(directory: Path) -> tuple[Path, Path]:
    generator = directory / "frontier2-generator"
    checker = directory / "frontier2-checker"
    subprocess.run(
        [
            "c++", "-std=c++17", "-O3",
            str(FRONTIER2_GENERATOR), "-o", str(generator),
        ],
        check=True,
    )
    subprocess.run(
        [
            "c++", "-std=c++17", "-O3",
            "-I/opt/homebrew/include",
            str(FRONTIER2_CHECKER),
            "/opt/homebrew/lib/libcadical.a",
            "-lpthread", "-o", str(checker),
        ],
        check=True,
    )
    return generator, checker


def compile_frontier3(directory: Path) -> Path:
    binary = directory / "frontier3-boundary"
    subprocess.run(
        [
            "c++", "-std=c++17", "-O3",
            str(FRONTIER3_SOURCE), "-o", str(binary),
        ],
        check=True,
    )
    return binary


def compile_frontier4(directory: Path) -> Path:
    binary = directory / "frontier4-boundary"
    subprocess.run(
        [
            "c++", "-std=c++17", "-O3",
            str(FRONTIER4_SOURCE), "-o", str(binary),
        ],
        check=True,
    )
    return binary


@lru_cache(maxsize=None)
def loopless_pairing_count(counts: tuple[int, ...]) -> int:
    """Count labelled cross-atom terminal matchings independently."""
    if not any(counts):
        return 1
    first = next(index for index, count in enumerate(counts) if count)
    remaining = list(counts)
    remaining[first] -= 1
    answer = 0
    for other, choices in enumerate(remaining):
        if other == first or not choices:
            continue
        remaining[other] -= 1
        answer += choices * loopless_pairing_count(tuple(remaining))
        remaining[other] += 1
    return answer


def macro_frontier2_count() -> tuple[int, int]:
    """Enumerate bridgeless multiplicity matrices and labelled lifts."""
    degrees = (5, 5, 4, 4)
    rows = []
    for m01 in range(6):
        for m02 in range(6):
            m03 = 5 - m01 - m02
            if m03 < 0:
                continue
            for m12 in range(6):
                m13 = 5 - m01 - m12
                m23 = 4 - m02 - m12
                if m13 < 0 or m23 < 0 or m03 + m13 + m23 != 4:
                    continue
                multiplicities = (
                    m01, m02, m03, m12, m13, m23
                )
                pairs = (
                    (0, 1), (0, 2), (0, 3),
                    (1, 2), (1, 3), (2, 3),
                )

                def connected(skipped: int = -1) -> bool:
                    adjacency = [set() for _ in range(4)]
                    for edge, ((left, right), copies) in enumerate(
                        zip(pairs, multiplicities)
                    ):
                        copies -= edge == skipped
                        if copies > 0:
                            adjacency[left].add(right)
                            adjacency[right].add(left)
                    seen = {0}
                    stack = [0]
                    while stack:
                        current = stack.pop()
                        for other in adjacency[current] - seen:
                            seen.add(other)
                            stack.append(other)
                    return len(seen) == 4

                if not connected():
                    continue
                if any(
                    not connected(edge)
                    for edge, copies in enumerate(multiplicities)
                    if copies
                ):
                    continue
                labelled = (
                    math.prod(math.factorial(degree) for degree in degrees)
                    // math.prod(
                        math.factorial(copies)
                        for copies in multiplicities
                    )
                )
                rows.append((multiplicities, labelled))
    return len(rows), sum(labelled for _, labelled in rows)


def frontier3_macro_counts() -> tuple[int, dict[str, int]]:
    """Independent degree-(5,5,4,4,4) macro census and quotient."""
    degrees = (5, 5, 4, 4, 4)
    pairs = tuple(combinations(range(5), 2))
    matrices = []

    def enumerate_matrices(
        edge_type: int, partial_degrees: list[int], values: list[int]
    ) -> None:
        if edge_type == len(pairs):
            if tuple(partial_degrees) != degrees:
                return

            def connected(skipped: int = -1) -> bool:
                adjacency = [set() for _ in range(5)]
                for edge, ((left, right), copies) in enumerate(
                    zip(pairs, values)
                ):
                    copies -= edge == skipped
                    if copies > 0:
                        adjacency[left].add(right)
                        adjacency[right].add(left)
                seen = {0}
                stack = [0]
                while stack:
                    current = stack.pop()
                    for other in adjacency[current] - seen:
                        seen.add(other)
                        stack.append(other)
                return len(seen) == 5

            if connected() and all(
                connected(edge)
                for edge, copies in enumerate(values)
                if copies
            ):
                matrices.append(tuple(values))
            return
        left, right = pairs[edge_type]
        maximum = min(
            degrees[left] - partial_degrees[left],
            degrees[right] - partial_degrees[right],
        )
        for copies in range(maximum + 1):
            partial_degrees[left] += copies
            partial_degrees[right] += copies
            values.append(copies)
            enumerate_matrices(edge_type + 1, partial_degrees, values)
            values.pop()
            partial_degrees[left] -= copies
            partial_degrees[right] -= copies

    enumerate_matrices(0, [0] * 5, [])

    def canonical(
        matrix_word: tuple[int, ...], types: tuple[str, ...]
    ) -> tuple[int, ...]:
        matrix = [[0] * 5 for _ in range(5)]
        for (left, right), copies in zip(pairs, matrix_word):
            matrix[left][right] = matrix[right][left] = copies
        words = []
        for order in permutations(range(5)):
            if all(types[order[position]] == types[position]
                   for position in range(5)):
                words.append(
                    tuple(matrix[order[left]][order[right]]
                          for left, right in pairs)
                )
        return min(words)

    counts = {}
    for mode in ("AAA", "AAB", "ABB", "BBB"):
        types = ("F", "F", *mode)
        counts[mode] = len({
            canonical(matrix, types) for matrix in matrices
        })
    return len(matrices), counts


def frontier4_macro_counts() -> tuple[int, dict[str, int]]:
    """Independent degree-(5,5,4,4,4,4) macro census and quotient."""
    degrees = (5, 5, 4, 4, 4, 4)
    pairs = tuple(combinations(range(6), 2))
    matrices = []

    def enumerate_matrices(
        edge_type: int, partial_degrees: list[int], values: list[int]
    ) -> None:
        if edge_type == len(pairs):
            if tuple(partial_degrees) != degrees:
                return

            def connected(skipped: int = -1) -> bool:
                adjacency = [set() for _ in range(6)]
                for edge, ((left, right), copies) in enumerate(
                    zip(pairs, values)
                ):
                    copies -= edge == skipped
                    if copies > 0:
                        adjacency[left].add(right)
                        adjacency[right].add(left)
                seen = {0}
                stack = [0]
                while stack:
                    current = stack.pop()
                    for other in adjacency[current] - seen:
                        seen.add(other)
                        stack.append(other)
                return len(seen) == 6

            if connected() and all(
                connected(edge)
                for edge, copies in enumerate(values)
                if copies
            ):
                matrices.append(tuple(values))
            return
        left, right = pairs[edge_type]
        maximum = min(
            degrees[left] - partial_degrees[left],
            degrees[right] - partial_degrees[right],
        )
        for copies in range(maximum + 1):
            partial_degrees[left] += copies
            partial_degrees[right] += copies
            values.append(copies)
            enumerate_matrices(edge_type + 1, partial_degrees, values)
            values.pop()
            partial_degrees[left] -= copies
            partial_degrees[right] -= copies

    enumerate_matrices(0, [0] * 6, [])

    def canonical(
        matrix_word: tuple[int, ...], types: tuple[str, ...]
    ) -> tuple[int, ...]:
        matrix = [[0] * 6 for _ in range(6)]
        for (left, right), copies in zip(pairs, matrix_word):
            matrix[left][right] = matrix[right][left] = copies
        groups = [
            tuple(index for index, value in enumerate(types) if value == kind)
            for kind in sorted(set(types))
        ]
        words = []

        def enumerate_orders(
            group: int, order: list[int]
        ) -> None:
            if group == len(groups):
                words.append(
                    tuple(matrix[order[left]][order[right]]
                          for left, right in pairs)
                )
                return
            positions = groups[group]
            for old_positions in permutations(positions):
                branch = order.copy()
                for new, old in zip(positions, old_positions):
                    branch[new] = old
                enumerate_orders(group + 1, branch)

        enumerate_orders(0, list(range(6)))
        return min(words)

    counts = {}
    for mode in ("AAAA", "AAAB", "AABB", "ABBB", "BBBB"):
        types = ("F", "F", *mode)
        counts[mode] = len({
            canonical(matrix, types) for matrix in matrices
        })
    return len(matrices), counts


def run_frontier3(directory: Path) -> dict[str, object]:
    binary = compile_frontier3(directory)
    completed = subprocess.run(
        [str(binary), "all"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert not completed.stderr
    row = json.loads(completed.stdout)
    expected = {
        "classification": "NO_EMPTY_D5_IN_CANONICAL_FRONTIER3",
        "relations": {
            "F_rows": 4620,
            "A_rows": 580,
            "B_rows": 630,
            "F_stabilizer": 10,
            "A_stabilizer": 8,
            "B_stabilizer": 24,
        },
        "labelled_macros": 178,
        "rows": [
            {
                "mode": "AAA", "canonical_macros": 25,
                "boundary_states": 97200, "empty_d5": 0,
            },
            {
                "mode": "AAB", "canonical_macros": 56,
                "boundary_states": 72576, "empty_d5": 0,
            },
            {
                "mode": "ABB", "canonical_macros": 56,
                "boundary_states": 24192, "empty_d5": 0,
            },
            {
                "mode": "BBB", "canonical_macros": 25,
                "boundary_states": 3600, "empty_d5": 0,
            },
        ],
        "boundary_states": 197568,
        "empty_d5": 0,
    }
    assert row == expected
    return row


def run_frontier4(directory: Path) -> dict[str, object]:
    binary = compile_frontier4(directory)
    expected_rows = {
        "AAAA": (143, 1667952),
        "AAAB": (410, 1594080),
        "AABB": (643, 833328),
        "ABBB": (410, 177120),
        "BBBB": (143, 20592),
    }
    processes = {
        mode: subprocess.Popen(
            [str(binary), mode],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for mode in expected_rows
    }
    rows = []
    for mode, process in processes.items():
        stdout, stderr = process.communicate()
        assert process.returncode == 0 and not stderr
        result = json.loads(stdout)
        canonical_macros, states = expected_rows[mode]
        assert result == {
            "classification": "NO_EMPTY_D5_IN_CANONICAL_FRONTIER4",
            "labelled_macros": 4222,
            "rows": [{
                "mode": mode,
                "canonical_macros": canonical_macros,
                "boundary_states": states,
                "empty_d5": 0,
            }],
            "boundary_states": states,
            "empty_d5": 0,
        }
        rows.append(result["rows"][0])
    return {
        "classification": "NO_EMPTY_D5_IN_CANONICAL_FRONTIER4",
        "labelled_macros": 4222,
        "rows": rows,
        "boundary_states": sum(row["boundary_states"] for row in rows),
        "empty_d5": 0,
    }


def independently_validate_graph(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> None:
    assert vertices > 0
    assert len(edges) == len(set(edges))
    assert all(0 <= left < right < vertices for left, right in edges)
    rows = incidence(vertices, edges)
    assert all(len(row) == 3 for row in rows)

    def connected(skipped: int = -1) -> bool:
        adjacency = [set() for _ in range(vertices)]
        for edge, (left, right) in enumerate(edges):
            if edge == skipped:
                continue
            adjacency[left].add(right)
            adjacency[right].add(left)
        seen = {0}
        stack = [0]
        while stack:
            current = stack.pop()
            for other in adjacency[current] - seen:
                seen.add(other)
                stack.append(other)
        return len(seen) == vertices

    assert connected()
    assert all(connected(edge) for edge in range(len(edges)))


def independently_tait_colorable(
    vertices: int, edges: tuple[tuple[int, int], ...]
) -> bool:
    """Exact three-edge-colouring backtracker, independent of CaDiCaL."""
    used = [0] * vertices
    colors = [0] * len(edges)

    def search() -> bool:
        best_edge = -1
        best_available = 0
        best_size = 4
        for edge, (left, right) in enumerate(edges):
            if colors[edge]:
                continue
            available = 0b111 & ~(used[left] | used[right])
            size = available.bit_count()
            if not size:
                return False
            if size < best_size:
                best_edge = edge
                best_available = available
                best_size = size
                if size == 1:
                    break
        if best_edge < 0:
            return True
        left, right = edges[best_edge]
        available = best_available
        while available:
            color = available & -available
            available -= color
            colors[best_edge] = color
            used[left] |= color
            used[right] |= color
            if search():
                return True
            used[left] ^= color
            used[right] ^= color
            colors[best_edge] = 0
        return False

    return search()


def validate_frontier2_witnesses() -> dict[str, list[dict[str, object]]]:
    package = json.loads(FRONTIER2_WITNESSES.read_text())
    assert package["schema"] == "d5-frontier2-nontait-fivecdc-witnesses-v1"
    modes = package["modes"]
    assert {mode: len(rows) for mode, rows in modes.items()} == {
        "AA": 2, "AB": 4, "BB": 6
    }
    for rows in modes.values():
        for row in rows:
            vertices, edges = parse_graph6(row["graph6"])
            independently_validate_graph(vertices, edges)
            assert not independently_tait_colorable(vertices, edges)
            labels = row["fivecdc_label_masks"]
            assert len(labels) == len(edges)
            assert all(label.bit_count() == 2 for label in labels)
            for incident_edges in incidence(vertices, edges):
                assert reduce(
                    int.__xor__,
                    (labels[edge] for edge in incident_edges),
                    0,
                ) == 0
    return modes


def run_frontier2(directory: Path) -> list[dict[str, object]]:
    generator, checker = compile_frontier2(directory)
    frozen_witnesses = validate_frontier2_witnesses()
    expected = {
        "AA": (
            252,
            "855bac19a88ad1ebb0f7d8f3c2c4e82095aab0f27b2487e9f0489b3f6abdab20",
            250,
            2,
        ),
        "AB": (
            765,
            "d77497f7d01c07983e973f1bb3e60a9812e1a3b2bf71e22f0567d44bf03d2122",
            761,
            4,
        ),
        "BB": (
            844,
            "89b119cb1f18ad8d7390a2c60f15b274a7685fe90225530f4821139aef62ac2a",
            838,
            6,
        ),
    }
    rows = []
    for mode, (classes, digest, tait, non_tait) in expected.items():
        canonical = directory / f"frontier2-{mode}.g6"
        generated = subprocess.Popen(
            [str(generator), mode],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert generated.stdout is not None
        with canonical.open("wb") as output:
            reduced = subprocess.run(
                [
                    "shortg", "-q", f"-T{directory}", "-Z50%",
                ],
                stdin=generated.stdout,
                stdout=output,
                stderr=subprocess.PIPE,
                check=True,
            )
        generated.stdout.close()
        generator_stderr = (
            generated.stderr.read().decode() if generated.stderr else ""
        )
        assert generated.wait() == 0
        assert not reduced.stderr
        generation = json.loads(generator_stderr)
        assert generation == {
            "mode": mode,
            "pairing_leaves": 4466880,
            "accepted": 4435200,
        }
        records = canonical.read_text().splitlines()
        assert len(records) == classes
        assert len(set(records)) == classes
        actual_digest = hashlib.sha256(canonical.read_bytes()).hexdigest()
        assert actual_digest == digest
        for record in records:
            independently_validate_graph(*parse_graph6(record))
        with canonical.open("rb") as source:
            checked = subprocess.run(
                [str(checker), "--emit-nontait"],
                stdin=source,
                capture_output=True,
                text=True,
                check=True,
            )
        emitted_witnesses = [
            json.loads(line) for line in checked.stderr.splitlines()
        ]
        assert emitted_witnesses == frozen_witnesses[mode]
        result = json.loads(checked.stdout)
        assert result == {
            "classification": "ALL_FIVECDC_SAT",
            "graphs": classes,
            "tait": tait,
            "non_tait": non_tait,
            "fivecdc": classes,
            "non_tait_fivecdc": non_tait,
        }
        rows.append(
            {
                "mode": mode,
                "pairing_leaves": generation["pairing_leaves"],
                "accepted_labelled_pairings": generation["accepted"],
                "isomorphism_classes": classes,
                "canonical_graph6_sha256": digest,
                "tait": tait,
                "non_tait": non_tait,
                "fivecdc": classes,
                "fivecdc_unsat": 0,
            }
        )
    return rows


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
    parser.add_argument("--frontier2", action="store_true")
    parser.add_argument("--frontier3", action="store_true")
    parser.add_argument("--frontier4", action="store_true")
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
    assert sum(
        transform_relation(c5_mask, permutation) == c5_mask
        for permutation in permutations(range(5))
    ) == 10
    assert sum(
        transform_relation(a_mask, permutation) == a_mask
        for permutation in permutations(range(4))
    ) == 8
    assert sum(
        transform_relation(b_mask, permutation) == b_mask
        for permutation in permutations(range(4))
    ) == 24
    assert loopless_pairing_count((5, 5, 4, 4)) == 4466880
    assert macro_frontier2_count() == (12, 4435200)
    assert frontier3_macro_counts() == (
        178, {"AAA": 25, "AAB": 56, "ABB": 56, "BBB": 25}
    )
    assert frontier4_macro_counts() == (
        4222,
        {
            "AAAA": 143, "AAAB": 410, "AABB": 643,
            "ABBB": 410, "BBBB": 143,
        },
    )

    with tempfile.TemporaryDirectory(prefix="d5-macro-replay-") as raw:
        replay_directory = Path(raw)
        binary = compile_search(replay_directory)
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
        frontier2_rows = (
            run_frontier2(replay_directory)
            if arguments.frontier2 else []
        )
        frontier3_row = (
            run_frontier3(replay_directory)
            if arguments.frontier3 else None
        )
        frontier4_row = (
            run_frontier4(replay_directory)
            if arguments.frontier4 else None
        )

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
                "frontier2_combinatorics": {
                    "loopless_pairing_leaves": 4466880,
                    "bridgeless_macro_matrices": 12,
                    "accepted_labelled_pairings_per_mode": 4435200,
                },
                "frontier2_rows": frontier2_rows,
                "frontier3": frontier3_row,
                "frontier4": frontier4_row,
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
