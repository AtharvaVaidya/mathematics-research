#!/usr/bin/env python3
"""Verify that the diagonal 2/3 conormal truncation omits essential tails."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from route_bd_case_c_radial_obstruction import (
    PARAMETERS,
    SP,
    p_exponents,
    q_exponents,
    solve_stage,
)
from route_bd_fbar_obstruction import (
    K,
    ONE,
    PRIME,
    outer_coefficients,
)
from scratch_hamiltonian_natural_obstruction import k3_modes


P_POLYGON = ((0, 0), (1, 0), (8, 14), (8, 16), (0, 8))
Q_POLYGON = ((0, 0), (2, 1), (12, 21), (12, 24), (0, 12))


def lattice_points(
    polygon: tuple[tuple[int, int], ...],
) -> set[tuple[int, int]]:
    def inside(point: tuple[int, int]) -> bool:
        x, y = point
        return all(
            (polygon[(index + 1) % len(polygon)][0] - polygon[index][0])
            * (y - polygon[index][1])
            - (
                polygon[(index + 1) % len(polygon)][1]
                - polygon[index][1]
            )
            * (x - polygon[index][0])
            >= 0
            for index in range(len(polygon))
        )

    return {
        (x, y)
        for x in range(max(vertex[0] for vertex in polygon) + 1)
        for y in range(max(vertex[1] for vertex in polygon) + 1)
        if inside((x, y))
    }


def layer_inventory() -> None:
    """Check the complete toric layer ranges and the final u-degrees."""

    expected_p = {
        0: range(0, 9),
        1: range(0, 9),
        2: range(0, 9),
        3: range(0, 8),
        4: range(0, 7),
        5: range(0, 6),
        6: range(0, 5),
        7: range(0, 4),
        8: range(0, 3),
        9: (1,),
    }
    expected_q = {
        0: range(0, 13),
        1: range(0, 13),
        2: range(0, 13),
        3: range(0, 13),
        4: range(0, 12),
        5: range(0, 11),
        6: range(0, 10),
        7: range(0, 9),
        8: range(0, 8),
        9: range(0, 7),
        10: range(0, 6),
        11: range(0, 5),
        12: range(0, 4),
        13: (2,),
    }

    def layers(
        polygon: tuple[tuple[int, int], ...],
        scale: int,
    ) -> dict[int, tuple[int, ...]]:
        result: dict[int, list[int]] = {}
        for a, b in lattice_points(polygon):
            result.setdefault(scale + a - b, []).append(a)
        return {
            index: tuple(sorted(degrees))
            for index, degrees in result.items()
        }

    assert layers(P_POLYGON, 8) == {
        index: tuple(degrees)
        for index, degrees in expected_p.items()
    }
    assert layers(Q_POLYGON, 12) == {
        index: tuple(degrees)
        for index, degrees in expected_q.items()
    }

    # u^(scale+a-b) (t+u*w)^a has final u-degree scale+2a-b.
    assert max(8 + 2 * a - b for a, b in lattice_points(P_POLYGON)) == 10
    assert max(12 + 2 * a - b for a, b in lattice_points(Q_POLYGON)) == 15


def canonical_blocks_through_deficit_four(
) -> tuple[dict[int, dict[int, SP]], dict[int, dict[int, SP]]]:
    """Repeat the canonical modular recurrence only through the square row."""

    primitive = K(26839)
    u, v = outer_coefficients(primitive)
    modes = k3_modes(u, v)
    p_blocks: dict[int, dict[int, SP]] = {
        2: {
            -1: SP(ONE),
            **{
                index - 1: SP(u[index])
                for index in range(1, 8)
            },
        }
    }
    q_blocks: dict[int, dict[int, SP]] = {
        3: {
            -1: SP(ONE),
            **{
                index - 1: SP(v[index])
                for index in range(1, 11)
            },
        }
    }
    offsets = {1: 0, 0: 2, -1: 4, -2: 6}
    constraints: list[SP] = []
    for p_degree in (1, 0, -1, -2):
        q_degree = p_degree + 1
        p_support = p_exponents(p_degree)
        q_support = q_exponents(q_degree)
        kernel_count = len(modes.get(2 - p_degree, ()))
        p_block, q_block, new_constraints, _profile = solve_stage(
            p_blocks,
            q_blocks,
            p_degree,
            p_support,
            q_degree,
            q_support,
            (SP() for _ in range(kernel_count)),
        )
        if kernel_count:
            offset = offsets[p_degree]
            for local_index, (p_mode, q_mode) in enumerate(
                modes[2 - p_degree]
            ):
                parameter = PARAMETERS[offset + local_index]
                for exponent in p_support:
                    p_block[exponent] = (
                        p_block.get(exponent, SP())
                        + parameter * p_mode.get(exponent, SP())
                    )
                    if not p_block[exponent]:
                        p_block.pop(exponent, None)
                for exponent in q_support:
                    q_block[exponent] = (
                        q_block.get(exponent, SP())
                        + parameter * q_mode.get(exponent, SP())
                    )
                    if not q_block[exponent]:
                        q_block.pop(exponent, None)
        p_blocks[p_degree] = p_block
        q_blocks[q_degree] = q_block
        constraints.extend(new_constraints)

    assert len(constraints) == 2
    return p_blocks, q_blocks


def evaluate(polynomial: SP, values: tuple[K, ...]) -> K:
    result = K()
    for monomial, coefficient in polynomial.terms.items():
        term = coefficient
        for exponent, value in zip(monomial, values):
            term *= value**exponent
        result += term
    return result


def signed(value: K) -> int:
    assert not value.c1 and not value.c2
    return value.c0 if value.c0 <= PRIME // 2 else value.c0 - PRIME


def exact_tail_cancellation() -> None:
    """Exhibit M=-T!=0 on a certified deficit-four square-branch point."""

    p_blocks, q_blocks = canonical_blocks_through_deficit_four()
    kappa = K(169) / 48
    # Raw canonical coordinates agree with endpoint coordinates when
    # X1=X3=0.
    values = (K(1), K(), kappa, K(), K(), K(), K())
    h = sp.symbols("h")

    def expression(block: dict[int, SP]) -> sp.Expr:
        return sum(
            signed(evaluate(coefficient, values)) * h**exponent
            for exponent, coefficient in block.items()
        )

    p = {
        degree: expression(p_blocks[degree])
        for degree in (-2, -1, 0, 1, 2)
    }
    q = {
        degree: expression(q_blocks[degree])
        for degree in (-1, 0, 1, 2, 3)
    }

    def bracket(p_degree: int, q_degree: int) -> sp.Poly:
        result = h * (
            p_degree * p[p_degree] * sp.diff(q[q_degree], h)
            - q_degree * sp.diff(p[p_degree], h) * q[q_degree]
        )
        return sp.Poly(result, h, modulus=PRIME)

    middle = bracket(0, 1) + bracket(1, 0)
    tail = bracket(-2, 3) + bracket(-1, 2) + bracket(2, -1)
    assert middle
    assert tail
    assert middle + tail == 0
    assert middle.degree() == tail.degree() == 18
    assert len(middle.terms()) == len(tail.terms()) == 18
    assert middle.nth(18) == -5457
    assert tail.nth(18) == 5457

    # The outer quartic does not kill the omitted tail.
    primitive = K(26839)
    u, v = outer_coefficients(primitive)
    outer_u = sp.Poly(
        sum(signed(coefficient) * h**index for index, coefficient in enumerate(u)),
        h,
        modulus=PRIME,
    )
    outer_v = sp.Poly(
        sum(signed(coefficient) * h**index for index, coefficient in enumerate(v)),
        h,
        modulus=PRIME,
    )
    leading_ratio = v[-1] ** 2 / u[-1] ** 3
    quartic = sp.Poly(
        h * outer_v.as_expr() ** 2
        - signed(leading_ratio) * outer_u.as_expr() ** 3,
        h,
        modulus=PRIME,
    )
    assert quartic.degree() == 4
    assert sp.gcd(quartic, quartic.diff()).degree() == 0
    remainder = sp.rem(tail, quartic)
    assert remainder.as_expr() == (
        6521 * h**3 + 1918 * h**2 - 13412 * h - 5808
    )
    assert sp.rem(tail, quartic * quartic)


def symbolic_euler_coefficient() -> None:
    """Check the coefficient formula for the full Euler bracket."""

    u, w = sp.symbols("u w")
    f = sp.symbols("f0:4")
    g = sp.symbols("g0:4")
    functions_f = [sp.Function(f"F{index}")(w) for index in range(4)]
    functions_g = [sp.Function(f"G{index}")(w) for index in range(4)]
    full_f = sum(u**index * value for index, value in enumerate(functions_f))
    full_g = sum(u**index * value for index, value in enumerate(functions_g))
    euler = sp.expand(
        u * (
            sp.diff(full_f, u) * sp.diff(full_g, w)
            - sp.diff(full_f, w) * sp.diff(full_g, u)
        )
        - 8 * full_f * sp.diff(full_g, w)
        + 12 * sp.diff(full_f, w) * full_g
    )
    for degree in range(4):
        expected = sum(
            (left - 8)
            * functions_f[left]
            * sp.diff(functions_g[degree - left], w)
            + (12 - (degree - left))
            * sp.diff(functions_f[left], w)
            * functions_g[degree - left]
            for left in range(degree + 1)
        )
        assert sp.expand(euler.coeff(u, degree) - expected) == 0


def main() -> None:
    layer_inventory()
    symbolic_euler_coefficient()
    exact_tail_cancellation()
    print("verified complete diagonal layer ranges 0..10 and 0..15")
    print("verified the full Euler-bracket coefficient formula")
    print("verified M=-T!=0 on the exact r1 square-branch point")
    print("verified the omitted tail is nonzero modulo the outer quartic and its square")
    print("RESULT: THE 2/3 CONORMAL TRUNCATION IS NOT A CASE-C INVARIANT")


if __name__ == "__main__":
    main()
