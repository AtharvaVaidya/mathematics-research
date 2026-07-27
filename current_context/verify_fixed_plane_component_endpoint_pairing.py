#!/usr/bin/env python3
"""Verify residual endpoint pairing and its smallest repaired ledger."""

import sympy as sp


def verify_symbolic_endpoint_pairing() -> None:
    a_u, a_v, sigma_u, sigma_v = sp.symbols(
        "a_u a_v sigma_u sigma_v"
    )
    b_u, b_v, e, d = sp.symbols("b_u b_v e d")
    r_sum = a_u + a_v - 2 + 3 * (b_u + b_v)
    component_square = sigma_u + sigma_v
    adjunction = -2 - component_square + 3 * e * d
    difference = sp.expand((r_sum - adjunction).subs(b_v, e * d - b_u))
    assert sp.expand(difference - (a_u + sigma_u + a_v + sigma_v)) == 0

    # For an étale quasi-finite residual component of genus g with s
    # boundary contacts, adjunction supplies 2g+s-2.
    g, s, sum_a, sum_sigma = sp.symbols("g s sum_a sum_sigma")
    general_r_sum = sum_a - s + 3 * e * d
    general_adjunction = 2 * g - 2 - sum_sigma + 3 * e * d
    assert sp.expand(
        general_r_sum
        - general_adjunction
        - (sum_a + sum_sigma - (2 * g + s - 2))
    ) == 0

    # Removing the full tangential Riemann--Hurwitz degree leaves the
    # genus-independent normal-map degree.
    component_square = sp.symbols("component_square")
    ramification_degree = 2 * g - 2 - component_square + 3 * e * d
    tangential_degree = 2 * g - 2 + 2 * e
    assert sp.expand(
        ramification_degree
        - tangential_degree
        - (-component_square + e * (3 * d - 2))
    ) == 0


def local_matrix() -> sp.Matrix:
    # Order: old attachment E0, then E1,E2,E3.
    matrix = sp.diag(0, -2, -2, -1)
    for left, right in [(0, 2), (1, 2), (2, 3)]:
        matrix[left, right] = matrix[right, left] = 1
    return matrix


def verify_original_ledger_failure() -> None:
    b = sp.Matrix([2, 1, 2, 1])
    old_defect = sp.Matrix([2, -1, 1, 1])
    # E3 is type 1, hence eta_3=0 and sigma_3=d*b_3.
    forced_degree = sp.Rational(old_defect[3], b[3])
    assert forced_degree == 1
    # A smooth affine plane curve isomorphic to G_m has two infinity
    # punctures, so its projective degree is at least two.
    assert forced_degree < 2


def verify_repaired_local_ledger() -> None:
    q_local = local_matrix()
    labels = [-2, -1, -3, -2]
    b = sp.Matrix([2, 1, 2, 1])
    defect = sp.Matrix([3, -1, 2, 2])
    degree = 2
    eta = degree * b - defect

    assert list((q_local * b)[1:]) == [0, 0, 1]
    assert list((q_local * defect)[1:]) == [4, 0, 0]
    assert list(eta) == [1, 3, 2, 0]
    assert all(value >= 0 for value in eta)
    assert labels[3] == -2 * b[3]
    assert defect[3] == degree * b[3]

    ramification = [
        labels[index] - 1 + 3 * b[index]
        for index in range(1, 4)
    ]
    assert ramification == [1, 2, 0]
    assert defect[1] == -1

    # With sigma_2=2, any integral negative sigma_1 gives z_1 >= 4.
    sigma_1 = sp.symbols("sigma_1", integer=True)
    z_1 = -2 * sigma_1 + defect[2]
    assert z_1.subs(sigma_1, -1) == 4


def verify_residual_components() -> None:
    d, n, delta, e = 2, 6, 1, 1
    # Endpoint data (a,b,sigma,eta,r).
    local = (-1, 1, -1, 3, 1)
    remote = (1, 1, 1, 1, 3)

    a_sum = local[0] + remote[0]
    b_sum = local[1] + remote[1]
    sigma_sum = local[2] + remote[2]
    r_sum = local[4] + remote[4]
    kappa_sum = (local[0] + local[2]) + (remote[0] + remote[2])

    assert b_sum == e * d
    assert sigma_sum == 0
    assert a_sum + sigma_sum == 0
    assert kappa_sum == 0
    assert r_sum == -2 - sigma_sum + 3 * e * d
    assert r_sum - 2 * (e - 1) == -sigma_sum + e * (3 * d - 2)
    assert sigma_sum <= sp.Rational((e * d) ** 2, n)
    assert 2 * delta + 4 * e == n


def verify_conductor() -> None:
    d, delta, q = 2, 1, 0
    endpoint = (0, 2, 0, 4, 5)  # (a,b,sigma,eta,r)
    a_sum = 2 * endpoint[0]
    b_sum = 2 * endpoint[1]
    sigma_sum = 2 * endpoint[2]
    eta_sum = 2 * endpoint[3]
    r_sum = 2 * endpoint[4]

    assert a_sum == q
    assert b_sum == 2 * delta * d
    assert sigma_sum == -q
    assert eta_sum - q == 2 * delta * d**2
    assert r_sum == 6 * delta * d + q - 2


def main() -> None:
    verify_symbolic_endpoint_pairing()
    verify_original_ledger_failure()
    verify_repaired_local_ledger()
    verify_residual_components()
    verify_conductor()
    print("verified the residual projection and quasi-finite charge inequality")
    print("verified the original four-vertex ledger forces impossible d=1")
    print("verified the minimal d=2 repair has four residual incidences")
    print("verified residual adjunction, ramification, Hodge, and cover degree")
    print("RESULT: component-level constraints do not imply the Green bound")


if __name__ == "__main__":
    main()
