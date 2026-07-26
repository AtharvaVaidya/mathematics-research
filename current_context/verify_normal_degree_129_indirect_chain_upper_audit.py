#!/usr/bin/env python3
"""Audit the order-13 indirect chain with every upper constant retained."""

import sympy as sp


X = sp.symbols("X")
a, c, k = sp.symbols("a c k", nonzero=True)
P = X**3 - 1
j = -sp.Rational(2, 3) * c

S_EQUAL = -sp.Rational(1, 2) * X**2 * (X**3 - 3)
Q_EQUAL = X
S_MIXED = -(
    3 * X**5
    - 2 * X**4
    + 2 * X**3
    - 9 * X**2
    + 14 * X
    + 10
) / 18
Q_MIXED = -(2 * X**2 - X + 2) / 3

assert sp.rem(Q_EQUAL * S_EQUAL, P, X) == 1
assert sp.rem(Q_MIXED * S_MIXED, P, X) == 1


def quotient(numerator, denominator):
    return sp.div(sp.expand(numerator), denominator, X)[0]


def audit_orbit(S, principal_q):
    """Return the delayed order-18 value and final order-47 residuals."""
    jets = {
        0: P**3,
        12: c * P,
        13: a * P * principal_q,
        17: S,
    }
    q_by_order = {}
    delayed_q18 = None

    def f_coefficient(order):
        if order == 0:
            return P**4

        value = sp.Rational(4, 3) * P * jets.get(order, 0)
        quadratic = sum(
            (
                jets[i] * jets[order - i]
                for i in jets
                if i > 0 and order - i in jets and order - i > 0
            ),
            sp.Integer(0),
        )
        value += sp.Rational(2, 9) * quotient(quadratic, P**2)

        cubic = sum(
            (
                jets[i] * jets[ell] * jets[order - i - ell]
                for i in jets
                for ell in jets
                if i > 0
                and ell > 0
                and order - i - ell in jets
                and order - i - ell > 0
            ),
            sp.Integer(0),
        )
        value -= sp.Rational(4, 81) * quotient(cubic, P**5)

        # Since deg(delta)<6, these are the exact polynomial parts of
        # g^(2/3) and g^(1/3), not truncated approximations.
        if order == 12:
            value += j * P**2
        elif order > 12:
            value += (
                sp.Rational(2, 3)
                * j
                * quotient(jets.get(order - 12, 0), P)
            )
        if order == 18:
            value += k * P
        return sp.expand(value)

    def pair(f_order, f_value, g_order, g_value):
        return sp.expand(
            (f_order - 24) * f_value * sp.diff(g_value, X)
            + (18 - g_order) * sp.diff(f_value, X) * g_value
        )

    def bracket_coefficient(order):
        return sp.expand(
            sum(
                (
                    pair(
                        f_order,
                        f_coefficient(f_order),
                        order - f_order,
                        jets[order - f_order],
                    )
                    for f_order in range(order + 1)
                    if f_coefficient(f_order) != 0
                    and order - f_order in jets
                ),
                sp.Integer(0),
            )
        )

    # The principal q is the complete order-13 kernel.  Together with
    # C=2c+3j=0, it makes every coefficient below the first descendant
    # equation vanish.
    for bracket_order in range(1, 31):
        assert bracket_coefficient(bracket_order) == 0

    for bracket_order in range(31, 48):
        remainder_order = bracket_order - 13
        quotient_order = bracket_order - 17
        bvars = sp.symbols(f"b{remainder_order}_0:3")
        qvars = sp.symbols(f"q{quotient_order}_0:3")
        remainder = sum(bvars[i] * X**i for i in range(3))
        multiple = P * sum(qvars[i] * X**i for i in range(3))
        jets[remainder_order] = sp.expand(
            jets.get(remainder_order, 0) + remainder
        )
        jets[quotient_order] = sp.expand(
            jets.get(quotient_order, 0) + multiple
        )
        q_by_order[quotient_order] = qvars

        expression = bracket_coefficient(bracket_order)
        polynomial = sp.Poly(expression, X)
        degrees = range(1, 13) if bracket_order == 34 else range(13)
        equations = [
            sp.expand(polynomial.coeff_monomial(X**degree))
            for degree in degrees
        ]

        matrix, rhs = sp.linear_eq_to_matrix(equations, bvars)
        independent_rows = list(sp.Matrix(matrix.T).rref()[1])
        assert len(independent_rows) == 3
        solution_vector = (
            matrix[independent_rows, :].inv() * rhs[independent_rows, :]
        )
        remainder_solution = {
            bvars[i]: sp.cancel(solution_vector[i])
            for i in range(3)
        }
        jets[remainder_order] = sp.expand(
            jets[remainder_order].subs(remainder_solution)
        )

        reduced = [
            sp.expand(equation.subs(remainder_solution))
            for equation in equations
        ]
        constraints = []
        for equation in reduced:
            if (
                equation != 0
                and equation not in constraints
                and -equation not in constraints
            ):
                constraints.append(equation)

        target_order = bracket_order - 21
        if not constraints:
            continue
        target = q_by_order[target_order]
        solutions = sp.solve(
            constraints,
            target,
            dict=True,
            simplify=False,
        )
        if bracket_order == 47:
            assert solutions == []
            partial = sp.solve(
                constraints[:3],
                target,
                dict=True,
                simplify=False,
            )
            assert len(partial) == 1
            residuals = [
                sp.factor(constraint.subs(partial[0]))
                for constraint in constraints[3:]
            ]
            return delayed_q18, partial[0], residuals

        assert len(solutions) == 1
        substitution = solutions[0]
        if target_order == 18:
            delayed_q18 = substitution
        for order in list(jets):
            jets[order] = sp.expand(jets[order].subs(substitution))

    raise AssertionError("the order-47 obstruction was not reached")


equal_q18, equal_partial, equal_residuals = audit_orbit(
    S_EQUAL,
    Q_EQUAL,
)
mixed_q18, mixed_partial, mixed_residuals = audit_orbit(
    S_MIXED,
    Q_MIXED,
)

assert equal_q18 == {
    sp.symbols("q18_0"): -a**4 / 9,
    sp.symbols("q18_1"): 0,
    sp.symbols("q18_2"): 0,
}
assert mixed_q18 == equal_q18

assert equal_partial[sp.symbols("q26_0")] == 0
assert equal_partial[sp.symbols("q26_1")] == 0
assert equal_residuals == [0, sp.Rational(189, 4) * a]

assert mixed_partial[sp.symbols("q26_0")] == -a**2 / 54
assert mixed_partial[sp.symbols("q26_1")] == -sp.Rational(139, 432) * a**2
assert mixed_residuals == [
    -sp.Rational(1729, 108) * a,
    sp.Rational(63, 4) * a,
]

print("verified upper-constant-stable order-47 indirect-chain obstruction")
