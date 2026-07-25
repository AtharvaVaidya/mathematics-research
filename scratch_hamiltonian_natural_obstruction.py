#!/usr/bin/env python3
"""Explore lower consistency equations in the canonical C-mode basis."""

from __future__ import annotations

import argparse
import subprocess

from route_bd_universal_radial_consistency import (
    FQ2,
    NVAR,
    ONE,
    PARAMETERS,
    SP,
    WPoly,
    ZERO,
    bracket,
    lower_support,
    outer_coefficients,
    rref_affine,
    wadd,
)
from route_bd_case_c_radial_obstruction import (
    PARAMETERS as K3_PARAMETERS,
    SP as K3SP,
    p_exponents as k3_p_exponents,
    q_exponents as k3_q_exponents,
    solve_stage as k3_solve_stage,
)
from route_bd_fbar_obstruction import (
    K,
    ONE as K_ONE,
    ZERO as K_ZERO,
    outer_coefficients as k3_outer_coefficients,
)


def c_pair(
    d: int,
    c_polynomial: dict[int, FQ2],
    u: list[FQ2],
    v: list[FQ2],
) -> tuple[WPoly, WPoly]:
    c = 5 - d
    assert c
    a: WPoly = {}
    b: WPoly = {}
    for exponent, coefficient in c_polynomial.items():
        for index, outer in enumerate(u):
            value = (
                FQ2(c * index + d - 3 - 2 * exponent)
                / c
                * coefficient
                * outer
            )
            if value:
                a[exponent + index] = (
                    a.get(exponent + index, SP()) + value
                )
        for index, outer in enumerate(v):
            value = (
                FQ2(c * index + d - 2 - 3 * exponent)
                / c
                * coefficient
                * outer
            )
            if value:
                b[exponent + index] = (
                    b.get(exponent + index, SP()) + value
                )
    return a, b


def high_d4_c(k: int, u: list[FQ2]) -> dict[int, FQ2]:
    d = 4
    c = 1
    p = 2 * k + 1
    top = k + 1
    coefficients = {top: ONE}
    for exponent in range(top - 1, 1, -1):
        output_exponent = p + exponent
        known = ZERO
        for c_exponent, c_coefficient in coefficients.items():
            u_index = output_exponent - c_exponent
            if 0 <= u_index <= p:
                known += (
                    FQ2(c * u_index + d - 3 - 2 * c_exponent)
                    * c_coefficient
                    * u[u_index]
                )
        pivot = (
            FQ2(c * p + d - 3 - 2 * exponent) * u[p]
        )
        assert pivot
        coefficients[exponent] = -known / pivot
    return coefficients


def canonical_modes(
    k: int,
    u: list[FQ2],
    v: list[FQ2],
) -> dict[int, list[tuple[WPoly, WPoly]]]:
    u_square: dict[int, FQ2] = {}
    for left, left_coefficient in enumerate(u):
        for right, right_coefficient in enumerate(u):
            u_square[left + right] = (
                u_square.get(left + right, ZERO)
                + left_coefficient * right_coefficient
            )
    high_d1 = {
        exponent - 1: coefficient
        for exponent, coefficient in u_square.items()
        if exponent >= 2 and coefficient
    }
    c_modes = {
        1: ({0: ONE}, high_d1),
        2: ({1: ONE}, {
            exponent: coefficient
            for exponent, coefficient in enumerate(v)
            if exponent >= 2 and coefficient
        }),
        3: ({1: ONE}, {
            exponent: coefficient
            for exponent, coefficient in enumerate(u)
            if exponent >= 2 and coefficient
        }),
        4: (high_d4_c(k, u),),
    }
    return {
        d: [c_pair(d, c_polynomial, u, v) for c_polynomial in modes]
        for d, modes in c_modes.items()
    }


def natural_consistency(
    k: int,
    max_deficit: int | None = None,
) -> list[SP]:
    u, v = outer_coefficients(k)
    modes = canonical_modes(k, u, v)
    p_blocks: dict[int, WPoly] = {
        2: {
            index - 1: SP(coefficient)
            for index, coefficient in enumerate(u)
        }
    }
    q_blocks: dict[int, WPoly] = {
        3: {
            index - 1: SP(coefficient)
            for index, coefficient in enumerate(v)
        }
    }
    p_bound = 2 * (k + 1)
    q_bound = 3 * (k + 1)
    parameter_offset = {1: 0, 2: 2, 3: 4, 4: 6}
    constraints: list[SP] = []

    final_deficit = 3 * (k + 2)
    if max_deficit is not None:
        final_deficit = min(final_deficit, max_deficit)
    for deficit in range(1, final_deficit + 1):
        p_degree = 2 - deficit
        q_degree = 3 - deficit
        output_degree = 4 - deficit
        p_support = lower_support(p_bound, p_degree, 2)
        q_support = lower_support(q_bound, q_degree, 3)
        source: WPoly = {}
        for left_degree, left in p_blocks.items():
            for right_degree, right in q_blocks.items():
                if left_degree + right_degree - 1 == output_degree:
                    source = wadd(
                        source,
                        bracket(left_degree, left, right_degree, right),
                    )
        columns: list[WPoly] = [
            bracket(
                p_degree,
                {exponent: SP(1)},
                3,
                q_blocks[3],
            )
            for exponent in p_support
        ]
        columns.extend(
            bracket(
                2,
                p_blocks[2],
                q_degree,
                {exponent: SP(1)},
            )
            for exponent in q_support
        )
        row_exponents = sorted(
            set(source).union(*(set(column) for column in columns))
        )
        matrix = [
            [
                column.get(exponent, SP()).terms.get(
                    (0,) * NVAR, ZERO
                )
                for column in columns
            ]
            for exponent in row_exponents
        ]
        source_vector = [
            source.get(exponent, SP()) for exponent in row_exponents
        ]
        kernel_count = len(modes.get(deficit, ()))
        solution, new_constraints, _rank = rref_affine(
            matrix,
            source_vector,
            (SP() for _ in range(kernel_count)),
        )
        if kernel_count:
            offset = parameter_offset[deficit]
            for local_index, (a_mode, b_mode) in enumerate(modes[deficit]):
                parameter = PARAMETERS[offset + local_index]
                for index, exponent in enumerate(p_support):
                    solution[index] += parameter * a_mode.get(
                        exponent, SP()
                    )
                split = len(p_support)
                for index, exponent in enumerate(q_support):
                    solution[split + index] += parameter * b_mode.get(
                        exponent, SP()
                    )
        split = len(p_support)
        p_blocks[p_degree] = {
            exponent: coefficient
            for exponent, coefficient in zip(p_support, solution[:split])
            if coefficient
        }
        q_blocks[q_degree] = {
            exponent: coefficient
            for exponent, coefficient in zip(
                q_support, solution[split:]
            )
            if coefficient
        }
        constraints.extend(new_constraints)
    return constraints


def k3_c_pair(
    d: int,
    c_polynomial: dict[int, K],
    u: list[K],
    v: list[K],
) -> tuple[dict[int, K3SP], dict[int, K3SP]]:
    c = 5 - d
    a: dict[int, K3SP] = {}
    b: dict[int, K3SP] = {}
    for exponent, coefficient in c_polynomial.items():
        for index, outer in enumerate(u):
            value = (
                K(c * index + d - 3 - 2 * exponent)
                / c
                * coefficient
                * outer
            )
            if value:
                a[exponent + index] = (
                    a.get(exponent + index, K3SP()) + value
                )
        for index, outer in enumerate(v):
            value = (
                K(c * index + d - 2 - 3 * exponent)
                / c
                * coefficient
                * outer
            )
            if value:
                b[exponent + index] = (
                    b.get(exponent + index, K3SP()) + value
                )
    return a, b


def k3_high_d4_c(u: list[K]) -> dict[int, K]:
    d = 4
    c = 1
    p = 7
    top = 4
    coefficients = {top: K_ONE}
    for exponent in range(top - 1, 1, -1):
        output_exponent = p + exponent
        known = K_ZERO
        for c_exponent, c_coefficient in coefficients.items():
            u_index = output_exponent - c_exponent
            if 0 <= u_index <= p:
                known += (
                    K(c * u_index + d - 3 - 2 * c_exponent)
                    * c_coefficient
                    * u[u_index]
                )
        pivot = K(c * p + d - 3 - 2 * exponent) * u[p]
        coefficients[exponent] = -known / pivot
    return coefficients


def k3_modes(
    u: list[K],
    v: list[K],
) -> dict[int, list[tuple[dict[int, K3SP], dict[int, K3SP]]]]:
    u_square: dict[int, K] = {}
    for left, left_coefficient in enumerate(u):
        for right, right_coefficient in enumerate(u):
            u_square[left + right] = (
                u_square.get(left + right, K_ZERO)
                + left_coefficient * right_coefficient
            )
    c_modes = {
        1: (
            {0: K_ONE},
            {
                exponent - 1: coefficient
                for exponent, coefficient in u_square.items()
                if exponent >= 2 and coefficient
            },
        ),
        2: (
            {1: K_ONE},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(v)
                if exponent >= 2 and coefficient
            },
        ),
        3: (
            {1: K_ONE},
            {
                exponent: coefficient
                for exponent, coefficient in enumerate(u)
                if exponent >= 2 and coefficient
            },
        ),
        4: (k3_high_d4_c(u),),
    }
    return {
        d: [
            k3_c_pair(d, c_polynomial, u, v)
            for c_polynomial in polynomials
        ]
        for d, polynomials in c_modes.items()
    }


def natural_consistency_k3(
    outer_parameter: K,
    max_deficit: int | None = None,
) -> list[K3SP]:
    u, v = k3_outer_coefficients(outer_parameter)
    modes = k3_modes(u, v)
    p_blocks = {
        2: {
            -1: K3SP(K_ONE),
            **{
                index - 1: K3SP(u[index])
                for index in range(1, 8)
            },
        }
    }
    q_blocks = {
        3: {
            -1: K3SP(K_ONE),
            **{
                index - 1: K3SP(v[index])
                for index in range(1, 11)
            },
        }
    }
    offsets = {1: 0, 0: 2, -1: 4, -2: 6}
    constraints: list[K3SP] = []
    final_deficit = 15 if max_deficit is None else min(15, max_deficit)
    for p_degree in range(1, 1 - final_deficit, -1):
        q_degree = p_degree + 1
        p_support = k3_p_exponents(p_degree)
        q_support = k3_q_exponents(q_degree)
        kernel_count = len(modes.get(2 - p_degree, ()))
        p_block, q_block, new_constraints, _profile = k3_solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
            p_support,
            q_degree,
            q_support,
            (K3SP() for _ in range(kernel_count)),
        )
        if kernel_count:
            offset = offsets[p_degree]
            for local_index, (a_mode, b_mode) in enumerate(
                modes[2 - p_degree]
            ):
                parameter = K3_PARAMETERS[offset + local_index]
                for exponent in p_support:
                    p_block[exponent] = (
                        p_block.get(exponent, K3SP())
                        + parameter * a_mode.get(exponent, K3SP())
                    )
                    if not p_block[exponent]:
                        p_block.pop(exponent, None)
                for exponent in q_support:
                    q_block[exponent] = (
                        q_block.get(exponent, K3SP())
                        + parameter * b_mode.get(exponent, K3SP())
                    )
                    if not q_block[exponent]:
                        q_block.pop(exponent, None)
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        constraints.extend(new_constraints)
    return constraints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, choices=(1, 2), default=1)
    parser.add_argument(
        "--k3-factor",
        choices=("r1", "r2", "cubic"),
    )
    parser.add_argument("--lex", action="store_true")
    args = parser.parse_args()
    if args.k3_factor:
        parameters = {
            "r1": K(26839),
            "r2": K(16621),
            "cubic": K(0, 1),
        }
        equations = natural_consistency_k3(
            parameters[args.k3_factor]
        )
        extension = args.k3_factor == "cubic"
        k_label = f"3-{args.k3_factor}"
    else:
        equations = natural_consistency(args.k)
        extension = args.k == 2
        k_label = str(args.k)
    prefix = [
        equation
        for equation in equations
        if next(iter(equation.weighted_degrees())) <= 8
    ]
    print(f"k={k_label}: {len(prefix)} equations of weights <=8")
    for index, equation in enumerate(prefix):
        weight = next(iter(equation.weighted_degrees()))
        print(
            f"E{index:02d} weight={weight}: "
            f"{equation.singular(allow_extension=extension) if args.k3_factor else equation.singular(extension=extension)}"
        )
    if args.lex:
        ring = (
            "ring R=(32003,t),(X1,X3,X5,X6,X0,X2,X4),lp;\n"
            "minpoly=t^3-11133*t^2-11294*t-6180;"
            if args.k3_factor and extension
            else
            "ring R=(32003,s),(X1,X3,X5,X6,X0,X2,X4),lp;\n"
            "minpoly=s^2+9432*s-2820;"
            if extension
            else "ring R=32003,(X1,X3,X5,X6,X0,X2,X4),lp;"
        )
        ideal = ",\n".join(
            (
                equation.singular(allow_extension=extension)
                if args.k3_factor
                else equation.singular(extension=extension)
            )
            for equation in prefix
        )
        program = f"""{ring}
option(redSB);
ideal I={ideal};
ideal G=std(I);
print("LEX SIZE "+string(size(G)));
for (int i=1;i<=size(G);i++) {{
  poly leadterm=lead(G[i]);
  if (size(leadterm)==1) {{ print(leadterm); }}
}}
"""
        result = subprocess.run(
            ["Singular", "-q"],
            input=program,
            text=True,
            capture_output=True,
            check=True,
        )
        print(result.stdout)


if __name__ == "__main__":
    main()
