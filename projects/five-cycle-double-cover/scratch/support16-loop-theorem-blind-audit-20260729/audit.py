#!/usr/bin/env python3
"""Independent audit of the support-16 two-occurrence loop theorem.

This file imports no code from the candidate package.  It separately checks:

* affine/dihedral canonicalization of marked dirty words of lengths 4--6;
* literal short-loop and short-triple deletion failures;
* the finite shape reduction after the elementary human reductions;
* all four remaining labeled interaction profiles, using literal endpoint
  sets for cleaning and literal visited colour sets for deletion; and
* source hashes and disclosure/scope markers.

Arithmetic in F_2^2 is represented by xor on {0,1,2,3}.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent / "support16-loop-higheroccurrence-reduction-20260729"
VALUES = (1, 2, 3)
LINEAR_MAPS = tuple((0,) + row for row in itertools.permutations(VALUES))

EXPECTED_HASHES = {
    "HUMAN-PROOF.md":
        "104cddcead47f35f4d58d68c178bf217b56304393ca2a1f29abe13652a1f859a",
    "README.md":
        "d4d96c24263f965bea3b3530349f8d29aab3cb193c1acf1475a7bb5ba61b372c",
    "verify.py":
        "1448dc8cec614b078cc22808781b7744f6f35aed17bc087e3cbe8390170c1fa6",
}

EXPECTED_LOOP_REPRESENTATIVES = (
    ("010123", (1, 2)),
    ("010123", (1, 3)),
    ("010123", (2, 5)),
    ("010213", (1, 2)),
    ("010232", (1, 5)),
    ("012013", (0, 2)),
    ("012013", (1, 4)),
)
EXPECTED_TRIPLE_REPRESENTATIVES = (
    ("010213", (0, 1, 3)),
    ("010213", (1, 4, 5)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xor_all(values) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def increments(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        word[(position - 1) % len(word)] ^ word[position]
        for position in range(len(word))
    )


def dirty_proper(word: tuple[int, ...]) -> bool:
    return (
        set(word) == {0, 1, 2, 3}
        and all(
            word[position - 1] != word[position]
            for position in range(len(word))
        )
    )


def marked_transform(
    word: tuple[int, ...],
    marks: tuple[int, ...],
    orientation: int,
    anchor: int,
    linear: tuple[int, ...],
    translation: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Apply one AGL(2,2) colour map and one dihedral index map.

    The new colour at k is L(old[anchor + orientation*k]) + translation.
    Marks label derivatives between positions p-1 and p.  Solving for the
    corresponding new derivative index gives p-anchor for orientation +1 and
    anchor+1-p for orientation -1.
    """

    length = len(word)
    transformed_word = tuple(
        linear[word[(anchor + orientation * position) % length]]
        ^ translation
        for position in range(length)
    )
    if orientation == 1:
        transformed_marks = tuple(
            sorted((mark - anchor) % length for mark in marks)
        )
    else:
        transformed_marks = tuple(
            sorted((anchor + 1 - mark) % length for mark in marks)
        )

    old_steps = increments(word)
    new_steps = increments(transformed_word)
    expected_values = sorted(linear[old_steps[mark]] for mark in marks)
    observed_values = sorted(
        new_steps[mark] for mark in transformed_marks
    )
    assert observed_values == expected_values
    return transformed_word, transformed_marks


def marked_canonical(
    word: tuple[int, ...], marks: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    images = []
    for orientation in (1, -1):
        for anchor in range(len(word)):
            for linear in LINEAR_MAPS:
                for translation in range(4):
                    images.append(marked_transform(
                        word, marks, orientation, anchor,
                        linear, translation,
                    ))
    return min(images)


def interval_add(
    word: tuple[int, ...], first: int, second: int, delta: int,
) -> tuple[int, ...]:
    assert 0 <= first < second < len(word)
    result = list(word)
    for position in range(first, second):
        result[position] ^= delta
    return tuple(result)


def marked_word_audit() -> dict:
    loop_orbits: dict[int, Counter] = {
        length: Counter() for length in (4, 5, 6)
    }
    triple_orbits: dict[int, Counter] = {
        length: Counter() for length in (4, 5, 6)
    }
    tested = Counter()
    dirty_words = Counter()

    for length in (4, 5, 6):
        for word in itertools.product(range(4), repeat=length):
            if not dirty_proper(word):
                continue
            dirty_words[length] += 1
            steps = increments(word)

            for first, second in itertools.combinations(range(length), 2):
                if steps[first] != steps[second]:
                    continue
                tested[("loop", length)] += 1
                old_value = steps[first]
                deletes = False
                for new_value in VALUES:
                    if new_value == old_value:
                        continue
                    changed = interval_add(
                        word, first, second, old_value ^ new_value
                    )
                    changed_steps = increments(changed)
                    assert (
                        changed_steps[first] == new_value
                        and changed_steps[second] == new_value
                    )
                    assert all(
                        changed_steps[position] == steps[position]
                        for position in range(length)
                        if position not in (first, second)
                    )
                    deletes |= len(set(changed)) < 4
                if not deletes:
                    canonical = marked_canonical(word, (first, second))
                    assert marked_canonical(*canonical) == canonical
                    loop_orbits[length][canonical] += 1

            for marks in itertools.combinations(range(length), 3):
                if {steps[position] for position in marks} != set(VALUES):
                    continue
                tested[("triple", length)] += 1
                deletes = False
                for first, second in itertools.combinations(marks, 2):
                    delta = steps[first] ^ steps[second]
                    changed = interval_add(word, first, second, delta)
                    changed_steps = increments(changed)
                    assert changed_steps[first] == steps[second]
                    assert changed_steps[second] == steps[first]
                    assert all(
                        changed_steps[position] == steps[position]
                        for position in range(length)
                        if position not in (first, second)
                    )
                    deletes |= len(set(changed)) < 4
                if not deletes:
                    canonical = marked_canonical(word, marks)
                    assert marked_canonical(*canonical) == canonical
                    triple_orbits[length][canonical] += 1

    expected_tested = {
        ("loop", 4): 48,
        ("loop", 5): 360,
        ("loop", 6): 2304,
        ("triple", 5): 360,
        ("triple", 6): 2112,
    }
    assert tested == expected_tested
    assert [len(loop_orbits[length]) for length in (4, 5, 6)] == [0, 0, 7]
    assert [len(triple_orbits[length]) for length in (4, 5, 6)] == [0, 0, 2]

    loop_representatives = tuple(
        ("".join(map(str, word)), marks)
        for word, marks in sorted(loop_orbits[6])
    )
    triple_representatives = tuple(
        ("".join(map(str, word)), marks)
        for word, marks in sorted(triple_orbits[6])
    )
    assert loop_representatives == EXPECTED_LOOP_REPRESENTATIVES
    assert triple_representatives == EXPECTED_TRIPLE_REPRESENTATIVES
    assert sum(loop_orbits[6].values()) == 1080
    assert sum(triple_orbits[6].values()) == 576

    def weighted_rows(counter: Counter) -> list[dict]:
        return [
            {
                "word": "".join(map(str, word)),
                "marks": list(marks),
                "raw_instances": weight,
            }
            for (word, marks), weight in sorted(counter.items())
        ]

    return {
        "dirty_words": {str(length): dirty_words[length]
                        for length in (4, 5, 6)},
        "loop_tested": [tested[("loop", length)] for length in (4, 5, 6)],
        "loop_failure_orbits": [
            len(loop_orbits[length]) for length in (4, 5, 6)
        ],
        "loop_failure_raw_instances": [
            sum(loop_orbits[length].values()) for length in (4, 5, 6)
        ],
        "loop_length6_orbits": weighted_rows(loop_orbits[6]),
        "triple_tested": [
            tested[("triple", length)] for length in (4, 5, 6)
        ],
        "triple_failure_orbits": [
            len(triple_orbits[length]) for length in (4, 5, 6)
        ],
        "triple_failure_raw_instances": [
            sum(triple_orbits[length].values()) for length in (4, 5, 6)
        ],
        "triple_length6_orbits": weighted_rows(triple_orbits[6]),
    }


def perfect_pairings(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        remainder = items[1:index] + items[index + 1:]
        for tail in perfect_pairings(remainder):
            yield ((first, second),) + tail


def paired_port_audit() -> dict:
    requested = {
        (5, 3): 10,
        (5, 5): 1,
        (7, 3): 105,
        (7, 5): 21,
        (7, 7): 1,
    }
    pattern_counts = {}
    residual = 0
    for (length, port_count), expected in requested.items():
        patterns = 0
        for ports in itertools.combinations(range(length), port_count):
            port_set = set(ports)
            loop_positions = tuple(
                position for position in range(length)
                if position not in port_set
            )
            for pairing in perfect_pairings(loop_positions):
                symbol_at = [-1] * length
                for symbol, position in enumerate(ports):
                    symbol_at[position] = symbol
                for loop_offset, pair in enumerate(pairing):
                    symbol = port_count + loop_offset
                    symbol_at[pair[0]] = symbol
                    symbol_at[pair[1]] = symbol
                patterns += 1
                found = False
                symbol_count = port_count + len(pairing)
                for values in itertools.product(VALUES, repeat=symbol_count):
                    if xor_all(values[:port_count]) != 0:
                        continue
                    point = 0
                    visited = set()
                    for symbol in symbol_at:
                        visited.add(point)
                        point ^= values[symbol]
                    assert point == 0
                    if len(visited) < 4:
                        found = True
                        break
                residual += not found
        assert patterns == expected
        pattern_counts[f"{length}:{port_count}"] = patterns
    assert residual == 0
    return {"patterns": pattern_counts, "residual": residual}


def connected_three(multiplicities: tuple[int, int, int]) -> bool:
    neighbours = [set(), set(), set()]
    for count, (left, right) in zip(
        multiplicities, ((0, 1), (0, 2), (1, 2))
    ):
        if count:
            neighbours[left].add(right)
            neighbours[right].add(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in neighbours[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == 3


def normalized_flow_count(
    multiplicities: tuple[int, int, int], loops: tuple[int, ...],
) -> int:
    endpoints: list[tuple[int, int]] = []
    for pair, count in zip(
        ((0, 1), (0, 2), (1, 2)), multiplicities
    ):
        endpoints.extend([pair] * count)
    for vertex, count in enumerate(loops):
        endpoints.extend([(vertex, vertex)] * count)
    assert endpoints
    count = 0
    for tail in itertools.product(VALUES, repeat=len(endpoints) - 1):
        values = (1,) + tail
        charge = [0, 0, 0]
        for value, (left, right) in zip(values, endpoints):
            charge[left] ^= value
            charge[right] ^= value
        count += charge == [0, 0, 0]
    return count


def canonical_shape(
    lengths: tuple[int, int, int],
    loops: tuple[int, int, int],
    multiplicities: tuple[int, int, int],
) -> tuple:
    matrix = [
        [0, multiplicities[0], multiplicities[1]],
        [multiplicities[0], 0, multiplicities[2]],
        [multiplicities[1], multiplicities[2], 0],
    ]
    images = []
    for permutation in itertools.permutations(range(3)):
        vertex_data = tuple(
            (lengths[old], loops[old]) for old in permutation
        )
        edge_data = tuple(
            matrix[permutation[left]][permutation[right]]
            for left, right in ((0, 1), (0, 2), (1, 2))
        )
        images.append(vertex_data + edge_data)
    return min(images)


def shape_reduction_audit() -> dict:
    """Exhaust the post-dirty, connected-core shapes through support 16."""

    reasons = Counter()
    residual_shapes = set()
    flowable_shapes = set()
    examined_loop_allocations = 0

    # One core vertex is an explicit imported dependency (the universal
    # one-circuit tensor theorem), so the finite reduction begins at two.
    for vertex_count in (2, 3, 4):
        for lengths in itertools.combinations_with_replacement(
            range(4, 17), vertex_count
        ):
            if sum(lengths) > 16 or sum(lengths) % 2:
                continue
            loop_ranges = [
                range(length // 2 + 1) for length in lengths
            ]
            for loops in itertools.product(*loop_ranges):
                if not any(loops):
                    continue
                examined_loop_allocations += 1
                degrees = tuple(
                    length - 2 * loop_count
                    for length, loop_count in zip(lengths, loops)
                )

                if vertex_count == 2:
                    if degrees[0] != degrees[1] or degrees[0] == 0:
                        continue
                    # A positive parallel bundle is connected and flowability
                    # is equivalent to a zero-xor assignment on its ports.
                    core_flowable = degrees[0] != 1
                    if not core_flowable:
                        reasons["unflowable"] += 1
                        continue
                    reasons["two_vertex_paired_port"] += 1
                    continue

                if vertex_count == 4:
                    # Minimum dirty lengths force (4,4,4,4), already caught
                    # below by the constant even-length flow.
                    assert lengths == (4, 4, 4, 4)
                    reasons["all_even"] += 1
                    continue

                d0, d1, d2 = degrees
                numerators = (
                    d0 + d1 - d2,
                    d0 + d2 - d1,
                    d1 + d2 - d0,
                )
                if any(value < 0 or value % 2 for value in numerators):
                    continue
                multiplicities = tuple(value // 2 for value in numerators)
                if not connected_three(multiplicities):
                    continue
                flow_count = normalized_flow_count(multiplicities, loops)
                if not flow_count:
                    reasons["unflowable"] += 1
                    continue
                shape = canonical_shape(lengths, loops, multiplicities)
                flowable_shapes.add(shape)

                if all(length % 2 == 0 for length in lengths):
                    reasons["all_even"] += 1
                elif any(
                    loop_count and length <= 5
                    for length, loop_count in zip(lengths, loops)
                ):
                    reasons["short_loop"] += 1
                else:
                    residual_shapes.add(shape)
                    reasons["residual"] += 1

    expected_data = (
        ((4, 0), (5, 0), (7, 1), 2, 2, 3),
        ((4, 0), (5, 0), (7, 2), 3, 1, 2),
        ((5, 0), (5, 0), (6, 1), 3, 2, 2),
        ((5, 0), (5, 0), (6, 2), 4, 1, 1),
    )
    expected = {
        canonical_shape(
            tuple(item[0] for item in row[:3]),
            tuple(item[1] for item in row[:3]),
            tuple(row[3:]),
        )
        for row in expected_data
    }
    assert residual_shapes == expected
    return {
        "examined_loop_allocations": examined_loop_allocations,
        "flowable_connected_three_vertex_shapes": len(flowable_shapes),
        "elimination_counts": dict(sorted(reasons.items())),
        "residual_count": len(residual_shapes),
        "residual_shapes": [repr(shape) for shape in sorted(residual_shapes)],
        "imported_dependencies": [
            "the prior loopless theorem",
            "the universal one-circuit tensor theorem",
        ],
    }


def necklace_orders(tokens: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    canonical = set()
    for ordering in set(itertools.permutations(tokens)):
        images = []
        reverse = tuple(reversed(ordering))
        for shift in range(len(ordering)):
            images.append(ordering[shift:] + ordering[:shift])
            images.append(reverse[shift:] + reverse[:shift])
        canonical.add(min(images))
    return tuple(sorted(canonical))


@dataclass(frozen=True)
class Profile:
    name: str
    lengths: tuple[int, int, int]
    multiplicities: tuple[int, int, int]
    loop_count_at_two: int
    expected_order_counts: tuple[int, int, int]
    expected_states: int
    expected_flows: int
    expected_selected_clean: int
    expected_selected_delete: int


PROFILES = (
    Profile("457-a", (4, 5, 7), (2, 2, 3), 1,
            (3, 12, 180), 6480, 138, 0, 6480),
    Profile("457-b", (4, 5, 7), (3, 1, 2), 2,
            (3, 12, 90), 3240, 126, 0, 3240),
    Profile("556-a", (5, 5, 6), (3, 2, 2), 1,
            (12, 12, 30), 4320, 138, 168, 4152),
    Profile("556-b", (5, 5, 6), (4, 1, 1), 2,
            (12, 12, 16), 2304, 180, 12, 2292),
)


def profile_objects(profile: Profile):
    endpoints: list[tuple[int, int]] = []
    for pair, count in zip(
        ((0, 1), (0, 2), (1, 2)), profile.multiplicities
    ):
        endpoints.extend([pair] * count)
    endpoints.extend([(2, 2)] * profile.loop_count_at_two)
    appearances: list[list[int]] = [[], [], []]
    for edge, (left, right) in enumerate(endpoints):
        appearances[left].append(edge)
        appearances[right].append(edge)
    assert tuple(map(len, appearances)) == profile.lengths
    orders = tuple(
        necklace_orders(tuple(row)) for row in appearances
    )
    assert tuple(map(len, orders)) == profile.expected_order_counts
    return tuple(endpoints), orders


def profile_flows(
    endpoints: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    flows = []
    for tail in itertools.product(VALUES, repeat=len(endpoints) - 1):
        values = (1,) + tail
        charge = [0, 0, 0]
        for value, (left, right) in zip(values, endpoints):
            assert value in VALUES
            charge[left] ^= value
            charge[right] ^= value
        if charge == [0, 0, 0]:
            flows.append(values)
    return tuple(flows)


def literal_outcome(
    orders: tuple[tuple[int, ...], ...],
    values: tuple[int, ...],
    endpoints: tuple[tuple[int, int], ...],
) -> str | None:
    occurrence_segments: list[list[tuple[int, frozenset[int]]]] = [
        [] for _ in values
    ]
    deletion = False
    for vertex, order in enumerate(orders):
        point = 0
        visited = set()
        for edge in order:
            visited.add(point)
            successor = point ^ values[edge]
            occurrence_segments[edge].append(
                (vertex, frozenset((point, successor)))
            )
            point = successor
        assert point == 0
        deletion |= len(visited) < 4
    if deletion:
        return "D"

    assert all(len(occurrences) == 2 for occurrences in occurrence_segments)
    for edge, occurrences in enumerate(occurrence_segments):
        vertices = tuple(vertex for vertex, _segment in occurrences)
        left, right = endpoints[edge]
        if left == right:
            assert vertices == (left, left)
        else:
            assert set(vertices) == {left, right}

    # Fix the first circuit translation to zero; try all relative
    # translations of the other two.  Compare literal unoriented K4 endpoint
    # sets for the two occurrences of every edge, including both loop ends.
    for shift_one, shift_two in itertools.product(range(4), repeat=2):
        shifts = (0, shift_one, shift_two)
        clean = True
        for occurrences in occurrence_segments:
            shifted = []
            for vertex, segment in occurrences:
                shifted.append(frozenset(
                    endpoint ^ shifts[vertex] for endpoint in segment
                ))
            if shifted[0] != shifted[1]:
                clean = False
                break
        if clean:
            return "C"
    return None


def profile_audit() -> dict:
    report = []
    stream = hashlib.sha256()
    for profile in PROFILES:
        endpoints, order_sets = profile_objects(profile)
        flows = profile_flows(endpoints)
        assert len(flows) == profile.expected_flows
        selected = Counter()
        states = 0
        for orders in itertools.product(*order_sets):
            states += 1
            category = "R"
            for values in flows:
                outcome = literal_outcome(orders, values, endpoints)
                if outcome is not None:
                    category = outcome
                    break
            selected[category] += 1
            stream.update((
                profile.name + "|"
                + "|".join(",".join(map(str, row)) for row in orders)
                + "|" + category + "\n"
            ).encode("ascii"))
        assert states == profile.expected_states
        assert selected == {
            "C": profile.expected_selected_clean,
            "D": profile.expected_selected_delete,
        } or (
            profile.expected_selected_clean == 0
            and selected == {"D": profile.expected_selected_delete}
        )
        assert selected["R"] == 0
        report.append({
            "name": profile.name,
            "order_counts": list(profile.expected_order_counts),
            "states": states,
            "normalized_flows": len(flows),
            "selected_clean": selected["C"],
            "selected_delete": selected["D"],
            "residual": selected["R"],
            "loops_checked_literally": profile.loop_count_at_two,
        })
    digest = stream.hexdigest()
    assert digest == (
        "8168cff38b861ac162ada05f89bb9f69"
        "86d9fe12d1ae3eb9b1bbb02682826228"
    )
    return {"profiles": report, "stream_sha256": digest}


def scope_audit() -> dict:
    observed = {
        name: sha256(CANDIDATE / name) for name in EXPECTED_HASHES
    }
    assert observed == EXPECTED_HASHES
    ledger = {}
    for line in (CANDIDATE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        ledger[name] = digest
    assert ledger == EXPECTED_HASHES

    proof = (CANDIDATE / "HUMAN-PROOF.md").read_text()
    readme = (CANDIDATE / "README.md").read_text()
    normalized_proof = " ".join(proof.split())
    required_scope_phrases = (
        "not the unrestricted FiveCDC conjecture",
        "It does not prove or disprove FiveCDC",
        "no minimum-projection or graph realization claim",
    )
    assert all(phrase in normalized_proof for phrase in required_scope_phrases)
    assert "OpenAI Codex agents" in normalized_proof
    assert "not received independent human peer review" in normalized_proof
    assert "not a resolution" in readme

    unledgered = sorted(
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and str(path.relative_to(CANDIDATE)) not in {
            "SHA256SUMS", *EXPECTED_HASHES.keys()
        }
    )
    return {
        "candidate_hashes": observed,
        "ledger_matches": True,
        "scope_disclaimers_present": True,
        "ai_disclosure_present": True,
        "unledgered_generated_files": unledgered,
    }


def main() -> None:
    output = {
        "schema": "support16-loop-theorem-blind-audit-v1",
        "marked_words": marked_word_audit(),
        "paired_ports": paired_port_audit(),
        "shape_reduction": shape_reduction_audit(),
        "profiles": profile_audit(),
        "scope": scope_audit(),
        "verdict": {
            "bounded_loop_theorem": "PASS_CONDITIONAL_ON_IMPORTED_RESULTS",
            "publication_gap": (
                "No finite-enumeration gap found.  The theorem statement "
                "still depends on the previously proved loopless theorem "
                "and universal one-circuit tensor theorem; cite/freeze "
                "those dependencies when publishing."
            ),
            "higher_occurrence_no_go": (
                "OUT_OF_SCOPE_FOR_THIS_BLIND_AUDIT except for the local "
                "length-6 triple failure-orbit census"
            ),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
