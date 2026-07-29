#!/usr/bin/env python3
"""Independent finite audit of the six-map parity identity."""

from __future__ import annotations

import itertools


IDENTITY = (0, 1, 2, 3)
GL = tuple(
    (0,) + permutation
    for permutation in itertools.permutations((1, 2, 3))
)


def compose(left, right):
    return tuple(left[right[value]] for value in range(4))


def group_order(linear_map):
    power = IDENTITY
    for exponent in range(1, 7):
        power = compose(linear_map, power)
        if power == IDENTITY:
            return exponent
    raise AssertionError(linear_map)


ORDER_THREE = tuple(
    linear_map for linear_map in GL
    if group_order(linear_map) == 3
)
INVOLUTIONS = tuple(
    linear_map for linear_map in GL
    if group_order(linear_map) == 2
)


def quadratic(value):
    return (value & 1) & (value >> 1 & 1)


def xor_all(values):
    result = 0
    for value in values:
        result ^= value
    return result


def local_sum(family, edge_value, potential):
    return xor_all(
        quadratic(
            edge_value
            ^ linear_map[potential]
            ^ potential
        )
        for linear_map in family
    )


def expected_h(edge_value, potential):
    return (
        quadratic(edge_value ^ potential)
        ^ (potential != 0)
    )


def audit_local_table():
    order_three_family = (IDENTITY,) + ORDER_THREE
    assert len(order_three_family) == 3
    assert len(INVOLUTIONS) == 3
    checked = 0
    for edge_value in range(4):
        for potential in range(4):
            expected = expected_h(edge_value, potential)
            assert (
                local_sum(
                    order_three_family,
                    edge_value,
                    potential,
                )
                == expected
            )
            assert (
                local_sum(
                    INVOLUTIONS,
                    edge_value,
                    potential,
                )
                == expected
            )
            checked += 1
    assert checked == 16
    return checked


def parity_row(transitions, selected):
    edge_values = []
    value = 0
    for transition in transitions:
        value ^= transition
        edge_values.append(value)
    assert value == 0

    potentials = []
    value = 0
    for transition, is_selected in zip(transitions, selected):
        if is_selected:
            value ^= transition
        potentials.append(value)
    assert value == 0

    cut_edges = tuple(
        edge
        for edge in range(len(transitions))
        if selected[edge] != selected[(edge + 1) % len(selected)]
    )

    values = []
    for linear_map in GL:
        values.append(
            xor_all(
                quadratic(
                    edge_values[edge]
                    ^ linear_map[potentials[edge]]
                    ^ potentials[edge]
                )
                for edge in cut_edges
            )
        )
    return tuple(values)


def audit_balanced_circuits(maximum_length=8):
    checked = 0
    order_three_family = (IDENTITY,) + ORDER_THREE
    for length in range(1, maximum_length + 1):
        for transitions in itertools.product(
            (1, 2, 3), repeat=length
        ):
            if xor_all(transitions):
                continue
            for selected in itertools.product((0, 1), repeat=length):
                if xor_all(
                    transition
                    for transition, is_selected
                    in zip(transitions, selected)
                    if is_selected
                ):
                    continue
                values = parity_row(transitions, selected)
                assert not xor_all(
                    values[GL.index(linear_map)]
                    for linear_map in order_three_family
                )
                assert not xor_all(
                    values[GL.index(linear_map)]
                    for linear_map in INVOLUTIONS
                )
                checked += 1
    assert checked == 126_258
    return checked


def main():
    local_rows = audit_local_table()
    circuit_rows = audit_balanced_circuits()
    print(f"SIX_MAP_TABLE rows={local_rows} failures=0")
    print(
        "BALANCED_CIRCUIT_ROWS"
        f" maximum_length=8 checked={circuit_rows} failures=0"
    )
    print("SINGLE_WITNESS_IDENTITY PASS")
    print("GLOBAL_CLEANLINESS_IMPLICATION NOT_CLAIMED")
    print("PASS")


if __name__ == "__main__":
    main()
