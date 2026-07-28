#!/usr/bin/env python3
"""Independent replay of the small outside D5-relation census.

The primary classifier uses a generic finite-domain CSP solver.  This
checker instead enumerates the allowed local completions at each vertex
and performs a vertex-row join over shared proper edges.  It independently
reconstructs the 62 coordinate orbits and the switching-core operator,
then compares the complete aggregate profiles with the retained JSON.

The structural pattern generator is imported from the primary script;
the D5 satisfiability and switching calculations are independently
implemented here.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import argparse
import json
from pathlib import Path

from classify_one_boundary_five_outside_relations import retained_patterns


COLORS = range(5)
VALUES = tuple(
    sum(1 << color for color in pair)
    for pair in combinations(COLORS, 2)
)
VALUE_SET = frozenset(VALUES)
COLOR_ACTIONS = tuple(permutations(COLORS))


@lru_cache(maxsize=None)
def act(value: int, permutation: tuple[int, ...]) -> int:
    return sum(
        1 << permutation[color]
        for color in COLORS
        if value >> color & 1
    )


@lru_cache(maxsize=None)
def representative(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(act(value, permutation) for value in word)
        for permutation in COLOR_ACTIONS
    )


def orbit_representatives() -> tuple[tuple[int, ...], ...]:
    answer = set()
    for prefix in product(VALUES, repeat=4):
        final = prefix[0] ^ prefix[1] ^ prefix[2] ^ prefix[3]
        if final in VALUE_SET:
            answer.add(representative((*prefix, final)))
    if len(answer) != 62:
        raise AssertionError("independent orbit reconstruction failed")
    return tuple(sorted(answer))


ORBITS = orbit_representatives()
ORBIT_SET = frozenset(ORBITS)


def proper_edges(adjacency: list[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left] >> right & 1
    )


def word_extends(
    adjacency: list[int],
    boundary: tuple[int, ...],
    word: tuple[int, ...],
) -> bool:
    """Join independently generated local rows over the proper edges."""
    edges = proper_edges(adjacency)
    incident: list[list[int]] = [[] for _ in adjacency]
    for edge, (left, right) in enumerate(edges):
        incident[left].append(edge)
        incident[right].append(edge)

    boundary_values: list[list[int]] = [[] for _ in adjacency]
    cursor = 0
    for vertex, multiplicity in enumerate(boundary):
        for _ in range(multiplicity):
            boundary_values[vertex].append(word[cursor])
            cursor += 1
    if cursor != 5:
        raise AssertionError("wrong number of boundary values")

    rows: list[tuple[tuple[int, ...], ...]] = []
    for vertex in range(len(adjacency)):
        fixed_xor = 0
        for value in boundary_values[vertex]:
            fixed_xor ^= value
        local = tuple(
            assignment
            for assignment in product(
                VALUES, repeat=len(incident[vertex])
            )
            if fixed_xor ^ xor_tuple(assignment) == 0
        )
        if not local:
            return False
        rows.append(local)

    assigned = [0] * len(edges)
    full_vertices = (1 << len(adjacency)) - 1
    failed: set[tuple[int, tuple[int, ...]]] = set()

    def visit(done: int) -> bool:
        if done == full_vertices:
            return True
        key = (done, tuple(assigned))
        if key in failed:
            return False

        best_vertex = -1
        best_rows: list[tuple[int, ...]] | None = None
        for vertex in range(len(adjacency)):
            if done >> vertex & 1:
                continue
            compatible = [
                row
                for row in rows[vertex]
                if all(
                    assigned[edge] in (0, value)
                    for edge, value in zip(incident[vertex], row)
                )
            ]
            if not compatible:
                failed.add(key)
                return False
            if best_rows is None or len(compatible) < len(best_rows):
                best_vertex = vertex
                best_rows = compatible
        if best_rows is None:
            raise AssertionError("missing unprocessed vertex")

        for row in best_rows:
            changed = []
            for edge, value in zip(incident[best_vertex], row):
                if assigned[edge] == 0:
                    assigned[edge] = value
                    changed.append(edge)
            if visit(done | (1 << best_vertex)):
                return True
            for edge in changed:
                assigned[edge] = 0
        failed.add(key)
        return False

    return visit(0)


def xor_tuple(values: tuple[int, ...]) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def relation(
    adjacency: list[int],
    boundary: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    return frozenset(
        word for word in ORBITS
        if word_extends(adjacency, boundary, word)
    )


def switch(
    word: tuple[int, ...],
    positions: tuple[int, ...],
    pair: int,
) -> tuple[int, ...]:
    output = list(word)
    for position in positions:
        output[position] ^= pair
    if any(value not in VALUE_SET for value in output):
        raise AssertionError("invalid switched label")
    return representative(tuple(output))


@lru_cache(maxsize=None)
def laws(
    word: tuple[int, ...],
) -> tuple[
    tuple[tuple[int, ...] | None, tuple[tuple[tuple[int, ...], ...], ...]],
    ...,
]:
    answer = []
    for left, right in combinations(COLORS, 2):
        pair = (1 << left) | (1 << right)
        ends = tuple(
            position
            for position, value in enumerate(word)
            if ((value >> left) & 1) != ((value >> right) & 1)
        )
        if not ends:
            continue
        if len(ends) == 2:
            output = switch(word, ends, pair)
            answer.append((output, ((output,),)))
            continue
        if len(ends) != 4:
            raise AssertionError("odd bichromatic boundary")
        a, b, c, d = ends
        alternatives = tuple(
            tuple(switch(word, path, pair) for path in pairing)
            for pairing in (
                ((a, b), (c, d)),
                ((a, c), (b, d)),
                ((a, d), (b, c)),
            )
        )
        answer.append((switch(word, ends, pair), alternatives))
    return tuple(answer)


def switching_core(
    initial: frozenset[tuple[int, ...]] | set[tuple[int, ...]],
) -> frozenset[tuple[int, ...]]:
    current = set(initial)
    while True:
        following = {
            word
            for word in current
            if all(
                mandatory in current
                and any(
                    all(output in current for output in alternative)
                    for alternative in alternatives
                )
                for mandatory, alternatives in laws(word)
            )
        }
        if following == current:
            return frozenset(current)
        current = following


def c5_cap_sets() -> tuple[frozenset[tuple[int, ...]], ...]:
    orders = tuple(
        (0, *tail)
        for tail in permutations((1, 2, 3, 4))
        if tail[0] < tail[-1]
    )
    answer = []
    for order in orders:
        accepted = set()
        for word in ORBITS:
            ordered = tuple(word[position] for position in order)
            for initial in VALUES:
                current = initial
                valid = True
                for value in ordered:
                    current ^= value
                    if current not in VALUE_SET:
                        valid = False
                        break
                if valid and current == initial:
                    accepted.add(word)
                    break
        answer.append(frozenset(accepted))
    result = tuple(answer)
    if len(result) != 12 or any(len(cap) != 46 for cap in result):
        raise AssertionError("independent C5-cap reconstruction failed")
    return result


def expected_profiles(report: dict[str, object]) -> dict[int, Counter]:
    result = {}
    for order in report["orders"]:
        counter = Counter()
        for row in order["profile"]:
            counter[(
                tuple(row["boundary_multiplicity_shape"]),
                row["outside_relation_orbits"],
                row["complement_greatest_switching_core_orbits"],
            )] += row["patterns"]
        result[order["s"]] = counter
    return result


def replay(report: dict[str, object]) -> dict[str, object]:
    expected = expected_profiles(report)
    caps = c5_cap_sets()
    actual: dict[int, Counter] = {}
    hit_profiles: dict[int, Counter] = {}

    for s in (1, 2):
        profile = Counter()
        hits = Counter()
        patterns = retained_patterns(s)
        for _, adjacency, boundary in patterns:
            outside = relation(adjacency, boundary)
            if switching_core(outside) != outside:
                raise AssertionError("independent outside relation not closed")
            core = switching_core(ORBIT_SET - outside)
            shape = tuple(
                sorted((value for value in boundary if value), reverse=True)
            )
            profile[(shape, len(outside), len(core))] += 1
            hits[tuple(len(core & cap) for cap in caps)] += 1

            stub_vertices = tuple(
                vertex
                for vertex, multiplicity in enumerate(boundary)
                for _ in range(multiplicity)
            )
            repeated = tuple(
                position
                for position, vertex in enumerate(stub_vertices)
                if stub_vertices.count(vertex) == 2
            )
            if repeated:
                left, right = repeated
                local_bad = frozenset(
                    word
                    for word in ORBITS
                    if (word[left] ^ word[right]) not in VALUE_SET
                )
                if len(local_bad) != 25 or core != local_bad:
                    raise AssertionError("independent local-core identity failed")

        if profile != expected[s]:
            raise AssertionError(
                f"aggregate relation profile differs for s={s}: "
                f"{profile!r} != {expected[s]!r}"
            )
        actual[s] = profile
        hit_profiles[s] = hits

    return {
        "schema": "one-boundary-five-outside-D5-independent-replay-v1",
        "status": "PASS",
        "boundary_color_orbits": len(ORBITS),
        "patterns": {
            str(s): sum(actual[s].values()) for s in actual
        },
        "profiles": {
            str(s): [
                {
                    "boundary_multiplicity_shape": list(shape),
                    "outside_relation_orbits": relation_size,
                    "complement_core_orbits": core_size,
                    "patterns": count,
                }
                for (shape, relation_size, core_size), count
                in sorted(actual[s].items())
            ]
            for s in actual
        },
        "switching_core_C5_cap_hit_profiles": {
            str(s): [
                {"hits": list(row), "patterns": count}
                for row, count in sorted(hit_profiles[s].items())
            ]
            for s in hit_profiles
        },
        "method": (
            "Independent local-row join over shared proper-edge labels; "
            "no use of the primary finite-domain satisfiability solver."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        type=Path,
        default=Path(__file__).with_name(
            "one-boundary-five-outside-relations.json"
        ),
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    report = json.loads(arguments.report.read_text(encoding="ascii"))
    result = replay(report)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(payload, end="")
    else:
        arguments.output.write_text(payload, encoding="ascii")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
