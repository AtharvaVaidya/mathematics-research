#!/usr/bin/env python3
"""Exact algebraic-closure obstruction for the full GGHV a/b branch.

This script works modulo p=32003.  It uses the coordinates

    z = x*y,  w = x*y^2

and writes

    P = z^2/w + a0(w) + z*a1(w) + z^2*a2(w),
    Q = z^3/w + b0(w) + z*b1(w) + z^2*b2(w) + z^3*b3(w).

The bracket equation is equivalent to five polynomial ODEs.  The outer one,
after U=1+w*a2 and V=1+w*b3, is

    U*V + 2*w*U*V' - 3*w*U'*V = 1,
    deg(U)=7, deg(V)=10.

The main program emits Singular input proving:

* the saturated outer variety has no point with u1=0;
* in the u1=1 chart it consists of five geometric points, two rational and
  three conjugate over a cubic extension;
* above every one of those five points the other four ODEs force all
  nonconstant a0 and b0 coefficients to vanish.

Since the a/b Newton polygons require [w^8]a0 and [w^12]b0 to be nonzero,
this rules out the full 25+47 a/b coefficient variety over Fbar_32003.

This script also verifies the special-fiber inputs to the characteristic-zero
bridge: the outer eliminant is squarefree, both required outer vertices are
units, and every lower projective coordinate is nilpotent.  The companion
``route_bd_ab_hurwitz_count.py`` gives exactly five automorphism-free tame
outer covers.  Prime-to-32003 tame specialization and properness of the
weighted projectivization of the original lower equations then rule out the
a/b branch in characteristic zero.  The geometric bridge is documented in
``ROUTE_B_FULL_MEMO.md``; it is not inferred from special-fiber emptiness
alone.

Run:

    .venv/bin/python route_bd_fbar_obstruction.py --run-singular

Singular 4.4 or newer must be available on PATH.
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from typing import Iterable, Sequence


PRIME = 32003
# t^3 - 11133*t^2 - 11294*t - 6180, irreducible over F_32003.
CUBIC = (PRIME - 6180, PRIME - 11294, PRIME - 11133, 1)


@dataclass(frozen=True)
class K:
    """Element of F_32003[t]/(CUBIC), stored low coefficient first."""

    c0: int = 0
    c1: int = 0
    c2: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "c0", self.c0 % PRIME)
        object.__setattr__(self, "c1", self.c1 % PRIME)
        object.__setattr__(self, "c2", self.c2 % PRIME)

    @staticmethod
    def coerce(value: int | K) -> K:
        return value if isinstance(value, K) else K(value)

    def __add__(self, other: int | K) -> K:
        if not isinstance(other, (int, K)):
            return NotImplemented
        other = self.coerce(other)
        return K(self.c0 + other.c0, self.c1 + other.c1, self.c2 + other.c2)

    __radd__ = __add__

    def __neg__(self) -> K:
        return K(-self.c0, -self.c1, -self.c2)

    def __sub__(self, other: int | K) -> K:
        if not isinstance(other, (int, K)):
            return NotImplemented
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | K) -> K:
        if not isinstance(other, (int, K)):
            return NotImplemented
        return self.coerce(other) - self

    def __mul__(self, other: int | K) -> K:
        if not isinstance(other, (int, K)):
            return NotImplemented
        other = self.coerce(other)
        raw = [0] * 5
        left = (self.c0, self.c1, self.c2)
        right = (other.c0, other.c1, other.c2)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                raw[i + j] = (raw[i + j] + a * b) % PRIME
        # t^3 = 11133*t^2 + 11294*t + 6180.
        for degree in (4, 3):
            coefficient = raw[degree] % PRIME
            if not coefficient:
                continue
            raw[degree] = 0
            raw[degree - 3] = (raw[degree - 3] + 6180 * coefficient) % PRIME
            raw[degree - 2] = (raw[degree - 2] + 11294 * coefficient) % PRIME
            raw[degree - 1] = (raw[degree - 1] + 11133 * coefficient) % PRIME
        return K(*raw[:3])

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> K:
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        result = K(1)
        base = self
        while exponent:
            if exponent & 1:
                result *= base
            base *= base
            exponent >>= 1
        return result

    def inverse(self) -> K:
        if not self:
            raise ZeroDivisionError("zero in cubic field")
        return self ** (PRIME**3 - 2)

    def __truediv__(self, other: int | K) -> K:
        return self * self.coerce(other).inverse()

    def __bool__(self) -> bool:
        return bool(self.c0 or self.c1 or self.c2)

    def singular(self) -> str:
        pieces: list[str] = []
        for coefficient, monomial in (
            (self.c0, ""),
            (self.c1, "t"),
            (self.c2, "t^2"),
        ):
            signed = coefficient if coefficient <= PRIME // 2 else coefficient - PRIME
            if not signed:
                continue
            if monomial and signed == 1:
                pieces.append(monomial)
            elif monomial and signed == -1:
                pieces.append("-" + monomial)
            else:
                pieces.append(f"{signed}{('*' + monomial) if monomial else ''}")
        if not pieces:
            return "0"
        return "+".join(pieces).replace("+-", "-")


ZERO = K()
ONE = K(1)
T = K(0, 1)


def verify_ab_support_compression() -> None:
    """Check the z,w compression against all 975 original bracket terms."""

    p_terms = ((2, -1),) + tuple(
        (z_degree, w_degree)
        for z_degree in range(3)
        for w_degree in range(9 - z_degree)
    )
    q_terms = ((3, -1),) + tuple(
        (z_degree, w_degree)
        for z_degree in range(4)
        for w_degree in range(13 - z_degree)
    )
    assert len(p_terms) == 25
    assert len(q_terms) == 47

    def xy_exponents(term: tuple[int, int]) -> tuple[int, int]:
        z_degree, w_degree = term
        return z_degree + w_degree, z_degree + 2 * w_degree

    rows: set[tuple[int, int]] = set()
    term_count = 0
    for p_term in p_terms:
        p_xy = xy_exponents(p_term)
        for q_term in q_terms:
            q_xy = xy_exponents(q_term)
            determinant_zw = (
                p_term[0] * q_term[1] - p_term[1] * q_term[0]
            )
            determinant_xy = (
                p_xy[0] * q_xy[1] - p_xy[1] * q_xy[0]
            )
            # [z,w]_(x,y)=w.
            assert determinant_xy == determinant_zw
            if not determinant_xy:
                continue
            output_zw = (
                p_term[0] + q_term[0] - 1,
                p_term[1] + q_term[1],
            )
            output_xy = (
                p_xy[0] + q_xy[0] - 1,
                p_xy[1] + q_xy[1] - 1,
            )
            assert xy_exponents(output_zw) == output_xy
            rows.add(output_xy)
            term_count += 1
    assert len(rows) == 92
    assert term_count == 975
    assert xy_exponents((4, -2)) == (2, 0)


@dataclass
class MP:
    """Sparse polynomial in (L,M,N0,N1) with coefficients in K."""

    terms: dict[tuple[int, int, int, int], K]

    def __init__(
        self,
        value: int | K = 0,
        terms: dict[tuple[int, int, int, int], K] | None = None,
    ) -> None:
        if terms is not None:
            self.terms = {monomial: coefficient for monomial, coefficient in terms.items() if coefficient}
        else:
            coefficient = K.coerce(value)
            self.terms = {(0, 0, 0, 0): coefficient} if coefficient else {}

    @staticmethod
    def coerce(value: int | K | MP) -> MP:
        return value if isinstance(value, MP) else MP(value)

    @staticmethod
    def variable(index: int) -> MP:
        monomial = [0, 0, 0, 0]
        monomial[index] = 1
        return MP(terms={tuple(monomial): ONE})

    def __add__(self, other: int | K | MP) -> MP:
        other = self.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, ZERO) + coefficient
            if not result[monomial]:
                del result[monomial]
        return MP(terms=result)

    __radd__ = __add__

    def __neg__(self) -> MP:
        return MP(terms={monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other: int | K | MP) -> MP:
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | K | MP) -> MP:
        return self.coerce(other) - self

    def __mul__(self, other: int | K | MP) -> MP:
        other = self.coerce(other)
        result: dict[tuple[int, int, int, int], K] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left_monomial[index] + right_monomial[index]
                    for index in range(4)
                )
                result[monomial] = (
                    result.get(monomial, ZERO)
                    + left_coefficient * right_coefficient
                )
                if not result[monomial]:
                    del result[monomial]
        return MP(terms=result)

    __rmul__ = __mul__

    def __bool__(self) -> bool:
        return bool(self.terms)

    def total_degree(self) -> int:
        return max((sum(monomial) for monomial in self.terms), default=-1)

    def weighted_degrees(self) -> set[int]:
        """Degrees for weights wt(L)=wt(M)=1, wt(N0)=wt(N1)=2."""

        return {
            monomial[0] + monomial[1] + 2 * monomial[2] + 2 * monomial[3]
            for monomial in self.terms
        }

    def singular(self) -> str:
        variables = ("L", "M", "N0", "N1")
        pieces: list[str] = []
        for monomial in sorted(self.terms, reverse=True):
            coefficient = self.terms[monomial]
            factors = [
                variable if exponent == 1 else f"{variable}^{exponent}"
                for variable, exponent in zip(variables, monomial)
                if exponent
            ]
            coefficient_text = coefficient.singular()
            if factors:
                if coefficient_text == "1":
                    pieces.append("*".join(factors))
                elif coefficient_text == "-1":
                    pieces.append("-" + "*".join(factors))
                else:
                    pieces.append(f"({coefficient_text})*" + "*".join(factors))
            else:
                pieces.append(coefficient_text)
        return "+".join(pieces).replace("+-", "-") if pieces else "0"


L, M, N0, N1 = (MP.variable(index) for index in range(4))


def trim(poly: list[MP]) -> list[MP]:
    while poly and not poly[-1]:
        poly.pop()
    return poly


def poly_add(*polynomials: Sequence[MP | K | int]) -> list[MP]:
    size = max((len(poly) for poly in polynomials), default=0)
    result = [MP() for _ in range(size)]
    for poly in polynomials:
        for index, coefficient in enumerate(poly):
            result[index] += coefficient
    return trim(result)


def poly_scale_shift(
    poly: Sequence[MP | K | int], scalar: MP | K | int, shift: int
) -> list[MP]:
    return [MP() for _ in range(shift)] + [MP.coerce(scalar) * coefficient for coefficient in poly]


def poly_derivative(poly: Sequence[MP | K | int]) -> list[MP]:
    return trim([MP.coerce(poly[degree]) * degree for degree in range(1, len(poly))])


def poly_multiply(
    left: Sequence[MP | K | int], right: Sequence[MP | K | int]
) -> list[MP]:
    if not left or not right:
        return []
    result = [MP() for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += MP.coerce(a) * b
    return trim(result)


def rref(matrix: Sequence[Sequence[K]]) -> tuple[list[list[K]], list[int]]:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [entry * inverse for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, pivots


def solve_affine(
    matrix: Sequence[Sequence[K]],
    source: Sequence[MP],
    free_parameters: Sequence[MP],
) -> tuple[list[MP], list[MP], list[int]]:
    """Solve matrix*x + source=0, retaining exact consistency equations."""

    work = [list(row) for row in matrix]
    rhs = list(source)
    row_count = len(work)
    column_count = len(work[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        rhs[pivot_row], rhs[selected] = rhs[selected], rhs[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [entry * inverse for entry in work[pivot_row]]
        rhs[pivot_row] *= inverse
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
            rhs[row] -= multiplier * rhs[pivot_row]
        pivots.append(column)
        pivot_row += 1
    free_columns = [
        column for column in range(column_count) if column not in pivots
    ]
    assert len(free_columns) == len(free_parameters)
    solution = [MP() for _ in range(column_count)]
    for column, parameter in zip(free_columns, free_parameters):
        solution[column] = parameter
    for row, column in enumerate(pivots):
        solution[column] = -rhs[row] - sum(
            (work[row][free] * solution[free] for free in free_columns),
            MP(),
        )
    consistency = [rhs[row] for row in range(pivot_row, row_count) if rhs[row]]
    return solution, consistency, pivots


def coefficient_matrix(
    operator,
    variable_lengths: Sequence[int],
    row_count: int,
) -> list[list[K]]:
    """Matrix of a linear polynomial operator over K."""

    total = sum(variable_lengths)
    columns: list[list[MP]] = []
    for flat_index in range(total):
        inputs: list[list[MP]] = []
        offset = 0
        for length in variable_lengths:
            vector = [MP() for _ in range(length)]
            if offset <= flat_index < offset + length:
                vector[flat_index - offset] = MP(1)
            inputs.append(vector)
            offset += length
        image = list(operator(*inputs))
        image += [MP() for _ in range(row_count - len(image))]
        columns.append(image)
    matrix: list[list[K]] = []
    for row in range(row_count):
        matrix_row: list[K] = []
        for column in range(total):
            entry = columns[column][row]
            assert set(entry.terms).issubset({(0, 0, 0, 0)})
            matrix_row.append(entry.terms.get((0, 0, 0, 0), ZERO))
        matrix.append(matrix_row)
    return matrix


def outer_coefficients(t: K) -> tuple[list[K], list[K]]:
    """Evaluate the modular FGLM parametrization at t."""

    u = [ZERO] * 8
    u[0] = ONE
    u[1] = ONE
    u[7] = (
        9966 * t**4 + 9165 * t**3 - 5116 * t**2 + 14472 * t + 1714
    )
    u[6] = (
        5086 * t**4 - 8016 * t**3 + 9655 * t**2 - 9341 * t + 6315
    )
    u[5] = (
        13872 * t**4 - 13574 * t**3 + 7956 * t**2 + 5586 * t - 5949
    )
    u[4] = (
        -7137 * t**4 + 1864 * t**3 - 12803 * t**2 + 16001 * t + 13291
    )
    u[3] = (
        10377 * t**4 - 11035 * t**3 + 4685 * t**2 - 4425 * t + 15969
    )
    u[2] = (
        14177 * t**4 + 4167 * t**3 - 3195 * t**2 + 5202 * t - 8983
    )
    v = [ZERO] * 11
    v[0] = ONE
    for degree in range(1, 11):
        known = sum(
            (
                (1 + 2 * (degree - i) - 3 * i)
                * u[i]
                * v[degree - i]
                for i in range(1, min(7, degree) + 1)
            ),
            ZERO,
        )
        v[degree] = -known / (1 + 2 * degree)
    for degree in range(1, 18):
        residual = sum(
            (
                (1 + 2 * j - 3 * i) * u[i] * v[j]
                for i in range(8)
                for j in range(11)
                if i + j == degree
            ),
            ZERO,
        )
        assert not residual
    assert u[7] * t == ONE
    assert v[10]
    return u, v


def lower_constraints(t: K) -> tuple[list[MP], dict[str, int]]:
    """Return the final four-parameter consistency ideal over one top branch."""

    u, v = outer_coefficients(t)
    a2 = [MP(coefficient) for coefficient in u[1:]]
    b3 = [MP(coefficient) for coefficient in v[1:]]

    def equation_three(a1: list[MP], b2: list[MP]) -> list[MP]:
        return poly_add(
            poly_scale_shift(poly_multiply(a2, poly_derivative(b2)), 2, 2),
            poly_scale_shift(poly_multiply(a1, poly_derivative(b3)), 1, 2),
            poly_scale_shift(poly_multiply(poly_derivative(a1), b3), -3, 2),
            poly_scale_shift(poly_multiply(poly_derivative(a2), b2), -2, 2),
            poly_scale_shift(b2, 2, 0),
            poly_scale_shift(poly_derivative(b2), 2, 1),
            poly_scale_shift(a1, -1, 0),
            poly_scale_shift(poly_derivative(a1), -3, 1),
        )

    matrix_three = coefficient_matrix(equation_three, (8, 11), 18)
    reduced_three, pivots_three = rref(matrix_three)
    free_three = [
        column for column in range(19) if column not in pivots_three
    ]
    assert len(pivots_three) == 17 and free_three == [17, 18]
    kernel: list[list[K]] = []
    for free in free_three:
        vector = [ZERO] * 19
        vector[free] = ONE
        for row, pivot in enumerate(pivots_three):
            vector[pivot] = -reduced_three[row][free]
        kernel.append(vector)
    stage_one = [
        MP(kernel[0][index]) * L + MP(kernel[1][index]) * M
        for index in range(19)
    ]
    a1 = stage_one[:8]
    b2 = stage_one[8:]

    def equation_two_linear(a0_tail: list[MP], b1: list[MP]) -> list[MP]:
        a0 = [MP()] + a0_tail
        return poly_add(
            poly_scale_shift(poly_multiply(a2, poly_derivative(b1)), 2, 2),
            poly_scale_shift(poly_multiply(poly_derivative(a2), b1), -1, 2),
            poly_scale_shift(poly_multiply(poly_derivative(a0), b3), -3, 2),
            b1,
            poly_scale_shift(poly_derivative(b1), 2, 1),
            poly_scale_shift(poly_derivative(a0), -3, 1),
        )

    matrix_two = coefficient_matrix(equation_two_linear, (8, 12), 19)
    source_two = poly_scale_shift(
        poly_add(
            poly_multiply(a1, poly_derivative(b2)),
            poly_scale_shift(poly_multiply(poly_derivative(a1), b2), -2, 0),
        ),
        1,
        2,
    )
    source_two += [MP() for _ in range(19 - len(source_two))]
    stage_two, consistency_two, pivots_two = solve_affine(
        matrix_two, source_two, (N0, N1)
    )
    assert len(pivots_two) == 18 and not consistency_two
    a0 = [MP()] + stage_two[:8]
    b1 = stage_two[8:]

    def equation_one_linear(b0_tail: list[MP]) -> list[MP]:
        b0 = [MP()] + b0_tail
        return poly_add(
            poly_scale_shift(poly_multiply(a2, poly_derivative(b0)), 2, 2),
            poly_scale_shift(poly_derivative(b0), 2, 1),
        )

    matrix_one = coefficient_matrix(equation_one_linear, (12,), 18)
    source_one = poly_scale_shift(
        poly_add(
            poly_multiply(a1, poly_derivative(b1)),
            poly_scale_shift(poly_multiply(poly_derivative(a1), b1), -1, 0),
            poly_scale_shift(poly_multiply(poly_derivative(a0), b2), -2, 0),
        ),
        1,
        2,
    )
    source_one += [MP() for _ in range(18 - len(source_one))]
    b0_tail, consistency_one, pivots_one = solve_affine(
        matrix_one, source_one, ()
    )
    assert len(pivots_one) == 12
    b0 = [MP()] + b0_tail

    equation_zero = poly_add(
        poly_multiply(a1, poly_derivative(b0)),
        poly_scale_shift(poly_multiply(poly_derivative(a0), b1), -1, 0),
    )
    constraints = consistency_one + [coefficient for coefficient in equation_zero if coefficient]
    assert len(consistency_one) == 5
    assert all(
        constraint.weighted_degrees() == {3}
        for constraint in consistency_one
    )
    assert all(
        constraint.weighted_degrees() == {4}
        for constraint in constraints[len(consistency_one) :]
    )
    # At L=M=N0=N1=0 every nonconstant lower coefficient is zero.
    origin = (0, 0, 0, 0)
    for coefficient in a0[1:] + b0[1:]:
        assert coefficient.terms.get(origin, ZERO) == ZERO
    return constraints, {
        "rank_eq3": len(pivots_three),
        "rank_eq2": len(pivots_two),
        "rank_eq1": len(pivots_one),
        "cubic_constraints": len(consistency_one),
        "quartic_constraints": len(constraints) - len(consistency_one),
    }


def lower_singular_program(t: K, label: str) -> str:
    constraints, stats = lower_constraints(t)
    equations = ",".join(constraint.singular() for constraint in constraints)
    return f"""
// Lower four ODEs over branch {label}.
ring lower_{label}=(32003,t),(L,M,N0,N1),dp;
minpoly=t^3-11133*t^2-11294*t-6180;
ideal I_{label}={equations};
option(redSB);
ideal G_{label}=std(I_{label});
print("LOWER {label} ranks {stats['rank_eq3']},{stats['rank_eq2']},{stats['rank_eq1']}");
print(size(G_{label}));
G_{label};
print("LOWER {label} PROJECTIVE NILPOTENCE");
reduce(L^12,G_{label});
reduce(M^12,G_{label});
reduce(N0^2,G_{label});
reduce(N1^2,G_{label});
"""


def outer_compatibility_ideal() -> str:
    """Return the six recursively eliminated outer compatibility equations."""

    # Recursively eliminate v1,...,v10.  The coefficient of v_k is 1+2k,
    # invertible modulo PRIME because PRIME>21.  Only degrees 11,...,16 then
    # remain as compatibility equations in u1,...,u7.  This is the same
    # outer ideal as the 16 bilinear coefficient equations, but makes the
    # Gröbner certificate much smaller.
    import sympy as sym

    u_symbols = sym.symbols("u1:8")
    u = {0: sym.Integer(1)}
    u.update({index: u_symbols[index - 1] for index in range(1, 8)})
    v: dict[int, sym.Expr] = {0: sym.Integer(1)}
    compatibility: list[sym.Expr] = []
    for degree in range(1, 18):
        known = sum(
            (
                (1 + 2 * (degree - i) - 3 * i)
                * u.get(i, 0)
                * v.get(degree - i, 0)
                for i in range(max(0, degree - 10), min(7, degree) + 1)
                if i != 0
            ),
            sym.Integer(0),
        )
        if degree <= 10:
            v[degree] = sym.cancel(-known / (1 + 2 * degree))
        elif degree < 17:
            numerator = sym.together(known).as_numer_denom()[0]
            compatibility.append(sym.primitive(numerator, *u_symbols)[1])
    ideal = ",".join(
        str(sym.expand(equation)).replace("**", "^")
        for equation in compatibility
    )
    return ideal


def outer_v10_numerator() -> str:
    """Return an integer numerator for the recursively eliminated v10."""

    import sympy as sym

    u_symbols = sym.symbols("u1:8")
    u = {0: sym.Integer(1)}
    u.update({index: u_symbols[index - 1] for index in range(1, 8)})
    v: dict[int, sym.Expr] = {0: sym.Integer(1)}
    for degree in range(1, 11):
        known = sum(
            (
                (1 + 2 * (degree - i) - 3 * i)
                * u.get(i, 0)
                * v.get(degree - i, 0)
                for i in range(1, min(7, degree) + 1)
            ),
            sym.Integer(0),
        )
        v[degree] = sym.cancel(-known / (1 + 2 * degree))
    numerator = sym.together(v[10]).as_numer_denom()[0]
    return str(sym.expand(numerator)).replace("**", "^")


def outer_singular_program() -> str:
    """Generate, rather than hard-code, the saturated outer equations."""

    ideal = outer_compatibility_ideal()
    variables = ",".join([f"u{index}" for index in range(1, 8)] + ["s"])
    return f"""
// Outer equation U*V+2wUV'-3wU'V=1.
ring outer=32003,({variables}),dp;
ideal E={ideal};
// The required upper vertex is u7 != 0.
ideal bad=E,u1,s*u7-1;
option(redSB);
ideal Gbad=std(bad);
print("OUTER U1=0 SATURATED");
Gbad;
// Normalize u1=1; v10 is automatically nonzero on the resulting five points.
ideal chart=E,u1-1,s*u7-1;
ideal Gchart=std(chart);
print("OUTER CHART VDIM");
vdim(Gchart);
ideal Iu7=Gchart,u7;
ideal Gu7=std(Iu7);
print("OUTER U7 UNIT");
Gu7;
poly v10numerator={outer_v10_numerator()};
ideal Iv10=Gchart,v10numerator;
ideal Gv10=std(Iv10);
print("OUTER V10 UNIT");
Gv10;
ring outerlex=32003,({variables}),lp;
ideal H=fglm(outer,Gchart);
print("OUTER FGLM SIZE");
size(H);
H;
print("OUTER ELIMINANT GCD");
gcd(H[1],diff(H[1],s));
print("OUTER QUINTIC FACTORS");
factorize(H[1],1);
"""


def rational_outer_singular_program() -> str:
    """Exact characteristic-zero outer basis and good-reduction check.

    This deliberately uses Singular's deterministic ``std`` over Q rather
    than inferring a rational result from modular samples.  On the reference
    machine the normalized-chart basis takes roughly 15--30 minutes.
    """

    ideal = outer_compatibility_ideal()
    variables = ",".join([f"u{index}" for index in range(1, 8)] + ["s"])
    expected = ",".join(
        (
            "s^5+9413*s^4+8734*s^3-3563*s^2+7508*s-3664",
            "u7-9966*s^4-9165*s^3+5116*s^2-14472*s-1714",
            "u6-5086*s^4+8016*s^3-9655*s^2+9341*s-6315",
            "u5-13872*s^4+13574*s^3-7956*s^2-5586*s+5949",
            "u4+7137*s^4-1864*s^3+12803*s^2-16001*s-13291",
            "u3-10377*s^4+11035*s^3-4685*s^2+4425*s-15969",
            "u2-14177*s^4-4167*s^3+3195*s^2-5202*s+8983",
            "u1-1",
        )
    )
    return f"""
option(redSB);
ring badq=0,({variables}),dp;
ideal Ibad={ideal},u1,s*u7-1;
ideal Gbadq=std(Ibad);
print("Q U1=0 SATURATED");
Gbadq;

ring chartq=0,({variables}),dp;
ideal Iq={ideal},u1-1,s*u7-1;
ideal Gq=std(Iq);
print("Q CHART VDIM");
vdim(Gq);

ring chartqlex=0,({variables}),lp;
ideal Hq=fglm(chartq,Gq);
print("Q FGLM SIZE");
size(Hq);
Hq;

ring reduction=32003,({variables}),lp;
ideal Hmod=imap(chartqlex,Hq);
ideal Hexpected={expected};
ideal forward=simplify(reduce(Hmod,Hexpected),2);
ideal backward=simplify(reduce(Hexpected,Hmod),2);
print("GOOD REDUCTION RESIDUAL SIZES");
size(forward);
size(backward);
quit;
"""


def full_singular_program() -> str:
    # Two roots of the outer quintic lie in the prime field.  The other three
    # are represented simultaneously by T in the cubic extension.
    rational_one = K(26839)
    rational_two = K(16621)
    return (
        outer_singular_program()
        + lower_singular_program(rational_one, "r1")
        + lower_singular_program(rational_two, "r2")
        + lower_singular_program(T, "cubic")
        + "\nquit;\n"
    )


def run_singular(program: str) -> str:
    completed = subprocess.run(
        ["Singular", "--no-tty"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
    )
    output = completed.stdout
    assert "OUTER U1=0 SATURATED" in output
    # The first printed basis after that marker is 1.
    assert "Gbad[1]=1" in output
    assert "OUTER CHART VDIM" in output and "\n5\n" in output
    assert "OUTER U7 UNIT\nGu7[1]=1" in output
    assert "OUTER V10 UNIT\nGv10[1]=1" in output
    assert "OUTER ELIMINANT GCD\n1" in output
    assert "LOWER r1 ranks 17,18,12" in output
    assert "LOWER r2 ranks 17,18,12" in output
    assert "LOWER cubic ranks 17,18,12" in output
    # Each lower basis has N0^2=N1^2=0, then M^3=0 modulo those,
    # and finally L^3=0.  Thus its geometric zero set is only the origin.
    for label in ("r1", "r2", "cubic"):
        assert f"G_{label}[1]=N1^2" in output
        assert f"G_{label}[3]=N0^2" in output
        assert f"G_{label}[9]=M^3" in output
        assert f"G_{label}[12]=L^3" in output
        nilpotence = output.split(
            f"LOWER {label} PROJECTIVE NILPOTENCE",
            1,
        )[1].splitlines()
        assert [line.strip() for line in nilpotence[1:5]] == ["0"] * 4
    return output


def run_rational_outer() -> str:
    completed = subprocess.run(
        ["Singular", "--no-tty"],
        input=rational_outer_singular_program(),
        text=True,
        capture_output=True,
        check=True,
    )
    output = completed.stdout
    assert "Q U1=0 SATURATED" in output and "Gbadq[1]=1" in output
    assert "Q CHART VDIM" in output and "\n5\n" in output
    assert "Q FGLM SIZE" in output and "\n8\n" in output
    marker = output.split("GOOD REDUCTION RESIDUAL SIZES", 1)[1]
    residual_sizes = [
        line.strip()
        for line in marker.splitlines()
        if line.strip().lstrip("-").isdigit()
    ]
    assert residual_sizes[:2] == ["0", "0"], residual_sizes[:2]
    return output


def main() -> None:
    verify_ab_support_compression()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-singular",
        action="store_true",
        help="run the emitted exact certificate with Singular",
    )
    parser.add_argument(
        "--emit-singular",
        action="store_true",
        help="print the generated Singular program",
    )
    parser.add_argument(
        "--run-rational-outer",
        action="store_true",
        help="run the slow deterministic Q outer-basis and good-reduction proof",
    )
    parser.add_argument(
        "--emit-rational-singular",
        action="store_true",
        help="print the slow deterministic Q outer-basis program",
    )
    args = parser.parse_args()
    if args.emit_rational_singular:
        print(rational_outer_singular_program())
        return
    if args.run_rational_outer:
        output = run_rational_outer()
        print(output)
        print("RESULT: Q OUTER CHART IS FINITE OF DEGREE 5")
        print("RESULT: ITS F_32003 REDUCTION IS THE CERTIFIED FIVE-POINT FIBER")
        return
    program = full_singular_program()
    if args.emit_singular:
        print(program)
    if args.run_singular:
        output = run_singular(program)
        print(output)
        print("RESULT: FULL a/b VARIETY IS EMPTY OVER FBAR_32003")
        print(
            "BRIDGE INPUTS: REDUCED FIVE-POINT OUTER FIBER, "
            "UNIT OUTER VERTICES, EMPTY LOWER WEIGHTED PROJ"
        )
        print(
            "CHARACTERISTIC ZERO: COMBINE WITH THE EXACT HURWITZ COUNT "
            "AND PRIME-TO-p TAME SPECIALIZATION"
        )
    elif not args.emit_singular:
        # Even without Singular, exercise all exact cubic-field reductions.
        for t in (K(26839), K(16621), T):
            constraints, stats = lower_constraints(t)
            print(
                f"branch {t}: {len(constraints)} constraints; "
                f"ranks={stats['rank_eq3']},{stats['rank_eq2']},{stats['rank_eq1']}"
            )
        print("Use --run-singular for the Gröbner certificates.")


if __name__ == "__main__":
    main()
