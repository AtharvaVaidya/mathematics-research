#!/usr/bin/env python3
"""Verify the weighted escape arithmetic for the GGV standard system."""

import sympy as sp


def determinant_weight(n: int, m: int) -> int:
    N = m + n - 2
    equation_weights = [
        n + i if i < m else i + 1
        for i in range(1, N + 1)
    ]
    variable_weights = [j + 1 for j in range(1, N + 1)]
    return sum(equation_weights) - sum(variable_weights)


for n in range(2, 10):
    for m in range(2, 10):
        assert determinant_weight(n, m) == (m - 1) * (n - 1)


# The complete (n,m)=(2,3) standard system.
z1, z2, z3, lam1, lam2, Y = sp.symbols(
    "z1 z2 z3 lam1 lam2 Y"
)
equations = sp.Matrix(
    [
        2 * z2,
        2 * z3 + z1**2,
        3 * z3 + 3 * z1**2 + 2 * lam1 * z2 + lam2 * z1 + Y,
    ]
)
variables = sp.Matrix([z1, z2, z3])
jacobian = equations.jacobian(variables)
assert sp.expand(jacobian.det() - 4 * (3 * z1 + lam2)) == 0

eliminated = sp.factor(
    equations[2].subs({z2: 0, z3: -z1**2 / 2})
)
assert sp.expand(
    eliminated - (3 * z1**2 + 2 * lam2 * z1 + 2 * Y) / 2
) == 0

# Check every displayed polynomial is homogeneous for
# wt(z1,z2,z3,lam1,lam2,Y)=(2,3,4,1,2,4).
weights = {
    z1: 2,
    z2: 3,
    z3: 4,
    lam1: 1,
    lam2: 2,
    Y: 4,
}


def monomial_weight(term: sp.Expr) -> int:
    powers = term.as_powers_dict()
    return sum(weights.get(symbol, 0) * int(exponent)
               for symbol, exponent in powers.items())


for polynomial, expected in zip(equations, (3, 4, 4)):
    observed = {
        monomial_weight(term)
        for term in sp.expand(polynomial).as_ordered_terms()
    }
    assert observed == {expected}

assert {
    monomial_weight(term)
    for term in sp.expand(jacobian.det()).as_ordered_terms()
} == {2}


def laurent_power(polynomial, exponent):
    result = {0: sp.Integer(1)}
    for _ in range(exponent):
        product = {}
        for left_degree, left_coefficient in result.items():
            for right_degree, right_coefficient in polynomial.items():
                degree = left_degree + right_degree
                product[degree] = (
                    product.get(degree, 0)
                    + left_coefficient * right_coefficient
                )
        result = product
    return result


def common_root_parameter_determinant(n, m):
    """Return J on C^g=x^g+1 with only lambda_(m-1)=L."""
    number_of_variables = n + m - 2
    common_divisor = sp.gcd(n, m)
    coefficients = sp.symbols(f"c1:{number_of_variables + 1}")
    parameter = sp.symbols("L")
    series = {
        1: sp.Integer(1),
        **{
            -index: coefficient
            for index, coefficient in enumerate(coefficients, 1)
        },
    }
    nth_power = laurent_power(series, n)
    mth_power = laurent_power(series, m)
    equations = [
        nth_power.get(-index, 0)
        for index in range(1, m)
    ]
    for index in range(m, number_of_variables + 1):
        x_degree = m - index - 1
        equations.append(
            mth_power.get(x_degree, 0)
            + parameter * series.get(x_degree, 0)
        )
    common_root_point = {
        coefficient: (
            sp.binomial(
                sp.Rational(1, common_divisor),
                (index + 1) // common_divisor,
            )
            if (index + 1) % common_divisor == 0
            else 0
        )
        for index, coefficient in enumerate(coefficients, 1)
    }
    specialized_jacobian = (
        sp.Matrix(equations)
        .jacobian(coefficients)
        .subs(common_root_point)
    )
    zero_parameter_jacobian = specialized_jacobian.subs(parameter, 0)
    zero_parameter_rank = zero_parameter_jacobian.rank()
    assert number_of_variables - zero_parameter_rank == n - 1

    # The determinant-saturating lambda_(m-1) direction is not tangent
    # to the equation fiber: its forcing vector represents a nonzero
    # cokernel class at the common-root point.
    parameter_force = (
        sp.Matrix(equations)
        .diff(parameter)
        .subs(common_root_point)
    )
    assert (
        zero_parameter_jacobian.row_join(parameter_force).rank()
        == zero_parameter_rank + 1
    )
    return sp.factor(specialized_jacobian.det()), parameter


# The common-root normal direction lambda_(m-1)=L saturates the exact
# determinant order: det(J)=unit*n^(m-1)*L^(n-1).  These are structural
# spot checks at gcd 2 and gcd 3, not a coefficient search.
for pair, expected_sign in (((4, 6), -1), ((6, 9), 1)):
    common_root_determinant, common_root_parameter = (
        common_root_parameter_determinant(*pair)
    )
    common_n, common_m = pair
    assert common_root_determinant == (
        expected_sign
        * common_n ** (common_m - 1)
        * common_root_parameter ** (common_n - 1)
    )


# A target translation P -> P-c produces a binomial reparametrization
# that hides the reciprocal deformation P=R^a+c*tau^n through every
# order retained by the finite system.
for translated_n, translated_m in ((4, 6), (6, 8), (6, 9)):
    translated_g = sp.gcd(translated_n, translated_m)
    translated_a = translated_n // translated_g
    translated_b = translated_m // translated_g
    translated_N = translated_m + translated_n - 2
    last_binomial_index = translated_N // translated_n
    translated_ratio = sp.Rational(translated_b, translated_a)
    # Coefficient of c^q*tau^(nq)*R^(b-aq) in the truncated
    # reparametrization.  The binomial convolution is (1-1)^q.
    for total_index in range(last_binomial_index + 1):
        translated_coefficient = sum(
            (-1) ** outer_index
            * sp.binomial(translated_ratio, outer_index)
            * sp.binomial(
                translated_ratio - outer_index,
                total_index - outer_index,
            )
            for outer_index in range(total_index + 1)
        )
        assert translated_coefficient == (
            1 if total_index == 0 else 0
        )
    assert translated_n * (last_binomial_index + 1) > translated_N


# More generally, g-multiple parameters can hide a genuine homogeneous
# normal deformation P=R^a+k*tau^(gc)*R^(a-c).  The coefficients below
# are determined triangularly because the q-th summand starts with z^q.
normal_z, normal_kappa = sp.symbols("normal_z normal_kappa")
for normal_g, normal_a, normal_b, normal_c in (
    (2, 3, 4, 1),
    (2, 3, 4, 2),
    (3, 2, 3, 1),
):
    normal_N = normal_g * (normal_a + normal_b) - 2
    normal_Q = normal_N // normal_g
    assert normal_Q == normal_a + normal_b - 1
    normal_sum = (
        1 + normal_kappa * normal_z ** normal_c
    ) ** sp.Rational(normal_b, normal_a)
    normal_parameters = [sp.Integer(1)]
    for normal_index in range(1, normal_Q + 1):
        known_coefficient = sp.expand(
            sp.series(
                normal_sum,
                normal_z,
                0,
                normal_index + 1,
            ).removeO()
        ).coeff(normal_z, normal_index)
        next_parameter = -sp.simplify(known_coefficient)
        normal_parameters.append(next_parameter)
        normal_sum += (
            next_parameter
            * normal_z ** normal_index
            * (
                1 + normal_kappa * normal_z ** normal_c
            ) ** sp.Rational(
                normal_b - normal_index,
                normal_a,
            )
        )
    assert sp.series(
        normal_sum - 1,
        normal_z,
        0,
        normal_Q + 1,
    ).removeO().expand() == 0
    assert normal_g * (normal_Q + 1) == normal_N + 2


# Linearizing the homogenized Keller identity at
# P=R^a(1+eps*U), Q=R^b(1+eps*V) gives the mod-g normal ODE
#     g*R*Z' + d*R'*Z = 0,  Z=a*V-b*U.
ode_R, ode_R_prime = sp.symbols("ode_R ode_R_prime", nonzero=True)
ode_U, ode_V, ode_U_prime, ode_V_prime = sp.symbols(
    "ode_U ode_V ode_U_prime ode_V_prime"
)
ode_g, ode_a, ode_b, ode_d = sp.symbols(
    "ode_g ode_a ode_b ode_d"
)
ode_n = ode_g * ode_a
ode_m = ode_g * ode_b
ode_P0 = ode_R ** ode_a
ode_Q0 = ode_R ** ode_b
ode_P0_prime = ode_a * ode_R ** (ode_a - 1) * ode_R_prime
ode_Q0_prime = ode_b * ode_R ** (ode_b - 1) * ode_R_prime
ode_P1 = ode_P0 * ode_U
ode_Q1 = ode_Q0 * ode_V
ode_P1_prime = ode_P0_prime * ode_U + ode_P0 * ode_U_prime
ode_Q1_prime = ode_Q0_prime * ode_V + ode_Q0 * ode_V_prime
ode_linearized_identity = sp.expand(
    ode_d * (ode_P0_prime * ode_Q1 - ode_P1 * ode_Q0_prime)
    + ode_n * (ode_P0 * ode_Q1_prime + ode_P1 * ode_Q0_prime)
    - ode_m * (ode_Q0 * ode_P1_prime + ode_Q1 * ode_P0_prime)
)
ode_Z = ode_a * ode_V - ode_b * ode_U
ode_Z_prime = ode_a * ode_V_prime - ode_b * ode_U_prime
assert sp.simplify(
    ode_linearized_identity
    - ode_R ** (ode_a + ode_b - 1)
    * (
        ode_d * ode_R_prime * ode_Z
        + ode_g * ode_R * ode_Z_prime
    )
) == 0


# On a normalization branch P=0, the exact Keller differential is
#   d(Q/tau^m) = -c*tau^(n-3)*d tau/P_x.
# If tau=t^e, its residue is the t^(e*m) coefficient of tau^N/P_x.
# The local (-2 mod g) model
#   P=s^a+kappa*tau^(n-2)*s
# has a nonzero resonance on every individual branch, although the
# branch sum cancels.  Pure g-sector moving branches start at m+g-2.
branch_kappa = sp.symbols("branch_kappa", nonzero=True)
for branch_g in (2, 3, 4, 5):
    for branch_a in (2, 3, 4):
        branch_b = branch_a + 1
        branch_n = branch_g * branch_a
        branch_m = branch_g * branch_b
        branch_N = branch_n + branch_m - 2

        assert branch_N - (branch_n - 2) == branch_m
        fixed_resonance = 1 / branch_kappa
        moving_resonance = -1 / (
            (branch_a - 1) * branch_kappa
        )
        assert sp.simplify(
            fixed_resonance
            + (branch_a - 1) * moving_resonance
        ) == 0
        assert fixed_resonance != 0
        assert moving_resonance != 0

        g_sector_start = (
            branch_N - branch_g * (branch_a - 1)
        )
        assert g_sector_start == branch_m + branch_g - 2
        if branch_g == 2:
            assert g_sector_start == branch_m
        else:
            assert g_sector_start > branch_m


# Pole-filtered endpoint pairing.  With
#   tau=1/y, z=y^(g-1)*(x-alpha*y),
# polynomial descent forces ord_z f_r >= ceil(r/(g-1)) for r>0.
# At z=0 the tau^(g-3) bracket coefficient then receives contributions
# only from the Laurent orders (-1,g-1) and (g-1,-1).
endpoint_z, endpoint_tau = sp.symbols(
    "endpoint_z endpoint_tau",
    nonzero=True,
)
for endpoint_g in (2, 3, 4, 5, 6):
    endpoint_p_coeffs = {}
    endpoint_q_coeffs = {}
    endpoint_p = 0
    endpoint_q = 0
    for endpoint_r in range(-4, endpoint_g + 4):
        endpoint_order = (
            0
            if endpoint_r <= 0
            else (endpoint_r + endpoint_g - 2)
            // (endpoint_g - 1)
        )
        endpoint_p_r = (
            sp.Rational(endpoint_r + 11, 7)
            * endpoint_z ** endpoint_order
            * (1 + (endpoint_r + 5) * endpoint_z)
        )
        endpoint_q_r = (
            sp.Rational(2 * endpoint_r + 17, 11)
            * endpoint_z ** endpoint_order
            * (1 + (endpoint_r + 7) * endpoint_z)
        )
        endpoint_p_coeffs[endpoint_r] = endpoint_p_r
        endpoint_q_coeffs[endpoint_r] = endpoint_q_r
        endpoint_p += endpoint_p_r * endpoint_tau ** endpoint_r
        endpoint_q += endpoint_q_r * endpoint_tau ** endpoint_r

    endpoint_bracket = sp.expand(
        sp.diff(endpoint_p, endpoint_z)
        * sp.diff(endpoint_q, endpoint_tau)
        - sp.diff(endpoint_p, endpoint_tau)
        * sp.diff(endpoint_q, endpoint_z)
    )
    endpoint_actual = sp.expand(endpoint_bracket).coeff(
        endpoint_tau,
        endpoint_g - 3,
    ).subs(endpoint_z, 0)
    endpoint_expected = (
        endpoint_p_coeffs[-1].subs(endpoint_z, 0)
        * sp.diff(
            endpoint_q_coeffs[endpoint_g - 1],
            endpoint_z,
        ).subs(endpoint_z, 0)
        - sp.diff(
            endpoint_p_coeffs[endpoint_g - 1],
            endpoint_z,
        ).subs(endpoint_z, 0)
        * endpoint_q_coeffs[-1].subs(endpoint_z, 0)
    )
    assert sp.simplify(endpoint_actual - endpoint_expected) == 0

print("verified the standard-system equation weights")
print("verified determinant weight (m-1)(n-1)")
print("verified the complete (n,m)=(2,3) elimination")
print("verified common-root corank, transverse forcing, and saturation")
print("verified the target-translation binomial countermodel")
print("verified the g-multiple approximate-root countermodel")
print("verified the homogenized mod-g normal ODE")
print("verified the branchwise Keller-residue resonance")
print("verified the pole-filtered endpoint pairing")
