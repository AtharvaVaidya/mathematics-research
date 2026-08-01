#!/usr/bin/env python3
"""Independent audit of every frozen 7+7 size-fourteen failure.

This program does not import the primary enumerator or either earlier Kempe
certificate checker.  It reconstructs the boundary semantics from the two
seven-circuit word and component partition, verifies that every listed row is
an actual clean-or-delete failure, and then proves a graph-independent Kempe
escape.

For a chosen component and two nonzero colours, an unknown cubic realization
pairs the selected boundary occurrences by Kempe paths.  We enumerate every
perfect matching of those occurrences.  A strategy is accepted only if every
matching contains a path whose switch has a checked clean-or-delete
certificate.  Cross-circuit switches may be compensated by a forced path in a
different component having exactly two selected occurrences, one on each
circuit.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path


LOOPS = (tuple(range(7)), tuple(range(7, 14)))
NONZERO = (1, 2, 3)
PAIRS = ((1, 2), (1, 3), (2, 3))
LINEAR_MAPS = tuple((0,) + p for p in itertools.permutations(NONZERO))
IDENTITY = (0, 1, 2, 3)

EXPECTED_INPUT_SHA256 = (
    "034deebf6d94bbb08a114165d28190fe6e97d4d42401eab8c25f45e46bb43ead"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "5c08f4a410a55c3460cb8742567a9da8613cf44faaf84d5b3a4df107a5c6724b"
)
EXPECTED_FOOTER = {
    "shape": "7+7",
    "canonical_words": 333,
    "charge_valid": 91_481_505,
    "dirty": 80_104_020,
    "direct_clean": 80_066_557,
    "delete_branch": 37_239,
    "dichotomy_failures": 224,
}

ROW_RE = re.compile(
    r"COUNTERSTATE word=([0-3]{7})\|([0-3]{7}) partition=([0-9]{14})"
)
FOOTER_RE = re.compile(
    r"RESULT shape=(\S+) canonical_words=(\d+) charge_valid=(\d+) "
    r"dirty=(\d+) direct_clean=(\d+) delete_branch=(\d+) "
    r"dichotomy_failures=(\d+)"
)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def boundary_derivative(word):
    derivative = [0] * 14
    for loop in LOOPS:
        for j, position in enumerate(loop):
            derivative[position] = word[loop[j - 1]] ^ word[position]
    return tuple(derivative)


def partition_blocks(partition):
    return tuple(
        tuple(i for i, component in enumerate(partition) if component == label)
        for label in range(max(partition) + 1)
    )


def restricted_growth(partition):
    if partition[0] != 0:
        return False
    largest = 0
    for label in partition[1:]:
        if label > largest + 1:
            return False
        largest = max(largest, label)
    return True


def dirty_boundary(word, partition):
    parity = [[0] * 4 for _ in partition_blocks(partition)]
    for loop in LOOPS:
        for j, left in enumerate(loop):
            right = loop[(j + 1) % len(loop)]
            a, b = partition[left], partition[right]
            if a != b:
                parity[a][word[left]] ^= 1
                parity[b][word[left]] ^= 1
    return any(parity[component][0] for component in range(len(parity)))


def integrate(transitions):
    base = [0] * 14
    for loop in LOOPS:
        running = 0
        for position in loop:
            running ^= transitions[position]
            base[position] = running
        if running:
            return None
    return tuple(base)


def cleaning_shift(base, partition):
    component_count = max(partition) + 1
    for relative_shift in range(4):
        parity = [[0] * 4 for _ in range(component_count)]
        for loop_number, loop in enumerate(LOOPS):
            shift = relative_shift if loop_number == 1 else 0
            for j, left in enumerate(loop):
                right = loop[(j + 1) % len(loop)]
                a, b = partition[left], partition[right]
                if a != b:
                    colour = base[left] ^ shift
                    parity[a][colour] ^= 1
                    parity[b][colour] ^= 1
        if not any(cell for row in parity for cell in row):
            return relative_shift
    return None


def deletion_witness(base):
    for loop_number, loop in enumerate(LOOPS):
        used = {base[position] for position in loop}
        for colour in range(4):
            if colour not in used:
                return loop_number, colour
    return None


def map_assignments(component_count):
    # Common postcomposition by a linear automorphism lets us normalize the
    # first component map to the identity without losing a clean/delete orbit.
    for tail in itertools.product(LINEAR_MAPS, repeat=component_count - 1):
        yield (IDENTITY,) + tail


def find_clean_or_delete(transitions, partition):
    component_count = max(partition) + 1
    first_clean = None
    for maps in map_assignments(component_count):
        changed = tuple(
            maps[partition[position]][transitions[position]]
            for position in range(14)
        )
        base = integrate(changed)
        if base is None:
            continue
        deletion = deletion_witness(base)
        if deletion is not None:
            return {
                "kind": "delete",
                "maps": ["".join(map(str, linear)) for linear in maps],
                "base": "".join(map(str, base[:7]))
                + "|"
                + "".join(map(str, base[7:])),
                "loop": deletion[0],
                "missing": deletion[1],
            }
        shift = cleaning_shift(base, partition)
        if shift is not None and first_clean is None:
            first_clean = {
                "kind": "clean",
                "maps": ["".join(map(str, linear)) for linear in maps],
                "base": "".join(map(str, base[:7]))
                + "|"
                + "".join(map(str, base[7:])),
                "relative_shift": shift,
            }
    return first_clean


def classify_failure(transitions, partition):
    component_count = max(partition) + 1
    feasible = clean = deletable = 0
    for maps in map_assignments(component_count):
        changed = tuple(
            maps[partition[position]][transitions[position]]
            for position in range(14)
        )
        base = integrate(changed)
        if base is None:
            continue
        feasible += 1
        if deletion_witness(base) is not None:
            deletable += 1
        if cleaning_shift(base, partition) is not None:
            clean += 1
    return feasible, clean, deletable


def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for j in range(1, len(items)):
        pair = (first, items[j])
        rest = items[1:j] + items[j + 1 :]
        for suffix in perfect_matchings(rest):
            yield (pair,) + suffix


def different_loops(a, b):
    return (a < 7) != (b < 7)


def perturb(transitions, primary, auxiliary, delta):
    changed = list(transitions)
    for endpoint in primary + auxiliary:
        changed[endpoint] ^= delta
    changed = tuple(changed)
    assert all(xor_all(changed[position] for position in loop) == 0 for loop in LOOPS)
    return changed


def pair_certificate(
    transitions, partition, blocks, active_component, colours, endpoints
):
    delta = colours[0] ^ colours[1]
    if not different_loops(*endpoints):
        auxiliary_options = ((),)
    else:
        auxiliary_options = []
        for component, block in enumerate(blocks):
            if component == active_component:
                continue
            selected = tuple(
                position
                for position in block
                if transitions[position] in colours
            )
            if len(selected) == 2 and different_loops(*selected):
                auxiliary_options.append(selected)

    for auxiliary in auxiliary_options:
        witness = find_clean_or_delete(
            perturb(transitions, endpoints, auxiliary, delta), partition
        )
        if witness is not None:
            witness["primary"] = list(endpoints)
            witness["auxiliary"] = list(auxiliary)
            witness["delta"] = delta
            return witness
    return None


def robust_strategy(transitions, partition):
    blocks = partition_blocks(partition)
    candidates = []
    for component, block in enumerate(blocks):
        for colours in PAIRS:
            selected = tuple(
                position
                for position in block
                if transitions[position] in colours
            )
            if len(selected) < 4 or len(selected) % 2:
                continue

            witnesses = {}
            for endpoints in itertools.combinations(selected, 2):
                witness = pair_certificate(
                    transitions,
                    partition,
                    blocks,
                    component,
                    colours,
                    endpoints,
                )
                if witness is not None:
                    witnesses[endpoints] = witness

            matchings = tuple(perfect_matchings(selected))
            if all(any(pair in witnesses for pair in matching) for matching in matchings):
                candidates.append(
                    {
                        "component": component,
                        "component_size": len(block),
                        "colours": list(colours),
                        "selected": list(selected),
                        "matching_count": len(matchings),
                        "good_pairs": [
                            {
                                "endpoints": list(pair),
                                "witness": witnesses[pair],
                            }
                            for pair in sorted(witnesses)
                        ],
                    }
                )
    if not candidates:
        return None
    # A deterministic choice makes the aggregate certificate hash stable.
    candidates.sort(
        key=lambda row: (
            row["component"],
            row["colours"],
            row["selected"],
            len(row["good_pairs"]),
        )
    )
    return candidates[0]


def read_census(path):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_INPUT_SHA256:
        raise AssertionError(
            f"unexpected census sha256 {digest}; expected {EXPECTED_INPUT_SHA256}"
        )

    states = []
    footer = None
    for line in raw.decode("utf-8").splitlines():
        row = ROW_RE.fullmatch(line)
        if row:
            states.append((row.group(1) + row.group(2), row.group(3)))
        result = FOOTER_RE.fullmatch(line)
        if result:
            values = result.groups()
            footer = {
                "shape": values[0],
                "canonical_words": int(values[1]),
                "charge_valid": int(values[2]),
                "dirty": int(values[3]),
                "direct_clean": int(values[4]),
                "delete_branch": int(values[5]),
                "dichotomy_failures": int(values[6]),
            }
    assert footer == EXPECTED_FOOTER, footer
    assert len(states) == EXPECTED_FOOTER["dichotomy_failures"]
    assert len(set(states)) == len(states)
    return states


def validate_row(word_text, partition_text):
    word = tuple(map(int, word_text))
    partition = tuple(map(int, partition_text))
    assert restricted_growth(partition)
    assert max(partition) == 4
    assert all(
        word[loop[j - 1]] != word[position]
        for loop in LOOPS
        for j, position in enumerate(loop)
    )
    assert all({word[position] for position in loop} == {0, 1, 2, 3} for loop in LOOPS)

    transitions = boundary_derivative(word)
    assert all(value in NONZERO for value in transitions)
    blocks = partition_blocks(partition)
    assert all(xor_all(transitions[position] for position in block) == 0 for block in blocks)
    assert dirty_boundary(word, partition)

    profile = tuple(sorted((len(block) for block in blocks), reverse=True))
    assert profile in ((6, 2, 2, 2, 2), (4, 4, 2, 2, 2))
    feasible, clean, deletable = classify_failure(transitions, partition)
    assert feasible > 0
    assert clean == 0
    assert deletable == 0
    return partition, transitions, profile, feasible


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "census",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("census-7+7.txt"),
    )
    parser.add_argument(
        "--certificate-json",
        type=Path,
        help="optionally write the full independently reconstructed certificate",
    )
    args = parser.parse_args()

    states = read_census(args.census)
    profile_counts = {}
    feasible_histogram = {}
    certificates = []
    witness_kinds = {"clean": 0, "delete": 0}
    compensation_counts = {0: 0, 2: 0}
    matching_obligations = 0

    for index, (word_text, partition_text) in enumerate(states):
        partition, transitions, profile, feasible = validate_row(
            word_text, partition_text
        )
        profile_counts[profile] = profile_counts.get(profile, 0) + 1
        feasible_histogram[feasible] = feasible_histogram.get(feasible, 0) + 1

        strategy = robust_strategy(transitions, partition)
        assert strategy is not None, (word_text, partition_text)
        matching_obligations += strategy["matching_count"]
        for pair in strategy["good_pairs"]:
            witness_kinds[pair["witness"]["kind"]] += 1
            compensation_counts[len(pair["witness"]["auxiliary"])] += 1
        certificates.append(
            {
                "index": index,
                "word": word_text[:7] + "|" + word_text[7:],
                "partition": partition_text[:7] + "|" + partition_text[7:],
                "profile": list(profile),
                "feasible_normalized_maps": feasible,
                "strategy": strategy,
            }
        )

    canonical = json.dumps(
        certificates, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    certificate_sha = hashlib.sha256(canonical).hexdigest()
    assert profile_counts == {
        (6, 2, 2, 2, 2): 46,
        (4, 4, 2, 2, 2): 178,
    }
    assert feasible_histogram == {320: 224}
    assert witness_kinds == {"clean": 0, "delete": 1_566}
    assert compensation_counts == {0: 750, 2: 816}
    assert matching_obligations == 984
    assert certificate_sha == EXPECTED_CERTIFICATE_SHA256
    frozen_certificates = json.loads(
        Path(__file__).with_name("certificates.json").read_text(encoding="utf-8")
    )
    assert frozen_certificates == certificates
    if args.certificate_json:
        args.certificate_json.write_text(
            json.dumps(certificates, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(f"input_sha256={EXPECTED_INPUT_SHA256}")
    print(f"states={len(states)}")
    print(
        "profiles="
        + ",".join(
            f"{'+'.join(map(str, profile))}:{count}"
            for profile, count in sorted(profile_counts.items())
        )
    )
    print(
        "feasible_normalized_map_histogram="
        + ",".join(
            f"{feasible}:{count}"
            for feasible, count in sorted(feasible_histogram.items())
        )
    )
    print(
        "selected_good_pair_witnesses="
        + ",".join(f"{kind}:{count}" for kind, count in witness_kinds.items())
    )
    print(
        "selected_good_pair_compensation="
        + ",".join(
            f"{endpoints}-endpoint:{count}"
            for endpoints, count in compensation_counts.items()
        )
    )
    print(f"perfect_matching_obligations={matching_obligations}")
    print(f"certificate_sha256={certificate_sha}")
    print(
        "PASS: all 224 listed 7+7 failures have a perfect-matching-robust "
        "two-colour Kempe clean-or-delete escape"
    )


if __name__ == "__main__":
    main()
