#!/usr/bin/env python3
"""Reconstruct an exact (3,5)-cell lead-membership certificate.

This is a controlled modular calculation, not a rational Groebner run.
A raw ``lift(I, <L>)`` is not canonical: two lifts can differ by any
syzygy of the six generators, and in this problem that ambiguity has
dimension 397 on the measured fixed support.  Coefficientwise CRT of raw
lifts is therefore invalid even when their monomial supports agree.

For every prime, this script instead computes a lift

    L = sum_i multiplier_i * generator_i

and reduces its multiplier vector modulo a standard basis of the full
syzygy module.  The resulting module normal form is canonical whenever
the leading module is stable.  Its support is required to agree with the
first good prime before coefficients are combined by CRT, rationally
reconstructed, and checked over Q exactly.

Use ``--emit-json`` to export the reconstructed support and coefficients
to stdout.  The script itself never writes generated certificate files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass

import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.modulargcd import _integer_rational_reconstruction

from route_bd_ab_delta1_five_cell_global import (
    fractional_system,
    singular_expression,
    triangular_data,
)


PRIMES = tuple(int(prime) for prime in tuple(sp.primerange(32003, 34000))[:100])


Monomial = tuple[int, ...]


@dataclass
class ModularCertificate:
    supports: tuple[tuple[Monomial, ...], ...]
    coefficients: tuple[tuple[int, ...], ...]


def certificate_system() -> tuple[
    list[sp.Expr],
    tuple[sp.Symbol, ...],
    sp.Expr,
]:
    A, B_tilde, remainder = triangular_data()
    return fractional_system(A, B_tilde, remainder, 3, 5)


def canonical_modular_certificate(
    prime: int,
    generators: list[sp.Expr],
    variables: tuple[sp.Symbol, ...],
    leading: sp.Expr,
) -> ModularCertificate:
    executable = shutil.which("Singular")
    assert executable is not None, "Singular is required"
    names = ",".join(map(str, variables))
    ideal = ",".join(singular_expression(generator) for generator in generators)
    target = singular_expression(leading)
    program = (
        f"ring r={prime},({names}),(dp,C);\n"
        f"ideal I={ideal};\n"
        f"ideal U={target};\n"
        "matrix M=lift(I,U);\n"
        "module V=M;\n"
        "option(returnSB);\n"
        "option(redSB);\n"
        "option(redTail);\n"
        "module G=syz(I);\n"
        "module N=reduce(V,G);\n"
        "int i;\n"
        f"for(i=1;i<={len(generators)};i++)"
        '{print("BEGIN"); print(i); print(N[1][i]); print("END");}\n'
        "quit;\n"
    )
    completed = subprocess.run(
        [executable, "-q"],
        input=program,
        text=True,
        capture_output=True,
        timeout=120,
        check=True,
    )
    assert completed.stderr == ""
    chunks = re.findall(
        r"BEGIN\n(\d+)\n(.*?)\nEND",
        completed.stdout,
        flags=re.DOTALL,
    )
    assert len(chunks) == len(generators)
    local_symbols = {str(variable): variable for variable in variables}

    all_supports: list[tuple[Monomial, ...]] = []
    all_coefficients: list[tuple[int, ...]] = []
    for expected_index, (raw_index, raw_polynomial) in enumerate(chunks, start=1):
        assert int(raw_index) == expected_index
        expression = sp.sympify(
            raw_polynomial.replace("^", "**"),
            locals=local_symbols,
        )
        terms = sp.Poly(
            expression,
            *variables,
            modulus=prime,
        ).terms()
        all_supports.append(tuple(monomial for monomial, _coefficient in terms))
        all_coefficients.append(
            tuple(int(coefficient) % prime for _monomial, coefficient in terms)
        )
    return ModularCertificate(tuple(all_supports), tuple(all_coefficients))


def support_digest(supports: tuple[tuple[Monomial, ...], ...]) -> str:
    payload = json.dumps(supports, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def crt_update(
    residues: list[list[int]],
    modulus: int,
    modular: ModularCertificate,
    prime: int,
) -> int:
    inverse = pow(modulus, -1, prime)
    for row, new_coefficients in zip(residues, modular.coefficients):
        assert len(row) == len(new_coefficients)
        for index, new_value in enumerate(new_coefficients):
            correction = ((new_value - row[index]) % prime) * inverse % prime
            row[index] += modulus * correction
    return modulus * prime


def rational_reconstruct(
    residues: list[list[int]],
    modulus: int,
) -> list[list[sp.Rational]] | None:
    reconstructed: list[list[sp.Rational]] = []
    for row in residues:
        reconstructed_row: list[sp.Rational] = []
        for residue in row:
            value = _integer_rational_reconstruction(
                ZZ(residue),
                ZZ(modulus),
                ZZ,
            )
            if value is None:
                return None
            reconstructed_row.append(
                sp.Rational(int(value.numerator), int(value.denominator))
            )
        reconstructed.append(reconstructed_row)
    return reconstructed


def reconstruction_count(residues: list[list[int]], modulus: int) -> int:
    count = 0
    for row in residues:
        for residue in row:
            if (
                _integer_rational_reconstruction(
                    ZZ(residue),
                    ZZ(modulus),
                    ZZ,
                )
                is not None
            ):
                count += 1
    return count


def exact_identity_holds(
    supports: tuple[tuple[Monomial, ...], ...],
    coefficients: list[list[sp.Rational]],
    generators: list[sp.Expr],
    variables: tuple[sp.Symbol, ...],
    leading: sp.Expr,
) -> bool:
    total = sp.Poly(0, *variables, domain=sp.QQ)
    for support, coefficient_row, generator in zip(
        supports,
        coefficients,
        generators,
    ):
        multiplier = sp.Poly.from_dict(
            dict(zip(support, coefficient_row)),
            variables,
            domain=sp.QQ,
        )
        total += multiplier * sp.Poly(generator, *variables, domain=sp.QQ)
    total -= sp.Poly(leading, *variables, domain=sp.QQ)
    return total.is_zero


def certificate_payload(
    supports: tuple[tuple[Monomial, ...], ...],
    coefficients: list[list[sp.Rational]],
    primes_used: list[int],
) -> dict[str, object]:
    return {
        "variables": ["a0", "a4", "a5", "a6", "a7"],
        "primes_used": primes_used,
        "support_sha256": support_digest(supports),
        "multipliers": [
            [
                {
                    "monomial": list(monomial),
                    "numerator": int(coefficient.p),
                    "denominator": int(coefficient.q),
                }
                for monomial, coefficient in zip(support, coefficient_row)
            ]
            for support, coefficient_row in zip(supports, coefficients)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-json", action="store_true")
    parser.add_argument("--max-primes", type=int, default=len(PRIMES))
    arguments = parser.parse_args()
    assert 2 <= arguments.max_primes <= len(PRIMES)

    generators, variables, leading = certificate_system()
    first_prime = PRIMES[0]
    first = canonical_modular_certificate(
        first_prime, generators, variables, leading
    )
    supports = first.supports
    residues = [list(row) for row in first.coefficients]
    modulus = first_prime
    primes_used = [first_prime]

    print("support sha256:", support_digest(supports))
    print("support sizes:", tuple(map(len, supports)))

    exact_coefficients: list[list[sp.Rational]] | None = None
    for prime in PRIMES[1 : arguments.max_primes]:
        modular = canonical_modular_certificate(
            prime, generators, variables, leading
        )
        if modular.supports != supports:
            print("bad prime skipped (support changed):", prime)
            continue
        modulus = crt_update(residues, modulus, modular, prime)
        primes_used.append(prime)
        candidate = rational_reconstruct(residues, modulus)
        reconstructed = candidate is not None
        verified = reconstructed and exact_identity_holds(
            supports,
            candidate,
            generators,
            variables,
            leading,
        )
        print(
            "prime:",
            prime,
            "modulus_bits:",
            modulus.bit_length(),
            "coefficients_reconstructed:",
            reconstruction_count(residues, modulus),
            "reconstructed:",
            reconstructed,
            "verified:",
            verified,
        )
        if verified:
            exact_coefficients = candidate
            break

    if exact_coefficients is None:
        print("RESULT: NO VERIFIED RATIONAL RECONSTRUCTION")
        raise SystemExit(1)

    maximum_numerator_bits = max(
        abs(int(coefficient.p)).bit_length()
        for row in exact_coefficients
        for coefficient in row
    )
    maximum_denominator_bits = max(
        int(coefficient.q).bit_length()
        for row in exact_coefficients
        for coefficient in row
    )
    print("primes used:", tuple(primes_used))
    print("maximum numerator bits:", maximum_numerator_bits)
    print("maximum denominator bits:", maximum_denominator_bits)
    print("RESULT: EXACT Q CERTIFICATE VERIFIED")
    if arguments.emit_json:
        print(
            json.dumps(
                certificate_payload(supports, exact_coefficients, primes_used),
                separators=(",", ":"),
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
