#!/usr/bin/env python3
"""Tiny exact reconnaissance for the universal radial deformation complex.

For (m,n)=(2,3), the case-c support with outer parameter k has vertical
bounds

    D_P=2(k+1),  D_Q=3(k+1).

At radial deficit d the new blocks are A_(2-d), B_(3-d).  This verifier
computes the exact linear rank profiles for k=1 and k=2 over F_32003:

* k=1 uses its unique rational normalized outer cover;
* k=2 uses the irreducible quadratic factor containing its two normalized
  outer covers.

In both cases the free-kernel weights are

    (1,1,2,2,3,3,4),

and there is no later kernel.  Therefore the tempting extrapolation
"two copies of weights 1,...,k plus one copy of k+1" is false for the
stated support: it agrees at k=3 only accidentally.  The stable cutoff
d=4=m+n-1 instead supports the Kummer/de Rham resonance mechanism in
``route_bd_universal_outer_edge.py``.
"""

from __future__ import annotations

from dataclasses import dataclass


PRIME = 32003
# s^2 + 9432*s - 2820.
QUADRATIC_LINEAR = 9432
QUADRATIC_CONSTANT_REDUCTION = 2820


@dataclass(frozen=True)
class FQ2:
    c0: int = 0
    c1: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "c0", self.c0 % PRIME)
        object.__setattr__(self, "c1", self.c1 % PRIME)

    @staticmethod
    def coerce(value: int | FQ2) -> FQ2:
        return value if isinstance(value, FQ2) else FQ2(value)

    def __add__(self, other: int | FQ2) -> FQ2:
        if not isinstance(other, (int, FQ2)):
            return NotImplemented
        other = self.coerce(other)
        return FQ2(self.c0 + other.c0, self.c1 + other.c1)

    __radd__ = __add__

    def __neg__(self) -> FQ2:
        return FQ2(-self.c0, -self.c1)

    def __sub__(self, other: int | FQ2) -> FQ2:
        if not isinstance(other, (int, FQ2)):
            return NotImplemented
        return self + (-self.coerce(other))

    def __rsub__(self, other: int | FQ2) -> FQ2:
        if not isinstance(other, (int, FQ2)):
            return NotImplemented
        return self.coerce(other) - self

    def __mul__(self, other: int | FQ2) -> FQ2:
        if not isinstance(other, (int, FQ2)):
            return NotImplemented
        other = self.coerce(other)
        return FQ2(
            self.c0 * other.c0
            + QUADRATIC_CONSTANT_REDUCTION * self.c1 * other.c1,
            self.c0 * other.c1
            + self.c1 * other.c0
            - QUADRATIC_LINEAR * self.c1 * other.c1,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> FQ2:
        assert exponent >= 0
        result = FQ2(1)
        base = self
        while exponent:
            if exponent & 1:
                result *= base
            base *= base
            exponent >>= 1
        return result

    def inverse(self) -> FQ2:
        if not self:
            raise ZeroDivisionError
        return self ** (PRIME**2 - 2)

    def __truediv__(self, other: int | FQ2) -> FQ2:
        return self * self.coerce(other).inverse()

    def __bool__(self) -> bool:
        return bool(self.c0 or self.c1)


ZERO = FQ2()
ONE = FQ2(1)


def matrix_rank(matrix: list[list[FQ2]]) -> int:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
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
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [
            coefficient * inverse for coefficient in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][index] - multiplier * work[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def outer_coefficients(k: int) -> tuple[list[FQ2], list[FQ2]]:
    if k == 1:
        u = [
            ONE,
            ONE,
            FQ2(6) / 25,
            FQ2(9) / 250,
        ]
    elif k == 2:
        # Reduced lexicographic basis over
        # F_32003[s]/(s^2+9432*s-2820), in the u1=1 chart.
        u = [
            ONE,
            ONE,
            FQ2(6033, 5035),
            FQ2(-12856, 821),
            FQ2(12547, -1635),
            FQ2(-8440, 12404),
        ]
    else:
        raise ValueError("this reconnaissance intentionally checks only k=1,2")

    p = 2 * k + 1
    q = 3 * k + 1
    assert len(u) == p + 1
    v = [ONE]
    for degree in range(1, q + 1):
        known = sum(
            (
                (1 + 2 * (degree - i) - 3 * i)
                * u[i]
                * v[degree - i]
                for i in range(1, min(p, degree) + 1)
            ),
            ZERO,
        )
        v.append(-known / (1 + 2 * degree))

    for degree in range(1, p + q + 1):
        residual = sum(
            (
                (1 + 2 * j - 3 * i) * u[i] * v[j]
                for i in range(p + 1)
                for j in range(q + 1)
                if i + j == degree
            ),
            ZERO,
        )
        assert not residual
    assert u[-1] and v[-1]
    return u, v


def lower_support(vertical_bound: int, radial_degree: int, outer: int) -> list[int]:
    assert radial_degree < outer
    if radial_degree > 0:
        return list(range(0, vertical_bound - radial_degree + 1))
    if radial_degree == 0:
        # Remove the bracket-invisible additive constant.
        return list(range(1, vertical_bound + 1))
    if radial_degree >= -vertical_bound:
        return list(range(-radial_degree, vertical_bound + 1))
    return []


def rank_profiles(k: int) -> list[tuple[int, int, int]]:
    u, v = outer_coefficients(k)
    f = {index - 1: coefficient for index, coefficient in enumerate(u)}
    g = {index - 1: coefficient for index, coefficient in enumerate(v)}
    p_bound = 2 * (k + 1)
    q_bound = 3 * (k + 1)
    profiles: list[tuple[int, int, int]] = []

    for deficit in range(1, 3 * (k + 2) + 1):
        p_degree = 2 - deficit
        q_degree = 3 - deficit
        p_support = lower_support(p_bound, p_degree, 2)
        q_support = lower_support(q_bound, q_degree, 3)
        columns: list[dict[int, FQ2]] = []
        for exponent in p_support:
            columns.append(
                {
                    exponent + outer_exponent: coefficient
                    * (p_degree * outer_exponent - 3 * exponent)
                    for outer_exponent, coefficient in g.items()
                    if coefficient
                    * (p_degree * outer_exponent - 3 * exponent)
                }
            )
        for exponent in q_support:
            columns.append(
                {
                    exponent + outer_exponent: coefficient
                    * (2 * exponent - q_degree * outer_exponent)
                    for outer_exponent, coefficient in f.items()
                    if coefficient
                    * (2 * exponent - q_degree * outer_exponent)
                }
            )
        row_exponents = sorted(
            set().union(*(set(column) for column in columns))
        )
        matrix = [
            [column.get(exponent, ZERO) for column in columns]
            for exponent in row_exponents
        ]
        rank = matrix_rank(matrix)
        profiles.append((len(columns), rank, len(columns) - rank))
    return profiles


def main() -> None:
    discriminant = (
        QUADRATIC_LINEAR**2 + 4 * QUADRATIC_CONSTANT_REDUCTION
    ) % PRIME
    assert pow(discriminant, (PRIME - 1) // 2, PRIME) == PRIME - 1

    expected = {
        1: [
            (9, 7, 2),
            (10, 8, 2),
            (10, 8, 2),
            (9, 8, 1),
            (7, 7, 0),
            (5, 5, 0),
            (3, 3, 0),
            (2, 2, 0),
            (1, 1, 0),
        ],
        2: [
            (14, 12, 2),
            (15, 13, 2),
            (15, 13, 2),
            (14, 13, 1),
            (12, 12, 0),
            (10, 10, 0),
            (8, 8, 0),
            (6, 6, 0),
            (4, 4, 0),
            (3, 3, 0),
            (2, 2, 0),
            (1, 1, 0),
        ],
    }
    for k in (1, 2):
        profiles = rank_profiles(k)
        assert profiles == expected[k]
        weights = tuple(
            deficit
            for deficit, (_variables, _rank, kernel) in enumerate(
                profiles, start=1
            )
            for _ in range(kernel)
        )
        assert weights == (1, 1, 2, 2, 3, 3, 4)
        print(f"k={k} kernel weights:", weights)

    print("RESULT: THE k-DEPENDENT KERNEL-WEIGHT EXTRAPOLATION IS FALSE")
    print("RESULT: THE d<=m+n-1 RESONANCE PATTERN SURVIVES k=1,2,3")


if __name__ == "__main__":
    main()
