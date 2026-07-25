#!/usr/bin/env python3
"""Exact limitations of two natural Hamiltonian shortcuts.

The all-k radial kernel theorem gives seven Hamiltonians

    H_{d,C} = -z^(5-d) C(w) / ((5-d) w)

of weights (1,1,2,2,3,3,4).  Four are the polynomial parts at infinity
of classes whose leading C monomial is

    C_d = w^((5-d) k + 1),  d=1,2,3,4.

This verifier records two negative results which constrain any proposed
uniform nonlinear proof.

1.  The leading infinity symbols of all four high classes are functions
    of the single monomial xi=z*w^k.  Their Hamiltonian brackets vanish.
    In fact the outer contact identity makes their complete infinity
    expansions powers of one common formal coordinate through every
    polynomial term.  The exact scalar C-star-D formula verifies the
    resulting cancellation.

2.  Giving the seven parameters the degrees of their C polynomials does
    not produce a zero-dimensional initial ideal.  For the complete k=1
    and k=2 outer coefficient fields, every weight-at-most-eight
    consistency equation has a unique highest term, a nonzero pure power
    of X1.  Consequently the initial ideal is only <X1^4>.

The script also checks that a finite-support Hamiltonian flow on the
Laurent Darboux torus need not have a locally nilpotent generator:
H=r*s generates the semisimple scaling derivation.

These are countermodels to proof strategies, not counterexamples to any
Jacobian-conjecture statement.
"""

from __future__ import annotations

import sympy as sy

from scratch_hamiltonian_natural_obstruction import natural_consistency


def cstar_monomial_coefficient(
    d: int,
    r: int | sy.Expr,
    e: int,
    s: int | sy.Expr,
) -> sy.Expr:
    """Coefficient of w^(r+s+1) in C-star-D for C=w^r,D=w^s."""

    c = 5 - d
    f = 5 - e
    g = 5 - d - e
    assert c and f and g
    return sy.factor(
        -g
        * (
            (sy.sympify(r) - 1) / c
            + (1 - sy.sympify(s)) / f
        )
    )


def verify_abelian_high_symbol() -> None:
    k, z, w = sy.symbols("k z w", integer=True, positive=True)
    xi = z * w**k
    for d in range(1, 5):
        c = 5 - d
        leading_c = w ** (c * k + 1)
        hamiltonian = sy.cancel(-z**c * leading_c / (c * w))
        assert sy.cancel(hamiltonian + xi**c / c) == 0

    for d in range(1, 5):
        c = 5 - d
        r = c * k + 1
        for e in range(d + 1, 5):
            f = 5 - e
            s = f * k + 1
            if d + e == 5:
                # Formula (31), rather than its g-normalized form (32),
                # applies.  Its monomial coefficient cancels too.
                coefficient = sy.factor(
                    (r - 1) / c + (1 - s) / f
                )
            else:
                coefficient = cstar_monomial_coefficient(
                    d, r, e, s
                )
            assert coefficient == 0


def leading_form(
    equation: object,
    filtration_weights: tuple[int, ...],
) -> tuple[tuple[int, ...], object]:
    """Return the unique highest-filtration monomial and coefficient."""

    terms = equation.terms
    maximum = max(
        sum(a * b for a, b in zip(monomial, filtration_weights))
        for monomial in terms
    )
    selected = [
        (monomial, coefficient)
        for monomial, coefficient in terms.items()
        if sum(
            a * b
            for a, b in zip(monomial, filtration_weights)
        )
        == maximum
    ]
    assert len(selected) == 1
    return selected[0]


def verify_naive_initial_ideal_failure() -> None:
    for k in (1, 2):
        # Degrees in w of the seven canonical C-polynomials:
        # low d=1, high d=1, low d=2, high d=2, low d=3,
        # high d=3, high d=4.
        filtration = (
            0,
            4 * k + 1,
            1,
            3 * k + 1,
            1,
            2 * k + 1,
            k + 1,
        )
        prefix = [
            equation
            for equation in natural_consistency(k)
            if next(iter(equation.weighted_degrees())) <= 8
        ]
        assert len(prefix) == (18 if k == 1 else 19)
        pure_powers: list[int] = []
        for equation in prefix:
            weight_set = equation.weighted_degrees()
            assert len(weight_set) == 1
            weighted_degree = next(iter(weight_set))
            monomial, coefficient = leading_form(
                equation, filtration
            )
            assert coefficient
            assert monomial == (
                0,
                weighted_degree,
                0,
                0,
                0,
                0,
                0,
            )
            pure_powers.append(weighted_degree)
        assert min(pure_powers) == 4
        # Hence all leading forms generate exactly <X1^4>, whose radical
        # leaves the other six coordinate directions free.


def verify_darboux_lnd_countermodel() -> None:
    z, w, r, s = sy.symbols("z w r s", nonzero=True)
    r_zw = z**5 / (5 * w)
    s_zw = 1 / w
    # ds ^ dr coefficient in dz ^ dw.
    ds_dr = sy.det(
        sy.Matrix(
            [
                [sy.diff(s_zw, z), sy.diff(s_zw, w)],
                [sy.diff(r_zw, z), sy.diff(r_zw, w)],
            ]
        )
    )
    assert sy.simplify(ds_dr - z**4 / w**3) == 0

    # For ds^dr and i_X(ds^dr)=d(rs), X=r*d_r-s*d_s,
    # up to the harmless global sign convention.  It is not locally
    # nilpotent: every positive iterate on r equals r.
    def derivation(polynomial: sy.Expr) -> sy.Expr:
        return sy.expand(
            r * sy.diff(polynomial, r)
            - s * sy.diff(polynomial, s)
        )

    value = r
    for _ in range(12):
        value = derivation(value)
        assert value == r
    assert derivation(s) == -s

    # Nevertheless its time-t flow scales Laurent monomials and therefore
    # preserves every finite Laurent support.
    a, b = sy.symbols("a b", integer=True)
    eigenvalue = derivation(r**a * s**b) / (r**a * s**b)
    assert sy.simplify(eigenvalue - (a - b)) == 0


def verify_first_tail_formula() -> None:
    """The first possible high-high bracket is a normalized tail mismatch."""

    c, f, k = sy.symbols(
        "c f k", integer=True, positive=True
    )
    a, b = sy.symbols("a b")
    r = c * k + 1
    s = f * k + 1
    # C=w^r+a*w^(r-1), D=w^s+b*w^(s-1).
    # In the unnormalized potential bracket (31), the coefficient at
    # w^(r+s-1) is b/f-a/c.  The w^(r+s) coefficient vanishes.
    leading = sy.factor((r - 1) / c + (1 - s) / f)
    first_tail = sy.factor(
        a * ((r - 2) / c + (1 - s) / f)
        + b * ((r - 1) / c + (2 - s) / f)
    )
    assert leading == 0
    assert sy.simplify(first_tail - (b / f - a / c)) == 0


def verify_common_coordinate_tail_identity() -> None:
    """All high polynomial parts come from w*chi^c; only tails can bracket."""

    w, chi = sy.symbols("w chi", nonzero=True)
    logarithmic_derivative = sy.symbols("lambda")
    c, f = sy.symbols("c f", nonzero=True)
    c_full, d_full = w * chi**c, w * chi**f

    # Substitute w*chi'/chi=lambda.  This is the unnormalized bracket
    # in (31), before multiplication by -g*w.
    w_c_prime_minus_c = c_full * c * logarithmic_derivative
    d_minus_w_d_prime = -d_full * f * logarithmic_derivative
    full_bracket = sy.simplify(
        w_c_prime_minus_c * d_full / c
        + c_full * d_minus_w_d_prime / f
    )
    assert full_bracket == 0

    # The Belyi contact order N=5k+2 is farther than every high
    # polynomial window r_c=c*k+1, c=1,...,4.  Thus replacing the
    # square-root coordinate from U by the cube-root coordinate from V
    # does not change any polynomial part.
    k = sy.symbols("k", integer=True, positive=True)
    contact_order = 5 * k + 2
    for exponent in range(1, 5):
        window = exponent * k + 1
        assert sy.simplify(contact_order - window) == (
            (5 - exponent) * k + 1
        )


def main() -> None:
    verify_abelian_high_symbol()
    verify_first_tail_formula()
    verify_common_coordinate_tail_identity()
    verify_naive_initial_ideal_failure()
    verify_darboux_lnd_countermodel()
    print("verified universal abelian high principal symbol")
    print("verified first-tail bracket is b/f-a/c")
    print("verified all high polynomial parts share one formal coordinate")
    print("verified k=1,2 naive initial ideal is only <X1^4>")
    print("verified finite Laurent support does not imply an LND")


if __name__ == "__main__":
    main()
