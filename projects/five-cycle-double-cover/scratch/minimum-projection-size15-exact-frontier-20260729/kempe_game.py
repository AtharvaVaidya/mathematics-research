#!/usr/bin/env python3
"""Game-theoretic one/two-path Kempe analysis of size-15 boundary states.

For one chosen two-colour subgraph in one complement component, Nature fixes
its perfect matching of boundary terminals.  We may switch any displayed
path.  A cross-circuit path can be charge-restored either by a second path
from the same matching or by a path in another component.  In the latter
case the certificate must work against every matching of that component.

This checker is exact for one supplied abstract state.  It does not assert
that the targeted extension family exhausts the full size-15 census.
"""

from __future__ import annotations

import functools
import itertools
import sys
from collections import Counter

from targeted_extensions import (
    GL,
    ID,
    circuits_for,
    clean,
    derivative,
    encode_word,
    integrate,
)


COLOUR_PAIRS = ((1, 2), (1, 3), (2, 3))


@functools.lru_cache(maxsize=None)
def classify_d(transitions, partition, lengths):
    circuits = circuits_for(lengths)
    components = max(partition) + 1
    feasible = clean_count = delete_count = 0
    certificate = None
    for tail in itertools.product(GL, repeat=components - 1):
        maps = (ID,) + tail
        transformed = tuple(
            maps[partition[position]][transitions[position]]
            for position in range(len(transitions))
        )
        base = integrate(transformed, circuits)
        if base is None:
            continue
        feasible += 1
        if clean(base, partition, circuits):
            clean_count += 1
            if certificate is None:
                certificate = ("clean", maps, base)
        for circuit_index, circuit in enumerate(circuits):
            used = {base[position] for position in circuit}
            if len(used) < 4:
                delete_count += 1
                if certificate is None:
                    missing = next(
                        value for value in range(4) if value not in used
                    )
                    certificate = (
                        "delete",
                        circuit_index,
                        missing,
                        maps,
                        base,
                    )
                break
    return feasible, clean_count, delete_count, certificate


def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for index in range(1, len(items)):
        second = items[index]
        rest = items[1:index] + items[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def circuit_indices(lengths):
    result = []
    for circuit_index, circuit in enumerate(circuits_for(lengths)):
        result.extend([circuit_index] * len(circuit))
    return tuple(result)


def switched(transitions, pairs, delta):
    result = list(transitions)
    for pair in pairs:
        for endpoint in pair:
            result[endpoint] ^= delta
    return tuple(result)


def terminal_blocks(transitions, partition, colours):
    components = max(partition) + 1
    return tuple(
        tuple(
            position
            for position, owner in enumerate(partition)
            if owner == block and transitions[position] in colours
        )
        for block in range(components)
    )


def analyze_state(word, partition, lengths, verbose=False):
    circuits = circuits_for(lengths)
    which_circuit = circuit_indices(lengths)
    transitions = derivative(word, circuits)
    assert all(
        functools.reduce(
            int.__xor__,
            (transitions[position] for position in circuit),
            0,
        )
        == 0
        for circuit in circuits
    )
    assert all(
        functools.reduce(
            int.__xor__,
            (
                transitions[position]
                for position, owner in enumerate(partition)
                if owner == block
            ),
            0,
        )
        == 0
        for block in range(max(partition) + 1)
    )
    initial = classify_d(transitions, partition, lengths)
    assert initial[0] and initial[1] == initial[2] == 0

    attempts = []
    for active_block in range(max(partition) + 1):
        for colours in COLOUR_PAIRS:
            delta = colours[0] ^ colours[1]
            terminals_by_block = terminal_blocks(
                transitions, partition, colours
            )
            terminals = terminals_by_block[active_block]
            if len(terminals) < 2:
                continue
            active_matchings = tuple(perfect_matchings(terminals))
            matching_rows = []
            all_rescued = True
            for matching in active_matchings:
                rescue = None
                for primary in matching:
                    primary_cross = (
                        which_circuit[primary[0]]
                        != which_circuit[primary[1]]
                    )
                    if not primary_cross:
                        result = classify_d(
                            switched(transitions, (primary,), delta),
                            partition,
                            lengths,
                        )
                        if result[1] or result[2]:
                            rescue = ("one", primary, result[3])
                            break
                    else:
                        # A second cross path in this same known matching.
                        for auxiliary in matching:
                            if auxiliary == primary:
                                continue
                            if (
                                which_circuit[auxiliary[0]]
                                == which_circuit[auxiliary[1]]
                            ):
                                continue
                            result = classify_d(
                                switched(
                                    transitions,
                                    (primary, auxiliary),
                                    delta,
                                ),
                                partition,
                                lengths,
                            )
                            if result[1] or result[2]:
                                rescue = (
                                    "same-block-two",
                                    primary,
                                    auxiliary,
                                    result[3],
                                )
                                break
                        if rescue is not None:
                            break

                        # Or use a second component, robust against its unknown
                        # path pairing.
                        for auxiliary_block, aux_terminals in enumerate(
                            terminals_by_block
                        ):
                            if auxiliary_block == active_block:
                                continue
                            aux_matchings = tuple(
                                perfect_matchings(aux_terminals)
                            )
                            if not aux_matchings:
                                continue
                            aux_rows = []
                            robust = True
                            for aux_matching in aux_matchings:
                                aux_rescue = None
                                for auxiliary in aux_matching:
                                    if (
                                        which_circuit[auxiliary[0]]
                                        == which_circuit[auxiliary[1]]
                                    ):
                                        continue
                                    result = classify_d(
                                        switched(
                                            transitions,
                                            (primary, auxiliary),
                                            delta,
                                        ),
                                        partition,
                                        lengths,
                                    )
                                    if result[1] or result[2]:
                                        aux_rescue = (
                                            auxiliary,
                                            result[3],
                                        )
                                        break
                                if aux_rescue is None:
                                    robust = False
                                    break
                                aux_rows.append(aux_rescue)
                            if robust:
                                rescue = (
                                    "other-block-two",
                                    primary,
                                    auxiliary_block,
                                    tuple(aux_rows),
                                )
                                break
                        if rescue is not None:
                            break
                if rescue is None:
                    all_rescued = False
                    matching_rows.append((matching, None))
                    break
                matching_rows.append((matching, rescue))
            attempts.append(
                (
                    active_block,
                    colours,
                    terminals,
                    len(active_matchings),
                    all_rescued,
                    tuple(matching_rows),
                )
            )
            if all_rescued:
                if verbose:
                    print(
                        "ROBUST"
                        f" block={active_block} colours={colours}"
                        f" terminals={terminals}"
                        f" matchings={len(active_matchings)}"
                    )
                return True, attempts
    if verbose:
        print("NO_ROBUST_ONE_OR_TWO_PATH_STRATEGY")
        for row in attempts:
            print(
                "ATTEMPT"
                f" block={row[0]} colours={row[1]}"
                f" terminals={row[2]} matchings={row[3]}"
                f" first_bad={row[5][-1][0] if row[5] else None}"
            )
    return False, attempts


def parse_state(encoded_word, encoded_partition):
    pieces = tuple(tuple(map(int, row)) for row in encoded_word.split("|"))
    lengths = tuple(map(len, pieces))
    return (
        tuple(value for row in pieces for value in row),
        tuple(map(int, encoded_partition)),
        lengths,
    )


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: analyze WORD PARTITION")
    state = parse_state(sys.argv[1], sys.argv[2])
    word, partition, lengths = state
    print(
        f"word={encode_word(word, lengths)}"
        f" partition={''.join(map(str, partition))}"
        f" profile={tuple(sorted(Counter(partition).values(), reverse=True))}"
    )
    robust, _attempts = analyze_state(*state, verbose=True)
    raise SystemExit(0 if robust else 1)


if __name__ == "__main__":
    main()
