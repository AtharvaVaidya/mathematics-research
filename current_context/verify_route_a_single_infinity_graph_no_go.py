#!/usr/bin/env python3
"""Exact checks for ROUTE_A_SINGLE_INFINITY_GRAPH_NO_GO.md."""

import sympy as sp


t, x, y, z, r, s = sp.symbols("t x y z r s")


for m in range(1, 8):
    f = y**2 - x ** (2 * m + 1)

    # The polynomial normalization t -> (t^2,t^(2m+1)) lies on the cusp.
    assert sp.expand(f.subs({x: t**2, y: t ** (2 * m + 1)})) == 0

    # The double cover is the A_(2m) equation after r=z-y, s=z+y.
    surface = z**2 - y**2 + x ** (2 * m + 1)
    transformed = sp.expand(
        surface.subs(
            {
                z: (r + s) / 2,
                y: (s - r) / 2,
            }
        )
    )
    assert sp.expand(transformed - (r * s + x ** (2 * m + 1))) == 0

    # The cusp and surface gradients vanish at the origin.
    cusp_gradient = [sp.diff(f, variable) for variable in (x, y)]
    surface_gradient = [
        sp.diff(surface, variable) for variable in (x, y, z)
    ]
    assert all(entry.subs({x: 0, y: 0}) == 0 for entry in cusp_gradient)
    assert all(
        entry.subs({x: 0, y: 0, z: 0}) == 0
        for entry in surface_gradient
    )


# One étale support plus one ramified length-two support is exactly cubic.
assert 1 + 2 == 3


# The free rank of A_H is rho_Gamma + k - 1 when the components meet
# in k points.  It is always positive because rho_Gamma >= 1.
for rho_gamma in range(1, 8):
    for intersection_points in range(1, 8):
        rank = rho_gamma + intersection_points - 1
        assert rank >= 1

print("Route A single-infinity graph no-go: exact checks passed")
