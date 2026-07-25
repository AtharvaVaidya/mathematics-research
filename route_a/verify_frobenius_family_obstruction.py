#!/usr/bin/env python3
"""Verify the Frobenius-central seed family and its mod-9 obstruction.

Let H be any positive-degree element of B over F_3 and put A=1+H^3.
Since A is Poisson central, the identities

    P = w + A*uv,
    Q = -v + uv^2 + A*v^2w

give {P,Q}=1.  Treating A as a central indeterminate, the unreduced
integer bracket has all nonconstant coefficients divisible by three.

For any centered integer lift of H, the functional

    ell(R) = [v]R + [uv^2]R

annihilates the full first-correction image but detects the integer
defect.  Reduced monomials in H^3 have the forms

    u^(3i)v^(3j),
    u^(3i+1)v^(3j)w, and u^(3i+2)v^(3j+1)w.

For positive-degree H these cannot alter either selected low coefficient.
Only the A-correction monomial vw and B-correction monomial v^2 can
contribute, and their two coefficients sum to zero.  Thus the
obstruction is support-independent.

The degree-five specializations H=v and H=u are:

For k=+/-1, both

    P_v = w + uv + k*uv^4,
    Q_v = -v + uv^2 + v^2w + k*v^5w

and

    P_u = w + uv + k*u^4v,
    Q_u = -v + uv^2 + v^2w + k*u^3v^2w

have bracket one over F_3.  For the centered integer representatives,
write {P,Q}=1+3E.  In all four cases the functional

    ell(R) = [v]R + [uv^2]R

annihilates every first-correction column but has ell(-E)=1.  Only the
A-monomial vw and the B-monomial v^2 can contribute to the selected
coefficients.  Exponent inspection bounds any possible contributor by
u-degree two and v-degree three; the larger rectangle below therefore
constitutes an all-support certificate.
"""

from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import add, bracket, mul, slice_for_p  # noqa: E402


V = (0, 1, 0)
UV2 = (1, 2, 0)


def ell(poly):
    return (poly.get(V, 0) + poly.get(UV2, 0)) % 3


def reduced_mod_three(poly):
    return {
        monomial: coefficient % 3
        for monomial, coefficient in poly.items()
        if coefficient % 3
    }


def seed(orbit, k):
    if orbit == "uv4":
        perturbation = (1, 4, 0)
        mate_perturbation = (0, 5, 1)
    elif orbit == "u4v":
        perturbation = (4, 1, 0)
        mate_perturbation = (3, 2, 1)
    else:
        raise ValueError(f"unknown orbit: {orbit}")
    P = {
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        perturbation: k,
    }
    Q = {
        (0, 1, 0): -1,
        (1, 2, 0): 1,
        (0, 2, 1): 1,
        mate_perturbation: k,
    }
    return P, Q


def verify_seed(orbit, k):
    P, Q = seed(orbit, k)
    P3 = reduced_mod_three(P)
    Q3 = reduced_mod_three(Q)
    if bracket(P3, Q3, 3) != {(0, 0, 0): 1}:
        raise AssertionError(f"{orbit}, k={k}: seed is not Darboux modulo 3")

    defect = add(bracket(P, Q), {(0, 0, 0): -1})
    if any(coefficient % 3 for coefficient in defect.values()):
        raise AssertionError(f"{orbit}, k={k}: defect is not divisible by 3")
    rhs = {
        monomial: (-(coefficient // 3)) % 3
        for monomial, coefficient in defect.items()
        if (-(coefficient // 3)) % 3
    }
    if ell(rhs) != 1:
        raise AssertionError(f"{orbit}, k={k}: ell misses the RHS")

    contributing_A = set()
    contributing_B = set()
    for w_degree in (0, 1):
        for u_degree in range(5):
            for v_degree in range(7):
                monomial = (u_degree, v_degree, w_degree)
                A_column = bracket({monomial: 1}, Q3, 3)
                B_column = bracket(P3, {monomial: 1}, 3)
                if A_column.get(V, 0) or A_column.get(UV2, 0):
                    contributing_A.add(monomial)
                if B_column.get(V, 0) or B_column.get(UV2, 0):
                    contributing_B.add(monomial)
                if ell(A_column) != 0 or ell(B_column) != 0:
                    raise AssertionError(
                        f"{orbit}, k={k}: ell fails on {monomial}"
                    )

    if contributing_A != {(0, 1, 1)}:
        raise AssertionError(
            f"{orbit}, k={k}: unexpected A support {contributing_A}"
        )
    if contributing_B != {(0, 2, 0)}:
        raise AssertionError(
            f"{orbit}, k={k}: unexpected B support {contributing_B}"
        )
    if slice_for_p(P3, q_degree=6, p=3) is None:
        raise AssertionError(f"{orbit}, k={k}: slice solver missed the seed")
    print(f"verified {orbit}, k={k}: exact pair and all-support obstruction")


def verify_frobenius_specializations():
    representatives = {
        "0": {},
        "u": {(1, 0, 0): 1},
        "v": {(0, 1, 0): 1},
        "w": {(0, 0, 1): 1},
        "u+v": {(1, 0, 0): 1, (0, 1, 0): 1},
        "uv+w": {(1, 1, 0): 1, (0, 0, 1): 1},
    }
    for name, H in representatives.items():
        H3 = mul(mul(H, H), H)
        central_factor = add({(0, 0, 0): 1}, H3)
        P = add(
            {(0, 0, 1): 1},
            mul(central_factor, {(1, 1, 0): 1}),
        )
        Q = add(
            {(0, 1, 0): -1, (1, 2, 0): 1},
            mul(central_factor, {(0, 2, 1): 1}),
        )
        P3 = reduced_mod_three(P)
        Q3 = reduced_mod_three(Q)
        if bracket(P3, Q3, 3) != {(0, 0, 0): 1}:
            raise AssertionError(f"H={name}: Frobenius pair failed")

        defect = add(bracket(P, Q), {(0, 0, 0): -1})
        if any(coefficient % 3 for coefficient in defect.values()):
            raise AssertionError(f"H={name}: defect is not divisible by 3")
        rhs = {
            monomial: (-(coefficient // 3)) % 3
            for monomial, coefficient in defect.items()
            if (-(coefficient // 3)) % 3
        }
        if ell(rhs) != 1:
            raise AssertionError(f"H={name}: ell misses the defect")

        contributing_A = set()
        contributing_B = set()
        for w_degree in (0, 1):
            for u_degree in range(7):
                for v_degree in range(9):
                    monomial = (u_degree, v_degree, w_degree)
                    A_column = bracket({monomial: 1}, Q3, 3)
                    B_column = bracket(P3, {monomial: 1}, 3)
                    if A_column.get(V, 0) or A_column.get(UV2, 0):
                        contributing_A.add(monomial)
                    if B_column.get(V, 0) or B_column.get(UV2, 0):
                        contributing_B.add(monomial)
                    if ell(A_column) != 0 or ell(B_column) != 0:
                        raise AssertionError(
                            f"H={name}: ell fails on {monomial}"
                        )
        if contributing_A != {(0, 1, 1)}:
            raise AssertionError(
                f"H={name}: unexpected A support {contributing_A}"
            )
        if contributing_B != {(0, 2, 0)}:
            raise AssertionError(
                f"H={name}: unexpected B support {contributing_B}"
            )
    print("verified: Frobenius-central family representatives and universal ell")


def main():
    verify_frobenius_specializations()
    for orbit in ("uv4", "u4v"):
        for k in (1, -1):
            verify_seed(orbit, k)
    print("Frobenius-family Hensel obstructions passed")


if __name__ == "__main__":
    main()
