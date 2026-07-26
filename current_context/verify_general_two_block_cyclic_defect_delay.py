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
    predicted = ceil((e_value + 4) / 3)
    if predicted % 2 == 0:
        predicted += 1
    actual = next(
        defect
        for defect in range(2, e_value + 2)
        if forbidden_character_offsets(s_value, e_value, defect)
    )
    assert actual == predicted
    assert forbidden_character_offsets(s_value, e_value, actual) == [
        (e_value - actual) // 2
    ]


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

print("verified: cyclic characters constrain every forbidden coordinate")
print("verified: no uniform bounded-defect exclusion is possible")
print("verified: the first possible resonant defect grows linearly with E")
print("verified: direct exact bounded recurrences through defect seven")
print("verified: (g,E,s)=(14,9,5) survives six and fails by seven")
