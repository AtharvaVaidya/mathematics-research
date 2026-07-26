#!/usr/bin/env python3
"""Clean-room audit of the retained stable-eight paired-cut result.

This implementation deliberately does not import or execute
check_stable8_paired_cuts.py.  It finds every cut of size at most three by
literal edge-deletion enumeration, reconstructs all 105 perfect matchings,
and checks the retained result after normalizing away row order.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_PATH = HERE / "stable8-paired-cut-result.json"
EXPANDED_PATH = HERE / "stable8-first.graph.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    values = [ord(character) - 63 for character in text.strip()]
    require(values and 0 <= values[0] <= 62, "only short graph6 supported")
    n = values[0]
    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: list[tuple[int, int]] = []
    position = 0
    for upper in range(1, n):
        for lower in range(upper):
            if bits[position]:
                edges.append((lower, upper))
            position += 1
    return n, tuple(sorted(edges))


def incidence(
    n: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    rows: list[list[int]] = [[] for _ in range(n)]
    for edge, (u, v) in enumerate(edges):
        rows[u].append(edge)
        rows[v].append(edge)
    return tuple(tuple(row) for row in rows)


def components_after_deletion(
    n: int,
    edges: tuple[tuple[int, int], ...],
    rows: tuple[tuple[int, ...], ...],
    deleted: frozenset[int],
) -> tuple[frozenset[int], ...]:
    seen = [False] * n
    parts: list[frozenset[int]] = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        stack = [root]
        part: set[int] = set()
        while stack:
            vertex = stack.pop()
            part.add(vertex)
            for edge in rows[vertex]:
                if edge in deleted:
                    continue
                u, v = edges[edge]
                other = v if u == vertex else u
                if not seen[other]:
                    seen[other] = True
                    stack.append(other)
        parts.append(frozenset(part))
    return tuple(parts)


def boundary_ids(
    edges: tuple[tuple[int, int], ...], shore: frozenset[int]
) -> tuple[int, ...]:
    return tuple(
        edge
        for edge, (u, v) in enumerate(edges)
        if (u in shore) != (v in shore)
    )


def induced_has_cycle(
    vertices: frozenset[int],
    edges: tuple[tuple[int, int], ...],
) -> bool:
    if not vertices:
        return False
    internal = [
        (u, v) for u, v in edges if u in vertices and v in vertices
    ]
    adjacency: dict[int, list[int]] = {vertex: [] for vertex in vertices}
    for u, v in internal:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen: set[int] = set()
    component_count = 0
    for root in vertices:
        if root in seen:
            continue
        component_count += 1
        seen.add(root)
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
    return len(internal) - len(vertices) + component_count > 0


def enumerate_small_cyclic_cuts(
    n: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[dict[str, object], ...]:
    """Enumerate by deleting every one-, two-, and three-edge set.

    For completeness, every union of deletion components is considered.
    Requiring vertex zero on the stored shore quotients by complementation.
    """

    rows = incidence(n, edges)
    all_vertices = frozenset(range(n))
    found: dict[tuple[int, ...], dict[str, object]] = {}
    for size in (1, 2, 3):
        for deleted_row in combinations(range(len(edges)), size):
            deleted = frozenset(deleted_row)
            parts = components_after_deletion(n, edges, rows, deleted)
            if len(parts) == 1:
                continue
            part_zero = next(
                index for index, part in enumerate(parts) if 0 in part
            )
            for selection in range(1, 1 << len(parts)):
                if not ((selection >> part_zero) & 1):
                    continue
                if selection == (1 << len(parts)) - 1:
                    continue
                shore = frozenset().union(*(
                    parts[index]
                    for index in range(len(parts))
                    if (selection >> index) & 1
                ))
                cut = boundary_ids(edges, shore)
                if not 1 <= len(cut) <= 3:
                    continue
                opposite = all_vertices - shore
                if not (
                    induced_has_cycle(shore, edges)
                    and induced_has_cycle(opposite, edges)
                ):
                    continue
                key = tuple(sorted(shore))
                found[key] = {
                    "shore": key,
                    "boundary_ids": cut,
                    "boundary": tuple(edges[edge] for edge in cut),
                    "boundary_size": len(cut),
                }
    return tuple(
        sorted(
            found.values(),
            key=lambda row: (
                int(row["boundary_size"]),
                tuple(row["boundary"]),
                tuple(row["shore"]),
            ),
        )
    )


def perfect_matchings(
    objects: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not objects:
        return ((),)
    first = objects[0]
    result: list[tuple[tuple[int, int], ...]] = []
    for position in range(1, len(objects)):
        second = objects[position]
        remaining = objects[1:position] + objects[position + 1 :]
        for tail in perfect_matchings(remaining):
            result.append(((first, second),) + tail)
    return tuple(result)


def mark_partition(
    marks: tuple[tuple[int, int], ...],
    shore: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    internal: list[int] = []
    boundary: list[int] = []
    external: list[int] = []
    for mark, (u, v) in enumerate(marks):
        membership = int(u in shore) + int(v in shore)
        if membership == 2:
            internal.append(mark)
        elif membership == 1:
            boundary.append(mark)
        else:
            external.append(mark)
    return tuple(internal), tuple(boundary), tuple(external)


def strict_pair_crossings(
    pairing: tuple[tuple[int, int], ...],
    internal: tuple[int, ...],
    external: tuple[int, ...],
) -> int:
    inside = set(internal)
    outside = set(external)
    return sum(
        (first in inside and second in outside)
        or (second in inside and first in outside)
        for first, second in pairing
    )


def optimal_boundary_assignment(
    pairing: tuple[tuple[int, int], ...],
    internal: tuple[int, ...],
    boundary: tuple[int, ...],
) -> frozenset[int]:
    inside = set(internal)
    flexible = set(boundary)
    selected = set(internal)
    for first, second in pairing:
        if first in inside and second in flexible:
            selected.add(second)
        elif second in inside and first in flexible:
            selected.add(first)
        # External-boundary pairs and boundary-boundary pairs are kept out.
    return frozenset(selected)


def pairing_crossings(
    pairing: tuple[tuple[int, int], ...], selected: frozenset[int]
) -> int:
    return sum((u in selected) != (v in selected) for u, v in pairing)


def expand_core(
    n: int,
    edges: tuple[tuple[int, int], ...],
    marks: tuple[tuple[int, int], ...],
    pairing: tuple[tuple[int, int], ...],
) -> tuple[int, tuple[tuple[int, int], ...]]:
    mark_set = set(marks)
    expanded = [edge for edge in edges if edge not in mark_set]
    for mark, (u, v) in enumerate(marks):
        terminal = n + mark
        expanded.extend(((u, terminal), (v, terminal)))
    expanded.extend((n + u, n + v) for u, v in pairing)
    return n + len(marks), tuple(sorted(tuple(sorted(edge)) for edge in expanded))


def cut_size(
    edges: tuple[tuple[int, int], ...], shore: frozenset[int]
) -> int:
    return sum((u in shore) != (v in shore) for u, v in edges)


def solve_cycle_containing_marks(
    n: int,
    edges: tuple[tuple[int, int], ...],
    marked_ids: frozenset[int],
) -> frozenset[int]:
    """Solve the vertex-parity equations by independent GF(2) elimination."""

    free_edges = [edge for edge in range(len(edges)) if edge not in marked_ids]
    column = {edge: index for index, edge in enumerate(free_edges)}
    rows: list[list[int]] = []
    for vertex in range(n):
        coefficients = 0
        right = 0
        for edge, (u, v) in enumerate(edges):
            if vertex not in (u, v):
                continue
            if edge in marked_ids:
                right ^= 1
            else:
                coefficients ^= 1 << column[edge]
        rows.append([coefficients, right])

    pivot_rows: list[tuple[int, int]] = []
    rank = 0
    for col in range(len(free_edges)):
        bit = 1 << col
        selected = next(
            (row for row in range(rank, len(rows)) if rows[row][0] & bit),
            None,
        )
        if selected is None:
            continue
        rows[rank], rows[selected] = rows[selected], rows[rank]
        for row in range(len(rows)):
            if row != rank and rows[row][0] & bit:
                rows[row][0] ^= rows[rank][0]
                rows[row][1] ^= rows[rank][1]
        pivot_rows.append((rank, col))
        rank += 1
    require(
        not any(coefficients == 0 and right for coefficients, right in rows),
        "the all-one mark restriction is not in the cycle-space image",
    )
    assignment = 0
    for row, col in reversed(pivot_rows):
        coefficients, right = rows[row]
        other_parity = (coefficients & assignment).bit_count() & 1
        if other_parity ^ right:
            assignment ^= 1 << col
    selected_edges = set(marked_ids)
    selected_edges.update(
        edge
        for edge in free_edges
        if (assignment >> column[edge]) & 1
    )
    return frozenset(selected_edges)


def normalized_cut(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(row["shore"]),
        tuple(tuple(edge) for edge in row["boundary"]),
        int(row["boundary_size"]),
    )


def normalized_violation(row: dict[str, object]) -> tuple[object, ...]:
    return (
        tuple(row["shore"]),
        tuple(tuple(edge) for edge in row["boundary"]),
        int(row["boundary_size"]),
        tuple(row["internal_marks"]),
        tuple(row["boundary_marks"]),
        tuple(row["external_marks"]),
        int(row["strict_pair_crossings"]),
        int(row["score"]),
    )


def main() -> None:
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    n, edges = decode_graph6(str(expected["graph6"]))
    marks = tuple(tuple(sorted(map(int, edge))) for edge in expected["marks"])
    require((n, len(edges)) == (60, 90), "core order/size mismatch")
    require(len(set(edges)) == len(edges), "core is not simple")
    rows = incidence(n, edges)
    require(all(len(row) == 3 for row in rows), "core is not cubic")
    require(
        len(components_after_deletion(n, edges, rows, frozenset())) == 1,
        "core is disconnected",
    )
    require(all(mark in set(edges) for mark in marks), "missing marked edge")
    mark_vertices = [vertex for edge in marks for vertex in edge]
    require(len(set(mark_vertices)) == 16, "marks are not a matching")
    require(
        all(
            len(components_after_deletion(n, edges, rows, frozenset((edge,))))
            == 1
            for edge in range(len(edges))
        ),
        "core has a bridge",
    )

    cuts = enumerate_small_cyclic_cuts(n, edges)
    expected_cuts = {
        normalized_cut(row) for row in expected["small_cyclic_cuts"]
    }
    actual_cuts = {
        (
            tuple(row["shore"]),
            tuple(row["boundary"]),
            int(row["boundary_size"]),
        )
        for row in cuts
    }
    require(actual_cuts == expected_cuts, "small cyclic-cut list mismatch")

    pairings = perfect_matchings(tuple(range(8)))
    require(len(pairings) == 105, "perfect-matching count mismatch")
    expected_rows = expected["rows"]
    require(
        [tuple(tuple(pair) for pair in row["pairing"]) for row in expected_rows]
        == list(pairings),
        "pairing order/content mismatch",
    )

    all_vertices = frozenset(range(n))
    minimum_histogram: Counter[int] = Counter()
    actual_survivors = 0
    formula_checks = 0
    lifted_witnesses = 0
    for index, (pairing, expected_row) in enumerate(
        zip(pairings, expected_rows), start=1
    ):
        expanded_n, expanded_edges = expand_core(n, edges, marks, pairing)
        require((expanded_n, len(expanded_edges)) == (68, 102), "bad expansion")
        violations: list[dict[str, object]] = []
        minimum = 20
        for cut in cuts:
            shore = frozenset(cut["shore"])
            internal, boundary, external = mark_partition(marks, shore)
            p_value = strict_pair_crossings(
                pairing, internal, external
            )
            score = int(cut["boundary_size"]) + p_value
            minimum = min(minimum, score)

            # Brute-force every flexible boundary assignment, rather than
            # relying on the closed-form optimization in the audited note.
            observed_pair_terms: list[int] = []
            for subset in range(1 << len(boundary)):
                selected = frozenset(
                    set(internal)
                    | {
                        boundary[position]
                        for position in range(len(boundary))
                        if (subset >> position) & 1
                    }
                )
                pair_term = pairing_crossings(pairing, selected)
                observed_pair_terms.append(pair_term)
                lifted_shore = frozenset(
                    set(shore) | {n + mark for mark in selected}
                )
                direct = cut_size(expanded_edges, lifted_shore)
                require(
                    direct == int(cut["boundary_size"]) + pair_term,
                    "paired lift formula failed",
                )
                require(
                    induced_has_cycle(lifted_shore, expanded_edges)
                    and induced_has_cycle(
                        frozenset(range(expanded_n)) - lifted_shore,
                        expanded_edges,
                    ),
                    "a lifted cyclic shore lost all circuits",
                )
                formula_checks += 1
            require(
                min(observed_pair_terms) == p_value,
                "boundary optimization formula failed",
            )
            optimal = optimal_boundary_assignment(
                pairing, internal, boundary
            )
            require(
                pairing_crossings(pairing, optimal) == p_value,
                "constructive boundary assignment is not optimal",
            )
            if score < 4:
                lifted_witnesses += 1
                violations.append(
                    {
                        "shore": tuple(cut["shore"]),
                        "boundary": tuple(cut["boundary"]),
                        "boundary_size": int(cut["boundary_size"]),
                        "internal_marks": internal,
                        "boundary_marks": boundary,
                        "external_marks": external,
                        "strict_pair_crossings": p_value,
                        "score": score,
                    }
                )
        minimum_histogram[minimum] += 1
        if not violations:
            actual_survivors += 1
        require(index == int(expected_row["index"]), "row index mismatch")
        require(minimum == int(expected_row["minimum_score"]), "minimum mismatch")
        require(
            (not violations) == bool(expected_row["paired_cut_condition"]),
            "paired-cut Boolean mismatch",
        )
        require(
            {normalized_violation(row) for row in violations}
            == {
                normalized_violation(row)
                for row in expected_row["violations"]
            },
            "violation set mismatch",
        )

    require(
        {str(key): value for key, value in sorted(minimum_histogram.items())}
        == expected["minimum_score_histogram"],
        "minimum-score histogram mismatch",
    )
    require(actual_survivors == int(expected["surviving_pairings"]), "survivors")

    first_pairing = pairings[0]
    expanded_n, expanded_edges = expand_core(n, edges, marks, first_pairing)
    retained_expanded = json.loads(EXPANDED_PATH.read_text(encoding="utf-8"))
    retained_edges = tuple(sorted(
        tuple(sorted((int(row["u"]), int(row["v"]))))
        for row in retained_expanded["edges"]
    ))
    require(
        (expanded_n, expanded_edges)
        == (int(retained_expanded["vertices"]), retained_edges),
        "first retained expansion does not reconstruct from the core",
    )

    marked_ids = frozenset(edges.index(mark) for mark in marks)
    all_mark_cycle = solve_cycle_containing_marks(n, edges, marked_ids)
    cycle_degrees = [0] * n
    for edge in all_mark_cycle:
        u, v = edges[edge]
        cycle_degrees[u] += 1
        cycle_degrees[v] += 1
    require(
        all(degree % 2 == 0 for degree in cycle_degrees)
        and marked_ids <= all_mark_cycle,
        "all-mark cycle-space witness failed",
    )

    report = {
        "schema": "stable8-paired-cut-clean-room-audit-v1",
        "classification": "PASS_EXACT_MATCH",
        "algorithm": (
            "literal enumeration of all 1-, 2-, and 3-edge deletions; "
            "all component unions; all 105 perfect matchings; and every "
            "flexible boundary assignment"
        ),
        "core": {
            "vertices": n,
            "edges": len(edges),
            "simple": True,
            "cubic": True,
            "connected": True,
            "bridgeless": True,
            "marks": len(marks),
        },
        "small_cyclic_cuts": {
            "count": len(cuts),
            "size_histogram": dict(sorted(
                Counter(int(row["boundary_size"]) for row in cuts).items()
            )),
        },
        "pairings": {
            "count": len(pairings),
            "surviving": actual_survivors,
            "minimum_score_histogram": dict(sorted(minimum_histogram.items())),
            "lift_formula_checks": formula_checks,
            "lifted_violations": lifted_witnesses,
        },
        "first_expansion_reconstructed": True,
        "binary_cycle_containing_all_marks": {
            "exists": True,
            "edge_count": len(all_mark_cycle),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
