#!/usr/bin/env python3
"""Verify the all-support mod-9 obstruction for the new uv^3 seed.

Over F_3 the Hamiltonian

    P = w + uv + uv^3

has the degree-nine mate Q displayed in ``seed()``.  For the centered
integer representatives write

    {P,Q} = 1 + 3E.

The first Hensel equation for arbitrary polynomial corrections A,B is

    {A,Q} + {P,B} = -E  (mod 3).

The functional

    ell(R) = [v^4]R + [uv^5]R

annihilates the left side for every reduced monomial in A and B, but
ell(-E)=1.  A bracket term contributing to either target coefficient can
lower either input exponent by at most one; hence it is enough to inspect
u-degree <=2 and v-degree <=6 (the larger rectangle used below includes
these bounds).  The only contributing A-monomials are v, v^2, v^5, and
v^4*w, and the only contributing B-monomial is v^5.  Thus this is an
all-degree certificate rather than a bounded correction search.
"""

from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import add, bracket, slice_for_p  # noqa: E402


V4 = (0, 4, 0)
UV5 = (1, 5, 0)


def ell(poly):
    return (poly.get(V4, 0) + poly.get(UV5, 0)) % 3


def seed():
    P = {
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 3, 0): 1,
    }
    Q = {
        (1, 0, 0): -1,
        (0, 1, 0): -1,
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        (2, 1, 0): -1,
        (1, 2, 0): 1,
        (1, 1, 1): 1,
        (0, 2, 1): 1,
        (2, 2, 0): -1,
        (0, 3, 1): 1,
        (1, 4, 0): 1,
        (1, 3, 1): 1,
        (0, 4, 1): -1,
        (1, 4, 1): 1,
        (2, 5, 0): -1,
        (1, 5, 1): -1,
        (0, 6, 1): 1,
        (1, 7, 1): 1,
    }
    return P, Q


def reduced_mod_three(poly):
    return {
        monomial: coefficient % 3
        for monomial, coefficient in poly.items()
        if coefficient % 3
    }


def main():
    P, Q = seed()
    P3 = reduced_mod_three(P)
    Q3 = reduced_mod_three(Q)
    if bracket(P3, Q3, 3) != {(0, 0, 0): 1}:
        raise AssertionError("uv^3 seed is not Darboux modulo 3")

    defect = add(bracket(P, Q), {(0, 0, 0): -1})
    if any(coefficient % 3 for coefficient in defect.values()):
        raise AssertionError("uv^3 integer defect is not divisible by 3")
    rhs = {
        monomial: (-(coefficient // 3)) % 3
        for monomial, coefficient in defect.items()
        if (-(coefficient // 3)) % 3
    }
    if ell(rhs) != 1:
        raise AssertionError("uv^3 obstruction does not detect the RHS")

    contributing_A = set()
    contributing_B = set()
    for w_degree in (0, 1):
        for u_degree in range(5):
            for v_degree in range(9):
                monomial = (u_degree, v_degree, w_degree)
                A_column = bracket({monomial: 1}, Q3, 3)
                B_column = bracket(P3, {monomial: 1}, 3)
                if A_column.get(V4, 0) or A_column.get(UV5, 0):
                    contributing_A.add(monomial)
                if B_column.get(V4, 0) or B_column.get(UV5, 0):
                    contributing_B.add(monomial)
                if ell(A_column) != 0 or ell(B_column) != 0:
                    raise AssertionError(
                        f"ell does not annihilate correction {monomial}"
                    )

    expected_A = {
        (0, 1, 0),
        (0, 2, 0),
        (0, 5, 0),
        (0, 4, 1),
    }
    expected_B = {(0, 5, 0)}
    if contributing_A != expected_A or contributing_B != expected_B:
        raise AssertionError(
            "unexpected uv^3 contributing supports: "
            f"A={contributing_A}, B={contributing_B}"
        )

    if slice_for_p(P3, q_degree=9, p=3) is None:
        raise AssertionError("degree-nine slice solver missed the uv^3 seed")
    print("verified: exact uv^3 mod-3 pair and all-support mod-9 obstruction")


if __name__ == "__main__":
    main()
