#!/usr/bin/env python3
"""Verify the globally coupled degree-nine endpoint countermodel.

The verifier checks a genuine smooth target curve and an exact numerical
source-boundary ledger.  It does not construct the two source sections
needed for a morphism, and the checked finality failure is intentional.
"""

from fractions import Fraction

import sympy as sp


def intersection_matrix(self_intersections, edges):
    size = len(self_intersections)
    matrix = sp.diag(*self_intersections)
    for left, right in edges:
        matrix[left, right] = matrix[right, left] = 1
    return matrix


def order_at_zero(expression, parameter):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    numerator_terms = sp.Poly(numerator, parameter).as_dict()
    denominator_terms = sp.Poly(denominator, parameter).as_dict()
    numerator_order = min(exponent[0] for exponent in numerator_terms)
    denominator_order = min(exponent[0] for exponent in denominator_terms)
    return numerator_order - denominator_order


def leading_coefficient(expression, parameter):
    order = order_at_zero(expression, parameter)
    return sp.limit(expression / parameter**order, parameter, 0)


def blow_up_along_branch(x_coordinate, y_coordinate, parameter):
    """Follow the strict branch, translating away a nonzero tangent.

    The translation matters at the two satellite centers: omitting it
    would retain only the first characteristic pair and give the wrong
    final target divisor.
    """

    x_order = order_at_zero(x_coordinate, parameter)
    y_order = order_at_zero(y_coordinate, parameter)
    if x_order <= y_order:
        quotient = sp.cancel(y_coordinate / x_coordinate)
        tangent = sp.limit(quotient, parameter, 0)
        return x_coordinate, sp.cancel(quotient - tangent)

    quotient = sp.cancel(x_coordinate / y_coordinate)
    tangent = sp.limit(quotient, parameter, 0)
    return sp.cancel(quotient - tangent), y_coordinate


def verify_target_curve():
    s, X, Y = sp.symbols("s X Y", nonzero=True)
    scale = sp.Rational(2, 3)
    x_of_s = s**-2 + scale * s**-1
    y_of_s = s + x_of_s**4
    target_equation = X * (Y - X**4) ** 2 - scale * (Y - X**4) - 1

    assert sp.factor(target_equation.subs({X: x_of_s, Y: y_of_s})) == 0
    assert sp.Poly(target_equation, X, Y).total_degree() == 9

    # T is a Laurent unit in the quotient, which proves that the
    # parametrization is a closed isomorphism rather than only birational.
    T = Y - X**4
    assert sp.rem(
        sp.Poly(T * (X * T - scale) - 1, Y),
        sp.Poly(target_equation, Y),
    ) == 0
    assert sp.factor((s * x_of_s - scale) - s**-1) == 0

    liouville_residue = sp.residue(
        sp.expand(x_of_s * sp.diff(y_of_s, s)), s, 0
    )
    assert liouville_residue == scale

    poincare_coefficient = sp.factor(
        sp.diff(x_of_s, s)
        / sp.diff(target_equation, Y).subs({X: x_of_s, Y: y_of_s})
    )
    assert poincare_coefficient == -s**-2
    residue_exponent = -1
    assert poincare_coefficient == -s**residue_exponent / s

    z_at_zero = sp.factor(1 / y_of_s)
    u_at_zero = sp.factor(x_of_s / y_of_s)
    assert (
        order_at_zero(u_at_zero, s),
        order_at_zero(z_at_zero, s),
    ) == (6, 8)
    assert leading_coefficient(u_at_zero, s) == 1
    assert leading_coefficient(z_at_zero, s) == 1

    tau = sp.symbols("tau")
    u_at_infinity = sp.factor(u_at_zero.subs(s, 1 / tau))
    z_at_infinity = sp.factor(z_at_zero.subs(s, 1 / tau))
    assert (
        order_at_zero(u_at_infinity, tau),
        order_at_zero(z_at_infinity, tau),
    ) == (2, 1)
    assert leading_coefficient(u_at_infinity, tau) == scale
    assert leading_coefficient(z_at_infinity, tau) == 1

    # This exact chart replay is the trust anchor for the high branch's
    # second characteristic exponent and the satellite blowups.
    transformed_x = z_at_zero
    transformed_y = u_at_zero
    order_pairs = []
    for _ in range(10):
        order_pairs.append(
            (
                order_at_zero(transformed_x, s),
                order_at_zero(transformed_y, s),
            )
        )
        transformed_x, transformed_y = blow_up_along_branch(
            transformed_x, transformed_y, s
        )
    assert order_pairs == [
        (8, 6),
        (2, 6),
        (2, 4),
        (2, 2),
        (2, 9),
        (2, 7),
        (2, 5),
        (2, 3),
        (2, 1),
        (1, 1),
    ]

    low_triple = (1, 7, 1)
    line = (1, 0, 0)
    first_exceptional = low_triple

    def crossing(left, right, strict_multiplicity):
        return (
            left[0] + right[0],
            left[1] + right[1] + strict_multiplicity,
            left[2] + right[2] + 1,
        )

    def generic(parent, strict_multiplicity):
        return (
            parent[0],
            parent[1] + strict_multiplicity,
            parent[2] + 1,
        )

    high_triples = []
    high_triples.append(crossing(line, first_exceptional, 2))
    high_triples.append(crossing(high_triples[-1], first_exceptional, 2))
    high_triples.append(crossing(high_triples[-1], first_exceptional, 2))
    for _ in range(4):
        high_triples.append(generic(high_triples[-1], 2))
    high_triples.append(generic(high_triples[-1], 1))
    high_triples.append(crossing(high_triples[-2], high_triples[-1], 1))
    assert high_triples == [
        (2, 9, 2),
        (3, 18, 4),
        (4, 27, 6),
        (4, 29, 7),
        (4, 31, 8),
        (4, 33, 9),
        (4, 35, 10),
        (4, 36, 11),
        (8, 72, 22),
    ]
    high_triple = high_triples[-1]

    degree = 9
    assert (degree - 3) * high_triple[0] + high_triple[2] - high_triple[1] == -2
    assert (degree - 3) * low_triple[0] + low_triple[2] - low_triple[1] == 0
    high_mu = Fraction(high_triple[2] + 1 - high_triple[1], high_triple[0])
    low_mu = Fraction(low_triple[2] + 1 - low_triple[1], low_triple[0])
    assert high_mu == Fraction(-49, 8)
    assert low_mu == -5

    return {
        "degree": degree,
        "j": residue_exponent,
        "high_triple": high_triple,
        "low_triple": low_triple,
        "high_mu": high_mu,
        "low_mu": low_mu,
    }


def verify_global_source_ledger(target):
    self_intersections = [
        -2,
        -3,
        -4,
        -3,
        -2,
        -5,
        -2,
        -2,
        -5,
        -3,
        -1,
        -1,
        -1,
        -2,
        -1,
        -1,
        -1,
        -1,
        -1,
    ]
    labels = [
        -2,
        -1,
        0,
        1,
        1,
        -1,
        0,
        -1,
        -2,
        -3,
        -5,
        -1,
        2,
        1,
        -2,
        -1,
        2,
        -1,
        0,
    ]
    edges = [
        (0, 1),
        (0, 5),
        (0, 15),
        (1, 2),
        (1, 18),
        (2, 4),
        (2, 13),
        (3, 12),
        (4, 12),
        (5, 9),
        (6, 7),
        (7, 8),
        (8, 10),
        (8, 11),
        (8, 17),
        (9, 10),
        (9, 14),
        (13, 16),
    ]
    q_matrix = intersection_matrix(self_intersections, edges)
    assert q_matrix.det() == 1

    b = sp.Matrix(
        [16, 12, 8, 8, 16, 4, 1, 2, 3, 4, 7, 3, 24, 4, 1, 16, 0, 3, 12]
    )
    y = sp.Matrix(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0]
    )
    eta = sp.Matrix(
        [
            138,
            105,
            72,
            74,
            147,
            33,
            8,
            15,
            21,
            27,
            48,
            21,
            221,
            36,
            0,
            138,
            0,
            21,
            105,
        ]
    )
    z = sp.zeros(19, 1)
    for strict_contact in (3, 4, 6, 7):
        z[strict_contact] = 1

    degree = target["degree"]
    assert q_matrix * b == y
    assert (b.T * q_matrix * b)[0] == 3
    assert q_matrix * eta + z == degree * y
    assert (eta.T * y)[0] == 0
    assert min(eta) >= 0
    assert all(eta[index] == 0 for index in range(19) if y[index] > 0)
    assert (b.T * z)[0] == 3 * degree

    ramification = sp.Matrix(
        [label - 1 + 3 * multiplicity for label, multiplicity in zip(labels, b)]
    )
    sigma = degree * b - eta
    kappa = sp.Matrix(labels) + sigma
    assert min(ramification) >= 0

    # These are the only contacts relevant to the claimed target match;
    # all other ledger rows remain purely numerical and make no local
    # morphism assertion.
    contacts = [
        {
            "node": 4,
            "beta": 2,
            "triple": target["high_triple"],
            "mu": target["high_mu"],
            "expected_kappa": -2,
            "expected_theta": 3,
        },
        {
            "node": 3,
            "beta": 1,
            "triple": target["high_triple"],
            "mu": target["high_mu"],
            "expected_kappa": -1,
            "expected_theta": 2,
        },
        {
            "node": 7,
            "beta": 2,
            "triple": target["low_triple"],
            "mu": target["low_mu"],
            "expected_kappa": 2,
            "expected_theta": 1,
        },
        {
            "node": 6,
            "beta": 1,
            "triple": target["low_triple"],
            "mu": target["low_mu"],
            "expected_kappa": 1,
            "expected_theta": 1,
        },
    ]
    for contact in contacts:
        node = contact["node"]
        beta = contact["beta"]
        M, N, c_relative = contact["triple"]
        theta = eta[node] - N * beta
        assert b[node] == M * beta
        assert kappa[node] == contact["expected_kappa"]
        assert theta == contact["expected_theta"]
        assert ramification[node] == c_relative * beta + beta + theta - 1
        assert ramification[node] == eta[node] + contact["mu"] * b[node] - 1
        if node in (4, 3):
            assert kappa[node] == beta * target["j"]
        else:
            assert kappa[node] == -beta * target["j"]

    assert b[4] + b[7] == 2 * degree
    assert eta[4] + eta[7] == 2 * degree**2
    assert kappa[4] + kappa[7] == 0
    assert kappa[3] + kappa[6] == 0

    conductor_self_intersection = 0
    residual_self_intersection = -1
    assert conductor_self_intersection + eta[4] + eta[7] == 2 * degree**2
    assert residual_self_intersection + eta[3] + eta[6] == degree**2
    assert ramification[4] + ramification[7] == 6 * degree - 2
    assert (
        ramification[3] + ramification[6]
        == -2 - residual_self_intersection + 3 * degree
    )
    total_square = (
        conductor_self_intersection
        + residual_self_intersection
        + (eta.T * q_matrix * eta)[0]
        + 2 * (eta.T * z)[0]
    )
    assert total_square == 3 * degree**2

    final_vertices = {
        index
        for index, self_intersection in enumerate(self_intersections)
        if index > 0 and self_intersection == -1
    }
    dicriticals = {index for index, value in enumerate(y) if value > 0}
    assert dicriticals == {14, 16}
    assert labels[14] == -2 * b[14] and b[14] > 0
    assert b[16] == 0 and labels[16] >= 1
    assert final_vertices - dicriticals == {10, 11, 12, 15, 17, 18}


def main():
    target = verify_target_curve()
    verify_global_source_ledger(target)
    print("verified the smooth degree-nine G_m target with residue 2/3 and j=-1")
    print("verified target triples (8,72,22) and (1,7,1)")
    print("verified all four conductor/residual normal-map contacts")
    print("verified one common 19-vertex pullback ledger and its six-curve finality failure")


if __name__ == "__main__":
    main()
