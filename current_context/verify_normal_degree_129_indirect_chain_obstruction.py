#!/usr/bin/env python3
"""All-character check for the earlier (order-13) indirect chain."""

import sympy as sp


X = sp.symbols("X")
P = X**3 - 1
a = sp.symbols("a", nonzero=True)

S_equal = -sp.Rational(1, 2) * X**2 * (X**3 - 3)
q_equal = X

S_mixed = -(
    3 * X**5
    - 2 * X**4
    + 2 * X**3
    - 9 * X**2
    + 14 * X
    + 10
) / 18
q_mixed = -(2 * X**2 - X + 2) / 3

assert sp.rem(q_equal * S_equal, P, X) == 1
assert sp.rem(q_mixed * S_mixed, P, X) == 1


def quotient(poly, divisor):
    return sp.div(sp.expand(poly), divisor, X)[0]


def triangular_obstruction(S, q):
    """Retain all three kernel characters and return the order-47 constraints."""
    jets = {
        13: a * P * q,
        17: S,
    }
    active_parameters = []
    parameter_index = 0
    order_39_quotient = None

    def f_coefficient(order):
        if order == 0:
            return P**4

        value = sp.Rational(4, 3) * P * jets.get(order, 0)
        quadratic = sum(
            (
                jets.get(i, 0) * jets.get(order - i, 0)
                for i in range(13, order - 12)
            ),
            sp.Integer(0),
        )
        value += sp.Rational(2, 9) * quotient(quadratic, P**2)

        cubic = sum(
            (
                jets.get(i, 0)
                * jets.get(j, 0)
                * jets.get(order - i - j, 0)
                for i in range(13, order - 25)
                for j in range(13, order - i - 12)
                if order - i - j >= 13
            ),
            sp.Integer(0),
        )
        value -= sp.Rational(4, 81) * quotient(cubic, P**5)
        return sp.expand(value)

    def g_coefficient(order):
        return P**3 if order == 0 else jets.get(order, 0)

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
                        i,
                        f_coefficient(i),
                        order - i,
                        g_coefficient(order - i),
                    )
                    for i in range(order + 1)
                    if f_coefficient(i) != 0
                    and g_coefficient(order - i) != 0
                ),
                sp.Integer(0),
            )
        )

    def substitute_everywhere(substitution):
        nonlocal jets, active_parameters
        jets = {
            order: sp.factor(value.subs(substitution))
            for order, value in jets.items()
        }
        active_parameters = [
            parameter
            for parameter in active_parameters
            if parameter not in substitution
        ]

    for bracket_order in range(26, 48):
        jet_order = bracket_order - 13
        if jet_order in jets:
            expression = bracket_coefficient(bracket_order)
            current_variables = []
        else:
            coefficients = sp.symbols(f"x{jet_order}_0:6")
            jets[jet_order] = sum(
                coefficients[i] * X**i for i in range(6)
            )
            current_variables = list(coefficients)
            expression = bracket_coefficient(bracket_order)

        if bracket_order == 34:
            scalar = sp.symbols("scalar")
            current_variables.append(scalar)
            expression -= scalar

        equations = sp.Poly(expression, X).all_coeffs()

        while current_variables:
            matrix, rhs = sp.linear_eq_to_matrix(
                equations, current_variables
            )
            constraints = [
                sp.factor((left.T * rhs)[0])
                for left in matrix.T.nullspace()
                if sp.factor((left.T * rhs)[0]) != 0
            ]
            if not constraints:
                break

            if bracket_order == 47:
                return constraints, order_39_quotient

            solutions = sp.solve(
                constraints,
                active_parameters,
                dict=True,
                simplify=False,
            )
            assert len(solutions) == 1
            substitution = solutions[0]
            substitute_everywhere(substitution)
            equations = [
                sp.factor(equation.subs(substitution))
                for equation in equations
            ]

        if not current_variables:
            assert all(equation == 0 for equation in equations)
            continue

        solution_set = sp.linsolve(equations, current_variables)
        assert solution_set is not sp.EmptySet

        solution = next(iter(solution_set))
        current_set = set(current_variables)
        free_current = (
            set().union(*(entry.free_symbols for entry in solution))
            & current_set
        )
        free_substitution = {}
        for free_symbol in sorted(free_current, key=str):
            parameter_index += 1
            parameter = sp.symbols(f"p{parameter_index}")
            active_parameters.append(parameter)
            free_substitution[free_symbol] = parameter

        solution = tuple(
            sp.factor(entry.subs(free_substitution))
            for entry in solution
        )
        variable_substitution = {
            current_variables[i]: solution[i]
            for i in range(len(current_variables))
        }
        jets[jet_order] = sp.factor(
            jets[jet_order].subs(variable_substitution)
        )
        if bracket_order == 39:
            # The apparent order-39 obstruction cancels through the
            # delayed P-multiple already introduced at jet order 18.
            order_39_quotient = sp.factor(quotient(jets[18], P))
            assert order_39_quotient == -a**4 / 9

    raise AssertionError("order-47 obstruction was not reached")


equal_constraints, equal_order_39_quotient = triangular_obstruction(
    S_equal, q_equal
)
mixed_constraints, mixed_order_39_quotient = triangular_obstruction(
    S_mixed, q_mixed
)
assert equal_order_39_quotient == -a**4 / 9
assert mixed_order_39_quotient == -a**4 / 9

# The equal-sign constraints force the last triple to zero and then
# demand a nonzero value for the same component.
equal_solution = sp.solve(equal_constraints[:3], dict=True)
assert len(equal_solution) == 1
equal_residuals = [
    sp.factor(constraint.subs(equal_solution[0]))
    for constraint in equal_constraints[3:]
]
assert any(residual != 0 for residual in equal_residuals)
assert sp.solve(equal_constraints, dict=True) == []

# The mixed-sign final system has the explicit residual pair in the note.
mixed_variables = sorted(
    set().union(*(constraint.free_symbols for constraint in mixed_constraints))
    - {a},
    key=str,
)
mixed_solution = sp.solve(
    mixed_constraints[:3],
    mixed_variables,
    dict=True,
)
assert len(mixed_solution) == 1
mixed_residuals = [
    sp.factor(constraint.subs(mixed_solution[0]))
    for constraint in mixed_constraints[3:]
]
assert mixed_residuals == [-2 * a, sp.Rational(28, 27) * a]
assert sp.solve(mixed_constraints, mixed_variables, dict=True) == []


print("verified all-character obstruction of the order-13 indirect chain")
