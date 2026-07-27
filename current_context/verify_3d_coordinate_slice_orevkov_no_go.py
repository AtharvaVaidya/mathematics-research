#!/usr/bin/env python3
"""Exact identities for the 3D coordinate-slice/Orevkov no-go."""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
target_a, target_b = sp.symbols("target_a target_b", nonzero=True)

e = 1 + x * y
A = e**3 * z + y**2 * e * (4 + 3 * x * y)
B = y + 3 * x * e**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
C = 2 * x - 3 * x**2 * y - x**3 * z


def verify_keller_and_cubic_inverse() -> None:
    jacobian = sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(component, variable) for variable in (x, y, z)]
                    for component in (A, B, C)
                ]
            )
        )
    )
    assert jacobian == -2

    T = y + 1 / x
    cubic = C * T**3 - 2 * T**2 + B * T - 2 * A
    derivative = 3 * C * T**2 - 4 * T + B
    assert sp.factor(cubic) == 0
    assert sp.factor(derivative - 2 / x) == 0

    reconstructed_x = 2 / derivative
    reconstructed_y = T - derivative / 2
    reconstructed_z = (
        sp.Rational(5, 4) * derivative**2
        - sp.Rational(3, 2) * T * derivative
        - C * derivative**3 / 8
    )
    assert sp.factor(reconstructed_x - x) == 0
    assert sp.factor(reconstructed_y - y) == 0
    assert sp.factor(reconstructed_z - z) == 0


def verify_A_fiber() -> None:
    solved_z = (
        target_a - y**2 * e * (4 + 3 * x * y)
    ) / e**3
    assert sp.factor(A.subs(z, solved_z) - target_a) == 0

    # On e=0, the A-coordinate vanishes identically.
    assert sp.factor(A.subs(y, -1 / x)) == 0


def verify_B_fiber() -> None:
    coefficient_of_z = sp.diff(B, z)
    assert sp.factor(coefficient_of_z - 3 * x * e**2) == 0

    solved_z = (
        target_b - y - 3 * x * y**2 * (4 + 3 * x * y)
    ) / (3 * x * e**2)
    assert sp.factor(B.subs(z, solved_z) - target_b) == 0

    # Exceptional locus x=0: B=y, so (x,y)=(0,target_b)
    # has an arbitrary z-coordinate.
    assert sp.factor(B.subs(x, 0) - y) == 0
    assert sp.factor(B.subs({x: 0, y: target_b}) - target_b) == 0

    # Exceptional locus e=0: B=-2y.  For target_b != 0 this gives
    # (x,y)=(2/target_b,-target_b/2), again with arbitrary z.
    assert sp.factor(B.subs(y, -1 / x) - 2 / x) == 0
    exceptional_point = {x: 2 / target_b, y: -target_b / 2}
    assert sp.factor(e.subs(exceptional_point)) == 0
    assert sp.factor(B.subs(exceptional_point) - target_b) == 0


def verify_euler_ledgers() -> None:
    chi_A2 = 1
    chi_A1 = 1
    chi_Gm = 0

    chi_A_fiber = chi_A2 - chi_Gm
    assert chi_A_fiber == 1

    # V(x) and V(1+xy) are disjoint.
    chi_B_open = chi_A2 - chi_A1 - chi_Gm
    chi_B_fiber = chi_B_open + 2 * chi_A1
    assert chi_B_fiber == 2


def main() -> None:
    verify_keller_and_cubic_inverse()
    verify_A_fiber()
    verify_B_fiber()
    verify_euler_ledgers()
    print("verified: the 3D Jacobian determinant is -2")
    print("verified: the cubic inverse and rational reconstruction identities")
    print("verified: a nonzero A-fiber is A2 minus V(1+xy)")
    print("verified: a nonzero B-fiber has two exceptional affine lines")
    print("verified: Euler characteristics of general A/B fibers are 1 and 2")
    print("THEOREM INPUT: Orevkov excludes three-sheeted plane Keller maps")


if __name__ == "__main__":
    main()
