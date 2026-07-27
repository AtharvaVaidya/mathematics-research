#!/usr/bin/env python3
"""Exact-Q audit of the two special case-c n=3 charts.

The generic-chart calculation treats ``L != 0`` and ``L = 0, A != 0``.
This companion reconstructs the same irreducible quintic outer field and
checks the two boundary charts directly in characteristic zero:

    L = A = 0, B != 0,
    L = A = B = 0.

The first is killed by the exact resultant of two quadratics.  On the
second, an exact 3-by-3 determinant forces X4=X5=0 and the five surviving
deficit-eight rows are nonzero multiples of X6^2.  Every scalar used as a
pivot is also specialized to the two rational factors and the cubic
factor modulo 32003.  Thus the script detects both a zero in the quintic
field and a hidden nonunit at the chosen good prime.

The historical ``scratch_`` filename is retained for provenance.  The
checks performed here are part of the audited certificate bridge in
``current_context/CASE_C_FULL_CERTIFICATE_BRIDGE.md``; runtime caches are
accelerators only and must be removed for a publication replay.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path
import pickle

import sympy as sp

from route_bd_ab_outer_lift import (
    WORKERS,
    lift_coefficients,
    modular_lex_basis,
    quotient_data,
    reconstruction_primes,
)
from route_bd_case_c_n3_hurwitz_bridge import (
    NVAR,
    ParameterPolynomial,
    QuotientElement,
    canonical_modes,
    parameter_coefficient,
    p_exponents,
    q_exponents,
    quadratic_resultant,
    small_determinant,
    solve_stage,
    substitute_endpoint_coordinates,
    univariate_coefficients,
)
from route_bd_case_c_radial_obstruction import (
    PARAMETERS as MODULAR_PARAMETERS,
    SP as ModularPolynomial,
)
from route_bd_fbar_obstruction import K, PRIME
from route_bd_universal_hamiltonian_endpoint_squares import (
    substitute,
    transformed_equations,
)
from scratch_hamiltonian_natural_obstruction import natural_consistency_k3


WEIGHTS = (1, 1, 2, 2, 3, 3, 4)
KAPPA = sp.Rational(169, 48)
ZERO_MONOMIAL = (0,) * NVAR
MODULAR_FACTORS = (
    ("r1", K(26839)),
    ("r2", K(16621)),
    ("cubic", K(0, 1)),
)
OUTER_CACHE = Path("tmp/case_c_n3_generic_charts_Q.pkl")
SPECIAL_CACHE = Path("tmp/case_c_n3_special_charts_Q.pkl")
RECURRENCE_CACHE = Path("tmp/case_c_n3_special_recurrence_Q.pkl")


def save_pickle(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        pickle.dump(value, stream, protocol=pickle.HIGHEST_PROTOCOL)
    temporary.replace(path)


def reconstruct_outer_algebra(
    workers: int,
) -> tuple[sp.Symbol, sp.Poly, list[sp.Expr], list[sp.Expr]]:
    """Reconstruct and independently certify the exact outer quotient."""
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


def exact_consistency_through_eight(
    u_expressions: list[sp.Expr],
    v_expressions: list[sp.Expr],
) -> list[ParameterPolynomial]:
    """Repeat the canonical seven-mode recurrence through deficit eight."""
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
    if RECURRENCE_CACHE.exists():
        with RECURRENCE_CACHE.open("rb") as stream:
            cached = pickle.load(stream)
        p_blocks = cached["p_blocks"]
        q_blocks = cached["q_blocks"]
        constraints = cached["constraints"]
        stage_counts = cached["stage_counts"]
        print(
            f"resuming exact recurrence after deficit {len(stage_counts)}",
            flush=True,
        )
    else:
        constraints: list[ParameterPolynomial] = []
        stage_counts: list[int] = []
    for deficit in range(len(stage_counts) + 1, 9):
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
        stage_counts.append(len(new_constraints))
        print(
            f"exact recurrence deficit {deficit}: "
            f"{len(new_constraints)} cokernel rows",
            flush=True,
        )
        save_pickle(
            RECURRENCE_CACHE,
            {
                "p_blocks": p_blocks,
                "q_blocks": q_blocks,
                "constraints": constraints,
                "stage_counts": stage_counts,
            },
        )
    assert stage_counts == [0, 0, 0, 2, 2, 4, 5, 6], stage_counts
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
    square_root = parameters[2] - KAPPA * parameters[0] * parameters[0]
    square = square_root * square_root
    weight_four = [
        equation
        for equation in transformed
        if equation and polynomial_weights(equation) == {4}
    ]
    assert len(weight_four) == 2
    square_pivot = (0, 0, 2, 0, 0, 0, 0)
    for index, equation in enumerate(weight_four):
        assert set(equation.terms) == set(square.terms)
        scalar = equation.terms[square_pivot]
        assert_global_unit(f"exact deficit-four square scalar {index}", scalar)
        assert all(
            equation.terms[monomial] == scalar * coefficient
            for monomial, coefficient in square.terms.items()
        )

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
    counts = Counter(
        next(iter(polynomial_weights(equation)))
        for equation in imposed
        if equation
    )
    assert counts == {5: 1, 6: 3, 7: 5, 8: 6}, counts
    return imposed


def specialize_coefficient(
    coefficient: QuotientElement,
    primitive: K,
) -> K:
    """Evaluate a reduced exact coefficient on one modular outer factor."""
    value = K()
    power = K(1)
    for rational in coefficient.coefficients:
        # Inverting the denominator here deliberately fails on a nonunit.
        value += (
            K(int(rational.p) % PRIME)
            / (int(rational.q) % PRIME)
            * power
        )
        power *= primitive
    return value


def specialize_univariate_rational(
    polynomial: sp.Poly,
    primitive: K,
) -> K:
    """Reduce a rational univariate polynomial and evaluate it in ``K``."""
    value = K()
    for coefficient in polynomial.all_coeffs():
        rational = sp.Rational(coefficient)
        value = (
            value * primitive
            + K(int(rational.p) % PRIME) / (int(rational.q) % PRIME)
        )
    return value


def verify_reconstructed_outer_reduction(eliminant: sp.Poly) -> None:
    """Tie the reconstructed exact quotient to all three modular factors."""
    derivative = eliminant.diff()
    for factor_label, primitive in MODULAR_FACTORS:
        assert specialize_univariate_rational(eliminant, primitive) == K(), (
            factor_label,
            "the reconstructed outer eliminant does not vanish",
        )
        assert specialize_univariate_rational(derivative, primitive) != K(), (
            factor_label,
            "the reconstructed outer eliminant is not squarefree",
        )
    print(
        "exact outer eliminant reduces to the two rational and cubic factors"
    )


def specialize_polynomial(
    polynomial: ParameterPolynomial,
    primitive: K,
) -> ModularPolynomial:
    terms = {}
    for monomial, coefficient in polynomial.terms.items():
        specialized = specialize_coefficient(coefficient, primitive)
        if specialized:
            terms[monomial] = specialized
    return ModularPolynomial(terms=terms)


def assert_global_unit(label: str, value: QuotientElement) -> None:
    """Check a field unit and its unit reductions on all five points."""
    assert value, f"{label}: zero in the exact quintic field"
    for factor_label, primitive in MODULAR_FACTORS:
        assert specialize_coefficient(value, primitive), (
            label,
            factor_label,
            "nonunit modulo 32003",
        )
    print(f"UNIT {label}")


def scalar_coefficient(polynomial: ParameterPolynomial) -> QuotientElement:
    assert set(polynomial.terms) == {ZERO_MONOMIAL}
    return polynomial.terms[ZERO_MONOMIAL]


def verify_row_specializations(
    exact_imposed: list[ParameterPolynomial],
) -> None:
    """Lock row order, primitive element, and every coefficient through d=8."""
    for label, primitive in MODULAR_FACTORS:
        modular_transformed = transformed_equations(
            natural_consistency_k3(
                primitive,
                max_deficit=8,
            ),
            MODULAR_PARAMETERS,
            K,
            K(),
            K(1),
        )
        modular_imposed = [
            substitute(
                equation,
                MODULAR_PARAMETERS,
                {
                    2: K(169)
                    / 48
                    * MODULAR_PARAMETERS[0]
                    * MODULAR_PARAMETERS[0],
                },
                K(),
                K(1),
            )
            for equation in modular_transformed
        ]
        assert len(exact_imposed) == len(modular_imposed)
        for index, (exact_row, modular_row) in enumerate(
            zip(exact_imposed, modular_imposed)
        ):
            specialized = specialize_polynomial(exact_row, primitive)
            assert specialized.terms == modular_row.terms, (label, index)
    print("exact rows through deficit eight specialize coefficient-for-coefficient")


def verify_special_charts(exact_imposed: list[ParameterPolynomial]) -> None:
    parameters = tuple(
        ParameterPolynomial.variable(index) for index in range(NVAR)
    )
    zero = QuotientElement.coerce(0)
    one = QuotientElement.coerce(1)
    zero_parameter = ParameterPolynomial()
    one_parameter = ParameterPolynomial(1)

    weight_five = [
        equation
        for equation in exact_imposed
        if equation and polynomial_weights(equation) == {5}
    ]
    weight_six = [
        equation
        for equation in exact_imposed
        if equation and polynomial_weights(equation) == {6}
    ]
    assert len(weight_five) == 1
    assert len(weight_six) == 3
    survivor = weight_five[0]

    # On L=0, solve its nonzero X1 coefficient and write
    # F5=A*X5+B*X4+C.
    linear_form = parameter_coefficient(survivor, 6, 1)
    l_x1 = linear_form.terms[(0, 1, 0, 0, 0, 0, 0)]
    l_y0 = linear_form.terms[(1, 0, 0, 0, 0, 0, 0)]
    assert_global_unit("coefficient(L,X1)", l_x1)
    assert_global_unit("coefficient(L,Y0)", l_y0)
    x1_on_l_zero = parameters[0] * (-l_y0 / l_x1)
    exceptional = substitute(
        survivor,
        parameters,
        {1: x1_on_l_zero},
        zero,
        one,
    )
    exceptional_weight_six = [
        substitute(
            equation,
            parameters,
            {1: x1_on_l_zero},
            zero,
            one,
        )
        for equation in weight_six
    ]
    coefficient_x5 = parameter_coefficient(exceptional, 5, 1)
    coefficient_x4 = parameter_coefficient(exceptional, 4, 1)
    a_x3 = coefficient_x5.terms[(0, 0, 0, 1, 0, 0, 0)]
    a_y0_square = coefficient_x5.terms[(2, 0, 0, 0, 0, 0, 0)]
    b_x3 = coefficient_x4.terms[(0, 0, 0, 1, 0, 0, 0)]
    b_y0_square = coefficient_x4.terms[(2, 0, 0, 0, 0, 0, 0)]
    assert_global_unit("coefficient(A,X3)", a_x3)
    coefficient_determinant = a_x3 * b_y0_square - b_x3 * a_y0_square
    assert_global_unit("determinant((A,B)/(X3,Y0^2))", coefficient_determinant)

    # Chart L=A=0,B!=0.  Solve A=0 for X3 and F5=0 for X4.
    x3_on_a_zero = (
        parameters[0]
        * parameters[0]
        * (-a_y0_square / a_x3)
    )
    chart_three_replacements = {
        1: x1_on_l_zero,
        3: x3_on_a_zero,
    }
    chart_three_survivor = substitute(
        survivor,
        parameters,
        chart_three_replacements,
        zero,
        one,
    )
    assert not parameter_coefficient(chart_three_survivor, 5, 1)
    chart_three_x4 = parameter_coefficient(
        chart_three_survivor,
        4,
        1,
    )
    assert set(chart_three_x4.terms) == {
        (2, 0, 0, 0, 0, 0, 0)
    }
    b_on_a_zero = chart_three_x4.terms[
        (2, 0, 0, 0, 0, 0, 0)
    ]
    assert_global_unit("B/Y0^2 on A=0", b_on_a_zero)
    chart_three_remainder = parameter_coefficient(
        chart_three_survivor,
        4,
        0,
    )
    chart_three_rows = []
    for equation in weight_six:
        restricted = substitute(
            equation,
            parameters,
            chart_three_replacements,
            zero,
            one,
        )
        constant = parameter_coefficient(restricted, 4, 0)
        linear = parameter_coefficient(restricted, 4, 1)
        quadratic = parameter_coefficient(restricted, 4, 2)
        chart_three_rows.append(
            chart_three_x4 * chart_three_x4 * constant
            - chart_three_x4 * linear * chart_three_remainder
            + quadratic * chart_three_remainder * chart_three_remainder
        )

    # B!=0 is Y0!=0 here, so weighted scaling permits Y0=1.
    normalized_chart_three = [
        substitute(
            equation,
            parameters,
            {0: one_parameter},
            zero,
            one,
        )
        for equation in chart_three_rows
    ]
    x6_coefficients = [
        parameter_coefficient(equation, 6, 1)
        for equation in normalized_chart_three
    ]
    linear_indices = [
        index for index, coefficient in enumerate(x6_coefficients)
        if coefficient
    ]
    independent_indices = [
        index for index, coefficient in enumerate(x6_coefficients)
        if not coefficient
    ]
    assert len(linear_indices) == 2
    assert len(independent_indices) == 1
    x6_scalars = []
    x6_free_parts = []
    for local_index, index in enumerate(linear_indices):
        scalar = scalar_coefficient(x6_coefficients[index])
        assert_global_unit(f"chart3 X6 pivot {local_index}", scalar)
        x6_scalars.append(scalar)
        x6_free_parts.append(
            parameter_coefficient(normalized_chart_three[index], 6, 0)
        )
    x6_compatibility = (
        x6_free_parts[1] * x6_scalars[0]
        - x6_free_parts[0] * x6_scalars[1]
    )
    independent_equation = normalized_chart_three[
        independent_indices[0]
    ]
    resultant = quadratic_resultant(
        univariate_coefficients(independent_equation, 5),
        univariate_coefficients(x6_compatibility, 5),
        zero,
    )
    assert_global_unit("chart3 quadratic resultant", resultant)
    print("EMPTY L=A=0,B!=0 over the exact quintic field")

    # Chart L=A=B=0 is Y0=X1=X3=0.  The deficit-six rows span
    # X4^2,X4*X5,X5^2.
    deepest_rows = [
        substitute(
            equation,
            parameters,
            {
                0: zero_parameter,
                1: zero_parameter,
                2: zero_parameter,
                3: zero_parameter,
            },
            zero,
            one,
        )
        for equation in weight_six
    ]
    deepest_monomials = (
        (0, 0, 0, 0, 2, 0, 0),
        (0, 0, 0, 0, 1, 1, 0),
        (0, 0, 0, 0, 0, 2, 0),
    )
    assert all(
        set(equation.terms) == set(deepest_monomials)
        for equation in deepest_rows
    )
    deepest_matrix = [
        [equation.terms[monomial] for monomial in deepest_monomials]
        for equation in deepest_rows
    ]
    deepest_determinant = small_determinant(deepest_matrix, zero)
    assert_global_unit("chart4 quadratic determinant", deepest_determinant)

    deepest_all_rows = [
        substitute(
            equation,
            parameters,
            {
                0: zero_parameter,
                1: zero_parameter,
                2: zero_parameter,
                3: zero_parameter,
                4: zero_parameter,
                5: zero_parameter,
            },
            zero,
            one,
        )
        for equation in exact_imposed
    ]
    assert not [
        equation
        for equation in deepest_all_rows
        if equation and polynomial_weights(equation) == {7}
    ]
    deepest_weight_eight = [
        equation
        for equation in deepest_all_rows
        if equation and polynomial_weights(equation) == {8}
    ]
    assert len(deepest_weight_eight) == 5
    for index, equation in enumerate(deepest_weight_eight):
        assert set(equation.terms) == {
            (0, 0, 0, 0, 0, 0, 2)
        }
        assert_global_unit(
            f"chart4 coefficient {index} of X6^2",
            equation.terms[(0, 0, 0, 0, 0, 0, 2)],
        )
    print("ONLY THE AFFINE CONE ORIGIN SURVIVES L=A=B=0")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=WORKERS)
    args = parser.parse_args()
    if OUTER_CACHE.exists():
        with OUTER_CACHE.open("rb") as stream:
            cached_outer = pickle.load(stream)
        s, eliminant, u, v = cached_outer["outer"]
        print("loaded exact outer algebra from cache", flush=True)
    else:
        s, eliminant, u, v = reconstruct_outer_algebra(args.workers)
        save_pickle(OUTER_CACHE, {"outer": (s, eliminant, u, v)})
    assert eliminant.gens == (s,)
    assert eliminant.is_irreducible
    assert sp.gcd(eliminant, eliminant.diff()) == 1
    print("exact outer eliminant:", eliminant.as_expr())
    verify_reconstructed_outer_reduction(eliminant)
    QuotientElement.configure(eliminant)
    assert_global_unit("outer coefficient u7", QuotientElement.coerce(u[7]))
    assert_global_unit("outer coefficient v10", QuotientElement.coerce(v[10]))
    if SPECIAL_CACHE.exists():
        with SPECIAL_CACHE.open("rb") as stream:
            exact_imposed = pickle.load(stream)["imposed"]
        print("loaded exact deficit-eight rows from cache", flush=True)
    else:
        transformed = exact_consistency_through_eight(u, v)
        exact_imposed = impose_square(transformed)
        save_pickle(SPECIAL_CACHE, {"imposed": exact_imposed})
    verify_row_specializations(exact_imposed)
    verify_special_charts(exact_imposed)
    print("RESULT: BOTH SPECIAL CHARTS ARE CERTIFIED OVER THE EXACT Q QUINTIC")
    print("RESULT: EVERY TRIANGULAR PIVOT IS A UNIT MODULO 32003")


if __name__ == "__main__":
    main()
