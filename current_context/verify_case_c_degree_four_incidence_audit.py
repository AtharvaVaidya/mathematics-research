#!/usr/bin/env python3
"""Exact checks for CASE_C_DEGREE_FOUR_INCIDENCE_AUDIT.md."""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from current_context.verify_case_c_outer_quartic_cokernel_no_go import (
    outer_data,
    signed_tuple,
)
from route_bd_fbar_obstruction import K


eta, h_normalized, cap_parameter, w = sp.symbols(
    "eta h_normalized cap_parameter w"
)
a, b = sp.symbols("a b", nonzero=True)

# The separate degrees 8 and 12 factor through the common degree 4.
p_face = a * eta**8
q_face = b * eta**12
substitution = {eta**4: h_normalized}
assert p_face.subs(substitution) == a * h_normalized**2
assert q_face.subs(substitution) == b * h_normalized**3
assert sp.cancel((a / b) * q_face / p_face - eta**4) == 0
assert sp.gcd(8, 12) == 4
assert sp.gcd(2, 3) == 1


def binary_quartic_invariants(
    coefficients: tuple[K, K, K, K, K],
) -> tuple[K, K]:
    leading, cubic, quadratic, linear, constant = coefficients
    invariant_i = (
        12 * leading * constant
        - 3 * cubic * linear
        + quadratic**2
    )
    invariant_j = (
        72 * leading * quadratic * constant
        + 9 * cubic * quadratic * linear
        - 27 * leading * linear**2
        - 27 * cubic**2 * constant
        - 2 * quadratic**3
    )
    return invariant_i, invariant_j


# X^4-cZ^4 has J=0.
kummer_i, kummer_j = binary_quartic_invariants(
    (K(1), K(), K(), K(), K(-7))
)
assert kummer_i
assert not kummer_j

expected_invariants = {
    "rational factor 1": (
        K(26839),
        (-6971, 0, 0),
        (2818, 0, 0),
    ),
    "rational factor 2": (
        K(16621),
        (927, 0, 0),
        (11135, 0, 0),
    ),
    "cubic factor": (
        K(0, 1),
        (190, 14982, -14886),
        (-13539, -15225, 8221),
    ),
}

for label, (parameter, expected_i, expected_j) in expected_invariants.items():
    _, _, outer_quartic = outer_data(parameter)
    coefficients = tuple(
        outer_quartic.get(exponent, K())
        for exponent in (4, 3, 2, 1, 0)
    )
    invariant_i, invariant_j = binary_quartic_invariants(coefficients)
    assert signed_tuple(invariant_i) == expected_i
    assert signed_tuple(invariant_j) == expected_j
    assert invariant_j
    print(
        f"{label}: I={expected_i}, J={expected_j} != 0"
    )

# The cap resultant varies while the outer quartic is held fixed.
cap_f = w**8 - cap_parameter
cap_g = w**12 + 2 * w
cap_resultant = sp.factor(sp.resultant(cap_f, cap_g, w))
assert cap_resultant == cap_parameter * (cap_parameter**11 - 256)
derivative_gcd = sp.Poly(
    sp.gcd(sp.diff(cap_f, w), sp.diff(cap_g, w)),
    w,
)
assert derivative_gcd.degree() == 0

# The corrected invariant-subset size four is present in (17,1^4),
# while the original separate-coordinate sizes are not.
cycle_sizes = (17, 1, 1, 1, 1)
subset_sizes = {
    sum(cycle_sizes[index] for index in range(len(cycle_sizes)) if mask & (1 << index))
    for mask in range(1 << len(cycle_sizes))
}
assert 4 in subset_sizes
assert 8 not in subset_sizes
assert 12 not in subset_sizes
assert 17 in subset_sizes

print("verified: the common cap normalization has degree gcd(8,12)=4")
print("verified: every certified outer quartic has J != 0")
print("verified: cap resultant A*(A^11-256) remains freely variable")
print("RESULT: THE NATURAL 8/12 LEAF-TO-SHEET INCIDENCE DOES NOT EXIST")
