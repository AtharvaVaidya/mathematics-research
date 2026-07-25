#!/usr/bin/env python3
"""Exclude every quadratic--quadratic Darboux pair in the fixed-plane ring.

The coefficient wedge of two elements in the nine-dimensional target
polynomial space of degrees one and two must be decomposable.  The bracket
equations are linear in that wedge.  Their exact affine solution forces a
four-index Pluecker coordinate to be 9/16, whereas decomposability forces it
to vanish.
"""

from itertools import combinations

import sympy as sp


t, c = sp.symbols("t c")
A, B, C = sp.symbols("A B C")

a = sp.expand(t + t**2 - c * t**3)
b = sp.expand(2 + 4 * t - 3 * c * t**2)


def jacobian(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, t) * sp.diff(right, c)
        - sp.diff(left, c) * sp.diff(right, t)
    )


target_basis: list[sp.Expr] = []
for total_degree in range(1, 3):
    for exponent_a in range(total_degree, -1, -1):
        for exponent_b in range(
            total_degree - exponent_a, -1, -1
        ):
            exponent_c = total_degree - exponent_a - exponent_b
            target_basis.append(
                sp.expand(
                    (
                        A**exponent_a
                        * B**exponent_b
                        * C**exponent_c
                    ).subs({A: a, B: b, C: c})
                )
            )

assert len(target_basis) == 9
pairs = list(combinations(range(len(target_basis)), 2))
pair_index = {pair: index for index, pair in enumerate(pairs)}
bracket_columns = [
    jacobian(target_basis[left], target_basis[right])
    for left, right in pairs
]
dictionaries = [
    sp.Poly(column, t, c).as_dict() for column in bracket_columns
]
rows = sorted(
    {(0, 0)}.union(
        exponent for dictionary in dictionaries for exponent in dictionary
    )
)
matrix = sp.Matrix(
    [
        [dictionary.get(exponent, 0) for dictionary in dictionaries]
        for exponent in rows
    ]
)
target = sp.Matrix([int(exponent == (0, 0)) for exponent in rows])

assert matrix.rank() == 26
assert matrix.row_join(target).rank() == 26
solution = list(sp.linsolve((matrix, target)))[0]


def wedge(left: int, right: int) -> sp.Expr:
    return solution[pair_index[(left, right)]]


# The bracket equations alone force these six wedge coordinates.
assert wedge(3, 6) == 0
assert wedge(3, 7) == 0
assert wedge(6, 8) == 0
assert wedge(7, 8) == 0
assert wedge(3, 8) == -sp.Rational(9, 4)
assert wedge(6, 7) == -sp.Rational(1, 4)

# A decomposable two-vector obeys every Pluecker relation.  On the four
# indices 3,6,7,8 the forced affine solution instead gives 9/16.
pluecker_3678 = sp.expand(
    wedge(3, 6) * wedge(7, 8)
    - wedge(3, 7) * wedge(6, 8)
    + wedge(3, 8) * wedge(6, 7)
)
assert pluecker_3678 == sp.Rational(9, 16)

print("verified complete quadratic-quadratic bracket solution space")
print("forced Pluecker coordinate:", pluecker_3678)
print("RESULT: NO FIXED-PLANE DARBOUX PAIR WITH BOTH DEGREES <= 2")
