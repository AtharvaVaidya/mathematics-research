#!/usr/bin/env python3
"""Independent literal audit of the five-block four-charge counterexample."""

from __future__ import annotations

import itertools
import json


MAPS = tuple((0,) + p for p in itertools.permutations((1, 2, 3)))
IDENTITY = (0, 1, 2, 3)
EDGES = tuple((a, b) for a in range(5) for b in range(a + 1, 5))
MASKS = (0, 0, 0, 0, 0, 0, 10, 0, 8, 2)

# Each (x,y) denotes the zero-charge word b(x),a(y),b(x),a(y) for
# edge a<b.  These terms were separately checked below against MASKS.
TERMS = (
    (),
    (),
    (),
    (),
    (),
    (),
    ((3, 1),),
    (),
    ((2, 1),),
    ((1, 1),),
)


def compose(left, right):
    return tuple(left[right[value]] for value in range(4))


def inverse(linear_map):
    return next(
        candidate
        for candidate in MAPS
        if compose(linear_map, candidate) == IDENTITY
        and compose(candidate, linear_map) == IDENTITY
    )


def alternating(left, right):
    return ((left & 1) & (right >> 1 & 1)) ^ (
        (left >> 1 & 1) & (right & 1)
    )


def quadratic(value):
    return (value & 1) & (value >> 1 & 1)


def matrix_entries(linear_map):
    return (
        linear_map[1] & 1,
        linear_map[1] >> 1 & 1,
        linear_map[2] & 1,
        linear_map[2] >> 1 & 1,
    )


def functional(mask, linear_map):
    return sum(
        (mask >> index & 1) * bit
        for index, bit in enumerate(matrix_entries(linear_map))
    ) & 1


def build_words():
    first = [(block, 1) for block in range(4)]
    for (left, right), terms in zip(EDGES, TERMS, strict=True):
        for x, y in terms:
            first.extend(((right, x), (left, y), (right, x), (left, y)))
    second = [(block, 1) for block in range(4)]
    return tuple(first), tuple(second)


WORDS = build_words()


def source_charges(word):
    result = [0] * 5
    for owner, derivative in word:
        result[owner] ^= derivative
    return tuple(result)


def literal_obstruction(local_maps, starts):
    result = [0] * 5
    for word, start in zip(WORDS, starts, strict=True):
        current = start
        for owner, source_derivative in word:
            following = current ^ local_maps[owner][source_derivative]
            result[owner] ^= quadratic(current) ^ quadratic(following)
            current = following
        if current != start:
            return None
    return tuple(result)


def tensor_obstruction(local_maps, relative_start):
    degree = [0] * 5
    for mask, (left, right) in zip(MASKS, EDGES, strict=True):
        relative_map = compose(inverse(local_maps[left]), local_maps[right])
        edge_value = functional(mask, relative_map)
        degree[left] ^= edge_value
        degree[right] ^= edge_value
    for block in range(4):
        degree[block] ^= alternating(relative_start, local_maps[block][1])
    return tuple(degree)


def audit_rank_one_realization():
    checks = 0
    for edge_index, ((left, right), terms) in enumerate(
        zip(EDGES, TERMS, strict=True)
    ):
        del left, right
        for left_map in MAPS:
            for right_map in MAPS:
                value = 0
                for x, y in terms:
                    value ^= alternating(right_map[x], left_map[y])
                relative_map = compose(inverse(left_map), right_map)
                assert value == functional(MASKS[edge_index], relative_map)
                checks += 1
    return checks


def audit_counterexample():
    assert tuple(map(source_charges, WORDS)) == (
        (1, 1, 1, 1, 0),
        (1, 1, 1, 1, 0),
    )

    all_map_assignments = feasible_maps = start_pairs = clean = 0
    formula_checks = common_shift_checks = 0
    solution_count_by_charge_shape = {"all_equal": 0, "two_pairs": 0}
    feasible_by_charge_shape = {"all_equal": 0, "two_pairs": 0}

    # Do not gauge-fix: enumerate all 6^5 local block maps independently.
    for local_maps in itertools.product(MAPS, repeat=5):
        all_map_assignments += 1
        transformed_charges = tuple(local_maps[a][1] for a in range(4))
        if transformed_charges[0] ^ transformed_charges[1] ^ transformed_charges[2] ^ transformed_charges[3]:
            continue
        feasible_maps += 1
        shape = (
            "all_equal"
            if len(set(transformed_charges)) == 1
            else "two_pairs"
        )
        assert shape == "all_equal" or sorted(
            transformed_charges.count(value) for value in set(transformed_charges)
        ) == [2, 2]
        feasible_by_charge_shape[shape] += 1

        for first_start in range(4):
            for second_start in range(4):
                start_pairs += 1
                literal = literal_obstruction(
                    local_maps, (first_start, second_start)
                )
                assert literal is not None
                relative = first_start ^ second_start
                predicted = tensor_obstruction(local_maps, relative)
                assert literal == predicted
                formula_checks += 1

                shifted = literal_obstruction(
                    local_maps, (first_start ^ 3, second_start ^ 3)
                )
                assert shifted == literal
                common_shift_checks += 1
                if not any(literal):
                    clean += 1
                    solution_count_by_charge_shape[shape] += 1

    assert all_map_assignments == 6**5
    assert feasible_maps == 2016
    assert start_pairs == feasible_maps * 16
    assert clean == 0
    return {
        "all_local_map_assignments": all_map_assignments,
        "integrable_local_map_assignments": feasible_maps,
        "literal_start_pairs_checked": start_pairs,
        "charged_tensor_formula_checks": formula_checks,
        "common_shift_invariance_checks": common_shift_checks,
        "feasible_maps_by_charge_shape": feasible_by_charge_shape,
        "clean_start_pairs_by_charge_shape": solution_count_by_charge_shape,
    }


def zero_tensor_translation_parity():
    """Count clean translations for the identically zero tensor family."""
    gauge_relative = full_start_pairs = 0
    shapes = {"all_equal": 0, "two_pairs": 0}
    for tail in itertools.product(MAPS, repeat=4):
        local_maps = (IDENTITY,) + tail
        charges = tuple(local_maps[a][1] for a in range(4))
        if charges[0] ^ charges[1] ^ charges[2] ^ charges[3]:
            continue
        shape = "all_equal" if len(set(charges)) == 1 else "two_pairs"
        clean_relative = sum(
            all(alternating(relative, charge) == 0 for charge in charges)
            for relative in range(4)
        )
        assert clean_relative == (2 if shape == "all_equal" else 1)
        shapes[shape] += clean_relative
        gauge_relative += clean_relative
        # Undoing the gauge supplies six common map choices; four common
        # circuit starts supply the other multiplicity.
        full_start_pairs += clean_relative * 6 * 4
    assert shapes == {"all_equal": 96, "two_pairs": 288}
    assert gauge_relative == 384 and full_start_pairs == 9216
    assert gauge_relative % 2 == full_start_pairs % 2 == 0
    return {
        "gauge_relative_translations": gauge_relative,
        "full_map_and_start_pairs": full_start_pairs,
        "parity": 0,
        "by_charge_shape_gauge": shapes,
    }


def main():
    rank_one_checks = audit_rank_one_realization()
    census = audit_counterexample()
    zero_tensor_parity = zero_tensor_translation_parity()
    print(
        json.dumps(
            {
                "status": "VERIFIED_FOUR_CHARGE_COUNTEREXAMPLE",
                "blocks": 5,
                "active_per_circuit_charge_blocks": 4,
                "circuit_lengths": tuple(map(len, WORDS)),
                "total_occurrences": sum(map(len, WORDS)),
                "per_circuit_source_charges": tuple(map(source_charges, WORDS)),
                "edge_order": EDGES,
                "tensor_masks": MASKS,
                "rank_one_realization_checks": rank_one_checks,
                "zero_tensor_solution_count": zero_tensor_parity,
                **census,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
