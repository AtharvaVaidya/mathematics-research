#!/usr/bin/env python3
"""Verify the global defect Green identities and local counterledger."""

import sympy as sp


def verify_conductor_and_component_identities() -> None:
    d, delta, q = sp.symbols("d delta q", integer=True, positive=True)
    b_sum = 2 * delta * d
    eta_sum = 2 * delta * d**2 + q
    assert sp.expand(d * b_sum - eta_sum) == -q

    # The q=0 endpoints in the 19-vertex ledger.
    b4, b7 = 16, 2
    eta4, eta7 = 147, 15
    assert (9 * b4 - eta4) + (9 * b7 - eta7) == 0


def verify_green_kernel() -> None:
    q_subtree = sp.Matrix([[-2, 1], [1, -2]])
    green = (-q_subtree).inv()
    assert green == sp.Matrix(
        [
            [sp.Rational(2, 3), sp.Rational(1, 3)],
            [sp.Rational(1, 3), sp.Rational(2, 3)],
        ]
    )
    assert all(entry > 0 for entry in green)

    # Two boundary attachments both meet the second point vertex.
    incidence = sp.Matrix([[0, 0], [1, 1]])
    attachment_defect = sp.Matrix([2, 1])
    strict_incidence = sp.Matrix([3, 0])
    interior_defect = green * (
        incidence * attachment_defect - strict_incidence
    )
    assert interior_defect == sp.Matrix([-1, 1])


def verify_local_finality_counterledger() -> None:
    # Order: old attachment E0, then E1,E2,E3.
    q_local = sp.diag(0, -2, -2, -1)
    for left, right in [(0, 2), (1, 2), (2, 3)]:
        q_local[left, right] = q_local[right, left] = 1

    labels = [-2, -1, -3, -2]
    b = sp.Matrix([2, 1, 2, 1])
    defect = sp.Matrix([2, -1, 1, 1])
    eta = b - defect

    assert list((q_local * b)[1:]) == [0, 0, 1]
    assert list((q_local * defect)[1:]) == [3, 0, 0]
    assert list(eta) == [0, 2, 1, 0]
    assert all(value >= 0 for value in eta)

    # The sole new final curve E3 is type 1.
    assert labels[3] == -2 * b[3]
    assert (q_local * b)[3] == 1
    assert eta[3] == 0
    ramification = [
        labels[index] - 1 + 3 * b[index]
        for index in range(1, 4)
    ]
    assert ramification == [1, 2, 0]
    assert defect[1] == -1


def main() -> None:
    verify_conductor_and_component_identities()
    verify_green_kernel()
    verify_local_finality_counterledger()
    print("verified the conductor defect budget sigma_alpha+sigma_beta=-q")
    print("verified the positive point-subtree Green kernel")
    print("verified the exact finality-compatible negative-defect counterledger")


if __name__ == "__main__":
    main()
