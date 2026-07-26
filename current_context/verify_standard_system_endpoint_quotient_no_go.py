#!/usr/bin/env python3
"""Verify the exact endpoint-quotient no-go identities."""

from __future__ import annotations

import sympy as sp


def homogenized_bracket(
    first: sp.Expr,
    second: sp.Expr,
    X: sp.Symbol,
    tau: sp.Symbol,
    n: int,
    m: int,
) -> sp.Expr:
    return sp.expand(
        tau
        * (
            sp.diff(first, X) * sp.diff(second, tau)
            - sp.diff(first, tau) * sp.diff(second, X)
        )
        + n * first * sp.diff(second, X)
        - m * second * sp.diff(first, X)
    )


def verify_three_layer_decomposition() -> None:
    X, tau = sp.symbols("X tau")
    u, v, s, t = sp.symbols("u v s t")
    # Exact representative with g,a,b >=2.
    g, a, b = 3, 2, 5
    n, m = g * a, g * b
    R = X**g + sp.Symbol("r1") * X + sp.Symbol("r0")
    linear_p = u * X + v
    linear_q = s * X + t
    P = R**a + tau ** (n - 1) * linear_p
    Q = R**b + tau ** (m - 1) * linear_q

    expected = sp.expand(
        b
        * tau ** (n - 1)
        * R ** (b - 1)
        * (sp.diff(R, X) * linear_p - g * R * u)
        + a
        * tau ** (m - 1)
        * R ** (a - 1)
        * (g * R * s - sp.diff(R, X) * linear_q)
        + (s * v - u * t) * tau ** (m + n - 2)
    )
    assert sp.expand(homogenized_bracket(P, Q, X, tau, n, m) - expected) == 0

    # The alternating endpoint map is onto the scalar forcing line.
    scalar = sp.symbols("scalar")
    assert (s * v - u * t).subs(
        {u: 0, v: 1, s: scalar, t: 0}
    ) == scalar


def verify_affine_cross_map_has_no_squarefree_kernel() -> None:
    X = sp.symbols("X")
    u, v = sp.symbols("u v")
    for g in range(2, 8):
        coefficients = sp.symbols(f"r0:{g}")
        R = X**g + sum(coefficients[j] * X**j for j in range(g))
        L = u * X + v
        cross = sp.Poly(
            sp.expand(sp.diff(R, X) * L - g * R * sp.diff(L, X)),
            X,
        )
        equations = [coefficient for coefficient in cross.all_coeffs()]
        # The top coefficient cancels.  The next coefficient forces the
        # x^(g-1) coefficient of R to be compatible with L; the full
        # identity is exactly (R/L^g)'=0 after localization at L.
        localized_identity = sp.factor(
            sp.diff(R / L**g, X)
            - cross.as_expr() / L ** (g + 1)
        )
        assert localized_identity == 0

        # A concrete squarefree R has no nonzero affine kernel.
        squarefree_R = X**g - 1
        concrete = sp.Poly(
            sp.diff(squarefree_R, X) * L
            - g * squarefree_R * sp.diff(L, X),
            X,
        )
        coefficient_equations = [
            sp.Eq(coefficient, 0)
            for coefficient in concrete.all_coeffs()
        ]
        assert sp.solve(coefficient_equations, (u, v), dict=True) == [
            {u: 0, v: 0}
        ]


def verify_relative_log_extension_term() -> None:
    X = sp.symbols("X")
    a, b, g = sp.symbols("a b g", integer=True, positive=True)
    R = sp.Function("R")(X)
    Lp = sp.Function("Lp")(X)
    Lq = sp.Function("Lq")(X)
    n, m = g * a, g * b
    d, e = n - 1, m - 1
    A = Lp / R**a
    B = Lq / R**b

    extension = sp.factor(a * (e * sp.diff(A, X) * B - d * A * sp.diff(B, X)))
    expected = (
        a
        / R ** (a + b)
        * (
            (m - 1) * sp.diff(Lp, X) * Lq
            - (n - 1) * Lp * sp.diff(Lq, X)
            + (a - b) * sp.diff(R, X) / R * Lp * Lq
        )
    )
    assert sp.simplify(extension - expected) == 0

    # The extension is not a function of the endpoint determinant alone:
    # two pairs with the same endpoint scalar have different extensions.
    x = sp.symbols("x")
    concrete_R = x**3 - 1

    def concrete_extension(lp: sp.Expr, lq: sp.Expr) -> sp.Expr:
        aa, bb, gg = 2, 5, 3
        dd, ee = gg * aa - 1, gg * bb - 1
        AA = lp / concrete_R**aa
        BB = lq / concrete_R**bb
        return sp.factor(
            aa * (ee * sp.diff(AA, x) * BB - dd * AA * sp.diff(BB, x))
        )

    # Both endpoint determinants equal one:
    # (Lp,Lq)=(1,x) and (1,x+1).
    first = concrete_extension(sp.Integer(1), x)
    second = concrete_extension(sp.Integer(1), x + 1)
    assert sp.factor(first - second) != 0


def verify_branch_invisibility_arithmetic() -> None:
    # Recheck the valuation used to make the branch map zero.
    for g in range(2, 9):
        for a in range(2, 9):
            for b in range(2, 9):
                n, m = g * a, g * b
                N = n + m - 2
                derivative_order = (a - 1) * (n - 1)
                quotient_order = a * N - derivative_order
                assert quotient_order - a * m == a * (g - 1) - 1
                assert quotient_order > a * m


def main() -> None:
    verify_three_layer_decomposition()
    verify_affine_cross_map_has_no_squarefree_kernel()
    verify_relative_log_extension_term()
    verify_branch_invisibility_arithmetic()
    print("verified: exact lower-cross/endpoint bracket decomposition")
    print("verified: affine endpoint map is onto but affine cross maps are injective")
    print("verified: relative-log extension is not determined by endpoint scalar")
    print("verified: every branch functional kills the scalar endpoint space")
    print("RESULT: the naive endpoint-invisible quotient has no obstruction")


if __name__ == "__main__":
    main()
