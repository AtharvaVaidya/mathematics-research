#!/usr/bin/env python3
"""Exact-Q audit of the two generic case-c n=3 charts.

This is deliberately separate from
``route_bd_case_c_n3_generic_charts.py``.  It reconstructs the normalized
five-point outer Hurwitz algebra over Q, builds the radial consistency
rows through deficit seven over its irreducible quintic field, and asks
Singular for unit-ideal certificates on the two triangular charts.

The calculation also specializes the exact rows back to the two rational
and one cubic factors modulo 32003.  This locks the primitive-element
order (s=u7^-1), the endpoint-coordinate substitution, and all row
scalars before the characteristic-zero Gröbner calculations are trusted.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path
import pickle
import shutil
import subprocess
import time

import sympy as sp

from route_bd_ab_outer_lift import (
    WORKERS,
    lift_coefficients,
    modular_lex_basis,
    quotient_data,
    reconstruction_primes,
)
from route_bd_case_c_n3_generic_charts import (
    assert_reduced_shape,
    assert_variable_support,
    build_reduced_charts_from_imposed,
    imposed_equations as modular_imposed_equations,
)
from route_bd_case_c_n3_hurwitz_bridge import (
    NVAR,
    ParameterPolynomial,
    QuotientElement,
    canonical_modes,
    p_exponents,
    q_exponents,
    solve_stage,
    substitute_endpoint_coordinates,
)
from route_bd_case_c_radial_obstruction import SP as ModularPolynomial
from route_bd_fbar_obstruction import K, PRIME
from route_bd_universal_hamiltonian_endpoint_squares import substitute


KAPPA = sp.Rational(169, 48)
WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
DEFAULT_CACHE = Path("tmp/case_c_n3_generic_charts_Q.pkl")


def reconstruct_outer_algebra(
    workers: int,
) -> tuple[sp.Symbol, sp.Poly, list[sp.Expr], list[sp.Expr]]:
    """CRT/rationally reconstruct and certify the exact outer quotient."""
    primes = reconstruction_primes()
    modular_bases: dict[int, list[int]] = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(modular_lex_basis, prime): prime
            for prime in primes
        }
        for count, future in enumerate(as_completed(futures), 1):
            modular_bases[futures[future]] = future.result()
            if count % 8 == 0:
                print(f"outer modular bases: {count}/{len(primes)}", flush=True)
    coefficients = lift_coefficients(primes, modular_bases)
    return quotient_data(coefficients)


def polynomial_weights(polynomial: ParameterPolynomial) -> set[int]:
    return {
        sum(
            exponent * weight
            for exponent, weight in zip(monomial, WEIGHTS)
        )
        for monomial in polynomial.terms
    }


def exact_consistency_through_seven(
    u_expressions: list[sp.Expr],
    v_expressions: list[sp.Expr],
) -> list[ParameterPolynomial]:
    """Repeat the canonical case-c recursion through radial deficit seven."""
    u = [QuotientElement.coerce(expression) for expression in u_expressions]
    v = [QuotientElement.coerce(expression) for expression in v_expressions]
    modes = canonical_modes(u, v)
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    offsets = {1: 0, 0: 2, -1: 4, -2: 6}
    p_blocks = {
        2: {
            -1: ParameterPolynomial(1),
            **{
                index - 1: ParameterPolynomial(u[index])
                for index in range(1, 8)
            },
        }
    }
    q_blocks = {
        3: {
            -1: ParameterPolynomial(1),
            **{
                index - 1: ParameterPolynomial(v[index])
                for index in range(1, 11)
            },
        }
    }
    constraints: list[ParameterPolynomial] = []
    counts: list[int] = []
    for deficit in range(1, 8):
        p_degree = 2 - deficit
        q_degree = p_degree + 1
        assert p_exponents(p_degree)
        assert q_exponents(q_degree)
        p_block, q_block, new_constraints = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
        )
        if deficit in modes:
            offset = offsets[p_degree]
            for local_index, (p_mode, q_mode) in enumerate(modes[deficit]):
                parameter = parameters[offset + local_index]
                for exponent, coefficient in p_mode.items():
                    p_block[exponent] = (
                        p_block.get(exponent, ParameterPolynomial())
                        + parameter * coefficient
                    )
                    if not p_block[exponent]:
                        del p_block[exponent]
                for exponent, coefficient in q_mode.items():
                    q_block[exponent] = (
                        q_block.get(exponent, ParameterPolynomial())
                        + parameter * coefficient
                    )
                    if not q_block[exponent]:
                        del q_block[exponent]
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        constraints.extend(new_constraints)
        counts.append(len(new_constraints))
        print(
            f"exact radial deficit {deficit}: "
            f"{len(new_constraints)} cokernel rows",
            flush=True,
        )

    # This is the cokernel-row inventory before the square is imposed.
    assert counts == [0, 0, 0, 2, 2, 4, 5], counts
    return [
        substitute_endpoint_coordinates(constraint, parameters)
        for constraint in constraints
    ]


def impose_square(
    transformed: list[ParameterPolynomial],
) -> list[ParameterPolynomial]:
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    zero = QuotientElement.coerce(0)
    one = QuotientElement.coerce(1)
    imposed = [
        substitute(
            equation,
            parameters,
            {2: KAPPA * parameters[0] * parameters[0]},
            zero,
            one,
        )
        for equation in transformed
    ]
    counts = {
        weight: sum(
            bool(equation) and polynomial_weights(equation) == {weight}
            for equation in imposed
        )
        for weight in range(4, 8)
    }
    assert counts == {4: 0, 5: 1, 6: 3, 7: 5}, counts
    return imposed


def specialize_coefficient(
    coefficient: QuotientElement,
    primitive: K,
) -> K:
    """Evaluate an exact power-basis coefficient at a modular factor."""
    value = K()
    power = K(1)
    for rational in coefficient.coefficients:
        numerator = int(rational.p) % PRIME
        denominator = int(rational.q) % PRIME
        value += K(numerator) / denominator * power
        power *= primitive
    return value


def specialize_polynomial(
    polynomial: ParameterPolynomial,
    primitive: K,
) -> ModularPolynomial:
    return ModularPolynomial(
        terms={
            monomial: specialize_coefficient(coefficient, primitive)
            for monomial, coefficient in polynomial.terms.items()
            if specialize_coefficient(coefficient, primitive)
        }
    )


def verify_modular_specializations(
    exact_imposed: list[ParameterPolynomial],
) -> None:
    """Diagnose primitive/scalar/order mistakes against the known fiber."""
    for label, primitive in (
        ("r1", K(26839)),
        ("r2", K(16621)),
        ("cubic", K(0, 1)),
    ):
        exact_rows = [
            specialize_polynomial(row, primitive)
            for row in exact_imposed
        ]
        modular_rows = modular_imposed_equations(primitive)
        assert len(exact_rows) == len(modular_rows)
        for index, (exact_row, modular_row) in enumerate(
            zip(exact_rows, modular_rows)
        ):
            assert exact_row.terms == modular_row.terms, (
                label,
                index,
                exact_row.terms,
                modular_row.terms,
            )
    print("exact rows specialize coefficient-for-coefficient in original order")


def quotient_text(coefficient: QuotientElement) -> str:
    pieces: list[str] = []
    for exponent, rational in enumerate(coefficient.coefficients):
        if not rational:
            continue
        scalar = (
            str(int(rational.p))
            if rational.q == 1
            else f"({int(rational.p)}/{int(rational.q)})"
        )
        if exponent == 0:
            term = scalar
        elif exponent == 1:
            term = f"({scalar})*s"
        else:
            # Singular otherwise parses ``huge_integer*s^k`` as a number
            # raised to a number.  Parenthesizing the coefficient and the
            # parameter power keeps the exponent in the integer parser.
            term = f"({scalar})*(s^{exponent})"
        pieces.append(term)
    return "+".join(pieces).replace("+-", "-") if pieces else "0"


def minpoly_text(eliminant: sp.Poly) -> str:
    pieces: list[str] = []
    for exponent in range(eliminant.degree(), -1, -1):
        rational = sp.Rational(eliminant.nth(exponent))
        if not rational:
            continue
        scalar = (
            str(int(rational.p))
            if rational.q == 1
            else f"({int(rational.p)}/{int(rational.q)})"
        )
        if exponent == 0:
            term = scalar
        elif exponent == 1:
            term = f"({scalar})*s"
        else:
            term = f"({scalar})*(s^{exponent})"
        pieces.append(term)
    return "+".join(pieces).replace("+-", "-")


def polynomial_text(polynomial: ParameterPolynomial) -> str:
    variables = tuple(f"X{index}" for index in range(NVAR))
    pieces: list[str] = []
    for monomial in sorted(polynomial.terms, reverse=True):
        coefficient = polynomial.terms[monomial]
        coefficient_text = quotient_text(coefficient)
        factors = [
            variable if exponent == 1 else f"{variable}^{exponent}"
            for variable, exponent in zip(variables, monomial)
            if exponent
        ]
        if not factors:
            pieces.append(f"({coefficient_text})")
        elif coefficient_text == "1":
            pieces.append("*".join(factors))
        elif coefficient_text == "-1":
            pieces.append("-" + "*".join(factors))
        else:
            pieces.append(f"({coefficient_text})*" + "*".join(factors))
    return "+".join(pieces).replace("+-", "-") if pieces else "0"


def rational_quotient_ring(
    free_variables: tuple[int, ...],
) -> str:
    variables = ",".join(
        ("s", *(f"X{index}" for index in free_variables), "h")
    )
    return (
        'LIB "modstd.lib";\n'
        f"ring R=0,({variables}),dp;\n"
        "option(redSB);"
    )


def certify_charts(
    eliminant: sp.Poly,
    exact_imposed: list[ParameterPolynomial],
) -> None:
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    zero = QuotientElement.coerce(0)
    one = QuotientElement.coerce(1)
    charts = build_reduced_charts_from_imposed(
        exact_imposed,
        parameters,
        zero,
        one,
    )
    for chart in charts:
        assert_variable_support(chart)
        assert_reduced_shape(chart)
        weight_six = list(chart.rows_by_weight[6])
        weight_seven = list(chart.rows_by_weight[7])
        choices = (
            tuple(combinations(range(3), 2))
            if chart.name == "L_NE_0"
            else tuple((index,) for index in range(3))
        )

        def run_choice(choice: tuple[int, ...]) -> str:
            rows = weight_six + [
                weight_seven[index] for index in choice
            ]
            ideal = ",\n".join(polynomial_text(row) for row in rows)
            program = "\n".join(
                (
                    rational_quotient_ring(chart.free_variables),
                    f"ideal J=\n{minpoly_text(eliminant)},\n{ideal};",
                    # modStd's global nonhomogeneous result is only
                    # high-probability even with exactness=1.  Homogenizing
                    # makes its verified standard-basis guarantee exact.
                    "ideal Jh=homog(J,h);",
                    "ideal Hh=modStd(Jh,1);",
                    "int hpower=0;",
                    "poly hp=1;",
                    "for (int exponent=1; exponent<=256; exponent++) {",
                    "  hp=hp*h;",
                    "  if (reduce(hp,Hh)==0) { hpower=exponent; break; }",
                    "}",
                    f'print("Q5 {chart.name} MINIMAL {choice} HPOWER "'
                    '+string(hpower));',
                )
            )
            result = subprocess.run(
                ["Singular", "-q"],
                input=program,
                text=True,
                capture_output=True,
                check=True,
            )
            output = result.stdout + result.stderr
            assert "error occurred" not in output.lower(), output
            marker = f"Q5 {chart.name} MINIMAL {choice} HPOWER "
            line = next(
                (line for line in output.splitlines() if marker in line),
                None,
            )
            assert line is not None, output
            exponent = int(line.rsplit(" ", 1)[1])
            assert exponent > 0, output
            return output.strip()

        # The three independent minimal certificates are faster and
        # stronger than first computing the proper deficit-six ideal.
        # Each unit ideal is a subset of the full deficit-seven ideal.
        with ThreadPoolExecutor(max_workers=len(choices)) as executor:
            futures = {
                executor.submit(run_choice, choice): choice
                for choice in choices
            }
            for future in as_completed(futures):
                print(future.result(), flush=True)
        print(
            f"Q5 {chart.name} FULL DEFICIT-SEVEN UNIT EXACT "
            "(homogeneous h-power certificates)",
            flush=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument(
        "--skip-modular-crosscheck",
        action="store_true",
        help="skip only the inexpensive mod-32003 row comparison",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=DEFAULT_CACHE,
        help="cache exact outer data and imposed rows after each costly phase",
    )
    args = parser.parse_args()
    assert shutil.which("Singular")

    start = time.monotonic()
    cache: dict[str, object] = {}
    if args.cache.exists():
        with args.cache.open("rb") as stream:
            cache = pickle.load(stream)
    if "outer" in cache:
        s, eliminant, u, v = cache["outer"]
        print(
            f"loaded exact outer cache in {time.monotonic() - start:.1f}s",
            flush=True,
        )
    else:
        s, eliminant, u, v = reconstruct_outer_algebra(args.workers)
        cache["outer"] = (s, eliminant, u, v)
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        with args.cache.open("wb") as stream:
            pickle.dump(cache, stream)
        print(
            f"reconstructed exact outer algebra in "
            f"{time.monotonic() - start:.1f}s",
            flush=True,
        )
    assert eliminant.gens == (s,)
    print("exact outer eliminant:", eliminant.as_expr(), flush=True)
    QuotientElement.configure(eliminant)

    recurrence_start = time.monotonic()
    if "imposed" in cache:
        exact_imposed = cache["imposed"]
        print(
            f"loaded imposed-row cache in "
            f"{time.monotonic() - recurrence_start:.1f}s",
            flush=True,
        )
    else:
        transformed = exact_consistency_through_seven(u, v)
        exact_imposed = impose_square(transformed)
        cache["imposed"] = exact_imposed
        with args.cache.open("wb") as stream:
            pickle.dump(cache, stream)
        print(
            f"exact seven-stage recurrence in "
            f"{time.monotonic() - recurrence_start:.1f}s",
            flush=True,
        )
    if not args.skip_modular_crosscheck:
        crosscheck_start = time.monotonic()
        verify_modular_specializations(exact_imposed)
        print(
            f"modular row crosscheck in "
            f"{time.monotonic() - crosscheck_start:.1f}s",
            flush=True,
        )
    groebner_start = time.monotonic()
    certify_charts(eliminant, exact_imposed)
    print(
        f"exact chart Groebner certificates in "
        f"{time.monotonic() - groebner_start:.1f}s",
        flush=True,
    )
    print(f"total elapsed {time.monotonic() - start:.1f}s", flush=True)
    print("RESULT: EXACT Q QUINTIC OUTER ALGEBRA RECONSTRUCTED")
    print("RESULT: BOTH GENERIC CHARTS ARE UNIT IDEALS AT DEFICIT SEVEN")


if __name__ == "__main__":
    main()
