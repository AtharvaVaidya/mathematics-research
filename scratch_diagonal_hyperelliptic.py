#!/usr/bin/env python3
"""Classify exactness on the global diagonal genus-three face.

For the monic degree-seven diagonal polynomial C(q), exactness of
q^16 dq / Y^5 on Y^2=C is equivalent to

    2*C*R' - 3*C'*R = 2*q^16

with deg(R)<=10.  The high coefficients solve R triangularly; this script
prints the six remaining exactness conditions in the coefficients of C.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    q = sp.symbols("q")
    coefficients = sp.symbols("c0:7")
    r = sp.symbols("r0:11")
    c = q**7 + sum(coefficients[index] * q**index for index in range(7))
    primitive = sum(r[index] * q**index for index in range(11))
    equation = sp.Poly(
        sp.expand(
            2 * c * sp.diff(primitive, q)
            - 3 * sp.diff(c, q) * primitive
            - 2 * q**16
        ),
        q,
    )

    substitutions: dict[sp.Symbol, sp.Expr] = {}
    for degree in range(16, 5, -1):
        coefficient = sp.expand(
            equation.coeff_monomial(q**degree).subs(substitutions)
        )
        variable = r[degree - 6]
        solution = sp.solve(coefficient, variable, dict=False)
        assert len(solution) == 1
        substitutions[variable] = sp.factor(solution[0])
        assert (
            sp.expand(coefficient.subs(variable, substitutions[variable]))
            == 0
        )

    print("R SOLUTION")
    for variable in reversed(r):
        print(variable, "=", substitutions[variable])

    print("REMAINDERS")
    remainders = []
    for degree in range(6):
        remainder = sp.factor(
            equation.coeff_monomial(q**degree).subs(substitutions)
        )
        remainders.append(remainder)
        print("q^", degree, ":", remainder)

    # The constant coefficient is nonzero on the case-c diagonal face.
    saturated = [
        sp.factor(remainder / coefficients[0])
        if remainder != 0 and sp.rem(
            sp.Poly(remainder, coefficients[0]),
            sp.Poly(coefficients[0], coefficients[0]),
        )
        == 0
        else remainder
        for remainder in remainders
    ]
    print("CONSTANT-NONZERO REMAINDERS")
    for remainder in saturated:
        print(remainder)


if __name__ == "__main__":
    main()
