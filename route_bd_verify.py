#!/usr/bin/env python3
"""Exact, dependency-free checks for the Route B/D memo.

This does not solve the full (72,108) coefficient variety.  It reconstructs the
two finite supports in Guccione--Guccione--Horruitiner--Valqui, Proposition 4.3,
counts the resulting bilinear equations, and verifies a five-row obstruction on
one forced-edge degeneration.

All arithmetic is over Z[t], represented as dictionaries exponent -> coefficient.
"""

from collections import defaultdict
from math import comb


AB_P_VERTICES = ((0, 0), (1, 0), (8, 14), (8, 16))
AB_Q_VERTICES = ((0, 0), (2, 1), (12, 21), (12, 24))
C_P_VERTICES = AB_P_VERTICES + ((0, 8),)
C_Q_VERTICES = AB_Q_VERTICES + ((0, 12),)


def cross(origin, point, query):
    return (
        (point[0] - origin[0]) * (query[1] - origin[1])
        - (point[1] - origin[1]) * (query[0] - origin[0])
    )


def convex_hull(points):
    points = sorted(set(points))
    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def lattice_points(vertices):
    hull = convex_hull(vertices)

    def inside(point):
        return all(
            cross(hull[index], hull[(index + 1) % len(hull)], point) >= 0
            for index in range(len(hull))
        )

    return tuple(
        (x_degree, y_degree)
        for x_degree in range(max(point[0] for point in vertices) + 1)
        for y_degree in range(max(point[1] for point in vertices) + 1)
        if inside((x_degree, y_degree))
    )


def equation_inventory(p_support, q_support):
    """Return output rows and nonzero bilinear terms in Jac(P,Q)."""
    rows = defaultdict(list)
    for u, v in p_support:
        for i, j in q_support:
            determinant = u * j - v * i
            if determinant:
                rows[(u + i - 1, v + j - 1)].append(
                    ((u, v), (i, j), determinant)
                )
    return rows


def poly_add(left, right):
    result = dict(left)
    for exponent, coefficient in right.items():
        result[exponent] = result.get(exponent, 0) + coefficient
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient
    }


def poly_multiply(left, right):
    result = {}
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = left_exponent + right_exponent
            result[exponent] = (
                result.get(exponent, 0)
                + left_coefficient * right_coefficient
            )
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient
    }


def poly_scale(polynomial, scalar):
    return {
        exponent: scalar * coefficient
        for exponent, coefficient in polynomial.items()
        if scalar * coefficient
    }


def bracket_monomial(p_point, p_coefficient, q_point):
    """Jac(a*x^u*y^v, x^i*y^j), coefficient and output row."""
    u, v = p_point
    i, j = q_point
    determinant = u * j - v * i
    return (
        (u + i - 1, v + j - 1),
        poly_scale(p_coefficient, determinant),
    )


def certificate_checks():
    # P_t = x + y^8 (xy-t)^8.
    p_coefficients = {(1, 0): {0: 1}}
    for u in range(9):
        # binom(8,u) (xy)^u (-t)^(8-u) y^8
        p_coefficients[(u, 8 + u)] = {
            8 - u: comb(8, u) * ((-1) ** (8 - u))
        }

    # L_t is supported on five coefficient rows.
    certificate = {
        (2, 0): {0: 576},
        (9, 16): {0: 24},
        (16, 32): {0: 51},
        (17, 33): {1: 612},
        (18, 34): {2: 4148},
    }

    q_support = lattice_points(C_Q_VERTICES)
    nonzero_residuals = {}
    for q_point in q_support:
        pairing = {}
        for p_point, p_coefficient in p_coefficients.items():
            output_row, bracket_coefficient = bracket_monomial(
                p_point, p_coefficient, q_point
            )
            if output_row in certificate:
                pairing = poly_add(
                    pairing,
                    poly_multiply(certificate[output_row], bracket_coefficient),
                )
        if pairing:
            nonzero_residuals[q_point] = pairing

    # The target is x^2, so L_t(x^2) is the coefficient at row (2,0).
    target_pairing = certificate[(2, 0)]

    # The certificate is not universal in all P-coefficients.  For the
    # perturbation eps*x*y and Q-monomial x^9*y^16, the affected output row is
    # (9,16), and the pairing is 24*(16-9)=168.
    perturbation_row, perturbation_bracket = bracket_monomial(
        (1, 1), {0: 1}, (9, 16)
    )
    perturbation_pairing = poly_multiply(
        certificate[perturbation_row], perturbation_bracket
    )

    assert not nonzero_residuals
    assert target_pairing == {0: 576}
    assert perturbation_pairing == {0: 168}
    return certificate, target_pairing, perturbation_pairing


def main():
    supports = {
        "a/b": (
            lattice_points(AB_P_VERTICES),
            lattice_points(AB_Q_VERTICES),
        ),
        "c": (
            lattice_points(C_P_VERTICES),
            lattice_points(C_Q_VERTICES),
        ),
    }

    print("Route B/D exact support inventory")
    for name, (p_support, q_support) in supports.items():
        rows = equation_inventory(p_support, q_support)
        term_count = sum(len(terms) for terms in rows.values())
        assert (2, 0) in rows
        assert all(x_degree - y_degree <= 2 for x_degree, y_degree in rows)
        print(
            f"case {name}: |S_P|={len(p_support)}, |S_Q|={len(q_support)}, "
            f"Jacobian rows={len(rows)}, nonzero bilinear terms={term_count}"
        )

    assert tuple(map(len, supports["a/b"])) == (25, 47)
    assert tuple(map(len, supports["c"])) == (61, 125)
    assert len(equation_inventory(*supports["a/b"])) == 92
    assert len(equation_inventory(*supports["c"])) == 302

    certificate, target_pairing, perturbation_pairing = certificate_checks()
    rendered = ", ".join(
        f"{row}:{polynomial}" for row, polynomial in certificate.items()
    )
    print(f"five-row certificate L_t: {rendered}")
    print(
        "verified for all 125 Q-monomials: "
        "L_t(Jac(x+y^8(xy-t)^8,Q))=0 in Z[t]"
    )
    print(f"target pairing L_t(x^2)={target_pairing[0]}")
    print(
        "generality gap witness: adding eps*x*y gives coefficient "
        f"{perturbation_pairing[0]}*eps on Q-monomial x^9*y^16"
    )
    print("RESULT: ALL EXACT CHECKS PASS")


if __name__ == "__main__":
    main()
