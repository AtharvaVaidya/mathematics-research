#!/usr/bin/env python3
"""Clean-room falsification checks for the charge-rigidity theorem.

This program deliberately uses a different formulation from the theorem
package's verifier:

* balanced charge tables are parametrized by their free top-left rectangle;
* left kernels are compared as literal sets after componentwise 2x2 maps;
* boundary words are generated circuit-by-circuit, already satisfying the
  circuit xor equations;
* circuit translations are found by a newly implemented GF(2) eliminator,
  not by enumerating base colours; and
* all six choices for the first component map are retained (no gauge fixing).

An assertion failure is a finite counterexample to one of the audited claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


K = range(4)
NONZERO = (1, 2, 3)


def vxor(items):
    out = 0
    for item in items:
        out ^= item
    return out


def quadratic(u):
    """q(x,y)=xy for u=x+2y."""
    return (u & 1) & ((u >> 1) & 1)


def alternating(u, v):
    """B((x,y),(X,Y))=xY+yX."""
    return ((u & 1) & ((v >> 1) & 1)) ^ (((u >> 1) & 1) & (v & 1))


def matrices_gl2():
    answer = []
    for a, b, c, d in product((0, 1), repeat=4):
        if (a & d) ^ (b & c):
            answer.append((a, b, c, d))
    assert len(answer) == 6
    return tuple(answer)


GL2 = matrices_gl2()
IDENTITY = (1, 0, 0, 1)


def act(matrix, u):
    a, b, c, d = matrix
    x, y = u & 1, (u >> 1) & 1
    return (a & x) ^ (b & y) ^ (2 * ((c & x) ^ (d & y)))


def inverse(matrix):
    a, b, c, d = matrix
    # Every nonzero determinant in F_2 is one.
    return d, b, c, a


def multiply(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return (
        (a & e) ^ (b & g),
        (a & f) ^ (b & h),
        (c & e) ^ (d & g),
        (c & f) ^ (d & h),
    )


def balanced_completion(rows, columns, free_entries):
    """Complete a balanced K-valued table from its NW rectangle."""
    table = [[0 for _ in range(columns)] for _ in range(rows)]
    cursor = iter(free_entries)
    for a in range(rows - 1):
        for j in range(columns - 1):
            table[a][j] = next(cursor)
    for a in range(rows - 1):
        table[a][columns - 1] = vxor(table[a][:-1])
    for j in range(columns - 1):
        table[rows - 1][j] = vxor(table[a][j] for a in range(rows - 1))
    table[rows - 1][columns - 1] = vxor(table[rows - 1][:-1])
    result = tuple(tuple(row) for row in table)
    assert all(vxor(row) == 0 for row in result)
    assert all(vxor(result[a][j] for a in range(rows)) == 0 for j in range(columns))
    return result


def charge_components(table):
    """Return (blocks,circuits), retaining isolated blocks only."""
    row_count, column_count = len(table), len(table[0])
    neighbours = {('a', a): [] for a in range(row_count)}
    neighbours.update({('j', j): [] for j in range(column_count)})
    for a in range(row_count):
        for j in range(column_count):
            if table[a][j] != 0:
                neighbours['a', a].append(('j', j))
                neighbours['j', j].append(('a', a))

    seen = set()
    answer = []
    for root in (('a', a) for a in range(row_count)):
        if root in seen:
            continue
        seen.add(root)
        frontier = [root]
        blocks, circuits = [], []
        while frontier:
            kind, index = frontier.pop()
            (blocks if kind == 'a' else circuits).append(index)
            for neighbour in neighbours[kind, index]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    frontier.append(neighbour)
        answer.append((tuple(sorted(blocks)), tuple(sorted(circuits))))
    return tuple(answer)


def local_scalar_kernel(table, blocks, circuits):
    values = set()
    for local_mask in range(1 << len(blocks)):
        if all(
            vxor(
                table[a][j]
                for position, a in enumerate(blocks)
                if (local_mask >> position) & 1
            ) == 0
            for j in circuits
        ):
            values.add(local_mask)
    return frozenset(values)


def is_charge_rigid(table):
    for blocks, circuits in charge_components(table):
        if local_scalar_kernel(table, blocks, circuits) != frozenset(
            (0, (1 << len(blocks)) - 1)
        ):
            return False
    return True


def component_maps(table, choice):
    components = charge_components(table)
    assert len(choice) == len(components)
    owner_map = {}
    for component_index, (blocks, _circuits) in enumerate(components):
        for a in blocks:
            owner_map[a] = choice[component_index]
    return owner_map


def literal_mapped_left_kernel(table, choice):
    maps = component_maps(table, choice)
    row_count, column_count = len(table), len(table[0])
    answer = set()
    for mask in range(1 << row_count):
        if all(
            vxor(
                act(maps[a], table[a][j])
                for a in range(row_count)
                if (mask >> a) & 1
            ) == 0
            for j in range(column_count)
        ):
            answer.add(mask)
    return frozenset(answer)


def component_product_kernel(table):
    """Direct product of the component kernels, in global row coordinates."""
    partial = {0}
    for blocks, circuits in charge_components(table):
        lifted = []
        for local_mask in local_scalar_kernel(table, blocks, circuits):
            global_mask = 0
            for position, a in enumerate(blocks):
                if (local_mask >> position) & 1:
                    global_mask |= 1 << a
            lifted.append(global_mask)
        partial = {old ^ new for old in partial for new in lifted}
    return frozenset(partial)


def component_indicator_span(table):
    answer = {0}
    for blocks, _circuits in charge_components(table):
        indicator = sum(1 << a for a in blocks)
        answer |= {mask ^ indicator for mask in tuple(answer)}
    return frozenset(answer)


def maximum_charge_degree(table):
    row_count, column_count = len(table), len(table[0])
    degrees = [0] * (row_count + column_count)
    for a in range(row_count):
        for j in range(column_count):
            if table[a][j]:
                degrees[a] += 1
                degrees[row_count + j] += 1
    return max(degrees, default=0)


def audit_balanced_tables():
    table_count = rigid_count = degree_two_count = 0
    mapped_kernel_checks = 0
    for rows in range(1, 5):
        for columns in range(1, 5):
            freedom = (rows - 1) * (columns - 1)
            for serial, free in enumerate(product(K, repeat=freedom)):
                table = balanced_completion(rows, columns, free)
                table_count += 1
                expected = component_product_kernel(table)

                # Test a nonuniform deterministic map tuple for every table.
                components = charge_components(table)
                choice = tuple(
                    GL2[(serial + 2 * component + rows + columns) % 6]
                    for component in range(len(components))
                )
                assert literal_mapped_left_kernel(table, choice) == expected
                mapped_kernel_checks += 1

                # For all tables through 3 x 3, test every component-map tuple.
                if rows <= 3 and columns <= 3:
                    for exhaustive_choice in product(GL2, repeat=len(components)):
                        assert literal_mapped_left_kernel(table, exhaustive_choice) == expected
                        mapped_kernel_checks += 1

                rigid = is_charge_rigid(table)
                if rigid:
                    rigid_count += 1
                    assert expected == component_indicator_span(table)
                if maximum_charge_degree(table) <= 2:
                    degree_two_count += 1
                    assert rigid
    return table_count, rigid_count, degree_two_count, mapped_kernel_checks


def audit_two_column_corollary():
    checked = 0
    for rows in range(1, 7):
        for charges in product(K, repeat=rows):
            if vxor(charges) != 0:
                continue
            if sum(value != 0 for value in charges) > 3:
                continue
            table = tuple((value, value) for value in charges)
            assert is_charge_rigid(table)
            checked += 1
    return checked


def matrix_bits(matrix):
    return sum(bit << position for position, bit in enumerate(matrix))


def linear_functional(mask, matrix):
    return (mask & matrix_bits(matrix)).bit_count() & 1


def audit_tensor_core():
    """Check lambda's annihilator and all 4,096 three-vertex tensors."""
    by_images = {tuple(act(matrix, u) for u in K): matrix for matrix in GL2}
    lambda_maps = (
        by_images[(0, 1, 3, 2)],
        by_images[(0, 2, 1, 3)],
        by_images[(0, 3, 2, 1)],
    )
    assert len(lambda_maps) == 3
    assert len(lambda_maps) & 1
    for functional in range(16):
        assert vxor(linear_functional(functional, matrix) for matrix in lambda_maps) == 0

    pairs = ((0, 1), (0, 2), (1, 2))
    systems = 0
    for masks in product(range(16), repeat=3):
        systems += 1
        found = False
        for maps in product(GL2, repeat=3):
            degrees = [0, 0, 0]
            for pair_index, (a, b) in enumerate(pairs):
                relative = multiply(inverse(maps[a]), maps[b])
                edge = linear_functional(masks[pair_index], relative)
                degrees[a] ^= edge
                degrees[b] ^= edge
            if degrees == [0, 0, 0]:
                found = True
                break
        assert found
    return systems


@dataclass(frozen=True)
class CircuitPattern:
    owners: tuple[int, ...]
    derivatives: tuple[int, ...]
    charges: tuple[int, ...]


def circuit_catalog(length, block_count):
    derivative_words = tuple(
        word for word in product(NONZERO, repeat=length) if vxor(word) == 0
    )
    answer = []
    for owners in product(range(block_count), repeat=length):
        for derivatives in derivative_words:
            charges = [0] * block_count
            for a, derivative in zip(owners, derivatives):
                charges[a] ^= derivative
            answer.append(CircuitPattern(owners, derivatives, tuple(charges)))
    return tuple(answer)


def table_from_patterns(patterns, block_count):
    return tuple(
        tuple(pattern.charges[a] for pattern in patterns)
        for a in range(block_count)
    )


def solve_binary(equations, right_sides, variable_count):
    """Return one solution bit-mask, or None, using lowest-pivot elimination."""
    pivots = {}
    for coefficients, right in zip(equations, right_sides):
        row, value = coefficients, right
        while row:
            pivot = (row & -row).bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (row, value)
                break
            old_row, old_value = pivots[pivot]
            row ^= old_row
            value ^= old_value
        if row == 0 and value:
            return None

    solution = 0
    for pivot in sorted(pivots, reverse=True):
        row, value = pivots[pivot]
        known = (row & solution).bit_count() & 1
        if known ^ value:
            solution |= 1 << pivot
    assert all(((row & solution).bit_count() & 1) == rhs for row, rhs in zip(equations, right_sides))
    assert solution < (1 << variable_count)
    return solution


def integrate_and_measure(patterns, transformed, starts, block_count):
    obstruction = [0] * block_count
    for pattern, derivatives, start in zip(patterns, transformed, starts):
        current = start
        for owner, derivative in zip(pattern.owners, derivatives):
            following = current ^ derivative
            obstruction[owner] ^= quadratic(current) ^ quadratic(following)
            current = following
        assert current == start
    return tuple(obstruction)


def clean_charge_rigid_state(patterns, table, block_count):
    """Search every component-map tuple, solving translations by elimination."""
    components = charge_components(table)
    component_of = {}
    for component, (blocks, _circuits) in enumerate(components):
        for a in blocks:
            component_of[a] = component

    map_trials = 0
    for chosen_maps in product(GL2, repeat=len(components)):
        map_trials += 1
        transformed = []
        for pattern in patterns:
            word = tuple(
                act(chosen_maps[component_of[a]], derivative)
                for a, derivative in zip(pattern.owners, pattern.derivatives)
            )
            # This is the integrability claim under direct attack.
            assert vxor(word) == 0
            transformed.append(word)

        zero_starts = (0,) * len(patterns)
        base = integrate_and_measure(patterns, transformed, zero_starts, block_count)

        # Aggregating block obstructions must equal measuring the meta-block
        # boundary directly; internal support edges then cancel literally.
        meta_patterns = tuple(
            CircuitPattern(
                tuple(component_of[a] for a in pattern.owners),
                pattern.derivatives,
                tuple(),
            )
            for pattern in patterns
        )
        meta_base = integrate_and_measure(
            meta_patterns, transformed, zero_starts, len(components)
        )
        component_sums = tuple(
            vxor(base[a] for a in blocks) for blocks, _circuits in components
        )
        assert meta_base == component_sums

        equations = []
        for a in range(block_count):
            coefficient_mask = 0
            local_map = chosen_maps[component_of[a]]
            for j in range(len(patterns)):
                mapped_charge = act(local_map, table[a][j])
                # B(x+2y, u+2v)=xv+yu.
                if (mapped_charge >> 1) & 1:
                    coefficient_mask |= 1 << (2 * j)
                if mapped_charge & 1:
                    coefficient_mask |= 1 << (2 * j + 1)
            equations.append(coefficient_mask)

        solution = solve_binary(equations, base, 2 * len(patterns))
        # The audited left-kernel calculation says these are equivalent.
        assert (solution is not None) == all(value == 0 for value in component_sums)
        if solution is None:
            continue

        starts = tuple((solution >> (2 * j)) & 3 for j in range(len(patterns)))
        assert integrate_and_measure(patterns, transformed, starts, block_count) == (0,) * block_count
        return map_trials

    raise AssertionError(("charge-rigid counterexample", patterns, table))


def audit_boundary_shapes():
    """Exhaust small labelled states, including the first four-block regime."""
    shape_families = {
        3: ((2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2),
            (2, 5), (3, 4), (2, 2, 3)),
        4: ((2, 2), (2, 3), (2, 4), (3, 3), (2, 2, 2)),
    }
    report = []
    for block_count, shapes in shape_families.items():
        catalogs = {
            length: circuit_catalog(length, block_count)
            for length in range(2, max(max(shape) for shape in shapes) + 1)
        }
        for shape in shapes:
            raw = admissible = rigid = map_trials = 0
            for patterns in product(*(catalogs[length] for length in shape)):
                raw += 1
                if any(vxor(pattern.charges[a] for pattern in patterns) for a in range(block_count)):
                    continue
                admissible += 1
                table = table_from_patterns(patterns, block_count)
                if not is_charge_rigid(table):
                    continue
                rigid += 1
                map_trials += clean_charge_rigid_state(patterns, table, block_count)
            report.append((block_count, shape, raw, admissible, rigid, map_trials))
    return tuple(report)


def audit_polarization():
    checked = 0
    for x, y, z in product(K, repeat=3):
        assert quadratic(x ^ y) ^ quadratic(x) ^ quadratic(y) == alternating(x, y)
        assert alternating(z, x ^ y) == (alternating(z, x) ^ alternating(z, y))
        for matrix in GL2:
            assert act(matrix, x ^ y) == (act(matrix, x) ^ act(matrix, y))
            assert alternating(act(matrix, x), act(matrix, y)) == alternating(x, y)
            checked += 1
    return checked


def main():
    polarization = audit_polarization()
    tensors = audit_tensor_core()
    tables = audit_balanced_tables()
    two_column = audit_two_column_corollary()
    boundaries = audit_boundary_shapes()

    print(f"polarization / symplectic checks: {polarization}")
    print(f"complete three-meta-block tensor systems: {tensors}")
    print(
        "balanced tables (total, rigid, max-degree<=2, mapped-kernel checks): "
        f"{tables}"
    )
    print(f"two-column <=3-nonzero-row tables: {two_column}")
    for block_count, shape, raw, admissible, rigid, map_trials in boundaries:
        label = "+".join(map(str, shape))
        print(
            f"boundary blocks={block_count} shape={label}: raw={raw} admissible={admissible} "
            f"rigid={rigid} component-map-trials={map_trials}"
        )
    print("NO COUNTEREXAMPLE FOUND; ALL INDEPENDENT AUDIT CHECKS PASSED")


if __name__ == "__main__":
    main()
