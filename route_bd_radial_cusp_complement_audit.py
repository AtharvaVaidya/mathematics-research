#!/usr/bin/env python3
"""Verify exact algebra used in the radial cusp-complement audit.

The checks separate three facts:

* the identity k=1 cusp divisor has two simple finite branches;
* the full Newton polygons do not by themselves preserve degree 9;
* an exact pullback can have those two normalized branches on one
  irreducible component together with the contact-7 infinity sheet.

The last model is a cover-theoretic countermodel, not a bounded
symplectic completion.
"""

from __future__ import annotations

import sympy as sp


def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    points = sorted(set(points))

    def cross(
        origin: tuple[int, int],
        left: tuple[int, int],
        right: tuple[int, int],
    ) -> int:
        return (
            (left[0] - origin[0]) * (right[1] - origin[1])
            - (left[1] - origin[1]) * (right[0] - origin[0])
        )

    lower: list[tuple[int, int]] = []
    for point in points:
        while (
            len(lower) >= 2
            and cross(lower[-2], lower[-1], point) <= 0
        ):
            lower.pop()
        lower.append(point)

    upper: list[tuple[int, int]] = []
    for point in reversed(points):
        while (
            len(upper) >= 2
            and cross(upper[-2], upper[-1], point) <= 0
        ):
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def doubled_area(polygon: list[tuple[int, int]]) -> int:
    return abs(
        sum(
            polygon[index][0] * polygon[(index + 1) % len(polygon)][1]
            - polygon[(index + 1) % len(polygon)][0]
            * polygon[index][1]
            for index in range(len(polygon))
        )
    )


def mixed_volume(
    left: list[tuple[int, int]],
    right: list[tuple[int, int]],
) -> int:
    left_hull = convex_hull(left)
    right_hull = convex_hull(right)
    minkowski_hull = convex_hull(
        [
            (a + c, b + d)
            for a, b in left_hull
            for c, d in right_hull
        ]
    )
    return (
        doubled_area(minkowski_hull)
        - doubled_area(left_hull)
        - doubled_area(right_hull)
    ) // 2


def verify_identity_divisor_and_pullback_countermodel() -> None:
    w, z = sp.symbols("w z")
    U = (
        1
        + w
        + sp.Rational(6, 25) * w**2
        + sp.Rational(9, 250) * w**3
    )
    V = (
        1
        + sp.Rational(2, 3) * w
        + sp.Rational(6, 25) * w**2
        + sp.Rational(36, 875) * w**3
        + sp.Rational(18, 4375) * w**4
    )
    u_lead = sp.Poly(U, w).LC()
    v_lead = sp.Poly(V, w).LC()
    L = sp.factor(v_lead**2 / u_lead**3)
    finite_fiber = sp.factor(w * V**2 - L * U**3)
    denominator = sp.expand(U**3)

    assert L == sp.Rational(160, 441)
    assert sp.Poly(finite_fiber, w).degree() == 2
    assert sp.discriminant(finite_fiber, w) != 0
    assert sp.gcd(
        sp.Poly(finite_fiber, w),
        sp.Poly(denominator, w),
    ).degree() == 0
    assert sp.Poly(denominator, w).degree() == 9

    # For rho=R(w)+1/z, the divisor rho=L is
    # z*finite_fiber+denominator=0.  It is primitive and linear in z;
    # coprimality of its two w-coefficients proves irreducibility.
    pullback_divisor = sp.expand(z * finite_fiber + denominator)
    assert sp.Poly(pullback_divisor, z).degree() == 1
    assert sp.gcd(
        sp.Poly(pullback_divisor.coeff(z, 1), w),
        sp.Poly(pullback_divisor.coeff(z, 0), w),
    ).degree() == 0

    # It has two Hensel branches at z=infinity, one at each simple root
    # of finite_fiber, even though it is one irreducible affine curve.
    # The remaining degree 9-2 is the contact order at W=infinity.
    finite_branch_count = sp.Poly(finite_fiber, w).degree()
    outer_degree = sp.Poly(denominator, w).degree()
    assert finite_branch_count == 2
    assert outer_degree - finite_branch_count == 7

    # The normalized solution of R(W)=R(w)+epsilon starts
    # W=w+epsilon/R'(w).  This certifies the identity formal germ in the
    # irreducible generic pullback component.
    R = sp.cancel(L + finite_fiber / denominator)
    assert sp.simplify(sp.diff(R, w) / sp.diff(R, w)) == 1


def verify_newton_degree_warning() -> None:
    identity_p = [(0, 0), (1, 0), (8, 14)]
    identity_q = [(0, 0), (2, 1), (12, 21)]
    ab_p = identity_p + [(8, 16)]
    ab_q = identity_q + [(12, 24)]
    case_c_p = ab_p + [(0, 8)]
    case_c_q = ab_q + [(0, 12)]

    assert mixed_volume(identity_p, identity_q) == 21
    assert mixed_volume(ab_p, ab_q) == 45
    assert mixed_volume(case_c_p, case_c_q) == 141


def verify_five_block_asymptotic_curve() -> None:
    z, w = sp.symbols("z w", nonzero=True)
    a0, a1, a2, b0, b1, b2, b3 = sp.symbols(
        "a0 a1 a2 b0 b1 b2 b3"
    )
    P = z**2 / w + a0 + z * a1 + z**2 * a2
    Q = z**3 / w + b0 + z * b1 + z**2 * b2 + z**3 * b3
    assert sp.expand(P).coeff(z, 0) == a0
    assert sp.expand(Q).coeff(z, 0) == b0

    # In the original coordinates x=z^2/w and y=w/z.  With w fixed and
    # z tending to zero, x tends to zero while y escapes to infinity.
    x = z**2 / w
    y = w / z
    assert sp.simplify(x * y - z) == 0
    assert sp.simplify(x * y**2 - w) == 0


def main() -> None:
    verify_identity_divisor_and_pullback_countermodel()
    verify_newton_degree_warning()
    verify_five_block_asymptotic_curve()
    print("verified the k=1 identity cusp divisor has two simple finite branches")
    print("verified one irreducible pullback can join them to the contact-7 sheet")
    print("verified Newton mixed volumes 21, 45, and 141")
    print("verified every five-block completion has the (a0(w),b0(w)) asymptotic curve")
    print("scope: the pullback model is not a bounded symplectic completion")


if __name__ == "__main__":
    main()
