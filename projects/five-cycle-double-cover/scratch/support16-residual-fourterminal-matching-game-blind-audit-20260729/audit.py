#!/usr/bin/env python3
"""Blind audit of the support-16 four-terminal matching game.

No code from the candidate package is imported.  The eight partitions are
read from the published residual TSV and every abstract matching play and
literal 42-vertex realization is rebuilt independently.
"""

from __future__ import annotations

from collections import Counter
import functools
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = (
    HERE.parent / "support16-residual-fourterminal-matching-game-20260729"
)
FRONTIER = HERE.parent / "unrestricted-support16-interaction-frontier-20260729"
RESIDUAL_TSV = FRONTIER / "residuals.tsv"

WORDS = ("01010123", "01012302")
WORD = tuple(map(int, "".join(WORDS)))
OFFSETS = (0, 8)
LENGTHS = (8, 8)
PAIRS = ((1, 2), (1, 3), (2, 3))
LINEAR = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)

EXPECTED_RESULTS = {
    "0001234000314200": ((15, 14), (15, 14), (3, 2)),
    "0001234003144422": ((3, 2), (9, 9), (1, 0)),
    "0012344041300022": ((3, 2), (15, 15), (1, 0)),
    "0012344044130244": ((3, 2), (9, 9), (3, 2)),
    "0012344400314200": ((3, 2), (9, 9), (3, 2)),
    "0012344403144422": ((3, 2), (15, 15), (1, 0)),
    "0123444441300022": ((3, 2), (9, 9), (1, 0)),
    "0123444444130244": ((15, 14), (15, 14), (3, 2)),
}

SURVIVORS = (
    "0001234000314200",
    "0123444444130244",
)

EXPECTED_ADVERSE_PATHS = {
    SURVIVORS[0]: {
        (1, 2): (
            (0, (1, 7)), (0, (2, 15)), (0, (8, 9)),
            (1, (3, 11)), (2, (4, 13)), (3, (5, 10)),
        ),
        (1, 3): (
            (0, (0, 1)), (0, (2, 7)), (0, (9, 14)),
            (1, (3, 11)), (2, (4, 13)), (3, (5, 10)),
            (4, (6, 12)),
        ),
        (2, 3): (
            (0, (0, 8)), (0, (14, 15)), (4, (6, 12)),
        ),
    },
    SURVIVORS[1]: {
        (1, 2): (
            (1, (1, 10)), (2, (2, 13)), (3, (3, 11)),
            (4, (4, 15)), (4, (5, 7)), (4, (8, 9)),
        ),
        (1, 3): (
            (0, (0, 12)), (1, (1, 10)), (2, (2, 13)),
            (3, (3, 11)), (4, (4, 7)), (4, (5, 6)),
            (4, (9, 14)),
        ),
        (2, 3): (
            (0, (0, 12)), (4, (6, 8)), (4, (14, 15)),
        ),
    },
}

BIG_ATTACHMENTS = {
    SURVIVORS[0]: (2, 1, 0, 7, 8, 9, 14, 15),
    SURVIVORS[1]: (4, 5, 6, 7, 8, 9, 14, 15),
}

BIG_INTERNAL = {
    1: ((2, 4), (6, 7), (8, 9)),
    2: ((0, 6), (1, 3), (2, 8), (5, 9)),
    3: ((0, 3), (1, 9), (4, 8), (5, 7)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xor_all(values) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


def derivative() -> tuple[int, ...]:
    result = []
    for offset, length in zip(OFFSETS, LENGTHS):
        for local in range(length):
            result.append(
                WORD[offset + (local - 1) % length]
                ^ WORD[offset + local]
            )
    return tuple(result)


DERIVATIVE = derivative()
assert DERIVATIVE == tuple(map(int, "3111113121113132"))


def read_published_states() -> tuple[dict, ...]:
    lines = RESIDUAL_TSV.read_text().splitlines()
    header = lines[0].split("\t")
    expected_header = (
        "partition", "profile", "per_circuit_matrix", "interaction_loop",
        "higher_occurrence", "existing_displayed",
    )
    assert tuple(header) == expected_header
    rows = []
    for line in lines[1:]:
        if not line:
            continue
        fields = dict(zip(header, line.split("\t"), strict=True))
        partition = fields["partition"]
        assert len(partition) == 16 and set(partition) <= set("01234")
        owner = tuple(map(int, partition))
        assert all(
            xor_all(
                DERIVATIVE[position]
                for position, value in enumerate(owner)
                if value == block
            ) == 0
            for block in range(5)
        )
        sizes = tuple(sorted(Counter(owner).values(), reverse=True))
        assert "+".join(map(str, sizes)) == fields["profile"]
        matrix = tuple(
            (
                sum(value == block for value in owner[:8]),
                sum(value == block for value in owner[8:]),
            )
            for block in range(5)
        )
        assert ",".join(f"{left}/{right}" for left, right in matrix) == (
            fields["per_circuit_matrix"]
        )
        loop = any(
            left == 2 and right == 0 or left == 0 and right == 2
            for left, right in matrix
        )
        assert int(fields["interaction_loop"]) == int(loop)
        assert int(fields["higher_occurrence"]) == int(max(sizes) >= 3)
        rows.append({
            "partition": partition,
            "profile": list(sizes),
            "per_circuit_matrix": [list(pair) for pair in matrix],
            "existing_displayed": int(fields["existing_displayed"]),
        })
    assert len(rows) == 8
    assert tuple(row["partition"] for row in rows) == tuple(EXPECTED_RESULTS)
    return tuple(rows)


def integrate(transitions: tuple[int, ...], owner: tuple[int, ...]):
    base = [0] * 16
    used = []
    for offset, length in zip(OFFSETS, LENGTHS):
        point = 0
        colours = set()
        for local in range(length):
            position = offset + local
            point ^= transitions[position]
            base[position] = point
            colours.add(point)
        if point:
            return None
        used.append(frozenset(colours))
    return tuple(base), tuple(used)


def literal_clean(
    base: tuple[int, ...], owner: tuple[int, ...],
) -> bool:
    return any(clean_at_relative(base, owner, relative)
               for relative in range(4))


def clean_at_relative(
    base: tuple[int, ...], owner: tuple[int, ...], relative: int,
) -> bool:
    block_count = max(owner) + 1
    parity = [[0] * 4 for _ in range(block_count)]
    for circuit, (offset, length) in enumerate(zip(OFFSETS, LENGTHS)):
        shift = relative if circuit else 0
        for local in range(length):
            position = offset + local
            successor = offset + (local + 1) % length
            first_block = owner[position]
            second_block = owner[successor]
            if first_block != second_block:
                colour = base[position] ^ shift
                parity[first_block][colour] ^= 1
                parity[second_block][colour] ^= 1
    return not any(value for row in parity for value in row)


@functools.lru_cache(maxsize=None)
def classify(
    transitions: tuple[int, ...], owner: tuple[int, ...],
) -> tuple[int, int, int]:
    """Count circuit-integrable, clean, and deleting component maps."""

    block_count = max(owner) + 1
    feasible = clean_count = delete_count = 0
    for tail in itertools.product(LINEAR, repeat=block_count - 1):
        maps = (IDENTITY,) + tail
        mapped = tuple(
            maps[owner[position]][transitions[position]]
            for position in range(16)
        )
        integrated = integrate(mapped, owner)
        if integrated is None:
            continue
        feasible += 1
        base, used = integrated
        clean_count += literal_clean(base, owner)
        delete_count += any(len(colours) < 4 for colours in used)
    return feasible, clean_count, delete_count


@functools.lru_cache(maxsize=None)
def perfect_matchings(items: tuple[int, ...]):
    if not items:
        return ((),)
    first = items[0]
    result = []
    for index in range(1, len(items)):
        second = items[index]
        remainder = items[1:index] + items[index + 1:]
        for tail in perfect_matchings(remainder):
            result.append(((first, second),) + tail)
    return tuple(result)


def component_matching_families(
    owner: tuple[int, ...], colours: tuple[int, int],
):
    rows = []
    for block in range(5):
        terminals = tuple(
            position for position in range(16)
            if owner[position] == block
            and DERIVATIVE[position] in colours
        )
        assert len(terminals) % 2 == 0
        rows.append((block, terminals, perfect_matchings(terminals)))
    return tuple(rows)


def change_by_subset(
    paths: tuple[tuple[int, tuple[int, int]], ...],
    mask: int,
    delta: int,
) -> tuple[int, ...] | None:
    changed = list(DERIVATIVE)
    endpoint_parity = [0, 0]
    for path_index, (_block, endpoints) in enumerate(paths):
        if not ((mask >> path_index) & 1):
            continue
        for endpoint in endpoints:
            changed[endpoint] ^= delta
            endpoint_parity[int(endpoint >= 8)] ^= 1
    if endpoint_parity != [0, 0]:
        return None
    return tuple(changed)


def path_key(paths: tuple[tuple[int, tuple[int, int]], ...]) -> str:
    by_block = {}
    for block, pair in paths:
        by_block.setdefault(block, []).append(pair)
    return ";".join(
        f"{block}:" + ",".join(f"{a}-{b}" for a, b in pairs)
        for block, pairs in sorted(by_block.items())
        if pairs
    )


def analyze_matching_game(states: tuple[dict, ...]) -> dict:
    state_rows = []
    robust_matching_rows = 0
    witness_stream = hashlib.sha256()
    adverse = {}
    nonobserved_rescues = 0

    for state in states:
        partition = state["partition"]
        owner = tuple(map(int, partition))
        assert classify(DERIVATIVE, owner) == (320, 0, 0)
        pair_rows = []
        robust_pairs = []
        for pair_index, colours in enumerate(PAIRS):
            families = component_matching_families(owner, colours)
            family_product = tuple(
                row[2] for row in families
            )
            joint_count = 1
            for family in family_product:
                joint_count *= len(family)
            rescued = 0
            bad_paths = []
            reachable_states = set()
            for matching_tuple in itertools.product(*family_product):
                paths = tuple(
                    (block, pair)
                    for (block, _terminals, _family), matching
                    in zip(families, matching_tuple, strict=True)
                    for pair in matching
                )
                rescue_mask = None
                rescue_counts = None
                for mask in range(1, 1 << len(paths)):
                    changed = change_by_subset(
                        paths, mask, colours[0] ^ colours[1]
                    )
                    if changed is None:
                        continue
                    reachable_states.add(changed)
                    counts = classify(changed, owner)
                    if rescue_mask is None and (counts[1] or counts[2]):
                        rescue_mask = mask
                        rescue_counts = counts
                if rescue_mask is None:
                    bad_paths.append(paths)
                else:
                    rescued += 1
                    witness_stream.update(
                        f"{partition}|{colours}|{path_key(paths)}|"
                        f"{rescue_mask}|{rescue_counts}\n".encode()
                    )
            expected_joint, expected_rescued = EXPECTED_RESULTS[
                partition
            ][pair_index]
            assert (joint_count, rescued) == (
                expected_joint, expected_rescued
            )
            if rescued == joint_count:
                robust_pairs.append(list(colours))
                robust_matching_rows += joint_count
            if partition in SURVIVORS:
                assert len(bad_paths) == 1
                adverse.setdefault(partition, {})[colours] = bad_paths[0]
                assert bad_paths[0] == EXPECTED_ADVERSE_PATHS[
                    partition
                ][colours]
            pair_rows.append({
                "colours": list(colours),
                "joint_matchings": joint_count,
                "rescued": rescued,
                "bad": joint_count - rescued,
                "full_reachable_transition_states": len(reachable_states),
                "terminal_sizes": [
                    len(row[1]) for row in families
                ],
                "component_matching_counts": [
                    len(row[2]) for row in families
                ],
            })

            # Matching-unobserved actions must use endpoint sets that are
            # unions of pairs in every perfect matching for that component.
            common_choices = []
            for _block, terminals, matchings in families:
                common = None
                for matching in matchings:
                    unions = set()
                    for mask in range(1 << len(matching)):
                        unions.add(frozenset(
                            endpoint
                            for index, pair in enumerate(matching)
                            if (mask >> index) & 1
                            for endpoint in pair
                        ))
                    common = unions if common is None else common & unions
                assert common == {
                    frozenset(), frozenset(terminals)
                }
                common_choices.append(tuple(common))
            delta = colours[0] ^ colours[1]
            for choices in itertools.product(*common_choices):
                endpoints = frozenset().union(*choices)
                if not endpoints:
                    continue
                parity = [
                    sum((endpoint >= 8) == bool(circuit)
                        for endpoint in endpoints) % 2
                    for circuit in range(2)
                ]
                if parity != [0, 0]:
                    continue
                changed = tuple(
                    value ^ delta if position in endpoints else value
                    for position, value in enumerate(DERIVATIVE)
                )
                counts = classify(changed, owner)
                nonobserved_rescues += bool(counts[1] or counts[2])
        state_rows.append({
            **state,
            "robust_pairs": robust_pairs,
            "pairs": pair_rows,
        })

    assert robust_matching_rows == 66
    assert nonobserved_rescues == 0
    assert all(
        row["robust_pairs"] == (
            [] if row["partition"] in SURVIVORS else [[1, 3]]
        )
        for row in state_rows
    )

    adverse_rows = []
    for partition in SURVIVORS:
        owner = tuple(map(int, partition))
        triple = adverse[partition]
        path_counts = []
        legal_subset_counts = []
        for colours in PAIRS:
            paths = triple[colours]
            legal = 0
            for mask in range(1, 1 << len(paths)):
                changed = change_by_subset(
                    paths, mask, colours[0] ^ colours[1]
                )
                if changed is None:
                    continue
                legal += 1
                assert classify(changed, owner) == (320, 0, 0)
            path_counts.append(len(paths))
            legal_subset_counts.append(legal)
        assert path_counts == [6, 7, 3]
        assert legal_subset_counts == [31, 63, 3]
        adverse_rows.append({
            "partition": partition,
            "path_counts_12_13_23": path_counts,
            "legal_nonempty_subsets_12_13_23": legal_subset_counts,
            "all_changed_states": "feasible=320 clean=0 delete=0",
        })

    return {
        "quantifiers": (
            "exists one colour pair P; for every componentwise abstract "
            "perfect-matching tuple M for P; after observing M, exists a "
            "nonempty circuit-closed subset S(M), then component maps and "
            "relative circuit translation"
        ),
        "cross_colour_mixing": False,
        "states": state_rows,
        "robust_states": sum(bool(row["robust_pairs"]) for row in state_rows),
        "robust_matching_rows": robust_matching_rows,
        "matching_unobserved_rescues": nonobserved_rescues,
        "adverse_triples": adverse_rows,
        "positive_witness_stream_sha256": witness_stream.hexdigest(),
    }


def parse_path_key(encoded: str) -> tuple[tuple[int, tuple[int, int]], ...]:
    paths = []
    if not encoded:
        return ()
    for block_row in encoded.split(";"):
        block_text, pairs_text = block_row.split(":", 1)
        block = int(block_text)
        for pair_text in pairs_text.split(","):
            first, second = map(int, pair_text.split("-"))
            assert first < second
            paths.append((block, (first, second)))
    return tuple(paths)


def rendered_base(base: tuple[int, ...]) -> str:
    return (
        "".join(map(str, base[:8]))
        + "|"
        + "".join(map(str, base[8:]))
    )


def validate_stored_witness(
    rescue: dict, changed: tuple[int, ...], owner: tuple[int, ...],
) -> None:
    counts = classify(changed, owner)
    assert (
        rescue["feasible"], rescue["clean"], rescue["delete"]
    ) == counts
    witness = rescue["witness"]
    kind = witness[0]
    if kind == "clean":
        _, raw_maps, raw_base, relative = witness
    elif kind == "delete":
        _, circuit, missing, raw_maps, raw_base = witness
    else:
        raise AssertionError(f"unknown witness kind {kind!r}")
    maps = tuple(tuple(map(int, row)) for row in raw_maps)
    assert len(maps) == max(owner) + 1
    assert maps[0] == IDENTITY
    assert all(mapping in LINEAR for mapping in maps)
    mapped = tuple(
        maps[owner[position]][changed[position]]
        for position in range(16)
    )
    integrated = integrate(mapped, owner)
    assert integrated is not None
    base, _used = integrated
    assert rendered_base(base) == raw_base
    if kind == "clean":
        assert relative in range(4)
        assert clean_at_relative(base, owner, relative)
    else:
        assert circuit in (0, 1) and missing in range(4)
        offset, length = OFFSETS[circuit], LENGTHS[circuit]
        assert missing not in base[offset:offset + length]


def certificate_audit(states: tuple[dict, ...]) -> dict:
    """Replay every stored row and witness without candidate imports."""

    certificate = json.loads(
        (CANDIDATE / "matching-game-certificate.json").read_text()
    )
    assert certificate["word"] == "01010123|01012302"
    assert certificate["derivative"] == "31111131|21113132"
    assert "for every independent abstract perfect matching" in (
        certificate["quantifiers"]["observed"]
    )
    assert "no play combines matchings" in (
        certificate["quantifiers"]["cross_colour_warning"]
    )
    by_partition = {
        row["partition"]: row for row in certificate["results"]
    }
    assert set(by_partition) == set(EXPECTED_RESULTS)

    row_count = rescue_count = bad_count = unobserved_count = 0
    for state in states:
        partition = state["partition"]
        owner = tuple(map(int, partition))
        stored = by_partition[partition]
        assert stored["profile"] == state["profile"]
        assert stored["initial"] == {
            "feasible": 320, "clean": 0, "delete": 0,
        }
        stored_pairs = {
            tuple(row["colours"]): row for row in stored["pairs"]
        }
        assert set(stored_pairs) == set(PAIRS)
        robust = []

        for pair_index, colours in enumerate(PAIRS):
            pair = stored_pairs[colours]
            families = component_matching_families(owner, colours)
            expected_terminals = [
                {
                    "block": block,
                    "positions": list(terminals),
                    "matching_count": len(matchings),
                }
                for block, terminals, matchings in families
            ]
            assert pair["terminals"] == expected_terminals
            matching_tuples = tuple(itertools.product(
                *(row[2] for row in families)
            ))
            paths_by_key = {}
            for matching_tuple in matching_tuples:
                paths = tuple(
                    (block, endpoint_pair)
                    for (block, _terminals, _matchings), matching
                    in zip(families, matching_tuple, strict=True)
                    for endpoint_pair in matching
                )
                paths_by_key[path_key(paths)] = paths
            assert len(paths_by_key) == len(matching_tuples)
            stored_rows = pair["rows"]
            assert [row["matching"] for row in stored_rows] == list(
                paths_by_key
            )

            # This certificate field records the distinct transitions
            # inspected by the deterministic search prefix.  On a rescued
            # matching, the producer stops at its first successful mask.
            # It is not the cardinality of the full reachable state set.
            searched_transitions = set()
            first_bad = None
            rescued = 0
            for row in stored_rows:
                paths = paths_by_key[row["matching"]]
                any_rescue = False
                for mask in range(1, 1 << len(paths)):
                    changed = change_by_subset(
                        paths, mask, colours[0] ^ colours[1]
                    )
                    if changed is None:
                        continue
                    searched_transitions.add(changed)
                    counts = classify(changed, owner)
                    if counts[1] or counts[2]:
                        any_rescue = True
                        break
                rescue = row["rescue"]
                assert (rescue is not None) == any_rescue
                if rescue is None:
                    bad_count += 1
                    if first_bad is None:
                        first_bad = row["matching"]
                    continue
                rescue_count += 1
                rescued += 1
                selected = tuple(
                    (block, (first, second))
                    for block, first, second in rescue["selected"]
                )
                assert selected and len(set(selected)) == len(selected)
                assert all(path in paths for path in selected)
                mask = sum(
                    1 << index for index, path in enumerate(paths)
                    if path in selected
                )
                changed = change_by_subset(
                    paths, mask, colours[0] ^ colours[1]
                )
                assert changed is not None
                assert "".join(map(str, changed)) == rescue["changed"]
                validate_stored_witness(rescue, changed, owner)

            expected_joint, expected_rescued = EXPECTED_RESULTS[
                partition
            ][pair_index]
            assert pair["joint_matching_count"] == expected_joint
            assert pair["rescued_matching_count"] == expected_rescued
            assert pair["bad_matching_count"] == (
                expected_joint - expected_rescued
            )
            assert rescued == expected_rescued
            assert pair["first_bad_matching"] == first_bad
            assert pair["reachable_transition_count"] == len(
                searched_transitions
            )
            row_count += expected_joint
            if expected_joint == expected_rescued:
                robust.append(list(colours))

        assert stored["pair_first_matching_observed_robust_pairs"] == robust

        unobserved_by_pair = {
            tuple(row["colours"]): row["actions"]
            for row in stored["matching_unobserved"]
        }
        assert set(unobserved_by_pair) == set(PAIRS)
        for colours in PAIRS:
            families = component_matching_families(owner, colours)
            choices_by_block = []
            for _block, terminals, matchings in families:
                common = None
                for matching in matchings:
                    unions = {
                        frozenset(
                            endpoint
                            for index, endpoint_pair
                            in enumerate(matching)
                            if (mask >> index) & 1
                            for endpoint in endpoint_pair
                        )
                        for mask in range(1 << len(matching))
                    }
                    common = unions if common is None else common & unions
                assert common == {
                    frozenset(), frozenset(terminals)
                }
                choices_by_block.append(common)
            expected_actions = set()
            for choices in itertools.product(*choices_by_block):
                endpoints = frozenset().union(*choices)
                if not endpoints:
                    continue
                if any(
                    sum(
                        (endpoint >= 8) == bool(circuit)
                        for endpoint in endpoints
                    ) % 2
                    for circuit in range(2)
                ):
                    continue
                changed = tuple(
                    value ^ (colours[0] ^ colours[1])
                    if position in endpoints else value
                    for position, value in enumerate(DERIVATIVE)
                )
                feasible, clean, delete = classify(changed, owner)
                assert feasible
                expected_actions.add((
                    tuple(sorted(endpoints)), clean, delete,
                ))
            observed_actions = {
                (
                    tuple(row["endpoints"]),
                    row["clean"],
                    row["delete"],
                )
                for row in unobserved_by_pair[colours]
            }
            assert observed_actions == expected_actions
            unobserved_count += len(expected_actions)

    assert row_count == 160
    assert rescue_count == 142
    assert bad_count == 18
    return {
        "stored_matching_rows_replayed": row_count,
        "stored_rescue_witnesses_replayed": rescue_count,
        "stored_bad_rows_replayed": bad_count,
        "stored_matching_unobserved_actions_replayed": unobserved_count,
        "all_stored_map_base_and_relative_witnesses_valid": True,
    }


def add_edge(
    edges: list[tuple[int, int, int, bool]],
    first: int, second: int, low: int, support: bool,
) -> None:
    assert first != second and low in range(4)
    edges.append((min(first, second), max(first, second), low, support))


def build_realization(partition: str):
    owner = tuple(map(int, partition))
    big = next(
        block for block, count in Counter(owner).items() if count == 8
    )
    edges: list[tuple[int, int, int, bool]] = []

    # Two support 8-cycles.
    for offset in OFFSETS:
        for local in range(8):
            add_edge(
                edges,
                offset + local,
                offset + (local + 1) % 8,
                WORD[offset + local],
                True,
            )

    block_vertices: dict[int, frozenset[int]] = {}
    next_vertex = 16
    for block in range(5):
        if block == big:
            continue
        occurrences = tuple(
            position for position, value in enumerate(owner)
            if value == block
        )
        assert len(occurrences) == 2
        terminal_colour = DERIVATIVE[occurrences[0]]
        assert DERIVATIVE[occurrences[1]] == terminal_colour
        vertices = tuple(range(next_vertex, next_vertex + 4))
        next_vertex += 4
        block_vertices[block] = frozenset(vertices)
        add_edge(edges, occurrences[0], vertices[0],
                 terminal_colour, False)
        add_edge(edges, occurrences[1], vertices[1],
                 terminal_colour, False)
        other = tuple(value for value in (1, 2, 3)
                      if value != terminal_colour)
        # A properly low-coloured K4 minus the pole edge 0--1.
        add_edge(edges, vertices[2], vertices[3],
                 terminal_colour, False)
        add_edge(edges, vertices[0], vertices[2], other[0], False)
        add_edge(edges, vertices[1], vertices[3], other[0], False)
        add_edge(edges, vertices[0], vertices[3], other[1], False)
        add_edge(edges, vertices[1], vertices[2], other[1], False)

    big_vertices = tuple(range(next_vertex, next_vertex + 10))
    next_vertex += 10
    assert next_vertex == 42
    block_vertices[big] = frozenset(big_vertices)
    attachments = BIG_ATTACHMENTS[partition]
    assert set(attachments) == {
        position for position, value in enumerate(owner) if value == big
    }
    assert tuple(DERIVATIVE[position] for position in attachments) == (
        1, 1, 3, 1, 2, 1, 3, 2,
    )
    for local, occurrence in enumerate(attachments):
        add_edge(
            edges, occurrence, big_vertices[local],
            DERIVATIVE[occurrence], False,
        )
    for low, matching in BIG_INTERNAL.items():
        for first, second in matching:
            add_edge(
                edges, big_vertices[first], big_vertices[second],
                low, False,
            )
    return 42, tuple(edges), block_vertices


def adjacency(
    vertex_count: int,
    edges: tuple[tuple[int, int, int, bool], ...],
    selected=None,
):
    result = [[] for _ in range(vertex_count)]
    for index, edge in enumerate(edges):
        first, second, low, support = edge
        if selected is not None and not selected(index, edge):
            continue
        result[first].append((second, index))
        result[second].append((first, index))
    return result


def connected_without(
    vertex_count: int,
    edges: tuple[tuple[int, int, int, bool], ...],
    omitted: int | None,
) -> bool:
    graph = adjacency(
        vertex_count, edges,
        lambda index, _edge: index != omitted,
    )
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour, _edge in graph[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == vertex_count


def realized_pairs(
    vertex_count: int,
    edges: tuple[tuple[int, int, int, bool], ...],
    block_vertices: dict[int, frozenset[int]],
    owner: tuple[int, ...],
    block: int,
    colours: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    terminals = {
        position for position, value in enumerate(owner)
        if value == block and DERIVATIVE[position] in colours
    }
    allowed_vertices = set(block_vertices[block]) | terminals
    graph = adjacency(
        vertex_count,
        edges,
        lambda _index, edge: not edge[3] and edge[2] in colours,
    )
    unseen_terminals = set(terminals)
    pairs = []
    while unseen_terminals:
        root = min(unseen_terminals)
        seen = {root}
        stack = [root]
        endpoints = set()
        while stack:
            vertex = stack.pop()
            if vertex in terminals:
                endpoints.add(vertex)
            for neighbour, _edge in graph[vertex]:
                if (
                    neighbour in allowed_vertices
                    and neighbour not in seen
                ):
                    seen.add(neighbour)
                    stack.append(neighbour)
        assert len(endpoints) == 2
        pair = tuple(sorted(endpoints))
        pairs.append(pair)
        unseen_terminals -= endpoints
    return tuple(sorted(pairs))


def tait_colouring(
    vertex_count: int,
    edges: tuple[tuple[int, int, int, bool], ...],
) -> tuple[int, ...]:
    colours = [0] * len(edges)
    used = [set() for _ in range(vertex_count)]

    def search(assigned: int) -> bool:
        if assigned == len(edges):
            return True
        best_edge = -1
        best_domain = None
        for edge, (left, right, _low, _support) in enumerate(edges):
            if colours[edge]:
                continue
            domain = tuple(
                colour for colour in (1, 2, 3)
                if colour not in used[left] and colour not in used[right]
            )
            if not domain:
                return False
            if best_domain is None or len(domain) < len(best_domain):
                best_edge, best_domain = edge, domain
        left, right, _low, _support = edges[best_edge]
        for colour in best_domain:
            colours[best_edge] = colour
            used[left].add(colour)
            used[right].add(colour)
            if search(assigned + 1):
                return True
            used[left].remove(colour)
            used[right].remove(colour)
            colours[best_edge] = 0
        return False

    assert search(0)
    result = tuple(colours)
    graph = adjacency(vertex_count, edges)
    assert all(
        {result[edge] for _neighbour, edge in row} == {1, 2, 3}
        for row in graph
    )
    return result


def graph6(
    vertex_count: int,
    edges: tuple[tuple[int, int, int, bool], ...],
) -> str:
    pairs = {(left, right) for left, right, _low, _support in edges}
    bits = [
        int((first, second) in pairs)
        for second in range(1, vertex_count)
        for first in range(second)
    ]
    bits.extend([0] * (-len(bits) % 6))
    return chr(63 + vertex_count) + "".join(
        chr(63 + sum(
            bits[offset + bit] << (5 - bit) for bit in range(6)
        ))
        for offset in range(0, len(bits), 6)
    )


def realization_audit() -> dict:
    rows = []
    for partition in SURVIVORS:
        owner = tuple(map(int, partition))
        vertex_count, edges, block_vertices = build_realization(partition)
        assert len(edges) == 63
        assert len({
            (left, right) for left, right, _low, _support in edges
        }) == 63
        graph = adjacency(vertex_count, edges)
        assert all(len(row) == 3 for row in graph)
        assert connected_without(vertex_count, edges, None)
        assert all(
            connected_without(vertex_count, edges, edge)
            for edge in range(len(edges))
        )

        # Literal nowhere-zero F_2^3 flow: high bit is the support
        # coordinate and the two low bits are the written low colour.
        full_values = tuple(
            low | (4 if support else 0)
            for _left, _right, low, support in edges
        )
        assert all(full_values)
        for vertex, incident in enumerate(graph):
            assert xor_all(full_values[edge]
                           for _neighbour, edge in incident) == 0, vertex

        path_rows = {}
        for colours in PAIRS:
            paths = []
            for block in range(5):
                paths.extend(
                    (block, pair)
                    for pair in realized_pairs(
                        vertex_count, edges, block_vertices,
                        owner, block, colours,
                    )
                )
            path_tuple = tuple(paths)
            assert path_tuple == EXPECTED_ADVERSE_PATHS[
                partition
            ][colours]
            legal = 0
            for mask in range(1, 1 << len(path_tuple)):
                changed = change_by_subset(
                    path_tuple, mask, colours[0] ^ colours[1]
                )
                if changed is None:
                    continue
                legal += 1
                assert classify(changed, owner) == (320, 0, 0)
            assert legal == {6: 31, 7: 63, 3: 3}[len(path_tuple)]
            path_rows["".join(map(str, colours))] = [
                [block, first, second]
                for block, (first, second) in path_tuple
            ]

        tait = tait_colouring(vertex_count, edges)
        encoded = graph6(vertex_count, edges)
        rows.append({
            "partition": partition,
            "vertices": vertex_count,
            "edges": len(edges),
            "simple": True,
            "cubic": True,
            "connected": True,
            "bridgeless": True,
            "flow": True,
            "path_systems": path_rows,
            "all_97_legal_subsets_fail": True,
            "tait_colouring": "".join(map(str, tait)),
            "labelled_graph6": encoded,
            "minimum_projection_size": 0,
        })
    return {"realizations": rows}


def scope_audit() -> dict:
    ledger = {}
    for line in (CANDIDATE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        ledger[name] = digest
    observed = {name: sha256(CANDIDATE / name) for name in ledger}
    assert observed == ledger
    human = " ".join((CANDIDATE / "HUMAN-PROOF.md").read_text().split())
    readme = " ".join((CANDIDATE / "README.md").read_text().split())
    assert "not globally minimum" in human
    assert "not FiveCDC counterexamples" in human
    assert "does not resolve FiveCDC" in readme
    assert "OpenAI Codex" in human
    assert "not received independent human peer review" in human
    unledgered = sorted(
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.rglob("*")
        if path.is_file()
        and path.name != "SHA256SUMS"
        and str(path.relative_to(CANDIDATE)) not in ledger
    )
    assert not unledgered
    return {
        "candidate_hashes": observed,
        "candidate_ledger_sha256": sha256(CANDIDATE / "SHA256SUMS"),
        "published_residual_tsv_sha256": sha256(RESIDUAL_TSV),
        "ledger_matches": True,
        "scope_disclaimers_present": True,
        "ai_disclosure_present": True,
        "unledgered_files": unledgered,
    }


def main() -> None:
    states = read_published_states()
    output = {
        "schema":
            "support16-fourterminal-matching-game-blind-audit-v1",
        "fixed_word": "|".join(WORDS),
        "fixed_derivative": "31111131|21113132",
        "source_states": list(states),
        "game": analyze_matching_game(states),
        "stored_certificate": certificate_audit(states),
        "graphs": realization_audit(),
        "scope": scope_audit(),
        "verdict": {
            "eight_state_one_round_game": "PASS",
            "six_matching_robust_reductions": "PASS",
            "two_simultaneously_realized_adverse_triples": "PASS",
            "fivecdc": "NOT_RESOLVED",
            "minimum_projection_obstruction": (
                "NO: both realized graphs are Tait-colourable and have "
                "minimum projection size zero"
            ),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
