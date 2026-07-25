#!/usr/bin/env python3
"""Independent exact-Q publication gate for the two generic case-c charts.

This deliberately avoids inferring a characteristic-zero chart result from
the three factors modulo 32003.  It reconstructs the normalized outer
number field K=Q[s]/(f), continues the radial recurrence through deficit
seven over K, and asks Singular for exact unit-ideal certificates in the two
normalized generic charts.

Every coefficient divided by in the chart construction is checked to be a
unit by gcd with the irreducible quintic (equivalently, by a nonzero norm).
"""

from __future__ import annotations

import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

import sympy as sp

from route_bd_ab_outer_lift import (
    WORKERS,
    lift_coefficients,
    modular_lex_basis,
    quotient_data,
    reconstruction_primes,
)
from route_bd_case_c_n3_generic_charts import (
    assert_chart_output,
    assert_reduced_shape,
    assert_variable_support,
    build_reduced_charts_from_imposed,
    unit_ideal_program,
)
from route_bd_case_c_n3_hurwitz_bridge import (
    KAPPA,
    NVAR,
    WEIGHTS,
    ParameterPolynomial,
    QuotientElement,
    canonical_modes,
    p_exponents,
    q_exponents,
    solve_stage,
    substitute_endpoint_coordinates,
)
from route_bd_universal_hamiltonian_endpoint_squares import substitute


def reconstruct_outer() -> tuple[
    sp.Symbol,
    sp.Poly,
    list[sp.Expr],
    list[sp.Expr],
]:
    primes = reconstruction_primes()
    modular_bases: dict[int, list[int]] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(modular_lex_basis, prime): prime
            for prime in primes
        }
        for future in as_completed(futures):
            modular_bases[futures[future]] = future.result()
    coefficients = lift_coefficients(primes, modular_bases)
    return quotient_data(coefficients)


def exact_constraints(
    u_expressions: list[sp.Expr],
    v_expressions: list[sp.Expr],
    max_deficit: int,
) -> list[ParameterPolynomial]:
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
    stage_counts: list[int] = []
    for p_degree in range(1, 1 - max_deficit, -1):
        q_degree = p_degree + 1
        p_block, q_block, new_constraints = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
        )
        deficit = 2 - p_degree
        offset = offsets.get(p_degree)
        if deficit in modes:
            assert offset is not None
            for local_index, (p_mode, q_mode) in enumerate(modes[deficit]):
                parameter = parameters[offset + local_index]
                for exponent, coefficient in p_mode.items():
                    p_block[exponent] = (
                        p_block.get(exponent, ParameterPolynomial())
                        + parameter * coefficient
                    )
                for exponent, coefficient in q_mode.items():
                    q_block[exponent] = (
                        q_block.get(exponent, ParameterPolynomial())
                        + parameter * coefficient
                    )
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        constraints.extend(new_constraints)
        stage_counts.append(len(new_constraints))
    assert stage_counts[:4] == [0, 0, 0, 2]
    return [
        substitute_endpoint_coordinates(constraint, parameters)
        for constraint in constraints
    ]


def polynomial_weight(polynomial: ParameterPolynomial) -> int:
    weights = {
        sum(exponent * weight for exponent, weight in zip(monomial, WEIGHTS))
        for monomial in polynomial.terms
    }
    assert len(weights) == 1
    return next(iter(weights))


def coefficient(
    polynomial: ParameterPolynomial,
    variable: int,
    exponent: int,
) -> ParameterPolynomial:
    return ParameterPolynomial(
        terms={
            tuple(
                0 if index == variable else value
                for index, value in enumerate(monomial)
            ): value
            for monomial, value in polynomial.terms.items()
            if monomial[variable] == exponent
        }
    )


def scalar(polynomial: ParameterPolynomial) -> QuotientElement:
    assert set(polynomial.terms) == {(0,) * NVAR}
    return polynomial.terms[(0,) * NVAR]


def assert_unit(
    label: str,
    value: QuotientElement,
    eliminant: sp.Poly,
) -> None:
    expression = sp.Poly(
        value.expression(),
        eliminant.gens[0],
        domain=sp.QQ,
    )
    divisor = sp.gcd(expression, eliminant)
    assert divisor.degree() == 0, (label, divisor)
    norm = sp.resultant(eliminant.as_expr(), expression.as_expr(), eliminant.gens[0])
    assert norm != 0
    print(f"{label} NORM_NONZERO")


def audit_chart_divisors(
    imposed: list[ParameterPolynomial],
    parameters: tuple[ParameterPolynomial, ...],
    eliminant: sp.Poly,
) -> None:
    survivor = next(
        equation for equation in imposed
        if equation and polynomial_weight(equation) == 5
    )
    linear_form = coefficient(survivor, 6, 1)
    l_x1 = scalar(coefficient(linear_form, 1, 1))
    l_y0 = scalar(coefficient(linear_form, 0, 1))
    assert_unit("L_X1", l_x1, eliminant)

    x1_on_l_zero = parameters[0] * (-l_y0 / l_x1)
    l_zero_survivor = substitute(
        survivor,
        parameters,
        {1: x1_on_l_zero},
        ParameterPolynomial(),
        ParameterPolynomial(1),
    )
    a_form = coefficient(l_zero_survivor, 5, 1)
    a_x3 = scalar(coefficient(a_form, 3, 1))
    assert_unit("A_X3", a_x3, eliminant)


def serialize(polynomial: ParameterPolynomial) -> str:
    pieces: list[str] = []
    for monomial, coefficient_value in polynomial.terms.items():
        coefficient_text = str(sp.factor(coefficient_value.expression())).replace(
            "**", "^"
        )
        factors = [
            f"X{index}^{exponent}" if exponent != 1 else f"X{index}"
            for index, exponent in enumerate(monomial)
            if exponent
        ]
        monomial_text = "*".join(factors)
        pieces.append(
            f"({coefficient_text})"
            + (f"*{monomial_text}" if monomial_text else "")
        )
    return "+".join(pieces) if pieces else "0"


def main() -> None:
    assert shutil.which("Singular")
    s, eliminant, u, v = reconstruct_outer()
    assert eliminant.is_irreducible
    assert sp.gcd(eliminant, eliminant.diff()) == 1
    QuotientElement.configure(eliminant)

    assert_unit("U7", QuotientElement.coerce(u[7]), eliminant)
    assert_unit("V10", QuotientElement.coerce(v[10]), eliminant)

    transformed = exact_constraints(u, v, max_deficit=7)
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    imposed = [
        substitute(
            equation,
            parameters,
            {2: KAPPA * parameters[0] * parameters[0]},
            ParameterPolynomial(),
            ParameterPolynomial(1),
        )
        for equation in transformed
    ]
    audit_chart_divisors(imposed, parameters, eliminant)
    charts = build_reduced_charts_from_imposed(
        imposed,
        parameters,
        ParameterPolynomial(),
        ParameterPolynomial(1),
    )
    minpoly = str(eliminant.as_expr()).replace("**", "^")
    for chart in charts:
        assert_variable_support(chart)
        assert_reduced_shape(chart)
        variables = ",".join(f"X{index}" for index in chart.free_variables)
        ring = (
            f"ring R=(0,{s}),({variables}),dp;\n"
            f"minpoly={minpoly};"
        )
        program = unit_ideal_program(
            "EXACT_Q",
            chart,
            ring,
            serialize,
        )
        completed = subprocess.run(
            ["Singular", "-q"],
            input=program,
            text=True,
            capture_output=True,
            check=True,
        )
        output = completed.stdout + completed.stderr
        print(output.strip())
        assert_chart_output("EXACT_Q", chart, output)

    primitive = eliminant.clear_denoms()[1].primitive()[1]
    print("OUTER_QUINTIC", primitive.as_expr())
    print("OUTER_ALGEBRA IRREDUCIBLE_REDUCED_FIELD_DEGREE_5")
    print("RESULT: BOTH GENERIC CASE-C CHARTS EMPTY OVER EXACT Q OUTER FIELD")


if __name__ == "__main__":
    main()
