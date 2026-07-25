#!/usr/bin/env python3
"""Verify the local (3,4) countermodel to polar-root consumption."""

from __future__ import annotations

import sympy as sp


def coefficient_bracket(
    p: list[sp.Expr],
    q: list[sp.Expr],
    p_derivative: list[sp.Expr],
    q_derivative: list[sp.Expr],
    degree: int,
) -> sp.Expr:
    return sp.expand(
        sum(
            i * p[i] * q_derivative[j]
            - j * p_derivative[i] * q[j]
            for i in range(len(p))
            for j in range(len(q))
            if i + j - 1 == degree
        )
    )


def verify_countermodel() -> None:
    z = sp.symbols("z")
    p = [sp.Integer(0), sp.Integer(2), sp.Integer(0), sp.Integer(1)]
    q = [
        sp.Integer(-3),
        sp.Integer(-3),
        sp.Integer(2),
        sp.Integer(-3),
        sp.Integer(-2),
    ]
    p_derivative = [
        sp.Integer(1),
        sp.Rational(305, 7244),
        sp.Rational(5361, 3622),
        sp.Rational(1, 8),
    ]
    q_derivative = [
        sp.Rational(-3, 2),
        sp.Rational(28061, 14488),
        sp.Rational(-7943, 1811),
        sp.Rational(-62617, 14488),
        sp.Integer(0),
    ]

    P = sum(coefficient * z**index for index, coefficient in enumerate(p))
    Q = sum(coefficient * z**index for index, coefficient in enumerate(q))
    P_h = sum(
        coefficient * z**index
        for index, coefficient in enumerate(p_derivative)
    )
    Q_h = sum(
        coefficient * z**index
        for index, coefficient in enumerate(q_derivative)
    )
    jacobian = sp.expand(sp.diff(P, z) * Q_h - P_h * sp.diff(Q, z))
    assert jacobian == z**6
    assert p[2] == 0
    assert p_derivative[2] != 0
    assert p_derivative[0] == 1
    assert p[3] and q[4]


def verify_analytic_ode_gate() -> None:
    p = [sp.Integer(0), sp.Integer(2), sp.Integer(0), sp.Integer(1)]
    q = [
        sp.Integer(-3),
        sp.Integer(-3),
        sp.Integer(2),
        sp.Integer(-3),
        sp.Integer(-2),
    ]
    p_derivative = sp.symbols("pd0:4")
    q_derivative = sp.symbols("qd0:5")
    variables = (*p_derivative, *q_derivative)
    rows = [
        coefficient_bracket(
            p,
            q,
            list(p_derivative),
            list(q_derivative),
            degree,
        )
        for degree in range(7)
    ]
    # The seven bracket rows together with these two harmless gauges
    # solve all nine coefficient derivatives analytically.
    rows.extend((p_derivative[0], q_derivative[4]))
    matrix = sp.Matrix(
        [
            [sp.diff(row, variable) for variable in variables]
            for row in rows
        ]
    )
    assert matrix.det() == -28976

    target = sp.Matrix([0, 0, 0, 0, 0, 0, 1, 1, 0])
    solution = matrix.inv() * target
    expected = sp.Matrix(
        [
            1,
            sp.Rational(305, 7244),
            sp.Rational(5361, 3622),
            sp.Rational(1, 8),
            sp.Rational(-3, 2),
            sp.Rational(28061, 14488),
            sp.Rational(-7943, 1811),
            sp.Rational(-62617, 14488),
            0,
        ]
    )
    assert solution == expected


def verify_pure_tschirnhaus_rows() -> None:
    z, h = sp.symbols("z h")
    m = sp.symbols("m", integer=True, positive=True)
    # Check concrete consecutive degrees; the coefficient formula is
    # uniform and the memo gives the general valuation argument.
    for m_value in range(2, 9):
        n_value = m_value + 1
        total = 2 * m_value
        H = sp.Function(f"H{m_value}")(h)
        s = sp.Function(f"s{m_value}")(h)
        u = sp.Function(f"u{m_value}")(h)
        q = [
            sp.Function(f"q{m_value}_{index}")(h)
            for index in range(n_value + 1)
        ]
        P = z**m_value + H
        Q = sum(q[index] * z**index for index in range(n_value + 1))
        residual = sp.expand(
            sp.diff(P, z) * sp.diff(Q, h)
            - sp.diff(P, h) * sp.diff(Q, z)
            - u * (z - s) ** total
        )
        row_zero = residual.coeff(z, 0)
        row_middle = residual.coeff(z, m_value)
        row_top = residual.coeff(z, total)
        assert sp.expand(
            row_zero
            + sp.diff(H, h) * q[1]
            + u * (-s) ** total
        ) == 0
        assert sp.expand(
            row_middle
            - m_value * sp.diff(q[1], h)
            + (m_value + 1) * sp.diff(H, h) * q[m_value + 1]
            + u
            * sp.binomial(total, m_value)
            * (-s) ** m_value
        ) == 0
        assert sp.expand(
            row_top
            - m_value * sp.diff(q[m_value + 1], h)
            + u
        ) == 0


def main() -> None:
    verify_countermodel()
    verify_analytic_ode_gate()
    verify_pure_tschirnhaus_rows()
    print("verified the exact (3,4) coefficient jet with Jacobian z^6")
    print("verified the nonsingular nine-equation analytic ODE gate")
    print("verified the pure (m,m+1) Tschirnhaus coefficient rows")
    print("RESULT: TRANSVERSE (3,4) ROOT-CONSUMPTION COUNTERMODEL PASSES")


if __name__ == "__main__":
    main()
