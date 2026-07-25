#!/usr/bin/env python3
"""Exact low-order obstruction to the cusp-compatible case-c stratum.

Assume the case-c supports, the full Newton vertices, and

    P(0,y) = A*y**8,
    Q(0,y) = B*y**12,
    B**2 = L*A**3,
    Q**2 - L*P**3 in (x**3).

Write P=sum_i x**i*p_i(y) and Q=sum_i x**i*q_i(y).  The coefficients
of x and x**2 in the cusp equation imply

    q_1 = (3B/(2A))*y**4*p_1,
    q_2 = (3B/(2A))*y**4*p_2
          + (3B/(8A**2))*p_1**2/y**4.

Polynomiality therefore forces y**4 | p_1**2, hence y**2 | p_1.
This contradicts the nonzero case-c vertex [x*y**0]P != 0.

Equivalently, if c=p_1(0), the coefficient of x**2*y**8 in
Q**2-L*P**3 is -3*B**2*c**2/(4*A**2), which cannot vanish in
characteristic zero when A, B, and c are nonzero.
"""

from __future__ import annotations

import sympy as sp

from route_bd_verify import C_P_VERTICES, C_Q_VERTICES, lattice_points


def verify_case_c_support_bounds() -> None:
    """Check the only Newton-support facts used by the obstruction."""

    p_support = set(lattice_points(C_P_VERTICES))
    q_support = set(lattice_points(C_Q_VERTICES))

    # The decisive full vertex.
    assert (1, 0) in p_support
    assert (1, 0) in C_P_VERTICES

    # Boundary monomials and the x-adic coefficient ranges.
    assert (0, 8) in C_P_VERTICES
    assert (0, 12) in C_Q_VERTICES
    assert sorted(j for i, j in p_support if i == 1) == list(range(10))
    assert sorted(j for i, j in p_support if i == 2) == list(range(2, 11))
    assert sorted(j for i, j in q_support if i == 1) == list(range(1, 14))
    assert sorted(j for i, j in q_support if i == 2) == list(range(1, 15))


def verify_x_adic_recurrence() -> None:
    """Derive the first two exact x-adic cusp recurrences."""

    y = sp.symbols("y")
    A, B = sp.symbols("A B", nonzero=True)
    L = B**2 / A**3
    p1 = sp.Function("p1")(y)
    p2 = sp.Function("p2")(y)
    q1 = sp.Function("q1")(y)
    q2 = sp.Function("q2")(y)

    p0 = A * y**8
    q0 = B * y**12

    cusp_x1 = sp.expand(2 * q0 * q1 - 3 * L * p0**2 * p1)
    solved_q1 = 3 * B * y**4 * p1 / (2 * A)
    assert sp.simplify(cusp_x1.subs(q1, solved_q1)) == 0

    cusp_x2 = sp.expand(
        q1**2
        + 2 * q0 * q2
        - 3 * L * (p0**2 * p2 + p0 * p1**2)
    )
    solved_q2 = (
        3 * B * y**4 * p2 / (2 * A)
        + 3 * B * p1**2 / (8 * A**2 * y**4)
    )
    assert sp.simplify(
        cusp_x2.subs({q1: solved_q1, q2: solved_q2})
    ) == 0

    # A denominator-free form of the divisibility conclusion.
    recurrence = sp.factor(
        cusp_x2.subs(q1, solved_q1)
    )
    expected = sp.factor(
        2 * B * y**12
        * (
            q2
            - 3 * B * y**4 * p2 / (2 * A)
            - 3 * B * p1**2 / (8 * A**2 * y**4)
        )
    )
    assert sp.expand(recurrence - expected) == 0


def verify_decisive_coefficient() -> None:
    """Check the x**2*y**8 coefficient and its nonvanishing."""

    y = sp.symbols("y")
    A, B, c = sp.symbols("A B c", nonzero=True)
    L = B**2 / A**3

    # Only constant/low-order placeholders are needed.  The y factors
    # make all omitted coefficients irrelevant to [y**8].
    p1_tail = sp.symbols("p1_tail")
    p1 = c + y * p1_tail
    p2 = y**2 * sp.symbols("p2_tail")
    q1 = 3 * B * y**4 * p1 / (2 * A)
    q2 = y * sp.symbols("q2_tail")

    p0 = A * y**8
    q0 = B * y**12
    cusp_x2 = sp.expand(
        q1**2
        + 2 * q0 * q2
        - 3 * L * (p0**2 * p2 + p0 * p1**2)
    )
    coefficient = sp.expand(cusp_x2).coeff(y, 8)
    assert sp.simplify(coefficient + 3 * B**2 * c**2 / (4 * A**2)) == 0


def main() -> None:
    verify_case_c_support_bounds()
    verify_x_adic_recurrence()
    verify_decisive_coefficient()
    print("verified the case-c x-adic cusp recurrences through order x^2")
    print("verified cusp compatibility forces y^2 | [x]P")
    print("verified [x^2*y^8](Q^2-L*P^3) = -3*B^2*[x]P(0)^2/(4*A^2)")
    print("RESULT: the cusp-compatible full-vertex case-c stratum is empty")


if __name__ == "__main__":
    main()
