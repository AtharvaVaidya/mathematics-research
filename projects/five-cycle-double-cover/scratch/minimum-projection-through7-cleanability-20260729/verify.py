#!/usr/bin/env python3
"""Exhaust the dirty size-six componentwise-GL boundary normal forms."""

from itertools import permutations, product


NONZERO = (1, 2, 3)
GL = tuple(
    (0,) + permutation
    for permutation in permutations(NONZERO)
    if permutation[2] == (permutation[0] ^ permutation[1])
)
AFFINE = tuple(permutations(range(4)))


def set_partitions(order):
    labels = [0] * order

    def recurse(index, maximum):
        if index == order:
            yield tuple(labels)
            return
        for value in range(maximum + 2):
            labels[index] = value
            yield from recurse(index + 1, max(maximum, value))

    yield from recurse(1, 0)


def normalize_partition(partition):
    names = {}
    result = []
    for value in partition:
        if value not in names:
            names[value] = len(names)
        result.append(names[value])
    return tuple(result)


def boundary_state(word, partition):
    order = len(word)
    pendant = tuple(word[index - 1] ^ word[index]
                    for index in range(order))
    dirty = []
    for component in range(max(partition) + 1):
        charge = 0
        for index in range(order):
            if partition[index] == component:
                charge ^= pendant[index]
        if charge:
            return None

        parities = []
        for colour in range(4):
            parity = 0
            for edge in range(order):
                crosses = ((partition[edge] == component)
                           != (partition[(edge + 1) % order] == component))
                parity ^= int(crosses and word[edge] == colour)
            parities.append(parity)
        if len(set(parities)) != 1:
            return None
        dirty.append(parities[0])
    return tuple(dirty) if any(dirty) else None


def componentwise_gl_repair(word, partition):
    order = len(word)
    pendant = tuple(word[index - 1] ^ word[index]
                    for index in range(order))
    components = max(partition) + 1
    for maps in product(GL, repeat=components):
        boundary = tuple(
            maps[partition[index]][pendant[index]]
            for index in range(order)
        )
        for starting_value in NONZERO:
            previous = starting_value
            circuit = []
            for value in boundary:
                previous ^= value
                circuit.append(previous)
                if previous == 0:
                    break
            else:
                if previous == starting_value:
                    # This is exactly the cyclic recurrence
                    # r_{i-1}+r_i=g_i with r_5=starting_value.
                    return True
    return False


def canonical_pair(word, partition):
    order = len(word)
    candidates = []
    for reflected in (False, True):
        for anchor in range(order):
            if not reflected:
                vertex_indices = tuple(
                    (anchor + index) % order for index in range(order)
                )
                edge_indices = vertex_indices
            else:
                # New vertex i is old vertex anchor-i.  New edge i then
                # joins old vertices anchor-i and anchor-i-1, so it is old
                # edge anchor-i-1.  Vertices and edges differ by this
                # essential one-step offset under reflection.
                vertex_indices = tuple(
                    (anchor - index) % order for index in range(order)
                )
                edge_indices = tuple(
                    (anchor - index - 1) % order for index in range(order)
                )
            shifted_word = tuple(word[index] for index in edge_indices)
            shifted_partition = normalize_partition(
                tuple(partition[index] for index in vertex_indices)
            )
            for affine_permutation in AFFINE:
                candidates.append((
                    tuple(affine_permutation[value]
                          for value in shifted_word),
                    shifted_partition,
                ))
    return min(candidates)


def classify(order, retain_orbits):
    orbit_counts = {}
    orbit_dirty = {}
    valid_dirty = 0
    failed_repair = 0
    failed_by_components = {}

    for word in product(range(4), repeat=order):
        if set(word) != set(range(4)):
            continue
        if any(word[index] == word[(index + 1) % order]
               for index in range(order)):
            continue
        for partition in set_partitions(order):
            if max(partition) == 0:
                continue
            dirty = boundary_state(word, partition)
            if dirty is None:
                continue
            valid_dirty += 1
            if componentwise_gl_repair(word, partition):
                continue
            failed_repair += 1
            components = max(partition) + 1
            failed_by_components[components] = (
                failed_by_components.get(components, 0) + 1
            )
            if not retain_orbits:
                continue
            representative = canonical_pair(word, partition)
            orbit_counts[representative] = (
                orbit_counts.get(representative, 0) + 1
            )
            orbit_dirty.setdefault(representative, dirty)
    return {
        "valid_dirty": valid_dirty,
        "failed_repair": failed_repair,
        "failed_by_components": failed_by_components,
        "orbit_counts": orbit_counts,
        "orbit_dirty": orbit_dirty,
    }


def main():
    assert len(GL) == 6
    assert len(AFFINE) == 24

    six = classify(6, retain_orbits=True)

    expected = {
        ((0, 1, 0, 1, 2, 3), (0, 0, 1, 0, 0, 1)): (1, 1),
        ((0, 1, 0, 2, 3, 2), (0, 0, 1, 0, 1, 0)): (1, 1),
        ((0, 1, 2, 0, 1, 3), (0, 0, 0, 1, 0, 1)): (1, 1),
    }
    assert six["valid_dirty"] == 2712
    assert six["failed_repair"] == 432
    assert six["failed_by_components"] == {2: 432}
    assert set(six["orbit_counts"]) == set(expected)
    assert set(six["orbit_counts"].values()) == {144}
    assert six["orbit_dirty"] == expected

    seven = classify(7, retain_orbits=False)
    assert seven["valid_dirty"] == 26880
    assert seven["failed_repair"] == 5376
    assert seven["failed_by_components"] == {2: 5376}

    # Audit the colour-avoiding arcs used for the exchange bounds.
    distance_rows = (
        ((0, 1, 0, 1, 2, 3), 2, 5, 3, False),
        ((0, 1, 0, 2, 3, 2), 2, 4, 2, True),
        ((0, 1, 2, 0, 1, 3), 3, 5, 2, True),
    )
    for word, first, second, claimed, complement_uses_all_four in distance_rows:
        arc = tuple(word[index] for index in range(first, second))
        complement = tuple(
            word[index % 6]
            for index in range(second, first + 6)
        )
        assert len(arc) == claimed
        assert len(set(arc)) < 4
        assert (len(set(complement)) == 4) == complement_uses_all_four

    print("PASS: exhaustive minimum-projection classification through size seven")
    print(
        "size6: "
        f"valid_dirty_pairs={six['valid_dirty']} "
        f"failed_componentwise_gl_repair={six['failed_repair']} "
        f"failed_by_components={six['failed_by_components']}"
    )
    for index, representative in enumerate(sorted(expected), start=1):
        word, partition = representative
        print(
            f"orbit_{index}: word={''.join(map(str, word))} "
            f"partition={''.join(map(str, partition))} "
            f"raw={six['orbit_counts'][representative]} "
            f"dirty={six['orbit_dirty'][representative]}"
        )
    print(
        "size7: "
        f"valid_dirty_pairs={seven['valid_dirty']} "
        f"failed_componentwise_gl_repair={seven['failed_repair']} "
        f"failed_by_components={seven['failed_by_components']} "
        "residual_after_two_component_theorem=0"
    )


if __name__ == "__main__":
    main()
