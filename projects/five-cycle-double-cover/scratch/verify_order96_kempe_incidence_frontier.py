#!/usr/bin/env python3
"""Verify the abstract order-96 Kempe-incidence frontier matrix.

This checks only the necessary incidence inequalities documented in
docs/audit-and-generalization-order94-kempe.md.  It does not construct a
cubic graph and does not test universal separation or five-CDC.
"""

from itertools import combinations


MATRIX = (
    (1, 3, 0, 3, 0, 0, 0, 0),
    (3, 1, 0, 0, 0, 0, 0, 3),
    (0, 0, 2, 0, 0, 0, 2, 1),
    (0, 0, 2, 1, 0, 2, 0, 0),
    (0, 1, 2, 0, 2, 0, 0, 0),
    (0, 0, 0, 1, 2, 2, 0, 0),
    (1, 0, 0, 0, 0, 2, 2, 0),
    (0, 0, 0, 0, 2, 0, 2, 1),
)

A_EXCESS = (2, 2, 0, 0, 0, 0, 0, 0)
B_EXCESS = (0, 0, 1, 0, 1, 1, 1, 0)


def transpose(matrix):
    return tuple(tuple(matrix[i][j] for i in range(8)) for j in range(8))


def support_component_count(matrix, rows):
    """Components of the bipartite support induced by rows and neighbours."""
    unseen = set(rows)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        seen_columns = set()
        while stack:
            row = stack.pop()
            new_columns = {
                column
                for column, value in enumerate(matrix[row])
                if value and column not in seen_columns
            }
            seen_columns.update(new_columns)
            joined_rows = {
                other
                for other in unseen
                if any(matrix[other][column] for column in new_columns)
            }
            unseen.difference_update(joined_rows)
            stack.extend(joined_rows)
    return components


def minimum_multiswitch_slack(matrix, excess):
    """Return min of d+h+r-2|N(I)| over all nonempty row subsets I."""
    minimum = None
    witness = None
    for size in range(1, 9):
        for rows in combinations(range(8), size):
            neighbours = {
                column
                for row in rows
                for column, value in enumerate(matrix[row])
                if value
            }
            half_length_sum = sum(5 + excess[row] for row in rows)
            components = support_component_count(matrix, rows)
            slack = (
                half_length_sum
                + components
                + size
                - 2 * len(neighbours)
            )
            if minimum is None or slack < minimum:
                minimum = slack
                witness = (rows, len(neighbours), components)
    return minimum, witness


def main():
    matrix_t = transpose(MATRIX)

    assert tuple(map(sum, MATRIX)) == tuple(5 + x for x in A_EXCESS)
    assert tuple(map(sum, matrix_t)) == tuple(5 + y for y in B_EXCESS)
    assert all(MATRIX[i][i] >= 1 for i in range(8))

    for i in range(8):
        for j in range(8):
            assert MATRIX[i][j] <= 1 + A_EXCESS[i] + B_EXCESS[j]

    for i, row in enumerate(MATRIX):
        support = sum(value > 0 for value in row)
        assert support <= (7 + A_EXCESS[i]) // 2
    for j, column in enumerate(matrix_t):
        support = sum(value > 0 for value in column)
        assert support <= (7 + B_EXCESS[j]) // 2

    row_slack, row_witness = minimum_multiswitch_slack(MATRIX, A_EXCESS)
    column_slack, column_witness = minimum_multiswitch_slack(
        matrix_t, B_EXCESS
    )
    assert row_slack >= 0
    assert column_slack >= 0

    print("order96 incidence frontier: PASS")
    print(f"minimum A-side multi-switch slack: {row_slack} at {row_witness}")
    print(
        "minimum B-side multi-switch slack: "
        f"{column_slack} at {column_witness}"
    )
    print("scope: abstract incidence constraints only; no graph realization")


if __name__ == "__main__":
    main()
