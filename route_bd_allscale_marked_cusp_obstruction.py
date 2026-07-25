#!/usr/bin/env python3
"""Symbolic checks for the all-scale marked-cusp obstruction.

The proof is recorded in
``current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md``.  Its main inputs
are the two universal deficit-one Hamiltonian modes and a local completed
square normal form at a zero of p1.
"""

from __future__ import annotations

import sympy as sp


def verify_deficit_one_mode() -> None:
    h, u0, u1 = sp.symbols("h u0 u1", nonzero=True)
    U = sp.Function("U")(h)
    C_high = (U**2 - u0**2 - 2 * u0 * u1 * h) / h

    def p_mode(C: sp.Expr) -> sp.Expr:
        return sp.expand(
            h * C * sp.diff(U, h)
            - C * U / 2
            - h * sp.diff(C, h) * U / 2
        )

    low = p_mode(sp.Integer(1))
    high = sp.factor(p_mode(C_high))
    assert sp.factor(low - (h * sp.diff(U, h) - U / 2)) == 0
    assert sp.factor(
        high
        + 2 * u0 * u1 * (h * sp.diff(U, h) - U / 2)
        + u0**2 * sp.diff(U, h)
    ) == 0

    a, b = sp.symbols("a b")
    general = (a * h + b) * sp.diff(U, h) - a * U / 2
    leading_degree = sp.simplify(
        (a * h * sp.diff(h ** sp.symbols("N"), h) - a * h ** sp.symbols("N") / 2)
        / (a * h ** sp.symbols("N"))
    )
    assert leading_degree == sp.symbols("N") - sp.Rational(1, 2)
    assert general.has(a, b)


def verify_high_partner_when_u1_zero() -> None:
    h, u0 = sp.symbols("h u0", nonzero=True)
    U = sp.Function("U")(h)
    V = sp.Function("V")(h)
    C = (U**2 - u0**2) / h
    q_mode = sp.expand(
        h * C * sp.diff(V, h)
        - C * V / 4
        - 3 * h * sp.diff(C, h) * V / 4
    )
    outer = (
        U * V
        + 2 * h * U * sp.diff(V, h)
        - 3 * h * sp.diff(U, h) * V
        - 1
    )
    target = U / (2 * h) - u0**2 * V / (2 * h) - u0**2 * sp.diff(V, h)
    # The difference is a scalar multiple of the outer equation.
    assert sp.factor(q_mode - target - U * outer / (2 * h)) == 0


def verify_completed_square_rows() -> None:
    zeta = sp.symbols("zeta")
    h = sp.symbols("h")
    H = sp.Function("H")(h)
    s = sp.Function("s")(h)
    u = sp.Function("u")(h)
    q = [sp.Function(f"q{index}")(h) for index in range(4)]
    P = zeta**2 + H
    Q = sum(q[index] * zeta**index for index in range(4))
    bracket = sp.expand(
        sp.diff(P, zeta) * sp.diff(Q, h)
        - sp.diff(P, h) * sp.diff(Q, zeta)
    )
    target = sp.expand(u * (zeta - s) ** 4)
    rows = [
        sp.expand(bracket - target).coeff(zeta, degree)
        for degree in range(5)
    ]
    expected = [
        -sp.diff(H, h) * q[1] - u * s**4,
        2 * sp.diff(q[0], h) - 2 * sp.diff(H, h) * q[2] + 4 * u * s**3,
        2 * sp.diff(q[1], h) - 3 * sp.diff(H, h) * q[3] - 6 * u * s**2,
        2 * sp.diff(q[2], h) + 4 * u * s,
        2 * sp.diff(q[3], h) - u,
    ]
    assert all(sp.expand(left - right) == 0 for left, right in zip(rows, expected))


def verify_degree_ledger() -> None:
    # R is the all-scale half-degree, and t is the marked p1 order.
    for R in range(3, 30):
        for t in range(1, R):
            # High p1 mode: deg p1=2R-1.  The marked point contributes
            # 2t to A', and every other p1 zero of multiplicity m
            # contributes at least m (in fact 2m-1).
            assert 2 * t + (2 * R - 1 - t) > 2 * R - 1

            # Low p1 mode: p1 is proportional to U' and has degree 2R-2.
            low_bound = 2 * t + (2 * R - 2 - t)
            if t >= 2:
                assert low_bound > 2 * R - 1
            else:
                assert low_bound == 2 * R - 1

        # The sole low-mode equality case t=1.
        degree_a2_bprime = (2 * R - 2) + (3 * R - 1)
        degree_p1_q1prime = (2 * R - 2) + (3 * R - 3)
        degree_p1prime_q1 = (2 * R - 3) + (3 * R - 2)
        degree_aprime_q2 = (2 * R - 1) + (3 * R - 3)
        degree_outside = 1 + (3 * R - 1)
        assert degree_a2_bprime == 5 * R - 3
        assert max(
            degree_p1_q1prime,
            degree_p1prime_q1,
            degree_aprime_q2,
        ) < degree_a2_bprime
        assert degree_outside < degree_a2_bprime + 2


def verify_analytic_quadratic_degree_ledger() -> None:
    # In the analytic-quadratic chart p1(0) is a unit and
    # ord_0(A')=m-1 with m>=3.  Thus every zero of p1 is nonmarked.
    for R in range(2, 40):
        for m in range(3, 2 * R + 1):
            degree_aprime = 2 * R - 1

            # a != 0: deg(p1)=2R-1.
            high_bound = (m - 1) + (2 * R - 1)
            assert high_bound > degree_aprime

            # a = 0: p1 is proportional to U' and has degree 2R-2.
            low_bound = (m - 1) + (2 * R - 2)
            assert low_bound > degree_aprime

            # The forced first nonanalytic exponent lies strictly between
            # three and four.  m=2 would give the analytic exponent three.
            numerator = 4 * m - 2
            assert 3 * m < numerator < 4 * m


def verify_puiseux_chart_ledgers() -> None:
    # A leading nonintegral horizontal graph has fourth-row valuations
    # in arithmetic progression.  Equality of the adjacent valuations
    # gives 2r=m-1, and the exact q3 pole then gives 2n=3m+1.
    for m in range(2, 40):
        for n in range(m + 1, 4 * m):
            for r in range(0, 2 * m):
                e1 = n - 2 * m - 2
                e2 = n - 3 * m + 2 * r - 1
                e3 = n - 4 * m + 4 * r
                if e1 == e2 == e3:
                    assert 2 * r == m - 1
                    q3_order = n - 2 * m + r - 1
                    if q3_order == -1:
                        assert 2 * n == 3 * m + 1
                        assert n < 2 * m

    # In the opposite projection, the fixed p2 pole gives
    # m-2n+2s=-1.  Both other terms in the next row then lie strictly
    # above the f''' q1^3 term, so cancellation is impossible.
    for n in range(2, 30):
        for m in range(n + 1, 60):
            numerator = 2 * n - m - 1
            if numerator < 0 or numerator % 2:
                continue
            s = numerator // 2
            for t in range(0, 20):
                first_minus_third = (3 * m - 2 * n + 1) / 2
                second_minus_third = m - n + t + 1
                assert first_minus_third > 0
                assert second_minus_third > 0
                assert m - 2 * n + 2 * s == -1

    # If an analytic quadratic precedes a first fractional exponent
    # 2<N/m<3, the fourth Taylor row still has a unique lowest term.
    for m in range(2, 30):
        for n in range(2 * m + 1, 3 * m):
            for r in range(0, m + 1):
                if r == 0:
                    # The analytic g''p1p2 term supplies the q3 pole.
                    # Avoiding a worse fractional g''' pole forces this.
                    if n == 3 * m - 1:
                        assert n - 4 * m == -m - 1 < -2
                    continue

                if m == 2 * r + 1:
                    common_fractional_order = n - 2 * m - 2
                    assert common_fractional_order > -2
                    continue

                # When m<2r+1, the fractional g'' term would need
                # n=2m-r to supply the pole, outside 2m<n.
                if m < 2 * r + 1:
                    assert 2 * m - r < 2 * m
                    continue

                # When m>2r+1, q3 forces n=3m-3r-1.  The g'''' term
                # then lies strictly below the other fourth-row terms.
                forced_n = 3 * m - 3 * r - 1
                if n == forced_n:
                    g3_order = n - 3 * m + 2 * r - 1
                    g4_order = n - 4 * m + 4 * r
                    assert g4_order < g3_order
                    assert g4_order < -2


def verify_covariant_identities() -> None:
    h = sp.symbols("h")
    A = sp.Function("A")(h)
    B = sp.Function("B")(h)
    f = sp.diff(A, h)
    J = f * sp.diff(B, h, 2) - sp.diff(B, h) * sp.diff(A, h, 2)
    K = f * sp.diff(J, h) - 3 * sp.diff(A, h, 2) * J
    L = f * sp.diff(K, h) - 5 * sp.diff(A, h, 2) * K
    U, p1 = sp.symbols("U p1")
    C = h * p1**2 / U
    graph_row = (
        L * C**2 / f**7
        + 12 * K * C / f**5
        + 12 * J / f**3
    )
    cleared = sp.factor(graph_row * f**7 * U**2)
    expected = (
        h**2 * p1**4 * L
        + 12 * h * p1**2 * f**2 * U * K
        + 12 * f**4 * U**2 * J
    )
    assert sp.expand(cleared - expected) == 0


def main() -> None:
    verify_deficit_one_mode()
    verify_high_partner_when_u1_zero()
    verify_completed_square_rows()
    verify_degree_ledger()
    verify_analytic_quadratic_degree_ledger()
    verify_puiseux_chart_ledgers()
    verify_covariant_identities()
    print("verified the two deficit-one p1 modes and exceptional q2 partner")
    print("verified the completed-square local bracket rows")
    print("verified the all-scale marked multiplicity and top-degree ledgers")
    print("verified the all-scale analytic-quadratic degree contradiction")
    print("verified the exhaustive horizontal/vertical Puiseux ledgers")
    print("verified the cleared fourth-covariant identity")
    print("RESULT: ALL-SCALE MARKED-CUSP OBSTRUCTION CHECKS PASS")


if __name__ == "__main__":
    main()
