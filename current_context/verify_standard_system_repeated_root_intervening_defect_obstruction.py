#!/usr/bin/env python3
"""Exact checks for the intervening total-defect obstruction."""

from __future__ import annotations

import sympy as sp


x, X, tau = sp.symbols("x X tau")
ell, u, beta = sp.symbols("ell u beta", nonzero=True)


def bounded_solution(
    A: sp.Expr,
    B: sp.Expr,
    h: sp.Expr,
    defect: int,
    g: int,
    field: sp.Domain,
) -> tuple[sp.Expr, sp.Expr] | None:
    """Solve A*q-B*p=h in the exact reciprocal degree bounds."""
    inverse = sp.invert(A, B, domain=field)
    q = sp.factor(sp.rem(sp.cancel(inverse * h), B, domain=field))
    p = sp.cancel((A * q - h) / B)
    if not p.is_polynomial(x):
        return None
    p = sp.factor(p)
    if sp.degree(q, x) > 3 * g - defect:
        return None
    if sp.degree(p, x) > 2 * g - defect:
        return None
    assert sp.cancel(A * q - B * p - h) == 0
    return p, q


def source_term(
    p: list[sp.Expr | None],
    q: list[sp.Expr | None],
    defect: int,
) -> sp.Expr:
    """Return H_defect in the filtered Keller recurrence."""
    value = 0
    for i in range(1, defect):
        j = defect - i
        assert p[i] is not None and q[j] is not None
        value += (
            j * sp.diff(p[i], x) * q[j]
            - i * p[i] * sp.diff(q[j], x)
        )
    return sp.expand(value)


def forbidden_coefficients(
    A: sp.Expr,
    B: sp.Expr,
    h: sp.Expr,
    defect: int,
    g: int,
    field: sp.Domain,
) -> tuple[sp.Expr, ...]:
    """Return the modular coordinates of coker(T_defect)."""
    inverse = sp.invert(A, B, domain=field)
    remainder = sp.rem(sp.cancel(inverse * h), B, domain=field)
    polynomial = sp.Poly(remainder, x, domain=field)
    return tuple(
        sp.factor(polynomial.coeff_monomial(x**power))
        for power in range(3 * g - defect + 1, 3 * g - 1)
    )


def recurrence_until_failure(
    p0: sp.Expr,
    q0: sp.Expr,
    g: int,
    field: sp.Domain,
    final_defect: int,
) -> tuple[
    list[sp.Expr | None],
    list[sp.Expr | None],
    dict[int, tuple[sp.Expr, ...]],
]:
    """Normalize the first jet and run the exact bounded recurrence."""
    A = sp.diff(p0, x)
    B = sp.diff(q0, x)
    assert sp.gcd(A, B) == 1
    inverse = sp.invert(A, B, domain=field)
    q1 = sp.factor(sp.rem(inverse, B, domain=field))
    p1 = sp.factor(sp.cancel((A * q1 - 1) / B))
    assert sp.cancel(A * q1 - B * p1 - 1) == 0
    assert sp.degree(p1, x) <= 2 * g - 1
    assert sp.degree(q1, x) <= 3 * g - 1

    p: list[sp.Expr | None] = [p0, p1]
    q: list[sp.Expr | None] = [q0, q1]
    obstructions: dict[int, tuple[sp.Expr, ...]] = {}
    for defect in range(2, final_defect + 1):
        H = source_term(p, q, defect)
        h = sp.cancel(-H / defect)
        obstruction = forbidden_coefficients(A, B, h, defect, g, field)
        obstructions[defect] = obstruction
        if any(entry != 0 for entry in obstruction):
            break
        solution = bounded_solution(A, B, h, defect, g, field)
        assert solution is not None
        p_new, q_new = solution
        p.append(p_new)
        q.append(q_new)
    return p, q, obstructions


def cubic_tail(poly: sp.Expr, N: int, field: sp.Domain) -> sp.Expr:
    """Return S in poly=poly_(<N)+x^N*S."""
    quotient, remainder = sp.div(
        sp.Poly(poly, x, domain=field),
        sp.Poly(x**N, x, domain=field),
    )
    assert remainder.degree() < N
    return quotient.as_expr()


def verify_saturated_family(g: int) -> None:
    """Check the closed defect-three/four formulas for one exact g."""
    d = x ** (g - 1) * (x + ell)
    p0 = sp.expand(d**2 + u * x)
    q0 = sp.expand(d**3)
    field = sp.QQ.frac_field(ell, u)
    p, q, obstructions = recurrence_until_failure(p0, q0, g, field, 3)

    d_prime = sp.diff(d, x)
    expected_p1 = -4 * d_prime / (3 * u**2)
    expected_q1 = 1 / u - 2 * d * d_prime / u**2
    assert sp.cancel(p[1] - expected_p1) == 0
    assert sp.cancel(q[1] - expected_q1) == 0
    assert obstructions[2] == ()

    # This is the sole nontrivial remainder needed for the closed
    # defect-two formulas in the note.
    r_g = sp.rem(d_prime**3, d, domain=field)
    expected_r_g = ell ** (2 * g - 2) * x ** (g - 1)
    assert sp.expand(r_g - expected_r_g) == 0
    d_second = sp.diff(d_prime, x)
    expected_q2 = (
        2 * d_second / (3 * u**4)
        + 4 * d_prime**3 / (3 * u**5)
        - 4 * d * d_prime * d_second / (3 * u**5)
        - 8 * d * d_prime * expected_r_g / (3 * u**6)
    )
    expected_p2 = (
        sp.Rational(8, 9)
        / u**5
        * (
            (d_prime**3 - expected_r_g) / d
            - d_prime * d_second
            - 2 * d_prime * expected_r_g / u
        )
    )
    assert sp.cancel(p[2] - expected_p2) == 0
    assert sp.cancel(q[2] - expected_q2) == 0

    expected_defect_three = (
        (-1) ** g
        * sp.Rational(64 * g, 9)
        * ell ** (g - 3)
        * (ell ** (2 * g - 1) + (g - 1) * u) ** 2
        / u**10,
    )
    assert tuple(map(sp.factor, obstructions[3])) == tuple(
        map(sp.factor, expected_defect_three)
    )

    # Direct cubic-tail certificate behind the generic formula.
    H3 = source_term(p, q, 3)
    h3 = sp.cancel(-H3 / 3)
    S3 = cubic_tail(sp.expand(q[1] * h3), 3 * g - 4, field)
    E = ell ** (2 * g - 1)
    C_g = (-1) ** g * sp.Rational(32, 27) / u**10
    special_root = -sp.Rational(g - 1, g) * ell
    expected_S3_data = (
        C_g * ell ** (g - 1) * u * (3 * E + (6 * g - 4) * u),
        C_g
        * ell ** (g - 2)
        * (
            -6 * E**2
            + (-15 * g + 12) * E * u
            + (-10 * g**2 + 16 * g - 6) * u**2
        ),
        2 * g * C_g * ell ** (g - 1) * u**2,
    )
    actual_S3_data = (
        S3.subs(x, -ell),
        sp.diff(S3, x).subs(x, -ell),
        S3.subs(x, special_root),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(actual_S3_data, expected_S3_data)
    )

    # On the only nonzero exceptional hypersurface at defect three,
    # both defect-four cokernel coordinates are explicitly nonzero.
    special_u = -ell ** (2 * g - 1) / (g - 1)
    special_p0 = sp.expand(d**2 + special_u * x)
    special_q0 = q0
    special_field = sp.QQ.frac_field(ell)
    special_p, special_q, special_obstructions = recurrence_until_failure(
        special_p0, special_q0, g, special_field, 4
    )
    assert special_obstructions[2] == ()
    assert special_obstructions[3] == (0,)
    expected_defect_four = (
        -sp.Rational(160, 243)
        * g
        * (g - 1) ** 12
        * (46 * g**2 - 25 * g - 8)
        / ell ** (20 * g - 7),
        -sp.Rational(160, 243)
        * g**2
        * (g - 1) ** 12
        * (23 * g - 7)
        / ell ** (20 * g - 6),
    )
    assert tuple(map(sp.factor, special_obstructions[4])) == tuple(
        map(sp.factor, expected_defect_four)
    )

    # Direct cubic-tail certificate on the exceptional branch.  The
    # recurrence has appended the unique bounded p3,q3 before failing
    # at defect four.
    assert len(special_p) == 4 and len(special_q) == 4
    special_H4 = source_term(special_p, special_q, 4)
    special_h4 = sp.cancel(-special_H4 / 4)
    S4 = cubic_tail(
        sp.expand(special_q[1] * special_h4),
        3 * g - 4,
        special_field,
    )
    expected_S4_data = (
        sp.Rational(32, 81)
        * (g - 1) ** 12
        * (9 * g**2 + 41 * g - 25)
        / ell ** (20 * g - 8),
        sp.Rational(160, 243)
        * g
        * (g - 1) ** 12
        * (11 * g + 8)
        / ell ** (20 * g - 7),
        sp.Rational(32, 27)
        * g
        * (g - 1) ** 12
        * (3 * g + 7)
        / ell ** (20 * g - 8),
    )
    actual_S4_data = (
        S4.subs(x, -ell),
        sp.diff(S4, x).subs(x, -ell),
        S4.subs(x, special_root),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(actual_S4_data, expected_S4_data)
    )


# The theorem is intentionally restricted to this finite range.  Each
# case is evaluated over its exact rational function coefficient
# field, including both cubic-tail certificates.
for checked_g in range(5, 21):
    verify_saturated_family(checked_g)


# Symbolic-in-g Hermite reconstruction.  These identities certify
# that the three parameter-g tail evaluations printed in the note
# imply the claimed quadratic coefficients, including the two
# obstruction coordinates.
G = sp.symbols("G", integer=True, positive=True)
E_symbolic = ell ** (2 * G - 1)
a0 = (
    6 * (G - 1) * E_symbolic**2
    + 3 * (G - 1) * (4 * G - 5) * E_symbolic * u
    + 2 * (3 * G**3 - 11 * G**2 + 14 * G - 5) * u**2
)
a1 = (
    6 * (2 * G - 1) * E_symbolic**2
    + 3 * (8 * G**2 - 13 * G + 4) * E_symbolic * u
    + 2 * (G - 1) * (2 * G - 3) * (3 * G - 1) * u**2
)
a2 = 6 * G * (E_symbolic + (G - 1) * u) ** 2
assert sp.factor(a0 - a1 + a2 - u * (3 * E_symbolic + (6 * G - 4) * u)) == 0
assert sp.factor(
    a1
    - 2 * a2
    - (
        -6 * E_symbolic**2
        + (-15 * G + 12) * E_symbolic * u
        + (-10 * G**2 + 16 * G - 6) * u**2
    )
) == 0
assert sp.factor(
    a0
    - (G - 1) * a1 / G
    + (G - 1) ** 2 * a2 / G**2
    - 2 * G * u**2
) == 0

b0 = 115 * G**3 - 117 * G**2 - 163 * G + 75
b1 = 5 * G * (46 * G**2 - 25 * G - 8)
b2 = 5 * G**2 * (23 * G - 7)
assert sp.factor(
    -b0 + b1 - b2 - 3 * (9 * G**2 + 41 * G - 25)
) == 0
assert sp.factor(
    b1 - 2 * b2 + 5 * G * (11 * G + 8)
) == 0
assert sp.factor(
    -b0
    + (G - 1) * b1 / G
    - (G - 1) ** 2 * b2 / G**2
    - 9 * G * (3 * G + 7)
) == 0


# The nonsaturated ell=0, g=5 branch passes defects three and four and
# fails the middle forbidden coordinate at defect five.
g_five = 5
d_zero = x**g_five
zero_p0 = sp.expand(d_zero**2 + u * x)
zero_q0 = sp.expand(d_zero**3)
zero_field = sp.QQ.frac_field(u)
_, _, zero_obstructions = recurrence_until_failure(
    zero_p0, zero_q0, g_five, zero_field, 5
)
assert zero_obstructions[2] == ()
assert zero_obstructions[3] == (0,)
assert zero_obstructions[4] == (0, 0)
assert zero_obstructions[5] == (
    0,
    sp.Rational(60160000, 243) / u**13,
    0,
)


# Recover the top forms of the concrete saturated deck countermodel.
R = X**2 * (X - 1) ** 3
L = X * (X - 1) ** 2 * (X - 2)
D = sp.expand(R + tau * L)
P = sp.expand(D**2 + tau**9 * (X - beta))
Q = sp.expand(D**3 + tau**14)


def homogeneous_piece(poly: sp.Expr, total_degree: int) -> sp.Expr:
    """Extract one ordinary homogeneous total-degree piece."""
    output = 0
    for powers, coefficient in sp.Poly(poly, X, tau).terms():
        if sum(powers) == total_degree:
            output += coefficient * X ** powers[0] * tau ** powers[1]
    return sp.expand(output)


P_top = homogeneous_piece(P, 10)
Q_top = homogeneous_piece(Q, 15)
concrete_d = x**4 * (x + 1)
concrete_p0 = concrete_d**2 + x
concrete_q0 = concrete_d**3
assert sp.expand(P_top - ((X**5 + tau * X**4) ** 2 + tau**9 * X)) == 0
assert sp.expand(Q_top - (X**5 + tau * X**4) ** 3) == 0
assert sp.expand(P_top.subs({X: x, tau: 1}) - concrete_p0) == 0
assert sp.expand(Q_top.subs({X: x, tau: 1}) - concrete_q0) == 0
assert (
    -sp.Rational(64 * g_five, 9) * (1 + 4) ** 2
    == -sp.Rational(8000, 9)
)


# Independent linear-algebra check of the concrete defect-three
# nonmembership, without using the modular remainder criterion.
concrete_p, concrete_q, _ = recurrence_until_failure(
    concrete_p0, concrete_q0, g_five, sp.QQ, 3
)
concrete_H3 = source_term(concrete_p, concrete_q, 3)
concrete_h3 = sp.expand(-concrete_H3 / 3)
concrete_A = sp.diff(concrete_p0, x)
concrete_B = sp.diff(concrete_q0, x)
q_variables = sp.symbols("q3_0:13")
p_variables = sp.symbols("p3_0:8")
trial_q = sum(
    coefficient * x**power for power, coefficient in enumerate(q_variables)
)
trial_p = sum(
    coefficient * x**power for power, coefficient in enumerate(p_variables)
)
columns = []
for variable in (*q_variables, *p_variables):
    image = sp.diff(concrete_A * trial_q - concrete_B * trial_p, variable)
    columns.append(
        [
            sp.Poly(image, x).coeff_monomial(x**power)
            for power in range(22)
        ]
    )
matrix = sp.Matrix(22, len(columns), lambda row, column: columns[column][row])
target = sp.Matrix(
    [sp.Poly(concrete_h3, x).coeff_monomial(x**power) for power in range(22)]
)
assert matrix.rank() == 21
assert matrix.row_join(target).rank() == 22

print("verified: exact total-defect recurrence and cokernel coordinates")
print("verified: symbolic Hermite reconstruction from the displayed tail data")
print("verified: exact defect-three recurrence for every g=5,...,20")
print("verified: exact exceptional defect-four recurrence for every g=5,...,20")
print("verified: nonsaturated g=5, ell=0 branch fails at defect five")
print("verified: every saturated d=x^(g-1)(x+ell) case in the stated range is excluded")
print("verified: the concrete multiplicities-(2,3) example fails at defect three")
print("verified: independent rank test confirms the concrete nonmembership")
