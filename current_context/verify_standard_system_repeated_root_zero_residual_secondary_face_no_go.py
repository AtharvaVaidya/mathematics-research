#!/usr/bin/env python3
"""Exact checks for the zero-residual secondary-face no-go."""

from __future__ import annotations

import math
from itertools import product

import sympy as sp


t, y = sp.symbols("t y")


def transformed_bracket(
    p: sp.Expr,
    q: sp.Expr,
    a: int | sp.Expr,
    b: int | sp.Expr,
    G: int | sp.Expr,
) -> sp.Expr:
    return sp.expand(
        t
        * (
            sp.diff(p, y) * sp.diff(q, t)
            - sp.diff(p, t) * sp.diff(q, y)
        )
        + a * G * p * sp.diff(q, y)
        - b * G * q * sp.diff(p, y)
    )


# The first chart has the claimed transformed operator and forcing
# exponent.
tau, s = sp.symbols("tau s")
a_s, b_s, g_s, e_s, h_s, d_s = sp.symbols(
    "a b g e h d", integer=True, positive=True
)
p_fun = sp.Function("p")(t, y)
q_fun = sp.Function("q")(t, y)
G_s = h_s * g_s - e_s * d_s

# Verify the chain rule on generic functions after expressing the
# original derivatives as differential operators in (t,y).
P_tilde = t ** (a_s * e_s * d_s) * p_fun
Q_tilde = t ** (b_s * e_s * d_s) * q_fun


def ds(expr: sp.Expr) -> sp.Expr:
    return t ** (-d_s) * sp.diff(expr, y)


def tau_dtau(expr: sp.Expr) -> sp.Expr:
    return (
        t * sp.diff(expr, t) - d_s * y * sp.diff(expr, y)
    ) / h_s


original_in_chart = sp.expand(
    ds(P_tilde) * tau_dtau(Q_tilde)
    - tau_dtau(P_tilde) * ds(Q_tilde)
    + a_s * g_s * P_tilde * ds(Q_tilde)
    - b_s * g_s * Q_tilde * ds(P_tilde)
)
expected_in_chart = (
    t ** ((a_s + b_s) * e_s * d_s - d_s)
    / h_s
    * (
        t
        * (
            sp.diff(p_fun, y) * sp.diff(q_fun, t)
            - sp.diff(p_fun, t) * sp.diff(q_fun, y)
        )
        + a_s * G_s * p_fun * sp.diff(q_fun, y)
        - b_s * G_s * q_fun * sp.diff(p_fun, y)
    )
)
assert sp.simplify(original_in_chart - expected_in_chart) == 0


# Matched-face Wronskian.
A0, A1, A2, B0, B1, B2 = sp.symbols(
    "A0 A1 A2 B0 B1 B2"
)
xi_symbol = sp.symbols("xi")
for a0, b0, f0, G0, D0, H0 in (
    (2, 3, 1, 5, 7, 2),
    (3, 5, 2, 7, 4, 3),
    (4, 7, 3, 11, 9, 5),
):
    xi = t**D0 / y**H0
    A_template = A0 + A1 * xi_symbol + A2 * xi_symbol**2
    B_template = B0 + B1 * xi_symbol + B2 * xi_symbol**2
    A_poly = A_template.subs(xi_symbol, xi)
    B_poly = B_template.subs(xi_symbol, xi)
    p_face = y ** (a0 * f0) * A_poly
    q_face = y ** (b0 * f0) * B_poly
    expected = (
        (D0 - sp.Rational(G0 * H0, f0))
        * y ** (f0 * (a0 + b0) - 1)
        * xi
        * (
            a0
            * f0
            * A_poly
            * sp.diff(B_template, xi_symbol).subs(xi_symbol, xi)
            - b0
            * f0
            * sp.diff(A_template, xi_symbol).subs(
                xi_symbol, xi
            )
            * B_poly
        )
    )
    assert sp.cancel(
        transformed_bracket(p_face, q_face, a0, b0, G0)
        - expected
    ) == 0


# The arbitrary-anchor formula, checked at several independent exact
# integer specializations (symbolic powers with symbolic exponents do
# not simplify reliably in SymPy).
AA = 1 + 2 * xi_symbol + 3 * xi_symbol**2
BB = 1 + 5 * xi_symbol + 7 * xi_symbol**2
for (
    r0,
    u0,
    s0,
    v0,
    D0,
    H0,
    a0,
    b0,
    G0,
) in (
    (2, 9, 3, 11, 4, 2, 2, 3, 5),
    (5, 13, 1, 8, 3, 1, 3, 5, 7),
    (1, 7, 6, 15, 5, 3, 4, 7, 2),
):
    xi_general = t**D0 / y**H0
    p_anchor = t**r0 * y**u0 * AA.subs(
        xi_symbol, xi_general
    )
    q_anchor = t**s0 * y**v0 * BB.subs(
        xi_symbol, xi_general
    )
    C0 = u0 * (s0 - b0 * G0) - v0 * (r0 - a0 * G0)
    CB = u0 * D0 + H0 * (r0 - a0 * G0)
    CA = H0 * (b0 * G0 - s0) - D0 * v0
    anchor_expected = (
        t ** (r0 + s0)
        * y ** (u0 + v0 - 1)
        * (
            C0 * AA * BB
            + CB * xi_symbol * AA * sp.diff(BB, xi_symbol)
            + CA * xi_symbol * sp.diff(AA, xi_symbol) * BB
        ).subs(xi_symbol, xi_general)
    )
    assert sp.cancel(
        transformed_bracket(
            p_anchor, q_anchor, a0, b0, G0
        )
        - anchor_expected
    ) == 0


# Every arbitrary-anchor scalar term comes from residual orders zero
# and one.  At H=1, the top-top coefficient is zero and only the two
# next-to-top pairs remain.
for u0, v0, H0 in product(range(18), range(18), range(1, 12)):
    scalar_numerator = u0 + v0 - 1
    if scalar_numerator < 0 or scalar_numerator % H0:
        continue
    J0 = scalar_numerator // H0
    alpha0 = u0 // H0
    beta0 = v0 // H0
    if J0 > alpha0 + beta0:
        continue
    pairs0 = [
        (i, J0 - i)
        for i in range(alpha0 + 1)
        if 0 <= J0 - i <= beta0
    ]
    residual_pairs = {
        (u0 - H0 * i, v0 - H0 * j) for i, j in pairs0
    }
    if H0 == 1:
        assert residual_pairs
        assert residual_pairs <= {(0, 1), (1, 0)}
    else:
        assert len(pairs0) == 1
        assert next(iter(residual_pairs)) in {(0, 1), (1, 0)}


# Pullback endpoint classification in the original reciprocal
# operator.
for n0 in range(2, 20):
    for m0 in range(2, 20):
        forcing0 = n0 + m0 - 2
        nonzero_endpoints = []
        for epsilon_p, epsilon_q in ((0, 1), (1, 0)):
            for I0 in range(n0 + 1):
                J0 = forcing0 - I0
                if J0 < 0 or J0 > m0:
                    continue
                if I0 + epsilon_p > n0:
                    continue
                if J0 + epsilon_q > m0:
                    continue
                coefficient = (
                    epsilon_p * (J0 - m0)
                    + epsilon_q * (n0 - I0)
                )
                if coefficient:
                    nonzero_endpoints.append(
                        (I0, J0, epsilon_p, epsilon_q)
                    )
        assert {
            endpoint[:2] for endpoint in nonzero_endpoints
        } == {(n0 - 1, m0 - 1)}


# Polynomiality plus the scalar exponent forces complementary
# remainders 0 and 1 for H>1.  At H=1 both remainders vanish and the
# scalar Wronskian coefficient is one degree below the cancelling top.
for aa, bb, ff, HH in product(
    range(2, 13), range(3, 17), range(1, 10), range(1, 40)
):
    if not aa < bb or math.gcd(aa, bb) != 1:
        continue
    numerator = ff * (aa + bb) - 1
    if numerator % HH:
        continue
    JJ = numerator // HH
    if JJ > aa * ff // HH + bb * ff // HH:
        continue
    remainders = sorted((aa * ff % HH, bb * ff % HH))
    if HH == 1:
        assert remainders == [0, 0]
        assert JJ == aa * ff + bb * ff - 1
        # The formal top coefficient cancels; the next coefficient
        # can only use one of the two top indices.
        contributing_pairs = [
            (i, JJ - i)
            for i in range(aa * ff + 1)
            if 0 <= JJ - i <= bb * ff
        ]
        assert contributing_pairs == [
            (aa * ff - 1, bb * ff),
            (aa * ff, bb * ff - 1),
        ]
    else:
        assert remainders == [0, 1]
        assert math.gcd(ff, HH) == 1
        assert (aa % HH == 0) ^ (bb % HH == 0)


# A bounded exhaustive audit of all scalar arithmetic.  Under the
# occupied-support integrality q_* in Z:
#   * strict cases contradict e<=g,
#   * resonant cases have zero prefactor,
#   * super cases violate the top reciprocal degree bound.
counts = {"strict": 0, "resonant": 0, "super": 0}
for aa in range(2, 10):
    for bb in range(aa + 1, 14):
        if math.gcd(aa, bb) != 1:
            continue
        total = aa + bb
        for gg in range(2, 32):
            for ee in range(2, gg + 1):
                for hh in range(2, ee + 1):
                    for kk in range(1, (ee - 1) // hh + 1):
                        ff = ee - kk * hh
                        for dd in range(
                            1, (hh * gg - 1) // ee + 1
                        ):
                            if math.gcd(dd, hh) != 1:
                                continue
                            GG = hh * gg - ee * dd
                            LL = gg - kk * dd
                            NN = total * GG + dd - 2 * hh
                            if NN <= 0:
                                continue
                            scalar_z_numerator = ff * total - 1
                            for HH in range(
                                1, scalar_z_numerator + 1
                            ):
                                if scalar_z_numerator % HH:
                                    continue
                                JJ = scalar_z_numerator // HH
                                if NN % JJ:
                                    continue
                                DD = NN // JJ
                                if DD <= 0:
                                    continue
                                if (DD + dd * HH) % hh:
                                    continue
                                q_step = (DD + dd * HH) // hh
                                remainders = sorted(
                                    (
                                        aa * ff % HH,
                                        bb * ff % HH,
                                    )
                                )
                                if HH == 1:
                                    if remainders != [0, 0]:
                                        continue
                                elif remainders != [0, 1]:
                                    continue

                                assert HH * JJ == ff * total - 1
                                assert DD * JJ == NN
                                assert q_step * JJ == total * LL - 2
                                assert (
                                    (2 * HH - q_step) * JJ
                                    == total * (2 * ff - LL)
                                )
                                assert (
                                    JJ * (ff * DD - GG * HH)
                                    == hh * (LL - 2 * ff)
                                )

                                defect = ff * DD - GG * HH
                                if defect < 0:
                                    counts["strict"] += 1
                                    # The proof derives H=b, r=1 and
                                    # ultimately g<e.  No candidate
                                    # with e<=g reaches this branch.
                                    rr_num = 2 * ff - LL
                                    assert rr_num % JJ == 0
                                    rr = rr_num // JJ
                                    assert (
                                        q_step
                                        == 2 * HH - total * rr
                                    )
                                    if HH == 1:
                                        assert (
                                            q_step
                                            <= 2 - total
                                            < 0
                                        )
                                    assert not (
                                        rr > 0 and q_step > 0
                                    ), (
                                        aa,
                                        bb,
                                        gg,
                                        ee,
                                        hh,
                                        dd,
                                        ff,
                                        HH,
                                        JJ,
                                        DD,
                                    )
                                elif defect == 0:
                                    counts["resonant"] += 1
                                    assert LL == 2 * ff
                                    assert (
                                        sp.Rational(DD, HH)
                                        == sp.Rational(GG, ff)
                                    )
                                else:
                                    counts["super"] += 1
                                    alpha = aa * ff // HH
                                    beta = bb * ff // HH
                                    if HH == 1:
                                        # Both top terms violate
                                        # their reciprocal bounds.
                                        assert (
                                            q_step * alpha
                                            > aa * LL
                                        )
                                        assert (
                                            q_step * beta
                                            > bb * LL
                                        )
                                    elif aa * ff % HH == 0:
                                        assert (
                                            q_step * alpha
                                            > aa * LL
                                        )
                                    else:
                                        assert bb * ff % HH == 0
                                        assert (
                                            q_step * beta
                                            > bb * LL
                                        )

assert counts["strict"] == 0
assert counts["resonant"] > 0
assert counts["super"] > 0


# Direct P-super x Q-Kummer formula.
for aa, bb, ff, GG, DD, HH, rr in (
    (2, 3, 2, 6, 5, 1, 1),
    (3, 5, 4, 6, 7, 2, 3),
    (2, 7, 6, 9, 8, 3, 5),
):
    cc = math.gcd(ff, GG)
    f_primitive = ff // cc
    G_primitive = GG // cc
    xi = t**DD / y**HH
    A_template = 1 + 2 * xi_symbol + 3 * xi_symbol**2
    A_poly = A_template.subs(xi_symbol, xi)
    p_super = y ** (aa * ff) * A_poly
    q_kummer = t ** (G_primitive * rr) * y ** (
        bb * ff - f_primitive * rr
    )
    delta = ff * DD - GG * HH
    expected = (
        t ** (G_primitive * rr)
        * y
        ** (
            aa * ff
            + bb * ff
            - f_primitive * rr
            - 1
        )
        * delta
        * (sp.Rational(rr, cc) - bb)
        * xi
        * sp.diff(A_template, xi_symbol).subs(xi_symbol, xi)
    )
    assert sp.cancel(
        transformed_bracket(
            p_super, q_kummer, aa, bb, GG
        )
        - expected
    ) == 0


# The formal arithmetic candidate below passes HJ and DJ if one uses
# only a primitive ray direction, but q_* is fractional and the
# required top terms violate deck equivariance.  This guards the
# occupied-support premise.
aa, bb, gg, ee, hh, dd = 2, 9, 12, 11, 6, 5
kk, ff = divmod(ee, hh)
GG = hh * gg - ee * dd
LL = gg - kk * dd
HH, JJ, DD = 3, 18, 10
assert HH * JJ == ff * (aa + bb) - 1
assert DD * JJ == (aa + bb) * GG + dd - 2 * hh
assert sp.Rational(DD + dd * HH, hh) == sp.Rational(25, 6)
alpha, beta = aa * ff // HH, bb * ff // HH
assert (alpha, beta, math.gcd(alpha, beta)) == (3, 15, 3)
assert (alpha * (DD + dd * HH)) % hh != 0
assert (beta * (DD + dd * HH)) % hh != 0


print("verified: first-chart transformed operator and forcing order")
print("verified: matched Wronskian and arbitrary-anchor operator")
print("verified: occupied-support equivariance is essential")
print("verified: strict/resonant/super matched-face no-go arithmetic")
print("verified: direct super-face x Kummer scalar no-go formula")
print("verified: every nonzero chain terminal is the affine defect-one pair")
print(f"audited scalar candidates: {counts}")
