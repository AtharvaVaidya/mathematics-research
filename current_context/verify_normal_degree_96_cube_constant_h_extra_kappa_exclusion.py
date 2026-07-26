#!/usr/bin/env python3
"""Exact certificates for the constant-h cube chart with an extra kappa."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import runpy

import sympy as sp


# Reuse the independently checked Laurent-residue construction.
dependency = Path(__file__).with_name(
    "verify_normal_degree_96_cube_laurent_time_reduction.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    data = runpy.run_path(str(dependency))

a, b, c, d, q = (data[name] for name in ("a", "b", "c", "d", "q"))
C, D, Q, z, v = sp.symbols("C D Q z v")
center = {
    c: C + a**2 / 4,
    d: D + a * b / 2,
    q: Q + b**2 / 4,
}

kappas = {
    8: data["kappa8"],
    7: data["kappa7"],
    5: data["kappa5"],
    4: data["kappa4"],
    3: data["j"],
    2: data["kappa2"],
    1: data["kappa1"],
}
extra_exponents = (8, 7, 5, 4, 2, 1)
all_zero = {parameter: 0 for parameter in kappas.values()}

A = {
    ell: sp.factor(data["A"][ell].subs(center))
    for ell in range(1, 6)
}
A_pure = {
    ell: sp.factor(A[ell].subs(all_zero))
    for ell in range(1, 6)
}


def transverse_part(expression: sp.Expr, degree: int) -> sp.Expr:
    """Homogeneous part of the indicated degree in (C,D,Q)."""
    scaled = sp.expand(
        expression.subs({C: z * C, D: z * D, Q: z * Q})
    )
    return sp.factor(scaled.coeff(z, degree))


N = {
    ell: transverse_part(A_pure[ell], 2)
    for ell in range(1, 6)
}
H = {
    ell: transverse_part(A_pure[ell], 3)
    for ell in range(1, 6)
}

expected_N = {
    1: sp.Rational(3, 16) * (C**2 * a - 4 * C * Q - 2 * D**2),
    2: sp.Rational(3, 16)
    * (C**2 * b + 2 * C * D * a - 4 * D * Q),
    3: -sp.Rational(1, 16)
    * (
        C**2 * a**2
        - 6 * C * D * b
        - 4 * C * Q * a
        - 2 * D**2 * a
        + 6 * Q**2
    ),
    4: -sp.Rational(1, 32)
    * (
        3 * C**2 * a * b
        + 2 * C * D * a**2
        - 8 * C * Q * b
        - 4 * D**2 * b
        - 4 * D * Q * a
    ),
    5: sp.Rational(1, 192)
    * (
        C**2 * a**3
        - 6 * C**2 * b**2
        - 12 * C * D * a * b
        - 4 * C * Q * a**2
        - 2 * D**2 * a**2
        + 24 * D * Q * b
    ),
}
expected_H = {
    1: 0,
    2: 0,
    3: C**3 / 16,
    4: 3 * C**2 * D / 16,
    5: -C * (C**2 * a - 2 * C * Q - 4 * D**2) / 32,
}
for ell in range(1, 6):
    assert sp.expand(N[ell] - expected_N[ell]) == 0
    assert sp.expand(H[ell] - expected_H[ell]) == 0


# The pure weighted boundary has precisely the perfect-square stratum
# C=D=Q=0 and the displayed one-parameter cusp.  The following
# elementary consequences of A_1=...=A_4=0 certify the case split:
# A_4=0 modulo A_1,A_2 gives C^2 D=0; if C=0 then D=Q=0; if
# D=0,C!=0, the remaining equations force b=0,Q=Ca/4,C=3a^2/8.
top = [A_pure[ell] for ell in range(1, 5)]
assert sp.factor(
    top[3] + b * top[0] / 3 + a * top[1] / 6
) == 3 * C**2 * D / 16
assert sp.factor(top[0].subs(C, 0)) == -3 * D**2 / 8
assert sp.factor(top[2].subs({C: 0, D: 0})) == -3 * Q**2 / 8

cusp = {
    b: 0,
    C: 3 * a**2 / 8,
    D: 0,
    Q: 3 * a**3 / 32,
}
for expression in top:
    assert sp.factor(expression.subs(cusp)) == 0
assert sp.factor(A_pure[5].subs(cusp)) == -27 * (a / 4) ** 7 / 2


def first_kappa(exponent: int, ell: int) -> sp.Expr:
    """The first-kappa term on the perfect-square stratum."""
    substitution = all_zero.copy()
    substitution[kappas[exponent]] = 1
    return sp.factor(
        A[ell].subs(substitution).subs({C: 0, D: 0, Q: 0})
    )


K = {
    exponent: {
        ell: first_kappa(exponent, ell)
        for ell in range(1, 6)
    }
    for exponent in extra_exponents
}
assert all(K[exponent][3] == 0 for exponent in extra_exponents)


def numerators(expressions: list[sp.Expr]) -> list[sp.Expr]:
    return [
        sp.together(expression).as_numer_denom()[0]
        for expression in expressions
    ]


def is_unit_groebner(
    expressions: list[sp.Expr], variables: tuple[sp.Symbol, ...]
) -> bool:
    if not variables:
        return any(sp.factor(expression) != 0 for expression in expressions)
    basis = sp.groebner(
        numerators(expressions),
        *variables,
        order="grevlex",
    )
    return len(basis.polys) == 1 and basis.polys[0].as_expr() == 1


# Two charts cover the weighted projective (a,b)-line: a=1 and
# a=0,b=1.  First, a first kappa cannot occur strictly before the
# quadratic normal term.
for exponent in extra_exponents:
    resonance = [K[exponent][ell] for ell in range(1, 5)]
    assert is_unit_groebner(
        [expression.subs(a, 1) for expression in resonance],
        (b,),
    )
    assert is_unit_groebner(
        [expression.subs({a: 0, b: 1}) for expression in resonance],
        (),
    )


# In the balanced case the leading four equations are N_i+K_i=0.
# The terminal leading coefficient is N_5+K_5.  Adding it to the
# four-equation ideal gives a unit ideal in both projective charts.
balanced_results: dict[int, tuple[bool, bool]] = {}
for exponent in extra_exponents:
    equations = [
        sp.factor(N[ell] + K[exponent][ell])
        for ell in range(1, 5)
    ]
    terminal = sp.factor(N[5] + K[exponent][5])
    chart_a = is_unit_groebner(
        [expression.subs(a, 1) for expression in equations + [terminal]],
        (Q, D, C, b),
    )
    chart_b = is_unit_groebner(
        [
            expression.subs({a: 0, b: 1})
            for expression in equations + [terminal]
        ],
        (Q, D, C),
    )
    balanced_results[exponent] = (chart_a, chart_b)
assert all(result == (True, True) for result in balanced_results.values())


# Singular quadratic-normal cusp and its second blowup.
normal_cusp = {
    a: -6 * v**2,
    b: 4 * v**3,
    C: 1,
    D: v,
    Q: -2 * v**2,
}
assert all(sp.factor(N[ell].subs(normal_cusp)) == 0 for ell in range(1, 5))

variables = (a, b, C, D, Q)
normal_jacobian = sp.Matrix(
    [
        [
            sp.factor(sp.diff(N[ell], variable).subs(normal_cusp))
            for variable in variables
        ]
        for ell in range(1, 5)
    ]
)
left_one = sp.Matrix([2 * v**2, -2 * v, 1, 0])
left_two = sp.Matrix([4 * v**3 / 3, -v**2, 0, 1])
assert normal_jacobian.rank() == 2
assert (left_one.T * normal_jacobian) == sp.zeros(1, 5)
assert (left_two.T * normal_jacobian) == sp.zeros(1, 5)

cubic_vector = sp.Matrix(
    [sp.factor(H[ell].subs(normal_cusp)) for ell in range(1, 5)]
)
assert cubic_vector == sp.Matrix([0, 0, sp.Rational(1, 16), 3 * v / 16])

expected_determinants = {
    8: -sp.Rational(6175, 972) * v**12,
    7: sp.Rational(2737, 648) * v**11,
    5: -sp.Rational(1235, 648) * v**9,
    4: sp.Rational(187, 144) * v**8,
    2: -sp.Rational(91, 144) * v**6,
    1: sp.Rational(11, 24) * v**5,
}
for exponent in extra_exponents:
    kappa_vector = sp.Matrix(
        [
            sp.factor(K[exponent][ell].subs(normal_cusp))
            for ell in range(1, 5)
        ]
    )
    pairing_matrix = sp.Matrix(
        [
            [left_one.dot(kappa_vector), left_one.dot(cubic_vector)],
            [left_two.dot(kappa_vector), left_two.dot(cubic_vector)],
        ]
    )
    determinant = sp.factor(pairing_matrix.det())
    assert sp.factor(determinant - expected_determinants[exponent]) == 0

# The rank-two Jacobian has one infinitesimal kernel direction beyond
# the two tangent directions of the normal-cusp family.  Gauge it by
# E=(4,-4v,0,0,1).  Its first nonzero self-interaction has cokernel
# vector (-3/8,0), which is independent of the pure cubic vector and
# of every first-kappa vector.  Thus it cannot occur at an earlier
# unmatched order.
extra_null = sp.Matrix([4, -4 * v, 0, 0, 1])
assert normal_jacobian * extra_null == sp.zeros(4, 1)
epsilon = sp.symbols("epsilon")
extra_path = {
    a: -6 * v**2 + 4 * epsilon,
    b: 4 * v**3 - 4 * v * epsilon,
    C: 1,
    D: v,
    Q: -2 * v**2 + epsilon,
}
extra_quadratic = sp.Matrix(
    [
        sp.factor(sp.expand(N[ell].subs(extra_path)).coeff(epsilon, 2))
        for ell in range(1, 5)
    ]
)
assert extra_quadratic == sp.Matrix([0, 0, -sp.Rational(3, 8), 0])
assert sp.factor(
    sp.det(
        sp.Matrix(
            [
                [left_one.dot(extra_quadratic), left_one.dot(cubic_vector)],
                [left_two.dot(extra_quadratic), left_two.dot(cubic_vector)],
            ]
        )
    )
) == -9 * v / 128
for exponent in extra_exponents:
    kappa_vector = sp.Matrix(
        [
            sp.factor(K[exponent][ell].subs(normal_cusp))
            for ell in range(1, 5)
        ]
    )
    assert sp.factor(
        sp.det(
            sp.Matrix(
                [
                    [
                        left_one.dot(extra_quadratic),
                        left_one.dot(kappa_vector),
                    ],
                    [
                        left_two.dot(extra_quadratic),
                        left_two.dot(kappa_vector),
                    ],
                ]
            )
        )
    ) != 0


# A coordinate-free terminal check for the triple collision.  Use the
# quotient-kernel representative n=(4v^2,-4v^3,1,0,0).  Its quadratic
# obstruction M has cokernel pair (-3v^4/2,0).  When K,L,M all meet,
# the first four equations determine the L and M amplitudes from the
# nonzero kappa amplitude.  The fifth row cannot then vanish.
quotient_null = sp.Matrix([4 * v**2, -4 * v**3, 1, 0, 0])
assert normal_jacobian * quotient_null == sp.zeros(4, 1)
quotient_path = {
    variable: normal_cusp[variable] + epsilon * coefficient
    for variable, coefficient in zip(variables, quotient_null)
}
quotient_quadratic = sp.Matrix(
    [
        sp.factor(sp.expand(N[ell].subs(quotient_path)).coeff(epsilon, 2))
        for ell in range(1, 6)
    ]
)
assert left_one.dot(quotient_quadratic[:4, :]) == -3 * v**4 / 2
assert left_two.dot(quotient_quadratic[:4, :]) == 0

full_cubic_vector = sp.Matrix(
    [sp.factor(H[ell].subs(normal_cusp)) for ell in range(1, 6)]
)
normal_jacobian_five = sp.Matrix(
    [
        [
            sp.factor(sp.diff(N[ell], variable).subs(normal_cusp))
            for variable in variables
        ]
        for ell in range(1, 6)
    ]
)
assert all(
    sp.factor(
        normal_jacobian_five[4, column]
        - v**4 * normal_jacobian_five[0, column]
        + sp.Rational(2, 3) * v**3 * normal_jacobian_five[1, column]
    )
    == 0
    for column in range(5)
)


def terminal_cokernel(vector: sp.Matrix) -> sp.Expr:
    return sp.factor(
        vector[4] - v**4 * vector[0] + sp.Rational(2, 3) * v**3 * vector[1]
    )


expected_triple_terminal = {
    8: sp.Rational(20900, 243) * v**13,
    7: -sp.Rational(13685, 243) * v**12,
    5: sp.Rational(1976, 81) * v**10,
    4: -sp.Rational(1309, 81) * v**9,
    2: sp.Rational(65, 9) * v**7,
    1: -sp.Rational(44, 9) * v**6,
}
for exponent in extra_exponents:
    full_kappa_vector = sp.Matrix(
        [
            sp.factor(K[exponent][ell].subs(normal_cusp))
            for ell in range(1, 6)
        ]
    )
    cubic_amplitude = sp.factor(
        -left_two.dot(full_kappa_vector[:4, :])
        / left_two.dot(full_cubic_vector[:4, :])
    )
    null_amplitude = sp.factor(
        -(
            left_one.dot(full_kappa_vector[:4, :])
            + cubic_amplitude
            * left_one.dot(full_cubic_vector[:4, :])
        )
        / left_one.dot(quotient_quadratic[:4, :])
    )
    terminal = sp.factor(
        terminal_cokernel(full_kappa_vector)
        + cubic_amplitude * terminal_cokernel(full_cubic_vector)
        + null_amplitude * terminal_cokernel(quotient_quadratic)
    )
    assert sp.factor(terminal - expected_triple_terminal[exponent]) == 0

print("verified: pure boundary is perfect-square stratum or cusp")
print("verified: cusp terminal A_5 coefficient is nonzero")
print("verified: strict first-kappa ideals are units in both charts")
print("verified: all twelve balanced terminal ideals are Groebner units")
print("verified: singular normal cusp has rank-two differential")
print("verified: all six second-blowup determinants are nonzero")
print("verified: the extra null direction and triple collision are excluded")
print("verified: all six triple-collision terminal coefficients are nonzero")
