#!/usr/bin/env python3
"""Second independent audit of the proposed size-14 clean-or-delete failure."""

from collections import Counter, defaultdict
from itertools import permutations, product


WORD = tuple(map(int, "01010230101232"))
PARTITION = tuple(map(int, "01234444413024"))
LENGTHS = (7, 7)
OFFSETS = (0, 7)
NONZERO = (1, 2, 3)
GL = tuple(
    (0,) + permutation
    for permutation in permutations(NONZERO)
    if permutation[2] == permutation[0] ^ permutation[1]
)


def pendant_values():
    result = []
    for offset, length in zip(OFFSETS, LENGTHS):
        result.extend(
            WORD[offset + (index - 1) % length]
            ^ WORD[offset + index]
            for index in range(length)
        )
    return tuple(result)


def cut_edges(component):
    result = []
    for offset, length in zip(OFFSETS, LENGTHS):
        for local in range(length):
            edge = offset + local
            successor = offset + (local + 1) % length
            if (
                (PARTITION[edge] == component)
                != (PARTITION[successor] == component)
            ):
                result.append(edge)
    return tuple(result)


def integrate(boundary):
    circuits = []
    for offset, length in zip(OFFSETS, LENGTHS):
        previous = 0
        circuit = []
        for local in range(length):
            previous ^= boundary[offset + local]
            circuit.append(previous)
        if previous:
            return None
        circuits.append(tuple(circuit))
    return tuple(circuits)


def translated(circuits, relative_start):
    return circuits[0] + tuple(
        value ^ relative_start for value in circuits[1]
    )


def defects(repaired):
    result = []
    for component in range(5):
        parity = []
        cut = cut_edges(component)
        for colour in range(4):
            parity.append(
                sum(repaired[edge] == colour for edge in cut) % 2
            )
        assert len(set(parity)) == 1
        result.append(parity[0])
    return tuple(result)


def inverse(mapping):
    result = [0] * 4
    for value, image in enumerate(mapping):
        result[image] = value
    return tuple(result)


def compose(first, second):
    """first after second."""
    return tuple(first[second[value]] for value in range(4))


def main():
    pendant = pendant_values()
    print("word", "".join(map(str, WORD)))
    print("partition", "".join(map(str, PARTITION)))
    print("pendant", "".join(map(str, pendant)))

    dirty = []
    charges = []
    for component in range(5):
        charge = 0
        for index, value in enumerate(pendant):
            if PARTITION[index] == component:
                charge ^= value
        charges.append(charge)
        parity = tuple(
            sum(WORD[edge] == colour for edge in cut_edges(component)) % 2
            for colour in range(4)
        )
        assert len(set(parity)) == 1
        dirty.append(parity[0])
    assert charges == [0] * 5
    assert any(dirty)
    print("charges", charges)
    print("dirty", dirty)
    print("cuts", [cut_edges(component) for component in range(5)])

    # Fix the first component map to identity using common postcomposition.
    identity = (0, 1, 2, 3)
    feasible = 0
    clean = 0
    deletable = 0
    defect_cosets = Counter()
    map_records = []
    for tail in product(GL, repeat=4):
        maps = (identity,) + tail
        boundary = tuple(
            maps[PARTITION[index]][pendant[index]]
            for index in range(14)
        )
        circuits = integrate(boundary)
        if circuits is None:
            continue
        feasible += 1
        ranges = tuple(frozenset(circuit) for circuit in circuits)
        can_delete = any(len(values) < 4 for values in ranges)
        deletable += can_delete
        rows = tuple(
            defects(translated(circuits, relative))
            for relative in range(4)
        )
        can_clean = (0, 0, 0, 0, 0) in rows
        clean += can_clean
        canonical_coset = tuple(sorted(
            sum(bit << index for index, bit in enumerate(row))
            for row in rows
        ))
        defect_cosets[canonical_coset] += 1
        map_records.append((maps, boundary, circuits, ranges, rows))

    assert feasible > 0
    assert clean == 0
    assert deletable == 0
    print("normalized_map_assignments", 6 ** 4)
    print("feasible_normalized_maps", feasible)
    print("direct_clean_maps", clean)
    print("circuit_deletion_maps", deletable)
    print("defect_coset_histogram")
    for coset, count in sorted(defect_cosets.items()):
        print(" ", coset, count)

    # Independently check that normalization loses only the six common
    # postcomposition copies and preserves all outcomes.
    full_feasible = 0
    for maps in product(GL, repeat=5):
        boundary = tuple(
            maps[PARTITION[index]][pendant[index]]
            for index in range(14)
        )
        circuits = integrate(boundary)
        if circuits is None:
            continue
        full_feasible += 1
        assert all(len(set(circuit)) == 4 for circuit in circuits)
        assert all(
            defects(translated(circuits, relative))
            != (0, 0, 0, 0, 0)
            for relative in range(4)
        )
        normalizer = inverse(maps[0])
        normalized = tuple(
            compose(normalizer, mapping) for mapping in maps
        )
        assert normalized[0] == identity
    assert full_feasible == 6 * feasible
    print("full_feasible_maps", full_feasible)

    # Human-scale reduction.  Blocks 1,2,3 only see transition value 1,
    # so their unused map orientation has no effect.  Block 4 sees 1 and
    # 2, so an effective normalized map is encoded by
    # (L1(1),L2(1),L3(1),L4(2);L4(1)).
    effective = defaultdict(list)
    for first, second, third, fourth in product(NONZERO, repeat=4):
        if 3 ^ first ^ second ^ third ^ fourth:
            continue
        for fifth in NONZERO:
            if fifth == fourth:
                continue
            maps = (
                identity,
                next(mapping for mapping in GL if mapping[1] == first),
                next(mapping for mapping in GL if mapping[1] == second),
                next(mapping for mapping in GL if mapping[1] == third),
                next(
                    mapping for mapping in GL
                    if mapping[2] == fourth and mapping[1] == fifth
                ),
            )
            boundary = tuple(
                maps[PARTITION[index]][pendant[index]]
                for index in range(14)
            )
            circuits = integrate(boundary)
            assert circuits is not None
            assert all(len(set(circuit)) == 4 for circuit in circuits)
            coset = tuple(sorted(
                sum(bit << index for index, bit in enumerate(
                    defects(translated(circuits, relative))
                ))
                for relative in range(4)
            ))
            effective[coset].append(
                f"{first}{second}{third}{fourth};{fifth}"
            )
    assert sum(map(len, effective.values())) == 40
    assert set(effective) == set(defect_cosets)
    print("effective_40_state_table")
    for coset, codes in sorted(effective.items()):
        assert len(codes) == 4
        print(" ", coset, " ".join(codes))
    print("PASS: abstract candidate is dirty, not direct-clean, not deletable")


if __name__ == "__main__":
    main()
