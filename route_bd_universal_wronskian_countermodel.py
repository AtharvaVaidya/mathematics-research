#!/usr/bin/env python3
"""A characteristic-zero countermodel to a Wronskian-only all-r proof.

At scale r=5, construct the normalized marked (3,5) system

    deg X=10, deg T=15,
    deg(2*X*T'-3*X'*T) <= 4,

with X-X(0) of order three and
T-b3*X-(T(0)-b3*X(0)) of order five.

The displayed F_32003 point is a simple zero of the ten-equation
saturated system.  Multivariate Hensel therefore lifts it to an isolated
point over Qbar embedded in Q_32003.  At the lifted point the lead remains
nonzero, X and T remain coprime and squarefree, and gcd(X',T') has degree
two.  A common polynomial right factor would have degree dividing
gcd(10,15)=5 and would force gcd(X',T') to have degree at least four.
Thus the lifted polynomial pair is primitive.

This is not a Keller map.  It proves that the depressed-Wronskian degree
bound plus the pole-sensitive marked local type cannot by themselves
eliminate all scales.
"""

from __future__ import annotations

import sympy as sp


PRIME = 32003
R = 5


def rational_mod_prime(value: sp.Expr) -> int:
    value = sp.Rational(value)
    return (
        int(value.p) % PRIME
        * pow(int(value.q) % PRIME, -1, PRIME)
        % PRIME
    )


def polynomial_mod_prime(expression: sp.Expr, h: sp.Symbol) -> sp.Poly:
    rational_poly = sp.Poly(sp.expand(expression), h, domain=sp.QQ)
    reduced = sum(
        rational_mod_prime(coefficient) * h ** monomial[0]
        for monomial, coefficient in rational_poly.terms()
    )
    return sp.Poly(reduced, h, modulus=PRIME)


def build_system() -> dict[str, object]:
    h = sp.symbols("h")
    a = sp.symbols("a0:10")
    b = sp.symbols("b0:15")
    aux = sp.symbols("aux")

    X = h**10 + sum(a[index] * h**index for index in range(10))
    T = h**15 + sum(b[index] * h**index for index in range(15))
    X = sp.expand(X.subs({a[1]: 0, a[2]: 0, a[3]: 1}))
    T = sp.expand(T.subs({b[1]: 0, b[2]: 0, b[4]: b[3] * a[4]}))
    W = sp.Poly(
        sp.expand(2 * X * sp.diff(T, h) - 3 * sp.diff(X, h) * T),
        h,
    )

    solved: dict[sp.Symbol, sp.Expr] = {}
    triangular_coefficients: list[sp.Expr] = []
    for index in range(14, 4, -1):
        degree = 9 + index
        equation = sp.expand(W.coeff_monomial(h**degree).subs(solved))
        coefficient = sp.diff(equation, b[index])
        assert coefficient and not coefficient.free_symbols
        triangular_coefficients.append(coefficient)
        answers = sp.solve(equation, b[index])
        assert len(answers) == 1
        solved[b[index]] = sp.factor(answers[0])

    residual_rationals = [
        sp.together(W.coeff_monomial(h**degree).subs(solved))
        for degree in range(13, 4, -1)
    ]
    residual = [
        sp.expand(equation.as_numer_denom()[0])
        for equation in residual_rationals
    ]
    lead = sp.together((b[5] - b[3] * a[5]).subs(solved))
    lead_numerator, lead_denominator = lead.as_numer_denom()
    variables = (a[0], *a[4:10], b[0], b[3], aux)
    equations = [
        *residual,
        sp.expand(aux * lead_numerator - 1),
    ]
    denominators = [
        *[equation.as_numer_denom()[1] for equation in residual_rationals],
        lead_denominator,
        *[
            sp.together(value).as_numer_denom()[1]
            for value in solved.values()
        ],
    ]
    return {
        "h": h,
        "a": a,
        "b": b,
        "aux": aux,
        "X": X,
        "T": T,
        "W": W,
        "solved": solved,
        "variables": variables,
        "equations": equations,
        "lead": lead,
        "lead_numerator": lead_numerator,
        "lead_denominator": lead_denominator,
        "denominators": denominators,
        "triangular_coefficients": triangular_coefficients,
    }


def finite_field_point(data: dict[str, object]) -> dict[sp.Symbol, int]:
    a = data["a"]
    b = data["b"]
    aux = data["aux"]
    return {
        a[0]: -1727,
        a[4]: -6872,
        a[5]: 8738,
        a[6]: -14424,
        a[7]: -9482,
        a[8]: -10323,
        a[9]: -10862,
        b[0]: -10303,
        b[3]: -7755,
        aux: -3823,
    }


def verify_simple_saturated_point(data: dict[str, object]) -> None:
    variables = data["variables"]
    equations = data["equations"]
    point = finite_field_point(data)

    residues = [
        rational_mod_prime(equation.subs(point))
        for equation in equations
    ]
    assert residues == [0] * len(equations)
    assert len(equations) == len(variables) == 10

    jacobian = sp.Matrix(
        [
            [sp.diff(equation, variable).subs(point) for variable in variables]
            for equation in equations
        ]
    )
    determinant = rational_mod_prime(jacobian.det())
    assert determinant == 13811
    assert determinant

    assert all(
        rational_mod_prime(coefficient) != 0
        for coefficient in data["triangular_coefficients"]
    )
    assert all(
        rational_mod_prime(denominator.subs(point)) != 0
        for denominator in data["denominators"]
    )
    assert rational_mod_prime(data["lead_numerator"].subs(point)) == 23523
    assert rational_mod_prime(data["lead_denominator"].subs(point)) == 6120


def verify_polynomial_geometry(data: dict[str, object]) -> None:
    h = data["h"]
    a = data["a"]
    b = data["b"]
    point = finite_field_point(data)
    solved = data["solved"]

    X = polynomial_mod_prime(data["X"].subs(point), h)
    T = polynomial_mod_prime(data["T"].subs(solved).subs(point), h)
    W = 2 * X * T.diff() - 3 * X.diff() * T
    D = T**2 - X**3
    B = T - (point[b[3]] % PRIME) * X

    assert (X.degree(), T.degree(), W.degree(), D.degree()) == (10, 15, 4, 10)
    assert [
        int(X.coeff_monomial(h**degree)) % PRIME
        for degree in range(7)
    ] == [30276, 0, 0, 1, 25131, 8738, 17579]
    assert [
        int(B.coeff_monomial(h**degree)) % PRIME
        for degree in range(7)
    ] == [6069, 0, 0, 0, 0, 14013, 20520]

    assert sp.gcd(X, T).degree() == 0
    assert sp.gcd(X, X.diff()).degree() == 0
    assert sp.gcd(T, T.diff()).degree() == 0
    assert sp.gcd(D, D.diff()).degree() == 0
    derivative_gcd = sp.gcd(X.diff(), T.diff())
    assert derivative_gcd.monic() == sp.Poly(h**2, h, modulus=PRIME)

    assert W.monic() == sp.Poly(
        h**2 * (h - 8183) * (h + 4956),
        h,
        modulus=PRIME,
    ).monic()
    assert X.eval(0) and T.eval(0) and D.eval(0)


def verify_ramification_ledger() -> None:
    # For coprime X,T and nonzero D of degree d, the leading term in
    # X*D'-3*X'*D is (d-6r)lc(D)h^(d+2r-1).  Division by monic T gives
    # deg W=d-r-1.  The displayed contributions then exhaust
    # Riemann--Hurwitz for R=T^2/X^3 of degree 6r.
    for r in range(2, 30):
        for degree_d in range(r + 1, 2 * r + 1):
            degree_w = degree_d - r - 1
            base_ramification = (
                3 * r  # simple-root baseline over R=0
                + 4 * r  # simple-root baseline over R=infinity
                + (6 * r - degree_d - 1)  # h=infinity over R=1
            )
            assert base_ramification + degree_w == 12 * r - 2


def main() -> None:
    data = build_system()
    verify_simple_saturated_point(data)
    verify_polynomial_geometry(data)
    verify_ramification_ledger()
    print("verified the explicit F_32003 saturated (3,5) point at r=5")
    print("verified 10x10 Jacobian determinant = 13811 mod 32003")
    print("Hensel consequence: an isolated characteristic-zero lift exists")
    print("lifted degrees: deg X=10, deg T=15, deg D=10, deg W=4")
    print("marked local orders: ord(X-X0)=3, ord(B-B0)=5")
    print("derivative gcd has degree two, excluding a degree-five composition")
    print("verified the exact almost-Belyi ramification ledger")
    print("RESULT: WRONSKIAN-ONLY ALL-r ELIMINATION IS FALSE")


if __name__ == "__main__":
    main()
