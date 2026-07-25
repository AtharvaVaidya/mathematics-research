#!/usr/bin/env python3
"""Verify the all-support mod-9 obstruction for the two w^2 seeds.

The apparent perturbation is reduced using w^2=u+u^2*v.  For k=+/-1,

    P_k = w + uv + k(u+u^2v)

has an exact characteristic-3 mate Q_k.  With the displayed integer
representatives, write

    {P_k,Q_k} = 1 + 3 E_k.

The first Hensel equation for arbitrary polynomial corrections A,B is

    {A,Q_k} + {P_k,B} = -E_k  (mod 3).

The functional ell(R)=[v]R+[uv^2]R annihilates the left side for every
reduced monomial in A and B, but ell(-E_k)=1.  Inspection of the bracket
exponents shows that only A-monomials v,v^2,vw and the B-monomial v^2 can
contribute to either coefficient in ell; the finite table checked below is
therefore an all-degree certificate, not a bounded correction search.
"""

from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import (  # noqa: E402
    add,
    basis,
    bracket,
    rref_solve_mod,
    scale,
    slice_for_p,
)


V = (0, 1, 0)
UV2 = (1, 2, 0)


def ell(poly):
    return (poly.get(V, 0) + poly.get(UV2, 0)) % 3


def seeds(k):
    P = {
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 0, 0): k,
        (2, 1, 0): k,
    }
    Q = {
        (0, 1, 0): -1,
        (0, 0, 1): 1,
        (0, 1, 1): -k,
        (1, 2, 0): 1,
        (0, 2, 1): 1,
        (1, 2, 1): k,
    }
    return P, Q


def reduced_mod_three(poly):
    return {
        monomial: coefficient % 3
        for monomial, coefficient in poly.items()
        if coefficient % 3
    }


def verify_seed(k):
    P, Q = seeds(k)
    P3 = reduced_mod_three(P)
    Q3 = reduced_mod_three(Q)
    if bracket(P3, Q3, 3) != {(0, 0, 0): 1}:
        raise AssertionError(f"k={k}: seed is not Darboux modulo 3")

    defect = add(bracket(P, Q), {(0, 0, 0): -1})
    if any(coefficient % 3 for coefficient in defect.values()):
        raise AssertionError(f"k={k}: integer defect is not divisible by 3")
    rhs = {
        monomial: (-(coefficient // 3)) % 3
        for monomial, coefficient in defect.items()
        if (-(coefficient // 3)) % 3
    }
    if ell(rhs) != 1:
        raise AssertionError(f"k={k}: obstruction does not detect the RHS")

    contributing_A = set()
    contributing_B = set()
    # This rectangle strictly contains every monomial allowed by the
    # exponent inspection in the module docstring.
    for w_degree in (0, 1):
        for u_degree in range(5):
            for v_degree in range(6):
                monomial = (u_degree, v_degree, w_degree)
                A_column = bracket({monomial: 1}, Q3, 3)
                B_column = bracket(P3, {monomial: 1}, 3)
                if A_column.get(V, 0) or A_column.get(UV2, 0):
                    contributing_A.add(monomial)
                if B_column.get(V, 0) or B_column.get(UV2, 0):
                    contributing_B.add(monomial)
                if ell(A_column) != 0 or ell(B_column) != 0:
                    raise AssertionError(
                        f"k={k}: ell does not annihilate correction {monomial}"
                    )

    expected_A = {(0, 1, 0), (0, 2, 0), (0, 1, 1)}
    expected_B = {(0, 2, 0)}
    if contributing_A != expected_A or contributing_B != expected_B:
        raise AssertionError(
            f"k={k}: unexpected contributing supports: "
            f"A={contributing_A}, B={contributing_B}"
        )

    # Independently reproduce that a mate is found in the original finite
    # characteristic-3 degree bound.
    if slice_for_p(P3, q_degree=5, p=3) is None:
        raise AssertionError(f"k={k}: exhaustive slice solver missed the seed")
    print(
        f"verified k={k}: exact mod-3 pair and all-support mod-9 obstruction"
    )


def solve_first_correction(P, Q, degree):
    P3 = reduced_mod_three(P)
    Q3 = reduced_mod_three(Q)
    defect = add(bracket(P, Q), {(0, 0, 0): -1})
    rhs = {
        monomial: (-(coefficient // 3)) % 3
        for monomial, coefficient in defect.items()
        if (-(coefficient // 3)) % 3
    }
    monomials = basis(degree)
    columns = []
    labels = []
    for which in ("A", "B"):
        for monomial in monomials:
            column = add(
                bracket({monomial: 1} if which == "A" else {}, Q3, 3),
                bracket(P3, {monomial: 1} if which == "B" else {}, 3),
                3,
            )
            columns.append(column)
            labels.append((which, monomial))
    support = sorted(set(rhs).union(*(column.keys() for column in columns)))
    solution = rref_solve_mod(
        [[column.get(monomial, 0) for column in columns] for monomial in support],
        [rhs.get(monomial, 0) for monomial in support],
        3,
    )
    if solution is None:
        return None
    A = {}
    B = {}
    for (which, monomial), coefficient in zip(labels, solution):
        if coefficient:
            (A if which == "A" else B)[monomial] = coefficient
    return A, B


def verify_w_plus_or_minus_u2_comparison():
    for k in (1, -1):
        P = {(0, 0, 1): 1, (2, 0, 0): k}
        Q = {
            (0, 1, 0): -1,
            (0, 0, 1): k,
            (1, 2, 0): 1,
            (1, 1, 1): k,
        }
        if solve_first_correction(P, Q, degree=7) is not None:
            raise AssertionError(f"k={k}: u^2 seed corrected below degree eight")
        correction = solve_first_correction(P, Q, degree=8)
        if correction is None:
            raise AssertionError(f"k={k}: missing degree-eight u^2 correction")
        A, B = correction
        lifted_P = add(P, scale(A, 3))
        lifted_Q = add(Q, scale(B, 3))
        lifted_defect = add(bracket(lifted_P, lifted_Q), {(0, 0, 0): -1})
        if any(coefficient % 9 for coefficient in lifted_defect.values()):
            raise AssertionError(f"k={k}: degree-eight correction failed modulo 9")
    print("verified comparison: w+/-u^2 first lifts occur at degree eight")


def main():
    verify_seed(1)
    verify_seed(-1)
    verify_w_plus_or_minus_u2_comparison()
    print("both w^2 Hensel obstructions passed")


if __name__ == "__main__":
    main()
