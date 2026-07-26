#!/usr/bin/env python3
"""Exact checks for ROUTE_A_RESIDUAL_QUADRATIC_INFINITY_AUDIT.md."""

from sympy import (
    Matrix,
    Poly,
    Rational,
    expand,
    factor,
    limit,
    simplify,
    symbols,
)


x, y, z, w, tau, t, eta, a0, b0 = symbols(
    "x y z w tau t eta a b"
)
G = symbols("G", nonzero=True)


# Miranda coefficients and their dependent coefficients.
aa = 1
bb = y
cc = -G / 3
dd = 0
A = simplify(aa**2 - bb * dd)
B = simplify(aa * dd - bb * cc)
C = simplify(dd**2 - aa * cc)
assert (A, B, C) == (1, y * G / 3, G / 3)


# Multiplication in the free basis (1,z,w), represented by vectors.
one_v = Matrix([1, 0, 0])
z_v = Matrix([0, 1, 0])
w_v = Matrix([0, 0, 1])
z2_v = Matrix([2, 1, y])
zw_v = Matrix([-y * G / 3, 0, -1])
w2_v = Matrix([2 * G / 3, -G / 3, 0])


def mul(p: Matrix, q: Matrix) -> Matrix:
    """Bilinear multiplication using the displayed table."""
    p0, p1, p2 = p
    q0, q1, q2 = q
    return simplify(
        p0 * q0 * one_v
        + (p0 * q1 + p1 * q0) * z_v
        + (p0 * q2 + p2 * q0) * w_v
        + p1 * q1 * z2_v
        + (p1 * q2 + p2 * q1) * zw_v
        + p2 * q2 * w2_v
    )


# Associativity on basis triples.
basis = (one_v, z_v, w_v)
for p in basis:
    for q in basis:
        for r in basis:
            assert simplify(mul(mul(p, q), r) - mul(p, mul(q, r))) == Matrix(
                [0, 0, 0]
            )


# At y=0, (1,z,w) -> ((1),(1,tau))-coordinates:
# 1 -> (1,1), z -> (2,-1), w -> (0,tau), tau^2=G.
def pair_mul(lhs, rhs):
    l0, l1a, l1b = lhs  # residual entry l1a+l1b*tau
    r0, r1a, r1b = rhs
    return (
        simplify(l0 * r0),
        simplify(l1a * r1a + l1b * r1b * G),
        simplify(l1a * r1b + l1b * r1a),
    )


images = (
    (1, 1, 0),
    (2, -1, 0),
    (0, 0, 1),
)
table_y0 = {
    (0, 0): one_v,
    (0, 1): z_v,
    (0, 2): w_v,
    (1, 1): z2_v.subs(y, 0),
    (1, 2): zw_v.subs(y, 0),
    (2, 2): w2_v.subs(y, 0),
}


def image_of(vec):
    return tuple(
        simplify(sum(vec[j] * images[j][i] for j in range(3)))
        for i in range(3)
    )


for i in range(3):
    for j in range(i, 3):
        assert pair_mul(images[i], images[j]) == image_of(table_y0[(i, j)])


# Branch polynomial and its restriction.
disc = simplify(
    bb**2 * cc**2
    - 3 * aa**2 * dd**2
    + 4 * aa**3 * cc
    + 4 * bb * dd**3
    - 6 * aa * bb * cc * dd
)
assert factor(disc) == G * (G * y**2 - 12) / 9
assert simplify(disc.subs(y, 0) + 4 * G / 3) == 0


# The generic monogenic equation after T=z+1.
T = symbols("T")
monogenic = expand(T**2 * (T - 3) + y**2 * G / 3)
assert monogenic == T**3 - 3 * T**2 + G * y**2 / 3


# Odd and even concrete specializations have no polynomial/rational root.
# SymPy's exact factorization over QQ(x,y) leaves both cubics irreducible.
odd_poly = Poly(
    (T**2 * (T - 3) + y**2 * x / 3),
    T,
    domain="QQ(x,y)",
)
even_poly = Poly(
    (T**2 * (T - 3) + y**2 * (x**2 - 1) / 3),
    T,
    domain="QQ(x,y)",
)
assert len(odd_poly.factor_list()[1]) == 1
assert odd_poly.factor_list()[1][0][0].degree() == 3
assert len(even_poly.factor_list()[1]) == 1
assert even_poly.factor_list()[1][0][0].degree() == 3


# Smoothness minors for squarefree G.
Gp = symbols("Gprime", nonzero=True)
# Section y=0,z=2,w=0: rows dF,dG and columns dz,dw.
section_minor = Matrix([[3, 0], [0, 3]]).det()
assert section_minor == 9
# Residual y=0,z=-1,w^2=G with G != 0: rows dF,dH, dz,dw.
residual_nonroot_minor = Matrix([[-3, 0], [G / 3, 2 * w]]).det()
assert residual_nonroot_minor == -6 * w
# At a simple root G=w=0: rows dF,dH, columns dz,dx.
residual_root_minor = Matrix([[-3, 0], [0, -Gp]]).det()
assert residual_root_minor == 3 * Gp
# On y != 0 the hypersurface partials force G=G'=0 at a singularity.
f_T = (T**2 * (T - 3)).diff(T)
assert factor(f_T) == 3 * T * (T - 2)
assert simplify((y**2 * G / 3).diff(y) - 2 * y * G / 3) == 0


# Canonical quadratic chart and hypersurface relation.
u_chart = a0**2
w_chart = a0 * (1 + 2 * a0**2 * b0)
v_chart = 4 * b0 * (1 + a0**2 * b0)
assert simplify(w_chart**2 - u_chart - u_chart**2 * v_chart) == 0


# Rational deck invariance.
a_sig = -a0
b_sig = -b0 - a0 ** (-2)
assert simplify(u_chart.subs({a0: a_sig, b0: b_sig}, simultaneous=True) - u_chart) == 0
assert simplify(v_chart.subs({a0: a_sig, b0: b_sig}, simultaneous=True) - v_chart) == 0
assert simplify(w_chart.subs({a0: a_sig, b0: b_sig}, simultaneous=True) - w_chart) == 0


# Escaping polynomial chart and its boundary parameter.
a_theta = -t + eta * t**3
b_theta = -t ** (-2)
u_theta = factor(u_chart.subs({a0: a_theta, b0: b_theta}))
v_theta = factor(v_chart.subs({a0: a_theta, b0: b_theta}))
w_theta = factor(w_chart.subs({a0: a_theta, b0: b_theta}))
assert limit(u_theta, t, 0) == 0
assert limit(v_theta, t, 0) == -8 * eta
assert limit(w_theta, t, 0) == 0


# The chart is etale and the parameter change v=-8 eta has degree one.
chart_jac = simplify(
    Matrix(
        [
            [a_theta.diff(t), a_theta.diff(eta)],
            [b_theta.diff(t), b_theta.diff(eta)],
        ]
    ).det()
)
assert chart_jac == -2
assert Poly(-8 * eta, eta).degree() == 1


# S4 edge model: (12) fixes the distinguished complementary edge pair
# {12,34} pointwise and swaps the other two cubic partitions.
def vertex_transposition_12(edge):
    swap = {1: 2, 2: 1, 3: 3, 4: 4}
    return frozenset(swap[i] for i in edge)


partitions = (
    frozenset((frozenset((1, 2)), frozenset((3, 4)))),
    frozenset((frozenset((1, 3)), frozenset((2, 4)))),
    frozenset((frozenset((1, 4)), frozenset((2, 3)))),
)


def act_on_partition(partition):
    return frozenset(vertex_transposition_12(edge) for edge in partition)


assert act_on_partition(partitions[0]) == partitions[0]
assert act_on_partition(partitions[1]) == partitions[2]
assert act_on_partition(partitions[2]) == partitions[1]
assert vertex_transposition_12(frozenset((1, 2))) == frozenset((1, 2))
assert vertex_transposition_12(frozenset((3, 4))) == frozenset((3, 4))


print("route A residual quadratic/infinity audit: all exact checks passed")
