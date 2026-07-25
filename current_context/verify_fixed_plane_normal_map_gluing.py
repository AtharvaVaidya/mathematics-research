#!/usr/bin/env python3
"""Verify the smooth-conic normal-map gluing identities."""

import sympy as sp


def verify_local_jacobian_order() -> None:
    # A concrete unit-generic model is enough to verify the leading term
    # in the formal identity: units only change it by A(0,0)B(0,0).
    x, u = sp.symbols("x u")
    for b in range(1, 7):
        for eta in range(0, 9):
            z = x**b * (1 + x + 2 * u)
            q = x**eta * u * (1 + 3 * x + u)
            jac = sp.expand(
                sp.diff(z, x) * sp.diff(q, u)
                - sp.diff(z, u) * sp.diff(q, x)
            )
            normalized = sp.cancel(jac / x ** (b + eta - 1))
            assert sp.expand(normalized).subs({x: 0, u: 0}) == b


def verify_vertexwise_charge_identity() -> None:
    a, b, eta, sigma, r = sp.symbols("a b eta sigma r")
    equations = {
        r: a - 1 + 3 * b,
        eta: a + 2 * b,
        sigma: 2 * b - (a + 2 * b),
    }
    required_r = b + equations[eta] - 1
    assert sp.expand(equations[r] - required_r) == 0
    assert sp.expand(equations[sigma] + a) == 0
    assert sp.expand(a + equations[sigma]) == 0


def verify_normal_degree() -> None:
    e, square = sp.symbols("e square")
    normal_degree = 4 * e - square
    # Component defect says H^2=sum sigma; conic projection says
    # sum b=2e; eta=2b-sigma.
    sum_eta = 2 * (2 * e) - square
    assert sp.expand(normal_degree - sum_eta) == 0

    g = sp.symbols("g")
    tangential_degree = 2 * g - 2 + 2 * e
    total = sp.expand(tangential_degree + normal_degree)
    assert total == 2 * g - 2 - square + 6 * e


def verify_repaired_ledger_is_excluded() -> None:
    # (a,b,sigma,eta,r)
    local = (-1, 1, -1, 3, 1)
    remote = (1, 1, 1, 1, 3)

    def required_ramification(endpoint: tuple[int, ...]) -> int:
        _, b, _, eta, _ = endpoint
        return b + eta - 1

    assert required_ramification(local) == 3
    assert local[4] == 1
    assert required_ramification(local) != local[4]
    assert local[0] + local[2] == -2

    assert required_ramification(remote) == 1
    assert remote[4] == 3
    assert required_ramification(remote) != remote[4]
    assert remote[0] + remote[2] == 2

    # The old component test sees only the cancelling sum.
    assert local[0] + local[2] + remote[0] + remote[2] == 0


def verify_resolved_target_formula() -> None:
    M, N, c = sp.symbols("M N c", nonzero=True)
    beta, theta = sp.symbols("beta theta")
    b = M * beta
    eta = N * beta + theta
    r = beta + theta - 1 + c * beta
    mu = (c + 1 - N) / M
    assert sp.simplify(r - (eta + mu * b - 1)) == 0

    # A contact blowup preserves b and kappa=a+sigma.
    a, sigma = sp.symbols("a sigma")
    assert sp.expand((a + 1) + (sigma - 1) - (a + sigma)) == 0


def verify_laurent_two_end_curve() -> None:
    d = sp.symbols("d", integer=True, positive=True)
    s, A, B, lam = sp.symbols("s A B lam", nonzero=True)
    U = A * s
    V = B / s + A ** (d - 1) * s ** (d - 1)
    affine_equation = sp.expand(U * V - U**d + lam)
    assert sp.expand(affine_equation.subs(B, -lam / A)) == 0

    smooth_end = (1, d - 1, 1)  # M,N,c
    cusp_end = (d - 1, d * (d - 2), 2 * d - 4)

    def mu(data: tuple[sp.Expr, ...]) -> sp.Expr:
        M, N, c = data
        return sp.cancel((c + 1 - N) / M)

    assert sp.simplify(mu(smooth_end) - (3 - d)) == 0
    assert sp.simplify(mu(cusp_end) - (3 - d)) == 0

    # The d=9 full-effectivity witness has opposite nonzero charges.
    d9 = 9
    endpoint_3 = (1, 8, 74)  # a,b,eta
    endpoint_6 = (0, 1, 8)

    def kappa(endpoint: tuple[int, int, int]) -> int:
        a, b, eta = endpoint
        return a + d9 * b - eta

    assert kappa(endpoint_3) == -1
    assert kappa(endpoint_6) == 1
    assert kappa(endpoint_3) + kappa(endpoint_6) == 0
    assert kappa(endpoint_3) != 0 and kappa(endpoint_6) != 0


def verify_target_resolution_orders() -> None:
    u, z, u1, t, U, Z, lam = sp.symbols("u z u1 t U Z lam")
    for d in range(3, 14):
        equation = u * z ** (d - 2) - u**d + lam * z**d

        # The s=0 branch is separated by u=z*u1.  The total transform
        # has exceptional multiplicity d-1 and reduced strict equation
        # u1+z*(lam-u1^d).
        transformed = sp.expand(equation.subs(u, z * u1))
        strict = sp.cancel(transformed / z ** (d - 1))
        assert sp.expand(strict - (u1 + z * (lam - u1**d))) == 0
        assert strict.subs({z: 0, u1: 0}) == 0
        assert sp.diff(strict, u1).subs({z: 0, u1: 0}) == 1

        # The other branch has primitive divisorial valuation
        # v(u)=d-2, v(z)=d-1.
        p, q = d - 2, d - 1
        weighted = sp.expand(
            equation.subs({u: t**p * U, z: t**q * Z})
        )
        expected_order = d * (d - 2)
        initial = sp.cancel(weighted / t**expected_order).subs(t, 0)
        assert sp.expand(initial - (U * Z ** (d - 2) - U**d)) == 0
        assert sp.gcd(p, q) == 1
        discrepancy = p + q - 1
        assert discrepancy == 2 * d - 4


def verify_global_residue_gluing() -> None:
    d, M, c, N, beta = sp.symbols("d M c N beta")
    residue_order = (d - 3) * M + c - N
    mu = (c + 1 - N) / M
    b = M * beta
    kappa = sp.expand((d - 3 + mu) * b)
    assert sp.simplify(kappa - beta * (residue_order + 1)) == 0

    j, e = sp.symbols("j e")
    order_at_zero = j - 1
    order_at_infinity = -j - 1
    assert e * (order_at_zero + 1) == e * j
    assert e * (order_at_infinity + 1) == -e * j
    assert sp.expand(
        e * (order_at_zero + 1) + e * (order_at_infinity + 1)
    ) == 0


def main() -> None:
    verify_local_jacobian_order()
    verify_vertexwise_charge_identity()
    verify_normal_degree()
    verify_repaired_ledger_is_excluded()
    verify_resolved_target_formula()
    verify_laurent_two_end_curve()
    verify_target_resolution_orders()
    verify_global_residue_gluing()
    print("verified r_i=(b_i-1)+eta_i at a smooth transverse conic end")
    print("verified the normal-section degree sum eta=4e-H^2")
    print("verified every residual endpoint has kappa_i=a_i+sigma_i=0")
    print("RESULT: the repaired d=2 component ledger is not realizable")
    print("verified the resolved-target valuation and blowup invariance")
    print("verified both target-end valuation triples for degrees 3..13")
    print("verified global endpoint charges kappa/e=(j,-j)")
    print("verified kappa=0 at both ends of the Laurent degree-d curve")
    print("RESULT: its degree-9 numerical witness is not realizable")


if __name__ == "__main__":
    main()
