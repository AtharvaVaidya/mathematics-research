#!/usr/bin/env python3
"""Independent exact checks for the displayed identities in ROUTE_A_MEMO.md."""

from route_a_search import add, bracket, derivative, format_polynomial, mul, scale


ONE = {(0, 0, 0): 1}
U = {(1, 0, 0): 1}
V = {(0, 1, 0): 1}
W = {(0, 0, 1): 1}


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}\nactual:   {format_polynomial(actual)}\n"
            f"expected: {format_polynomial(expected)}"
        )
    print("verified:", label)


def check_generator_brackets():
    assert_equal(bracket(U, V), {(0, 0, 1): -2}, "{u,v}=-2w")
    assert_equal(bracket(U, W), {(2, 0, 0): -1}, "{u,w}=-u^2")
    assert_equal(
        bracket(V, W),
        {(0, 0, 0): 1, (1, 1, 0): 2},
        "{v,w}=1+2uv",
    )


def check_characteristic_three_and_first_lift():
    p0 = W
    q0 = {(0, 1, 0): 2, (1, 2, 0): 1}
    expected_seed = {(0, 0, 0): -2, (1, 1, 0): -6, (2, 2, 0): -3}
    assert_equal(bracket(p0, q0), expected_seed, "integer seed bracket")
    assert_equal(bracket(p0, q0, 3), ONE, "characteristic-3 seed bracket")

    first_a = {(1, 1, 1): 2, (2, 2, 1): 2}
    first_b = {(0, 1, 0): 2, (3, 4, 0): 2}
    target = {(0, 0, 0): 1, (1, 1, 0): 2, (2, 2, 0): 1}
    lhs = add(bracket(first_a, q0, 3), bracket(p0, first_b, 3), 3)
    assert_equal(lhs, target, "first Hensel equation modulo 3")

    lifted_p = add(p0, scale(first_a, 3))
    lifted_q = add(q0, scale(first_b, 3))
    error = add(bracket(lifted_p, lifted_q), {(0, 0, 0): -1})
    if not all(coefficient % 9 == 0 for coefficient in error.values()):
        raise AssertionError("first integer lift is not a solution modulo 9")
    print("verified: first integer lift modulo 9")


def check_symplectic_primitive():
    theta_u = {(0, 2, 1): -4}
    theta_v = {(0, 0, 1): 1, (1, 1, 1): -2}
    theta_w = {(0, 1, 0): 2, (1, 2, 0): 4}

    coeff_uv = add(derivative(theta_v, 0), scale(derivative(theta_u, 1), -1))
    coeff_uw = add(derivative(theta_w, 0), scale(derivative(theta_u, 2), -1))
    coeff_vw = add(derivative(theta_w, 1), scale(derivative(theta_v, 2), -1))

    # Any two-form A du^dv+B du^dw+C dv^dw equals
    # (-2w A-u^2 B+(1+2uv)C) Omega.
    scalar = add(
        add(
            mul({(0, 0, 1): -2}, coeff_uv),
            mul({(2, 0, 0): -1}, coeff_uw),
        ),
        mul({(0, 0, 0): 1, (1, 1, 0): 2}, coeff_vw),
    )
    assert_equal(scalar, ONE, "d beta=Omega in Kahler differentials")


def check_plane_cover():
    def xy_add(a, b):
        out = dict(a)
        for m, c in b.items():
            out[m] = out.get(m, 0) + c
            if not out[m]:
                del out[m]
        return out

    def xy_mul(a, b):
        out = {}
        for (i, j), c in a.items():
            for (k, ell), d in b.items():
                out[i + k, j + ell] = out.get((i + k, j + ell), 0) + c * d
        return {m: c for m, c in out.items() if c}

    def xy_derivative(a, variable):
        out = {}
        for m, c in a.items():
            exponent = m[variable]
            if exponent:
                mm = list(m)
                mm[variable] -= 1
                out[tuple(mm)] = c * exponent
        return out

    def jacobian(a, b):
        return xy_add(
            xy_mul(xy_derivative(a, 0), xy_derivative(b, 1)),
            {m: -c for m, c in xy_mul(xy_derivative(a, 1), xy_derivative(b, 0)).items()},
        )

    u = {(2, 0): 1}
    v = {(0, 1): 4, (2, 2): 4}
    w = {(1, 0): 1, (3, 1): 2}
    if xy_mul(w, w) != xy_add(u, xy_mul(xy_mul(u, u), v)):
        raise AssertionError("the cover does not satisfy the surface equation")
    print("verified: pi lands in B")

    expected = [
        ({(0, 0, 1): -2}, jacobian(u, v)),
        ({(2, 0, 0): -1}, jacobian(u, w)),
        ({(0, 0, 0): 1, (1, 1, 0): 2}, jacobian(v, w)),
    ]
    substitutions = {
        (0, 0, 0): {(0, 0): 1},
        (1, 0, 0): u,
        (0, 1, 0): v,
        (0, 0, 1): w,
        (2, 0, 0): xy_mul(u, u),
        (1, 1, 0): xy_mul(u, v),
    }
    for poisson, plane_jacobian in expected:
        pulled_back = {}
        for monomial, coefficient in poisson.items():
            term = substitutions[monomial]
            pulled_back = xy_add(pulled_back, {m: -4 * coefficient * c for m, c in term.items()})
        if plane_jacobian != pulled_back:
            raise AssertionError("J(pi^*f,pi^*g)=-4*pi^*{f,g} failed")
    print("verified: plane Jacobian is -4 times the pulled-back bracket")


def main():
    check_generator_brackets()
    check_characteristic_three_and_first_lift()
    check_symplectic_primitive()
    check_plane_cover()
    print("all Route A identity checks passed")


if __name__ == "__main__":
    main()
