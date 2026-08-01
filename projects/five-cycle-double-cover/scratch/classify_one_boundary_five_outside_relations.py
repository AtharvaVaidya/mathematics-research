#!/usr/bin/env python3
"""Exact D5 boundary relations of the small one-boundary-five outsides.

This is a standard-library finite census for the retained incidence
patterns produced by ``enumerate_one_boundary_five_outside.py``.

For s in {1,2}, the outside has:

* W = U union A, with |U|=4 and |A|=s;
* root edges 01 and 23 in U;
* s+1 indistinguishable cubic vertices Z, each adjacent to three
  distinct vertices of W; and
* five ordered boundary semiedges, with as many semiedges at w as the
  unused cubic degree of w.

Every proper edge and boundary semiedge is labelled by a two-subset of
{0,1,2,3,4}.  The xor of the incident labels is zero at every completed
cubic vertex.  The script computes the exact ordered boundary relation,
quotiented only by the global S5 action on coordinates.

It also computes the greatest subset of the complement that obeys the
elementary bichromatic-path switching laws forced on every realizable
five-pole relation.  An empty greatest core proves that no nonempty
realizable relation can avoid the outside relation.  A nonempty core is
only a limitation of this switching test; it is not a graph-realizable
obstruction.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import argparse
import json
from pathlib import Path

from enumerate_one_boundary_five_outside import (
    attainable_profile,
    component_boundary_condition,
    graph_data,
    locally_cyclic_four,
    strict_hall,
)
from pole_state_search import (
    D,
    boundary_orbit_representatives,
    color_orbit_representative,
    satisfiable,
)


COLORS = range(5)
REPRESENTATIVES = boundary_orbit_representatives()
REPRESENTATIVE_SET = frozenset(REPRESENTATIVES)


def retained_patterns(
    s: int,
) -> tuple[
    tuple[
        tuple[tuple[int, int, int], ...],
        list[int],
        tuple[int, ...],
    ],
    ...,
]:
    """Return (Z-neighbourhoods, adjacency, boundary multiplicities)."""
    w_count = s + 4
    rows_available = tuple(combinations(range(w_count), 3))
    answer = []
    for rows in combinations_with_replacement(rows_available, s + 1):
        adjacency, boundary = graph_data(s, rows)
        if any(value < 0 for value in boundary):
            continue
        if not strict_hall(s, rows, boundary):
            continue
        if not component_boundary_condition(adjacency, boundary):
            continue
        if not locally_cyclic_four(adjacency, boundary):
            continue
        _, by_root = attainable_profile(s, rows, boundary)
        if any(not values for values in by_root):
            continue
        if sum(boundary) != 5:
            raise AssertionError("outside does not have five semiedges")
        answer.append((rows, adjacency, boundary))
    return tuple(answer)


def internal_edges(adjacency: list[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left, row in enumerate(adjacency)
        for right in range(left + 1, len(adjacency))
        if row >> right & 1
    )


def boundary_relation(
    adjacency: list[int],
    boundary: tuple[int, ...],
) -> frozenset[tuple[int, ...]]:
    """Compute the exact 62-orbit relation for the canonical stub order."""
    edges = internal_edges(adjacency)
    incident: list[list[int]] = [[] for _ in adjacency]
    for edge_id, (left, right) in enumerate(edges):
        incident[left].append(edge_id)
        incident[right].append(edge_id)

    boundary_positions: list[list[int]] = [[] for _ in adjacency]
    cursor = 0
    for vertex, multiplicity in enumerate(boundary):
        for _ in range(multiplicity):
            boundary_positions[vertex].append(cursor)
            cursor += 1
    if cursor != 5:
        raise AssertionError("wrong boundary size")

    result = set()
    for word in REPRESENTATIVES:
        constraints = []
        for vertex in range(len(adjacency)):
            target = 0
            for position in boundary_positions[vertex]:
                target ^= word[position]
            constraints.append((tuple(incident[vertex]), target))
        if satisfiable(len(edges), tuple(constraints)):
            result.add(word)
    return frozenset(result)


def toggle(
    word: tuple[int, ...],
    positions: tuple[int, ...],
    pair: int,
) -> tuple[int, ...]:
    output = list(word)
    for position in positions:
        output[position] ^= pair
        if output[position] not in D:
            raise AssertionError("switch left the D5 alphabet")
    representative = color_orbit_representative(tuple(output))
    if representative not in REPRESENTATIVE_SET:
        raise AssertionError("switch broke the even-boundary condition")
    return representative


@lru_cache(maxsize=None)
def switching_requirements(
    word: tuple[int, ...],
) -> tuple[
    tuple[
        tuple[tuple[int, ...], ...],
        tuple[tuple[tuple[int, ...], ...], ...],
    ],
    ...,
]:
    """Return (mandatory states, alternative state-groups) per color pair.

    Every mandatory state must remain.  At least one alternative group
    must remain in its entirety.  For four boundary ends the mandatory
    state is obtained by switching both paths, while each of the three
    alternative groups corresponds to one possible pairing of the four
    ends and contains the two single-path switches.
    """
    result = []
    for left, right in combinations(COLORS, 2):
        pair = (1 << left) | (1 << right)
        positions = tuple(
            position
            for position, value in enumerate(word)
            if bool(value & (1 << left))
            ^ bool(value & (1 << right))
        )
        if len(positions) == 0:
            continue
        if len(positions) == 2:
            switched = toggle(word, positions, pair)
            result.append(((switched,), ((switched,),)))
            continue
        if len(positions) != 4:
            raise AssertionError("boundary parity produced 1, 3, or 5 ends")
        first, second, third, fourth = positions
        pairings = (
            ((first, second), (third, fourth)),
            ((first, third), (second, fourth)),
            ((first, fourth), (second, third)),
        )
        mandatory = (toggle(word, positions, pair),)
        alternatives = tuple(
            tuple(toggle(word, endpoint_pair, pair)
                  for endpoint_pair in pairing)
            for pairing in pairings
        )
        result.append((mandatory, alternatives))
    return tuple(result)


def greatest_switching_core(
    allowed: frozenset[tuple[int, ...]] | set[tuple[int, ...]],
) -> frozenset[tuple[int, ...]]:
    """Greatest subset closed under the elementary path-switching laws."""
    current = set(allowed)
    while True:
        retained = set()
        for word in current:
            valid = True
            for mandatory, alternatives in switching_requirements(word):
                if any(state not in current for state in mandatory):
                    valid = False
                    break
                if not any(
                    all(state in current for state in group)
                    for group in alternatives
                ):
                    valid = False
                    break
            if valid:
                retained.add(word)
        if retained == current:
            return frozenset(current)
        current = retained


def cap_extension_count(boundary: tuple[int, ...]) -> int:
    count = 0
    for start in D:
        current = start
        for value in boundary:
            current ^= value
            if current not in D:
                break
        else:
            if current != start:
                raise AssertionError("even boundary did not close")
            count += 1
    return count


def five_cycle_cap_relations() -> tuple[frozenset[tuple[int, ...]], ...]:
    """The 12 distinct ordered C5-cap relations modulo reversal/rotation."""
    from itertools import permutations

    cyclic_orders = tuple(
        (0, *tail)
        for tail in permutations((1, 2, 3, 4))
        if tail[0] < tail[-1]
    )
    relations = tuple(
        frozenset(
            word
            for word in REPRESENTATIVES
            if cap_extension_count(
                tuple(word[position] for position in order)
            )
        )
        for order in cyclic_orders
    )
    if len(relations) != 12 or any(len(relation) != 46
                                   for relation in relations):
        raise AssertionError("C5-cap relation census changed")
    return relations


def profile_order(s: int) -> dict[str, object]:
    patterns = retained_patterns(s)
    cap_relations = five_cycle_cap_relations()
    profile: Counter[tuple[tuple[int, ...], int, int]] = Counter()
    cap_hit_profiles: Counter[tuple[int, ...]] = Counter()
    examples: dict[tuple[tuple[int, ...], int, int], dict[str, object]] = {}

    for rows, adjacency, boundary in patterns:
        relation = boundary_relation(adjacency, boundary)
        if greatest_switching_core(relation) != relation:
            raise AssertionError("computed cap relation is not switch-closed")
        complement = REPRESENTATIVE_SET - relation
        core = greatest_switching_core(complement)
        stub_vertices = [
            vertex
            for vertex, multiplicity in enumerate(boundary)
            for _ in range(multiplicity)
        ]
        repeated_positions = tuple(
            position
            for position, vertex in enumerate(stub_vertices)
            if stub_vertices.count(vertex) == 2
        )
        local_incompatible = None
        if repeated_positions:
            if len(repeated_positions) != 2:
                raise AssertionError("unexpected boundary multiplicity")
            left, right = repeated_positions
            local_incompatible = frozenset(
                word
                for word in REPRESENTATIVES
                if (word[left] ^ word[right]) not in D
            )
            if len(local_incompatible) != 25:
                raise AssertionError("local incompatible orbit count changed")
            if core != local_incompatible:
                raise AssertionError(
                    "complement core is not exactly the local obstruction"
                )
        shape = tuple(sorted((value for value in boundary if value),
                             reverse=True))
        key = (shape, len(relation), len(core))
        profile[key] += 1
        hits = tuple(len(core & cap) for cap in cap_relations)
        cap_hit_profiles[hits] += 1
        examples.setdefault(key, {
            "z_neighbourhoods": [list(row) for row in rows],
            "boundary_multiplicities": list(boundary),
            "boundary_stub_vertices": [
                *stub_vertices
            ],
            "repeated_boundary_positions": list(repeated_positions),
            "core_equals_local_repeated_vertex_incompatibility": (
                local_incompatible is not None
                and core == local_incompatible
            ),
            "outside_relation_indices": [
                index for index, word in enumerate(REPRESENTATIVES)
                if word in relation
            ],
            "complement_switching_core_indices": [
                index for index, word in enumerate(REPRESENTATIVES)
                if word in core
            ],
            "switching_core_C5_cap_hits": list(hits),
        })

    return {
        "s": s,
        "retained_patterns": len(patterns),
        "profile": [
            {
                "boundary_multiplicity_shape": list(shape),
                "outside_relation_orbits": relation_size,
                "complement_greatest_switching_core_orbits": core_size,
                "patterns": count,
                "example": examples[(shape, relation_size, core_size)],
            }
            for (shape, relation_size, core_size), count
            in sorted(profile.items())
        ],
        "switching_core_C5_cap_hit_profiles": [
            {"hits": list(hits), "patterns": count}
            for hits, count in sorted(cap_hit_profiles.items())
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        help="write the canonical JSON report to this path instead of stdout",
    )
    parser.add_argument(
        "--max-s",
        type=int,
        default=2,
        choices=(1, 2, 3),
        help="largest outside parameter to classify (default: 2)",
    )
    arguments = parser.parse_args()
    report = {
        "schema": "one-boundary-five-outside-D5-relations-v1",
        "classification": "EXACT FINITE BOUNDARY-RELATION CENSUS",
        "boundary_color_orbits": len(REPRESENTATIVES),
        "orders": [
            profile_order(s) for s in range(1, arguments.max_s + 1)
        ],
        "interpretation": {
            "empty_complement_core": (
                "Every nonempty graph-realizable five-pole relation "
                "intersects this outside relation, using only elementary "
                "bichromatic path switching."
            ),
            "nonempty_complement_core": (
                "The elementary switching axioms alone do not force an "
                "intersection. No graph realizing the core is asserted."
            ),
        },
        "scope_warning": (
            "This closes only the outside relations with empty complement "
            "core. It is not a proof or disproof of FiveCDC."
        ),
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(payload, end="")
    else:
        arguments.output.write_text(payload, encoding="ascii")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
