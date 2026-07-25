#!/usr/bin/env python3
"""Verify the Hamiltonian meaning of the all-k radial kernel classes.

For the (2,3) outer pair

    P0=z^2*U(w)/w,  Q0=z^3*V(w)/w,

the constant outer equation gives

    Omega=dP0 wedge dQ0=(E*z^4/w^3) dz wedge dw.

After harmlessly normalizing E=1, a deficit-d kernel polynomial C, with
c=5-d nonzero, has Hamiltonian

    H_(d,C)=-z^c*C(w)/(c*w)

for this two-form, using the convention i_(X_H) Omega=dH.  Its vector field

    X_H =
      z^(1-d)*w*(C-w*C')/c * partial_z
      + z^(-d)*w^2*C * partial_w

satisfies

    X_H(P0)=z^(2-d)*A_C,
    X_H(Q0)=z^(3-d)*B_C.

Every formal Hamiltonian flow exp(X_H) preserves Omega, so the nonlinear
lower bracket equations are formally unobstructed before imposing bounded
polynomial support.  The observed consistency equations measure support
escape of these flows.

The commutator is again Hamiltonian.  If f=5-e and g=5-d-e, then

    [X_(d,C),X_(e,D)] = X_K,

where

    K=z^g*((w*C'-C)*D/c + C*(D-w*D')/f).

For g nonzero this is H_(d+e,CstarD), with

    CstarD=-g*w*((w*C'-C)*D/c + C*(D-w*D')/f).

This gives the exact graded Lie operation on the scalar C-potentials.
"""

from __future__ import annotations

import sympy as sp


def verify_hamiltonian_gauge() -> None:
    z, w = sp.symbols("z w", nonzero=True)
    d = sp.symbols("d", integer=True)
    c = 5 - d
    u = sp.Function("U")(w)
    v = sp.Function("V")(w)
    parameter = sp.Function("C")(w)

    p0 = z**2 * u / w
    q0 = z**3 * v / w
    edge = u * v + 2 * w * u * sp.diff(v, w) - 3 * w * sp.diff(u, w) * v
    jacobian = sp.simplify(
        sp.diff(p0, z) * sp.diff(q0, w)
        - sp.diff(p0, w) * sp.diff(q0, z)
    )
    assert sp.simplify(jacobian - edge * z**4 / w**3) == 0

    hamiltonian = -z**c * parameter / (c * w)
    density = edge * z**4 / w**3
    # i_X(Omega)=dH for Omega=density*dz^dw.
    vector_z = sp.diff(hamiltonian, w) / density
    vector_w = -sp.diff(hamiltonian, z) / density
    expected_z = (
        z ** (1 - d)
        * w
        * (parameter - w * sp.diff(parameter, w))
        / (c * edge)
    )
    expected_w = z ** (-d) * w**2 * parameter / edge
    assert sp.simplify(vector_z - expected_z) == 0
    assert sp.simplify(vector_w - expected_w) == 0

    represented_a = (
        c * w * parameter * sp.diff(u, w)
        + (d - 3) * parameter * u
        - 2 * w * sp.diff(parameter, w) * u
    ) / c
    represented_b = (
        c * w * parameter * sp.diff(v, w)
        + (d - 2) * parameter * v
        - 3 * w * sp.diff(parameter, w) * v
    ) / c

    action_p = sp.simplify(
        vector_z * sp.diff(p0, z) + vector_w * sp.diff(p0, w)
    )
    action_q = sp.simplify(
        vector_z * sp.diff(q0, z) + vector_w * sp.diff(q0, w)
    )
    assert sp.simplify(
        action_p - z ** (2 - d) * represented_a / edge
    ) == 0
    assert sp.simplify(
        action_q - z ** (3 - d) * represented_b / edge
    ) == 0


def verify_scalar_lie_bracket() -> None:
    z, w = sp.symbols("z w", nonzero=True)
    d, e = sp.symbols("d e", integer=True)
    c = 5 - d
    f = 5 - e
    g = 5 - d - e
    left = sp.Function("C")(w)
    right = sp.Function("D")(w)
    left_hamiltonian = -z**c * left / (c * w)
    right_hamiltonian = -z**f * right / (f * w)

    # Normalize E=1.  For i_X Omega=dH, the commutator potential is X_H(K).
    inverse_density = w**3 / z**4
    commutator_potential = sp.simplify(
        inverse_density
        * (
            sp.diff(left_hamiltonian, w)
            * sp.diff(right_hamiltonian, z)
            - sp.diff(left_hamiltonian, z)
            * sp.diff(right_hamiltonian, w)
        )
    )
    expected_potential = z**g * (
        (w * sp.diff(left, w) - left) * right / c
        + left * (right - w * sp.diff(right, w)) / f
    )
    assert sp.simplify(
        commutator_potential - expected_potential
    ) == 0

    scalar_bracket = -g * w * (
        (w * sp.diff(left, w) - left) * right / c
        + left * (right - w * sp.diff(right, w)) / f
    )
    represented = -z**g * scalar_bracket / (g * w)
    assert sp.simplify(represented - expected_potential) == 0

    swapped = -g * w * (
        (w * sp.diff(right, w) - right) * left / f
        + right * (left - w * sp.diff(left, w)) / c
    )
    assert sp.simplify(scalar_bracket + swapped) == 0


def main() -> None:
    verify_hamiltonian_gauge()
    verify_scalar_lie_bracket()
    print("Omega=dP0^dQ0=E*z^4/w^3 dz^dw")
    print("H_(d,C)=-z^(5-d)C/((5-d)w) generates (A_C,B_C)")
    print("formal Hamiltonian flows preserve the full bracket exactly")
    print("the scalar C-potentials carry an explicit graded Lie bracket")
    print("RESULT: RADIAL KERNELS ARE HAMILTONIAN GAUGE MODES")


if __name__ == "__main__":
    main()
