#!/usr/bin/env python3
"""Verify the exact degree-eleven augmented Newton-basis obstruction."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure as boundary
import verify_weighted_lift_nonhomogeneous_degree_ten_newton_basis_closure as degree_ten
import verify_weighted_lift_sagbi_saturation_next_generator_audit as saturation


u = boundary.u
f = boundary.f_symbol


def invariants(a: int, b: int, c: int) -> tuple[int, int, int]:
    beta = -2 * a - b + c
    height = 6 * a + 5 * b
    return beta, height, height + beta


def ordinary_support(maximum_degree: int = 11) -> list[tuple[int, int, int]]:
    return [
        (a, b, total_degree - a - b)
        for total_degree in range(1, maximum_degree + 1)
        for a in range(total_degree + 1)
        for b in range(total_degree - a + 1)
    ]


MULTIPLIERS = [
    (a, b, total_degree - a - b)
    for total_degree in range(3)
    for a in range(total_degree + 1)
    for b in range(total_degree - a + 1)
]
EXCLUDED = {
    (5 + a, b, 4 + c)
    for a, b, c in MULTIPLIERS
}


def target_atoms() -> tuple[
    tuple[sp.Symbol, sp.Symbol, sp.Symbol],
    dict[str, sp.Expr],
]:
    (A, B, C), T, U, W = degree_ten.target_polynomials()
    return (A, B, C), {
        "T": T,
        "AT": A * T,
        "A2T": A**2 * T,
        "W": W,
        "AW": A * W,
        "BW": B * W,
        "U": U,
        "AU": A * U,
        "BU": B * U,
        "CU": C * U,
    }


def verify_collision_basis() -> None:
    support = ordinary_support()
    collisions = {
        frozenset((left, right))
        for left, right in itertools.combinations(support, 2)
        if invariants(*left)[:2] == invariants(*right)[:2]
    }
    expected = {
        frozenset(
            (
                (a, 6 + b, c),
                (5 + a, b, 4 + c),
            )
        )
        for a, b, c in MULTIPLIERS
    }
    assert collisions == expected

    (A, B, C), atoms = target_atoms()
    upper = sorted(EXCLUDED)
    replacement_names = [
        "T",
        "AT",
        "W",
        "U",
        "A2T",
        "AW",
        "AU",
        "BW",
        "BU",
        "CU",
    ]
    coefficient_matrix = sp.Matrix(
        [
            [
                sp.Poly(atoms[name], A, B, C).coeff_monomial(
                    A**a * B**b * C**c
                )
                for a, b, c in upper
            ]
            for name in replacement_names
        ]
    )
    assert coefficient_matrix.det() != 0

    retained = [triple for triple in support if triple not in EXCLUDED]
    regular_keys = [invariants(*triple)[:2] for triple in retained]
    polar_keys = [
        (invariants(*triple)[0], invariants(*triple)[2])
        for triple in retained
    ]
    assert len(regular_keys) == len(set(regular_keys))
    assert len(polar_keys) == len(set(polar_keys))


def pareto_frontier(polynomial: sp.Expr) -> list[tuple[int, int]]:
    support = [
        pair
        for pair, coefficient in sp.Poly(polynomial, u, f).terms()
        if coefficient != 0
    ]
    return sorted(
        [
            pair
            for pair in support
            if not any(
                other[0] >= pair[0]
                and other[1] >= pair[1]
                and other != pair
                for other in support
            )
        ]
    )


FRONTIERS = {
    "T": [(-6, 25, 19)],
    "AT": [(-8, 31, 23)],
    "A2T": [(-10, 37, 27)],
    "W": [(-7, 26, 19), (-7, 25, 20)],
    "AW": [(-9, 32, 23), (-9, 31, 24)],
    "BW": [(-8, 31, 23), (-8, 30, 24)],
    "U": [(-5, 20, 17)],
    "AU": [(-7, 26, 21)],
    "BU": [(-6, 25, 21)],
    "CU": [(-4, 20, 18)],
}


def boundary_atoms() -> tuple[sp.Expr, dict[str, sp.Expr]]:
    _, _, _, template_a, template_b, template_u = (
        boundary.boundary_functions()
    )
    template_w, template_t, _ = saturation.build_boundary_subduction()
    atoms = {
        "T": template_t,
        "AT": template_a * template_t,
        "A2T": template_a**2 * template_t,
        "W": template_w,
        "AW": template_a * template_w,
        "BW": template_b * template_w,
        "U": template_u,
        "AU": template_a * template_u,
        "BU": template_b * template_u,
        "CU": f * template_u,
    }
    return template_u, atoms


def verify_boundary_frontiers() -> None:
    _, atoms = boundary_atoms()
    for name, polynomial in atoms.items():
        expected = sorted(
            (height, gamma_power)
            for _, height, gamma_power in FRONTIERS[name]
        )
        assert pareto_frontier(polynomial) == expected

    # The U atom is removed only modulo the actual first coordinate.
    U_symbol, R_symbol, Q_zero, mu = sp.symbols(
        "U_symbol R_symbol Q_zero mu"
    )
    P = U_symbol + R_symbol
    assert sp.expand(mu * U_symbol + Q_zero - mu * P) == (
        Q_zero - mu * R_symbol
    )


def regular_label(
    frontier: list[tuple[int, int, int]],
    graph_degree: int,
) -> tuple[int, int]:
    beta = frontier[0][0]
    return beta, max(
        height + graph_degree * gamma_power
        for _, height, gamma_power in frontier
    )


def verify_regular_boundaries() -> None:
    retained = [
        triple for triple in ordinary_support() if triple not in EXCLUDED
    ]
    standard = [
        (
            invariants(*triple)[0],
            invariants(*triple)[1],
            invariants(*triple)[2],
            str(triple),
        )
        for triple in retained
    ]

    # Pairwise equality of regular labels is linear in L.  Check every
    # possible integer root, not a bounded range of graph degrees.
    records = standard + [
        (
            frontier[0][0],
            max(
                frontier,
                key=lambda item: (item[2], -item[1]),
            )[1],
            max(
                frontier,
                key=lambda item: (item[2], -item[1]),
            )[2],
            name,
        )
        for name, frontier in FRONTIERS.items()
        if name != "U"
    ]
    for left, right in itertools.combinations(records, 2):
        beta_left, height_left, q_left, _ = left
        beta_right, height_right, q_right, _ = right
        if beta_left != beta_right:
            continue
        if q_left == q_right:
            assert height_left != height_right
            continue
        possible = sp.Rational(
            height_right - height_left,
            q_left - q_right,
        )
        assert not (possible.is_integer and possible >= 2)

    L = sp.symbols("L", integer=True, positive=True)
    degree_u = 20 + 17 * L
    expected_characteristics = {
        "T": 7 * L - 5,
        "AT": 21 * L + 5,
        "A2T": 35 * L + 15,
        "W": 19 * L + 15,
        "AW": 33 * L + 25,
        "BW": 16 * L + 10,
        "AU": 14 * L + 10,
        "BU": -3 * L - 5,
        "CU": -22 * L - 20,
    }
    for name, expression in expected_characteristics.items():
        beta, height, gamma_power = max(
            FRONTIERS[name],
            key=lambda item: (item[2], -item[1]),
        )
        actual = sp.expand(
            -5 * (height + gamma_power * L) - beta * degree_u
        )
        assert actual == expression
        assert actual.subs(L, 2) != 0
        slope = sp.Poly(actual, L).coeff_monomial(L)
        intercept = actual.subs(L, 0)
        assert slope * 2 + intercept != 0
        possible_root = -sp.Rational(intercept, slope)
        assert not (
            possible_root.is_integer
            and possible_root >= 2
        )

    # If an ordinary characteristic vanishes, its first deviation loses
    # at most L.  The next lower atom on that beta-face is farther away.
    resonant_records = []
    for triple in retained:
        beta, height, gamma_power = invariants(*triple)
        slope = -5 * gamma_power - 17 * beta
        intercept = -5 * height - 20 * beta
        if slope == 0:
            continue
        possible = -sp.Rational(intercept, slope)
        if not (possible.is_integer and possible >= 2):
            continue
        graph_degree = int(possible)
        current_degree = height + graph_degree * gamma_power
        other_degrees = [
            other_height + graph_degree * other_q
            for other in retained
            if other != triple
            for other_beta, other_height, other_q in [
                invariants(*other)
            ]
            if other_beta == beta
        ]
        other_degrees.extend(
            regular_label(frontier, graph_degree)[1]
            for name, frontier in FRONTIERS.items()
            if name != "U" and frontier[0][0] == beta
        )
        lower = [
            current_degree - other_degree
            for other_degree in other_degrees
            if other_degree < current_degree
        ]
        assert lower and min(lower) > graph_degree
        resonant_records.append((triple, graph_degree, min(lower)))
    assert resonant_records == [
        ((1, 4, 0), 5, 6),
        ((3, 5, 1), 3, 4),
        ((4, 3, 2), 5, 6),
        ((5, 1, 3), 15, 16),
        ((2, 8, 0), 5, 12),
        ((3, 6, 1), 10, 11),
        ((2, 9, 0), 25, 78),
    ]

    resonant_linear_graph = []
    for triple in retained:
        beta, height, gamma_power = invariants(*triple)
        current_degree = height + gamma_power
        if -5 * current_degree - 37 * beta != 0:
            continue
        lower_degrees = [
            other_height + other_q
            for other in retained
            if other != triple
            for other_beta, other_height, other_q in [
                invariants(*other)
            ]
            if other_beta == beta
            and other_height + other_q < current_degree
        ]
        lower_degrees.extend(
            regular_label(frontier, 1)[1]
            for name, frontier in FRONTIERS.items()
            if name != "U"
            and frontier[0][0] == beta
            and regular_label(frontier, 1)[1] < current_degree
        )
        gap = current_degree - max(lower_degrees)
        assert gap > 1
        resonant_linear_graph.append((triple, gap))
    assert resonant_linear_graph == [
        ((1, 3, 0), 6),
        ((2, 6, 0), 2),
    ]

    # At L=1 the four and only four repeated labels are exact
    # two-dimensional groups.
    fixed = sp.Rational(91, 34) - sp.Rational(57, 34) * u
    template_u, atoms = boundary_atoms()
    exact_degrees = {
        name: sp.Poly(sp.expand(atom.subs(f, fixed)), u).degree()
        for name, atom in atoms.items()
        if name != "U"
    }
    groups: dict[tuple[int, int], list[str]] = {}
    for triple in retained:
        beta, height, gamma_power = invariants(*triple)
        groups.setdefault((beta, height + gamma_power), []).append(
            str(triple)
        )
    for name, degree in exact_degrees.items():
        groups.setdefault((FRONTIERS[name][0][0], degree), []).append(name)
    assert {
        key: values
        for key, values in groups.items()
        if len(values) > 1
    } == {
        (-4, 38): ["(1, 3, 1)", "CU"],
        (-6, 46): ["(1, 4, 0)", "BU"],
        (-7, 47): ["(2, 3, 0)", "AU"],
        (-8, 54): ["AT", "BW"],
    }

    # The normalized next/top coefficient slopes distinguish both
    # Wronskians inside each repeated group.
    _, _, _, template_a, template_b, _ = boundary.boundary_functions()
    group_targets = {
        "CU": (-4, atoms["CU"], template_a * template_b**3 * f),
        "BU": (-6, atoms["BU"], template_a * template_b**4),
        "AU": (-7, atoms["AU"], template_a**2 * template_b**3),
        "AT_BW": (-8, atoms["AT"], atoms["BW"]),
    }
    expected_slopes = {
        "CU": -sp.Rational(481, 342),
        "BU": -sp.Rational(91, 152),
        "AU": -sp.Rational(2639, 1368),
        "AT_BW": sp.Rational(8968203125, 121057727177),
    }
    H = sp.expand(template_u.subs(f, fixed))
    for name, (beta, left, right) in group_targets.items():
        wronskians = []
        for target in (left, right):
            V = sp.expand(target.subs(f, fixed))
            wronskians.append(
                sp.Poly(
                    sp.expand(
                        -5 * H * sp.diff(V, u)
                        - beta * sp.diff(H, u) * V
                    ),
                    u,
                )
            )
        assert wronskians[0].degree() == wronskians[1].degree()
        degree = wronskians[0].degree()
        slope_difference = sp.factor(
            wronskians[0].nth(degree - 1)
            / wronskians[0].nth(degree)
            - wronskians[1].nth(degree - 1)
            / wronskians[1].nth(degree)
        )
        assert slope_difference == expected_slopes[name]

    # Injectivity says that a nonzero combination in a repeated group
    # loses at most one u-degree.  Every other label on the same
    # beta-face is at least two degrees lower.
    for repeated_label in ((-4, 38), (-6, 46), (-7, 47), (-8, 54)):
        beta, degree = repeated_label
        lower_degrees = [
            other_degree
            for other_beta, other_degree in groups
            if other_beta == beta and other_degree < degree
        ]
        assert lower_degrees
        assert degree - max(lower_degrees) == 2


POLAR_GROUPS = {
    "W": (-7, 20, 25, 19),
    "CU": (-4, 18, 20, -22),
    "BU": (-6, 21, 25, -3),
    "BW": (-8, 24, 30, 16),
    "AU": (-7, 21, 26, 14),
    "AW": (-9, 24, 31, 33),
}


def verify_polar_classification() -> None:
    retained = [
        triple for triple in ordinary_support() if triple not in EXCLUDED
    ]
    polar_groups: dict[tuple[int, int], list[str]] = {}
    for triple in retained:
        beta, _, gamma_power = invariants(*triple)
        polar_groups.setdefault((beta, gamma_power), []).append(str(triple))
    for name, frontier in FRONTIERS.items():
        if name == "U":
            continue
        beta = frontier[0][0]
        gamma_power = max(item[2] for item in frontier)
        polar_groups.setdefault((beta, gamma_power), []).append(name)
    assert {
        key: values
        for key, values in polar_groups.items()
        if len(values) > 1
    } == {
        (-7, 20): ["(2, 3, 0)", "W"],
        (-4, 18): ["(2, 2, 2)", "CU"],
        (-6, 21): ["(2, 3, 1)", "BU"],
        (-8, 24): ["(2, 4, 0)", "BW"],
        (-7, 21): ["(3, 2, 1)", "AU"],
        (-9, 24): ["(3, 3, 0)", "AW"],
    }

    rho, nu = sp.symbols("rho nu", integer=True)
    alpha = -5 + 17 * rho
    for name, (beta, gamma_power, _, coefficient) in POLAR_GROUPS.items():
        assert -5 * gamma_power - 17 * beta == coefficient
        if name == "W":
            assert sp.expand(
                (coefficient * nu + alpha).subs(nu, 2 - rho)
            ) == 33 - 2 * rho
        elif name in ("CU", "BU"):
            assert coefficient < 0
        elif name == "AW":
            assert sp.expand(
                (coefficient * nu + alpha).subs(nu, 2 - rho)
            ) == 61 - 16 * rho

    k = sp.symbols("k", integer=True, positive=True)
    assert sp.solve(
        sp.Eq(16 * nu, 5 - 17 * rho),
        (rho, nu),
    ) == [(sp.Rational(5, 17) - sp.Rational(16, 17) * nu, nu)]
    # Reduction modulo the denominator proves that every integral
    # solution lies in the displayed residue class.
    assert [
        residue
        for residue in range(16)
        if (5 - 17 * residue) % 16 == 0
    ] == [5]
    assert [
        residue
        for residue in range(14)
        if (5 - 17 * residue) % 14 == 0
    ] == [11]
    # Substitution then records every integral solution; graph
    # compatibility nu >= 2-rho is exactly k >= 2.
    rho_bw, nu_bw = 5 - 16 * k, 17 * k - 5
    rho_au, nu_au = 11 - 14 * k, 17 * k - 13
    assert sp.expand(16 * nu_bw - (5 - 17 * rho_bw)) == 0
    assert sp.expand(14 * nu_au - (5 - 17 * rho_au)) == 0
    assert sp.expand(nu_bw - (2 - rho_bw)) == k - 2
    assert sp.expand(nu_au - (2 - rho_au)) == 3 * k - 4


def gamma_coefficient(expression: sp.Expr, power: int) -> sp.Expr:
    return sp.Poly(expression, f).coeff_monomial(f**power)


def normalized_next_at(
    point: sp.Rational,
    alpha: int,
    beta: int,
    rho: sp.Expr,
    h_top: sp.Expr,
    h_next: sp.Expr,
    q_top: sp.Expr,
    q_next: sp.Expr,
    m: int,
    n: int,
    logarithmic_derivative: sp.Expr,
    fixed: sp.Expr,
) -> sp.Expr:
    def layers(
        top: sp.Expr,
        nxt: sp.Expr,
        power: int,
    ) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
        top_value = top.subs(u, point)
        top_derivative = sp.diff(top, u).subs(u, point)
        fixed_value = fixed.subs(u, point)
        fixed_derivative = sp.diff(fixed, u).subs(u, point)
        next_value = nxt.subs(u, point)
        next_derivative = sp.diff(nxt, u).subs(u, point)
        correction = power * top_value * fixed_value + next_value
        correction_derivative = (
            power
            * (
                top_derivative * fixed_value
                + top_value * fixed_derivative
            )
            + next_derivative
        )
        return (
            top_value,
            top_derivative + power * top_value * logarithmic_derivative,
            correction,
            (power - 1) * logarithmic_derivative * correction
            + correction_derivative,
        )

    h0, dh0, h1, dh1 = layers(h_top, h_next, m)
    q0, dq0, q1, dq1 = layers(q_top, q_next, n)
    a0 = alpha + m * rho
    a1 = alpha + (m - 1) * rho
    b0 = beta + n * rho
    b1 = beta + (n - 1) * rho
    leading = sp.factor(a0 * h0 * dq0 - b0 * dh0 * q0)
    assert leading == 0
    return sp.factor(
        a0 * h0 * dq1
        - b1 * dh0 * q1
        + a1 * h1 * dq0
        - b0 * dh1 * q0
    )


def normalized_leading_at(
    point: sp.Rational,
    alpha: int,
    beta: int,
    rho: sp.Expr,
    h_top: sp.Expr,
    target_top: sp.Expr,
    m: int,
    n: int,
    logarithmic_derivative: sp.Expr,
) -> sp.Expr:
    h = h_top.subs(u, point)
    dh = sp.diff(h_top, u).subs(u, point) + m * h * logarithmic_derivative
    target = target_top.subs(u, point)
    dtarget = (
        sp.diff(target_top, u).subs(u, point)
        + n * target * logarithmic_derivative
    )
    a0 = alpha + m * rho
    b0 = beta + n * rho
    return sp.factor(a0 * h * dtarget - b0 * dh * target)


def normalized_next_expression(
    alpha: int,
    beta: int,
    rho: sp.Expr,
    h_top: sp.Expr,
    h_next: sp.Expr,
    q_top: sp.Expr,
    q_next: sp.Expr,
    m: int,
    n: int,
    logarithmic_derivative: sp.Expr,
    sector_zero: sp.Expr,
) -> sp.Expr:
    h0 = h_top
    dh0 = sp.diff(h_top, u) + m * h_top * logarithmic_derivative
    h1 = m * h_top * sector_zero + h_next
    dh1 = (
        (m - 1) * logarithmic_derivative * h1
        + m
        * (
            sp.diff(h_top, u) * sector_zero
            + h_top * sp.diff(sector_zero, u)
        )
        + sp.diff(h_next, u)
    )
    q0 = q_top
    dq0 = sp.diff(q_top, u) + n * q_top * logarithmic_derivative
    q1 = n * q_top * sector_zero + q_next
    dq1 = (
        (n - 1) * logarithmic_derivative * q1
        + n
        * (
            sp.diff(q_top, u) * sector_zero
            + q_top * sp.diff(sector_zero, u)
        )
        + sp.diff(q_next, u)
    )
    a0 = alpha + m * rho
    a1 = alpha + (m - 1) * rho
    b0 = beta + n * rho
    b1 = beta + (n - 1) * rho
    leading = sp.factor(a0 * h0 * dq0 - b0 * dh0 * q0)
    assert leading == 0
    return sp.factor(
        a0 * h0 * dq1
        - b1 * dh0 * q1
        + a1 * h1 * dq0
        - b0 * dh1 * q0
    )


def normalized_leading_expression(
    alpha: int,
    beta: int,
    rho: sp.Expr,
    h_top: sp.Expr,
    target_top: sp.Expr,
    m: int,
    n: int,
    logarithmic_derivative: sp.Expr,
) -> sp.Expr:
    a0 = alpha + m * rho
    b0 = beta + n * rho
    return sp.factor(
        a0
        * h_top
        * (
            sp.diff(target_top, u)
            + n * target_top * logarithmic_derivative
        )
        - b0
        * (
            sp.diff(h_top, u)
            + m * h_top * logarithmic_derivative
        )
        * target_top
    )


def laurent_coefficients(
    expression: sp.Expr,
    minimum: int,
    maximum: int,
) -> list[sp.Expr]:
    z = sp.symbols("z")
    series = sp.series(
        expression.subs(u, 1 + z),
        z,
        0,
        maximum + 1,
    ).removeO()
    return [
        sp.factor(sp.expand(series).coeff(z, degree))
        for degree in range(minimum, maximum + 1)
    ]


def verify_characteristic_operator(
    alpha: int,
    beta: int,
    m: int,
    n: int,
    h_top: sp.Expr,
    target_top: sp.Expr,
    sector: sp.Expr,
    sector_index: sp.Expr,
) -> None:
    """Check the exact linear top-gamma characteristic on one sector."""

    coefficient_u = sp.expand(
        h_top * target_top * (alpha * n - beta * m)
    )
    coefficient_x = sp.expand(
        h_top * m * sp.diff(target_top, u)
        - sp.diff(h_top, u) * target_top * n
    )
    coefficient_zero = sp.expand(
        alpha * h_top * sp.diff(target_top, u)
        - beta * sp.diff(h_top, u) * target_top
    )
    residual = sp.factor(
        coefficient_u * sp.diff(sector, u)
        + (coefficient_zero + sector_index * coefficient_x) * sector
    )
    assert residual == 0


def verify_resonant_rays_and_interference() -> None:
    p, q, _, template_a, template_b, template_u = (
        boundary.boundary_functions()
    )
    template_w, template_t, _ = saturation.build_boundary_subduction()
    p5 = sp.Poly(p, boundary.nonlinear.w).coeff_monomial(
        boundary.nonlinear.w**5
    )
    q6 = sp.Poly(q, boundary.nonlinear.w).coeff_monomial(
        boundary.nonlinear.w**6
    )
    theta = gamma_coefficient(template_u, 17) / u**20
    kappa20 = gamma_coefficient(template_w, 20) / u**25
    target_bw = sp.expand(
        template_a**2 * template_b**4
        - q6**2 * p5**3 / kappa20 * template_b * template_w
    )
    target_au = sp.expand(
        template_a**3 * template_b**2 * f
        - q6**2 * p5**2 / theta * template_a * template_u
    )
    assert sp.factor(
        gamma_coefficient(target_bw, 24)
        - sp.Rational(2025, 37897187584) * u**30 * (u**2 - 1)
    ) == 0
    assert sp.factor(
        gamma_coefficient(target_au, 21)
        + sp.Rational(1125, 1647703808) * u**26 * (u**2 - 1)
    ) == 0

    h_top = gamma_coefficient(template_u, 17)
    h_next = gamma_coefficient(template_u, 16)
    k = sp.symbols("k", integer=True, positive=True)
    sector_scale = sp.symbols("sector_scale", nonzero=True)
    s2, s3 = sp.symbols("s2 s3")
    sector_zero = (
        1
        - sp.Rational(57, 34) * (u - 1)
        + s2 * (u - 1) ** 2
        + s3 * (u - 1) ** 3
    )

    rho_bw = 5 - 16 * k
    sector_bw = (
        sector_scale
        * u ** (30 * k - 10)
        * (u**2 - 1) ** (17 * k - 5)
    )
    verify_characteristic_operator(
        -5,
        -8,
        17,
        24,
        h_top,
        gamma_coefficient(target_bw, 24),
        sector_bw,
        rho_bw,
    )
    log_bw = (
        (30 * k - 10) / u
        + 2 * (17 * k - 5) * u / (u**2 - 1)
    )
    bw_residue = laurent_coefficients(
        normalized_next_expression(
            -5,
            -8,
            rho_bw,
            h_top,
            h_next,
            gamma_coefficient(target_bw, 24),
            gamma_coefficient(target_bw, 23),
            17,
            24,
            log_bw,
            sector_zero,
        ),
        -1,
        0,
    )
    at_leading = laurent_coefficients(
        normalized_leading_expression(
            -5,
            -8,
            rho_bw,
            h_top,
            gamma_coefficient(template_a * template_t, 23),
            17,
            23,
            log_bw,
        ),
        -1,
        0,
    )
    determinant_bw = sp.factor(
        bw_residue[0] * at_leading[1]
        - bw_residue[1] * at_leading[0]
    )
    quotient_bw = sp.factor(
        determinant_bw
        / ((17 * k - 5) * (105 * k - 32))
    )
    assert quotient_bw.is_Rational and quotient_bw != 0
    assert s2 not in determinant_bw.free_symbols

    rho_au = 11 - 14 * k
    sector_au = (
        sector_scale
        * u ** (22 * k - 18)
        * (u**2 - 1) ** (17 * k - 13)
    )
    verify_characteristic_operator(
        -5,
        -7,
        17,
        21,
        h_top,
        gamma_coefficient(target_au, 21),
        sector_au,
        rho_au,
    )
    log_au = (
        (22 * k - 18) / u
        + 2 * (17 * k - 13) * u / (u**2 - 1)
    )
    au_residue = laurent_coefficients(
        normalized_next_expression(
            -5,
            -7,
            rho_au,
            h_top,
            h_next,
            gamma_coefficient(target_au, 21),
            gamma_coefficient(target_au, 20),
            17,
            21,
            log_au,
            sector_zero,
        ),
        -1,
        1,
    )
    w_leading = laurent_coefficients(
        normalized_leading_expression(
            -5,
            -7,
            rho_au,
            h_top,
            gamma_coefficient(template_w, 20),
            17,
            20,
            log_au,
        ),
        -1,
        1,
    )
    ordinary_w_leading = laurent_coefficients(
        normalized_leading_expression(
            -5,
            -7,
            rho_au,
            h_top,
            q6**2 * p5**3 * u**27,
            17,
            20,
            log_au,
        ),
        -1,
        1,
    )
    determinant_au = sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [
                        au_residue[index],
                        w_leading[index],
                        ordinary_w_leading[index],
                    ]
                    for index in range(3)
                ]
            )
        )
    )
    quotient_au = sp.factor(determinant_au / (17 * k - 13) ** 2)
    assert quotient_au.is_Rational and quotient_au != 0
    assert s2 not in determinant_au.free_symbols
    assert s3 not in determinant_au.free_symbols

    # At the first lower total-gamma layer the only possible leading
    # interference is AT for BW, and the W/A^2B^3 group for AU.
    polar_records = [
        (*invariants(*triple)[::2], str(triple))
        for triple in [
            item for item in ordinary_support() if item not in EXCLUDED
        ]
    ]
    polar_records.extend(
        (
            frontier[0][0],
            max(item[2] for item in frontier),
            name,
        )
        for name, frontier in FRONTIERS.items()
        if name != "U"
    )

    # On a resonant ray the earliest E-face contains only the indicated
    # two-dimensional group.  Enumerate as well every face strictly
    # between it and the first lower-total-gamma residue.
    expected_resonant_faces = {
        "BW": {
            (-8, 24, "BW"),
            (-8, 24, "(2, 4, 0)"),
        },
        "AU": {
            (-7, 21, "AU"),
            (-7, 21, "(3, 2, 1)"),
        },
    }
    expected_intervening = {
        "BW": {
            (-7, 24, "(1, 5, 0)"),
            (-6, 24, "(0, 6, 0)"),
            (-5, 24, "(4, 1, 4)"),
            (-4, 24, "(3, 2, 4)"),
            (-3, 24, "(2, 3, 4)"),
            (-2, 24, "(1, 4, 4)"),
            (-1, 24, "(0, 5, 4)"),
        },
        "AU": {
            (-10, 20, "(5, 0, 0)"),
            (-9, 20, "(4, 1, 0)"),
            (-8, 20, "(3, 2, 0)"),
            (-6, 21, "BU"),
            (-6, 21, "(2, 3, 1)"),
            (-5, 21, "(1, 4, 1)"),
            (-4, 21, "(0, 5, 1)"),
            (-3, 21, "(4, 0, 5)"),
            (-2, 21, "(3, 1, 5)"),
            (-1, 21, "(2, 2, 5)"),
            (0, 21, "(1, 3, 5)"),
            (1, 21, "(0, 4, 5)"),
        },
    }
    for name, rho_family, beta, q_power in (
        ("BW", rho_bw, -8, 24),
        ("AU", rho_au, -7, 21),
    ):
        resonant_order = sp.expand(beta + rho_family * q_power)
        residue_order = sp.expand(resonant_order - rho_family)
        same_face = set()
        intervening = set()
        for other_beta, other_q, label in polar_records:
            other_order = sp.expand(other_beta + rho_family * other_q)
            lower_gap = sp.expand(other_order - resonant_order)
            upper_gap = sp.expand(residue_order - other_order)
            if lower_gap == 0:
                same_face.add((other_beta, other_q, label))
                continue
            lower_polynomial = sp.Poly(lower_gap, k)
            upper_polynomial = sp.Poly(upper_gap, k)
            if (
                lower_gap.subs(k, 2) > 0
                and upper_gap.subs(k, 2) > 0
                and lower_polynomial.LC() >= 0
                and upper_polynomial.LC() >= 0
            ):
                intervening.add((other_beta, other_q, label))
        assert same_face == expected_resonant_faces[name]
        assert intervening == expected_intervening[name]

    # The only repeated intervening AU face is the BU group.  It is
    # nonresonant for the AU characteristic family.
    alpha_au = -5 + 17 * rho_au
    assert sp.expand(-3 * (17 * k - 13) + alpha_au) == -289 * k + 221
    assert (-289 * k + 221).subs(k, 2) < 0

    expected_lower = {
        "BW": {(-8, 23, "AT")},
        "AU": {
            (-7, 20, "W"),
            (-7, 20, "(2, 3, 0)"),
        },
    }
    for name, rho_family, beta, q_power in (
        ("BW", rho_bw, -8, 24),
        ("AU", rho_au, -7, 21),
    ):
        next_value = beta + rho_family * (q_power - 1)
        matches = set()
        for other_beta, other_q, label in polar_records:
            difference = sp.expand(
                other_beta + rho_family * other_q - next_value
            )
            if difference == 0:
                matches.add((other_beta, other_q, label))
                continue
            roots = sp.solve(sp.Eq(difference, 0), k)
            assert not any(
                root.is_integer and root >= 2
                for root in roots
            )
        assert matches == expected_lower[name]

    # A degree-two first-coordinate perturbation starts strictly after
    # the resonant residue layer.
    degree_two = ordinary_support(2)
    for rho_family in (rho_bw, rho_au):
        alpha = -5 + 17 * rho_family
        for triple in degree_two:
            beta, _, gamma_power = invariants(*triple)
            gap = sp.expand(
                beta + rho_family * gamma_power - (alpha - rho_family)
            )
            assert sp.Poly(gap, k).LC() > 0
            assert gap.subs(k, 2) > 0


def main() -> None:
    verify_collision_basis()
    verify_boundary_frontiers()
    verify_regular_boundaries()
    verify_polar_classification()
    verify_resonant_rays_and_interference()
    print("verified: ten and only ten cusp collisions through degree eleven")
    print("verified: exact triangular basis through T, U, and W products")
    print("verified: every regular boundary, including all four L=1 groups")
    print("verified: exact L=1 next-label gaps")
    print("verified: all six polar groups and the two resonance families")
    print("verified: resonant-face uniqueness and intervening-face audit")
    print("verified: BW/AT and AU/W-group interference determinants")
    print("RESULT: arbitrary nonhomogeneous target degree <=11 is obstructed")


if __name__ == "__main__":
    main()
