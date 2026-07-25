#!/usr/bin/env python3
"""Build the characteristic-3 Hensel tower in the equivariant subansatz.

Set s=uv, P=w*a(s), Q=v*b(s).  A direct calculation gives

    {P,Q} = -(1/a) * d/ds [s(1+s)*a(s)^2*b(s)].

Equivalently, the Darboux equation is

    E(a,b) := d/ds [s(1+s)*a(s)^2*b(s)] + a(s) = 0.

The seed a=1, b=s+2 is an exact solution modulo 3.  This script performs
coefficientwise exact Hensel lifting and reports the minimum correction degree
at each stage (within corrections of equal degree bound for a and b).
"""

from __future__ import annotations

import argparse
import sys

from route_a_search import rref_solve_mod


Poly = dict[int, int]


def add(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for degree, coefficient in b.items():
        out[degree] = out.get(degree, 0) + coefficient
        if not out[degree]:
            del out[degree]
    return out


def scale(a: Poly, coefficient: int) -> Poly:
    return {degree: coefficient * value for degree, value in a.items() if coefficient * value}


def mul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for i, c in a.items():
        for j, d in b.items():
            out[i + j] = out.get(i + j, 0) + c * d
    return {degree: coefficient for degree, coefficient in out.items() if coefficient}


def derivative(a: Poly) -> Poly:
    return {degree - 1: degree * coefficient for degree, coefficient in a.items() if degree}


def reduce_mod(a: Poly, modulus: int) -> Poly:
    return {degree: coefficient % modulus for degree, coefficient in a.items() if coefficient % modulus}


S_ONE_PLUS_S = {1: 1, 2: 1}


def error(a: Poly, b: Poly) -> Poly:
    return add(derivative(mul(S_ONE_PLUS_S, mul(mul(a, a), b))), a)


def bracket(a: Poly, b: Poly) -> Poly:
    """Return {w*a(uv), v*b(uv)} as a univariate polynomial in s."""
    first = mul(scale(mul(S_ONE_PLUS_S, derivative(a)), 2), b)
    second_factor = add(mul({0: 1, 1: 2}, b), mul(S_ONE_PLUS_S, derivative(b)))
    return scale(add(first, mul(a, second_factor)), -1)


def linearized_error(alpha: Poly, beta: Poly) -> Poly:
    """Linearization of E at a0=1, b0=s+2, reduced modulo 3 later."""
    a0 = {0: 1}
    b0 = {0: 2, 1: 1}
    inside = add(mul(scale(mul(a0, b0), 2), alpha), mul(mul(a0, a0), beta))
    return add(derivative(mul(S_ONE_PLUS_S, inside)), alpha)


def solve_correction(rhs: Poly, degree_bound: int):
    columns = []
    labels = []
    for which in ("alpha", "beta"):
        for degree in range(degree_bound + 1):
            alpha = {degree: 1} if which == "alpha" else {}
            beta = {degree: 1} if which == "beta" else {}
            columns.append(reduce_mod(linearized_error(alpha, beta), 3))
            labels.append((which, degree))
    support = sorted(set(rhs).union(*(column.keys() for column in columns)))
    matrix = [[column.get(degree, 0) for column in columns] for degree in support]
    target = [rhs.get(degree, 0) for degree in support]
    solution = rref_solve_mod(matrix, target, 3)
    if solution is None:
        return None
    alpha: Poly = {}
    beta: Poly = {}
    for (which, degree), coefficient in zip(labels, solution):
        if coefficient:
            (alpha if which == "alpha" else beta)[degree] = coefficient
    return alpha, beta


def format_poly(a: Poly) -> str:
    if not a:
        return "0"
    return " + ".join(f"({a[d]})s^{d}" for d in sorted(a))


def lift(stages: int, max_degree: int):
    # This representative makes the first error exactly -3(1+s)^2,
    # matching the deformation equation used in the research brief.
    a: Poly = {0: 1}
    b: Poly = {0: 2, 1: 1}
    for n in range(1, stages + 1):
        modulus = 3**n
        current_error = error(a, b)
        if any(coefficient % modulus for coefficient in current_error.values()):
            raise AssertionError(f"stage {n}: E is not divisible by {modulus}")
        rhs = reduce_mod(
            {degree: -(coefficient // modulus) for degree, coefficient in current_error.items()},
            3,
        )
        correction = None
        minimum_degree = None
        for degree_bound in range(max_degree + 1):
            correction = solve_correction(rhs, degree_bound)
            if correction is not None:
                minimum_degree = degree_bound
                break
        if correction is None:
            print(f"stage {n}: no correction through degree {max_degree}")
            return 1
        alpha, beta = correction
        a = add(a, scale(alpha, modulus))
        b = add(b, scale(beta, modulus))
        next_modulus = modulus * 3
        direct_bracket = bracket(a, b)
        bracket_error = add(direct_bracket, {0: -1})
        verified = not any(coefficient % next_modulus for coefficient in bracket_error.values())
        print(f"stage {n}: minimum correction degree {minimum_degree}")
        print("  alpha =", format_poly(alpha))
        print("  beta  =", format_poly(beta))
        print(f"  verified {{P,Q}}=1 mod {next_modulus}: {verified}")
        if not verified:
            return 2
    print("a =", format_poly(a))
    print("b =", format_poly(b))
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stages", type=int, default=6)
    parser.add_argument("--max-degree", type=int, default=100)
    args = parser.parse_args()
    sys.exit(lift(args.stages, args.max_degree))


if __name__ == "__main__":
    main()
