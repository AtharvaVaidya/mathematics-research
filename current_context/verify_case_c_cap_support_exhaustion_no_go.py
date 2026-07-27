#!/usr/bin/env python3
"""Exact checks for the case-c cap support-exhaustion no-go theorem."""

from fractions import Fraction

import sympy as sp


def cross(origin, first, second):
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (
        first[1] - origin[1]
    ) * (second[0] - origin[0])


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


def twice_area(polygon):
    return abs(
        sum(
            polygon[i][0] * polygon[(i + 1) % len(polygon)][1]
            - polygon[(i + 1) % len(polygon)][0] * polygon[i][1]
            for i in range(len(polygon))
        )
    )


def lattice_points(polygon):
    def inside(point):
        signs = [
            cross(polygon[i], polygon[(i + 1) % len(polygon)], point)
            for i in range(len(polygon))
        ]
        return all(value >= 0 for value in signs) or all(value <= 0 for value in signs)

    max_x = max(point[0] for point in polygon)
    max_y = max(point[1] for point in polygon)
    return [
        (x, y)
        for x in range(max_x + 1)
        for y in range(max_y + 1)
        if inside((x, y))
    ]


P_vertices = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
Q_vertices = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
P_polygon = convex_hull(P_vertices)
Q_polygon = convex_hull(Q_vertices)
P_points = lattice_points(P_polygon)
Q_points = lattice_points(Q_polygon)
assert len(P_points) == 61
assert len(Q_points) == 125

minkowski = convex_hull(
    [(a + c, b + d) for a, b in P_polygon for c, d in Q_polygon]
)
mixed_volume = Fraction(
    twice_area(minkowski) - twice_area(P_polygon) - twice_area(Q_polygon), 2
)
assert mixed_volume == 141

# Both constrained cap faces have lattice points at normal distance one,
# so algebraically generic unprescribed coefficients supply a unit u-term.
assert max(x for x, _ in P_points) == 8
assert sorted(set(x for x, _ in P_points), reverse=True)[:2] == [8, 7]
assert max(x for x, _ in Q_points) == 12
assert sorted(set(x for x, _ in Q_points), reverse=True)[:2] == [12, 11]

P_diag_levels = sorted(set(y - x for x, y in P_points), reverse=True)
Q_diag_levels = sorted(set(y - x for x, y in Q_points), reverse=True)
assert P_diag_levels[:2] == [8, 7]
assert Q_diag_levels[:2] == [12, 11]

# Check compatibility and multiplicities of the prescribed faces.
y, z, s, lam, u7, v10 = sp.symbols(
    "y z s lam u7 v10", nonzero=True
)
P_vertical = sp.expand(u7 * y**14 * (1 - y / s) ** 2)
Q_vertical = sp.expand(v10 * y**21 * (1 - y / s) ** 3)
assert sp.Poly(P_vertical, y).coeff_monomial(y**14) == u7
assert sp.Poly(P_vertical, y).coeff_monomial(y**16) == u7 / s**2
assert sp.Poly(Q_vertical, y).coeff_monomial(y**21) == v10
assert sp.Poly(Q_vertical, y).coeff_monomial(y**24) == -v10 / s**3

P_diagonal = sp.expand((u7 / s**2) * y**8 * (z - lam) ** 8)
Q_diagonal = sp.expand((-v10 / s**3) * y**12 * (z - lam) ** 12)
assert sp.Poly(P_diagonal / y**8, z).coeff_monomial(z**8) == u7 / s**2
assert sp.Poly(Q_diagonal / y**12, z).coeff_monomial(z**12) == -v10 / s**3
assert sp.cancel(P_vertical / y**14 - (u7 / s**2) * (y - s) ** 2) == 0
assert sp.cancel(Q_vertical / y**21 + (v10 / s**3) * (y - s) ** 3) == 0
assert sp.cancel(P_diagonal / y**8 - (u7 / s**2) * (z - lam) ** 8) == 0
assert sp.cancel(Q_diagonal / y**12 + (v10 / s**3) * (z - lam) ** 12) == 0

# Generic transverse u-jets make the local intersection lengths the
# smaller face multiplicities.
u, v, alpha, beta, A1, B1 = sp.symbols(
    "u v alpha beta A1 B1", nonzero=True
)
vertical_remainder = sp.expand(
    (beta * v**3 + B1 * u) - (B1 / A1) * (alpha * v**2 + A1 * u)
)
diagonal_remainder = sp.expand(
    (beta * v**12 + B1 * u) - (B1 / A1) * (alpha * v**8 + A1 * u)
)
assert sp.Poly(vertical_remainder, v).as_dict()[(2,)] != 0
assert sp.Poly(diagonal_remainder, v).as_dict()[(8,)] != 0
vertical_loss = 2
diagonal_loss = 8
case_c_degree = mixed_volume - vertical_loss - diagonal_loss
assert case_c_degree == 131

# The outer rational map w*V^2/U^3 has degree 21.
outer_degree = max(1 + 2 * 10, 3 * 7)
assert outer_degree == 21
assert case_c_degree % outer_degree == 5

print("verified the 61/125 case-c lattice inventories")
print("verified mixed volume 141")
print("verified both prescribed cap faces and their shared-vertex coefficients")
print("verified generic boundary intersection losses 2 and 8")
print("verified generic constrained degree 131 versus endpoint degree 21")
print("RESULT: the actual case-c cap faces do not imply Darboux support exhaustion")
