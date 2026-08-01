#!/usr/bin/env python3
"""Independent exact audit of the charge-rigidity cleaning theorem."""

from __future__ import annotations

import itertools
import random


KSTAR = (1, 2, 3)
MAPS = tuple((0,) + p for p in itertools.permutations(KSTAR))
IDENTITY = (0, 1, 2, 3)


def q(x):
    return (x & 1) & ((x >> 1) & 1)


def xor_all(values):
    answer = 0
    for value in values:
        answer ^= value
    return answer


def rank_binary(vectors):
    basis = []
    for value in vectors:
        x = value
        for pivot in basis:
            x = min(x, x ^ pivot)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return len(basis)


def balanced(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    return (
        all(xor_all(matrix[a][j] for j in range(cols)) == 0 for a in range(rows))
        and all(xor_all(matrix[a][j] for a in range(rows)) == 0 for j in range(cols))
    )


def incidence_components(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    adjacency = [[] for _ in range(rows + cols)]
    for a in range(rows):
        for j in range(cols):
            if matrix[a][j]:
                adjacency[a].append(rows + j)
                adjacency[rows + j].append(a)
    seen = set()
    components = []
    # Retain every block, including isolated blocks.  Isolated circuits do
    # not participate in the block-row kernel and are intentionally ignored.
    for start in range(rows):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        block_nodes = []
        circuit_nodes = []
        while stack:
            node = stack.pop()
            if node < rows:
                block_nodes.append(node)
            else:
                circuit_nodes.append(node - rows)
            for other in adjacency[node]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append((tuple(sorted(block_nodes)), tuple(sorted(circuit_nodes))))
    return tuple(components)


def component_kernel(matrix, blocks, circuits):
    kernel = []
    for mask in range(1 << len(blocks)):
        if all(
            xor_all(
                matrix[block][circuit]
                for local, block in enumerate(blocks)
                if mask >> local & 1
            ) == 0
            for circuit in circuits
        ):
            kernel.append(mask)
    return tuple(kernel)


def charge_rigid(matrix):
    for blocks, circuits in incidence_components(matrix):
        kernel = component_kernel(matrix, blocks, circuits)
        if kernel != (0, (1 << len(blocks)) - 1):
            return False
    return True


def maximum_incidence_degree(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    degrees = [0] * (rows + cols)
    for a in range(rows):
        for j in range(cols):
            if matrix[a][j]:
                degrees[a] += 1
                degrees[rows + j] += 1
    return max(degrees, default=0)


def audit_matrices():
    checked = balanced_count = rigid_count = max2_count = 0
    for rows in range(1, 4):
        for cols in range(1, 4):
            for flat in itertools.product(range(4), repeat=rows * cols):
                checked += 1
                matrix = tuple(
                    tuple(flat[a * cols + j] for j in range(cols))
                    for a in range(rows)
                )
                if not balanced(matrix):
                    continue
                balanced_count += 1
                rigid_count += charge_rigid(matrix)
                if maximum_incidence_degree(matrix) <= 2:
                    max2_count += 1
                    assert charge_rigid(matrix)

    rng = random.Random(20260731)
    random_balanced = 0
    random_max2 = 0
    # Generate balanced 4 x 4 matrices by choosing the top-left 3 x 3
    # freely and solving the final row and column.  The bottom-right entry
    # is consistent because the xor of all prescribed row sums equals the
    # xor of all prescribed column sums.
    for _ in range(100_000):
        matrix = [[0] * 4 for _ in range(4)]
        for a in range(3):
            for j in range(3):
                matrix[a][j] = rng.randrange(4)
        for a in range(3):
            matrix[a][3] = xor_all(matrix[a][:3])
        for j in range(3):
            matrix[3][j] = xor_all(matrix[a][j] for a in range(3))
        matrix[3][3] = xor_all(matrix[3][:3])
        matrix = tuple(tuple(row) for row in matrix)
        assert balanced(matrix)
        random_balanced += 1
        if maximum_incidence_degree(matrix) <= 2:
            random_max2 += 1
            assert charge_rigid(matrix)
    return checked, balanced_count, rigid_count, max2_count, random_balanced, random_max2


def charges(owners_by_circuit, values_by_circuit, block_count):
    result = [[0] * len(owners_by_circuit) for _ in range(block_count)]
    for j, (owners, values) in enumerate(zip(owners_by_circuit, values_by_circuit)):
        for owner, value in zip(owners, values):
            result[owner][j] ^= value
    return tuple(tuple(row) for row in result)


def direct_obstructions(owners_by_circuit, transformed_by_circuit, starts, block_count):
    result = [0] * block_count
    for owners, values, start in zip(owners_by_circuit, transformed_by_circuit, starts):
        current = start
        for owner, value in zip(owners, values):
            before = current
            current ^= value
            result[owner] ^= q(before) ^ q(current)
        assert current == start
    return tuple(result)


def theorem_witness(owners_by_circuit, values_by_circuit, block_count):
    matrix = charges(owners_by_circuit, values_by_circuit, block_count)
    assert balanced(matrix)
    if not charge_rigid(matrix):
        return None
    components = incidence_components(matrix)
    group_of = {}
    for group, (blocks, _circuits) in enumerate(components):
        for block in blocks:
            group_of[block] = group

    # The theorem chooses one map per charge component.  Fixing the first
    # map to the identity is a harmless common GL(2,2) gauge.
    for tail in itertools.product(MAPS, repeat=max(0, len(components) - 1)):
        group_maps = (IDENTITY,) + tail if components else ()
        transformed = []
        for owners, values in zip(owners_by_circuit, values_by_circuit):
            row = tuple(group_maps[group_of[a]][d] for a, d in zip(owners, values))
            if xor_all(row):
                raise AssertionError("constant component maps must be integrable")
            transformed.append(row)
        for starts_tail in itertools.product(range(4), repeat=max(0, len(owners_by_circuit) - 1)):
            starts = (0,) + starts_tail if owners_by_circuit else ()
            if not any(direct_obstructions(owners_by_circuit, transformed, starts, block_count)):
                return group_maps, starts
    raise AssertionError("charge-rigid state lacked the promised cleaning")


def audit_boundary_shape(shape, block_count=3, limit=None):
    length = sum(shape)
    checked = admissible = rigid = 0
    alphabet = tuple(itertools.product(range(block_count), KSTAR))
    for word in itertools.product(alphabet, repeat=length):
        if limit is not None and checked >= limit:
            break
        checked += 1
        owners_by_circuit = []
        values_by_circuit = []
        offset = 0
        okay = True
        for circuit_length in shape:
            segment = word[offset:offset + circuit_length]
            offset += circuit_length
            owners = tuple(x[0] for x in segment)
            values = tuple(x[1] for x in segment)
            if xor_all(values):
                okay = False
                break
            owners_by_circuit.append(owners)
            values_by_circuit.append(values)
        if not okay:
            continue
        total = [0] * block_count
        for owners, values in zip(owners_by_circuit, values_by_circuit):
            for owner, value in zip(owners, values):
                total[owner] ^= value
        if any(total):
            continue
        admissible += 1
        matrix = charges(owners_by_circuit, values_by_circuit, block_count)
        if charge_rigid(matrix):
            rigid += 1
            assert theorem_witness(
                tuple(owners_by_circuit), tuple(values_by_circuit), block_count
            ) is not None
    return checked, admissible, rigid


def audit_two_circuit_corollary():
    checked = 0
    for block_count in (2, 3):
        # A two-column balanced matrix has rows (x,x).  Enumerate all such
        # matrices and verify the stated <=3-nonzero-row corollary literally.
        for row_values in itertools.product(range(4), repeat=block_count):
            if xor_all(row_values):
                continue
            matrix = tuple((x, x) for x in row_values)
            nonzero = sum(x != 0 for x in row_values)
            if nonzero <= 3:
                assert charge_rigid(matrix)
                checked += 1
    return checked


def main():
    matrix_counts = audit_matrices()
    shape22 = audit_boundary_shape((2, 2))
    shape23 = audit_boundary_shape((2, 3))
    # Deterministic prefix of the larger 3+3 raw stream; the algebraic matrix
    # exhaustion above is complete, while this is deliberately a direct
    # semantic stress test rather than a completeness claim for 3+3 words.
    shape33 = audit_boundary_shape((3, 3), limit=150_000)
    two_circuit = audit_two_circuit_corollary()
    print("balanced charge-matrix audit")
    print(f"  raw matrices through 3x3: {matrix_counts[0]}")
    print(f"  balanced matrices: {matrix_counts[1]}")
    print(f"  charge-rigid matrices: {matrix_counts[2]}")
    print(f"  balanced max-degree-two matrices: {matrix_counts[3]}")
    print(f"  deterministic balanced 4x4 matrices: {matrix_counts[4]}")
    print(f"  sampled max-degree-two 4x4 matrices: {matrix_counts[5]}")
    print(f"boundary shape 2+2 (raw, admissible, rigid): {shape22}")
    print(f"boundary shape 2+3 (raw, admissible, rigid): {shape23}")
    print(f"boundary shape 3+3 prefix (raw, admissible, rigid): {shape33}")
    print(f"two-circuit <=3-row charge matrices: {two_circuit}")
    print("ALL CHARGE-RIGIDITY CHECKS PASSED")


if __name__ == "__main__":
    main()
