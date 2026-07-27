#!/usr/bin/env python3
"""Exact checks for the cyclic two-block defect-delay theorem."""

from __future__ import annotations

from math import ceil

import sympy as sp


x, ell, u = sp.symbols("x ell u", nonzero=True)


def filtered_recurrence(
    s_value: int,
    e_value: int,
    final_defect: int,
) -> tuple[dict[int, list[sp.Expr]], list[sp.Expr], list[sp.Expr]]:
    """Return exact forbidden vectors and the constructed filtered jets."""
    g_value = s_value + e_value
    d = x**s_value * (x**e_value + ell)
    d1 = sp.diff(d, x)
    field = sp.QQ.frac_field(ell, u)
    A = u + 2 * d * d1
    B = 3 * d**2 * d1
    inverse_a = sp.invert(A, B, domain=field)
    p = [d**2 + u * x, -4 * d1 / (3 * u**2)]
    q = [d**3, 1 / u - 2 * d * d1 / u**2]
    forbidden: dict[int, list[sp.Expr]] = {}

    for defect in range(2, final_defect + 1):
        h = -sum(
            j * sp.diff(p[i], x) * q[j]
            - i * p[i] * sp.diff(q[j], x)
            for i in range(1, defect)
            for j in [defect - i]
        ) / defect
        q_new = sp.rem(
            sp.expand(inverse_a * h),
            B,
            x,
            domain=field,
        )
        p_new = sp.cancel((A * q_new - h) / B)
        assert p_new.is_polynomial(x)
        q_polynomial = sp.Poly(q_new, x)
        forbidden[defect] = [
            sp.factor(q_polynomial.coeff_monomial(x**power))
            for power in range(
                3 * g_value - defect + 1,
                3 * g_value - 1,
            )
        ]
        p.append(sp.factor(p_new))
        q.append(sp.factor(q_new))

    return forbidden, p, q


def forbidden_character_offsets(
    s_value: int,
    e_value: int,
    defect: int,
) -> list[int]:
    """Offsets in the forbidden interval matching the q_defect character."""
    assert (2 * s_value - 1) % e_value == 0
    return [
        offset
        for offset in range(1, defect - 1)
        if (offset - defect * (s_value - 1)) % e_value == 0
    ]


# The character identities used in the proof are exact modulo E.
for e_value in range(1, 40):
    for s_value in range(2, 60):
        if (2 * s_value - 1) % e_value:
            continue
        delta = s_value - 2
        for defect in range(0, 20):
            p_character = 1 + defect * delta
            q_character = 3 * s_value + defect * delta
            assert (
                (3 * s_value - 1) + p_character - q_character
            ) % e_value == 0
            if defect >= 2:
                for left_defect in range(1, defect):
                    right_defect = defect - left_defect
                    source_character = (
                        (1 + left_defect * delta)
                        - 1
                        + (3 * s_value + right_defect * delta)
                    )
                    assert (source_character - q_character) % e_value == 0


# For arbitrary K, the prescribed odd E has no matching forbidden
# character through K.  The first possible defect agrees with the
# closed formula in the note.
for cutoff in range(2, 80):
    e_value = 3 * cutoff - 3
    if e_value % 2 == 0:
        e_value += 1
    assert e_value > 3 * cutoff - 4
    s_value = (e_value + 1) // 2
    for defect in range(2, cutoff + 1):
        assert not forbidden_character_offsets(
            s_value,
            e_value,
            defect,
        )

for e_value in range(5, 80, 2):
    s_value = (e_value + 1) // 2
    chamber_index = (e_value - 1) // 6
    predicted = ceil((e_value + 4) / 3)
    if predicted % 2 == 0:
        predicted += 1
    assert predicted == 2 * chamber_index + 3
    actual = next(
        defect
        for defect in range(2, e_value + 2)
        if forbidden_character_offsets(s_value, e_value, defect)
    )
    assert actual == predicted
    assert forbidden_character_offsets(s_value, e_value, actual) == [
        (e_value - actual) // 2
    ]
    first_numerator_parameter_weight = (9 * actual - 13) // 2
    next_numerator_parameter_weight = (9 * (actual + 2) - 13) // 2
    assert first_numerator_parameter_weight == 9 * chamber_index + 7
    assert next_numerator_parameter_weight == 9 * chamber_index + 16
    assert (
        first_numerator_parameter_weight - 1
    ) // 3 == 3 * chamber_index + 2
    assert (
        next_numerator_parameter_weight - 1
    ) // 3 == 3 * chamber_index + 5


# Direct exact recurrence checks, independent of the congruence-only
# proof.  Each E is chosen above 3K-4.
for cutoff, e_value in ((4, 11), (5, 13), (6, 17), (7, 19)):
    s_value = (e_value + 1) // 2
    obstruction_vectors, p_values, q_values = filtered_recurrence(
        s_value,
        e_value,
        cutoff,
    )
    g_value = s_value + e_value
    for defect in range(2, cutoff + 1):
        assert all(value == 0 for value in obstruction_vectors[defect])
        assert sp.degree(p_values[defect], x) <= 2 * g_value - defect
        assert sp.degree(q_values[defect], x) <= 3 * g_value - defect


# The exact hostile endpoint (g,E,s)=(14,9,5).
vectors, _, _ = filtered_recurrence(5, 9, 7)
assert all(
    all(value == 0 for value in vectors[defect])
    for defect in (2, 3, 4, 6)
)
assert sum(value != 0 for value in vectors[5]) == 1
assert sum(value != 0 for value in vectors[7]) == 1

p5 = sp.Poly(
    186838225 * u**5
    + 23740768548 * u**4
    + 532637805132 * u**3
    + 4447199793231 * u**2
    + 15962498987778 * u
    + 23724081064404,
    u,
    domain=sp.QQ,
)
p7 = sp.Poly(
    3559879483055 * u**8
    + 1254368611253457 * u**7
    + 74129178578871600 * u**6
    + 1662884438039607177 * u**5
    + 18545694665345607285 * u**4
    + 115093632573725049054 * u**3
    + 411718849720612848108 * u**2
    + 810110778243003255744 * u
    + 713249706931339822992,
    u,
    domain=sp.QQ,
)

actual5 = next(value for value in vectors[5] if value != 0)
actual7 = next(value for value in vectors[7] if value != 0)
numerator5 = sp.Poly(
    sp.cancel(actual5.subs(ell, 1)).as_numer_denom()[0],
    u,
    domain=sp.QQ,
)
numerator7 = sp.Poly(
    sp.cancel(actual7.subs(ell, 1)).as_numer_denom()[0],
    u,
    domain=sp.QQ,
)
assert sp.monic(numerator5) == sp.monic(p5)
assert sp.monic(numerator7) == sp.monic(p7)
assert sp.gcd(p5, p7).degree() == 0
assert p5.TC() != 0

# The exceptional small chamber E=7 has its second permitted class
# at the even defect six, not at defect seven.
vectors7, _, _ = filtered_recurrence(4, 7, 6)
actual7_5 = [value for value in vectors7[5] if value != 0]
actual7_6 = [value for value in vectors7[6] if value != 0]
assert len(actual7_5) == 1
assert len(actual7_6) == 1
numerator7_5 = sp.Poly(
    sp.cancel(actual7_5[0].subs(ell, 1)).as_numer_denom()[0],
    u,
    domain=sp.QQ,
)
numerator7_6 = sp.Poly(
    sp.cancel(actual7_6[0].subs(ell, 1)).as_numer_denom()[0],
    u,
    domain=sp.QQ,
)
assert sp.gcd(numerator7_5, numerator7_6).degree() == 0
assert numerator7_5.TC() != 0
assert numerator7_6.TC() != 0

# Exact growing-chamber samples cited in the note.  E=9 is checked
# above and E=11 is checked by the companion resultant verifier.
for e_value in (13, 15, 17):
    s_value = (e_value + 1) // 2
    first_defect = ceil((e_value + 4) / 3)
    if first_defect % 2 == 0:
        first_defect += 1
    sample_vectors, _, _ = filtered_recurrence(
        s_value,
        e_value,
        first_defect + 2,
    )
    first_values = [
        value
        for value in sample_vectors[first_defect]
        if value != 0
    ]
    next_values = [
        value
        for value in sample_vectors[first_defect + 2]
        if value != 0
    ]
    assert len(first_values) == 1
    assert len(next_values) == 1
    first_polynomial = sp.Poly(
        sp.cancel(first_values[0].subs(ell, 1)).as_numer_denom()[0],
        u,
        domain=sp.QQ,
    )
    next_polynomial = sp.Poly(
        sp.cancel(next_values[0].subs(ell, 1)).as_numer_denom()[0],
        u,
        domain=sp.QQ,
    )
    assert sp.gcd(first_polynomial, next_polynomial).degree() == 0
    assert first_polynomial.TC() != 0
    assert next_polynomial.TC() != 0


# Symbolic quotient-ring audit for the all-order resonant equation.
E_symbol, X, Z = sp.symbols("E X Z", nonzero=True)
s_symbol = (E_symbol + 1) / 2
delta_symbol = (E_symbol - 3) / 2
g_symbol = (3 * E_symbol + 1) / 2
a0 = u + X * (X + ell) ** 2
b0 = X**2 * (X + ell) ** 3
a1 = -4 * (g_symbol * X + s_symbol * ell) / (3 * u**2)
b1 = (
    1 / u
    - 2 * X * (X + ell) * (g_symbol * X + s_symbol * ell) / u**2
)
omega = sp.factor(
    (
        (delta_symbol + 1) * a1
        + E_symbol * X * sp.diff(a1, X)
    )
    * b1
    - E_symbol * X * a1 * sp.diff(b1, X)
)

# Catalan expansion of Phi through Z^7, audited independently of the
# larger quotient-polynomial coefficients.
omega_scalar = sp.symbols("omega")
phi = sum(
    (-1) ** (degree - 1)
    * sp.catalan(degree - 1)
    * omega_scalar ** (degree - 1)
    * Z**degree
    / 2 ** (degree - 1)
    for degree in range(1, 8)
)
assert all(
    sp.factor(
        sp.expand(
            phi + omega_scalar * phi**2 / 2 - Z
        ).coeff(Z, degree)
    )
    == 0
    for degree in range(1, 8)
)

# If Phi+omega*Phi^2/2=Z, then Phi_Z=(1+omega*Phi)^-1.
# The quotient PDE numerator is affine in Phi; these are its exact
# constant and linear coefficients.
base_constant = sp.factor(
    E_symbol
    * X
    * (
        sp.diff(a0, X) * b1
        - a1 * sp.diff(b0, X)
    )
    + a0 * b1
    + delta_symbol * b0 * a1
)
base_linear = sp.factor(
    E_symbol
    * X
    * (
        sp.diff(a1, X) * b1
        - a1 * sp.diff(b1, X)
    )
    + (delta_symbol + 1) * a1 * b1
)
assert sp.factor(base_constant - 1) == 0
assert sp.factor(base_linear - omega) == 0

# The quotient curvature is the physical straight-tube curvature,
# and it cannot vanish because its (d')^3 term has strictly largest
# x-degree.
for e_value in (5, 9, 17):
    s_value = (e_value + 1) // 2
    delta_value = (e_value - 3) // 2
    d_value = x**s_value * (x**e_value + ell)
    omega_value = omega.subs(
        {
            E_symbol: e_value,
            X: x**e_value,
        }
    )
    assert sp.factor(
        x**delta_value * omega_value
        + 4
        * (
            u * sp.diff(d_value, x, 2)
            + 2 * sp.diff(d_value, x) ** 3
        )
        / (3 * u**4)
    ) == 0

# The Laurent windows are exactly equivalent to the original
# reciprocal degree and nonnegative-exponent bounds.
for e_value in range(5, 40, 2):
    delta_value = (e_value - 3) // 2
    g_value = (3 * e_value + 1) // 2
    for defect in range(0, min(15, 2 * g_value) + 1):
        a_min = ceil(-(1 + defect * delta_value) / e_value)
        a_max = (3 * e_value - defect - defect * delta_value) // e_value
        for exponent in range(a_min, a_max + 1):
            original_exponent = 1 + defect * delta_value + exponent * e_value
            assert 0 <= original_exponent <= 2 * g_value - defect
        assert 1 + defect * delta_value + (a_min - 1) * e_value < 0
        assert (
            1 + defect * delta_value + (a_max + 1) * e_value
            > 2 * g_value - defect
        )

        b_min = ceil(-((defect - 1) * delta_value) / e_value)
        b_max = (
            (10 - defect) * e_value + defect
        ) // (2 * e_value)
        for exponent in range(b_min, b_max + 1):
            original_exponent = (
                (defect - 1) * delta_value + exponent * e_value
            )
            assert 0 <= original_exponent <= 3 * g_value - defect
        assert (
            (defect - 1) * delta_value + (b_min - 1) * e_value < 0
        )
        assert (
            (defect - 1) * delta_value + (b_max + 1) * e_value
            > 3 * g_value - defect
        )


def negative_continued_fraction(
    numerator: int,
    denominator: int,
) -> list[int]:
    """Return the Hirzebruch--Jung expansion numerator/denominator."""
    output: list[int] = []
    while denominator:
        coefficient = (numerator + denominator - 1) // denominator
        output.append(coefficient)
        numerator, denominator = (
            denominator,
            coefficient * denominator - numerator,
        )
    return output


# Exact quotient singularity strings and special-fiber multiplicities.
for e_value in range(5, 100, 2):
    if e_value % 3:
        quotient_order = e_value
        quotient_weight = (e_value + 3) // 2
        if e_value % 6 == 1:
            expected_chain = [2, (e_value - 1) // 6 + 1, 3]
        else:
            expected_chain = [2, (e_value - 5) // 6 + 2, 2, 2]
    else:
        quotient_order = e_value // 3
        quotient_weight = (quotient_order + 1) // 2
        expected_chain = [2, (quotient_order + 1) // 2]
    assert sp.gcd(quotient_order, quotient_weight) == 1
    assert negative_continued_fraction(
        quotient_order,
        quotient_weight,
    ) == expected_chain
    inverse_weight = pow(quotient_weight, -1, quotient_order)
    multiplicity_zero = quotient_order // sp.gcd(
        quotient_order,
        quotient_weight - 1,
    )
    multiplicity_infinity = quotient_order // sp.gcd(
        quotient_order,
        inverse_weight - 1,
    )
    assert multiplicity_zero == quotient_order
    assert multiplicity_infinity == quotient_order

print("verified: cyclic characters constrain every forbidden coordinate")
print("verified: no uniform bounded-defect exclusion is possible")
print("verified: the first possible resonant defect grows linearly with E")
print("verified: direct exact bounded recurrences through defect seven")
print("verified: (g,E,s)=(14,9,5) survives six and fails by seven")
print("verified: the exceptional E=7 chamber fails by defects five/six")
print("verified: first-two-class coprimality at E=13,15,17")
print("verified: resonant quotient PDE and Catalan generating solution")
print("verified: exact all-order reciprocal Laurent windows")
print("verified: short Hirzebruch--Jung strings and fiber multiplicities")
