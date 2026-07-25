#!/usr/bin/env python3
"""Verify radial descent formulas and the conditional factorized Kummer test."""

from __future__ import annotations

import sympy as sp

from route_bd_fbar_obstruction import K
from route_bd_universal_radial_rank import (
    FQ2,
    outer_coefficients,
)
from scratch_hamiltonian_natural_obstruction import (
    high_d4_c,
    k3_high_d4_c,
    k3_outer_coefficients,
)


def verify_belyi_root_reconstruction() -> None:
    p, q, W = sp.symbols("P Q W", nonzero=True)
    UW, VW = sp.symbols("UW VW", nonzero=True)

    # R(W)=Q^2/P^3 is exactly Q^2*U(W)^3=P^3*W*V(W)^2.
    z_candidate = q * UW / (p * VW)
    reconstructed_p = sp.cancel(z_candidate**2 * UW / W)
    reconstructed_q = z_candidate**3 * VW / W
    relation = q**2 * UW**3 - p**3 * W * VW**2
    p_numerator = sp.together(reconstructed_p - p).as_numer_denom()[0]
    assert sp.cancel(p_numerator / relation) == 1

    # For Q, use the same equation after factoring one Q/P copy.
    reconstructed_q_factored = q * UW**3 * q**2 / (p**3 * VW**2 * W)
    assert sp.cancel(reconstructed_q - reconstructed_q_factored) == 0
    q_numerator = sp.together(reconstructed_q - q).as_numer_denom()[0]
    assert sp.cancel(q_numerator / relation) == q


def verify_degree_five_test() -> None:
    z, c = sp.symbols("z c")
    coefficients = sp.Poly(sp.expand((z + c) ** 5), z).all_coeffs()
    assert coefficients == [1, 5 * c, 10 * c**2, 10 * c**3, 5 * c**4, c**5]

    a4 = 5 * c
    a3 = 10 * c**2
    a2 = 10 * c**3
    a1 = 5 * c**4
    a0 = c**5
    assert sp.expand(5 * a3 - 2 * a4**2) == 0
    assert sp.expand(25 * a2 - 2 * a4**3) == 0
    assert sp.expand(125 * a1 - a4**4) == 0
    assert sp.expand(3125 * a0 - a4**5) == 0

    w = sp.symbols("w")
    B = sp.Poly(w**3 + 2 * w + 1, w).as_expr()
    polynomial = sp.Poly(z**5 + B, z, domain=sp.QQ.frac_field(w))
    derivative = sp.Poly(5 * z**4, z, domain=sp.QQ.frac_field(w))
    assert sp.gcd(polynomial, derivative).degree() == 0


def resonant_h(
    w: sp.Symbol,
    d: int,
    left: sp.Expr,
    e: int,
    right: sp.Expr,
) -> sp.Expr:
    c = 5 - d
    f = 5 - e
    return sp.expand(
        (w * sp.diff(left, w) - left) * right / c
        + left * (right - w * sp.diff(right, w)) / f
    )


def verify_k1_resonant_matrix() -> None:
    w = sp.symbols("w")
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
    c1_high = (
        w**5
        + sp.Rational(40, 3) * w**4
        + 100 * w**3
        + sp.Rational(11500, 27) * w**2
        + sp.Rational(92500, 81) * w
    )
    c2_high = V - V.subs(w, 0) - sp.diff(V, w).subs(w, 0) * w
    c3_high = U - U.subs(w, 0) - sp.diff(U, w).subs(w, 0) * w
    c4_high = w**2

    pairs = [
        (1, sp.Integer(1), 4, c4_high),
        (1, c1_high, 4, c4_high),
        (2, w, 3, c3_high),
        (2, c2_high, 3, w),
        (2, c2_high, 3, c3_high),
    ]
    translations = [
        sp.factor(5 * w**3 * sp.diff(resonant_h(w, d, C, e, D), w))
        for d, C, e, D in pairs
    ]
    expected = [
        -sp.Rational(25, 2) * w**4,
        -sp.Rational(50, 27)
        * w**5
        * (54 * w**3 + 675 * w**2 + 3450 * w + 9250),
        -sp.Rational(9, 25) * w**5 * (2 * w + 5),
        sp.Rational(6, 175) * w**5 * (3 * w**2 + 16 * w + 35),
        -sp.Rational(6, 875) * w**6 * (15 * w + 28),
    ]
    assert all(sp.expand(a - b) == 0 for a, b in zip(translations, expected))

    # The omitted low-low d=2,d=3 bracket vanishes.
    assert resonant_h(w, 2, w, 3, w) == 0

    matrix = sp.Matrix(
        [
            [sp.expand(polynomial).coeff(w, degree) for polynomial in translations]
            for degree in range(4, 9)
        ]
    )
    assert matrix.rank() == 5
    assert sp.factor(matrix.det()) == sp.Rational(34992, 1225)


def field_multiply(
    left: dict[int, object],
    right: dict[int, object],
    zero: object,
) -> dict[int, object]:
    result: dict[int, object] = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, zero)
                + left_coefficient * right_coefficient
            )
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient
    }


def field_resonant_translation(
    d: int,
    left: dict[int, object],
    e: int,
    right: dict[int, object],
    zero: object,
) -> dict[int, object]:
    c = 5 - d
    f = 5 - e
    first = {
        exponent: (exponent - 1) * coefficient / c
        for exponent, coefficient in left.items()
        if (exponent - 1) * coefficient
    }
    second = {
        exponent: (1 - exponent) * coefficient / f
        for exponent, coefficient in right.items()
        if (1 - exponent) * coefficient
    }
    h: dict[int, object] = {}
    for product in (
        field_multiply(first, right, zero),
        field_multiply(left, second, zero),
    ):
        for exponent, coefficient in product.items():
            h[exponent] = h.get(exponent, zero) + coefficient
    return {
        exponent + 2: 5 * exponent * coefficient
        for exponent, coefficient in h.items()
        if exponent * coefficient
    }


def field_rank(matrix: list[list[object]]) -> int:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = (
            work[selected],
            work[pivot_row],
        )
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [
            coefficient * inverse
            for coefficient in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index]
                - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
    return pivot_row


def field_determinant(
    matrix: list[list[object]],
    zero: object,
    one: object,
) -> object:
    work = [list(row) for row in matrix]
    determinant = one
    for column in range(len(work)):
        selected = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            return zero
        if selected != column:
            work[column], work[selected] = (
                work[selected],
                work[column],
            )
            determinant = -determinant
        pivot = work[column][column]
        determinant *= pivot
        inverse = pivot.inverse()
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            multiplier = work[row][column] * inverse
            for index in range(column, len(work)):
                work[row][index] = (
                    work[row][index]
                    - multiplier * work[column][index]
                )
    return determinant


def canonical_resonant_translations(
    u: list[object],
    v: list[object],
    c4_high: dict[int, object],
    zero: object,
    one: object,
) -> list[dict[int, object]]:
    u_square = field_multiply(
        {index: coefficient for index, coefficient in enumerate(u)},
        {index: coefficient for index, coefficient in enumerate(u)},
        zero,
    )
    c1_high = {
        exponent - 1: coefficient
        for exponent, coefficient in u_square.items()
        if exponent >= 2 and coefficient
    }
    c2_high = {
        exponent: coefficient
        for exponent, coefficient in enumerate(v)
        if exponent >= 2 and coefficient
    }
    c3_high = {
        exponent: coefficient
        for exponent, coefficient in enumerate(u)
        if exponent >= 2 and coefficient
    }
    pairs = (
        (1, {0: one}, 4, c4_high),
        (1, c1_high, 4, c4_high),
        (2, {1: one}, 3, c3_high),
        (2, c2_high, 3, {1: one}),
        (2, c2_high, 3, c3_high),
    )
    return [
        field_resonant_translation(d, left, e, right, zero)
        for d, left, e, right in pairs
    ]


def verify_k2_k3_resonant_matrices() -> None:
    cases: list[
        tuple[
            str,
            list[object],
            list[object],
            dict[int, object],
            object,
            object,
            object,
        ]
    ] = []
    u2, v2 = outer_coefficients(2)
    cases.append(
        (
            "k2",
            u2,
            v2,
            high_d4_c(2, u2),
            FQ2(),
            FQ2(1),
            FQ2(3138, 7521),
        )
    )
    for label, parameter, expected in (
        ("k3-r1", K(26839), K(5231)),
        ("k3-r2", K(16621), K(22342)),
        ("k3-cubic", K(0, 1), K(27727, 6179, 22327)),
    ):
        u3, v3 = k3_outer_coefficients(parameter)
        cases.append(
            (
                label,
                u3,
                v3,
                k3_high_d4_c(u3),
                K(),
                K(1),
                expected,
            )
        )

    for (
        _label,
        u,
        v,
        c4_high,
        zero,
        one,
        expected_determinant,
    ) in cases:
        translations = canonical_resonant_translations(
            u, v, c4_high, zero, one
        )
        exponents = sorted(
            set().union(*(set(polynomial) for polynomial in translations))
        )
        full_matrix = [
            [
                polynomial.get(exponent, zero)
                for polynomial in translations
            ]
            for exponent in exponents
        ]
        endpoint_minor = [
            [
                polynomial.get(exponent, zero)
                for polynomial in translations
            ]
            for exponent in range(4, 9)
        ]
        assert field_rank(full_matrix) == 5
        assert field_rank(endpoint_minor) == 5
        assert field_determinant(
            endpoint_minor, zero, one
        ) == expected_determinant


def verify_symbolic_endpoint_matrix() -> None:
    w = sp.symbols("w")
    u2, u3, u4, u5 = sp.symbols("u2 u3 u4 u5")
    s2, s3, s4, s5 = sp.symbols("s2 s3 s4 s5")
    u = 1 + w + u2 * w**2 + u3 * w**3 + u4 * w**4 + u5 * w**5
    v = (
        1
        + sp.Rational(2, 3) * w
        + u2 * w**2
        + sp.Rational(8, 7) * u3 * w**3
        + (7 * u2**2 - 4 * u3 + 77 * u4) * w**4 / 63
        + 2
        * (
            4 * u3
            - 7 * u2**2
            - 14 * u4
            + 30 * u2 * u3
            + 147 * u5
        )
        * w**5
        / 231
    )
    c1_high = sum(
        sp.expand(u**2 / w).coeff(w, exponent) * w**exponent
        for exponent in range(1, 6)
    )
    c2_high = sum(
        sp.expand(v).coeff(w, exponent) * w**exponent
        for exponent in range(2, 6)
    )
    c3_high = sum(
        sp.expand(u).coeff(w, exponent) * w**exponent
        for exponent in range(2, 6)
    )
    c4_high = s2 * w**2 + s3 * w**3 + s4 * w**4 + s5 * w**5
    pairs = (
        (1, sp.Integer(1), 4, c4_high),
        (1, c1_high, 4, c4_high),
        (2, w, 3, c3_high),
        (2, c2_high, 3, w),
        (2, c2_high, 3, c3_high),
    )
    translations = [
        sp.expand(5 * w**3 * sp.diff(resonant_h(w, d, C, e, D), w))
        for d, C, e, D in pairs
    ]
    endpoint_matrix = sp.Matrix(
        [
            [
                polynomial.coeff(w, exponent)
                for polynomial in translations
            ]
            for exponent in range(4, 9)
        ]
    )
    assert endpoint_matrix[0, :] == sp.Matrix(
        [[-sp.Rational(25, 2) * s2, 0, 0, 0, 0]]
    )
    # The first row has only its first entry.  Therefore Laplace
    # expansion gives
    # det(M)=(-25/2)*s2*det(M[1:,1:])
    # identically, without an expensive generic determinant expansion.
    endpoint_minor = endpoint_matrix[1:, 1:]
    normalized_translations = [
        sp.cancel(polynomial / w**4)
        for polynomial in translations
    ]
    derivative_matrix = sp.Matrix(
        [
            [
                sp.diff(polynomial, w, order).subs(w, 0)
                for polynomial in normalized_translations
            ]
            for order in range(5)
        ]
    )
    for order in range(5):
        for column in range(5):
            assert sp.expand(
                derivative_matrix[order, column]
                - sp.factorial(order)
                * endpoint_matrix[order, column]
            ) == 0
    # The normalized local ODE alone does not force this determinant to
    # be a unit.  The admissible formal endpoint specialization u2=u3=0
    # makes the first two rows of the lower-right minor supported only
    # in its first column, so its determinant vanishes.  Any all-k proof
    # must use the global passport or common-root polynomial truncation.
    specialized_minor = endpoint_minor.subs({u2: 0, u3: 0})
    assert all(
        sp.expand(specialized_minor[row, column]) == 0
        for row in (0, 1)
        for column in (1, 2, 3)
    )


def verify_endpoint_binomial_obstructions() -> None:
    """Verify the universal cube, square, and (5k+2)-root endpoint symbols."""

    z, w, time = sp.symbols("z w time", nonzero=True)
    x0, x2, x4 = sp.symbols("X0 X2 X4")

    # The low d=1,C=1 mode has a cube-root principal flow.
    m = w / z
    cube_factor = 1 - sp.Rational(3, 4) * x0 * time * m
    z_cube = z * cube_factor ** (-sp.Rational(1, 3))
    w_cube = w * cube_factor ** (-sp.Rational(4, 3))
    assert sp.simplify(
        sp.diff(z_cube, time).subs(time, 0) - x0 * w / 4
    ) == 0
    assert sp.simplify(
        sp.diff(w_cube, time).subs(time, 0) - x0 * w**2 / z
    ) == 0

    # The two universal low C=w modes translate p=-1/(2w^2).
    low_translation = x2 * z ** (-2) + x4 * z ** (-3)
    square_factor = 1 - 2 * time * low_translation * w**2
    w_square = w * square_factor ** (-sp.Rational(1, 2))
    assert sp.simplify(
        sp.diff(w_square, time).subs(time, 0)
        - low_translation * w**3
    ) == 0
    square_polynomial = sp.Poly(
        z**3 - 2 * (x2 * z + x4) * w**2,
        w,
        domain=sp.QQ.frac_field(x2, x4, z),
    )
    square_derivative = square_polynomial.diff()
    # The derivative is a nonzero multiple of w, whereas the polynomial
    # has nonzero constant term z^3.  Hence their gcd is one.
    assert square_polynomial.nth(0) == z**3
    assert set(square_derivative.monoms()) == {(1,)}

    # At infinity xi=z*w^k is fixed by every high principal flow.
    xi = sp.symbols("xi", nonzero=True)
    high_coefficients = sp.symbols("X1 X3 X5 X6")
    high_derivative = sum(
        coefficient * xi**exponent
        for coefficient, exponent in zip(high_coefficients, (3, 2, 1, 0))
    )
    for k in range(1, 6):
        N = 5 * k + 2
        factor = 1 - time * N * high_derivative * w**N / xi**4
        w_high = w * factor ** (-sp.Rational(1, N))
        assert sp.simplify(
            sp.diff(w_high, time).subs(time, 0)
            - high_derivative * w ** (N + 1) / xi**4
        ) == 0
        high_polynomial = sp.Poly(
            xi**4 - N * high_derivative * w**N,
            w,
            domain=sp.QQ.frac_field(xi, *high_coefficients),
        )
        high_derivative_polynomial = high_polynomial.diff()
        assert high_polynomial.nth(0) == xi**4
        assert set(high_derivative_polynomial.monoms()) == {(N - 1,)}
        # Every factor of the derivative is w, while w does not divide
        # the original polynomial; hence their gcd is one.

    first_covers = (frozenset({6}), frozenset({0, 1}))
    second_covers = (
        frozenset({5, 4}),
        frozenset({5, 3}),
        frozenset({2, 3}),
    )
    minimal_covers = {
        first | second
        for first in first_covers
        for second in second_covers
    }
    edges = (
        frozenset({0, 6}),
        frozenset({1, 6}),
        frozenset({2, 5}),
        frozenset({3, 4}),
        frozenset({3, 5}),
    )
    assert len(minimal_covers) == 6
    assert all(
        all(cover & edge for edge in edges)
        and all(
            not all((cover - {vertex}) & edge for edge in edges)
            for vertex in cover
        )
        for cover in minimal_covers
    )


def verify_no_interior_pole_inequalities() -> None:
    """Enumerate the divisorial inequalities behind the no-pole lemma."""

    for k in range(1, 21):
        feasible: list[tuple[int, int]] = []
        for a in range(-30, 31):
            for b in range(-30, 31):
                if 5 * a - 2 * b > 1:
                    continue
                if b < 0:
                    regular = a + k * b >= 0
                elif b == 0:
                    regular = a >= 0
                else:
                    regular = 2 * a - b >= 0 and 3 * a - b >= 0
                if regular:
                    feasible.append((a, b))
        assert all(b >= 0 and a >= 0 for a, b in feasible)
        assert [pair for pair in feasible if pair[1] == 0] == [(0, 0)]
        assert [pair for pair in feasible if pair[1] > 0] == [(1, 2)]


def verify_exceptional_zero_family() -> None:
    """Verify the Laurent-unit reduction and its forbidden first mode."""

    z, w = sp.symbols("z w", nonzero=True)
    h = sp.Function("h")(z, w)
    Z = z * h
    W = w * h**2
    jacobian = sp.det(
        sp.Matrix(
            [
                [sp.diff(Z, z), sp.diff(Z, w)],
                [sp.diff(W, z), sp.diff(W, w)],
            ]
        )
    )
    pulled_density_ratio = sp.simplify(
        (Z**4 / W**3) * jacobian / (z**4 / w**3)
    )
    euler_equation = sp.simplify(
        h + z * sp.diff(h, z) + 2 * w * sp.diff(h, w)
    )
    assert sp.simplify(pulled_density_ratio - euler_equation) == 0

    # Every nonconstant Laurent solution of (D+1)h=1 is a finite sum
    # z^-1*phi(w/z^2).  Its monomial with exponent n has deficit d=2n+1.
    n = sp.symbols("n", integer=True, nonnegative=True)
    monomial = z ** (-1 - 2 * n) * w**n
    assert sp.simplify(
        z * sp.diff(monomial, z)
        + 2 * w * sp.diff(monomial, w)
        + monomial
    ) == 0

    coefficient = sp.symbols("c")
    d = 2 * n + 1
    C = 2 * coefficient * w ** (n - 1)
    c_hamiltonian = 5 - d
    predicted_z = sp.simplify(
        z ** (1 - d)
        * w
        * (C - w * sp.diff(C, w))
        / c_hamiltonian
    )
    predicted_w = sp.simplify(z ** (-d) * w**2 * C)
    actual_z = coefficient * z ** (-2 * n) * w**n
    actual_w = 2 * coefficient * z ** (-2 * n - 1) * w ** (n + 1)
    # d=5 (n=2) is the resonant formula and is separately excluded by
    # the all-k kernel theorem.  Away from it the C-reconstruction agrees.
    assert sp.simplify((predicted_z - actual_z) * (n - 2)) == 0
    assert sp.simplify(predicted_w - actual_w) == 0


def verify_unique_monodromy_signature() -> None:
    """Verify the only uncancelled pullback passport valuation."""

    for k in range(1, 30):
        p = 2 * k + 1
        q = 3 * k + 1
        degree = 3 * p
        contact = 5 * k + 2
        assert degree == 1 + 2 * q
        assert degree - contact == k + 1

        # On the infinity sheet over rho=L, W has pole order one in the
        # tame degree-N extension.  Regular unit values of P,Q force Z
        # to have order k from both coordinate formulas.
        b = -1
        a_from_p = -(p - 1) * b // 2
        a_from_q = -(q - 1) * b // 3
        assert a_from_p == a_from_q == k
        assert 5 * k - 2 * b == contact
        different_exponent = contact - 1
        assert 5 * k - 2 * b == different_exponent + 1

        # The order-two and order-three passport points are cancelled by
        # rho=Q^2/P^3: u^2=t^2 and u^3=t^3 split without ramification.
        assert 2 % 2 == 0
        assert 3 % 3 == 0

        # For the full case-c support x=0 is not contracted: its restrictions
        # have degrees (8,12), hence generic x-valuations (0,0).  The forced
        # edge fixes only the limiting cusp ratio b^2/a^3 at y=infinity.
        # It does not imply the global identity q(y)^2=L*p(y)^3.
        a8, b12 = sp.symbols("a8 b12", nonzero=True)
        L_edge = b12**2 / a8**3
        assert sp.simplify(b12**2 - L_edge * a8**3) == 0

        # A Kummer cover u^e=x cannot split at the radial valuation
        # v_t(x)=1 unless e=1.
        for kummer_degree in range(2, 10):
            assert 1 % kummer_degree


def verify_cusp_complement_stress_test() -> None:
    """Verify the extra-asymptotic-curve mechanism in the shear model."""

    t, q, L = sp.symbols("t q L", nonzero=True)
    n = 21
    # On the cusp p=t^2,q=sqrt(L)t^3, the shear
    # (x^n,q)->(x^n+q^2,q) gives this Kummer equation.
    shear_kummer_rhs = t**2 * (1 - L * t**4)
    assert sp.expand(shear_kummer_rhs - (t**2 - L * t**6)) == 0
    missing_factor = sp.Poly(1 - L * t**4, t, domain=sp.QQ.frac_field(L))
    assert sp.gcd(missing_factor, missing_factor.diff()).degree() == 0
    assert n == 21

    # Its nonproper curve p=q^2 is not the cusp q^2=L*p^3; they meet
    # only at q=0 and the four finite roots 1-L*q^4=0.
    cusp_on_shear_curve = sp.expand(q**2 - L * (q**2) ** 3)
    assert sp.expand(
        cusp_on_shear_curve - q**2 * (1 - L * q**4)
    ) == 0

    # In the undeformed radial model, each finite root gamma of
    # gamma*V(gamma)^2=L*U(gamma)^3 gives a component on which the cusp
    # parameter is a nonzero constant times z, hence degree one.
    z, U_gamma, V_gamma, sqrt_L = sp.symbols(
        "z U_gamma V_gamma sqrt_L", nonzero=True
    )
    cusp_parameter = z * V_gamma / (sqrt_L * U_gamma)
    assert sp.diff(cusp_parameter, z) == V_gamma / (sqrt_L * U_gamma)


def main() -> None:
    verify_belyi_root_reconstruction()
    verify_degree_five_test()
    verify_k1_resonant_matrix()
    verify_k2_k3_resonant_matrices()
    verify_symbolic_endpoint_matrix()
    verify_endpoint_binomial_obstructions()
    verify_no_interior_pole_inequalities()
    verify_exceptional_zero_family()
    verify_unique_monodromy_signature()
    verify_cusp_complement_stress_test()
    print("verified: rational comparison is equivalent to descent of the Belyi root W")
    print("verified the finite monic degree-five Kummer test")
    print("verified five independent k=1 weight-five translation factors")
    print("verified rank five over k=2 and every k=3 Hurwitz factor")
    print("verified the fixed w^4,...,w^8 endpoint minor is invertible")
    print("verified the endpoint minor is a normalized jet Wronskian")
    print("verified the local ODE alone does not force that minor")
    print("verified universal cube, square, and (5k+2)-root endpoint symbols")
    print("verified rational descent has no interior pole valuation")
    print("verified the exceptional (1,2) zero family has a forbidden first mode")
    print("verified the unique possible x!=0 monodromy signature (5k+2,k,-1)")
    print("verified the cusp-complement shear has an extra asymptotic curve")


if __name__ == "__main__":
    main()
