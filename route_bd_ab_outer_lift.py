#!/usr/bin/env python3
"""Modularly lift and certify the characteristic-zero a/b outer algebra.

The normalized outer equation is

    U*V + 2*w*U*V' - 3*w*U'*V = 1,
    deg(U)=7, deg(V)=10, U(0)=V(0)=1, [w]U=1.

The six compatibility equations in u2,...,u7 have a five-dimensional
lexicographic quotient at every prime used below.  We reconstruct its
triangular basis over Q by CRT and Wang rational reconstruction.  Three
independent primes are withheld from reconstruction and used as checks.

The result is then certified without a characteristic-zero Groebner basis:

* the reconstructed quintic is squarefree and irreducible;
* s*u7=1 and every coefficient of the outer ODE reduces to zero;
* hence its five roots give five normalized characteristic-zero solutions;
* the independent Hurwitz count is five, so these exhaust the outer maps.

The lift is deliberately separate from the fast verifier because it runs
64 independent modular FGLM computations (about two minutes on the
reference machine).  All computations are exact.
"""

from __future__ import annotations

import math
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from typing import Sequence

import sympy as sym
from sympy.ntheory.modular import crt

from route_bd_ab_hurwitz_count import hurwitz_number
from route_bd_fbar_obstruction import outer_compatibility_ideal


MODULAR_BASIS_COUNT = 64
HOLDOUT_COUNT = 3
WORKERS = 8


def reconstruction_primes() -> list[int]:
    """Return deterministic 31-bit good-prime candidates."""

    primes: list[int] = []
    candidate = 1_200_000_000
    while len(primes) < MODULAR_BASIS_COUNT:
        candidate = int(sym.nextprime(candidate + 100))
        primes.append(candidate)
    return primes


def rational_reconstruction(residue: int, modulus: int) -> Fraction | None:
    """Wang reconstruction using an integer, rather than floating, bound."""

    residue %= modulus
    r0, s0 = modulus, 0
    r1, s1 = residue, 1
    bound = math.isqrt(modulus // 2)
    while r1 >= bound:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        s0, s1 = s1, s0 - quotient * s1
    if not s1 or abs(s1) >= bound:
        return None
    numerator, denominator = (-r1, -s1) if s1 < 0 else (r1, s1)
    return Fraction(numerator, denominator)


def modular_lex_basis(prime: int) -> list[int]:
    """Return the 35 non-leading coefficients of the modular lex basis."""

    variables = ",".join([f"u{index}" for index in range(1, 8)] + ["s"])
    program = f"""
option(redSB);
ring outer={prime},({variables}),dp;
ideal E={outer_compatibility_ideal()};
ideal chart=E,u1-1,s*u7-1;
ideal G=std(chart);
print("VDIM");
vdim(G);
ring outerlex={prime},({variables}),lp;
ideal H=fglm(outer,G);
print("SIZE");
size(H);
H;
quit;
"""
    completed = subprocess.run(
        ["Singular", "--no-tty"],
        input=program,
        text=True,
        capture_output=True,
        check=True,
    )
    output = completed.stdout
    assert re.search(r"VDIM\s*\n5\s*\nSIZE\s*\n8", output), output[-2000:]
    rows = [
        line.split("=", 1)[1]
        for line in output.splitlines()
        if line.startswith("H[")
    ]
    assert len(rows) == 8

    s = sym.symbols("s")
    u = sym.symbols("u1:8")
    coefficients: list[int] = []
    eliminant = sym.Poly(
        sym.sympify(rows[0].replace("^", "**")),
        s,
        modulus=prime,
    )
    coefficients.extend(
        int(eliminant.nth(degree)) % prime
        for degree in range(4, -1, -1)
    )
    for row, variable in zip(rows[1:7], reversed(u[1:])):
        relation = sym.Poly(
            sym.sympify(row.replace("^", "**")) - variable,
            s,
            modulus=prime,
        )
        coefficients.extend(
            int(relation.nth(degree)) % prime
            for degree in range(4, -1, -1)
        )
    assert len(coefficients) == 35
    return coefficients


def lift_coefficients(
    primes: Sequence[int],
    modular_bases: dict[int, list[int]],
) -> list[Fraction]:
    """CRT-lift with three primes reserved for independent validation."""

    holdouts = list(primes[:HOLDOUT_COUNT])
    lifting_primes = list(primes[HOLDOUT_COUNT:])
    modulus = math.prod(lifting_primes)
    coefficients: list[Fraction] = []
    for column in range(35):
        residue = int(
            crt(
                lifting_primes,
                [modular_bases[prime][column] for prime in lifting_primes],
            )[0]
        )
        reconstructed = rational_reconstruction(residue, modulus)
        assert reconstructed is not None, (
            column,
            len(str(modulus)),
        )
        coefficients.append(reconstructed)

    for prime in holdouts:
        for coefficient, expected in zip(coefficients, modular_bases[prime]):
            assert coefficient.denominator % prime
            actual = (
                coefficient.numerator
                * pow(coefficient.denominator, -1, prime)
            ) % prime
            assert actual == expected
    return coefficients


def quotient_data(
    coefficients: Sequence[Fraction],
) -> tuple[sym.Symbol, sym.Poly, list[sym.Expr], list[sym.Expr]]:
    """Build U,V in Q[s]/(f) and verify every outer coefficient."""

    s, w = sym.symbols("s w")
    rows = [
        sum(
            sym.Rational(value.numerator, value.denominator) * s ** (4 - index)
            for index, value in enumerate(coefficients[offset : offset + 5])
        )
        for offset in range(0, 35, 5)
    ]
    eliminant = sym.Poly(s**5 + rows[0], s, domain=sym.QQ)
    assert sym.gcd(eliminant, eliminant.diff()) == 1
    assert eliminant.is_irreducible

    def reduce_s(expression: sym.Expr) -> sym.Expr:
        return sym.rem(
            sym.Poly(sym.cancel(expression), s, domain=sym.QQ),
            eliminant,
        ).as_expr()

    u: list[sym.Expr] = [sym.Integer(1), sym.Integer(1)] + [sym.Integer(0)] * 6
    for row, degree in zip(rows[1:], range(7, 1, -1)):
        u[degree] = reduce_s(-row)
    assert reduce_s(s * u[7] - 1) == 0

    v: list[sym.Expr] = [sym.Integer(1)]
    for degree in range(1, 11):
        known = sum(
            (
                (1 + 2 * (degree - index) - 3 * index)
                * u[index]
                * v[degree - index]
                for index in range(1, min(7, degree) + 1)
            ),
            sym.Integer(0),
        )
        v.append(reduce_s(-known / (1 + 2 * degree)))

    for degree in range(1, 18):
        residual = sum(
            (
                (1 + 2 * j - 3 * i) * u[i] * v[j]
                for i in range(8)
                for j in range(11)
                if i + j == degree
            ),
            sym.Integer(0),
        )
        assert reduce_s(residual) == 0, degree

    U = sum(u[index] * w**index for index in range(8))
    V = sum(v[index] * w**index for index in range(11))
    outer = sym.expand(U * V + 2 * w * U * sym.diff(V, w) - 3 * w * sym.diff(U, w) * V - 1)
    for coefficient in sym.Poly(outer, w).all_coeffs():
        assert reduce_s(coefficient) == 0
    return s, eliminant, u, v


def main() -> None:
    assert subprocess.run(
        ["Singular", "--version"],
        capture_output=True,
        check=True,
    )
    primes = reconstruction_primes()
    modular_bases: dict[int, list[int]] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(modular_lex_basis, prime): prime
            for prime in primes
        }
        for completed_count, future in enumerate(as_completed(futures), 1):
            prime = futures[future]
            modular_bases[prime] = future.result()
            if completed_count % 8 == 0:
                print(f"modular bases: {completed_count}/{len(primes)}", flush=True)

    coefficients = lift_coefficients(primes, modular_bases)
    _s, eliminant, _u, _v = quotient_data(coefficients)
    _character_sum, weighted_count, _nonzero_terms = hurwitz_number()
    assert weighted_count == 5

    primitive_eliminant = eliminant.clear_denoms()[1].primitive()[1]
    print("outer eliminant:")
    print(primitive_eliminant.as_expr())
    print("CRT digits:", len(str(math.prod(primes[HOLDOUT_COUNT:]))))
    print("holdout primes:", *primes[:HOLDOUT_COUNT])
    print("RESULT: EXACT Q OUTER ALGEBRA HAS FIVE HURWITZ-EXHAUSTIVE POINTS")


if __name__ == "__main__":
    main()
