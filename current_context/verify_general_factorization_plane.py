#!/usr/bin/env python3
"""Exact checks for GENERAL_FACTORIZATION_PLANE_NO_GO.md."""

import sympy as sp


z, w, p, q = sp.symbols("z w p q")


def verify_wronskian_determinant(d: int) -> None:
    """Verify (d+1) det(M)=W(F,G)(-q,p) in degree d+1."""

    n = d + 1
    f = sp.symbols(f"f0:{n + 1}")
    g = sp.symbols(f"g0:{n + 1}")

    # Columns are a_0,...,a_d,s,t.  The first n+1 rows encode
    # p*a_k+q*a_{k-1}-s*f_k-t*g_k, and the last row is the resultant.
    rows = []
    for k in range(n + 1):
        row = [sp.Integer(0)] * (d + 3)
        if k <= d:
            row[k] = p
        if k >= 1:
            row[k - 1] += q
        row[d + 1] = -f[k]
        row[d + 2] = -g[k]
        rows.append(row)

    resultant_row = [
        (-q) ** (d - i) * p**i for i in range(d + 1)
    ] + [sp.Integer(0), sp.Integer(0)]
    rows.append(resultant_row)
    matrix = sp.Matrix(rows)

    F = sum(f[k] * z ** (n - k) * w**k for k in range(n + 1))
    G = sum(g[k] * z ** (n - k) * w**k for k in range(n + 1))
    wronskian = sp.diff(F, z) * sp.diff(G, w) - sp.diff(F, w) * sp.diff(G, z)
    evaluated = sp.expand(wronskian.subs({z: -q, w: p}))

    assert sp.expand((d + 1) * matrix.det() - evaluated) == 0
    print(f"verified: degree {d + 1} Wronskian determinant")


for complementary_degree in range(2, 7):
    verify_wronskian_determinant(complementary_degree)


# Verify the exact homogeneous common-factor identity
# m*W(Rf,Rg)=(m+r)*R^2*W(f,g) with fully generic binary forms.
for r_degree, reduced_degree in ((1, 2), (2, 2), (3, 1), (3, 3)):
    r_coeff = sp.symbols(f"r{r_degree}_0:{r_degree + 1}")
    f_coeff = sp.symbols(f"ff{r_degree}_{reduced_degree}_0:{reduced_degree + 1}")
    g_coeff = sp.symbols(f"gg{r_degree}_{reduced_degree}_0:{reduced_degree + 1}")
    R = sum(
        r_coeff[i] * z ** (r_degree - i) * w**i
        for i in range(r_degree + 1)
    )
    f_form = sum(
        f_coeff[i] * z ** (reduced_degree - i) * w**i
        for i in range(reduced_degree + 1)
    )
    g_form = sum(
        g_coeff[i] * z ** (reduced_degree - i) * w**i
        for i in range(reduced_degree + 1)
    )

    def W(left, right):
        return sp.diff(left, z) * sp.diff(right, w) - sp.diff(
            left, w
        ) * sp.diff(right, z)

    assert sp.expand(
        reduced_degree * W(R * f_form, R * g_form)
        - (reduced_degree + r_degree) * R**2 * W(f_form, g_form)
    ) == 0

print("verified: homogeneous common-factor Wronskian identity")


# Verify the p != 0 recurrence and resultant reconstruction in the
# exceptional pencil for several arbitrary degrees.
for d in range(2, 8):
    fixed = sp.symbols(f"c{d}_0:{d}")
    coeff = []
    for i in range(d):
        if i == 0:
            coeff.append(fixed[0] / p)
        else:
            coeff.append(sp.factor((fixed[i] - q * coeff[i - 1]) / p))

    partial_resultant = sum(
        coeff[i] * (-q) ** (d - i) * p**i for i in range(d)
    )
    a_d = sp.factor((1 - partial_resultant) / p**d)
    all_coeff = coeff + [a_d]

    for k in range(d):
        previous = all_coeff[k - 1] if k else 0
        assert sp.factor(p * all_coeff[k] + q * previous - fixed[k]) == 0

    resultant = sum(
        all_coeff[i] * (-q) ** (d - i) * p**i for i in range(d + 1)
    )
    assert sp.factor(resultant - 1) == 0

print("verified: exceptional-pencil Laurent reconstruction")


# On the flat p=0 branch the final two target coordinates are diagonal
# linear coordinates on the two free coefficients.
q_flat, a_penultimate, a_last = sp.symbols(
    "q_flat a_penultimate a_last", nonzero=True
)
A_d_flat = q_flat * a_penultimate
A_last_flat = q_flat * a_last
flat_jacobian = sp.Matrix(
    [
        [sp.diff(A_d_flat, a_penultimate), sp.diff(A_d_flat, a_last)],
        [sp.diff(A_last_flat, a_penultimate), sp.diff(A_last_flat, a_last)],
    ]
).det()
assert sp.factor(flat_jacobian - q_flat**2) == 0
print("verified: flat exceptional component maps by a linear automorphism")

print("all general factorization-plane checks passed")
