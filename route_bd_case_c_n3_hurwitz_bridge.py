#!/usr/bin/env python3
"""Bridge the first integral compatibility to the five outer Hurwitz points.

The integral normal form says that grade n=3 is the first row with no new
S-coefficient.  A coefficient z^j y^3 in that row has radial degree j-3
for w=z*y.  Its z^7 coefficient is the outer equation, the z^6,z^5,z^4
coefficients are the first three radial descents, and z^3 is radial
deficit four.

This verifier checks on the complete reduced five-point outer fiber that
the first three descents are automatic and that deficit four consists of
two nonzero multiples of

    (Y2 - 169*Y0^2/48)^2,

where Y0=X0-2X1 and Y2=X2-2X3/3 are the canonical opposite-endpoint
coordinates.  Thus n=3 genuinely cuts the lower modes, but only by one
radical equation; it is not a contradiction.

At deficit five there is one weight-five survivor.  The verifier also
checks that it is triangularly solvable: off an outer-dependent linear
divisor it determines X6, while on that divisor its X4/X5 coefficient
matrix is invertible in the two variables (X3,Y0^2).  Hence the survivor
never empties a lower-mode fiber, and the next possible obstruction lies
at a later radial layer.

At deficit six the same finite cover becomes informative.  The first two
charts are genuinely cut; the chart L=A=0,B!=0 is empty by a nonzero
quadratic resultant; and the deepest chart forces X4=X5=0 while leaving
X6 free.  Deficit seven is automatic on that deepest chart, while its
five deficit-eight rows are nonzero multiples of X6^2 and force X6=0.

The default check is the fast exact F_32003 audit over the two rational
points and the cubic factor.  ``--exact-lift`` reconstructs the outer
five-point algebra over Q and repeats the four-stage calculation there.
It is intentionally not part of the fast bundled verifier.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from fractions import Fraction
from typing import ClassVar

import sympy as sp

from route_bd_ab_outer_lift import (
    WORKERS,
    lift_coefficients,
    modular_lex_basis,
    quotient_data,
    reconstruction_primes,
)
from route_bd_case_c_radial_obstruction import (
    PARAMETERS as MODULAR_PARAMETERS,
)
from route_bd_fbar_obstruction import K
from route_bd_universal_hamiltonian_endpoint_squares import (
    proportional,
    substitute,
    transformed_equations,
    verify_symbolic_kappa_ratio,
)
from scratch_hamiltonian_natural_obstruction import (
    natural_consistency_k3,
)


WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
NVAR = len(WEIGHTS)
KAPPA = sp.Rational(169, 48)


def verify_grade_radial_dictionary() -> None:
    """Check which radial stages occur inside the n=3 integral row."""
    integral_grade = 3
    dictionary = {
        z_degree: z_degree - integral_grade
        for z_degree in range(3, 8)
    }
    assert dictionary == {3: 0, 4: 1, 5: 2, 6: 3, 7: 4}
    # The outer bracket has radial degree four.  Descending radial
    # deficits 1,2,3,4 therefore correspond to degrees 3,2,1,0.
    assert {
        deficit: 4 - deficit for deficit in range(1, 5)
    } == {1: 3, 2: 2, 3: 1, 4: 0}


def parameter_coefficient(
    polynomial: object,
    variable: int,
    exponent: int,
) -> object:
    """Extract a coefficient while retaining the seven-variable format."""
    return type(polynomial)(
        terms={
            tuple(
                0 if index == variable else value
                for index, value in enumerate(monomial)
            ): coefficient
            for monomial, coefficient in polynomial.terms.items()
            if monomial[variable] == exponent
        }
    )


def small_determinant(matrix: list[list[object]], zero: object) -> object:
    """Determinant for the 3x3 and 4x4 certificate matrices below."""
    from itertools import permutations

    size = len(matrix)
    result = zero
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = matrix[0][permutation[0]]
        for row in range(1, size):
            term *= matrix[row][permutation[row]]
        result += -term if inversions % 2 else term
    return result


def univariate_coefficients(
    polynomial: object,
    variable: int,
) -> dict[int, object]:
    result: dict[int, object] = {}
    for monomial, coefficient in polynomial.terms.items():
        assert all(
            exponent == 0
            for index, exponent in enumerate(monomial)
            if index != variable
        )
        result[monomial[variable]] = coefficient
    return result


def quadratic_resultant(
    left: dict[int, object],
    right: dict[int, object],
    zero: object,
) -> object:
    """Resultant of two degree-at-most-two univariate polynomials."""
    left_row = [left.get(index, zero) for index in (2, 1, 0)]
    right_row = [right.get(index, zero) for index in (2, 1, 0)]
    return small_determinant(
        [
            [*left_row, zero],
            [zero, *left_row],
            [*right_row, zero],
            [zero, *right_row],
        ],
        zero,
    )


def verify_modular_five_point_square() -> None:
    """Verify the square and the exhaustive deficit-six triangular cover."""
    square_root = (
        MODULAR_PARAMETERS[2]
        - K(169)
        / 48
        * MODULAR_PARAMETERS[0]
        * MODULAR_PARAMETERS[0]
    )
    square = square_root * square_root
    for outer_parameter in (K(26839), K(16621), K(0, 1)):
        equations = natural_consistency_k3(
            outer_parameter,
            max_deficit=8,
        )
        transformed = transformed_equations(
            equations,
            MODULAR_PARAMETERS,
            K,
            K(),
            K(1),
        )
        weight_four = [
            equation
            for equation in transformed
            if equation and equation.weighted_degrees() == {4}
        ]
        # Deficits one through three have zero consistency rows, and
        # deficit four contributes precisely the two displayed squares.
        assert len(weight_four) == 2
        assert all(proportional(equation, square) for equation in weight_four)

        imposed = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {
                    2: K(169)
                    / 48
                    * MODULAR_PARAMETERS[0]
                    * MODULAR_PARAMETERS[0],
                },
                K(),
                K(1),
            )
            for equation in transformed
        ]
        assert not [
            equation
            for equation in imposed
            if equation and equation.weighted_degrees() == {4}
        ]
        weight_five = [
            equation
            for equation in imposed
            if equation and equation.weighted_degrees() == {5}
        ]
        # The next radial layer has one genuinely new condition.  Since
        # it is not divisible by Y0, the square branch cannot be reduced
        # to the special subbranch Y0=0 without losing solutions.
        assert len(weight_five) == 1
        assert min(monomial[0] for monomial in weight_five[0].terms) == 0

        survivor = weight_five[0]
        x6_x1 = survivor.terms[(0, 1, 0, 0, 0, 0, 1)]
        x6_y0 = survivor.terms[(1, 0, 0, 0, 0, 0, 1)]
        assert x6_x1 and x6_y0
        x1_on_exceptional_divisor = (
            -x6_y0 / x6_x1 * MODULAR_PARAMETERS[0]
        )
        exceptional = substitute(
            survivor,
            MODULAR_PARAMETERS,
            {1: x1_on_exceptional_divisor},
            K(),
            K(1),
        )
        expected_support = {
            (0, 0, 0, 1, 0, 1, 0),
            (0, 0, 0, 1, 1, 0, 0),
            (2, 0, 0, 0, 0, 1, 0),
            (2, 0, 0, 0, 1, 0, 0),
            (1, 0, 0, 2, 0, 0, 0),
            (3, 0, 0, 1, 0, 0, 0),
            (5, 0, 0, 0, 0, 0, 0),
        }
        assert set(exceptional.terms) == expected_support
        coefficient_determinant = (
            exceptional.terms[(0, 0, 0, 1, 0, 1, 0)]
            * exceptional.terms[(2, 0, 0, 0, 1, 0, 0)]
            - exceptional.terms[(0, 0, 0, 1, 1, 0, 0)]
            * exceptional.terms[(2, 0, 0, 0, 0, 1, 0)]
        )
        assert coefficient_determinant

        weight_six = [
            equation
            for equation in imposed
            if equation and equation.weighted_degrees() == {6}
        ]
        assert len(weight_six) == 3

        # Chart 1: off L=coefficient(F5,X6), eliminate X6.  All three
        # cleared deficit-six rows survive and are pairwise nonproportional.
        linear_form = parameter_coefficient(survivor, 6, 1)
        survivor_without_x6 = parameter_coefficient(survivor, 6, 0)
        chart_one_rows = [
            linear_form * parameter_coefficient(equation, 6, 0)
            - parameter_coefficient(equation, 6, 1)
            * survivor_without_x6
            for equation in weight_six
        ]
        assert all(chart_one_rows)
        assert all(
            not proportional(chart_one_rows[left], chart_one_rows[right])
            for left in range(3)
            for right in range(left + 1, 3)
        )

        # On L=0 write F5=A*X5+B*X4+C.  The determinant checked above
        # says that A=B=0 is equivalent, set-theoretically, to
        # (X3,Y0^2)=(0,0).
        exceptional_weight_six = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {1: x1_on_exceptional_divisor},
                K(),
                K(1),
            )
            for equation in weight_six
        ]
        coefficient_x5 = parameter_coefficient(exceptional, 5, 1)
        coefficient_x4 = parameter_coefficient(exceptional, 4, 1)
        remainder_after_x5 = parameter_coefficient(exceptional, 5, 0)
        assert coefficient_x5 and coefficient_x4

        # Chart 2: L=0,A!=0.  Eliminate X5 by the linear F5 row.
        # One cleared deficit-six equation is independent of X6 and
        # nonzero, so this layer genuinely cuts rather than merely
        # choosing X6.
        chart_two_rows = []
        for equation in exceptional_weight_six:
            constant = parameter_coefficient(equation, 5, 0)
            linear = parameter_coefficient(equation, 5, 1)
            quadratic = parameter_coefficient(equation, 5, 2)
            chart_two_rows.append(
                coefficient_x5 * coefficient_x5 * constant
                - coefficient_x5 * linear * remainder_after_x5
                + quadratic * remainder_after_x5 * remainder_after_x5
            )
        assert all(chart_two_rows)
        chart_two_x6_coefficients = [
            parameter_coefficient(equation, 6, 1)
            for equation in chart_two_rows
        ]
        assert sum(bool(value) for value in chart_two_x6_coefficients) == 2

        # Chart 3: L=A=0,B!=0.  A is a unit-coefficient linear form in
        # X3 and Y0^2, so solve A=0 for X3 and F5=0 for X4.
        a_x3 = coefficient_x5.terms[(0, 0, 0, 1, 0, 0, 0)]
        a_y0_square = coefficient_x5.terms[(2, 0, 0, 0, 0, 0, 0)]
        x3_on_a_zero = (
            -a_y0_square
            / a_x3
            * MODULAR_PARAMETERS[0]
            * MODULAR_PARAMETERS[0]
        )
        chart_three_replacements = {
            1: x1_on_exceptional_divisor,
            3: x3_on_a_zero,
        }
        chart_three_survivor = substitute(
            survivor,
            MODULAR_PARAMETERS,
            chart_three_replacements,
            K(),
            K(1),
        )
        assert not parameter_coefficient(chart_three_survivor, 5, 1)
        chart_three_x4 = parameter_coefficient(
            chart_three_survivor, 4, 1
        )
        assert set(chart_three_x4.terms) == {
            (2, 0, 0, 0, 0, 0, 0)
        }
        chart_three_remainder = parameter_coefficient(
            chart_three_survivor, 4, 0
        )
        chart_three_rows = []
        for equation in weight_six:
            restricted = substitute(
                equation,
                MODULAR_PARAMETERS,
                chart_three_replacements,
                K(),
                K(1),
            )
            constant = parameter_coefficient(restricted, 4, 0)
            linear = parameter_coefficient(restricted, 4, 1)
            quadratic = parameter_coefficient(restricted, 4, 2)
            chart_three_rows.append(
                chart_three_x4 * chart_three_x4 * constant
                - chart_three_x4 * linear * chart_three_remainder
                + quadratic
                * chart_three_remainder
                * chart_three_remainder
            )

        # B!=0 is the same as Y0!=0 on this chart, so normalize Y0=1.
        one_parameter = type(survivor)(K(1))
        normalized_chart_three = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {0: one_parameter},
                K(),
                K(1),
            )
            for equation in chart_three_rows
        ]
        x6_coefficients = [
            parameter_coefficient(equation, 6, 1)
            for equation in normalized_chart_three
        ]
        linear_indices = [
            index for index, coefficient in enumerate(x6_coefficients)
            if coefficient
        ]
        independent_indices = [
            index for index, coefficient in enumerate(x6_coefficients)
            if not coefficient
        ]
        assert len(linear_indices) == 2
        assert len(independent_indices) == 1
        x6_scalars = []
        x6_free_parts = []
        for index in linear_indices:
            assert set(x6_coefficients[index].terms) == {(0,) * NVAR}
            x6_scalars.append(
                x6_coefficients[index].terms[(0,) * NVAR]
            )
            x6_free_parts.append(
                parameter_coefficient(
                    normalized_chart_three[index], 6, 0
                )
            )
        x6_compatibility = (
            x6_scalars[0] * x6_free_parts[1]
            - x6_scalars[1] * x6_free_parts[0]
        )
        independent_equation = normalized_chart_three[
            independent_indices[0]
        ]
        resultant = quadratic_resultant(
            univariate_coefficients(independent_equation, 5),
            univariate_coefficients(x6_compatibility, 5),
            K(),
        )
        # The nonzero resultant proves that chart 3 is empty at deficit
        # six, over the algebraic closure of every outer factor.
        assert resultant

        # Chart 4: L=A=B=0, equivalently Y0=X1=X3=0.  The three
        # quadratic rows span X4^2,X4*X5,X5^2, hence force X4=X5=0
        # set-theoretically; X6 remains free at this layer.
        zero_parameter = type(survivor)()
        deepest_rows = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {
                    0: zero_parameter,
                    1: zero_parameter,
                    2: zero_parameter,
                    3: zero_parameter,
                },
                K(),
                K(1),
            )
            for equation in weight_six
        ]
        deepest_monomials = [
            (0, 0, 0, 0, 2, 0, 0),
            (0, 0, 0, 0, 1, 1, 0),
            (0, 0, 0, 0, 0, 2, 0),
        ]
        assert all(
            set(equation.terms) == set(deepest_monomials)
            for equation in deepest_rows
        )
        deepest_matrix = [
            [
                equation.terms[monomial]
                for monomial in deepest_monomials
            ]
            for equation in deepest_rows
        ]
        assert small_determinant(deepest_matrix, K())

        # The deepest branch now has only X6.  Deficit seven is
        # automatic by the weight grading.  At deficit eight there are
        # five nonzero rows, all scalar multiples of X6^2, so this last
        # mode is forced to zero set-theoretically.
        deepest_all_rows = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {
                    0: zero_parameter,
                    1: zero_parameter,
                    2: zero_parameter,
                    3: zero_parameter,
                    4: zero_parameter,
                    5: zero_parameter,
                },
                K(),
                K(1),
            )
            for equation in imposed
        ]
        assert not [
            equation
            for equation in deepest_all_rows
            if equation and equation.weighted_degrees() == {7}
        ]
        deepest_weight_eight = [
            equation
            for equation in deepest_all_rows
            if equation and equation.weighted_degrees() == {8}
        ]
        x6_square = (
            MODULAR_PARAMETERS[6] * MODULAR_PARAMETERS[6]
        )
        assert len(deepest_weight_eight) == 5
        assert all(
            proportional(equation, x6_square)
            for equation in deepest_weight_eight
        )


@dataclass(frozen=True)
class QuotientElement:
    """An exact element of Q[s]/(f), stored in the power basis."""

    coefficients: tuple[sp.Rational, ...]

    modulus: ClassVar[sp.Poly | None] = None
    relation: ClassVar[tuple[sp.Rational, ...] | None] = None

    @classmethod
    def configure(cls, modulus: sp.Poly) -> None:
        cls.modulus = modulus
        assert modulus.LC() == 1
        cls.relation = tuple(
            sp.Rational(modulus.nth(index))
            for index in range(modulus.degree())
        )

    @classmethod
    def coerce(cls, value: object) -> "QuotientElement":
        if isinstance(value, cls):
            return value
        assert cls.modulus is not None
        if isinstance(value, Fraction):
            return cls(
                (
                    sp.Rational(value.numerator, value.denominator),
                    *(sp.Integer(0) for _ in range(cls.modulus.degree() - 1)),
                )
            )
        if isinstance(value, (int, sp.Integer, sp.Rational)):
            return cls(
                (
                    sp.Rational(value),
                    *(sp.Integer(0) for _ in range(cls.modulus.degree() - 1)),
                )
            )
        polynomial = sp.Poly(
            sp.sympify(value),
            cls.modulus.gens[0],
            domain=sp.QQ,
        )
        remainder = sp.rem(polynomial, cls.modulus)
        return cls(
            tuple(
                sp.Rational(remainder.nth(index))
                for index in range(cls.modulus.degree())
            )
        )

    def expression(self) -> sp.Expr:
        assert self.modulus is not None
        variable = self.modulus.gens[0]
        return sum(
            coefficient * variable**index
            for index, coefficient in enumerate(self.coefficients)
        )

    def __bool__(self) -> bool:
        return any(self.coefficients)

    def __add__(self, other: object) -> "QuotientElement":
        other = self.coerce(other)
        return type(self)(
            tuple(
                left + right
                for left, right in zip(
                    self.coefficients,
                    other.coefficients,
                )
            )
        )

    __radd__ = __add__

    def __neg__(self) -> "QuotientElement":
        return type(self)(tuple(-value for value in self.coefficients))

    def __sub__(self, other: object) -> "QuotientElement":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "QuotientElement":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "QuotientElement":
        other = self.coerce(other)
        assert self.modulus is not None
        assert self.relation is not None
        degree = self.modulus.degree()
        product = [sp.Integer(0)] * (2 * degree - 1)
        for left_index, left in enumerate(self.coefficients):
            for right_index, right in enumerate(other.coefficients):
                product[left_index + right_index] += left * right
        for exponent in range(2 * degree - 2, degree - 1, -1):
            coefficient = product[exponent]
            if not coefficient:
                continue
            product[exponent] = sp.Integer(0)
            offset = exponent - degree
            for index, relation_coefficient in enumerate(self.relation):
                product[offset + index] -= (
                    coefficient * relation_coefficient
                )
        return type(self)(tuple(product[:degree]))

    __rmul__ = __mul__

    def inverse(self) -> "QuotientElement":
        assert self.modulus is not None
        inverse = sp.invert(
            sp.Poly(
                self.expression(),
                self.modulus.gens[0],
                domain=sp.QQ,
            ),
            self.modulus,
        )
        return self.coerce(inverse.as_expr())

    def __truediv__(self, other: object) -> "QuotientElement":
        return self * self.coerce(other).inverse()

    def __pow__(self, exponent: int) -> "QuotientElement":
        assert exponent >= 0
        result = self.coerce(1)
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result *= base
            base *= base
            remaining >>= 1
        return result


@dataclass
class ParameterPolynomial:
    """A polynomial in the seven modes over the exact outer quotient."""

    terms: dict[tuple[int, ...], QuotientElement]

    def __init__(
        self,
        value: object = 0,
        terms: dict[tuple[int, ...], QuotientElement] | None = None,
    ) -> None:
        if terms is None:
            coefficient = QuotientElement.coerce(value)
            self.terms = (
                {(0,) * NVAR: coefficient} if coefficient else {}
            )
        else:
            self.terms = {
                monomial: coefficient
                for monomial, coefficient in terms.items()
                if coefficient
            }

    @classmethod
    def variable(cls, index: int) -> "ParameterPolynomial":
        exponent = [0] * NVAR
        exponent[index] = 1
        return cls(
            terms={
                tuple(exponent): QuotientElement.coerce(1),
            }
        )

    @classmethod
    def coerce(cls, value: object) -> "ParameterPolynomial":
        return value if isinstance(value, cls) else cls(value)

    def __bool__(self) -> bool:
        return bool(self.terms)

    def __add__(self, other: object) -> "ParameterPolynomial":
        other = self.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = (
                result.get(monomial, QuotientElement.coerce(0))
                + coefficient
            )
            if not result[monomial]:
                del result[monomial]
        return type(self)(terms=result)

    __radd__ = __add__

    def __neg__(self) -> "ParameterPolynomial":
        return type(self)(
            terms={
                monomial: -coefficient
                for monomial, coefficient in self.terms.items()
            }
        )

    def __sub__(self, other: object) -> "ParameterPolynomial":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "ParameterPolynomial":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "ParameterPolynomial":
        other = self.coerce(other)
        result: dict[tuple[int, ...], QuotientElement] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left_monomial[index] + right_monomial[index]
                    for index in range(NVAR)
                )
                result[monomial] = (
                    result.get(monomial, QuotientElement.coerce(0))
                    + left_coefficient * right_coefficient
                )
                if not result[monomial]:
                    del result[monomial]
        return type(self)(terms=result)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "ParameterPolynomial":
        assert exponent >= 0
        result = type(self)(1)
        for _ in range(exponent):
            result *= self
        return result


WPolynomial = dict[int, ParameterPolynomial]


def wadd(*polynomials: WPolynomial) -> WPolynomial:
    result: WPolynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = (
                result.get(exponent, ParameterPolynomial()) + coefficient
            )
            if not result[exponent]:
                del result[exponent]
    return result


def wscale(polynomial: WPolynomial, scalar: object) -> WPolynomial:
    scalar = ParameterPolynomial.coerce(scalar)
    return {
        exponent: scalar * coefficient
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient
    }


def wmultiply(left: WPolynomial, right: WPolynomial) -> WPolynomial:
    result: WPolynomial = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, ParameterPolynomial())
                + left_coefficient * right_coefficient
            )
            if not result[exponent]:
                del result[exponent]
    return result


def wderivative(polynomial: WPolynomial) -> WPolynomial:
    return {
        exponent - 1: exponent * coefficient
        for exponent, coefficient in polynomial.items()
        if exponent and exponent * coefficient
    }


def bracket(
    p_degree: int,
    p: WPolynomial,
    q_degree: int,
    q: WPolynomial,
) -> WPolynomial:
    core = wadd(
        wscale(wmultiply(p, wderivative(q)), p_degree),
        wscale(wmultiply(wderivative(p), q), -q_degree),
    )
    return {
        exponent + 1: coefficient
        for exponent, coefficient in core.items()
    }


def p_exponents(radial_degree: int) -> list[int]:
    if radial_degree == 1:
        return list(range(8))
    if radial_degree == 0:
        return list(range(1, 9))
    if -8 <= radial_degree <= -1:
        return list(range(-radial_degree, 9))
    return []


def q_exponents(radial_degree: int) -> list[int]:
    if radial_degree == 2:
        return list(range(11))
    if radial_degree == 1:
        return list(range(12))
    if radial_degree == 0:
        return list(range(1, 13))
    if -12 <= radial_degree <= -1:
        return list(range(-radial_degree, 13))
    return []


def rref_affine(
    matrix: list[list[QuotientElement]],
    source: list[ParameterPolynomial],
) -> tuple[list[ParameterPolynomial], list[ParameterPolynomial]]:
    work = [list(row) for row in matrix]
    rhs = list(source)
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        rhs[pivot_row], rhs[selected] = rhs[selected], rhs[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [
            coefficient * inverse
            for coefficient in work[pivot_row]
        ]
        rhs[pivot_row] *= inverse
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index]
                - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
            rhs[row] -= rhs[pivot_row] * multiplier
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    solution = [ParameterPolynomial() for _ in range(column_count)]
    for row, column in enumerate(pivots):
        solution[column] = -rhs[row]
    consistency = [
        rhs[row]
        for row in range(pivot_row, row_count)
        if rhs[row]
    ]
    return solution, consistency


def solve_stage(
    p_blocks: dict[int, WPolynomial],
    q_blocks: dict[int, WPolynomial],
    p_degree: int,
) -> tuple[WPolynomial, WPolynomial, list[ParameterPolynomial]]:
    q_degree = p_degree + 1
    p_support = p_exponents(p_degree)
    q_support = q_exponents(q_degree)
    output_degree = p_degree + 2
    source: WPolynomial = {}
    for left_degree, left in p_blocks.items():
        for right_degree, right in q_blocks.items():
            if left_degree + right_degree - 1 == output_degree:
                source = wadd(
                    source,
                    bracket(left_degree, left, right_degree, right),
                )
    columns = [
        bracket(
            p_degree,
            {exponent: ParameterPolynomial(1)},
            3,
            q_blocks[3],
        )
        for exponent in p_support
    ]
    columns.extend(
        bracket(
            2,
            p_blocks[2],
            q_degree,
            {exponent: ParameterPolynomial(1)},
        )
        for exponent in q_support
    )
    row_exponents = sorted(
        set(source).union(*(set(column) for column in columns))
    )
    matrix = [
        [
            column.get(exponent, ParameterPolynomial())
            .terms.get((0,) * NVAR, QuotientElement.coerce(0))
            for column in columns
        ]
        for exponent in row_exponents
    ]
    source_vector = [
        source.get(exponent, ParameterPolynomial())
        for exponent in row_exponents
    ]
    solution, consistency = rref_affine(matrix, source_vector)
    split = len(p_support)
    return (
        dict(zip(p_support, solution[:split])),
        dict(zip(q_support, solution[split:])),
        consistency,
    )


def c_pair(
    deficit: int,
    c_polynomial: dict[int, QuotientElement],
    u: list[QuotientElement],
    v: list[QuotientElement],
) -> tuple[WPolynomial, WPolynomial]:
    complement = 5 - deficit
    p_mode: WPolynomial = {}
    q_mode: WPolynomial = {}
    for exponent, coefficient in c_polynomial.items():
        for index, outer in enumerate(u):
            value = (
                QuotientElement.coerce(
                    Fraction(
                        complement * index
                        + deficit
                        - 3
                        - 2 * exponent,
                        complement,
                    )
                )
                * coefficient
                * outer
            )
            if value:
                p_mode[exponent + index] = (
                    p_mode.get(
                        exponent + index,
                        ParameterPolynomial(),
                    )
                    + ParameterPolynomial(value)
                )
        for index, outer in enumerate(v):
            value = (
                QuotientElement.coerce(
                    Fraction(
                        complement * index
                        + deficit
                        - 2
                        - 3 * exponent,
                        complement,
                    )
                )
                * coefficient
                * outer
            )
            if value:
                q_mode[exponent + index] = (
                    q_mode.get(
                        exponent + index,
                        ParameterPolynomial(),
                    )
                    + ParameterPolynomial(value)
                )
    return p_mode, q_mode


def canonical_modes(
    u: list[QuotientElement],
    v: list[QuotientElement],
) -> dict[int, list[tuple[WPolynomial, WPolynomial]]]:
    u_square = [QuotientElement.coerce(0) for _ in range(15)]
    for left, left_coefficient in enumerate(u):
        for right, right_coefficient in enumerate(u):
            u_square[left + right] += (
                left_coefficient * right_coefficient
            )
    high_one = {
        exponent - 1: coefficient
        for exponent, coefficient in enumerate(u_square)
        if exponent >= 2 and coefficient
    }
    high_four: dict[int, QuotientElement] = {
        4: QuotientElement.coerce(1)
    }
    for exponent in range(3, 1, -1):
        output_exponent = 7 + exponent
        known = QuotientElement.coerce(0)
        for c_exponent, c_coefficient in high_four.items():
            u_index = output_exponent - c_exponent
            if 0 <= u_index <= 7:
                known += (
                    (u_index + 1 - 2 * c_exponent)
                    * c_coefficient
                    * u[u_index]
                )
        pivot = (8 - 2 * exponent) * u[7]
        high_four[exponent] = -known / pivot
    polynomials = {
        1: ({0: QuotientElement.coerce(1)}, high_one),
        2: (
            {1: QuotientElement.coerce(1)},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(v)
                if exponent >= 2 and coefficient
            },
        ),
        3: (
            {1: QuotientElement.coerce(1)},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(u)
                if exponent >= 2 and coefficient
            },
        ),
        4: (high_four,),
    }
    return {
        deficit: [
            c_pair(deficit, polynomial, u, v)
            for polynomial in deficit_polynomials
        ]
        for deficit, deficit_polynomials in polynomials.items()
    }


def substitute_endpoint_coordinates(
    polynomial: ParameterPolynomial,
    parameters: tuple[ParameterPolynomial, ...],
) -> ParameterPolynomial:
    replacements = {
        0: parameters[0] + 2 * parameters[1],
        2: parameters[2]
        + parameters[3] * QuotientElement.coerce(Fraction(2, 3)),
    }
    result = ParameterPolynomial()
    for monomial, coefficient in polynomial.terms.items():
        term = ParameterPolynomial(coefficient)
        for index, exponent in enumerate(monomial):
            term *= replacements.get(index, parameters[index]) ** exponent
        result += term
    return result


def exact_four_stage_constraints(
    u_expressions: list[sp.Expr],
    v_expressions: list[sp.Expr],
) -> list[ParameterPolynomial]:
    u = [QuotientElement.coerce(expression) for expression in u_expressions]
    v = [QuotientElement.coerce(expression) for expression in v_expressions]
    modes = canonical_modes(u, v)
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    offsets = {1: 0, 0: 2, -1: 4, -2: 6}
    p_blocks: dict[int, WPolynomial] = {
        2: {
            -1: ParameterPolynomial(1),
            **{
                index - 1: ParameterPolynomial(u[index])
                for index in range(1, 8)
            },
        }
    }
    q_blocks: dict[int, WPolynomial] = {
        3: {
            -1: ParameterPolynomial(1),
            **{
                index - 1: ParameterPolynomial(v[index])
                for index in range(1, 11)
            },
        }
    }
    constraints: list[ParameterPolynomial] = []
    stage_counts: list[int] = []
    for p_degree in range(1, -3, -1):
        p_block, q_block, new_constraints = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
        )
        deficit = 2 - p_degree
        offset = offsets[p_degree]
        for local_index, (p_mode, q_mode) in enumerate(
            modes.get(deficit, ())
        ):
            parameter = parameters[offset + local_index]
            for exponent, coefficient in p_mode.items():
                p_block[exponent] = (
                    p_block.get(exponent, ParameterPolynomial())
                    + parameter * coefficient
                )
            for exponent, coefficient in q_mode.items():
                q_block[exponent] = (
                    q_block.get(exponent, ParameterPolynomial())
                    + parameter * coefficient
                )
        p_blocks[p_degree] = p_block
        q_blocks[p_degree + 1] = q_block
        constraints.extend(new_constraints)
        stage_counts.append(len(new_constraints))
    assert stage_counts == [0, 0, 0, 2]
    return [
        substitute_endpoint_coordinates(constraint, parameters)
        for constraint in constraints
    ]


def verify_exact_characteristic_zero_square() -> None:
    """Reconstruct Q outer algebra and verify the square inside it."""
    primes = reconstruction_primes()
    modular_bases: dict[int, list[int]] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(modular_lex_basis, prime): prime
            for prime in primes
        }
        for future in as_completed(futures):
            modular_bases[futures[future]] = future.result()
    coefficients = lift_coefficients(primes, modular_bases)
    _s, eliminant, u, v = quotient_data(coefficients)
    QuotientElement.configure(eliminant)
    transformed = exact_four_stage_constraints(u, v)
    assert len(transformed) == 2

    square_coefficients = {
        (4, 0, 0, 0, 0, 0, 0): QuotientElement.coerce(KAPPA**2),
        (2, 0, 1, 0, 0, 0, 0): QuotientElement.coerce(-2 * KAPPA),
        (0, 0, 2, 0, 0, 0, 0): QuotientElement.coerce(1),
    }
    for equation in transformed:
        assert set(equation.terms) == set(square_coefficients)
        scalar = equation.terms[
            (0, 0, 2, 0, 0, 0, 0)
        ]
        assert scalar
        assert all(
            equation.terms[monomial]
            == scalar * target_coefficient
            for monomial, target_coefficient in square_coefficients.items()
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--exact-lift",
        action="store_true",
        help="also run the slow characteristic-zero outer reconstruction",
    )
    args = parser.parse_args()
    verify_grade_radial_dictionary()
    verify_symbolic_kappa_ratio()
    verify_modular_five_point_square()
    print("n=3: outer and first three radial coefficients are automatic")
    print("first nonautomatic coefficient: z^3 y^3 (radial deficit four)")
    print("five-point reduction: two nonzero multiples of")
    print("(Y2-169*Y0^2/48)^2")
    print("on the square branch: one weight-five survivor, not divisible by Y0")
    print("weight five is triangularly solvable; the next obstruction is later")
    print("deficit six: charts 1/2 cut, chart 3 empty, chart 4 forces X4=X5=0")
    print("deepest chart: deficit 7 automatic, deficit 8 forces X6=0")
    if args.exact_lift:
        verify_exact_characteristic_zero_square()
        print("characteristic-zero five-point quotient: exact square verified")
    print("RESULT: CASE-C n=3 HURWITZ BRIDGE PASSES")


if __name__ == "__main__":
    main()
