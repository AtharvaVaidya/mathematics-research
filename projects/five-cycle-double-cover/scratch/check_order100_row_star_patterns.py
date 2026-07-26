#!/usr/bin/env python3
"""Exact cyclic-word filter for order-100 incidence matrices.

For one marked A-factor circuit, a cyclic word records which opposite
B-factor circuit contains each of its c-edges.  The distinguished mark is
fixed at position zero.  For every repeated neighbour, this checker asks
whether the resulting *fixed A-side gaps* extend to any weighted
three-matching kernel of girth at least ten.

This is a necessary row-local condition only.  Passing does not construct a
common set of B rotations, a cubic graph, universal separation, or a 5-CDC.
"""

from __future__ import annotations

import functools
import itertools


def compositions(total: int, parts: int):
    if parts == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


@functools.lru_cache(maxsize=None)
def b_weight_sequences(half_length: int, overlap: int, diagonal: bool):
    result = set()
    for gaps in compositions(half_length, overlap):
        if diagonal:
            result.add(tuple(2 * gap - 1 for gap in gaps))
            continue
        for marked_gap in range(overlap):
            if gaps[marked_gap] < 2:
                continue
            result.add(
                tuple(
                    2 * gap - 1 + (index == marked_gap)
                    for index, gap in enumerate(gaps)
                )
            )
    return tuple(sorted(result))


def kernel_edges(overlap: int, permutation, orientation_mask: int):
    """Return (u,v,kind,index) for Q, fixed A, and variable B matchings."""
    edges = []
    for edge in range(overlap):
        edges.append((2 * edge, 2 * edge + 1, 0, edge))
    for edge in range(overlap):
        edges.append(
            (2 * edge + 1, 2 * ((edge + 1) % overlap), 1, edge)
        )
    for position in range(overlap):
        current = permutation[position]
        following = permutation[(position + 1) % overlap]
        current_reverse = (orientation_mask >> current) & 1
        following_reverse = (orientation_mask >> following) & 1
        exit_vertex = 2 * current + (0 if current_reverse else 1)
        entry_vertex = 2 * following + (1 if following_reverse else 0)
        edges.append((exit_vertex, entry_vertex, 2, position))
    return tuple(edges)


@functools.lru_cache(maxsize=None)
def kernel_cycles(overlap: int, permutation, orientation_mask: int):
    """Enumerate all topological circuits, including two parallel paths."""
    edges = kernel_edges(overlap, permutation, orientation_mask)
    incidence = [[] for _ in range(2 * overlap)]
    for edge_id, (u, v, _kind, _index) in enumerate(edges):
        incidence[u].append(edge_id)
        incidence[v].append(edge_id)
    result = set()
    used = [False] * (2 * overlap)

    for start in range(2 * overlap):
        used[start] = True

        def visit(current: int, edge_mask: int, edge_count: int):
            for edge_id in incidence[current]:
                if edge_mask >> edge_id & 1:
                    continue
                u, v, _kind, _index = edges[edge_id]
                following = v if u == current else u
                if following == start:
                    if edge_count >= 1:
                        result.add(edge_mask | (1 << edge_id))
                    continue
                if following < start or used[following]:
                    continue
                used[following] = True
                visit(
                    following,
                    edge_mask | (1 << edge_id),
                    edge_count + 1,
                )
                used[following] = False

        visit(start, 0, 0)
        used[start] = False
    return tuple(sorted(result, key=lambda mask: (mask.bit_count(), mask)))


def fixed_a_weights(half_length: int, positions, diagonal: bool):
    positions = tuple(sorted(positions))
    overlap = len(positions)
    if diagonal:
        assert positions[0] == 0
    else:
        assert 0 not in positions
    gaps = tuple(
        (
            positions[(index + 1) % overlap]
            - positions[index]
        )
        % half_length
        or half_length
        for index in range(overlap)
    )
    assert all(gap >= 1 for gap in gaps) and sum(gaps) == half_length
    weights = [2 * gap - 1 for gap in gaps]
    if not diagonal:
        # With positions sorted away from zero, the wraparound residual path
        # is the unique one containing the private marked c-edge at position 0.
        assert gaps[-1] >= 2
        weights[-1] += 1
    return tuple(weights)


@functools.lru_cache(maxsize=None)
def pair_extends(x: int, y: int, diagonal: bool, positions):
    """Whether fixed A common-edge positions admit some complete B circuit."""
    half_a = 5 + x
    half_b = 5 + y
    positions = tuple(positions)
    overlap = len(positions)
    if overlap == 0:
        return True
    if not diagonal and (0 in positions or overlap >= min(half_a, half_b)):
        return False
    if diagonal and 0 not in positions:
        return False
    a_weights = fixed_a_weights(half_a, positions, diagonal)
    b_sequences = b_weight_sequences(half_b, overlap, diagonal)
    if not b_sequences:
        return False
    tail = tuple(range(1, overlap))
    for tail_permutation in itertools.permutations(tail):
        permutation = (0,) + tail_permutation
        for orientation_mask in range(1 << overlap):
            edges = kernel_edges(overlap, permutation, orientation_mask)
            cycles = kernel_cycles(overlap, permutation, orientation_mask)
            for b_weights in b_sequences:
                good = True
                for cycle in cycles:
                    length = 0
                    for edge_id, (_u, _v, kind, index) in enumerate(edges):
                        if not (cycle >> edge_id) & 1:
                            continue
                        if kind == 0:
                            length += 2 if diagonal and index == 0 else 1
                        elif kind == 1:
                            length += a_weights[index]
                        else:
                            length += b_weights[index]
                    if length < 10:
                        good = False
                        break
                if good:
                    return True
    return False


def multiset_words(counts):
    """Yield all words with the requested label multiplicities."""
    counts = list(counts)
    length = sum(counts)
    word = [0] * length

    def visit(position):
        if position == length:
            yield tuple(word)
            return
        for label, count in enumerate(counts):
            if count == 0:
                continue
            counts[label] -= 1
            word[position] = label
            yield from visit(position + 1)
            counts[label] += 1

    yield from visit(0)


def first_row_word(x, y, matrix, row: int):
    """Return the first A cyclic word passing every repeated-neighbour test."""
    counts = list(matrix[row])
    assert counts[row] >= 1
    counts[row] -= 1
    for tail in multiset_words(counts):
        word = (row,) + tail
        good = True
        for column, multiplicity in enumerate(matrix[row]):
            if multiplicity <= 1:
                continue
            positions = tuple(
                position
                for position, label in enumerate(word)
                if label == column
            )
            if not pair_extends(
                x[row], y[column], row == column, positions
            ):
                good = False
                break
        if good:
            return word
    return None


def matrix_passes_rows(x, y, matrix):
    words = []
    for row in range(8):
        word = first_row_word(x, y, matrix, row)
        if word is None:
            return False, tuple(words), row
        words.append(word)
    return True, tuple(words), None


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(8)) for column in range(8))


def matrix_passes_both_sides(x, y, matrix):
    left = matrix_passes_rows(x, y, matrix)
    if not left[0]:
        return False, left, None
    right = matrix_passes_rows(y, x, transpose(matrix))
    return right[0], left, right


def canonical_frontier_control():
    x = (4, 1, 1, 0, 0, 0, 0, 0)
    y = (0, 0, 0, 2, 2, 1, 1, 0)
    matrix = (
        (2, 2, 2, 0, 0, 0, 1, 2),
        (2, 1, 2, 0, 1, 0, 0, 0),
        (0, 2, 1, 0, 0, 1, 0, 2),
        (0, 0, 0, 1, 2, 0, 2, 0),
        (1, 0, 0, 0, 2, 0, 2, 0),
        (0, 0, 0, 2, 2, 1, 0, 0),
        (0, 0, 0, 2, 0, 2, 1, 0),
        (0, 0, 0, 2, 0, 2, 0, 1),
    )
    passed, left, right = matrix_passes_both_sides(x, y, matrix)
    print("order-100 row-star canonical control: PASS")
    print(f"matrix_survives={str(passed).lower()}")
    if not left[0]:
        print(f"first_failed_A_row={left[2]}")
    elif right is not None and not right[0]:
        print(f"first_failed_B_column={right[2]}")
    print(f"pair_predicate_cache={pair_extends.cache_info()}")
    assert not passed


def verify_local_cap_tables():
    expected_offdiagonal = (
        (1, 2, 2, 2, 2),
        (2, 2, 2, 3, 3),
        (2, 2, 3, 3, 4),
        (2, 3, 3, 3, 4),
        (2, 3, 4, 4, 4),
    )
    expected_diagonal = (
        (1, 1, 2, 2, 2),
        (1, 2, 2, 2, 3),
        (2, 2, 2, 3, 3),
        (2, 2, 3, 3, 4),
        (2, 3, 3, 4, 4),
    )
    observed = {False: [], True: []}
    for diagonal in (False, True):
        for x in range(5):
            row = []
            for y in range(5):
                maximum = 0
                half_a = 5 + x
                expected = (
                    expected_diagonal if diagonal else expected_offdiagonal
                )[x][y]
                # Test every multiplicity through the first forbidden one.
                # The independent C++ cap census handles all higher
                # multiplicities (including its Moore-bound tail).
                for overlap in range(1, expected + 2):
                    choices = (
                        (
                            (0,) + tail
                            for tail in itertools.combinations(
                                range(1, half_a), overlap - 1
                            )
                        )
                        if diagonal
                        else itertools.combinations(
                            range(1, half_a), overlap
                        )
                    )
                    if any(
                        pair_extends(x, y, diagonal, tuple(positions))
                        for positions in choices
                    ):
                        maximum = overlap
                row.append(maximum)
            observed[diagonal].append(tuple(row))
    assert tuple(observed[False]) == expected_offdiagonal
    assert tuple(observed[True]) == expected_diagonal
    print("fixed-gap kernel cap-table self-check: PASS")


if __name__ == "__main__":
    verify_local_cap_tables()
    canonical_frontier_control()
