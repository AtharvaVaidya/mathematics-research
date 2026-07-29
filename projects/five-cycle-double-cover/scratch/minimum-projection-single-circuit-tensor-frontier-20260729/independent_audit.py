#!/usr/bin/env python3
"""Independent small audit of the tensor model and gadget realization."""

from __future__ import annotations

import itertools


MAPS = tuple((0,) + permutation for permutation in itertools.permutations((1, 2, 3)))
I = (0, 1, 2, 3)
LAMBDA_SUPPORT = (1, 2, 5)


def composition(left, right):
    return tuple(left[right[x]] for x in range(4))


def inverse(g):
    return next(h for h in MAPS if composition(g, h) == I == composition(h, g))


def entries(g):
    return (g[1] & 1, g[1] >> 1 & 1, g[2] & 1, g[2] >> 1 & 1)


def functional(mask, g):
    return sum((mask >> j & 1) * x for j, x in enumerate(entries(g))) & 1


def alternating(x, y):
    return ((x & 1) * (y >> 1 & 1) ^ (x >> 1 & 1) * (y & 1))


def rank_one_terms(mask):
    """Find at most two nonzero (x,y) with phi(h)=sum B(hx,y)."""
    target = tuple(functional(mask, g) for g in MAPS)
    atoms = tuple(
        (
            x,
            y,
            tuple(alternating(g[x], y) for g in MAPS),
        )
        for x in (1, 2, 3)
        for y in (1, 2, 3)
    )
    if not mask:
        return ()
    for x, y, values in atoms:
        if values == target:
            return ((x, y),)
    for first in atoms:
        for second in atoms:
            if tuple(a ^ b for a, b in zip(first[2], second[2])) == target:
                return ((first[0], first[1]), (second[0], second[1]))
    raise AssertionError(mask)


def gadget_value(terms, left, right):
    # Each term is the segment b(x),a(y),b(x),a(y).
    sequence = []
    for x, y in terms:
        sequence.extend(((1, x), (0, y), (1, x), (0, y)))
    transformed = [
        (owner, (right if owner else left)[value])
        for owner, value in sequence
    ]
    result = 0
    for later in range(len(transformed)):
        owner_later, value_later = transformed[later]
        if owner_later != 0:
            continue
        for earlier in range(later):
            owner_earlier, value_earlier = transformed[earlier]
            if owner_earlier == 1:
                result ^= alternating(value_earlier, value_later)
    return result


def audit_gadgets():
    for mask in range(16):
        terms = rank_one_terms(mask)
        for left in MAPS:
            for right in MAPS:
                relative = composition(inverse(left), right)
                assert gadget_value(terms, left, right) == functional(mask, relative)
    return 16


def audit_lambda():
    assert len(LAMBDA_SUPPORT) & 1
    for entry in range(4):
        assert not sum(
            entries(MAPS[index])[entry]
            for index in LAMBDA_SUPPORT
        ) & 1

    # For either endpoint fixed, every edge tensor is a coordinate-linear
    # function of the other endpoint and is therefore killed by lambda.
    for mask in range(16):
        for fixed in MAPS:
            assert not sum(
                functional(
                    mask,
                    composition(inverse(MAPS[index]), fixed),
                )
                for index in LAMBDA_SUPPORT
            ) & 1
            assert not sum(
                functional(
                    mask,
                    composition(inverse(fixed), MAPS[index]),
                )
                for index in LAMBDA_SUPPORT
            ) & 1
    return len(LAMBDA_SUPPORT)


def audit_expansion_cancellation(maximum=7):
    """Check the grouped-term argument on complete graphs through maximum."""
    checked = 0
    for vertex_count in range(1, maximum + 1):
        edges = tuple(
            (a, b)
            for a in range(vertex_count)
            for b in range(a + 1, vertex_count)
        )
        incident = tuple(
            tuple(
                edge_index
                for edge_index, edge in enumerate(edges)
                if vertex in edge
            )
            for vertex in range(vertex_count)
        )
        parity = {}
        for choices in itertools.product(
            *( (None,) + row for row in incident )
        ):
            edge_mask = 0
            for choice in choices:
                if choice is not None:
                    edge_mask |= 1 << choice
            parity[edge_mask] = parity.get(edge_mask, 0) ^ 1

        for edge_mask, coefficient in parity.items():
            if not coefficient or not edge_mask:
                continue
            degree = [0] * vertex_count
            for edge_index, (a, b) in enumerate(edges):
                if edge_mask >> edge_index & 1:
                    degree[a] += 1
                    degree[b] += 1
            assert 1 in degree
        checked += len(parity)
    return checked


def direct_obstruction(owners, values, base, vertex_count):
    integrated = []
    current = base
    for value in values:
        current ^= value
        integrated.append(current)
    assert current == base

    result = [0] * vertex_count
    for index, owner in enumerate(owners):
        result[owner] ^= (
            ((integrated[index - 1] & 1)
             * (integrated[index - 1] >> 1 & 1))
            ^ ((integrated[index] & 1)
               * (integrated[index] >> 1 & 1))
        )
    return tuple(result)


def cross_pair_obstruction(owners, values, vertex_count):
    edge_values = {}
    result = [0] * vertex_count
    for left in range(vertex_count):
        for right in range(left + 1, vertex_count):
            # Orient the unordered pair from ``left`` to ``right``:
            # right-owned occurrences precede left-owned occurrences.
            forward = 0
            reverse = 0
            for later in range(len(values)):
                for earlier in range(later):
                    if owners[earlier] == right and owners[later] == left:
                        forward ^= alternating(values[earlier], values[later])
                    if owners[earlier] == left and owners[later] == right:
                        reverse ^= alternating(values[earlier], values[later])
            assert forward == reverse
            edge_values[left, right] = forward
            result[left] ^= forward
            result[right] ^= forward
    return tuple(result), edge_values


def audit_cross_pair_reduction(maximum_length=6, vertex_count=3):
    """Exhaust the cyclic reduction on all small charge-zero words."""
    checked = 0
    for length in range(2, maximum_length + 1):
        for owners in itertools.product(range(vertex_count), repeat=length):
            for values in itertools.product((1, 2, 3), repeat=length):
                charge = [0] * vertex_count
                for owner, value in zip(owners, values):
                    charge[owner] ^= value
                if any(charge):
                    continue

                expected, edge_values = cross_pair_obstruction(
                    owners, values, vertex_count
                )
                for base in range(4):
                    assert (
                        direct_obstruction(
                            owners, values, base, vertex_count
                        )
                        == expected
                    )
                for cut in range(length):
                    rotated_owners = owners[cut:] + owners[:cut]
                    rotated_values = values[cut:] + values[:cut]
                    rotated, rotated_edges = cross_pair_obstruction(
                        rotated_owners, rotated_values, vertex_count
                    )
                    assert rotated == expected
                    assert rotated_edges == edge_values
                checked += 1
    return checked


def clean_assignment(vertex_count, masks):
    edge_list = tuple(
        (a, b)
        for a in range(vertex_count)
        for b in range(a + 1, vertex_count)
    )
    for tail in itertools.product(MAPS, repeat=vertex_count - 1):
        local = (I,) + tail
        degree = [0] * vertex_count
        for mask, (a, b) in zip(masks, edge_list):
            relative = composition(inverse(local[a]), local[b])
            value = functional(mask, relative)
            degree[a] ^= value
            degree[b] ^= value
        if not any(degree):
            return local
    return None


def exhaustive_k3():
    minimum = 6 ** 2
    minimizer = None
    fixed_gauge_support_failures = 0
    full_lambda_failures = 0
    for masks in itertools.product(range(16), repeat=3):
        count = 0
        for first, second in itertools.product(MAPS, repeat=2):
            local = (I, first, second)
            degrees = [0, 0, 0]
            for mask, (a, b) in zip(masks, ((0, 1), (0, 2), (1, 2))):
                relative = composition(inverse(local[a]), local[b])
                value = functional(mask, relative)
                degrees[a] ^= value
                degrees[b] ^= value
            count += not any(degrees)
        assert count
        if count < minimum:
            minimum, minimizer = count, masks
        fixed_gauge_support_parity = 0
        for first, second in itertools.product(
            LAMBDA_SUPPORT, repeat=2
        ):
            local = (I, MAPS[first], MAPS[second])
            degrees = [0, 0, 0]
            for mask, (a, b) in zip(masks, ((0, 1), (0, 2), (1, 2))):
                relative = composition(inverse(local[a]), local[b])
                value = functional(mask, relative)
                degrees[a] ^= value
                degrees[b] ^= value
            fixed_gauge_support_parity ^= not any(degrees)
        fixed_gauge_support_failures += fixed_gauge_support_parity != 1

        # This is the literal Lambda=lambda^{tensor 3} calculation in
        # the human proof; unlike the preceding relative-gauge census,
        # no map is fixed to the identity.
        full_lambda_parity = 0
        for local_indices in itertools.product(
            LAMBDA_SUPPORT, repeat=3
        ):
            local = tuple(MAPS[index] for index in local_indices)
            degrees = [0, 0, 0]
            for mask, (a, b) in zip(masks, ((0, 1), (0, 2), (1, 2))):
                relative = composition(inverse(local[a]), local[b])
                value = functional(mask, relative)
                degrees[a] ^= value
                degrees[b] ^= value
            full_lambda_parity ^= not any(degrees)
        full_lambda_failures += full_lambda_parity != 1

    assert not fixed_gauge_support_failures
    assert not full_lambda_failures
    return minimum, minimizer


def main():
    gadget_count = audit_gadgets()
    lambda_points = audit_lambda()
    expansion_groups = audit_expansion_cancellation()
    cross_pair_words = audit_cross_pair_reduction()
    minimum, minimizer = exhaustive_k3()
    print(f"gadget masks checked: {gadget_count}")
    print(f"lambda support points: {lambda_points}")
    print(f"expansion groups checked through K7: {expansion_groups}")
    print(f"charge-zero cyclic words checked through length 6: {cross_pair_words}")
    print(f"k=3 tensor systems checked: {16**3}")
    print("k=3 fixed-gauge support identities: 4096")
    print("k=3 full Lambda identities: 4096")
    print(f"minimum clean relative assignments: {minimum}")
    print("one minimizer:", " ".join(map(str, minimizer)))
    print("independent audit: PASS")


if __name__ == "__main__":
    main()
