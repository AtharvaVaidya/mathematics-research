#!/usr/bin/env python3
"""Exact endpoint-square reconnaissance in the seven Hamiltonian modes.

Use the canonical parameter order

    (X0,X1; X2,X3; X4,X5; X6)

for the low/high C-classes of weights (1,1,2,2,3,3,4).  In the normalized
u1=1 chart the three opposite-end mismatch coordinates are

    Y0 = X0 - 2 X1,
    Y2 = X2 - (2/3) X3,
    Y3 = X4 - X5.

The constants are structural boundary coefficients: 2 is the constant
term of U^2/w, while V'(0)=2/3 and U'(0)=1.

For k=1,2,3, exact arithmetic shows that the weight-four ideal contains

    (Y2 - kappa_k Y0^2)^2,
    kappa_k = (4k+1)^2/(16k).

The test covers the complete k=2 quadratic coefficient field and all
three k=3 Hurwitz factors.  On Y0=Y2=0, every tested scale also contains
a nonzero multiple of Y3^2 at weight six.

The longer k=1 common-factor chain is not universal.  At k=2 the second
weight-four equation has nonzero resultant with the displayed square and
already forces Y0=Y2=0.  At k=3 both weight-four rows are multiples of
the square, but after imposing it a weight-five row survives which is not
divisible by Y0.

The all-k square relation is a conjecture supported by these complete
small Hurwitz fibers, not a theorem proved by this script.  Its coefficient
does have a symbolic Hamiltonian derivation.  If xi=z*w^k, then the low Y0
and Y2 vector fields satisfy

    X_(1,1)(xi) = ((4k+1)/4) w^(k+1),
    X_(2,w)(xi) = k w^(k+2)/z,

and kappa_k=X_(1,1)(xi)^2/(xi*X_(2,w)(xi)).
"""

from __future__ import annotations

from typing import Any

import sympy as sy

from route_bd_case_c_radial_obstruction import (
    PARAMETERS as K3_PARAMETERS,
)
from route_bd_fbar_obstruction import K
from route_bd_universal_radial_consistency import (
    FQ2,
    PARAMETERS,
)
from scratch_hamiltonian_natural_obstruction import (
    natural_consistency,
    natural_consistency_k3,
)


def power(value: Any, exponent: int, one: Any) -> Any:
    result = type(value)(one)
    for _ in range(exponent):
        result *= value
    return result


def substitute(
    polynomial: Any,
    variables: tuple[Any, ...],
    replacements: dict[int, Any],
    zero: Any,
    one: Any,
) -> Any:
    result = type(polynomial)(zero)
    for monomial, coefficient in polynomial.terms.items():
        term = type(polynomial)(coefficient)
        for index, exponent in enumerate(monomial):
            term *= power(
                replacements.get(index, variables[index]),
                exponent,
                one,
            )
        result += term
    return result


def proportional(polynomial: Any, target: Any) -> bool:
    if not polynomial or not target:
        return False
    pivot = next(iter(target.terms))
    if pivot not in polynomial.terms:
        return False
    scalar = polynomial.terms[pivot] / target.terms[pivot]
    return polynomial.terms == (scalar * target).terms


def transformed_equations(
    equations: list[Any],
    variables: tuple[Any, ...],
    scalar: Any,
    zero: Any,
    one: Any,
) -> list[Any]:
    replacements = {
        0: variables[0] + scalar(2) * variables[1],
        2: variables[2] + scalar(2) / 3 * variables[3],
    }
    return [
        substitute(
            equation,
            variables,
            replacements,
            zero,
            one,
        )
        for equation in equations
    ]


def verify_scale(
    k: int,
    equations: list[Any],
    variables: tuple[Any, ...],
    scalar: Any,
    zero: Any,
    one: Any,
    expected_square_rows: int,
) -> None:
    transformed = transformed_equations(
        equations, variables, scalar, zero, one
    )
    kappa = scalar((4 * k + 1) ** 2) / (16 * k)
    square_root = (
        variables[2] - kappa * variables[0] * variables[0]
    )
    square = square_root * square_root
    weight_four = [
        equation
        for equation in transformed
        if equation and equation.weighted_degrees() == {4}
    ]
    square_rows = [
        equation
        for equation in weight_four
        if proportional(equation, square)
    ]
    assert len(square_rows) == expected_square_rows

    imposed = [
        substitute(
            equation,
            variables,
            {2: kappa * variables[0] * variables[0]},
            zero,
            one,
        )
        for equation in transformed
    ]
    imposed_weight_four = [
        equation
        for equation in imposed
        if equation and equation.weighted_degrees() == {4}
    ]
    if k == 2:
        assert len(imposed_weight_four) == 1
        assert set(imposed_weight_four[0].terms) == {
            (4, 0, 0, 0, 0, 0, 0)
        }
    if k == 3:
        assert not imposed_weight_four
        weight_five = [
            equation
            for equation in imposed
            if equation and equation.weighted_degrees() == {5}
        ]
        assert len(weight_five) == 1
        assert min(
            monomial[0] for monomial in weight_five[0].terms
        ) == 0

    boundary_replacements = {
        0: scalar(2) * variables[1],
        2: scalar(2) / 3 * variables[3],
    }
    boundary = [
        substitute(
            equation,
            variables,
            boundary_replacements,
            zero,
            one,
        )
        for equation in equations
    ]
    y3_square = (
        variables[4] - variables[5]
    ) * (
        variables[4] - variables[5]
    )
    weight_six = [
        equation
        for equation in boundary
        if equation and equation.weighted_degrees() == {6}
    ]
    assert any(
        proportional(equation, y3_square)
        for equation in weight_six
    )


def verify_symbolic_kappa_ratio() -> None:
    z, w = sy.symbols("z w", nonzero=True)
    k = sy.symbols("k", integer=True, positive=True)
    xi = z * w**k

    def x_low_one(polynomial: sy.Expr) -> sy.Expr:
        return sy.expand(
            w * sy.diff(polynomial, z) / 4
            + w**2 * sy.diff(polynomial, w) / z
        )

    def x_low_two(polynomial: sy.Expr) -> sy.Expr:
        return sy.expand(
            w**3 * sy.diff(polynomial, w) / z**2
        )

    first = sy.factor(x_low_one(xi))
    second = sy.factor(x_low_two(xi))
    assert sy.simplify(
        first - (4 * k + 1) * w ** (k + 1) / 4
    ) == 0
    assert sy.simplify(
        second - k * w ** (k + 2) / z
    ) == 0
    ratio = sy.factor(first**2 / (xi * second))
    assert ratio == (4 * k + 1) ** 2 / (16 * k)


def main() -> None:
    verify_symbolic_kappa_ratio()
    verify_scale(
        1,
        natural_consistency(1, max_deficit=6),
        PARAMETERS,
        FQ2,
        FQ2(),
        FQ2(1),
        expected_square_rows=1,
    )
    verify_scale(
        2,
        natural_consistency(2, max_deficit=6),
        PARAMETERS,
        FQ2,
        FQ2(),
        FQ2(1),
        expected_square_rows=1,
    )
    for outer_parameter in (K(26839), K(16621), K(0, 1)):
        verify_scale(
            3,
            natural_consistency_k3(
                outer_parameter, max_deficit=6
            ),
            K3_PARAMETERS,
            K,
            K(),
            K(1),
            expected_square_rows=2,
        )
    print("verified endpoint square at k=1,2 and every k=3 factor")
    print("derived kappa symbolically from the two low vector fields")
    print("verified kappa=(4k+1)^2/(16k) for k=1,2,3")
    print("verified the k=1 common-factor chain fails at k=2,3")
    print("verified Y3^2 on Y0=Y2=0 at every tested scale")
    print("the all-k kappa formula remains conjectural")


if __name__ == "__main__":
    main()
