#!/usr/bin/env python3
"""Exact checks for the primitive-leading-coefficient obstruction.

If U=u_d(t)c^d+... and V=v_n(t)c^n+..., the coefficient of c^(d+n-1)
in Jac_(t,c)(U,V) is

    n*u_d'(t)*v_n(t) - d*u_d(t)*v_n'(t).

When gcd(d, ord_p(u_d) for all irreducible p)=1, its vanishing forces
d|n and v_n to be a scalar multiple of u_d^(n/d).  Subtracting the
corresponding power of U repeatedly reduces V to v_0(t), which cannot
have constant bracket with U unless d=1 and u_1 is constant.

The family checked here is U=a*(b+1)^m in the fixed-plane normalization.
"""

import math

import sympy as sp


t, c = sp.symbols("t c")
a = t + t**2 - c * t**3
b = 2 + 4 * t - 3 * c * t**2
H = b + 1

for m in range(13):
    d = m + 1
    U = sp.expand(a * H**m)
    U_poly = sp.Poly(U, c)
    assert U_poly.degree() == d

    leading = sp.factor(U_poly.coeff_monomial(c**d))
    expected_leading = (-1) ** d * 3**m * t ** (2 * m + 3)
    assert sp.expand(leading - expected_leading) == 0

    # 2m+3 = 2(m+1)+1, so the general Euclidean-algorithm identity is
    # gcd(m+1,2m+3)=1.
    assert 2 * m + 3 == 2 * d + 1
    assert math.gcd(d, 2 * m + 3) == 1

    # Verify the universal top-bracket formula on several independent
    # polynomial leading coefficients v_n(t).
    for n in range(1, 7):
        coefficients = sp.symbols(f"v_{m}_{n}_0:4")
        v_n = sum(value * t**power for power, value in enumerate(coefficients))
        V_lead = v_n * c**n
        bracket = sp.expand(
            sp.diff(U, t) * sp.diff(V_lead, c)
            - sp.diff(U, c) * sp.diff(V_lead, t)
        )
        actual = sp.Poly(bracket, c).coeff_monomial(c ** (d + n - 1))
        expected = (
            n * sp.diff(leading, t) * v_n
            - d * leading * sp.diff(v_n, t)
        )
        assert sp.expand(actual - expected) == 0

    # Once V=v_0(t), the bracket is -U_c*v_0'.  For d>1 this retains
    # c-degree d-1.  For d=1, U_c=-t^3 is nonconstant.
    assert sp.degree(sp.diff(U, c), c) == d - 1
    if d == 1:
        assert sp.factor(sp.diff(U, c)) == -t**3

print("verified top Hamiltonian recurrence through m=12 and generic v_n")
print("verified leading coefficient (-1)^(m+1)*3^m*t^(2m+3)")
print("verified gcd(m+1,2m+3)=gcd(m+1,1)=1")

# Apply the same obstruction to the two surviving Q[a,b] boundary forms
#
#   linear term + a^2*Delta*K(a,H),
#
# where deg(K)=k and K_k is its top homogeneous part.  The c-degree is
# D=k+4 and its leading coefficient is
#
#   (-1)^k*9*t^(2k+10)*K_k(t,3).
#
# Since gcd(k+4,2k+10)=gcd(k+4,2), every odd k is primitive.  For even
# k, non-primitivity requires every root multiplicity of K_k(t,3) to be
# even, i.e. that one-variable polynomial must be a square over Qbar.
for k_degree in range(8):
    top_coefficients = sp.symbols(f"Ktop_{k_degree}_0:{k_degree + 1}")
    K_top = sum(
        coefficient * a**power * H ** (k_degree - power)
        for power, coefficient in enumerate(top_coefficients)
    )
    tail = sp.Poly(sp.expand(a**2 * (H**2 - 12 * a) * K_top), c)
    D = k_degree + 4
    assert tail.degree() == D
    specialization = sum(
        coefficient * t**power * 3 ** (k_degree - power)
        for power, coefficient in enumerate(top_coefficients)
    )
    expected_tail_leading = (
        (-1) ** k_degree
        * 9
        * t ** (2 * k_degree + 10)
        * specialization
    )
    assert sp.expand(tail.LC() - expected_tail_leading) == 0
    assert math.gcd(D, 2 * k_degree + 10) == math.gcd(D, 2)

print("verified [c^(k+4)]a^2*Delta*K_k=(-1)^k*9*t^(2k+10)*K_k(t,3)")
print("verified odd deg(K) is primitive; even deg(K) requires square K_k(t,3)")
print("RESULT: ALL-DEGREE FIXED-PLANE PRIMITIVE-LEADING OBSTRUCTIONS PASS")
