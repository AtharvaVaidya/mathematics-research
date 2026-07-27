#!/usr/bin/env python3
"""Exact checks for the finite-flat triple non-Gorenstein audit.

The script verifies Miranda's multiplication identities, the explicit
normal S3 countermodel, its branch discriminant, and its singular locus.
"""

from __future__ import annotations

import shutil
import subprocess

import sympy as sp


def miranda_associativity() -> None:
    a, b, c, d = sp.symbols("a b c d")
    A = a**2 - b * d
    B = a * d - b * c
    C = d**2 - a * c

    one = sp.Matrix([1, 0, 0])
    z = sp.Matrix([0, 1, 0])
    w = sp.Matrix([0, 0, 1])
    z2 = sp.Matrix([2 * A, a, b])
    zw = sp.Matrix([-B, -d, -a])
    w2 = sp.Matrix([2 * C, c, d])

    def multiply(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
        result = sp.zeros(3, 1)
        basis = (one, z, w)
        table = (
            (one, z, w),
            (z, z2, zw),
            (w, zw, w2),
        )
        for i in range(3):
            for j in range(3):
                result += left[i] * right[j] * table[i][j]
        return sp.simplify(result)

    for left in (one, z, w):
        for middle in (one, z, w):
            for right in (one, z, w):
                lhs = multiply(multiply(left, middle), right)
                rhs = multiply(left, multiply(middle, right))
                assert sp.simplify(lhs - rhs) == sp.zeros(3, 1)

    # At a=b=c=d=0, the trace-zero maximal ideal squares to zero.
    zero_substitution = {a: 0, b: 0, c: 0, d: 0}
    assert z2.subs(zero_substitution) == sp.zeros(3, 1)
    assert zw.subs(zero_substitution) == sp.zeros(3, 1)
    assert w2.subs(zero_substitution) == sp.zeros(3, 1)


def explicit_countermodel() -> None:
    x, y, z, w, t, Z = sp.symbols("x y z w t Z")
    a = x
    b = y
    c = x + y
    d = x + 2 * y
    A = sp.expand(a**2 - b * d)
    B = sp.expand(a * d - b * c)
    C = sp.expand(d**2 - a * c)

    assert A == x**2 - x * y - 2 * y**2
    assert B == x**2 + x * y - y**2
    assert C == 3 * x * y + 4 * y**2

    discriminant = sp.factor(B**2 - 4 * A * C)
    expected = (
        (x**2 - 9 * x * y - 11 * y**2)
        * (x**2 - x * y - 3 * y**2)
    )
    assert sp.expand(discriminant - expected) == 0
    assert sp.gcd(
        sp.gcd(discriminant, sp.diff(discriminant, x)),
        sp.diff(discriminant, y),
    ) == 1

    cubic = sp.expand(
        z**3
        + 3 * (b * d - a**2) * z
        + (3 * a * b * d - 2 * a**3 - b**2 * c)
    )
    dehomogenized = sp.expand(cubic.subs({x: t, y: 1, z: Z}))
    expected_cubic = (
        Z**3
        + (-3 * t**2 + 3 * t + 6) * Z
        - 2 * t**3
        + 3 * t**2
        + 5 * t
        - 1
    )
    assert sp.expand(dehomogenized - expected_cubic) == 0

    alpha, beta = sp.symbols("alpha beta")
    root_test = sp.Poly(
        sp.expand(expected_cubic.subs(Z, alpha * t + beta)),
        t,
    )
    coefficient_equations = root_test.all_coeffs()
    assert sp.solve(
        coefficient_equations,
        [alpha, beta],
        dict=True,
    ) == []

    # In the alpha=-1 branch, the remaining two equations have no
    # common beta root; this records the exact resultant certificate.
    beta_third = -3 * beta**2 + 3 * beta - 1
    beta_fourth = beta**3 + 6 * beta - 1
    assert sp.resultant(beta_third, beta_fourth, beta) == -208


def singular_normality_certificate() -> None:
    singular = shutil.which("Singular")
    if singular is None:
        raise RuntimeError("Singular executable is required for this certificate")

    program = r'''
LIB "primdec.lib";
ring r=0,(x,y,z,w),dp;
poly a=x;
poly b=y;
poly c=x+y;
poly d=x+2y;
poly aa=a^2-b*d;
poly bb=a*d-b*c;
poly cc=d^2-a*c;
ideal I=
  z^2-a*z-b*w-2*aa,
  z*w+d*z+a*w+bb,
  w^2-c*z-d*w-2*cc;
list L=minAssGTZ(I);
"MINASS",size(L);
"DIM",dim(std(I));
"HILBERT";
hilb(std(I));
matrix J=jacob(I);
ideal SI=I+minor(J,2);
"RADICAL_SINGULAR";
std(radical(SI));
'''
    completed = subprocess.run(
        [singular, "-q"],
        input=program,
        text=True,
        check=True,
        capture_output=True,
    )
    output = completed.stdout
    assert "MINASS 1" in output
    assert "DIM 2" in output
    assert "(2t+1) / (1-t)^2" in output
    radical_block = output.split("RADICAL_SINGULAR", maxsplit=1)[1]
    for generator in ("_[1]=w", "_[2]=z", "_[3]=y", "_[4]=x"):
        assert generator in radical_block


def topology_counts() -> None:
    # Four affine lines through one point.
    chi_four_lines = 4 - 3
    transitive_points = 1
    assert chi_four_lines == 1
    assert 4 + chi_four_lines + transitive_points == 6

    # One irreducible rational curve with four normalization points
    # identified at an ordinary quadruple point.
    chi_irreducible_quadruple = 1 - (4 - 1)
    assert chi_irreducible_quadruple == -2
    assert 1 + chi_irreducible_quadruple + transitive_points == 0
    boundary_components = 2 - chi_irreducible_quadruple - transitive_points
    assert boundary_components == 3

    # Four ordinary-quadruple branch meridians can have product one
    # and still generate S3.
    identity = (0, 1, 2)
    transposition_12 = (1, 0, 2)
    transposition_23 = (0, 2, 1)

    def compose(
        left: tuple[int, ...],
        right: tuple[int, ...],
    ) -> tuple[int, ...]:
        return tuple(left[right[index]] for index in range(3))

    product = identity
    for generator in (
        transposition_12,
        transposition_12,
        transposition_23,
        transposition_23,
    ):
        product = compose(product, generator)
    assert product == identity

    generated = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in (transposition_12, transposition_23):
            candidate = compose(current, generator)
            if candidate not in generated:
                generated.add(candidate)
                frontier.append(candidate)
    assert len(generated) == 6


def main() -> None:
    miranda_associativity()
    explicit_countermodel()
    singular_normality_certificate()
    topology_counts()
    print("verified: Miranda rank-three multiplication is associative")
    print("verified: non-Gorenstein fiber is k[z,w]/(z,w)^2")
    print("verified: explicit cubic field is irreducible with nonsquare branch")
    print("verified: branch is four distinct lines and generic group is S3")
    print("verified: total space is the normal twisted-cubic cone")
    print("verified: only singular point is the non-Gorenstein vertex")
    print("verified: local non-Gorenstein topology has compatible global counts")
    print("RESULT: normal S3 triple covers can have non-Gorenstein points")


if __name__ == "__main__":
    main()
