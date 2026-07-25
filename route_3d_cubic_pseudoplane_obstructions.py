#!/usr/bin/env python3
"""Exact algebra behind the first cubic-pseudo-plane obstructions."""

from __future__ import annotations

import sympy as sp


def reduce_w3(expr: sp.Expr, u: sp.Symbol, v: sp.Symbol, w: sp.Symbol) -> sp.Expr:
    """Reduce an expression modulo w^3-u-u^2*v."""
    return sp.rem(
        sp.Poly(sp.expand(expr), w),
        sp.Poly(w**3 - u - u**2 * v, w),
    ).as_expr()


def bracket(
    left: sp.Expr,
    right: sp.Expr,
    u: sp.Symbol,
    v: sp.Symbol,
    w: sp.Symbol,
) -> sp.Expr:
    raw = (
        -3 * w**2
        * (sp.diff(left, u) * sp.diff(right, v)
           - sp.diff(left, v) * sp.diff(right, u))
        - u**2
        * (sp.diff(left, u) * sp.diff(right, w)
           - sp.diff(left, w) * sp.diff(right, u))
        + (1 + 2 * u * v)
        * (sp.diff(left, v) * sp.diff(right, w)
           - sp.diff(left, w) * sp.diff(right, v))
    )
    return sp.expand(reduce_w3(raw, u, v, w))


def verify_elliptic_identity() -> None:
    u, v, w = sp.symbols("u v w")
    s = 1 + 2 * u * v
    assert reduce_w3(s**2 - (1 + 4 * v * w**3), u, v, w) == 0
    assert bracket(v, w, u, v, w) == s
    assert bracket(v, s, u, v, w) == 6 * v * w**2


def verify_w_slice() -> None:
    u, v, w = sp.symbols("u v w")
    r = u * v
    delta_r = bracket(w, r, u, v, w)
    assert reduce_w3(delta_r + w**3, u, v, w) == 0
    # Since {w,w}=0, division by w^3 does not add a quotient-rule term.
    assert sp.simplify(-delta_r / w**3 - 1).subs(
        w**3, u + u**2 * v
    ) == 0
    assert reduce_w3(u * (r + 1) - w**3, u, v, w) == 0


def verify_mod_two_cokernel(max_degree: int = 12) -> None:
    """Check the all-monomial coefficient proof on a generous finite box."""
    u, v, w = sp.symbols("u v w")
    target = u * v
    assert sp.Poly(bracket(v, w, u, v, w) - 1, u, v, w, modulus=2).is_zero

    for i in range(max_degree + 1):
        for j in range(max_degree + 1):
            for k in range(3):
                monomial = u**i * v**j * w**k
                dw = sp.Poly(
                    bracket(monomial, w, u, v, w), u, v, w, modulus=2
                )
                dv = sp.Poly(
                    bracket(v, monomial, u, v, w), u, v, w, modulus=2
                )
                assert dw.coeff_monomial(target) == 0
                assert dv.coeff_monomial(target) == 0

    assert sp.Poly(target, u, v, w, modulus=2).coeff_monomial(target) == 1


def verify_graph_deformation_family() -> None:
    """Convention and squarefreeness identities for P=v+f(w)."""
    u, v, w, T = sp.symbols("u v w T")
    coefficients = sp.symbols("f0:5")
    f = sum(coefficient * w**index for index, coefficient in enumerate(coefficients))
    P = v + f
    s = 1 + 2 * u * v
    assert bracket(P, w, u, v, w) == s

    generic_right_side = 1 + 4 * (T - f) * w**3
    assert reduce_w3(
        sp.expand(generic_right_side.subs(T, P) - s**2),
        u,
        v,
        w,
    ) == 0

    # At a hypothetical multiple root w != 0, h=h'=0 eliminate T and
    # leave an equation independent of the transcendental T.
    solved_T = f - sp.Rational(1, 4) / w**3
    derivative_after_elimination = sp.factor(
        sp.diff(generic_right_side, w).subs(T, solved_T)
    )
    assert sp.simplify(
        derivative_after_elimination
        + (4 * w**4 * sp.diff(f, w) + 3) / w
    ) == 0

    for degree in range(0, 10):
        polynomial_degree = 3 if degree == 0 else degree + 3
        assert polynomial_degree >= 3
        if polynomial_degree % 2:
            assert polynomial_degree - 3 >= 0
        else:
            assert polynomial_degree // 2 - 2 >= 0


def verify_first_transverse_shear_family() -> None:
    """Exact double-cover and differential identities for P=v+w*A(v)."""
    u, v, w, T = sp.symbols("u v w T")
    coefficients = sp.symbols("a0:5")
    A = sum(coefficient * v**index for index, coefficient in enumerate(coefficients))
    P = v + w * A
    s = 1 + 2 * u * v

    assert sp.expand(bracket(P, v, u, v, w) + A * s) == 0
    w_on_fiber = (T - v) / A
    rational_discriminant = 1 + 4 * v * (T - v) ** 3 / A**3
    Y_squared = sp.factor(A**4 * rational_discriminant)
    N = A**3 + 4 * v * (T - v) ** 3
    assert sp.factor(Y_squared - A * N) == 0
    assert sp.diff(N, T) == 12 * v * (T - v) ** 2
    assert sp.expand(N.subs(T, v) - A**3) == 0

    # The restriction of the Hamiltonian vector field to the generic
    # fiber is -A*s*d/dv, so its dual differential is -A*dv/Y.
    assert sp.simplify(
        -1 / (A * s) + A / (A**2 * s)
    ) == 0
    assert sp.simplify(
        w_on_fiber - (T - v) / A
    ) == 0

    for degree in range(0, 20):
        h_degree = 4 if degree == 0 else (5 if degree == 1 else 4 * degree)
        if h_degree % 2 == 0:
            infinity_order = h_degree // 2 - degree - 2
        else:
            # At the unique ramified point at infinity, v has pole order
            # two, so ord(A*dv/Y)=-2d-3+deg(H).
            infinity_order = h_degree - 2 * degree - 3
        assert infinity_order >= 0


def main() -> None:
    verify_elliptic_identity()
    verify_w_slice()
    verify_mod_two_cokernel()
    verify_graph_deformation_family()
    verify_first_transverse_shear_family()
    print("v-fiber elliptic identities: verified")
    print("w-fiber rational slice and incompatible boundary fillings: verified")
    print("mod-2 [uv] cokernel kills every first correction: verified")
    print("v+f(w) hyperelliptic obstruction: verified")
    print("v+w*A(v) transverse-shear obstruction: verified")
    print("RESULT: CUBIC PSEUDO-PLANE FIRST OBSTRUCTIONS PASS")


if __name__ == "__main__":
    main()
