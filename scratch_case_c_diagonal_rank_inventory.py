#!/usr/bin/env python3
"""Linear rank inventory for case c in the diagonal a/b chart.

After z=xy and w=xy^2, case c is a finite Laurent extension of the a/b
five-block form.  This script fixes one point of the known cubic outer
factor over F_32003 and computes the rank/kernel/cokernel dimensions of
each new descending radial block.
"""

from __future__ import annotations

from route_bd_fbar_obstruction import (
    K,
    ONE,
    T,
    ZERO,
    outer_coefficients,
    rref,
)


Laurent = dict[int, K]


def derivative(poly: Laurent) -> Laurent:
    return {
        exponent - 1: coefficient * exponent
        for exponent, coefficient in poly.items()
        if exponent and coefficient
    }


def multiply(left: Laurent, right: Laurent) -> Laurent:
    result: Laurent = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, ZERO)
                + left_coefficient * right_coefficient
            )
            if not result[exponent]:
                del result[exponent]
    return result


def add(*polys: Laurent) -> Laurent:
    result: Laurent = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            result[exponent] = result.get(exponent, ZERO) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def scale_shift(poly: Laurent, scalar: int | K, shift: int) -> Laurent:
    scalar = K.coerce(scalar)
    return {
        exponent + shift: scalar * coefficient
        for exponent, coefficient in poly.items()
        if scalar * coefficient
    }


def bracket_block(
    left_degree: int,
    left: Laurent,
    right_degree: int,
    right: Laurent,
) -> Laurent:
    # [z^i*A(w),z^j*B(w)]
    # =z^(i+j-1)*w*(i*A*B'-j*A'*B).
    return add(
        scale_shift(
            multiply(left, derivative(right)),
            left_degree,
            1,
        ),
        scale_shift(
            multiply(derivative(left), right),
            -right_degree,
            1,
        ),
    )


def supports(radial_degree: int, is_q: bool) -> tuple[int, ...]:
    maximum = 12 if is_q else 8
    if radial_degree >= 0:
        if is_q:
            return tuple(range(13 - radial_degree))
        return tuple(range(9 - radial_degree))
    return tuple(range(-radial_degree, maximum + 1))


def matrix_for_stage(
    stage: int,
    a2: Laurent,
    b3: Laurent,
) -> tuple[list[list[K]], tuple[int, ...], int, int]:
    new_a_degree = stage - 2
    new_b_degree = stage - 1
    a_support = (
        supports(new_a_degree, False)
        if -8 <= new_a_degree <= -1
        else ()
    )
    b_support = (
        supports(new_b_degree, True)
        if -12 <= new_b_degree <= 0
        else ()
    )
    columns: list[Laurent] = []
    for exponent in a_support:
        columns.append(
            bracket_block(
                new_a_degree,
                {exponent: ONE},
                3,
                b3,
            )
        )
    for exponent in b_support:
        columns.append(
            bracket_block(
                2,
                a2,
                new_b_degree,
                {exponent: ONE},
            )
        )
    row_exponents = tuple(
        sorted(
            {
                exponent
                for column in columns
                for exponent in column
            }
        )
    )
    matrix = [
        [column.get(exponent, ZERO) for column in columns]
        for exponent in row_exponents
    ]
    return matrix, row_exponents, len(a_support), len(b_support)


def main() -> None:
    u, v = outer_coefficients(T)
    a2 = {-1: ONE}
    a2.update({index: coefficient for index, coefficient in enumerate(u[1:])})
    b3 = {-1: ONE}
    b3.update({index: coefficient for index, coefficient in enumerate(v[1:])})

    print("stage,newA,newB,rows,variables,rank,kernel,cokernel,row-range")
    for stage in range(1, -12, -1):
        matrix, rows, a_count, b_count = matrix_for_stage(stage, a2, b3)
        _, pivots = rref(matrix)
        variables = a_count + b_count
        print(
            stage,
            stage - 2 if a_count else None,
            stage - 1 if b_count else None,
            len(rows),
            variables,
            len(pivots),
            variables - len(pivots),
            len(rows) - len(pivots),
            (rows[0], rows[-1]) if rows else (),
            sep=",",
        )


if __name__ == "__main__":
    main()
