#!/usr/bin/env python3
"""Independent audit of the proposed size-14 -> size-15 smoothing induction.

The checker has no imports from the primary size-14 or size-15 programs.
It does three things:

* canonicalizes two-circuit boundary states under affine colour changes,
  independent dihedral circuit actions, equal-length circuit interchange,
  and complement-component renaming;
* checks whether each supplied size-15 residual has a removable same-block
  smoothing equivalent to one of the frozen 224 size-14 residual rows;
* independently replays the displayed split-block smoothing obstruction.

The input residual files are text files containing lines

    COUNTERSTATE word=... partition=...

All other lines are ignored.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRATCH = HERE.parent
SIZE14 = (
    SCRATCH
    / "minimum-projection-size14-kempe-escape-20260729"
    / "failure-states.txt"
)
TARGETED = (
    SCRATCH
    / "minimum-projection-size15-exact-frontier-20260729"
    / "targeted-extension-output.txt"
)
ROW = re.compile(r"COUNTERSTATE word=(\S+) partition=(\d+)$")
RESIDUAL = re.compile(r"RESIDUAL word=(\S+) partition=(\d+)(?: .*)?$")
GL = tuple((0,) + image for image in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
EXPECTED_SIZE14_DIGEST = (
    "c41b8887e7863d5b8f773b95f806ee183fe604ead6313a32ec9df572bc3e99d3"
)
EXPECTED_TARGET_DIGEST = (
    "703a6beac5682565e1c0f0bc6a4f4e481ea2508cde4589047c87483fdb1c416a"
)
EXPECTED_FULL_7P8_DIGEST = (
    "f2c0c2b53322c72f00672e3f9c7d807aeb26a6ba771357a673c84c2fdaf96206"
)


def parse_state(encoded_word: str, encoded_partition: str):
    pieces = tuple(tuple(map(int, piece)) for piece in encoded_word.split("|"))
    lengths = tuple(map(len, pieces))
    word = tuple(value for piece in pieces for value in piece)
    partition = tuple(map(int, encoded_partition))
    assert len(word) == len(partition)
    return word, partition, lengths


def encode_word(word, lengths):
    result = []
    offset = 0
    for length in lengths:
        result.append("".join(map(str, word[offset : offset + length])))
        offset += length
    return "|".join(result)


def first_occurrence_normalize(values):
    names = {}
    result = []
    for value in values:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def circuit_actions(length: int, offset: int):
    """Return (edge indices, preceding-boundary indices) for D_length.

    A rotation lists old edges anchor+i in the new direction, so its
    preceding boundary has the same old index.  A reflection lists old edge
    anchor-i-1; its preceding boundary in the reversed direction is the old
    boundary after that edge, at anchor-i.
    """

    for anchor in range(length):
        yield (
            tuple(offset + (anchor + i) % length for i in range(length)),
            tuple(offset + (anchor + i) % length for i in range(length)),
        )
        yield (
            tuple(offset + (anchor - i - 1) % length for i in range(length)),
            tuple(offset + (anchor - i) % length for i in range(length)),
        )


def canonical_state(word, partition, lengths):
    """Canonical boundary-state key for one or two support circuits."""

    offsets = []
    offset = 0
    for length in lengths:
        offsets.append(offset)
        offset += length
    actions = tuple(
        tuple(circuit_actions(length, start))
        for length, start in zip(lengths, offsets)
    )
    orders = [tuple(range(len(lengths)))]
    if len(lengths) == 2 and lengths[0] == lengths[1]:
        orders.append((1, 0))
    best = None
    for selected in itertools.product(*actions):
        for order in orders:
            edge_indices = tuple(
                index for circuit in order for index in selected[circuit][0]
            )
            boundary_indices = tuple(
                index for circuit in order for index in selected[circuit][1]
            )
            transformed_word = first_occurrence_normalize(
                tuple(word[index] for index in edge_indices)
            )
            transformed_partition = first_occurrence_normalize(
                tuple(partition[index] for index in boundary_indices)
            )
            transformed_lengths = tuple(lengths[circuit] for circuit in order)
            key = (
                transformed_lengths,
                transformed_word,
                transformed_partition,
            )
            if best is None or key < best:
                best = key
    assert best is not None
    return best


def encoded_canonical_key(key):
    lengths, word, partition = key
    return (
        "+".join(map(str, lengths))
        + " "
        + encode_word(word, lengths)
        + " "
        + "".join(map(str, partition))
    )


def canonical_digest(keys):
    payload = "".join(
        encoded_canonical_key(key) + "\n" for key in sorted(keys)
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def circuits(lengths):
    result = []
    offset = 0
    for length in lengths:
        result.append(tuple(range(offset, offset + length)))
        offset += length
    return tuple(result)


def derivative(word, lengths):
    result = [0] * len(word)
    for circuit in circuits(lengths):
        for local, position in enumerate(circuit):
            result[position] = word[circuit[local - 1]] ^ word[position]
    return tuple(result)


def integrate(transitions, lengths):
    result = [0] * len(transitions)
    for circuit in circuits(lengths):
        value = 0
        for position in circuit:
            value ^= transitions[position]
            result[position] = value
        if value:
            return None
    return tuple(result)


def is_clean(base, partition, lengths):
    support_circuits = circuits(lengths)
    for tail in itertools.product(range(4), repeat=len(lengths) - 1):
        shifts = (0,) + tail
        parity = [
            [0, 0, 0, 0] for _ in range(max(partition, default=-1) + 1)
        ]
        for circuit_index, circuit in enumerate(support_circuits):
            for local, edge in enumerate(circuit):
                successor = circuit[(local + 1) % len(circuit)]
                left = partition[edge]
                right = partition[successor]
                if left != right:
                    colour = base[edge] ^ shifts[circuit_index]
                    parity[left][colour] ^= 1
                    parity[right][colour] ^= 1
        if not any(value for row in parity for value in row):
            return True
    return False


def classify(state):
    """Return exact feasible, clean-map, and deletion-map counts."""

    word, partition, lengths = state
    d = derivative(word, lengths)
    component_count = max(partition) + 1
    feasible = clean_count = delete_count = 0
    for tail in itertools.product(GL, repeat=component_count - 1):
        maps = (IDENTITY,) + tail
        transformed = tuple(
            maps[partition[position]][d[position]]
            for position in range(len(word))
        )
        base = integrate(transformed, lengths)
        if base is None:
            continue
        feasible += 1
        if is_clean(base, partition, lengths):
            clean_count += 1
        if any(
            len({base[position] for position in circuit}) < 4
            for circuit in circuits(lengths)
        ):
            delete_count += 1
    return feasible, clean_count, delete_count


def removable_positions(word, lengths):
    """Yield the repeated-colour deletions preserving proper all-four use."""

    for circuit_index, circuit in enumerate(circuits(lengths)):
        piece = tuple(word[position] for position in circuit)
        for local, colour in enumerate(piece):
            remaining = piece[:local] + piece[local + 1 :]
            if piece.count(colour) < 2:
                continue
            if piece[local - 1] == piece[(local + 1) % len(piece)]:
                continue
            if len(set(remaining)) != 4:
                continue
            yield circuit_index, local


def smooth(state, circuit_index, local):
    word, partition, lengths = state
    offset = sum(lengths[:circuit_index])
    length = lengths[circuit_index]
    removed = offset + local
    successor = offset + (local + 1) % length
    left_block = partition[removed]
    right_block = partition[successor]

    new_word = word[:removed] + word[removed + 1 :]
    raw_partition = list(partition)
    raw_partition.pop(removed)
    if left_block != right_block:
        raw_partition = [
            left_block if block == right_block else block
            for block in raw_partition
        ]
    new_partition = first_occurrence_normalize(raw_partition)
    new_lengths = (
        lengths[:circuit_index]
        + (length - 1,)
        + lengths[circuit_index + 1 :]
    )
    return (
        (new_word, new_partition, new_lengths),
        (left_block, right_block),
    )


def read_size14_keys():
    literal_rows = 0
    keys = set()
    for raw in SIZE14.read_text(encoding="utf-8").splitlines():
        match = ROW.fullmatch(raw)
        assert match is not None, raw
        literal_rows += 1
        state = parse_state(*match.groups())
        assert state[2] == (7, 7)
        keys.add(canonical_state(*state))
    assert literal_rows == 224
    return literal_rows, keys


def iter_states(paths):
    for path in paths:
        payload = path.read_text(encoding="utf-8")
        lines = payload.splitlines()
        for line_number, raw in enumerate(lines, 1):
            match = ROW.fullmatch(raw) or RESIDUAL.fullmatch(raw)
            if match is not None:
                encoded_word, encoded_partition = match.groups()
                word_length = len(encoded_word.replace("|", ""))
                if len(encoded_partition) != word_length:
                    if (
                        line_number == len(lines)
                        and not payload.endswith("\n")
                    ):
                        # A live census can be observed between writes making
                        # up one buffered line.  Ignore only that final
                        # unterminated fragment.
                        continue
                    raise AssertionError(
                        f"malformed residual row {path}:{line_number}: {raw}"
                    )
                yield (
                    path,
                    line_number,
                    parse_state(encoded_word, encoded_partition),
                )


def audit_residuals(paths, size14_keys):
    checked = covered = 0
    failures = []
    smoothing_histogram = {}
    input_canonical_keys = set()
    for path, line_number, state in iter_states(paths):
        checked += 1
        input_canonical_keys.add(canonical_state(*state))
        matches = []
        same_block_count = 0
        for circuit_index, local in removable_positions(
            state[0], state[2]
        ):
            short, blocks = smooth(state, circuit_index, local)
            if blocks[0] != blocks[1]:
                continue
            same_block_count += 1
            if canonical_state(*short) in size14_keys:
                matches.append((circuit_index, local))
        smoothing_histogram[same_block_count] = (
            smoothing_histogram.get(same_block_count, 0) + 1
        )
        if matches:
            covered += 1
        else:
            failures.append(
                {
                    "file": str(path),
                    "line": line_number,
                    "word": encode_word(state[0], state[2]),
                    "partition": "".join(map(str, state[1])),
                    "same_block_smoothings": same_block_count,
                }
            )
    return (
        checked,
        covered,
        smoothing_histogram,
        failures,
        input_canonical_keys,
    )


def verify_displayed_obstruction(size14_keys):
    original = parse_state(
        "01010123|0101232",
        "001234404130002",
    )
    assert classify(original) == (320, 0, 0)
    rows = []
    for circuit_index, local in removable_positions(
        original[0], original[2]
    ):
        short, blocks = smooth(original, circuit_index, local)
        counts = classify(short)
        in_224 = canonical_state(*short) in size14_keys
        rows.append(
            (
                circuit_index,
                local,
                blocks,
                encode_word(short[0], short[2]),
                "".join(map(str, short[1])),
                counts,
                in_224,
            )
        )

    expected = {
        (0, 0): ((0, 0), (320, 0, 40), False),
        (0, 5): ((4, 4), (320, 0, 0), True),
        (1, 0): ((4, 1), (56, 16, 0), False),
        (1, 3): ((0, 0), (320, 0, 80), False),
        (1, 4): ((0, 0), (320, 0, 80), False),
        (1, 6): ((2, 4), (56, 16, 0), False),
    }
    assert len(rows) == len(expected)
    for row in rows:
        key = (row[0], row[1])
        assert (row[2], row[5], row[6]) == expected[key]
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="full-census residual files; defaults to the targeted 6,180 rows",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="permit a zero-residual input collection",
    )
    parser.add_argument(
        "--expect-full-7p8",
        action="store_true",
        help="assert the frozen complete 7+8 residual counts and digest",
    )
    args = parser.parse_args()
    paths = args.files or [TARGETED]

    literal14, keys14 = read_size14_keys()
    digest14 = canonical_digest(keys14)
    assert len(keys14) == 200
    assert digest14 == EXPECTED_SIZE14_DIGEST
    print(
        f"SIZE14 literal_residuals={literal14}"
        f" canonical_equivalence_classes={len(keys14)}"
        f" canonical_digest={digest14}"
    )

    obstruction_rows = verify_displayed_obstruction(keys14)
    print("OBSTRUCTION original_feasible=320 clean=0 delete=0")
    for row in obstruction_rows:
        print(
            "SMOOTH"
            f" circuit={row[0]} local={row[1]}"
            f" blocks={row[2][0]},{row[2][1]}"
            f" word={row[3]} partition={row[4]}"
            f" feasible={row[5][0]} clean={row[5][1]}"
            f" delete={row[5][2]} equivalent_to_224={int(row[6])}"
        )

    (
        checked,
        covered,
        histogram,
        failures,
        input_keys,
    ) = audit_residuals(paths, keys14)
    input_digest = canonical_digest(input_keys)
    if not args.files:
        assert checked == covered == 6180
        assert not failures
        assert histogram == {3: 1076, 4: 4208, 5: 896}
        assert len(input_keys) == 5622
        assert input_digest == EXPECTED_TARGET_DIGEST
    if args.expect_full_7p8:
        assert args.files
        assert checked == covered == 6036
        assert not failures
        assert histogram == {3: 926, 4: 4060, 5: 1050}
        assert len(input_keys) == 5200
        assert input_digest == EXPECTED_FULL_7P8_DIGEST
    print(
        f"AUDIT checked={checked} covered={covered}"
        f" failures={len(failures)}"
        f" same_block_smoothing_histogram={sorted(histogram.items())}"
        f" canonical_input_classes={len(input_keys)}"
        f" canonical_input_digest={input_digest}"
    )
    for failure in failures[:20]:
        print(
            "INDUCTION_COUNTERSTATE"
            f" file={failure['file']} line={failure['line']}"
            f" word={failure['word']}"
            f" partition={failure['partition']}"
            f" same_block_smoothings={failure['same_block_smoothings']}"
        )
    if checked == 0 and not args.allow_empty:
        print("ERROR no residual rows found; use --allow-empty intentionally")
        raise SystemExit(2)
    if failures:
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
