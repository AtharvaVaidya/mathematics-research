#!/usr/bin/env python3
"""Exact one-colour-pair Kempe matching game on eight support-16 residuals.

For a fixed bichromatic pair {x,y}, each complement component supplies a
perfect matching of its x/y boundary terminals.  Nature chooses one matching
per component.  An observing strategy may switch any subset of the displayed
paths, provided the support-circuit closure equations remain zero.  After the
switch, all componentwise GL(2,2) maps and relative circuit translations are
searched for a clean or deleting extension.

No matching from a second colour pair is used in the same play.
"""

from __future__ import annotations

import functools
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = (
    ROOT.parent
    / "unrestricted-support16-interaction-frontier-20260729"
    / "residuals.tsv"
)
WORD_ROWS = ("01010123", "01012302")
WORD = tuple(map(int, "".join(WORD_ROWS)))
LENGTHS = (8, 8)
OFFSETS = (0, 8)
COLOUR_PAIRS = ((1, 2), (1, 3), (2, 3))
GL = tuple((0,) + row for row in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
RESIDUALS = (
    "0001234000314200",
    "0001234003144422",
    "0012344041300022",
    "0012344044130244",
    "0012344400314200",
    "0012344403144422",
    "0123444441300022",
    "0123444444130244",
)


def derivatives() -> tuple[int, ...]:
    answer = []
    for offset, length in zip(OFFSETS, LENGTHS):
        answer.extend(
            WORD[offset + (local - 1) % length] ^ WORD[offset + local]
            for local in range(length)
        )
    return tuple(answer)


DERIVATIVE = derivatives()
WHICH_CIRCUIT = (0,) * 8 + (1,) * 8


def xor(values) -> int:
    answer = 0
    for value in values:
        answer ^= value
    return answer


@functools.lru_cache(maxsize=None)
def perfect_matchings(items: tuple[int, ...]):
    if not items:
        return ((),)
    first = items[0]
    answer = []
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def integrate(values: tuple[int, ...]):
    base = [0] * 16
    used = []
    for offset, length in zip(OFFSETS, LENGTHS):
        point = 0
        colours = set()
        for local in range(length):
            position = offset + local
            point ^= values[position]
            base[position] = point
            colours.add(point)
        if point:
            return None
        used.append(tuple(sorted(colours)))
    return tuple(base), tuple(used)


def clean(base: tuple[int, ...], owner: tuple[int, ...]) -> tuple[bool, int]:
    blocks = max(owner) + 1
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(blocks)]
        for circuit, (offset, length) in enumerate(zip(OFFSETS, LENGTHS)):
            shift = relative_shift if circuit else 0
            for local in range(length):
                edge = offset + local
                successor = offset + (local + 1) % length
                first = owner[edge]
                second = owner[successor]
                if first == second:
                    continue
                colour = base[edge] ^ shift
                parity[first][colour] ^= 1
                parity[second][colour] ^= 1
        if not any(value for row in parity for value in row):
            return True, relative_shift
    return False, -1


@functools.lru_cache(maxsize=None)
def classify(
    transitions: tuple[int, ...], owner: tuple[int, ...]
) -> tuple[int, int, int, tuple | None]:
    """Return feasible/clean/delete counts and the first exact witness."""

    blocks = max(owner) + 1
    feasible = clean_count = delete_count = 0
    witness = None
    for tail in itertools.product(GL, repeat=blocks - 1):
        maps = (IDENTITY,) + tail
        values = tuple(
            maps[owner[position]][transitions[position]]
            for position in range(16)
        )
        integrated = integrate(values)
        if integrated is None:
            continue
        feasible += 1
        base, used = integrated
        is_clean, relative_shift = clean(base, owner)
        if is_clean:
            clean_count += 1
            if witness is None:
                witness = (
                    "clean",
                    tuple("".join(map(str, row)) for row in maps),
                    "".join(map(str, base[:8]))
                    + "|"
                    + "".join(map(str, base[8:])),
                    relative_shift,
                )
        deleting_circuit = next(
            (
                circuit
                for circuit, colours in enumerate(used)
                if len(colours) < 4
            ),
            None,
        )
        if deleting_circuit is not None:
            delete_count += 1
            if witness is None:
                missing = next(
                    colour
                    for colour in range(4)
                    if colour not in used[deleting_circuit]
                )
                witness = (
                    "delete",
                    deleting_circuit,
                    missing,
                    tuple("".join(map(str, row)) for row in maps),
                    "".join(map(str, base[:8]))
                    + "|"
                    + "".join(map(str, base[8:])),
                )
    return feasible, clean_count, delete_count, witness


def load_source() -> tuple[str, ...]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    assert header[0] == "partition"
    parsed = tuple(line.split("\t")[0] for line in lines[1:] if line)
    assert parsed == RESIDUALS
    return parsed


def terminal_matchings(
    transitions: tuple[int, ...],
    owner: tuple[int, ...],
    colours: tuple[int, int],
):
    blocks = max(owner) + 1
    rows = []
    for block in range(blocks):
        terminals = tuple(
            position
            for position in range(16)
            if owner[position] == block
            and transitions[position] in colours
        )
        assert len(terminals) % 2 == 0
        rows.append((block, terminals, perfect_matchings(terminals)))
    return tuple(rows)


def matching_key(joint_matching) -> str:
    return ";".join(
        f"{block}:"
        + ",".join(f"{first}-{second}" for first, second in matching)
        for block, matching in joint_matching
        if matching
    )


def selected_transition(
    transitions: tuple[int, ...],
    paths: tuple[tuple[int, tuple[int, int]], ...],
    selected_mask: int,
    delta: int,
):
    result = list(transitions)
    closure = [0, 0]
    selected = []
    for index, (block, pair) in enumerate(paths):
        if not (selected_mask >> index) & 1:
            continue
        selected.append((block, pair))
        for endpoint in pair:
            result[endpoint] ^= delta
            closure[WHICH_CIRCUIT[endpoint]] ^= delta
    if closure != [0, 0]:
        return None
    return tuple(result), tuple(selected)


def analyze_pair(
    transitions: tuple[int, ...],
    owner: tuple[int, ...],
    colours: tuple[int, int],
):
    terminal_rows = terminal_matchings(transitions, owner, colours)
    matching_families = tuple(row[2] for row in terminal_rows)
    total_matchings = 1
    for family in matching_families:
        total_matchings *= len(family)

    rows = []
    bad = []
    delta = colours[0] ^ colours[1]
    reachable_states = set()
    for matching_tuple in itertools.product(*matching_families):
        joint = tuple(
            (block, matching)
            for (block, _terminals, _family), matching in zip(
                terminal_rows, matching_tuple
            )
        )
        paths = tuple(
            (block, pair)
            for block, matching in joint
            for pair in matching
        )
        rescue = None
        for selected_mask in range(1, 1 << len(paths)):
            changed = selected_transition(
                transitions, paths, selected_mask, delta
            )
            if changed is None:
                continue
            changed_transitions, selected = changed
            reachable_states.add(changed_transitions)
            result = classify(changed_transitions, owner)
            if result[1] or result[2]:
                rescue = {
                    "selected": [
                        [block, first, second]
                        for block, (first, second) in selected
                    ],
                    "changed": "".join(map(str, changed_transitions)),
                    "feasible": result[0],
                    "clean": result[1],
                    "delete": result[2],
                    "witness": result[3],
                }
                break
        key = matching_key(joint)
        if rescue is None:
            bad.append(key)
        rows.append({"matching": key, "rescue": rescue})

    assert len(rows) == total_matchings
    return {
        "colours": list(colours),
        "terminals": [
            {
                "block": block,
                "positions": list(terminals),
                "matching_count": len(family),
            }
            for block, terminals, family in terminal_rows
        ],
        "joint_matching_count": total_matchings,
        "reachable_transition_count": len(reachable_states),
        "rescued_matching_count": total_matchings - len(bad),
        "bad_matching_count": len(bad),
        "first_bad_matching": bad[0] if bad else None,
        "rows": rows,
    }


def nonobserving_boundary_actions(
    transitions: tuple[int, ...],
    owner: tuple[int, ...],
    colours: tuple[int, int],
):
    """Enumerate matching-independent endpoint sets.

    For a terminal set of size at least four, the only unions of matched
    pairs common to every perfect matching are empty and the full terminal
    set.  The code checks this literally and combines those choices across
    components, retaining only circuit-closed actions.
    """

    terminal_rows = terminal_matchings(transitions, owner, colours)
    common_by_block = []
    for block, terminals, matchings in terminal_rows:
        endpoint_sets = None
        for matching in matchings:
            unions = set()
            for mask in range(1 << len(matching)):
                endpoints = frozenset(
                    endpoint
                    for index, pair in enumerate(matching)
                    if (mask >> index) & 1
                    for endpoint in pair
                )
                unions.add(endpoints)
            endpoint_sets = (
                unions if endpoint_sets is None else endpoint_sets & unions
            )
        assert endpoint_sets is not None
        if len(terminals) >= 4:
            assert endpoint_sets == {
                frozenset(),
                frozenset(terminals),
            }
        common_by_block.append((block, tuple(sorted(endpoint_sets, key=tuple))))

    delta = colours[0] ^ colours[1]
    actions = []
    for chosen in itertools.product(*(row[1] for row in common_by_block)):
        endpoints = frozenset().union(*chosen)
        if not endpoints:
            continue
        closure = [0, 0]
        changed = list(transitions)
        for endpoint in endpoints:
            closure[WHICH_CIRCUIT[endpoint]] ^= delta
            changed[endpoint] ^= delta
        if closure != [0, 0]:
            continue
        result = classify(tuple(changed), owner)
        actions.append(
            {
                "endpoints": sorted(endpoints),
                "clean": result[1],
                "delete": result[2],
            }
        )
    return actions


def analyze_state(partition: str):
    owner = tuple(map(int, partition))
    profile = tuple(sorted(Counter(owner).values(), reverse=True))
    initial = classify(DERIVATIVE, owner)
    assert initial[:3] == (320, 0, 0)
    pair_rows = [
        analyze_pair(DERIVATIVE, owner, colours)
        for colours in COLOUR_PAIRS
    ]
    nonobserving = [
        {
            "colours": list(colours),
            "actions": nonobserving_boundary_actions(
                DERIVATIVE, owner, colours
            ),
        }
        for colours in COLOUR_PAIRS
    ]
    robust_pairs = [
        row["colours"] for row in pair_rows if row["bad_matching_count"] == 0
    ]
    assert not any(
        action["clean"] or action["delete"]
        for row in nonobserving
        for action in row["actions"]
    )
    return {
        "partition": partition,
        "profile": list(profile),
        "initial": {
            "feasible": initial[0],
            "clean": initial[1],
            "delete": initial[2],
        },
        "pair_first_matching_observed_robust_pairs": robust_pairs,
        "pairs": pair_rows,
        "matching_unobserved": nonobserving,
    }


def compact_summary(result):
    return {
        "partition": result["partition"],
        "profile": result["profile"],
        "robust_pairs": result[
            "pair_first_matching_observed_robust_pairs"
        ],
        "pairs": [
            {
                "colours": row["colours"],
                "joint_matchings": row["joint_matching_count"],
                "rescued": row["rescued_matching_count"],
                "bad": row["bad_matching_count"],
                "first_bad": row["first_bad_matching"],
            }
            for row in result["pairs"]
        ],
    }


def main() -> None:
    assert DERIVATIVE == tuple(map(int, "3111113121113132"))
    load_source()

    # Requested order: triple-containing residuals first, then the two
    # 8+2+2+2+2 states, then the remaining two profiles.
    triple_first = (
        RESIDUALS[1],
        RESIDUALS[2],
        RESIDUALS[5],
        RESIDUALS[6],
    )
    eight_next = (RESIDUALS[0], RESIDUALS[7])
    rest = (RESIDUALS[3], RESIDUALS[4])
    order = triple_first + eight_next + rest
    assert set(order) == set(RESIDUALS)

    results = [analyze_state(partition) for partition in order]
    output = {
        "word": "|".join(WORD_ROWS),
        "derivative": "31111131|21113132",
        "quantifiers": {
            "observed": (
                "exists colour pair P; for every independent abstract "
                "perfect matching tuple M for P; exists a nonempty "
                "circuit-closed subset of paths S in M and component maps"
            ),
            "unobserved": (
                "matching-independent endpoint action common to every "
                "perfect matching in each component"
            ),
            "cross_colour_warning": (
                "no play combines matchings belonging to different "
                "bichromatic colour pairs"
            ),
        },
        "results": results,
    }
    certificate = ROOT / "matching-game-certificate.json"
    payload = (json.dumps(output, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    certificate_digest = hashlib.sha256(payload).hexdigest()
    assert certificate_digest == (
        "96a5ff4201c411c278e03ea9941a06656"
        "69575bb07da73aeff59d0cca38c6966"
    )
    certificate.write_bytes(payload)

    summaries = [compact_summary(result) for result in results]
    summary_text = json.dumps(summaries, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(summary_text.encode("ascii")).hexdigest()
    assert digest == (
        "f9cad161398b57531704f05bb7f5e1c"
        "92faf0f5d66c5b217242ee41e38d871ff"
    )
    for summary in summaries:
        print(
            "STATE"
            f" partition={summary['partition']}"
            f" profile={'+'.join(map(str, summary['profile']))}"
            f" robust_pairs={summary['robust_pairs']}"
        )
        for row in summary["pairs"]:
            print(
                " PAIR"
                f" colours={tuple(row['colours'])}"
                f" matchings={row['joint_matchings']}"
                f" rescued={row['rescued']}"
                f" bad={row['bad']}"
                f" first_bad={row['first_bad']}"
            )
    print(f"SUMMARY_SHA256 {digest}")
    print(f"CERTIFICATE_SHA256 {certificate_digest}")
    print("PASS support-16 four-terminal matching game")


if __name__ == "__main__":
    main()
