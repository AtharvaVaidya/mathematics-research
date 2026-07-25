#!/usr/bin/env python3
"""Verify the fixed-plane compactification pullback ledgers.

The first tree satisfies the canonical/pullback-line equations but has
an exact dual certificate excluding an effective conductor-image
pullback.  The second tree satisfies the full effective G ledger and the
component adjunction equations, but deliberately fails the theorem that
every final boundary curve is type 1 or type 3.  These are numerical
intersection ledgers; this script does not construct a morphism.
"""

from fractions import Fraction

import sympy as sp


def intersection_matrix(self_intersections, edges):
    size = len(self_intersections)
    matrix = sp.diag(*self_intersections)
    for left, right in edges:
        matrix[left, right] = matrix[right, left] = 1
    return matrix


def verify_full_ledger_blowup_history(expected_self, expected_labels, expected_edges):
    """Rebuild the 19-node tree from the stated eleven blowups."""

    self_intersections = [-1, -2, -3, -2, -1, -3, -2, -1]
    labels = [-2, -1, 0, 1, 1, -1, 0, -1]
    edges = {
        (0, 1), (0, 5), (1, 2), (2, 4), (3, 4), (5, 7), (6, 7)
    }

    def crossing(left, right):
        edge = tuple(sorted((left, right)))
        assert edge in edges
        edges.remove(edge)
        self_intersections[left] -= 1
        self_intersections[right] -= 1
        new = len(labels)
        labels.append(labels[left] + labels[right])
        self_intersections.append(-1)
        edges.add(tuple(sorted((left, new))))
        edges.add(tuple(sorted((right, new))))
        return new

    def generic(parent):
        self_intersections[parent] -= 1
        new = len(labels)
        labels.append(labels[parent] + 1)
        self_intersections.append(-1)
        edges.add(tuple(sorted((parent, new))))
        return new

    assert crossing(5, 7) == 8
    assert crossing(5, 8) == 9
    assert crossing(8, 9) == 10
    assert generic(8) == 11
    assert crossing(3, 4) == 12
    assert generic(2) == 13
    assert generic(9) == 14
    assert generic(0) == 15
    assert generic(13) == 16
    assert generic(8) == 17
    assert generic(1) == 18

    assert self_intersections == expected_self
    assert labels == expected_labels
    assert edges == {tuple(sorted(edge)) for edge in expected_edges}


def verify_scalar_tree_and_dual_obstruction() -> None:
    self_intersections = [
        -1, -2, -3, -4, -1, -6, -2, -3, -3, -1, -3, -1, -1, -1, -1
    ]
    labels = [-2, -1, 0, 1, 1, -1, 0, -1, -2, 2, -3, -4, 2, -3, -2]
    edges = [
        (0, 1), (0, 5), (1, 2), (2, 4), (3, 4), (3, 9), (3, 12),
        (5, 11), (6, 7), (7, 13), (8, 10), (8, 13), (10, 11),
        (10, 14),
    ]
    q_matrix = intersection_matrix(self_intersections, edges)
    b = sp.Matrix([16, 12, 8, 4, 12, 4, 1, 2, 3, 0, 4, 8, 4, 5, 1])
    y = q_matrix * b
    assert list(y) == [0] * 9 + [4] + [0] * 4 + [3]
    assert (b.T * q_matrix * b)[0] == 3
    assert all(label - 1 + 3 * multiplicity >= 0 for label, multiplicity in zip(labels, b))
    assert labels[14] == -2 * b[14] and y[14] > 0
    assert b[9] == 0 and labels[9] >= 1 and y[9] > 0
    assert b[4] + b[7] == 2 * 1 * 7
    assert labels[4] + labels[7] == 0

    # If eta is an effective boundary part of G=7P, it is supported on
    # y=0 and z=7y-Qeta must contain C at nodes 4 and 7.  The following
    # exact dual vector proves eta_4+eta_7 <= 483/5 < 98, contradicting
    # G.C=2*7^2 and C^2=0.
    dual = sp.Matrix(
        [
            2, Fraction(6, 5), Fraction(2, 5), Fraction(3, 5), 0,
            Fraction(4, 5), 0, 0, 1, Fraction(9, 5), 2,
            Fraction(14, 5), Fraction(3, 5), 1, Fraction(11, 5),
        ]
    )
    objective = sp.zeros(15, 1)
    objective[4] = objective[7] = 1
    dual_pullback = q_matrix * dual
    for index in range(15):
        if index not in (9, 14):
            assert dual_pullback[index] == objective[index]
    right_side = 7 * y - objective
    assert (dual.T * right_side)[0] == Fraction(483, 5)
    assert Fraction(483, 5) < 98


def verify_full_effective_ledger_and_finality_failure() -> None:
    self_intersections = [
        -2, -3, -4, -3, -2, -5, -2, -2, -5, -3, -1, -1, -1, -2,
        -1, -1, -1, -1, -1,
    ]
    labels = [
        -2, -1, 0, 1, 1, -1, 0, -1, -2, -3, -5, -1, 2, 1, -2,
        -1, 2, -1, 0,
    ]
    edges = [
        (0, 1), (0, 5), (0, 15), (1, 2), (1, 18), (2, 4), (2, 13),
        (3, 12), (4, 12), (5, 9), (6, 7), (7, 8), (8, 10), (8, 11),
        (8, 17), (9, 10), (9, 14), (13, 16),
    ]
    verify_full_ledger_blowup_history(self_intersections, labels, edges)
    q_matrix = intersection_matrix(self_intersections, edges)
    assert q_matrix.det() == 1

    b = sp.Matrix([16, 12, 8, 8, 16, 4, 1, 2, 3, 4, 7, 3, 24, 4, 1, 16, 0, 3, 12])
    y = sp.Matrix([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0])
    eta = sp.Matrix([138, 105, 72, 74, 147, 33, 8, 15, 21, 27, 48, 21, 221, 36, 0, 138, 0, 21, 105])
    z = sp.Matrix([0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    degree = 9
    delta = 1

    assert q_matrix * b == y
    assert (b.T * q_matrix * b)[0] == 3
    assert q_matrix * eta + z == degree * y
    assert all(eta[i] == 0 for i in range(19) if y[i] > 0)
    assert b[4] + b[7] == 2 * delta * degree
    assert eta[4] + eta[7] == 2 * delta * degree**2
    assert (b.T * z)[0] == 3 * degree
    assert (y.T * eta)[0] == 0

    ramification = sp.Matrix(
        [label - 1 + 3 * multiplicity for label, multiplicity in zip(labels, b)]
    )
    assert min(ramification) >= 0
    assert labels[14] == -2 * b[14] and y[14] == 3
    assert b[16] == 0 and labels[16] == 2 and y[16] == 4

    # C meets nodes 4,7; the single residual H meets nodes 3,6.
    # The divisor equation forces C^2=0 and H^2=-1.  Its square and
    # both adjunction/ramification ledgers are then exact.
    c_self = 0
    h_self = -1
    assert c_self + eta[4] + eta[7] == 2 * delta * degree**2
    assert h_self + eta[3] + eta[6] == degree**2
    assert ramification[4] + ramification[7] == 6 * delta * degree - 2
    assert ramification[3] + ramification[6] == -2 - h_self + 3 * degree
    total_square = (
        c_self
        + h_self
        + (eta.T * q_matrix * eta)[0]
        + 2 * (eta.T * z)[0]
    )
    assert total_square == 3 * degree**2

    # "Final" means no later blowup was centered on the exceptional
    # curve, equivalently self-intersection -1.  It is not the same as
    # being a leaf of the dual graph: a crossing blowup is born with
    # valency two.
    final_vertices = [
        i
        for i, self_intersection in enumerate(self_intersections)
        if i > 0 and self_intersection == -1
    ]
    dicriticals = {14, 16}
    bad_final_vertices = set(final_vertices) - dicriticals
    assert bad_final_vertices == {10, 11, 12, 15, 17, 18}

    # A curve-level degree-nine G_m model with the required residue.
    s, scale_a = sp.symbols("s scale_a", nonzero=True)
    scale_b = -sp.Rational(2, 3) / scale_a
    u = scale_a * s
    v = scale_b / s + scale_a**8 * s**8
    assert sp.expand(u * v - u**9 + sp.Rational(2, 3)) == 0
    residue = sp.expand(u * sp.diff(v, s)).coeff(s, -1)
    assert residue == sp.Rational(2, 3)


def main() -> None:
    verify_scalar_tree_and_dual_obstruction()
    verify_full_effective_ledger_and_finality_failure()
    print("verified the scalar compactification witness and exact G-obstruction")
    print("verified the full effective G ledger and rational residual bridge")
    print("verified the precise remaining final-boundary failure")


if __name__ == "__main__":
    main()
