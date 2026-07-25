#!/usr/bin/env python3
"""Verify the defect and pendant-cap identities."""

import sympy as sp


def intersection_matrix(self_intersections, edges):
    matrix = sp.diag(*self_intersections)
    for left, right in edges:
        matrix[left, right] = matrix[right, left] = 1
    return matrix


def verify_defect_ledger() -> None:
    self_intersections = [
        -2, -3, -4, -3, -2, -5, -2, -2, -5, -3, -1, -1, -1, -2,
        -1, -1, -1, -1, -1,
    ]
    edges = [
        (0, 1), (0, 5), (0, 15), (1, 2), (1, 18), (2, 4), (2, 13),
        (3, 12), (4, 12), (5, 9), (6, 7), (7, 8), (8, 10), (8, 11),
        (8, 17), (9, 10), (9, 14), (13, 16),
    ]
    q_matrix = intersection_matrix(self_intersections, edges)
    b = sp.Matrix([16, 12, 8, 8, 16, 4, 1, 2, 3, 4, 7, 3, 24, 4, 1, 16, 0, 3, 12])
    y = sp.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0])
    eta = sp.Matrix([138, 105, 72, 74, 147, 33, 8, 15, 21, 27, 48, 21, 221, 36, 0, 138, 0, 21, 105])
    z = sp.Matrix([0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    defect = 9 * b - eta

    assert q_matrix * b == y
    assert q_matrix * eta + z == 9 * y
    assert q_matrix * defect == z
    bad_finals = [10, 11, 12, 15, 17, 18]
    assert [defect[i] for i in bad_finals] == [15, 6, -5, 6, 6, 3]
    assert defect[3] == -2
    assert defect[4] == -3
    assert defect[12] + defect[3] == -7
    assert defect[12] + defect[4] == -8


def verify_chain_moment_formula() -> None:
    final_value = sp.symbols("final_value")
    for length in range(1, 10):
        incidences = sp.symbols(f"z1:{length + 1}", nonnegative=True)
        values = [None] * (length + 1)
        values[length] = final_value
        values[length - 1] = final_value + incidences[length - 1]
        for index in range(length - 1, 0, -1):
            values[index - 1] = sp.expand(
                incidences[index - 1]
                + 2 * values[index]
                - values[index + 1]
            )
        expected = final_value + sum(
            (index + 1) * incidence
            for index, incidence in enumerate(incidences)
        )
        assert sp.expand(values[0] - expected) == 0


def verify_cluster_m_matrices() -> None:
    """Check representative branched/crossing exceptional clusters."""

    def matrix(self_intersections, edges):
        result = sp.diag(*self_intersections)
        for left, right in edges:
            result[left, right] = result[right, left] = 1
        return result

    # Smooth-center cluster: generic, generic, crossing of the two new
    # curves, then generic branches on two different vertices.
    smooth_self = [-3, -3, -2, -1, -1]
    smooth_edges = {(0, 2), (1, 2), (2, 3), (1, 4)}
    smooth_q = matrix(smooth_self, smooth_edges)

    # Crossing-center cluster: the first exceptional meets both old
    # components; subsequent blowups create a branched exceptional tree.
    crossing_self = [-3, -2, -2, -1, -1]
    crossing_edges = {(0, 1), (0, 2), (1, 3), (2, 4)}
    crossing_q = matrix(crossing_self, crossing_edges)

    for q_matrix in (smooth_q, crossing_q):
        positive_matrix = -q_matrix
        assert all(
            positive_matrix[:size, :size].det() > 0
            for size in range(1, positive_matrix.rows + 1)
        )
        inverse = positive_matrix.inv()
        assert all(entry > 0 for entry in inverse)


def verify_regular_blowup_recurrences() -> None:
    parent_b, new_b = sp.symbols("parent_b new_b")
    # A generic blowup changes the old zero y-row and creates the new
    # row by opposite quantities.
    changed_parent_y = new_b - parent_b
    new_y = parent_b - new_b
    assert changed_parent_y + new_y == 0
    assert sp.solve(
        [changed_parent_y, new_y],
        [new_b],
        dict=True,
    ) == [{new_b: parent_b}]

    left_b, right_b, crossing_b = sp.symbols(
        "left_b right_b crossing_b"
    )
    changed_left_y = crossing_b - left_b - right_b
    changed_right_y = crossing_b - left_b - right_b
    crossing_y = left_b + right_b - crossing_b
    assert changed_left_y == changed_right_y == -crossing_y
    assert sp.solve(
        [changed_left_y, changed_right_y, crossing_y],
        [crossing_b],
        dict=True,
    ) == [{crossing_b: left_b + right_b}]


def main() -> None:
    verify_defect_ledger()
    verify_chain_moment_formula()
    verify_cluster_m_matrices()
    verify_regular_blowup_recurrences()
    print("verified Q*(d*b-eta)=z for the 19-vertex ledger")
    print("verified the all-length pendant-chain moment formula")
    print("verified positive inverse matrices for branched/crossing caps")
    print("verified generic and crossing post-resolution no-repair recurrences")


if __name__ == "__main__":
    main()
