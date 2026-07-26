#!/usr/bin/env python3
"""Verify the exact degree-ten augmented Newton basis."""

from __future__ import annotations

import itertools

import sympy as sp

import verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure as boundary
import verify_weighted_lift_first_nonlinear_cusp_subduction as cusp
import verify_weighted_lift_sagbi_saturation_next_generator_audit as saturation


u = boundary.u
f = boundary.f_symbol


def invariants(a: int, b: int, c: int) -> tuple[int, int, int]:
    beta = -2 * a - b + c
    height = 6 * a + 5 * b
    return beta, height, height + beta


def ordinary_support() -> list[tuple[int, int, int]]:
    return [
        (a, b, total_degree - a - b)
        for total_degree in range(1, 11)
        for a in range(total_degree + 1)
        for b in range(total_degree - a + 1)
    ]


EXCLUDED = {
    (5, 0, 4),
    (6, 0, 4),
    (5, 1, 4),
    (5, 0, 5),
}


def verify_collision_classification() -> None:
    support = ordinary_support()
    collisions = {
        frozenset((left, right))
        for left, right in itertools.combinations(support, 2)
        if invariants(*left)[:2] == invariants(*right)[:2]
    }
    assert collisions == {
        frozenset(((0, 6, 0), (5, 0, 4))),
        frozenset(((0, 7, 0), (5, 1, 4))),
        frozenset(((1, 6, 0), (6, 0, 4))),
        frozenset(((0, 6, 1), (5, 0, 5))),
    }

    retained = [triple for triple in support if triple not in EXCLUDED]
    regular_keys = [invariants(*triple)[:2] for triple in retained]
    polar_keys = [
        (invariants(*triple)[0], invariants(*triple)[2])
        for triple in retained
    ]
    assert len(regular_keys) == len(set(regular_keys))
    assert len(polar_keys) == len(set(polar_keys))

    # T and AT are new singleton atoms.  W has one and only one
    # polar collision, with A^2 B^3.
    assert (-6, 25) not in regular_keys
    assert (-8, 31) not in regular_keys
    assert (-6, 19) not in polar_keys
    assert (-8, 23) not in polar_keys
    assert [
        triple
        for triple in retained
        if (invariants(*triple)[0], invariants(*triple)[2])
        == (-7, 20)
    ] == [(2, 3, 0)]


def target_polynomials() -> tuple[
    tuple[sp.Symbol, sp.Symbol, sp.Symbol],
    sp.Expr,
    sp.Expr,
    sp.Expr,
]:
    A, B, C = sp.symbols("A B C")
    p, q = cusp.build_seed()
    p5 = sp.Poly(p, cusp.w).coeff_monomial(cusp.w**5)
    q6 = sp.Poly(q, cusp.w).coeff_monomial(cusp.w**6)
    _, _, lambda_zero, _ = cusp.build_maximal_subductions(p, q)

    first_coefficients = (
        -sp.Rational(8505, 18948593792),
        -sp.Rational(79515, 151588750336),
        sp.Rational(1587485, 303177500672),
        -sp.Rational(1079635, 303177500672),
    )
    T = sp.expand(
        p5**6 * A**5 * C**4
        - q6**5 * B**6
        + first_coefficients[0] * A**4 * B * C**3
        + first_coefficients[1] * A**3 * B**2 * C**2
        + first_coefficients[2] * A**2 * B**3 * C
        + first_coefficients[3] * A * B**4
    )

    second_coefficients = (
        -sp.Rational(
            10204102899,
            11489574614215070056448,
        ),
        sp.Rational(
            5559334317,
            249773361178588479488,
        ),
        -sp.Rational(
            1028649031155,
            11489574614215070056448,
        ),
        sp.Rational(
            16337519127,
            359049206694220939264,
        ),
    )
    U = sp.expand(
        p5**5 * T * C
        - lambda_zero * B**5
        + second_coefficients[0] * A**4 * C**3
        + second_coefficients[1] * A**3 * B * C**2
        + second_coefficients[2] * A**2 * B**2 * C
        + second_coefficients[3] * A * B**3
    )

    w_coefficients = (
        -sp.Rational(
            1289186932405,
            367666387654882241806336,
        ),
        sp.Rational(
            967724214885,
            183833193827441120903168,
        ),
        sp.Rational(
            280059055635,
            367666387654882241806336,
        ),
    )
    W = sp.expand(
        q6**5 * B * T
        - p5 * lambda_zero * A**5 * C**3
        + w_coefficients[0] * A**4 * B * C**2
        + w_coefficients[1] * A**3 * B**2 * C
        + w_coefficients[2] * A**2 * B**3
    )
    return (A, B, C), T, U, W


def verify_exact_basis_change() -> None:
    (A, B, C), T, U, W = target_polynomials()
    p, q = cusp.build_seed()
    p5 = sp.Poly(p, cusp.w).coeff_monomial(cusp.w**5)
    q6 = sp.Poly(q, cusp.w).coeff_monomial(cusp.w**6)

    assert sp.Poly(T, A, B, C).total_degree() == 9
    assert sp.Poly(A * T, A, B, C).total_degree() == 10
    assert sp.Poly(U, A, B, C).total_degree() == 10
    assert sp.Poly(W, A, B, C).total_degree() == 10

    # Relative to the four removed monomials, the sequential change
    # of basis is triangular with this nonzero diagonal.
    diagonal = (
        sp.Poly(T, A, B, C).coeff_monomial(A**5 * C**4),
        sp.Poly(A * T, A, B, C).coeff_monomial(A**6 * C**4),
        sp.Poly(W, A, B, C).coeff_monomial(A**5 * B * C**4),
        sp.Poly(U, A, B, C).coeff_monomial(A**5 * C**5),
    )
    assert diagonal == (
        p5**6,
        p5**6,
        q6**5 * p5**6,
        p5**5 * p5**6,
    )
    assert sp.prod(diagonal) != 0

    # Audit the target formulas against the exact boundary builders.
    completed_w, template_t, _ = saturation.build_boundary_subduction()
    _, _, _, template_a, template_b, template_u = (
        boundary.boundary_functions()
    )
    substitution = {
        A: template_a,
        B: template_b,
        C: f,
    }
    assert sp.expand(T.subs(substitution) - template_t) == 0
    assert sp.expand(U.subs(substitution) - template_u) == 0
    assert sp.expand(W.subs(substitution) - completed_w) == 0


def pareto_frontier(polynomial: sp.Poly) -> list[tuple[int, int]]:
    support = [
        pair
        for pair, coefficient in polynomial.terms()
        if coefficient != 0
    ]
    return [
        pair
        for pair in support
        if not any(
            other[0] >= pair[0]
            and other[1] >= pair[1]
            and other != pair
            for other in support
        )
    ]


def verify_augmented_boundary_atoms() -> None:
    completed_w, template_t, _ = saturation.build_boundary_subduction()
    _, _, _, template_a, _, template_u = boundary.boundary_functions()
    atoms = {
        "U": (sp.Poly(template_u, u, f), (20, 17)),
        "T": (sp.Poly(template_t, u, f), (25, 19)),
        "AT": (
            sp.Poly(sp.expand(template_a * template_t), u, f),
            (31, 23),
        ),
        "W": (sp.Poly(completed_w, u, f), (25, 20)),
    }

    for name in ("U", "T", "AT"):
        polynomial, top = atoms[name]
        assert polynomial.coeff_monomial(u ** top[0] * f ** top[1]) != 0
        assert pareto_frontier(polynomial) == [top]
        assert [
            pair
            for pair, coefficient in polynomial.terms()
            if coefficient != 0 and pair[1] == top[1]
        ] == [top]

    # T and AT have the full L+1 regular gap and a unique maximal
    # f-power, so their non-top terms are later at a pole.
    for name in ("T", "AT"):
        polynomial, top = atoms[name]
        for (i, j), coefficient in polynomial.terms():
            if coefficient == 0 or (i, j) == top:
                continue
            assert top[0] - i >= 1
            assert top[1] - j >= 1

    polynomial_w, top_w = atoms["W"]
    assert pareto_frontier(polynomial_w) == [(26, 19), (25, 20)]
    assert max(
        j
        for (i, j), coefficient in polynomial_w.terms()
        if coefficient != 0
    ) == 20
    assert [
        (i, j)
        for (i, j), coefficient in polynomial_w.terms()
        if coefficient != 0 and j == 20
    ] == [top_w]

    # For L>=2 the q=20 term uniquely leads.  At L=1 the two
    # frontier terms tie, but the exact fixed graph coefficient is
    # nonzero.
    for graph_degree in range(2, 40):
        maximum = max(
            i + graph_degree * j
            for (i, j), coefficient in polynomial_w.terms()
            if coefficient != 0
        )
        assert [
            pair
            for pair, coefficient in polynomial_w.terms()
            if coefficient != 0
            and pair[0] + graph_degree * pair[1] == maximum
        ] == [(25, 20)]
    fixed_linear_f = sp.Rational(91, 34) - sp.Rational(57, 34) * u
    specialized_w = sp.Poly(
        sp.expand(polynomial_w.as_expr().subs(f, fixed_linear_f)),
        u,
    )
    assert specialized_w.degree() == 45
    assert specialized_w.LC() != 0


def verify_regular_separation_and_characteristics() -> None:
    retained = [
        triple
        for triple in ordinary_support()
        if triple not in EXCLUDED
    ]

    # Ordinary atoms and T,AT are injective in (beta,h).  W has
    # beta=-7 and projected degree 25+20L for L>=2, or degree 45
    # for the fixed L=1 graph.
    standard_atoms = [
        (invariants(*triple)[0], invariants(*triple)[1], triple)
        for triple in retained
    ] + [
        (-6, 25, "T"),
        (-8, 31, "AT"),
    ]
    keys = [(beta, height) for beta, height, _ in standard_atoms]
    assert len(keys) == len(set(keys))

    for graph_degree in range(2, 80):
        labels = [
            (
                beta,
                height + graph_degree * (height + beta),
            )
            for beta, height, _ in standard_atoms
        ]
        labels.append((-7, 25 + 20 * graph_degree))
        assert len(labels) == len(set(labels))
    labels_l1 = [
        (beta, 2 * height + beta)
        for beta, height, _ in standard_atoms
    ]
    labels_l1.append((-7, 45))
    assert len(labels_l1) == len(set(labels_l1))

    # Symbolic all-L audit of W versus every ordinary beta=-7 atom.
    # Equality for L>=2 is (L+1)(h-27)=-2.
    beta_minus_seven_heights = [
        height
        for beta, height, atom in standard_atoms
        if beta == -7
    ]
    assert 26 not in beta_minus_seven_heights
    for height in beta_minus_seven_heights:
        if height == 27:
            assert (height - 27) + 2 != 0
            continue
        possible_graph_degree = (
            -sp.Rational(2, height - 27) - 1
        )
        assert not (
            possible_graph_degree.is_integer
            and possible_graph_degree >= 2
        )

    L = sp.symbols("L", integer=True, positive=True)
    degree_u = 20 + 17 * L
    characteristics = {
        "T": sp.expand(-5 * (25 + 19 * L) + 6 * degree_u),
        "AT": sp.expand(-5 * (31 + 23 * L) + 8 * degree_u),
        "W": sp.expand(-5 * (25 + 20 * L) + 7 * degree_u),
    }
    assert characteristics == {
        "T": 7 * L - 5,
        "AT": 21 * L + 5,
        "W": 19 * L + 15,
    }
    assert all(
        expression.subs(L, value) != 0
        for expression in characteristics.values()
        for value in range(1, 80)
    )
    assert -5 * 45 + 7 * 37 == 34

    # The sole ordinary atom less than L+1 above W is A^2 B^3,
    # and its regular characteristic is never zero.
    beta, height, gamma_power = invariants(2, 3, 0)
    assert (beta, height, gamma_power) == (-7, 27, 20)
    ordinary_characteristic = sp.expand(
        -5 * (height + gamma_power * L)
        - beta * degree_u
    )
    assert ordinary_characteristic == 19 * L + 5


def verify_polar_group() -> None:
    rho = sp.symbols("rho", integer=True, negative=True)
    nu = sp.symbols("nu", integer=True, positive=True)
    alpha = -5 + 17 * rho

    # For a singleton standard atom h=q-beta.  If the coefficient
    # of f' vanishes, the coefficient of f is 2E, not zero.
    beta, q = sp.symbols("beta q", integer=True)
    height = q - beta
    E = beta + rho * q
    coefficient_f_prime = sp.expand(alpha * q - 17 * E)
    coefficient_f = sp.expand(alpha * height - 20 * E)
    beta_under_cancellation = -sp.Rational(5, 17) * q
    assert sp.expand(
        coefficient_f.subs(beta, beta_under_cancellation)
        - 2 * E.subs(beta, beta_under_cancellation)
    ) == 0
    assert sp.expand(
        E.subs(beta, beta_under_cancellation) - alpha * q / 17
    ) == 0

    # The exceptional polar group is
    # f^20 P, P=a*u^27+b*u^25.  Its f'-coefficient is exactly 19.
    a, b = sp.symbols("a b")
    P = a * u**27 + b * u**25
    E_w = -7 + 20 * rho
    f_function = sp.Function("f")(u)
    H = u**20 * f_function**17
    V = f_function**20 * P
    wronskian = sp.expand(
        alpha * H * sp.diff(V, u)
        - E_w * sp.diff(H, u) * V
    )
    expected = sp.expand(
        u**19
        * f_function**36
        * (
            19 * u * sp.diff(f_function, u) * P
            + f_function
            * (alpha * u * sp.diff(P, u) - 20 * E_w * P)
        )
    )
    assert sp.expand(wronskian - expected) == 0

    # If P(1)=0 and P is nonzero, then b=-a and P has a simple
    # zero.  The first surviving local coefficient is
    # (19*nu+alpha)P'(1), and graph bounds make it positive.
    P_cancelled = sp.expand(P.subs(b, -a))
    assert P_cancelled.subs(u, 1) == 0
    assert sp.diff(P_cancelled, u).subs(u, 1) == 2 * a
    lower_bound = sp.expand(
        (19 * nu + alpha).subs(nu, 2 - rho)
    )
    assert lower_bound == 33 - 2 * rho
    for rho_value in range(-30, 0):
        for nu_value in range(2 - rho_value, 50 - rho_value):
            assert (
                19 * nu_value
                + alpha.subs(rho, rho_value)
                > 0
            )


def verify_first_coordinate_reduction() -> None:
    # Eliminating a coefficient mu*U must be done modulo
    # P=U+R, not modulo U: Q-mu*P changes only degree-<=2 ordinary
    # coefficients and preserves the Jacobian.
    U_symbol, R_symbol, Q_zero, mu = sp.symbols(
        "U_symbol R_symbol Q_zero mu"
    )
    P = U_symbol + R_symbol
    Q = mu * U_symbol + Q_zero
    reduced = sp.expand(Q - mu * P)
    assert reduced == Q_zero - mu * R_symbol

    x, y = sp.symbols("x y")

    def jacobian(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(left, x) * sp.diff(right, y)
            - sp.diff(left, y) * sp.diff(right, x)
        )

    P_xy = sp.Function("P")(x, y)
    Q_xy = sp.Function("Q")(x, y)
    assert jacobian(P_xy, Q_xy - mu * P_xy) == jacobian(P_xy, Q_xy)


def main() -> None:
    verify_collision_classification()
    verify_exact_basis_change()
    verify_augmented_boundary_atoms()
    verify_regular_separation_and_characteristics()
    verify_polar_group()
    verify_first_coordinate_reduction()
    print("verified: exactly four ordinary cusp collisions through degree ten")
    print("verified: triangular exact basis change through T, U, and W")
    print("verified: exact regular and polar tops of T, AT, and W")
    print("verified: all regular augmented Newton labels are separated")
    print("verified: the exceptional W/A^2B^3 polar group is nonzero")
    print("verified: U elimination is valid modulo the first coordinate")
    print("RESULT: arbitrary nonhomogeneous target degree <=10 is obstructed")


if __name__ == "__main__":
    main()
