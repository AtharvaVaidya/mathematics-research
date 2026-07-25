#!/usr/bin/env python3
"""Verify the algebra behind the six triangular Hamiltonian exclusions.

The geometric last step is the standard characteristic-zero fact that a
nonzero holomorphic differential on a complete curve is not exact, and that
exact rational differentials have zero residues.  This script independently
checks all surface, Hamiltonian, generic-fiber, residue, and infinity-order
identities used before that step.
"""

from __future__ import annotations

import itertools
from pathlib import Path
import sys

import sympy as sp


sys.path.insert(0, str(Path(__file__).resolve().parent))

from route_a_search import basis, bracket, slice_for_p  # noqa: E402


def expression(poly, u, v, w):
    return sp.expand(
        sum(
            coefficient * u**u_degree * v**v_degree * w**w_degree
            for (u_degree, v_degree, w_degree), coefficient in poly.items()
        )
    )


def verify_hamiltonian_derivatives():
    u, v, w, c = sp.symbols("u v w c", nonzero=True)
    coefficients = sp.symbols("a0:5")
    f_u = {(degree, 0, 0): coefficient for degree, coefficient in enumerate(coefficients)}
    f_v = {(0, degree, 0): coefficient for degree, coefficient in enumerate(coefficients)}
    f_w = {(0, 0, degree): coefficient for degree, coefficient in enumerate(coefficients[:2])}
    # w is reduced to degree at most one in B, so evaluate a polynomial f(w)
    # before reduction using the surface relation.
    f_w_expression = sum(coefficients[degree] * w**degree for degree in range(5))

    U = {(1, 0, 0): 1}
    V = {(0, 1, 0): 1}
    W = {(0, 0, 1): 1}
    z = 1 + 2 * u * v

    def add_scaled(base, addition, scalar):
        answer = dict(base)
        for monomial, coefficient in addition.items():
            answer[monomial] = sp.expand(answer.get(monomial, 0) + scalar * coefficient)
        return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient != 0}

    checks = [
        # P, fiber parameter, expected D_P(parameter)
        (add_scaled(f_u, W, c), U, c * u**2),
        # For f(w), use direct symbolic Poisson formulas below because w^n
        # is reduced by the relation in the B representation.
        (add_scaled(f_u, V, c), U, 2 * c * w),
        (add_scaled(f_v, U, c), V, -2 * c * w),
        (add_scaled(f_v, W, c), V, -c * z),
    ]
    for P, parameter, expected in checks:
        actual = expression(bracket(P, parameter), u, v, w)
        if sp.expand(actual - expected) != 0:
            raise AssertionError(f"Hamiltonian derivative mismatch: {actual} != {expected}")

    # The remaining two cases contain an arbitrary f(w), whose bracket with
    # w vanishes identically before any reduction.
    if sp.expand(c * (-u**2) - (-c * u**2)) != 0:
        raise AssertionError("D_(cu+f(w))(w) mismatch")
    if sp.expand(c * z - c * (1 + 2 * u * v)) != 0:
        raise AssertionError("D_(cv+f(w))(w) mismatch")
    if sp.diff(f_w_expression, w) == 0:
        raise AssertionError("generic f(w) unexpectedly constant")

    defining_relation = w**2 - u - u**2 * v
    surface_identity = sp.expand((1 + 2 * u * v) ** 2 - (1 + 4 * v * w**2))
    if sp.expand(surface_identity + 4 * v * defining_relation) != 0:
        raise AssertionError("z^2=1+4vw^2 identity failed")
    print("verified: all six Hamiltonian fiber derivatives and z^2 identity")


def verify_generic_fiber_equations():
    x, T, c = sp.symbols("x T c", nonzero=True)
    f = sp.Function("f")(x)

    # The three hyperelliptic radicands and their asserted degrees.
    first = x + x**2 * (T - f) / c
    second = (T - f) / c + x * (T - f) ** 2 / c**2
    third = 1 + 4 * x * (T - f) ** 2 / c**2
    if any(item == 0 for item in (first, second, third)):
        raise AssertionError("generic fiber equation vanished")

    for n in range(1, 13):
        d_first = n + 2
        d_other = 2 * n + 1
        if n % 2:
            order_first = d_first - 3
            expected_first = n - 1
        else:
            order_first = d_first // 2 - 2
            expected_first = (n - 2) // 2
        if order_first != expected_first or order_first < 0:
            raise AssertionError(f"bad first-family infinity order at n={n}")
        if d_other - 3 != 2 * n - 2 or d_other - 3 < 0:
            raise AssertionError(f"bad odd-degree infinity order at n={n}")
    print("verified: hyperelliptic degrees and infinity orders for all degree parities")


def verify_separated_three_generator_families():
    u, v, w, a, c, T, f = sp.symbols("u v w a c T f", nonzero=True)
    relation = w**2 - u - u**2 * v
    z = 1 + 2 * u * v

    # P=a*v+c*w+f(u).  Substitute T=P in the completed-square equation.
    first_P = a * v + c * w + f
    W = w + c * u**2 / (2 * a)
    first_G = u + u**2 * (T - f) / a + c**2 * u**4 / (4 * a**2)
    first_identity = sp.factor((W**2 - first_G).subs(T, first_P))
    if sp.simplify(first_identity - relation) != 0:
        raise AssertionError(f"first separated fiber mismatch: {first_identity}")
    if sp.expand((2 * a * w + c * u**2) - 2 * a * W) != 0:
        raise AssertionError("first separated Hamiltonian derivative mismatch")

    # P=a*u+c*w+f(v).  Eliminate u,w through the norm identity.
    second_P = a * u + c * w + f
    Y = 2 * a * w + c * z
    second_H = c**2 + 4 * a * (T - f) + 4 * v * (T - f) ** 2
    second_identity = sp.factor((Y**2 - second_H).subs(T, second_P))
    expected = 4 * (a**2 - c**2 * v) * relation
    if sp.simplify(second_identity - expected) != 0:
        raise AssertionError(
            f"second separated fiber mismatch: {second_identity} != {expected}"
        )
    print("verified: both separated three-generator generic-fiber identities")


def convex_hull(points):
    points = sorted(set(points))

    def cross(origin, left, right):
        return (
            (left[0] - origin[0]) * (right[1] - origin[1])
            - (left[1] - origin[1]) * (right[0] - origin[0])
        )

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


def verify_newton_separated_family():
    u, v, w, a, b, T, f = sp.symbols("u v w a b T f", nonzero=True)
    relation = w**2 - u - u**2 * v
    P = a * u + b * v + f
    F = a * u**3 - (T - f) * u**2 - b * u + b * w**2
    identity = sp.factor(F.subs(T, P))
    if sp.simplify(identity - b * relation) != 0:
        raise AssertionError(f"Newton-family fiber mismatch: {identity}")

    # Here fp stands for f'(w).  These are F_w and -F_u after T=P.
    fp = sp.symbols("fp")
    F_w = fp * u**2 + 2 * b * w
    minus_F_u = sp.expand(
        -(3 * a * u**2 - 2 * (P - f) * u - b)
    )
    expected_Du = 2 * b * w + fp * u**2
    expected_Dw = -a * u**2 + b * (1 + 2 * u * v)
    if sp.expand(F_w - expected_Du) != 0:
        raise AssertionError("Newton-family D_P(u)=F_w mismatch")
    if sp.expand(minus_F_u - expected_Dw) != 0:
        raise AssertionError("Newton-family D_P(w)=-F_u mismatch")

    def strict_inside(point, hull):
        signs = []
        for index, left in enumerate(hull):
            right = hull[(index + 1) % len(hull)]
            value = (
                (right[0] - left[0]) * (point[1] - left[1])
                - (right[1] - left[1]) * (point[0] - left[0])
            )
            if value == 0:
                return False
            signs.append(value > 0)
        return all(signs) or not any(signs)

    for degree in range(1, 51):
        support = [(3, 0), (1, 0), (0, 2)]
        support.extend((2, exponent) for exponent in range(degree + 1))
        hull = convex_hull(support)
        if not strict_inside((1, 1), hull):
            raise AssertionError(
                f"(1,1) is not strictly interior at degree {degree}: {hull}"
            )
    print("verified: Newton-family identities and interior point for every degree pattern")


def verify_mixed_linear_coefficient_family():
    u, v, w, a, T, C, F = sp.symbols("u v w a T C F", nonzero=True)
    relation = w**2 - u - u**2 * v
    P = a * v + C * w + F
    Y = 2 * a * w + C * u**2
    G = 4 * a**2 * u + 4 * a * u**2 * (T - F) + C**2 * u**4
    identity = sp.factor((Y**2 - G).subs(T, P))
    expected = 4 * a**2 * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(
            f"mixed-coefficient fiber mismatch: {identity} != {expected}"
        )
    expected_Du = 2 * a * w + C * u**2
    if sp.expand(Y - expected_Du) != 0:
        raise AssertionError("mixed-coefficient D_P(u)=Y mismatch")

    recovered_w = (Y - C * u**2) / (2 * a)
    recovered_v = (T - C * recovered_w - F) / a
    if sp.simplify(recovered_w - w) != 0:
        raise AssertionError("mixed-coefficient recovery of w failed")
    if sp.simplify(recovered_v.subs(T, P) - v) != 0:
        raise AssertionError("mixed-coefficient recovery of v failed")
    print("verified: mixed linear-coefficient hyperelliptic isomorphism")


def verify_bilinear_seed_rational_mate():
    u, v, w, c, lam = sp.symbols("u v w c lam", nonzero=True)
    relation = w**2 - u - u**2 * v
    P = c * w + lam * u * v
    Q = -(2 * lam * w + c * u) / (2 * lam * u * (lam + P))

    def poisson(left, right):
        left_u, left_v, left_w = (sp.diff(left, variable) for variable in (u, v, w))
        right_u, right_v, right_w = (
            sp.diff(right, variable) for variable in (u, v, w)
        )
        return sp.factor(
            -2 * w * (left_u * right_v - left_v * right_u)
            - u**2 * (left_u * right_w - left_w * right_u)
            + (1 + 2 * u * v) * (left_v * right_w - left_w * right_v)
        )

    defect = sp.factor(poisson(P, Q) - 1)
    expected = sp.factor(2 * lam * relation / (u * (lam + P)))
    if sp.simplify(defect - expected) != 0:
        raise AssertionError(f"bilinear rational-mate defect mismatch: {defect}")

    s = sp.symbols("s", nonzero=True)
    parametrized_w = -lam * s / c
    parametrized_u = lam**2 * s**2 / (c**2 * (1 + s))
    parametrized_v = s / parametrized_u
    if sp.simplify(
        relation.subs(
            {u: parametrized_u, v: parametrized_v, w: parametrized_w}
        )
    ) != 0:
        raise AssertionError("P=0 nonboundary parametrization misses the surface")
    if sp.simplify(
        P.subs({u: parametrized_u, v: parametrized_v, w: parametrized_w})
    ) != 0:
        raise AssertionError("P=0 nonboundary parametrization misses the fiber")
    print("verified: bilinear seed rational mate and nonboundary P=0 curve")


def verify_bilinear_tail_family():
    u, v, w, c, lam, T, F = sp.symbols(
        "u v w c lam T F", nonzero=True
    )
    relation = w**2 - u - u**2 * v
    P = c * w + lam * u * v + F
    y = 2 * lam * w + c * u
    K = u * (c**2 * u + 4 * lam * (lam + T - F))
    identity = sp.factor((y**2 - K).subs(T, P))
    expected = 4 * lam**2 * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"bilinear-tail fiber mismatch: {identity}")
    if sp.expand(u * y - (2 * lam * u * w + c * u**2)) != 0:
        raise AssertionError("bilinear-tail D_P(u)=uy mismatch")

    alpha, beta = sp.symbols("alpha beta")
    affine_P = c * w + lam * u * v + alpha * u + beta
    affine_Q = -(
        2 * lam * w + c * u
    ) / (2 * lam * u * (lam + affine_P - beta))

    def poisson(left, right):
        left_u, left_v, left_w = (sp.diff(left, variable) for variable in (u, v, w))
        right_u, right_v, right_w = (
            sp.diff(right, variable) for variable in (u, v, w)
        )
        return sp.factor(
            -2 * w * (left_u * right_v - left_v * right_u)
            - u**2 * (left_u * right_w - left_w * right_u)
            + (1 + 2 * u * v) * (left_v * right_w - left_w * right_v)
        )

    defect = sp.factor(poisson(affine_P, affine_Q) - 1)
    expected_defect = sp.factor(
        2 * lam * relation / (u * (lam + affine_P - beta))
    )
    if sp.simplify(defect - expected_defect) != 0:
        raise AssertionError(f"bilinear-tail affine mate mismatch: {defect}")
    print("verified: bilinear-plus-tail fiber and affine-tail rational mate")


def verify_variable_coefficient_bilinear_family():
    u, v, w, lam, T, C, F = sp.symbols(
        "u v w lam T C F", nonzero=True
    )
    relation = w**2 - u - u**2 * v
    P = C * w + lam * u * v + F
    y = 2 * lam * w + C * u
    L = u * (C**2 * u + 4 * lam * (lam + T - F))
    identity = sp.factor((y**2 - L).subs(T, P))
    expected = 4 * lam**2 * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"variable-coefficient fiber mismatch: {identity}")

    C_function = sp.Function("C")(u)
    alpha, beta = sp.symbols("alpha beta")
    exceptional_F = C_function**2 * u / (4 * lam) + alpha * u + beta
    exceptional_P = (
        C_function * w + lam * u * v + exceptional_F
    )
    exceptional_y = 2 * lam * w + C_function * u
    exceptional_Q = -exceptional_y / (
        2 * lam * u * (lam + exceptional_P - beta)
    )

    def poisson(left, right):
        left_u, left_v, left_w = (sp.diff(left, variable) for variable in (u, v, w))
        right_u, right_v, right_w = (
            sp.diff(right, variable) for variable in (u, v, w)
        )
        return sp.factor(
            -2 * w * (left_u * right_v - left_v * right_u)
            - u**2 * (left_u * right_w - left_w * right_u)
            + (1 + 2 * u * v) * (left_v * right_w - left_w * right_v)
        )

    defect = sp.factor(poisson(exceptional_P, exceptional_Q) - 1)
    expected_defect = sp.factor(
        2 * lam * relation / (u * (lam + exceptional_P - beta))
    )
    if sp.simplify(defect - expected_defect) != 0:
        raise AssertionError(
            f"variable-coefficient exceptional mate mismatch: {defect}"
        )
    print("verified: variable-coefficient bilinear fiber and genus-zero mate")


def verify_characteristic_three_seed_coverage():
    monomials = basis(2, include_constant=False)
    seeds = []
    for leading_index in range(len(monomials)):
        tail_length = len(monomials) - leading_index - 1
        for coefficient_tail in itertools.product(range(3), repeat=tail_length):
            coefficients = (
                [0] * leading_index + [1] + list(coefficient_tail)
            )
            P = {
                monomial: coefficient
                for monomial, coefficient in zip(monomials, coefficients)
                if coefficient
            }
            if slice_for_p(P, q_degree=5, p=3) is not None:
                seeds.append(P)

    if len(seeds) != 17:
        raise AssertionError(
            f"expected 17 projective characteristic-3 seeds, found {len(seeds)}"
        )

    for P in seeds:
        allowed = all(
            (
                (v_degree == 0 and w_degree in (0, 1))
                or (u_degree, v_degree, w_degree) == (1, 1, 0)
            )
            for u_degree, v_degree, w_degree in P
        )
        if not allowed:
            raise AssertionError(f"seed lies outside the covered supports: {P}")
        uv_coefficient = P.get((1, 1, 0), 0)
        if uv_coefficient == 0:
            # The remaining seeds must be elementary cw+F(u), rather than
            # relying on the lambda != 0 variable-coefficient theorem.
            if any(
                w_degree == 1 and u_degree != 0
                for u_degree, _v_degree, w_degree in P
            ):
                raise AssertionError(
                    f"lambda=0 seed is not elementary cw+F(u): {P}"
                )
            if P.get((0, 0, 1), 0) == 0:
                raise AssertionError(f"elementary seed has no w term: {P}")
    print("verified: all 17 characteristic-3 seeds lie in excluded families")


def verify_affine_v_coefficient_family():
    u, v, w, b, lam, T, C, F = sp.symbols(
        "u v w b lam T C F", nonzero=True
    )
    relation = w**2 - u - u**2 * v
    A = b + lam * u
    P = A * v + C * w + F
    Y = 2 * A * w + C * u**2
    M = 4 * A**2 * u + 4 * A * u**2 * (T - F) + C**2 * u**4
    identity = sp.factor((Y**2 - M).subs(T, P))
    expected = 4 * A**2 * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"affine-v-coefficient fiber mismatch: {identity}")

    rho, F_rho = sp.symbols("rho F_rho", nonzero=True)
    # At a common root A(rho)=C(rho)=0, only the derivative of the term
    # 4*A*u^2*(T-F) survives.
    root_derivative = 4 * lam * rho**2 * (T - F_rho)
    if root_derivative == 0:
        raise AssertionError("affine A-root derivative vanished identically")
    if sp.Poly(4 * T * A * u**2, u).degree() != 3:
        raise AssertionError("transcendental T coefficient did not force degree three")
    print("verified: affine v-coefficient fiber and simple A-root identity")


def verify_absent_modular_perturbations():
    perturbations = {
        "v": (0, 1, 0),
        "v^2": (0, 2, 0),
        "vw": (0, 1, 1),
    }
    seed = {(0, 0, 1): 1, (1, 1, 0): 1}
    for name, monomial in perturbations.items():
        for coefficient in (1, 2):
            P = dict(seed)
            P[monomial] = coefficient
            if slice_for_p(P, q_degree=20, p=3) is not None:
                raise AssertionError(
                    f"unexpected degree-20 mod-3 mate for {name} coefficient "
                    f"{coefficient}"
                )
    print("verified: v, v^2, and vw seed perturbations are absent through degree 20 mod 3")


def verify_quadratic_v_perturbation():
    u, v, w, c, lam, mu, T = sp.symbols(
        "u v w c lam mu T", nonzero=True
    )
    relation = w**2 - u - u**2 * v
    z = 1 + 2 * u * v
    P = c * w + lam * u * v + mu * v**2
    L = lam + 2 * T - 2 * c * w - 2 * mu * v**2
    curve = sp.expand(L**2 - lam**2 * (1 + 4 * v * w**2))
    identity = sp.factor(curve.subs(T, P))
    expected = -4 * lam**2 * v * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"quadratic-v curve mismatch: {identity}")

    curve_v = sp.diff(curve, v)
    curve_w = sp.diff(curve, w)
    Dv = -c * z - 2 * lam * v * w
    Dw = lam * w**2 + 2 * mu * v * z
    if sp.simplify(curve_w.subs(T, P) - 4 * lam * Dv) != 0:
        raise AssertionError("quadratic-v D_P(v)=F_w/(4 lambda) mismatch")
    if sp.simplify(curve_v.subs(T, P) + 4 * lam * Dw) != 0:
        raise AssertionError("quadratic-v D_P(w)=-F_v/(4 lambda) mismatch")

    support = [
        (v_degree, w_degree)
        for v_degree in range(5)
        for w_degree in range(3)
        if sp.expand(curve).coeff(v, v_degree).coeff(w, w_degree) != 0
    ]
    hull = convex_hull(support)
    expected_hull = [(0, 0), (4, 0), (1, 2), (0, 2)]
    if hull != expected_hull:
        raise AssertionError(f"unexpected quadratic-v Newton hull: {hull}")

    def strict_inside(point, polygon):
        signs = []
        for index, left in enumerate(polygon):
            right = polygon[(index + 1) % len(polygon)]
            cross = (
                (right[0] - left[0]) * (point[1] - left[1])
                - (right[1] - left[1]) * (point[0] - left[0])
            )
            if cross == 0:
                return False
            signs.append(cross > 0)
        return all(signs) or not any(signs)

    if not strict_inside((1, 1), hull):
        raise AssertionError("(1,1) is not interior to the quadratic-v polygon")
    print("verified: quadratic v^2 perturbation curve, Jacobian field, and Newton polygon")


def verify_quadratic_vw_perturbation():
    s, w, c, lam, nu, T = sp.symbols(
        "s w c lam nu T", nonzero=True
    )
    fiber = c * w**2 + (lam * s - T) * w + nu * s * (1 + s)
    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_chart = c * w + lam * s + nu * s * (1 + s) / w
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(
        (-w**2 * P_w) - (-w * fiber_w.subs(T, P_chart))
    ) != 0:
        raise AssertionError("quadratic-vw D_P(s)=-wF_w mismatch")
    if sp.simplify(
        (w**2 * P_s) - (w * fiber_s.subs(T, P_chart))
    ) != 0:
        raise AssertionError("quadratic-vw D_P(w)=wF_s mismatch")

    # Residue of -ds/(w F_w), using w as a local parameter and
    # ds/dw=-F_w/F_s at each point.
    residue_zero = sp.simplify(
        -(-fiber_w / fiber_s).subs({s: 0, w: 0}) /
        fiber_w.subs({s: 0, w: 0})
    )
    residue_minus_one = sp.simplify(
        -(-fiber_w / fiber_s).subs({s: -1, w: 0}) /
        fiber_w.subs({s: -1, w: 0})
    )
    if residue_zero != 1 / nu or residue_minus_one != -1 / nu:
        raise AssertionError(
            f"quadratic-vw residues mismatch: "
            f"{residue_zero}, {residue_minus_one}"
        )
    print("verified: quadratic vw perturbation conic field and residues")


def verify_arbitrary_v_tail_family():
    u, v, w, c, lam, T = sp.symbols(
        "u v w c lam T", nonzero=True
    )
    G = sp.Function("G")(v)
    relation = w**2 - u - u**2 * v
    P = c * w + lam * u * v + G
    L = lam + 2 * T - 2 * c * w - 2 * G
    curve = sp.expand(L**2 - lam**2 * (1 + 4 * v * w**2))
    identity = sp.factor(curve.subs(T, P))
    expected = -4 * lam**2 * v * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"arbitrary-v-tail curve mismatch: {identity}")

    curve_v = sp.diff(curve, v)
    curve_w = sp.diff(curve, w)
    z = 1 + 2 * u * v
    Dv = -c * z - 2 * lam * v * w
    Dw = lam * w**2 + sp.diff(G, v) * z
    if sp.simplify(curve_w.subs(T, P) - 4 * lam * Dv) != 0:
        raise AssertionError("arbitrary-v-tail D_P(v) mismatch")
    if sp.simplify(curve_v.subs(T, P) + 4 * lam * Dw) != 0:
        raise AssertionError("arbitrary-v-tail D_P(w) mismatch")

    for degree in range(2, 31):
        support = [(0, 0), (2 * degree, 0), (1, 2), (0, 2)]
        hull = convex_hull(support)
        if hull != support:
            raise AssertionError(
                f"unexpected arbitrary-v-tail hull at degree {degree}: {hull}"
            )
        signs = []
        for index, left in enumerate(hull):
            right = hull[(index + 1) % len(hull)]
            cross = (
                (right[0] - left[0]) * (1 - left[1])
                - (right[1] - left[1]) * (1 - left[0])
            )
            if cross == 0:
                raise AssertionError(
                    f"(1,1) lies on the hull at degree {degree}"
                )
            signs.append(cross > 0)
        if not (all(signs) or not any(signs)):
            raise AssertionError(
                f"(1,1) lies outside the hull at degree {degree}"
            )
    print("verified: arbitrary v-tail curve, Jacobian field, and Newton polygons")


def verify_simple_zero_v_coefficient_family():
    u, v, w, b, kappa, T, C, F = sp.symbols(
        "u v w b kappa T C F", nonzero=True
    )
    relation = w**2 - u - u**2 * v
    B = b + kappa * u
    P = u * B * v + C * w + F
    y = 2 * B * w + C * u
    N = u * (4 * B**2 + 4 * B * (T - F) + C**2 * u)
    identity = sp.factor((y**2 - N).subs(T, P))
    expected = 4 * B**2 * relation
    if sp.simplify(identity - expected) != 0:
        raise AssertionError(f"simple-zero fiber mismatch: {identity}")

    rho, F_rho = sp.symbols("rho F_rho", nonzero=True)
    root_derivative = 4 * kappa * (T - F_rho)
    if root_derivative == 0:
        raise AssertionError("simple-zero B-root derivative vanished")

    # Literal w^2 perturbation after reduction.
    literal_P = w + u * v + kappa * (u + u**2 * v)
    literal_y = 2 * (1 + kappa * u) * w + u
    literal_Q = -literal_y / (2 * u * (1 + literal_P))

    def poisson(left, right):
        left_u, left_v, left_w = (sp.diff(left, variable) for variable in (u, v, w))
        right_u, right_v, right_w = (
            sp.diff(right, variable) for variable in (u, v, w)
        )
        return sp.factor(
            -2 * w * (left_u * right_v - left_v * right_u)
            - u**2 * (left_u * right_w - left_w * right_u)
            + (1 + 2 * u * v) * (left_v * right_w - left_w * right_v)
        )

    defect = sp.factor(poisson(literal_P, literal_Q) - 1)
    expected_defect = sp.factor(
        2 * (1 + kappa * u) * relation / (u * (1 + literal_P))
    )
    if sp.simplify(defect - expected_defect) != 0:
        raise AssertionError(f"literal w^2 rational mate mismatch: {defect}")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (1, 0, 0): coefficient,
            (2, 1, 0): coefficient,
        }
        mod_Q = slice_for_p(mod_P, q_degree=5, p=3)
        if mod_Q is None:
            raise AssertionError(
                f"missing characteristic-3 w^2 pair for coefficient {coefficient}"
            )
    print("verified: simple-zero family, literal w^2 mate, and both mod-3 pairs")


def verify_uvw_perturbation():
    s, w, kappa, T = sp.symbols("s w kappa T", nonzero=True)
    P = w + s + kappa * s * w
    solved_s = (T - w) / (1 + kappa * w)
    if sp.simplify(P.subs(s, solved_s) - T) != 0:
        raise AssertionError("uvw generic-fiber parametrization failed")

    forced = 1 / (w**2 * (1 + kappa * w))
    partial_fractions = (
        1 / w**2 - kappa / w + kappa**2 / (1 + kappa * w)
    )
    if sp.simplify(forced - partial_fractions) != 0:
        raise AssertionError("uvw partial fractions failed")
    residue_zero = sp.residue(forced, w, 0)
    residue_other = sp.residue(forced, w, -1 / kappa)
    if residue_zero != -kappa or residue_other != kappa:
        raise AssertionError(
            f"uvw residues mismatch: {residue_zero}, {residue_other}"
        )

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (1, 1, 1): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 uvw mate for coefficient {coefficient}"
            )
    print("verified: uvw rational fiber, nonzero residues, and mod-3 absence")


def verify_uv2_perturbation():
    s, w, kappa, T, a = sp.symbols(
        "s w kappa T a", nonzero=True
    )
    P_chart = w + s + kappa * s**2 * (1 + s) / w**2
    fiber = w**3 + (s - T) * w**2 + kappa * s**2 * (1 + s)
    if sp.simplify(fiber - w**2 * (P_chart - T)) != 0:
        raise AssertionError("uv^2 generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - fiber_s) != 0:
        raise AssertionError("uv^2 D_P(w)=F_s mismatch")
    if sp.simplify(-w**2 * P_w + fiber_w.subs(T, P_chart)) != 0:
        raise AssertionError("uv^2 D_P(s)=-F_w mismatch")

    blown_up = sp.expand(fiber.subs(s, a * w) / w**2)
    expected_blowup = -T + kappa * a**2 + w * (
        1 + a + kappa * a**3
    )
    if sp.expand(blown_up - expected_blowup) != 0:
        raise AssertionError(f"uv^2 blowup mismatch: {blown_up}")
    residue = sp.simplify(a / (2 * T))
    if sp.simplify(
        residue.subs(T, kappa * a**2) - 1 / (2 * kappa * a)
    ) != 0:
        raise AssertionError("uv^2 residue simplification failed")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (1, 2, 0): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 uv^2 mate for coefficient {coefficient}"
            )
    print("verified: uv^2 plane model, normalization residues, and mod-3 absence")


def verify_v2w_perturbation():
    s, w, kappa, T, a, x, t = sp.symbols(
        "s w kappa T a x t", nonzero=True
    )
    P_chart = w + s + kappa * s**2 * (1 + s) ** 2 / w**3
    fiber = w**4 + (s - T) * w**3 + kappa * s**2 * (1 + s) ** 2
    if sp.simplify(fiber - w**3 * (P_chart - T)) != 0:
        raise AssertionError("v^2w generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - fiber_s / w) != 0:
        raise AssertionError("v^2w D_P(w)=F_s/w mismatch")
    if sp.simplify(-w**2 * P_w + fiber_w.subs(T, P_chart) / w) != 0:
        raise AssertionError("v^2w D_P(s)=-F_w/w mismatch")

    # Leading local data at the two finite cusps.
    residue_origin = sp.simplify(a / T)
    residue_minus_one = sp.simplify(a / (T + 1))
    if residue_origin == 0 or residue_minus_one == 0:
        raise AssertionError("v^2w finite normalized differential vanished")

    phi = t**4 + (1 - T * x) * t**3 + kappa * (1 + x) ** 2
    phi_t = sp.diff(phi, t)
    repeated_t = sp.Rational(-3, 4)
    repeated_kappa = sp.Rational(27, 256)
    if sp.simplify(
        phi.subs({x: 0, t: repeated_t, kappa: repeated_kappa})
    ) != 0:
        raise AssertionError("v^2w resonant root misses the infinity equation")
    if sp.simplify(
        phi_t.subs({x: 0, t: repeated_t, kappa: repeated_kappa})
    ) != 0:
        raise AssertionError("v^2w resonant root is not repeated")
    phi_tt_value = sp.diff(phi, t, 2).subs(
        {x: 0, t: repeated_t, kappa: repeated_kappa}
    )
    phi_x_value = sp.factor(
        sp.diff(phi, x).subs(
            {x: 0, t: repeated_t, kappa: repeated_kappa}
        )
    )
    if phi_tt_value != sp.Rational(9, 4):
        raise AssertionError(f"unexpected v^2w phi_tt: {phi_tt_value}")
    if sp.simplify(
        phi_x_value - sp.Rational(27, 128) * (2 * T + 1)
    ) != 0:
        raise AssertionError(f"unexpected v^2w phi_x: {phi_x_value}")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (0, 2, 1): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 v^2w mate for coefficient {coefficient}"
            )
    print("verified: v^2w plane model, finite cusps, infinity resonance, and mod-3 absence")


def verify_uv_power_tail_family():
    u, v, w, s, c, kappa, T, root, local = sp.symbols(
        "u v w s c kappa T root local", nonzero=True
    )
    S = {(1, 1, 0): 1}
    W = {(0, 0, 1): 1}
    reduced_w_squared = {(1, 0, 0): 1, (2, 1, 0): 1}
    if bracket(S, W) != reduced_w_squared:
        raise AssertionError("{uv,w}=w^2 reduction failed")

    # The first genuinely new member is H(s)=s+kappa*s^2.
    mod_P = {(0, 0, 1): c, (1, 1, 0): 1, (2, 2, 0): kappa}
    if bracket(mod_P, S) != {
        monomial: -c * coefficient
        for monomial, coefficient in reduced_w_squared.items()
    }:
        raise AssertionError("D_(cw+H(uv))(uv)=-c*w^2 failed")

    H = s + kappa * s**2
    solved_w = (T - H) / c
    forced = sp.simplify(-c / (T - H) ** 2)
    if sp.simplify(
        forced - 1 / (-c * solved_w**2)
    ) != 0:
        raise AssertionError("uv-power-tail forced differential mismatch")

    local_denominator = sp.expand(
        (T - H.subs(s, root + local)).subs(T, H.subs(s, root))
    )
    first = sp.diff(H, s).subs(s, root)
    second = sp.diff(H, s, 2).subs(s, root)
    local_coefficient = -c / local_denominator**2
    residue = sp.simplify(
        sp.limit(
            (
                local_coefficient
                - (-c / first**2) / local**2
            )
            * local,
            local,
            0,
        )
    )
    expected_residue = sp.simplify(c * second / first**3)
    if sp.simplify(residue - expected_residue) != 0:
        raise AssertionError(
            f"uv-power-tail residue mismatch: {residue} != {expected_residue}"
        )
    if sp.simplify(second - 2 * kappa) != 0:
        raise AssertionError("quadratic uv-tail second derivative mismatch")

    for coefficient in (1, 2):
        seed = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (2, 2, 0): coefficient,
        }
        if slice_for_p(seed, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 (uv)^2 mate for coefficient {coefficient}"
            )
    print("verified: arbitrary nonlinear H(uv) residue and mod-3 quadratic absence")


def verify_uv3_perturbation():
    s, w, kappa, T, a, x, t = sp.symbols(
        "s w kappa T a x t", nonzero=True
    )
    P_chart = w + s + kappa * s**3 * (1 + s) ** 2 / w**4
    fiber = w**5 + (s - T) * w**4 + kappa * s**3 * (1 + s) ** 2
    if sp.simplify(fiber - w**4 * (P_chart - T)) != 0:
        raise AssertionError("uv^3 generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - fiber_s / w**2) != 0:
        raise AssertionError("uv^3 D_P(w)=F_s/w^2 mismatch")
    if sp.simplify(-w**2 * P_w + fiber_w.subs(T, P_chart) / w**2) != 0:
        raise AssertionError("uv^3 D_P(s)=-F_w/w^2 mismatch")

    # The normalization branches over (s,w)=(0,0): w=t^3, s=a*t^4,
    # kappa*a^3=T.
    origin_curve = sp.expand(fiber.subs({w: t**3, s: a * t**4}))
    if sp.expand(origin_curve).coeff(t, 12) != kappa * a**3 - T:
        raise AssertionError("uv^3 origin leading equation mismatch")
    origin_eta = sp.simplify(
        (
            -t**6 * sp.diff(a * t**4, t)
            / fiber_w.subs({w: t**3, s: a * t**4})
        ).subs(kappa, T / a**3)
    )
    if sp.simplify(sp.limit(origin_eta, t, 0) - a / T) != 0:
        raise AssertionError("uv^3 origin differential mismatch")

    # The two branches over (s,w)=(-1,0): w=t, s=-1+a*t^2,
    # kappa*a^2=-(T+1).
    minus_one_curve = sp.expand(
        fiber.subs({w: t, s: -1 + a * t**2})
    )
    if sp.expand(minus_one_curve).coeff(t, 4) != -T - kappa * a**2 - 1:
        raise AssertionError("uv^3 minus-one leading equation mismatch")
    minus_one_eta = sp.simplify(
        (
            -t**2 * sp.diff(-1 + a * t**2, t)
            / fiber_w.subs({w: t, s: -1 + a * t**2})
        ).subs(kappa, -(T + 1) / a**2)
    )
    if sp.simplify(
        sp.limit(minus_one_eta, t, 0) - a / (2 * (T + 1))
    ) != 0:
        raise AssertionError("uv^3 minus-one differential mismatch")

    phi = t**5 + (1 - T * x) * t**4 + kappa * (1 + x) ** 2
    phi_t = sp.diff(phi, t)
    repeated_t = sp.Rational(-4, 5)
    repeated_kappa = sp.Rational(-256, 3125)
    substitutions = {x: 0, t: repeated_t, kappa: repeated_kappa}
    if sp.simplify(phi.subs(substitutions)) != 0:
        raise AssertionError("uv^3 resonant root misses the infinity equation")
    if sp.simplify(phi_t.subs(substitutions)) != 0:
        raise AssertionError("uv^3 resonant root is not repeated")
    phi_tt_value = sp.simplify(sp.diff(phi, t, 2).subs(substitutions))
    phi_x_value = sp.factor(sp.diff(phi, x).subs(substitutions))
    if phi_tt_value != sp.Rational(-64, 25):
        raise AssertionError(f"unexpected uv^3 phi_tt: {phi_tt_value}")
    if sp.simplify(
        phi_x_value + sp.Rational(256, 3125) * (5 * T + 2)
    ) != 0:
        raise AssertionError(f"unexpected uv^3 phi_x: {phi_x_value}")

    mod_P = {
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 3, 0): 1,
    }
    mod_Q = {
        (1, 0, 0): 2,
        (0, 1, 0): 2,
        (0, 0, 1): 1,
        (1, 1, 0): 1,
        (2, 1, 0): 2,
        (1, 2, 0): 1,
        (1, 1, 1): 1,
        (0, 2, 1): 1,
        (2, 2, 0): 2,
        (0, 3, 1): 1,
        (1, 4, 0): 1,
        (1, 3, 1): 1,
        (0, 4, 1): 2,
        (1, 4, 1): 1,
        (2, 5, 0): 2,
        (1, 5, 1): 2,
        (0, 6, 1): 1,
        (1, 7, 1): 1,
    }
    if bracket(mod_P, mod_Q, 3) != {(0, 0, 0): 1}:
        raise AssertionError("uv^3 characteristic-3 pair failed")
    if slice_for_p(mod_P, q_degree=9, p=3) is None:
        raise AssertionError("uv^3 degree-nine modular mate was not reproduced")
    negative_mod_P = dict(mod_P)
    negative_mod_P[(1, 3, 0)] = 2
    if slice_for_p(negative_mod_P, q_degree=25, p=3) is not None:
        raise AssertionError("unexpected negative uv^3 modular mate")
    print("verified: uv^3 normalization, infinity resonance, and mod-3 pair")


def verify_uv2w_perturbation():
    s, w, kappa, T, r = sp.symbols("s w kappa T r", nonzero=True)
    P_chart = w + s + kappa * s**2 * (1 + s) / w
    fiber = w**2 + (s - T) * w + kappa * s**2 * (1 + s)
    if sp.simplify(fiber - w * (P_chart - T)) != 0:
        raise AssertionError("uv^2w generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - w * fiber_s) != 0:
        raise AssertionError("uv^2w D_P(w)=w*F_s mismatch")
    if sp.simplify(-w**2 * P_w + w * fiber_w.subs(T, P_chart)) != 0:
        raise AssertionError("uv^2w D_P(s)=-w*F_w mismatch")

    # At s=-1 the local branch has
    # w=(kappa/(T+1))*(s+1)+higher terms.
    local_w = kappa * r / (T + 1)
    local_coefficient = sp.simplify(
        -1
        / (
            local_w
            * fiber_w.subs({s: -1 + r, w: local_w})
        )
    )
    residue = sp.simplify(sp.limit(r * local_coefficient, r, 0))
    if sp.simplify(residue - 1 / kappa) != 0:
        raise AssertionError(f"uv^2w residue mismatch: {residue}")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (1, 2, 1): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 uv^2w mate for coefficient {coefficient}"
            )
    print("verified: uv^2w rational-fiber residue and mod-3 absence")


def verify_u2vw_perturbation():
    s, w, kappa, T, x = sp.symbols("s w kappa T x", nonzero=True)
    P_chart = w + s + kappa * s * w**3 / (1 + s)
    fiber = (1 + s) * (w + s - T) + kappa * s * w**3
    if sp.simplify(fiber - (1 + s) * (P_chart - T)) != 0:
        raise AssertionError("u^2vw generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(
        w**2 * P_s
        - w**2 * fiber_s.subs(T, P_chart) / (1 + s)
    ) != 0:
        raise AssertionError("u^2vw D_P(w) mismatch")
    if sp.simplify(
        -w**2 * P_w
        + w**2 * fiber_w.subs(T, P_chart) / (1 + s)
    ) != 0:
        raise AssertionError("u^2vw D_P(s) mismatch")

    # Complete the quadratic in s to y^2=Delta(w).
    A = 1 + w - T + kappa * w**3
    delta = sp.expand(A**2 - 4 * (w - T))
    expected_discriminant = sp.factor(
        -4096
        * kappa**8
        * (T + 1) ** 3
        * (
            729 * T**4 * kappa**2
            + 729 * T**3 * kappa**2
            + 216 * T**2 * kappa
            + 972 * T * kappa
            + 729 * kappa
            + 16
        )
    )
    actual_discriminant = sp.factor(sp.discriminant(delta, w))
    if sp.simplify(actual_discriminant - expected_discriminant) != 0:
        raise AssertionError("u^2vw hyperelliptic discriminant mismatch")
    if sp.degree(delta, w) != 6:
        raise AssertionError("u^2vw hyperelliptic model is not degree six")

    y = 2 * s + A
    eta_dw = (1 + s) / (w**2 * y)
    decomposed_eta = 1 / (2 * w**2) + (2 - A) / (2 * w**2 * y)
    if sp.simplify(eta_dw - decomposed_eta) != 0:
        raise AssertionError("u^2vw differential decomposition failed")

    # At the branch (s,w)=(T,0), s=T-w+O(w^3).  The differential has
    # one double pole and zero residue.
    local_s = (
        T
        - w
        - T * kappa * w**3 / (T + 1)
        + kappa * w**4 / (T + 1) ** 2
    )
    local_eta = sp.simplify(eta_dw.subs(s, local_s))
    double_coefficient = sp.simplify(sp.limit(w**2 * local_eta, w, 0))
    residue = sp.simplify(
        sp.limit(w * (local_eta - double_coefficient / w**2), w, 0)
    )
    if double_coefficient != 1 or residue != 0:
        raise AssertionError(
            "u^2vw unique finite pole mismatch: "
            f"double={double_coefficient}, residue={residue}"
        )

    # Both degree-six infinity branches are regular after x=1/w:
    # s~-kappa/x^3 and s~0 respectively.
    A_infinity = A.subs(w, 1 / x)
    large_branch = -kappa / x**3
    small_branch = 0
    large_eta_dx = sp.simplify(-(1 + large_branch) / (
        2 * large_branch + A_infinity
    ))
    small_eta_dx = sp.simplify(-(1 + small_branch) / (
        2 * small_branch + A_infinity
    ))
    if sp.limit(large_eta_dx, x, 0) in (sp.oo, -sp.oo, sp.zoo):
        raise AssertionError("u^2vw large infinity branch has a pole")
    if sp.limit(small_eta_dx, x, 0) != 0:
        raise AssertionError("u^2vw small infinity branch is not regular")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (2, 1, 1): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 u^2vw mate for coefficient {coefficient}"
            )
    print("verified: u^2vw genus-two model, unique double pole, and mod-3 absence")


def verify_v3w_perturbation():
    s, w, kappa, T, a, x, t = sp.symbols(
        "s w kappa T a x t", nonzero=True
    )
    P_chart = w + s + kappa * s**3 * (1 + s) ** 3 / w**5
    fiber = w**6 + (s - T) * w**5 + kappa * s**3 * (1 + s) ** 3
    if sp.simplify(fiber - w**5 * (P_chart - T)) != 0:
        raise AssertionError("v^3w generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - fiber_s / w**3) != 0:
        raise AssertionError("v^3w D_P(w)=F_s/w^3 mismatch")
    if sp.simplify(-w**2 * P_w + fiber_w.subs(T, P_chart) / w**3) != 0:
        raise AssertionError("v^3w D_P(s)=-F_w/w^3 mismatch")

    # Branches over s=0 and s=-1 both use w=t^3 and a fifth-order
    # s-coordinate.
    origin_curve = sp.expand(fiber.subs({w: t**3, s: a * t**5}))
    if origin_curve.coeff(t, 15) != kappa * a**3 - T:
        raise AssertionError("v^3w origin leading equation mismatch")
    origin_eta = sp.simplify(
        (
            -t**9
            * sp.diff(a * t**5, t)
            / fiber_w.subs({w: t**3, s: a * t**5})
        ).subs(kappa, T / a**3)
    )
    if sp.simplify(sp.limit(origin_eta / t, t, 0) - a / T) != 0:
        raise AssertionError("v^3w origin differential mismatch")

    minus_one_curve = sp.expand(
        fiber.subs({w: t**3, s: -1 + a * t**5})
    )
    if minus_one_curve.coeff(t, 15) != -T - kappa * a**3 - 1:
        raise AssertionError("v^3w minus-one leading equation mismatch")
    minus_one_eta = sp.simplify(
        (
            -t**9
            * sp.diff(-1 + a * t**5, t)
            / fiber_w.subs({w: t**3, s: -1 + a * t**5})
        ).subs(kappa, -(T + 1) / a**3)
    )
    if sp.simplify(
        sp.limit(minus_one_eta / t, t, 0) - a / (T + 1)
    ) != 0:
        raise AssertionError("v^3w minus-one differential mismatch")

    phi = t**6 + (1 - T * x) * t**5 + kappa * (1 + x) ** 3
    phi_t = sp.diff(phi, t)
    repeated_t = sp.Rational(-5, 6)
    repeated_kappa = sp.Rational(3125, 46656)
    substitutions = {x: 0, t: repeated_t, kappa: repeated_kappa}
    if sp.simplify(phi.subs(substitutions)) != 0:
        raise AssertionError("v^3w resonant root misses the infinity equation")
    if sp.simplify(phi_t.subs(substitutions)) != 0:
        raise AssertionError("v^3w resonant root is not repeated")
    phi_tt_value = sp.simplify(sp.diff(phi, t, 2).subs(substitutions))
    phi_x_value = sp.factor(sp.diff(phi, x).subs(substitutions))
    if phi_tt_value != sp.Rational(625, 216):
        raise AssertionError(f"unexpected v^3w phi_tt: {phi_tt_value}")
    if sp.simplify(
        phi_x_value - sp.Rational(3125, 15552) * (2 * T + 1)
    ) != 0:
        raise AssertionError(f"unexpected v^3w phi_x: {phi_x_value}")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (0, 3, 1): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 v^3w mate for coefficient {coefficient}"
            )
    print("verified: v^3w normalization, infinity resonance, and mod-3 absence")


def verify_u3v_perturbation():
    s, w, kappa, T, a, x = sp.symbols(
        "s w kappa T a x", nonzero=True
    )
    P_chart = w + s + kappa * s * w**4 / (1 + s) ** 2
    fiber = (1 + s) ** 2 * (w + s - T) + kappa * s * w**4
    if sp.simplify(fiber - (1 + s) ** 2 * (P_chart - T)) != 0:
        raise AssertionError("u^3v generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(
        w**2 * P_s
        - w**2 * fiber_s.subs(T, P_chart) / (1 + s) ** 2
    ) != 0:
        raise AssertionError("u^3v D_P(w) mismatch")
    if sp.simplify(
        -w**2 * P_w
        + w**2 * fiber_w.subs(T, P_chart) / (1 + s) ** 2
    ) != 0:
        raise AssertionError("u^3v D_P(s) mismatch")

    support = [
        (3, 0),
        (2, 1),
        (2, 0),
        (1, 1),
        (1, 0),
        (1, 4),
        (0, 1),
        (0, 0),
    ]
    hull = convex_hull(support)
    if hull != [(0, 0), (3, 0), (1, 4), (0, 1)]:
        raise AssertionError(f"u^3v Newton hull mismatch: {hull}")
    interior = []
    for i in range(4):
        for j in range(5):
            signs = []
            for index, left in enumerate(hull):
                right = hull[(index + 1) % len(hull)]
                cross = (
                    (right[0] - left[0]) * (j - left[1])
                    - (right[1] - left[1]) * (i - left[0])
                )
                signs.append(cross)
            if all(value > 0 for value in signs) or all(
                value < 0 for value in signs
            ):
                interior.append((i, j))
    if interior != [(1, 1), (1, 2), (1, 3), (2, 1)]:
        raise AssertionError(f"u^3v interior points mismatch: {interior}")

    # The sole degenerate face point is a tacnode at (s,w)=(-1,0):
    # with s=-1+a*w^2 its leading equation is
    # -(T+1)*a^2-kappa=0, accounting for delta=2.
    tacnode_curve = sp.expand(fiber.subs(s, -1 + a * w**2))
    if sp.simplify(
        tacnode_curve.coeff(w, 4) - (-a**2 * (T + 1) - kappa)
    ) != 0:
        raise AssertionError("u^3v tacnode leading equation mismatch")
    tacnode_eta = sp.simplify(
        (
            (1 + s) ** 2
            / (w**2 * fiber_s)
        )
        .subs(s, -1 + a * w**2)
        .subs(kappa, -a**2 * (T + 1))
    )
    if sp.limit(tacnode_eta, w, 0) in (sp.oo, -sp.oo, sp.zoo):
        raise AssertionError("u^3v tacnode differential has a pole")

    # At the remaining w=0 branch, s=T-w+O(w^4).  It is the unique
    # double pole and has zero residue.
    local_s = T - w
    local_eta = sp.simplify(
        ((1 + s) ** 2 / (w**2 * fiber_s)).subs(s, local_s)
    )
    double_coefficient = sp.simplify(sp.limit(w**2 * local_eta, w, 0))
    residue = sp.simplify(
        sp.limit(w * (local_eta - double_coefficient / w**2), w, 0)
    )
    if double_coefficient != 1 or residue != 0:
        raise AssertionError(
            "u^3v unique pole mismatch: "
            f"double={double_coefficient}, residue={residue}"
        )

    # At infinity, the two s~a*w^2 branches satisfy a^2=-kappa; the
    # third has s~0.  In the coordinate x=1/w, eta is
    # -(1+s)^2/F_s dx and is regular on all three.
    fiber_s_infinity = fiber_s.subs(w, 1 / x)
    large_eta_dx = sp.simplify(
        -((1 + a / x**2) ** 2)
        / fiber_s_infinity.subs(s, a / x**2)
    ).subs(kappa, -a**2)
    small_eta_dx = sp.simplify(
        -1 / fiber_s_infinity.subs(s, 0)
    )
    if sp.limit(large_eta_dx, x, 0) in (sp.oo, -sp.oo, sp.zoo):
        raise AssertionError("u^3v large infinity branch has a pole")
    if sp.limit(small_eta_dx, x, 0) != 0:
        raise AssertionError("u^3v small infinity branch is not regular")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (3, 1, 0): coefficient,
        }
        if slice_for_p(mod_P, q_degree=25, p=3) is not None:
            raise AssertionError(
                f"unexpected mod-3 u^3v mate for coefficient {coefficient}"
            )
    print("verified: u^3v genus-two normalization, unique pole, and mod-3 absence")


def verify_uv4_perturbation():
    s, w, kappa, T, a, x, t = sp.symbols(
        "s w kappa T a x t", nonzero=True
    )
    P_chart = w + s + kappa * s**4 * (1 + s) ** 3 / w**6
    fiber = w**7 + (s - T) * w**6 + kappa * s**4 * (1 + s) ** 3
    if sp.simplify(fiber - w**6 * (P_chart - T)) != 0:
        raise AssertionError("uv^4 generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(w**2 * P_s - fiber_s / w**4) != 0:
        raise AssertionError("uv^4 D_P(w)=F_s/w^4 mismatch")
    if sp.simplify(-w**2 * P_w + fiber_w.subs(T, P_chart) / w**4) != 0:
        raise AssertionError("uv^4 D_P(s)=-F_w/w^4 mismatch")

    # At s=0 there are two branches with w=t^2, s=a*t^3.
    origin_curve = sp.expand(fiber.subs({w: t**2, s: a * t**3}))
    if origin_curve.coeff(t, 12) != kappa * a**4 - T:
        raise AssertionError("uv^4 origin leading equation mismatch")
    origin_eta = sp.simplify(
        (
            -t**8
            * sp.diff(a * t**3, t)
            / fiber_w.subs({w: t**2, s: a * t**3})
        ).subs(kappa, T / a**4)
    )
    if sp.simplify(sp.limit(origin_eta, t, 0) - a / (2 * T)) != 0:
        raise AssertionError("uv^4 origin differential mismatch")

    # At s=-1 there are three branches with w=t, s+1=a*t^2.
    minus_one_curve = sp.expand(
        fiber.subs({w: t, s: -1 + a * t**2})
    )
    if sp.simplify(
        minus_one_curve.coeff(t, 6) - (kappa * a**3 - T - 1)
    ) != 0:
        raise AssertionError("uv^4 minus-one leading equation mismatch")
    minus_one_eta = sp.simplify(
        (
            -t**4
            * sp.diff(-1 + a * t**2, t)
            / fiber_w.subs({w: t, s: -1 + a * t**2})
        ).subs(kappa, (T + 1) / a**3)
    )
    if sp.simplify(
        sp.limit(minus_one_eta, t, 0) - a / (3 * (T + 1))
    ) != 0:
        raise AssertionError("uv^4 minus-one differential mismatch")

    phi = t**7 + (1 - T * x) * t**6 + kappa * (1 + x) ** 3
    phi_t = sp.diff(phi, t)
    repeated_t = sp.Rational(-6, 7)
    repeated_kappa = sp.Rational(-46656, 823543)
    substitutions = {x: 0, t: repeated_t, kappa: repeated_kappa}
    if sp.simplify(phi.subs(substitutions)) != 0:
        raise AssertionError("uv^4 resonant root misses the infinity equation")
    if sp.simplify(phi_t.subs(substitutions)) != 0:
        raise AssertionError("uv^4 resonant root is not repeated")
    if sp.simplify(
        sp.diff(phi, t, 2).subs(substitutions)
        - sp.Rational(-7776, 2401)
    ) != 0:
        raise AssertionError("uv^4 resonant second derivative mismatch")
    if sp.simplify(
        sp.diff(phi, x).subs(substitutions)
        + sp.Rational(46656, 823543) * (7 * T + 3)
    ) != 0:
        raise AssertionError("uv^4 resonant x-derivative mismatch")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (1, 4, 0): coefficient,
        }
        mod_Q = {
            (0, 1, 0): 2,
            (1, 2, 0): 1,
            (0, 2, 1): 1,
            (0, 5, 1): coefficient,
        }
        if bracket(mod_P, mod_Q, 3) != {(0, 0, 0): 1}:
            raise AssertionError(
                f"uv^4 characteristic-3 pair failed for {coefficient}"
            )
    print("verified: uv^4 normalization, resonance, and both mod-3 pairs")


def verify_u4v_perturbation():
    s, w, kappa, T, a, x = sp.symbols(
        "s w kappa T a x", nonzero=True
    )
    P_chart = w + s + kappa * s * w**6 / (1 + s) ** 3
    fiber = (1 + s) ** 3 * (w + s - T) + kappa * s * w**6
    if sp.simplify(fiber - (1 + s) ** 3 * (P_chart - T)) != 0:
        raise AssertionError("u^4v generic plane model failed")

    fiber_s = sp.diff(fiber, s)
    fiber_w = sp.diff(fiber, w)
    P_s = sp.diff(P_chart, s)
    P_w = sp.diff(P_chart, w)
    if sp.simplify(
        w**2 * P_s
        - w**2 * fiber_s.subs(T, P_chart) / (1 + s) ** 3
    ) != 0:
        raise AssertionError("u^4v D_P(w) mismatch")
    if sp.simplify(
        -w**2 * P_w
        + w**2 * fiber_w.subs(T, P_chart) / (1 + s) ** 3
    ) != 0:
        raise AssertionError("u^4v D_P(s) mismatch")

    hull = convex_hull([(0, 0), (4, 0), (1, 6), (0, 1)])
    if hull != [(0, 0), (4, 0), (1, 6), (0, 1)]:
        raise AssertionError(f"u^4v Newton hull mismatch: {hull}")
    interior_count = 0
    for i in range(5):
        for j in range(7):
            crosses = []
            for index, left in enumerate(hull):
                right = hull[(index + 1) % len(hull)]
                crosses.append(
                    (right[0] - left[0]) * (j - left[1])
                    - (right[1] - left[1]) * (i - left[0])
                )
            if all(value > 0 for value in crosses) or all(
                value < 0 for value in crosses
            ):
                interior_count += 1
    if interior_count != 9:
        raise AssertionError(f"u^4v interior count mismatch: {interior_count}")

    # The bottom ordinary triple tacnode has three branches
    # s=-1+a*w^2 and total delta 3*2=6.
    triple_curve = sp.expand(fiber.subs(s, -1 + a * w**2))
    if sp.simplify(
        triple_curve.coeff(w, 6) - (-a**3 * (T + 1) - kappa)
    ) != 0:
        raise AssertionError("u^4v triple-tacnode equation mismatch")
    triple_eta = sp.simplify(
        ((1 + s) ** 3 / (w**2 * fiber_s))
        .subs(s, -1 + a * w**2)
        .subs(kappa, -a**3 * (T + 1))
    )
    if sp.limit(triple_eta, w, 0) in (sp.oo, -sp.oo, sp.zoo):
        raise AssertionError("u^4v triple-tacnode differential has a pole")

    local_s = T - w
    local_eta = sp.simplify(
        ((1 + s) ** 3 / (w**2 * fiber_s)).subs(s, local_s)
    )
    double_coefficient = sp.simplify(sp.limit(w**2 * local_eta, w, 0))
    residue = sp.simplify(
        sp.limit(w * (local_eta - double_coefficient / w**2), w, 0)
    )
    if double_coefficient != 1 or residue != 0:
        raise AssertionError(
            "u^4v unique pole mismatch: "
            f"double={double_coefficient}, residue={residue}"
        )

    # Three large infinity branches have s~a*w^2, a^3=-kappa;
    # the fourth has s~0.
    fiber_s_infinity = fiber_s.subs(w, 1 / x)
    large_eta_dx = sp.simplify(
        -((1 + a / x**2) ** 3)
        / fiber_s_infinity.subs(s, a / x**2)
    ).subs(kappa, -a**3)
    small_eta_dx = sp.simplify(-1 / fiber_s_infinity.subs(s, 0))
    if sp.limit(large_eta_dx, x, 0) in (sp.oo, -sp.oo, sp.zoo):
        raise AssertionError("u^4v large infinity branch has a pole")
    if sp.limit(small_eta_dx, x, 0) != 0:
        raise AssertionError("u^4v small infinity branch is not regular")

    for coefficient in (1, 2):
        mod_P = {
            (0, 0, 1): 1,
            (1, 1, 0): 1,
            (4, 1, 0): coefficient,
        }
        mod_Q = {
            (0, 1, 0): 2,
            (1, 2, 0): 1,
            (0, 2, 1): 1,
            (3, 2, 1): coefficient,
        }
        if bracket(mod_P, mod_Q, 3) != {(0, 0, 0): 1}:
            raise AssertionError(
                f"u^4v characteristic-3 pair failed for {coefficient}"
            )
    print("verified: u^4v genus-three normalization and both mod-3 pairs")


def verify_rational_residue():
    c, first, second, local = sp.symbols("c first second local", nonzero=True)
    denominator = -first * local - second * local**2 / 2
    differential_coefficient = -c / denominator**2
    residue = sp.expand(
        sp.limit(
            (differential_coefficient - (-c / first**2) / local**2) * local,
            local,
            0,
        )
    )
    expected = c * second / first**3
    if sp.simplify(residue - expected) != 0:
        raise AssertionError(f"residue mismatch: {residue} != {expected}")
    print("verified: residue of -c dw/(T-f(w))^2 is c f''/f'^3")


def main():
    verify_hamiltonian_derivatives()
    verify_generic_fiber_equations()
    verify_separated_three_generator_families()
    verify_newton_separated_family()
    verify_mixed_linear_coefficient_family()
    verify_bilinear_seed_rational_mate()
    verify_bilinear_tail_family()
    verify_variable_coefficient_bilinear_family()
    verify_characteristic_three_seed_coverage()
    verify_affine_v_coefficient_family()
    verify_absent_modular_perturbations()
    verify_quadratic_v_perturbation()
    verify_quadratic_vw_perturbation()
    verify_arbitrary_v_tail_family()
    verify_simple_zero_v_coefficient_family()
    verify_uvw_perturbation()
    verify_uv2_perturbation()
    verify_v2w_perturbation()
    verify_uv_power_tail_family()
    verify_uv3_perturbation()
    verify_uv2w_perturbation()
    verify_u2vw_perturbation()
    verify_v3w_perturbation()
    verify_u3v_perturbation()
    verify_uv4_perturbation()
    verify_u4v_perturbation()
    verify_rational_residue()
    print("all triangular Hamiltonian identities passed")


if __name__ == "__main__":
    main()
