#!/usr/bin/env python3
"""Audit the exact interface for the GGHV case-c certificate.

The default run is intentionally quick.  It checks:

* every lattice point of the two polygons in GGHV Proposition 4.3(1);
* the unimodular radial coordinate dictionary;
* the location of the two required opposite vertices;
* the five-point Hurwitz count;
* the seven kernel dimensions and the absence of later kernels; and
* the complete factorization of the exact outer quintic modulo 32003.

The optional flags invoke the slower certificate layers:

    --run-special-fiber
        the complete finite-field weighted-projective origin certificate;

    --run-direct-q
        the homogeneous characteristic-zero h-power certificates for the
        two generic charts (using Singular modStd with exactness=1);

    --run-special-q
        the exact-quintic determinant/resultant certificates for the two
        boundary charts and the coefficientwise good-reduction check.

For a cache-free publication run, first move the three
``tmp/case_c_n3_*_Q.pkl`` files out of ``tmp`` and then use
``--run-special-fiber --run-special-q``.  The direct-Q experiment is
optional and is not part of the proof protocol.  The cache files are
accelerators, not certificate inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import warnings

import sympy as sp
from sympy.utilities.exceptions import SymPyDeprecationWarning

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
warnings.filterwarnings("ignore", category=SymPyDeprecationWarning)

from route_bd_ab_hurwitz_count import hurwitz_number
from route_bd_case_c_radial_obstruction import (
    p_exponents,
    q_exponents,
    verify_support_inventory,
)
from route_bd_fbar_obstruction import K, PRIME, outer_coefficients

P_POLYGON = ((0, 0), (1, 0), (8, 14), (8, 16), (0, 8))
Q_POLYGON = ((0, 0), (2, 1), (12, 21), (12, 24), (0, 12))

# Primitive integer form of the exact normalized outer eliminant.
OUTER_QUINTIC_COEFFICIENTS = (
    5515523528689697521685932802788985662696864088064,
    65062739516770841146036374449381894864326252512971587584,
    344441584702591633271258969281268771087358180440968435133841408,
    1237781539078909858338290542300930711454790682861991293593776119332864,
    2419327446396921250927947382299550515503991095316771187749320719639052502144,
    -930206660129096433749475266122359445351031352517661885125550567798599734193335611,
)


def lattice_points(
    polygon: tuple[tuple[int, int], ...],
) -> set[tuple[int, int]]:
    """Enumerate the lattice points of a counterclockwise convex polygon."""

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


def radial(point: tuple[int, int]) -> tuple[int, int]:
    """x^a y^b = z^(2a-b) h^(b-a), for z=xy and h=xy^2."""

    a, b = point
    return 2 * a - b, b - a


def expected_radial_supports() -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    p_support = {
        (2, exponent)
        for exponent in range(-1, 7)
    }
    q_support = {
        (3, exponent)
        for exponent in range(-1, 10)
    }
    for degree in range(1, -9, -1):
        p_support.update((degree, exponent) for exponent in p_exponents(degree))
    for degree in range(2, -13, -1):
        q_support.update((degree, exponent) for exponent in q_exponents(degree))
    # The recurrence deliberately removes the two bracket-invisible constants.
    p_support.add((0, 0))
    q_support.add((0, 0))
    return p_support, q_support


def verify_polygon_dictionary() -> None:
    p_points = lattice_points(P_POLYGON)
    q_points = lattice_points(Q_POLYGON)
    expected_p, expected_q = expected_radial_supports()
    assert {radial(point) for point in p_points} == expected_p
    assert {radial(point) for point in q_points} == expected_q
    assert len(p_points) == 61
    assert len(q_points) == 125

    # The determinant of (a,b) -> (2a-b,b-a) is one.
    assert 2 * 1 - (-1) * (-1) == 1

    # These are the required case-c vertices.  They occur in the last
    # radial blocks, not in the early deficit-two/three blocks.
    assert radial((0, 8)) == (-8, 8)
    assert radial((0, 12)) == (-12, 12)
    assert 2 - (-8) == 10       # P deficit
    assert 3 - (-12) == 15      # Q deficit
    verify_support_inventory()
    print("support: exact 61/125-point GGHV polygon dictionary")
    print("required vertices: z^-8 h^8 (deficit 10), z^-12 h^12 (deficit 15)")


def verify_outer_good_reduction() -> None:
    s = sp.symbols("s")
    quintic = sum(
        coefficient * s ** (5 - index)
        for index, coefficient in enumerate(OUTER_QUINTIC_COEFFICIENTS)
    )
    factors = sp.factor_list(quintic, modulus=PRIME)[1]
    monic_factors = {
        sp.Poly(factor, s, modulus=PRIME).monic().as_expr(): multiplicity
        for factor, multiplicity in factors
    }
    expected = {
        sp.Poly(s - 26839, s, modulus=PRIME).monic().as_expr(): 1,
        sp.Poly(s - 16621, s, modulus=PRIME).monic().as_expr(): 1,
        sp.Poly(
            s**3 - 11133 * s**2 - 11294 * s - 6180,
            s,
            modulus=PRIME,
        ).monic().as_expr(): 1,
    }
    assert monic_factors == expected
    assert sum(sp.degree(factor) * multiplicity for factor, multiplicity in factors) == 5
    print("outer reduction: squarefree factor degrees 1+1+3 at 32003")


def verify_hurwitz_and_kernel_counts() -> None:
    _character_sum, weighted_count, _nonzero_terms = hurwitz_number()
    assert weighted_count == 5

    def matrix_rank(matrix: list[list[K]]) -> int:
        work = [list(row) for row in matrix]
        pivot_row = 0
        for column in range(len(work[0]) if work else 0):
            selected = next(
                (
                    row
                    for row in range(pivot_row, len(work))
                    if work[row][column]
                ),
                None,
            )
            if selected is None:
                continue
            work[pivot_row], work[selected] = work[selected], work[pivot_row]
            inverse = work[pivot_row][column].inverse()
            work[pivot_row] = [
                coefficient * inverse
                for coefficient in work[pivot_row]
            ]
            for row in range(len(work)):
                if row == pivot_row or not work[row][column]:
                    continue
                multiplier = work[row][column]
                work[row] = [
                    work[row][index] - multiplier * work[pivot_row][index]
                    for index in range(len(work[row]))
                ]
            pivot_row += 1
            if pivot_row == len(work):
                break
        return pivot_row

    def kernel_dimensions(primitive: K) -> tuple[int, ...]:
        u, v = outer_coefficients(primitive)
        p_outer = {
            index - 1: coefficient
            for index, coefficient in enumerate(u)
        }
        q_outer = {
            index - 1: coefficient
            for index, coefficient in enumerate(v)
        }
        dimensions: list[int] = []
        for deficit in range(1, 16):
            p_degree = 2 - deficit
            q_degree = 3 - deficit
            columns: list[dict[int, K]] = []
            for exponent in p_exponents(p_degree):
                columns.append(
                    {
                        exponent + outer_exponent:
                        coefficient
                        * (p_degree * outer_exponent - 3 * exponent)
                        for outer_exponent, coefficient in q_outer.items()
                        if coefficient
                        * (p_degree * outer_exponent - 3 * exponent)
                    }
                )
            for exponent in q_exponents(q_degree):
                columns.append(
                    {
                        exponent + outer_exponent:
                        coefficient
                        * (2 * exponent - q_degree * outer_exponent)
                        for outer_exponent, coefficient in p_outer.items()
                        if coefficient
                        * (2 * exponent - q_degree * outer_exponent)
                    }
                )
            rows = sorted(set().union(*(set(column) for column in columns)))
            matrix = [
                [column.get(exponent, K()) for column in columns]
                for exponent in rows
            ]
            dimensions.append(len(columns) - matrix_rank(matrix))
        return tuple(dimensions)

    expected_kernel_dimensions = (2, 2, 2, 1) + (0,) * 11
    for label, primitive in (
        ("r1", K(26839)),
        ("r2", K(16621)),
        ("cubic", K(0, 1)),
    ):
        dimensions = kernel_dimensions(primitive)
        assert dimensions == expected_kernel_dimensions
        print(f"{label} kernel dimensions: {dimensions}")

    print("Hurwitz count: five normalized covers")
    print("later propagation: no new kernel after deficit four")


def run_script(script: str, *arguments: str) -> None:
    command = [sys.executable, str(ROOT / script), *arguments]
    print(f"\n==> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-special-fiber", action="store_true")
    parser.add_argument("--run-direct-q", action="store_true")
    parser.add_argument("--run-special-q", action="store_true")
    args = parser.parse_args()

    verify_polygon_dictionary()
    verify_outer_good_reduction()
    verify_hurwitz_and_kernel_counts()

    if args.run_special_fiber:
        run_script("route_bd_case_c_radial_obstruction.py")
    if args.run_direct_q:
        for chart in ("L_NE_0", "L_EQ_0_A_NE_0"):
            run_script(
                "scratch_case_c_n3_generic_charts_Q.py",
                "--skip-modular-crosscheck",
                "--chart",
                chart,
                "--one-certificate",
            )
    if args.run_special_q:
        run_script("scratch_case_c_n3_special_charts_Q.py")

    print("\nRESULT: CASE-c CERTIFICATE INTERFACE CHECKS PASSED")


if __name__ == "__main__":
    main()
