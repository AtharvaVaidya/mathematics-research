#!/usr/bin/env python3
"""Exact reduced-chart audit for the two generic case-c n=3 branches.

After the deficit-four square and the triangular deficit-five equation,
the only charts not treated in ``route_bd_case_c_n3_hurwitz_bridge.py`` are

    I.  L != 0,
    II. L = 0, A != 0.

All equations are weighted homogeneous.  Over an algebraic closure, chart I
may therefore be normalized by L=1 and chart II by A=1.  The deficit-five
row then eliminates X6 on chart I and X5 on chart II.  This leaves four and
three variables, respectively.  The present script constructs those exact
reduced equations over each factor of the complete F_32003 five-point
Hurwitz fiber and asks Singular for a unit-ideal certificate.

The modular calculation is intended as a discovery and reduction audit.
Any characteristic-zero conclusion additionally uses the projectivity /
proper-specialization argument for the original weighted homogeneous fiber.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import shutil
import subprocess
from dataclasses import dataclass

from route_bd_case_c_n3_hurwitz_bridge import (
    NVAR,
    WEIGHTS,
    parameter_coefficient,
)
from route_bd_case_c_radial_obstruction import PARAMETERS
from route_bd_fbar_obstruction import K
from route_bd_universal_hamiltonian_endpoint_squares import (
    substitute,
    transformed_equations,
)
from scratch_hamiltonian_natural_obstruction import natural_consistency_k3


KAPPA = K(169) / 48
ZERO_MONOMIAL = (0,) * NVAR


@dataclass(frozen=True)
class ReducedChart:
    name: str
    free_variables: tuple[int, ...]
    rows_by_weight: dict[int, tuple[object, ...]]

    @property
    def rows(self) -> tuple[object, ...]:
        return tuple(
            row
            for weight in sorted(self.rows_by_weight)
            for row in self.rows_by_weight[weight]
        )


def scalar_coefficient(polynomial: object) -> object:
    assert set(polynomial.terms) == {ZERO_MONOMIAL}
    return polynomial.terms[ZERO_MONOMIAL]


def polynomial_weights(polynomial: object) -> set[int]:
    return {
        sum(
            exponent * weight
            for exponent, weight in zip(monomial, WEIGHTS)
        )
        for monomial in polynomial.terms
    }


def imposed_equations(outer_parameter: K) -> list[object]:
    equations = transformed_equations(
        # Deficit seven already decides both normalized generic charts.
        # Do not build the unused later coefficient recursion.
        natural_consistency_k3(outer_parameter, max_deficit=7),
        PARAMETERS,
        K,
        K(),
        K(1),
    )
    return [
        substitute(
            equation,
            PARAMETERS,
            {2: KAPPA * PARAMETERS[0] * PARAMETERS[0]},
            K(),
            K(1),
        )
        for equation in equations
    ]


def group_rows(
    weighted_equations: list[tuple[int, object]],
) -> dict[int, tuple[object, ...]]:
    grouped: dict[int, list[object]] = {}
    for inherited_weight, equation in weighted_equations:
        if not equation:
            continue
        # Chart normalization destroys weighted homogeneity, so retain the
        # weight of the source consistency row rather than recomputing it.
        grouped.setdefault(inherited_weight, []).append(equation)
    return {
        weight: tuple(rows)
        for weight, rows in grouped.items()
    }


def build_reduced_charts_from_imposed(
    imposed: list[object],
    parameters: tuple[object, ...],
    zero: object,
    one: object,
) -> tuple[ReducedChart, ReducedChart]:
    def constant(value: object) -> object:
        return type(parameters[0])(value)

    weighted_imposed = [
        (next(iter(polynomial_weights(equation))), equation)
        for equation in imposed
        if equation
    ]
    weight_five = [
        equation
        for equation in imposed
        if equation and polynomial_weights(equation) == {5}
    ]
    assert len(weight_five) == 1
    survivor = weight_five[0]

    linear_form = parameter_coefficient(survivor, 6, 1)
    l_x1 = linear_form.terms[(0, 1, 0, 0, 0, 0, 0)]
    l_y0 = linear_form.terms[(1, 0, 0, 0, 0, 0, 0)]
    assert l_x1 and l_y0

    # Chart I: normalize L=1, solve the resulting monic deficit-five row
    # for X6, and substitute it into every later row.
    x1_on_l_one = (
        constant(one) - parameters[0] * l_y0
    ) * (one / l_x1)
    l_one_rows = [
        (
            weight,
            substitute(
                equation,
                parameters,
                {1: x1_on_l_one},
                zero,
                one,
            ),
        )
        for weight, equation in weighted_imposed
    ]
    l_one_survivor = substitute(
        survivor,
        parameters,
        {1: x1_on_l_one},
        zero,
        one,
    )
    x6_coefficient = parameter_coefficient(l_one_survivor, 6, 1)
    assert scalar_coefficient(x6_coefficient) == one
    x6_value = -parameter_coefficient(l_one_survivor, 6, 0)
    chart_one_rows = [
        (
            weight,
            substitute(
                equation,
                parameters,
                {6: x6_value},
                zero,
                one,
            ),
        )
        for weight, equation in l_one_rows
    ]
    chart_one = ReducedChart(
        name="L_NE_0",
        free_variables=(0, 3, 4, 5),
        rows_by_weight=group_rows(chart_one_rows),
    )

    # Chart II: impose L=0.  Its deficit-five row is A*X5+remainder.
    # Normalize the weight-two form A=1, solve for X3, then solve F5 for X5.
    x1_on_l_zero = parameters[0] * (-l_y0 / l_x1)
    l_zero_rows = [
        (
            weight,
            substitute(
                equation,
                parameters,
                {1: x1_on_l_zero},
                zero,
                one,
            ),
        )
        for weight, equation in weighted_imposed
    ]
    l_zero_survivor = substitute(
        survivor,
        parameters,
        {1: x1_on_l_zero},
        zero,
        one,
    )
    coefficient_x5 = parameter_coefficient(l_zero_survivor, 5, 1)
    a_x3 = coefficient_x5.terms[(0, 0, 0, 1, 0, 0, 0)]
    a_y0_square = coefficient_x5.terms[(2, 0, 0, 0, 0, 0, 0)]
    assert a_x3 and a_y0_square
    x3_on_a_one = (
        constant(one)
        - parameters[0] * parameters[0] * a_y0_square
    ) * (one / a_x3)
    a_one_rows = [
        (
            weight,
            substitute(
                equation,
                parameters,
                {3: x3_on_a_one},
                zero,
                one,
            ),
        )
        for weight, equation in l_zero_rows
    ]
    a_one_survivor = substitute(
        l_zero_survivor,
        parameters,
        {3: x3_on_a_one},
        zero,
        one,
    )
    x5_coefficient = parameter_coefficient(a_one_survivor, 5, 1)
    assert scalar_coefficient(x5_coefficient) == one
    x5_value = -parameter_coefficient(a_one_survivor, 5, 0)
    chart_two_rows = [
        (
            weight,
            substitute(
                equation,
                parameters,
                {5: x5_value},
                zero,
                one,
            ),
        )
        for weight, equation in a_one_rows
    ]
    chart_two = ReducedChart(
        name="L_EQ_0_A_NE_0",
        free_variables=(0, 4, 6),
        rows_by_weight=group_rows(chart_two_rows),
    )
    return chart_one, chart_two


def build_reduced_charts(outer_parameter: K) -> tuple[ReducedChart, ReducedChart]:
    return build_reduced_charts_from_imposed(
        imposed_equations(outer_parameter),
        PARAMETERS,
        K(),
        K(1),
    )


def assert_variable_support(chart: ReducedChart) -> None:
    forbidden = set(range(NVAR)).difference(chart.free_variables)
    for row in chart.rows:
        assert all(
            monomial[index] == 0
            for monomial in row.terms
            for index in forbidden
        )


def assert_reduced_shape(chart: ReducedChart) -> None:
    """Lock the small chart presentations used by the unit certificates."""
    assert set(chart.rows_by_weight) == {6, 7}
    assert tuple(
        len(row.terms) for row in chart.rows_by_weight[6]
    ) == (
        (41, 41, 15)
        if chart.name == "L_NE_0"
        else (15, 15, 12)
    )
    assert tuple(
        len(row.terms) for row in chart.rows_by_weight[7]
    ) == (
        (60, 60, 60, 56, 15)
        if chart.name == "L_NE_0"
        else (19, 19, 19, 19, 12)
    )


def unit_ideal_program(
    label: str,
    chart: ReducedChart,
    ring: str,
    serialize: object,
) -> str:
    weight_six = list(chart.rows_by_weight[6])
    weight_seven = list(chart.rows_by_weight[7])

    def ideal_text(rows: list[object]) -> str:
        return ",\n".join(serialize(row) for row in rows)

    minimal_choices = (
        tuple(combinations(range(3), 2))
        if chart.name == "L_NE_0"
        else tuple((index,) for index in range(3))
    )
    minimal_declarations: list[str] = []
    minimal_checks: list[str] = []
    for index, choice in enumerate(minimal_choices):
        rows = weight_six + [
            weight_seven[row_index] for row_index in choice
        ]
        minimal_declarations.append(
            f"ideal J_{index}=\n{ideal_text(rows)};\n"
            f"ideal H_{index}=std(J_{index});"
        )
        minimal_checks.append(
            f"int minimal_unit_{index}=0;\n"
            f"if (size(H_{index})==1 && H_{index}[1]!=0 && "
            f"leadexp(H_{index}[1])==0) {{ minimal_unit_{index}=1; }}\n"
            f'print("{label} {chart.name} MINIMAL {choice} UNIT "'
            f"+string(minimal_unit_{index}));"
        )
    return "\n".join(
        (
            ring,
            f"ideal I_6=\n{ideal_text(weight_six)};",
            "ideal G_6=std(I_6);",
            f"ideal I_7=\n{ideal_text(weight_six + weight_seven)};",
            "ideal G_7=std(I_7);",
            "int unit_6=0;",
            "if (size(G_6)==1 && G_6[1]!=0 && "
            "leadexp(G_6[1])==0) { unit_6=1; }",
            "int unit_7=0;",
            "if (size(G_7)==1 && G_7[1]!=0 && "
            "leadexp(G_7[1])==0) { unit_7=1; }",
            f'print("{label} {chart.name} THROUGH 6 UNIT "+string(unit_6));',
            f'print("{label} {chart.name} THROUGH 7 UNIT "+string(unit_7));',
            *minimal_declarations,
            *minimal_checks,
            f"if (unit_6!=0) {{ print(\"{label} {chart.name} FAILED_EARLY\"); }}",
            f"if (unit_7==1) {{ print(\"{label} {chart.name} CERTIFIED\"); }}",
        )
    )


def singular_program(
    label: str,
    chart: ReducedChart,
    allow_extension: bool,
) -> str:
    variables = ",".join(f"X{index}" for index in chart.free_variables)
    ring = (
        f"ring R=(32003,t),({variables}),dp;\n"
        "minpoly=t^3-11133*t^2-11294*t-6180;"
        if allow_extension
        else f"ring R=32003,({variables}),dp;"
    )
    return unit_ideal_program(
        label,
        chart,
        ring,
        lambda row: row.singular(allow_extension=allow_extension),
    )


def assert_chart_output(label: str, chart: ReducedChart, output: str) -> None:
    assert "error occurred" not in output.lower()
    assert f"{label} {chart.name} THROUGH 6 UNIT 0" in output
    assert f"{label} {chart.name} THROUGH 7 UNIT 1" in output
    assert f"{label} {chart.name} CERTIFIED" in output
    assert f"{label} {chart.name} FAILED_EARLY" not in output
    minimal_choices = (
        tuple(combinations(range(3), 2))
        if chart.name == "L_NE_0"
        else tuple((index,) for index in range(3))
    )
    assert all(
        f"{label} {chart.name} MINIMAL {choice} UNIT 1" in output
        for choice in minimal_choices
    )


def audit_factor(
    label: str,
    outer_parameter: K,
    allow_extension: bool,
) -> None:
    for chart in build_reduced_charts(outer_parameter):
        assert_variable_support(chart)
        assert_reduced_shape(chart)
        program = singular_program(label, chart, allow_extension)
        result = subprocess.run(
            ["Singular", "-q"],
            input=program,
            text=True,
            capture_output=True,
            check=True,
        )
        output = result.stdout + result.stderr
        print(output.strip())
        assert_chart_output(label, chart, output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--factor",
        choices=("all", "r1", "r2", "cubic"),
        default="all",
    )
    args = parser.parse_args()
    assert shutil.which("Singular")
    factors = {
        "r1": (K(26839), False),
        "r2": (K(16621), False),
        "cubic": (K(0, 1), True),
    }
    selected = factors if args.factor == "all" else {
        args.factor: factors[args.factor]
    }
    for label, (outer_parameter, allow_extension) in selected.items():
        audit_factor(label, outer_parameter, allow_extension)
    print("RESULT: BOTH GENERIC CHARTS SURVIVE DEFICIT SIX")
    print("RESULT: BOTH GENERIC CHARTS ARE EMPTY AT DEFICIT SEVEN")
    print("RESULT: ALL FIVE OUTER HURWITZ POINTS ARE CERTIFIED MOD 32003")


if __name__ == "__main__":
    main()
