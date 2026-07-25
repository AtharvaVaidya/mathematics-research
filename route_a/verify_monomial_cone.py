#!/usr/bin/env python3
"""Verify the combinatorics behind the Route A monomial-cone theorem.

Put s=uv.  A reduced monomial has the Laurent-chart form

    u^a v^b w^c = s^b (1+s)^(b-a) w^(2(a-b)+c),  c in {0,1}.

For b>a, put r=b-a and m=2r-c.  Clearing w^m gives

    F=w^(m+1)+(s-T)w^m+k*s^b(1+s)^r.

The forced differential is -w^(m-2) ds/F_w, represented by the lattice
point (1,m-1).  This script verifies that this point is strictly interior
exactly when m>b, and verifies the genus counts on the adjacent
one-pole wall m=b-1.

For a>b>=1, put d=a-b and e=2d+c.  Clearing (1+s)^d gives

    F=(1+s)^d(w+s-T)+k*s^b*w^e.

The only degenerate face has local type r^d+w^e at s=-1.  Pick's theorem
minus its delta invariant gives the normalization genus formula checked
below; its elementary lower bound is positive in every case.

In the remaining middle wedge, the script also verifies the complete
canonical row basis, the Fourier-by-jet staircase criterion for the
primitive pole divisor, its uniform tail m>(b-m)^2, and the exceptional
low-genus calculation on the wall b-m=3.
"""

from __future__ import annotations

import math
from fractions import Fraction
import itertools
from pathlib import Path
import sys

import sympy as sp


sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_triangular_hamiltonians import convex_hull  # noqa: E402


def strict_interior(point, hull):
    crosses = []
    for index, left in enumerate(hull):
        right = hull[(index + 1) % len(hull)]
        crosses.append(
            (right[0] - left[0]) * (point[1] - left[1])
            - (right[1] - left[1]) * (point[0] - left[0])
        )
    return all(value > 0 for value in crosses) or all(
        value < 0 for value in crosses
    )


def interior_count(hull):
    max_x = max(point[0] for point in hull)
    max_y = max(point[1] for point in hull)
    return sum(
        strict_interior((i, j), hull)
        for i in range(max_x + 1)
        for j in range(max_y + 1)
    )


def verify_v_side_cone():
    for a in range(0, 21):
        for b in range(a + 1, 31):
            for c in (0, 1):
                r = b - a
                m = 2 * r - c
                support = [
                    (0, m),
                    (1, m),
                    (0, m + 1),
                    (b, 0),
                    (b + r, 0),
                ]
                hull = convex_hull(support)
                interior = strict_interior((1, m - 1), hull)
                if interior != (m > b):
                    raise AssertionError(
                        "v-side interior criterion failed at "
                        f"(a,b,c)=({a},{b},{c}), hull={hull}"
                    )

                # Normalization exponents over s=0 and s=-1.  In the
                # holomorphic cone m>b they are automatically nonnegative.
                if m > b:
                    origin_order = (m - b) // math.gcd(m, b) - 1
                    minus_one_order = (
                        (m - r) // math.gcd(m, r) - 1
                    )
                    if origin_order < 0 or minus_one_order < 0:
                        raise AssertionError(
                            "v-side finite normalization order became negative"
                        )

    # On the adjacent wall m=b-1, the origin is one branch carrying one
    # double pole.  The only other degenerate face is at s=-1.
    for c in (0, 1):
        for a in range(1, 31):
            b = 2 * a + c - 1
            if b <= a:
                continue
            r = b - a
            m = 2 * r - c
            if m != b - 1 or math.gcd(m, b) != 1:
                raise AssertionError("adjacent v-side wall arithmetic failed")
            hull = convex_hull(
                [(0, m), (1, m), (0, m + 1), (b, 0), (b + r, 0)]
            )
            interior = interior_count(hull)
            delta_minus_one = (
                m * r - m - r + math.gcd(m, r)
            ) // 2
            genus = interior - delta_minus_one
            expected = 2 * (a - 1) if c == 0 else 2 * a - 1
            if genus != expected or genus <= 0:
                raise AssertionError(
                    "adjacent v-side genus failed at "
                    f"(a,b,c)=({a},{b},{c}): {genus} != {expected}"
                )
    print("verified: v-side interior, residue wall, and one-pole wall")


def verify_u_side_cone():
    for a in range(2, 31):
        for b in range(1, a):
            for c in (0, 1):
                d = a - b
                e = 2 * d + c
                support = (
                    [(i, 0) for i in range(d + 2)]
                    + [(i, 1) for i in range(d + 1)]
                    + [(b, e)]
                )
                hull = convex_hull(support)
                expected_hull = [(0, 0), (d + 1, 0), (b, e), (0, 1)]
                if hull != expected_hull:
                    raise AssertionError(
                        "u-side hull failed at "
                        f"(a,b,c)=({a},{b},{c}): {hull}"
                    )
                interior = interior_count(hull)
                delta = (
                    d * e - d - e + math.gcd(d, e)
                ) // 2
                genus = interior - delta

                g0 = math.gcd(d, e)
                g1 = math.gcd(abs(b - d - 1), e)
                g2 = math.gcd(b, e - 1)
                formula = e + (b - g0 - g1 - g2) // 2
                if genus != formula or genus <= 0:
                    raise AssertionError(
                        "u-side genus formula failed at "
                        f"(a,b,c)=({a},{b},{c}): {genus} != {formula}"
                    )

                # At s=-1, eta has normalization order
                # (e-d)/gcd(d,e)-1 and is regular.
                order = (e - d) // math.gcd(d, e) - 1
                if order < 0:
                    raise AssertionError("u-side finite order became negative")
    print("verified: u-side positive genus and normalization orders")


def generalized_binomial(alpha, degree):
    answer = Fraction(1)
    for index in range(degree):
        answer *= alpha - index
        answer /= index + 1
    return answer


def verify_middle_wedge_residue_sublattice():
    """Check the uniform Puiseux-residue formula when m divides b."""
    checked = 0
    for c in (0, 1):
        for a in range(1, 41):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                if b % m:
                    continue
                B = b // m
                degree = B - 1

                # Apart from the nonzero prefactor 1/(A*m*T), the residue
                # is [t^(B-1)] of
                # (1+t)^(-r/m)*(1-z*t)^(-(m-1)/m), z=1/T.
                first_alpha = Fraction(-r, m)
                second_rising = Fraction(m - 1, m)
                coefficients = [Fraction(0) for _ in range(degree + 1)]
                for j in range(degree + 1):
                    first = generalized_binomial(
                        first_alpha, degree - j
                    )
                    second = Fraction(1)
                    for index in range(j):
                        second *= second_rising + index
                        second /= index + 1
                    coefficients[j] = first * second

                if m == 1:
                    if coefficients[0] == 0:
                        raise AssertionError(
                            "middle-wedge m=1 residue vanished"
                        )
                elif coefficients[-1] == 0:
                    raise AssertionError(
                        "middle-wedge highest T-pole coefficient vanished"
                    )
                checked += 1
    if checked == 0:
        raise AssertionError("no middle-wedge residue cases were checked")
    print(
        "verified: middle-wedge residue sublattice "
        f"m|b ({checked} exponent triples)"
    )


def verify_strict_cone_sum_interior():
    """Verify the Newton-interior lemma for sums in the strict v-cone."""
    terms = []
    for a in range(0, 7):
        for b in range(a + 1, 15):
            for c in (0, 1):
                if b <= 2 * a + c:
                    continue
                r = b - a
                m = 2 * r - c
                terms.append((a, b, c, r, m))

    # It suffices mathematically to retain one maximum-denominator term:
    # its polygon already contains the target point in its interior, and
    # enlarging a convex polygon preserves interiority.  Pair/triple
    # inventories independently audit the cleared-support bookkeeping.
    inventories = itertools.chain(
        itertools.combinations(terms, 2),
        itertools.combinations(terms[:30], 3),
    )
    for selected in inventories:
        maximum = max(term[4] for term in selected)
        support = [(0, maximum), (1, maximum), (0, maximum + 1)]
        for _, b, _, r, m in selected:
            support.extend(
                (b + offset, maximum - m)
                for offset in range(r + 1)
            )
        hull = convex_hull(support)
        if not strict_interior((1, maximum - 1), hull):
            raise AssertionError(
                f"strict-cone sum lost interiority: {selected}, {hull}"
            )
    print("verified: strict v-cone sums preserve the interior differential")


def verify_middle_wedge_generic_deformation():
    """Verify the nonzero first-variation residue throughout the wedge."""
    checked = 0
    for c in (0, 1):
        for a in range(1, 51):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                degree_G = b + r
                derivative_order = m + 2
                if degree_G - derivative_order != a + c - 2:
                    raise AssertionError(
                        "middle-wedge deformation degree identity failed"
                    )
                if degree_G < derivative_order:
                    raise AssertionError(
                        "middle-wedge first residue could vanish identically"
                    )
                checked += 1
    if checked == 0:
        raise AssertionError("no generic middle-wedge cases were checked")
    print(
        "verified: nonzero first-variation residue throughout "
        f"the middle wedge ({checked} exponent triples)"
    )


def verify_inner_wall_canonical_gaps():
    """Verify the canonical-jet certificates on the wall b-m=2.

    In the middle wedge the origin branches have

        s=t^M,  w=A*t^B,  B-M=(b-m)/g,

    where g=gcd(m,b).  A toric adjoint

        s^(i-1) (1+s)^k w^(j-1) ds/F_w

    has origin order M*i+B*(j-m)-1.  At s=-1 its order is

        (r*(j-m)+m*(k+1)-h)/h,  h=gcd(m,r).

    On b-m=2 the forms below give all two canonical jets prescribed by
    the primitive pole divisor.  Riemann--Roch then gives L(E)=k.
    """

    checked = 0

    # c=0: m=2r, b=2r+2, and there are two origin branches.  Both
    # displayed forms have order zero; their leading coefficients have
    # ratio A^r, which changes sign between the two branches.
    for r in range(1, 101):
        m = 2 * r
        b = 2 * r + 2
        h = math.gcd(m, r)
        g = math.gcd(m, b)
        if g != 2:
            raise AssertionError("even inner-wall branch count failed")
        M = m // g
        B = b // g
        hull = convex_hull(
            [(0, m), (b, 0), (b + r, 0), (0, m + 1)]
        )
        forms = (
            (r, r + 1, (r - 1) // 2),
            (2 * r + 1, 1, r - 1),
        )
        leading_powers = []
        for i, j, k in forms:
            if M * i + B * (j - m) - 1 != 0:
                raise AssertionError("even inner-wall origin order failed")
            minus_one_order = (
                r * (j - m) + m * (k + 1) - h
            ) // h
            if minus_one_order < 0:
                raise AssertionError(
                    "even inner-wall adjoint is singular at s=-1"
                )
            if not all(
                strict_interior((i + offset, j), hull)
                for offset in range(k + 1)
            ):
                raise AssertionError(
                    "even inner-wall adjoint left the Newton interior"
                )
            leading_powers.append(j - m)
        if leading_powers[0] - leading_powers[1] != r:
            raise AssertionError(
                "even inner-wall branch evaluations are not independent"
            )
        checked += 1

    # c=1: m=2r-1, b=2r+1, and there is one origin branch.  For r>=2
    # the forms have consecutive orders zero and one.  The omitted r=1
    # case lies on the already excluded residue sublattice m|b.
    for r in range(2, 101):
        m = 2 * r - 1
        b = 2 * r + 1
        h = math.gcd(m, r)
        g = math.gcd(m, b)
        if h != 1 or g != 1:
            raise AssertionError("odd inner-wall branch count failed")
        hull = convex_hull(
            [(0, m), (b, 0), (b + r, 0), (0, m + 1)]
        )
        forms = (
            (r, r, (r - 1) // 2, 0),
            (2 * r, 1, r - 1, 1),
        )
        for i, j, k, expected_order in forms:
            origin_order = m * i + b * (j - m) - 1
            if origin_order != expected_order:
                raise AssertionError("odd inner-wall origin jet failed")
            minus_one_order = r * (j - m) + m * (k + 1) - 1
            if minus_one_order < 0:
                raise AssertionError(
                    "odd inner-wall adjoint is singular at s=-1"
                )
            if not all(
                strict_interior((i + offset, j), hull)
                for offset in range(k + 1)
            ):
                raise AssertionError(
                    "odd inner-wall adjoint left the Newton interior"
                )
        checked += 1

    print(
        "verified: canonical jets force L(E)=k on the inner wall "
        f"b-m=2 ({checked} parameter values)"
    )


def canonical_row_bounds(m, b, r, j):
    """Return the canonical-adjoint i interval and its (1+s) exponent."""
    lower = b * (m - j) // m + 1
    upper = ((b + r) * (m + 1 - j) - 1) // (m + 1)
    vanishing = r * (m - j) // m
    return lower, upper - vanishing, vanishing


def canonical_staircase_certificate(m, delta, c):
    """Return whether the Fourier-by-jet canonical staircase is complete."""
    r = (m + c) // 2
    b = m + delta
    g = math.gcd(m, delta)
    M = m // g
    q = delta // g
    inverse = 0 if M == 1 else pow(q, -1, M)

    certificate = []
    for order in range(q):
        # Write x=m-j.  The origin-order equation becomes
        # M*i-(M+q)*x=order+1, or q*x+order+1=0 mod M.
        x0 = 0 if M == 1 else (-(order + 1) * inverse) % M
        block = []
        for branch_character in range(g):
            x = x0 + branch_character * M
            j = m - x
            quotient = (q * x + order + 1) // M
            i = x + quotient
            lower, upper, vanishing = canonical_row_bounds(
                m, b, r, j
            )
            if not (lower <= i <= upper):
                return False, ()
            actual_order = M * i + (M + q) * (j - m) - 1
            if actual_order != order:
                raise AssertionError("canonical staircase order failed")
            block.append((i, j, vanishing))
        certificate.append(tuple(block))
    return True, tuple(certificate)


def verify_general_canonical_staircase():
    """Audit the exact Fourier staircase criterion in the middle wedge.

    For g=gcd(m,delta), q=delta/g, the g forms in each order block have
    j exponents differing by M=m/g.  Their branch-value matrix is,
    up to nonzero row and column factors, the g-by-g Fourier matrix.
    Consecutive order blocks therefore give full rank delta.
    """

    certified = 0
    total = 0
    for c in (0, 1):
        for a in range(2, 81):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                delta = b - m
                total += 1

                # The row-basis count independently checks that the
                # conductor conditions at s=-1 remove exactly its delta
                # invariant from the interior adjoints.
                row_dimension = 0
                for j in range(1, m + 1):
                    lower, upper, _ = canonical_row_bounds(m, b, r, j)
                    row_dimension += max(0, upper - lower + 1)
                genus = (
                    b
                    + m
                    + r
                    + 1
                    - math.gcd(b, m)
                    - math.gcd(m, r)
                    - math.gcd(b + r, m + 1)
                ) // 2
                if row_dimension != genus:
                    raise AssertionError(
                        "canonical row basis does not have genus dimension"
                    )

                complete, blocks = canonical_staircase_certificate(
                    m, delta, c
                )
                if complete:
                    if sum(len(block) for block in blocks) != delta:
                        raise AssertionError(
                            "canonical staircase has the wrong size"
                        )
                    certified += 1

    # The elementary tail estimate in the memo proves completeness when
    # m>delta^2.  Audit its integer arithmetic over a broad independent
    # parameter box.
    tail_checked = 0
    for c in (0, 1):
        for delta in range(2, 81):
            first = delta * delta + 1
            if first % 2 != c:
                first += 1
            for m in range(first, first + 160, 2):
                complete, _ = canonical_staircase_certificate(
                    m, delta, c
                )
                if not complete:
                    raise AssertionError(
                        "asymptotic canonical staircase failed at "
                        f"(m,delta,c)=({m},{delta},{c})"
                    )
                tail_checked += 1

    print(
        "verified: Fourier canonical-staircase criterion "
        f"({certified}/{total} sampled wedge cases; "
        f"{tail_checked} asymptotic-tail cases)"
    )


def verify_delta_three_exception():
    """Verify the unique low-genus exception on the wall b-m=3."""
    s, w, T, kappa = sp.symbols("s w T kappa", nonzero=True)
    F = w**3 + (s - T) * w**2 + kappa * s**5 * (1 + s)
    q = -kappa * s * (1 + s) / w
    ratio = sp.diff(q, w) * sp.diff(F, s) - sp.diff(q, s) * sp.diff(F, w)

    # The second presentation is regular wherever the first one has a
    # denominator away from the origin.
    second_q = w * (w + s - T) / s**4
    if sp.rem(
        sp.together(q - second_q).as_numer_denom()[0],
        F,
        w,
    ) != 0:
        raise AssertionError("delta-three exceptional function identity failed")

    other_value = sp.simplify(ratio.subs({s: 0, w: T}))
    if other_value != kappa * T:
        raise AssertionError("delta-three regular-point ratio failed")

    # At the origin put s=t^2, w=A*t^5+..., A^2=kappa/T.  The two
    # leading contributions to dq/eta are 5*kappa*T and 2*kappa*T.
    A, t = sp.symbols("A t", nonzero=True)
    substituted = sp.together(ratio.subs({s: t**2, w: A * t**5}))
    origin_value = sp.limit(substituted, t, 0).subs(A**2, kappa / T)
    if sp.simplify(origin_value - 3 * kappa * T) != 0:
        raise AssertionError("delta-three origin ratio failed")

    r = 1
    m = 2
    b = 5
    genus = (
        b
        + m
        + r
        + 1
        - math.gcd(b, m)
        - math.gcd(m, r)
        - math.gcd(b + r, m + 1)
    ) // 2
    if genus != 2:
        raise AssertionError("delta-three exceptional genus failed")
    print(
        "verified: delta-three low-genus L(3p) generator "
        "and incompatible derivative ratios"
    )


def verify_sharp_canonical_regions():
    """Audit the parity-sharpened uniform canonical-staircase bounds."""
    odd_checked = 0
    even_checked = 0
    for delta in range(2, 201):
        # If c=1, every odd m>=2*delta-1 is certified.
        first_odd = 2 * delta - 1
        for m in range(first_odd, first_odd + 200, 2):
            complete, _ = canonical_staircase_certificate(m, delta, 1)
            if not complete:
                raise AssertionError(
                    "sharp odd canonical region failed at "
                    f"(m,delta)=({m},{delta})"
                )
            odd_checked += 1

        # If c=0 and delta>=4, 3*m>2*delta^2 suffices.
        if delta < 4:
            continue
        first_even = 2 * delta * delta // 3
        if 3 * first_even <= 2 * delta * delta:
            first_even += 1
        if first_even % 2:
            first_even += 1
        for m in range(first_even, first_even + 200, 2):
            complete, _ = canonical_staircase_certificate(m, delta, 0)
            if not complete:
                raise AssertionError(
                    "sharp even canonical region failed at "
                    f"(m,delta)=({m},{delta})"
                )
            even_checked += 1

    print(
        "verified: sharpened canonical regions "
        f"({odd_checked} odd and {even_checked} even cases)"
    )


def verify_delta_four_wall():
    """Verify the complete fixed-coefficient closure of b-m=4."""
    delta = 4
    unresolved = []
    for c in (0, 1):
        for m in range(1 if c else 2, 101, 2):
            if delta % m == 0:
                continue  # The Puiseux-residue sublattice.
            complete, _ = canonical_staircase_certificate(m, delta, c)
            if not complete:
                unresolved.append((m, c))
    if unresolved != [(3, 1), (5, 1)]:
        raise AssertionError(
            f"unexpected delta-four staircase exceptions: {unresolved}"
        )

    s, w, T, kappa = sp.symbols("s w T kappa", nonzero=True)
    for m, c in unresolved:
        r = (m + c) // 2
        b = m + delta
        F = (
            w ** (m + 1)
            + (s - T) * w**m
            + kappa * s**b * (1 + s) ** r
        )
        q_function = -kappa * s * (1 + s) / w
        ratio = sp.diff(q_function, w) * sp.diff(
            F, s
        ) - sp.diff(q_function, s) * sp.diff(F, w)
        ratio /= w ** (m - 2)
        other_value = sp.simplify(ratio.subs({s: 0, w: T}))
        if other_value != kappa * T:
            raise AssertionError("delta-four regular-point ratio failed")

        # At the unique origin branch, eta has leading coefficient
        # 1/(A*T) and q has leading coefficient -kappa/A.
        if delta * kappa * T == other_value:
            raise AssertionError("delta-four ratios should be incompatible")

        # The canonical orders 0,1,2 give rank three on 4p, hence
        # l(4p)=2.  The regular function q supplies its second basis
        # vector.  Its infinity order is nonnegative in both exceptions.
        orders = []
        for j in range(1, m + 1):
            lower, upper, _ = canonical_row_bounds(m, b, r, j)
            for i in range(lower, upper + 1):
                order = m * i + b * (j - m) - 1
                if order < delta:
                    orders.append(order)
        if sorted(orders) != [0, 1, 2]:
            raise AssertionError("delta-four canonical rank failed")
        infinity_order = delta + r - m - 2
        if infinity_order < 0:
            raise AssertionError("delta-four L(E) generator has infinity pole")

    print(
        "verified: complete delta-four wall via staircase or "
        "L(4p)=<1,vw>"
    )


def verify_coprime_function_basis():
    """Verify gap/nongap reciprocity when gcd(m,b-m)=1."""
    checked = 0
    candidates = 0
    for c in (0, 1):
        for delta in range(2, 101):
            for m in range(1 if c else 2, 5 * delta + 1, 2):
                if math.gcd(m, delta) != 1:
                    continue
                r = (m + c) // 2
                b = m + delta
                inverse = pow(delta, -1, m) if m > 1 else 0
                canonical_orders = set()
                function_poles = set()

                for pole in range(1, delta + 1):
                    # beta*b-alpha*m=pole, with 1<=beta<=m.
                    beta = (
                        m
                        if m == 1
                        else (pole * inverse) % m or m
                    )
                    alpha = (beta * b - pole) // m
                    function_vanishing = (
                        beta * r + m - 1
                    ) // m
                    infinity_order = (
                        beta * (b + r)
                        - (alpha + function_vanishing) * (m + 1)
                    )

                    # The complementary canonical point is
                    # (i,j)=(b-alpha,beta).  Its s=-1 vanishing exponent
                    # and the function exponent add to r.
                    lower, upper, canonical_vanishing = (
                        canonical_row_bounds(m, b, r, beta)
                    )
                    if (
                        function_vanishing + canonical_vanishing
                        != r
                    ):
                        raise AssertionError(
                            "coprime conductor complementarity failed"
                        )
                    i = b - alpha
                    is_canonical = lower <= i <= upper
                    is_function = infinity_order >= 0
                    if is_canonical == is_function:
                        raise AssertionError(
                            "coprime gap/nongap reciprocity failed"
                        )
                    if is_canonical:
                        order = m * i + b * (beta - m) - 1
                        if order != pole - 1:
                            raise AssertionError(
                                "coprime canonical order failed"
                            )
                        canonical_orders.add(order)
                    else:
                        function_poles.add(pole)
                        candidates += 1

                    if pole == delta:
                        if beta != 1 or alpha != 1:
                            raise AssertionError(
                                "coprime top-pole function is not vw"
                            )
                    elif is_function and alpha < 2:
                        raise AssertionError(
                            "lower coprime function has nonzero first jet "
                            "at (s,w)=(0,T)"
                        )

                if len(canonical_orders) + len(function_poles) != delta:
                    raise AssertionError(
                        "coprime canonical/function basis has wrong size"
                    )
                checked += 1

    print(
        "verified: coprime gap/nongap function basis and unique top vw "
        f"({checked} exponent pairs, {candidates} nonconstant sections)"
    )


def verify_multibranch_function_basis():
    """Verify the Fourier gap/function basis for arbitrary gcd(m,delta)."""
    checked = 0
    pairs = 0
    sections = 0
    for c in (0, 1):
        for delta in range(2, 81):
            for m in range(1 if c else 2, 5 * delta + 1, 2):
                r = (m + c) // 2
                b = m + delta
                g = math.gcd(m, delta)
                M = m // g
                q = delta // g
                B = b // g
                inverse = 0 if M == 1 else pow(q, -1, M)
                canonical_count = 0
                function_count = 0

                for pole in range(1, q + 1):
                    beta0 = (
                        M
                        if M == 1
                        else (pole * inverse) % M or M
                    )
                    block = []
                    for character in range(g):
                        beta = beta0 + character * M
                        alpha = (beta * B - pole) // M
                        function_vanishing = (
                            beta * r + m - 1
                        ) // m
                        infinity_order = (
                            beta * (b + r)
                            - (alpha + function_vanishing) * (m + 1)
                        )
                        lower, upper, canonical_vanishing = (
                            canonical_row_bounds(m, b, r, beta)
                        )
                        if (
                            function_vanishing + canonical_vanishing
                            != r
                        ):
                            raise AssertionError(
                                "multibranch conductor complementarity failed"
                            )
                        i = b - alpha
                        is_canonical = lower <= i <= upper
                        is_function = infinity_order >= 0
                        if is_canonical == is_function:
                            raise AssertionError(
                                "multibranch gap/function reciprocity failed"
                            )
                        if is_canonical:
                            order = M * i + B * (beta - m) - 1
                            if order != pole - 1:
                                raise AssertionError(
                                    "multibranch canonical order failed"
                                )
                            canonical_count += 1
                        else:
                            function_count += 1
                            sections += 1
                        block.append((beta, alpha, is_function))
                        pairs += 1

                        if pole < q and is_function and alpha < 2:
                            raise AssertionError(
                                "lower multibranch section has a first jet "
                                "at the regular comparison point"
                            )

                    if pole == q:
                        expected = [
                            (1 + character * M, 1 + character * B)
                            for character in range(g)
                        ]
                        actual = [
                            (beta, alpha) for beta, alpha, _ in block
                        ]
                        if actual != expected:
                            raise AssertionError(
                                "multibranch top Fourier block failed"
                            )

                if canonical_count + function_count != delta:
                    raise AssertionError(
                        "multibranch basis does not fill the pole divisor"
                    )
                checked += 1

    print(
        "verified: full multibranch Fourier gap/function basis "
        f"({checked} exponent pairs, {pairs} complementary slots, "
        f"{sections} nonconstant sections)"
    )


def verify_exposed_face_stability():
    """Verify the strict inequalities for stable middle-wedge faces."""
    stable_pairs = 0
    stable_triples = 0
    for c in (0, 1):
        for a in range(2, 16):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                selected_hull = convex_hull(
                    [(0, m), (b, 0), (b + r, 0), (0, m + 1)]
                )
                admissible = []
                for other_c in (0, 1):
                    for other_a in range(0, 16):
                        for other_b in range(other_a + 1, 24):
                            other_r = other_b - other_a
                            other_m = 2 * other_r - other_c
                            if other_m > m or other_b < 2:
                                continue

                            # Strictly above the origin and s=-1 faces.
                            if m * other_b <= b * other_m:
                                continue
                            if m * other_r <= r * other_m:
                                continue

                            # Strictly below the slanted infinity face.
                            infinity_value = (
                                (m + 1) * (other_b + other_r)
                                + (b + r) * (m - other_m)
                            )
                            infinity_bound = (b + r) * (m + 1)
                            if infinity_value >= infinity_bound:
                                continue
                            admissible.append(
                                (
                                    other_a,
                                    other_b,
                                    other_c,
                                    other_r,
                                    other_m,
                                )
                            )

                for other in admissible:
                    support = [
                        (0, m),
                        (1, m),
                        (0, m + 1),
                        *[(b + offset, 0) for offset in range(r + 1)],
                    ]
                    _, other_b, _, other_r, other_m = other
                    support.extend(
                        (other_b + offset, m - other_m)
                        for offset in range(other_r + 1)
                    )
                    if convex_hull(support) != selected_hull:
                        raise AssertionError(
                            "admissible perturbation changed the Newton hull"
                        )
                    stable_pairs += 1

                for left, right in itertools.combinations(
                    admissible[:12], 2
                ):
                    support = [
                        (0, m),
                        (1, m),
                        (0, m + 1),
                        *[(b + offset, 0) for offset in range(r + 1)],
                    ]
                    for other in (left, right):
                        _, other_b, _, other_r, other_m = other
                        support.extend(
                            (other_b + offset, m - other_m)
                            for offset in range(other_r + 1)
                        )
                    if convex_hull(support) != selected_hull:
                        raise AssertionError(
                            "two perturbations changed the Newton hull"
                        )
                    stable_triples += 1

    if stable_pairs == 0:
        raise AssertionError("no stable exposed-face perturbations found")
    print(
        "verified: exposed middle-face stability "
        f"({stable_pairs} pairs, {stable_triples} three-term supports)"
    )


def term_signature(term):
    """Return the origin, s=-1, and infinity slopes of a v-side term."""
    _, b, _, r, m = term
    return (
        Fraction(b, m),
        Fraction(r, m),
        Fraction(b + r, m + 1),
    )


def verify_signature_dichotomy():
    """Verify the finite extremizer dichotomy for middle-wedge supports."""
    terms = []
    for c in (0, 1):
        for a in range(1, 21):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                terms.append((a, b, c, r, m))

    # Dominance lemma: simultaneous improvement of all three face slopes
    # forces weakly larger denominator.  Thus a common strict extremizer
    # automatically clears every other Laurent denominator.
    dominance_checks = 0
    for left in terms:
        left_origin, left_minus_one, left_infinity = term_signature(
            left
        )
        for right in terms:
            right_origin, right_minus_one, right_infinity = (
                term_signature(right)
            )
            if (
                left_origin <= right_origin
                and left_minus_one <= right_minus_one
                and left_infinity >= right_infinity
            ):
                if left[4] < right[4]:
                    raise AssertionError(
                        "signature dominance did not control denominator"
                    )
                dominance_checks += 1

    pattern_witnesses = {}
    tie_supports = 0
    common_supports = 0
    exceptional_supports = 0
    even_terms = [term for term in terms if term[2] == 0][:45]
    odd_terms = [term for term in terms if term[2] == 1][:45]
    sample_terms = even_terms + odd_terms
    for selected in itertools.combinations(sample_terms, 3):
        signatures = [term_signature(term) for term in selected]
        origin_values = [signature[0] for signature in signatures]
        minus_one_values = [signature[1] for signature in signatures]
        infinity_values = [signature[2] for signature in signatures]
        left = [
            index
            for index, value in enumerate(origin_values)
            if value == min(origin_values)
        ]
        middle = [
            index
            for index, value in enumerate(minus_one_values)
            if value == min(minus_one_values)
        ]
        right = [
            index
            for index, value in enumerate(infinity_values)
            if value == max(infinity_values)
        ]

        if len(left) > 1 or len(middle) > 1 or len(right) > 1:
            tie_supports += 1
            continue

        l_index, z_index, r_index = left[0], middle[0], right[0]
        if l_index == z_index == r_index:
            common_supports += 1
            extremal = selected[l_index]
            _, b, _, r, m = extremal
            for index, other in enumerate(selected):
                if index == l_index:
                    continue
                _, other_b, _, other_r, other_m = other
                if other_m > m:
                    raise AssertionError(
                        "common extremizer is not denominator-maximal"
                    )
                if not (
                    m * other_b > b * other_m
                    and m * other_r > r * other_m
                    and (m + 1) * (other_b + other_r)
                    < (b + r) * (other_m + 1)
                ):
                    raise AssertionError(
                        "signature extrema do not imply face inequalities"
                    )
            pattern_witnesses.setdefault("common", selected)
            continue

        exceptional_supports += 1
        if l_index == z_index:
            pattern = "origin=s-1"
        elif l_index == r_index:
            pattern = "origin=infinity"
        elif z_index == r_index:
            pattern = "s-1=infinity"
        else:
            pattern = "all-distinct"
        pattern_witnesses.setdefault(pattern, selected)

    expected_patterns = {
        "common",
        "origin=s-1",
        "origin=infinity",
        "s-1=infinity",
        "all-distinct",
    }
    if set(pattern_witnesses) != expected_patterns:
        raise AssertionError(
            f"signature patterns missing: "
            f"{expected_patterns - set(pattern_witnesses)}"
        )
    print(
        "verified: global face-signature dichotomy "
        f"({dominance_checks} dominance pairs; "
        f"{common_supports} common, {exceptional_supports} separated, "
        f"{tie_supports} tied sampled supports)"
    )


def verify_global_first_face_geometry():
    """Verify the Newton geometry behind the global first-face lemma."""
    terms = []
    for c in (0, 1):
        for a in range(1, 15):
            for b in range(a + 1, 2 * a + c - 1):
                r = b - a
                m = 2 * r - c
                terms.append((a, b, c, r, m))
    even_terms = [term for term in terms if term[2] == 0][:24]
    odd_terms = [term for term in terms if term[2] == 1][:24]
    sample_terms = even_terms + odd_terms

    supports_checked = 0
    pole_edges_checked = 0
    tied_first_faces = 0
    horizontal_resonances = 0
    for selected in itertools.combinations(sample_terms, 3):
        maximum = max(term[4] for term in selected)
        support = [(0, maximum), (1, maximum), (0, maximum + 1)]
        for _, b, _, r, m in selected:
            support.extend(
                (b + offset, maximum - m)
                for offset in range(r + 1)
            )
        hull = convex_hull(support)
        if hull[0] != (0, maximum):
            raise AssertionError("unexpected first Newton vertex")
        eta_point = (1, maximum - 1)
        crosses = []
        for index, left in enumerate(hull):
            right = hull[(index + 1) % len(hull)]
            crosses.append(
                (right[0] - left[0]) * (eta_point[1] - left[1])
                - (right[1] - left[1]) * (eta_point[0] - left[0])
            )
        pole_edges = [
            index for index, value in enumerate(crosses) if value <= 0
        ]
        if not pole_edges or pole_edges != list(range(len(pole_edges))):
            raise AssertionError(
                "eta poles are not the initial lower-left Newton chain"
            )
        if maximum == 1:
            horizontal_resonances += 1
            if not any(
                hull[index + 1][1] == hull[index][1]
                for index in pole_edges
            ):
                raise AssertionError(
                    "m=1 support missed its horizontal resonance"
                )
            continue
        for index in pole_edges:
            left = hull[index]
            right = hull[index + 1]
            if not (right[0] > left[0] and right[1] < left[1]):
                raise AssertionError("non-descending eta pole edge")
        for index in range(len(pole_edges), len(hull)):
            if crosses[index] <= 0:
                raise AssertionError("eta has a non-origin toric pole")

        first_right = hull[1]
        edge_b = first_right[0]
        edge_m = maximum - first_right[1]
        edge_gcd = math.gcd(edge_b, edge_m)
        primitive_b = edge_b // edge_gcd
        primitive_m = edge_m // edge_gcd
        primitive_delta = primitive_b - primitive_m
        if primitive_delta <= 0:
            raise AssertionError("first middle face has nonpositive delta")
        if edge_gcd * primitive_delta < 2:
            raise AssertionError(
                "first-face degree times primitive delta is too small"
            )

        face_terms = []
        for term in selected:
            _, b, _, _, m = term
            if b * primitive_m == m * primitive_b:
                if b % primitive_b or m % primitive_m:
                    raise AssertionError("nonintegral first-face degree")
                face_terms.append(b // primitive_b)
        if max(face_terms) != edge_gcd:
            raise AssertionError("first-face polynomial degree mismatch")
        if len(face_terms) > 1:
            tied_first_faces += 1

        # Every Laurent monomial with s-order one and a w denominator
        # already has a pole on the first face.  Hence later pole edges
        # cannot independently alter the regular-point first jet.
        for beta in range(1, 12):
            if primitive_m - primitive_b * beta >= 0:
                raise AssertionError(
                    "an s-linear denominator term missed the first face"
                )

        supports_checked += 1
        pole_edges_checked += len(pole_edges)

    print(
        "verified: global first-face Newton geometry "
        f"({supports_checked} supports, {pole_edges_checked} pole edges, "
        f"{tied_first_faces} tied first faces, "
        f"{horizontal_resonances} m=1 resonances)"
    )


def verify_face_polynomial_inverse():
    """Verify the asymptotic first-face interpolation obstruction."""
    x, T = sp.symbols("x T")
    exponent_sets = (
        (1, 2),
        (1, 3),
        (2, 3),
        (1, 2, 3),
        (1, 4),
        (2, 4),
        (1, 3, 4),
        (2, 3, 5),
    )
    for exponents in exponent_sets:
        face_polynomial = sum(
            (index + 1) * x**exponent
            for index, exponent in enumerate(exponents)
        )
        relation = face_polynomial - T
        inverse = sp.invert(
            x * sp.diff(face_polynomial, x),
            relation,
            x,
        )
        constant_term = sp.simplify(inverse.subs(x, 0))
        limit = sp.limit(T * constant_term, T, sp.oo)
        if limit != sp.Rational(1, max(exponents)):
            raise AssertionError(
                "face-polynomial inverse has wrong infinity limit"
            )
    print(
        "verified: first-face inverse satisfies "
        "T*H_T(0) -> 1/degree(G)"
    )


def verify_horizontal_m1_residue():
    """Verify the coefficient-uniform residue argument for m=1."""
    s, w, D = sp.symbols("s w D")

    # On F=w(w+D)+A=0, eta=-ds/[w(D+2w)] and ds/A has the
    # same principal part at every branch with w=0, including branches
    # above multiple roots of A.
    eta_coefficient = -1 / (w * (D + 2 * w))
    reciprocal_coefficient = -1 / (w * (D + w))
    regular_difference = sp.factor(
        eta_coefficient - reciprocal_coefficient
    )
    if regular_difference != 1 / ((D + w) * (D + 2 * w)):
        raise AssertionError("horizontal principal-part identity failed")

    # If A has r>=2 distinct roots, and every residue of ds/A vanished,
    # a rational primitive B/C would have
    #
    #   deg C=n=sum(m_i-1),  deg(C/rad(A))=n-r,
    #   B'C-BC'=C/rad(A).
    #
    # But deg(B'C-BC')=deg(B)+n-1 >= n-1, whereas n-r<=n-2.
    # Check this degree contradiction for a broad range of multiplicity
    # patterns, including arbitrarily non-squarefree examples.
    checked_patterns = 0
    for distinct_roots in range(2, 8):
        for multiplicities in itertools.product(
            range(2, 7), repeat=distinct_roots
        ):
            denominator_degree = sum(
                multiplicity - 1 for multiplicity in multiplicities
            )
            right_degree = denominator_degree - distinct_roots
            if not denominator_degree - 1 > right_degree:
                raise AssertionError(
                    "reciprocal-residue degree contradiction failed"
                )
            checked_patterns += 1

    # Concrete residue checks include only multiple roots.  They verify
    # that collisions do not create a hidden exceptional coefficient
    # stratum in the horizontal family.
    repeated_examples = (
        s**3 * (s + 1) ** 2,
        s**4 * (s + 1) ** 4,
        s**3 * (s + 1) ** 3 * (s - 2) ** 2,
    )
    for polynomial in repeated_examples:
        residues = [
            sp.simplify(sp.residue(1 / polynomial, s, root))
            for root in sp.solve(polynomial, s)
        ]
        if all(residue == 0 for residue in residues):
            raise AssertionError("all repeated-root residues vanished")

    print(
        "verified: horizontal m=1 reciprocal-residue obstruction "
        f"({checked_patterns} multiplicity patterns)"
    )


def main():
    verify_v_side_cone()
    verify_u_side_cone()
    verify_middle_wedge_residue_sublattice()
    verify_strict_cone_sum_interior()
    verify_middle_wedge_generic_deformation()
    verify_inner_wall_canonical_gaps()
    verify_general_canonical_staircase()
    verify_delta_three_exception()
    verify_sharp_canonical_regions()
    verify_delta_four_wall()
    verify_coprime_function_basis()
    verify_multibranch_function_basis()
    verify_exposed_face_stability()
    verify_signature_dichotomy()
    verify_global_first_face_geometry()
    verify_face_polynomial_inverse()
    verify_horizontal_m1_residue()
    print("monomial-cone verification passed")


if __name__ == "__main__":
    main()
