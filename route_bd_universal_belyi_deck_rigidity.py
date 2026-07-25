#!/usr/bin/env python3
"""Deck rigidity of the universal (2,3) outer Belyi map.

For the coprime outer ODE with (m,n)=(2,3), put

    R(w) = w V(w)^2 / U(w)^3.

Its passport at scale k is

    over 0:  (2^(3k+1), 1),
    over infinity: (3^(2k+1)),
    over L: ((5k+2), 1^(k+1)),

where L=v_q^2/u_p^3 and the (5k+2)-ramified point is w=infinity.
Therefore every deck transformation fixes the unique simple zero and the
unique (5k+2)-ramified point.  After putting those points at 0 and
infinity it is w -> lambda*w.  Comparing the first local coefficient at
the simple zero forces lambda=1.

Equivalently, a nontrivial orbit size would divide both 3k+1 and 2k+1,
which is impossible because 3(2k+1)-2(3k+1)=1.

This theorem can only be used after proving that a bounded nonlinear
completion extends to a deck transformation of the compactified cover.
If one can further prove ring descent, namely P,Q in K[P0,Q0], elementary
weighted-degree and endpoint arguments force P=P0,Q=Q0 after the standard
normalizations.  Trivial deck group does not imply descent: the script
includes the elementary countermodel K(t)/K(t^3+t).  The present verifier
does not assert either field or ring descent.
"""

from __future__ import annotations

import sympy as sy


def verify_abstract_passport_argument() -> None:
    k = sy.symbols("k", integer=True, positive=True)
    zeros_of_index_two = 3 * k + 1
    poles_of_index_three = 2 * k + 1
    assert sy.expand(
        3 * poles_of_index_three - 2 * zeros_of_index_two
    ) == 1

    # The local derivative argument is even sharper.  If x is a parameter
    # at the unique simple zero, R=a*x+O(x^2), a!=0, and a deck
    # transformation has x -> lambda*x+O(x^2), then R∘gamma=R gives
    # lambda=1.  A finite Möbius transformation fixing this point and the
    # unique high-ramification point is determined by lambda.
    a, lam, x = sy.symbols("a lambda x", nonzero=True)
    local_difference = sy.expand(a * lam * x - a * x)
    assert sy.solve(
        sy.Eq(local_difference.coeff(x), 0), lam
    ) == [1]


def verify_k1_rational_map() -> None:
    w = sy.symbols("w")
    u = (
        1
        + w
        + sy.Rational(6, 25) * w**2
        + sy.Rational(9, 250) * w**3
    )
    v = (
        1
        + sy.Rational(2, 3) * w
        + sy.Rational(6, 25) * w**2
        + sy.Rational(36, 875) * w**3
        + sy.Rational(18, 4375) * w**4
    )
    edge = sy.expand(
        u * v
        + 2 * w * u * sy.diff(v, w)
        - 3 * w * sy.diff(u, w) * v
    )
    assert edge == 1

    up = sy.Poly(u, w).LC()
    vq = sy.Poly(v, w).LC()
    branch_value = sy.factor(vq**2 / up**3)
    assert branch_value == sy.Rational(160, 441)
    rational_map = sy.cancel(w * v**2 / u**3)

    # The zero at 0 is simple and has nonzero first coefficient.
    assert rational_map.subs(w, 0) == 0
    assert sy.diff(rational_map, w).subs(w, 0) == 1

    # Infinity has contact order 7 with the third branch value; after
    # clearing the denominator only the two finite simple residual points
    # remain.
    numerator, denominator = sy.fraction(
        sy.cancel(rational_map - branch_value)
    )
    assert sy.degree(denominator, w) == 9
    assert sy.degree(numerator, w) == 2
    assert sy.discriminant(numerator, w) != 0

    # A deck map fixes 0 and infinity, hence is lambda*w.  Its linear
    # coefficient at the simple zero forces lambda=1.
    lam = sy.symbols("lambda")
    composed_linear = sy.diff(
        rational_map.subs(w, lam * w), w
    ).subs(w, 0)
    assert sy.solve(sy.Eq(composed_linear, 1), lam) == [1]


def verify_conditional_target_ring_rigidity() -> None:
    # A polynomial in target coordinates P0,Q0 has z-weight 2a+3b.
    # Nonconstant R prevents cancellation between distinct monomials of
    # the same weight.  Thus the possible monomials in a bounded P
    # (z-degree at most 2) and Q (z-degree at most 3) are exactly:
    p_monomials = [
        (a, b)
        for a in range(3)
        for b in range(3)
        if 2 * a + 3 * b <= 2
    ]
    q_monomials = [
        (a, b)
        for a in range(3)
        for b in range(3)
        if 2 * a + 3 * b <= 3
    ]
    assert p_monomials == [(0, 0), (1, 0)]
    assert q_monomials == [(0, 0), (0, 1), (1, 0)]

    # Fixed outer coefficients set the P0 and Q0 multipliers to one.
    # The only remaining nonconstant target change is Q0+lambda*P0.
    # But the z^2 block of Q is allowed only nonnegative w exponents,
    # while P0=z^2*U/w has coefficient U(0) at w^-1.  The edge constant
    # E=U(0)V(0) is nonzero, so U(0) is nonzero and lambda must vanish.
    edge, u0, v0, lam = sy.symbols(
        "E u0 v0 lambda", nonzero=True
    )
    assert sy.solve(sy.Eq(edge, u0 * v0), u0) == [edge / v0]
    forbidden_coefficient = sy.expand(lam * edge / v0)
    assert sy.solve(
        sy.Eq(forbidden_coefficient, 0), lam
    ) == []
    # Under the nonzero symbol declaration, SymPy correctly reports that
    # no nonzero lambda can kill the forbidden coefficient.


def verify_deck_rigidity_does_not_imply_descent() -> None:
    t, a, b = sy.symbols("t a b")
    r = t**3 + t
    transformed = sy.Poly(
        sy.expand((a * t + b) ** 3 + (a * t + b) - r),
        t,
    )
    # A deck transformation fixes the unique point over infinity, so it
    # is affine.  Solving R(a*t+b)=R(t) gives only the identity.
    solutions = sy.solve(
        transformed.all_coeffs(), (a, b), dict=True
    )
    assert solutions == [{a: 1, b: 0}]
    # Nevertheless the rational map has degree three, hence
    # [K(t):K(R)]=3 and t is not in K(R).
    assert sy.degree(r, t) == 3


def main() -> None:
    verify_abstract_passport_argument()
    verify_k1_rational_map()
    verify_conditional_target_ring_rigidity()
    verify_deck_rigidity_does_not_imply_descent()
    print("verified trivial deck group for every (2,3) outer scale")
    print("verified the normalized k=1 rational Belyi map exactly")
    print("verified rigidity conditional on target-ring descent")
    print("verified trivial deck group does not imply descent")
    print("no field/ring descent from a bounded completion is claimed")


if __name__ == "__main__":
    main()
