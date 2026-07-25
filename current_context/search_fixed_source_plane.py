#!/usr/bin/env python3
"""Counterexample search inside a fixed source plane of the 3D map.

Fix x=1 in the verified three-dimensional Keller counterexample.  The
restricted target subalgebra R=Q[a(y,z),b(y,z),c(y,z)] is noninjective:
an exact quadratic-field collision is verified below.  Thus any pair
U,V in R with Jac_(y,z)(U,V)=1 would be an immediate plane counterexample.

This script performs exact linear slice searches.  For every small integral
linear Hamiltonian U in a documented finite set, it tests every V that is a
target polynomial of total degree at most MAX_TARGET_DEGREE.  Failure is a
bounded result only.
"""

from itertools import product

import sympy as sp


y, z = sp.symbols("y z")
x = sp.Integer(1)

a = sp.expand((1 + x * y) ** 3 * z + y**2 * (1 + x * y) * (4 + 3 * x * y))
b = sp.expand(y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y**2 * (4 + 3 * x * y))
c = sp.expand(2 * x - 3 * x**2 * y - x**3 * z)


def jacobian(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, y) * sp.diff(right, z)
        - sp.diff(left, z) * sp.diff(right, y)
    )


# Exact collision over Q(theta), theta^2-3theta-6=0.
theta = sp.symbols("theta")
theta_relation = theta**2 - 3 * theta - 6
source_z = sp.cancel((6 * theta + 8) / (3 * theta + 6))
other_z = sp.cancel(source_z - 3 * theta)


def reduce_theta(expression: sp.Expr) -> sp.Expr:
    numerator, denominator = sp.cancel(expression).as_numer_denom()
    inverse_denominator = sp.invert(
        sp.Poly(denominator, theta), sp.Poly(theta_relation, theta)
    ).as_expr()
    return sp.rem(
        sp.Poly(sp.expand(numerator * inverse_denominator), theta),
        sp.Poly(theta_relation, theta),
    ).as_expr()


first_point = {y: 0, z: source_z}
second_point = {y: theta, z: other_z}
for component in (a, b, c):
    assert reduce_theta(
        component.subs(first_point) - component.subs(second_point)
    ) == 0
assert reduce_theta(theta) != 0
print(
    "verified exact fixed-plane collision over "
    "Q(theta), theta^2-3*theta-6=0"
)


def target_monomials(degree_bound: int) -> list[sp.Expr]:
    answer = []
    for total_degree in range(1, degree_bound + 1):
        for i in range(total_degree, -1, -1):
            for j in range(total_degree - i, -1, -1):
                k = total_degree - i - j
                answer.append(sp.expand(a**i * b**j * c**k))
    return answer


def constant_in_span(polynomials: list[sp.Expr]) -> tuple[bool, int, int]:
    dictionaries = [sp.Poly(poly, y, z).as_dict() for poly in polynomials]
    rows = sorted(
        {(0, 0)}.union(
            exponent for dictionary in dictionaries for exponent in dictionary
        )
    )
    matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows),
        len(dictionaries),
        [
            [dictionary.get(exponent, 0) for dictionary in dictionaries]
            for exponent in rows
        ],
    )
    target = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows),
        1,
        [[int(exponent == (0, 0))] for exponent in rows],
    )
    rank = matrix.rank()
    augmented_rank = matrix.hstack(target).rank()
    return rank == augmented_rank, rank, augmented_rank


def constant_in_span_mod_prime(
    polynomials: list[sp.Expr], prime: int = 32003
) -> tuple[bool, int, int]:
    """A modular rank gap is an exact characteristic-zero obstruction."""

    dictionaries = [sp.Poly(poly, y, z).as_dict() for poly in polynomials]
    rows = sorted(
        {(0, 0)}.union(
            exponent for dictionary in dictionaries for exponent in dictionary
        )
    )
    matrix = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows),
        len(dictionaries),
        [
            [dictionary.get(exponent, 0) for dictionary in dictionaries]
            for exponent in rows
        ],
    ).convert_to(sp.GF(prime))
    target = sp.polys.matrices.DomainMatrix.from_list_sympy(
        len(rows),
        1,
        [[int(exponent == (0, 0))] for exponent in rows],
    ).convert_to(sp.GF(prime))
    rank = matrix.rank()
    augmented_rank = matrix.hstack(target).rank()
    return rank == augmented_rank, rank, augmented_rank


MAX_TARGET_DEGREE = 8
partner_space = target_monomials(MAX_TARGET_DEGREE)

# Primitive representatives of all nonzero coefficient triples in {-1,0,1}.
directions: list[tuple[int, int, int]] = []
for coefficients in product((-1, 0, 1), repeat=3):
    if coefficients == (0, 0, 0):
        continue
    first_nonzero = next(value for value in coefficients if value)
    if first_nonzero < 0:
        continue
    directions.append(coefficients)

for coefficients in directions:
    hamiltonian = sp.expand(
        coefficients[0] * a + coefficients[1] * b + coefficients[2] * c
    )
    bracket_columns = [
        jacobian(hamiltonian, partner) for partner in partner_space
    ]
    has_partner, rank, augmented_rank = constant_in_span_mod_prime(
        bracket_columns
    )
    if has_partner:
        raise AssertionError(
            "canonical pair found; reconstruct coefficients for "
            f"linear direction {coefficients}"
        )
    assert augmented_rank == rank + 1

print(
    f"exact modular-minor certificates exclude {len(directions)} "
    "linear target Hamiltonian "
    f"directions against all {len(partner_space)} target monomials "
    f"of degree <= {MAX_TARGET_DEGREE}"
)

# A wider exact obstruction search for genuinely nonlinear Hamiltonians.
# If a rational partner existed, the augmented rank could not jump after
# reduction at 32003.  The observed modular rank jump is therefore a valid
# characteristic-zero certificate, not a claim about finite-field geometry.
quadratic_hamiltonians = (
    a**2,
    a * b,
    a * c,
    b**2,
    b * c,
    c**2,
)
QUADRATIC_PARTNER_DEGREE = 6
quadratic_partner_space = target_monomials(QUADRATIC_PARTNER_DEGREE)
for hamiltonian in quadratic_hamiltonians:
    bracket_columns = [
        jacobian(hamiltonian, partner)
        for partner in quadratic_partner_space
    ]
    has_partner, rank, augmented_rank = constant_in_span_mod_prime(
        bracket_columns
    )
    assert not has_partner and augmented_rank == rank + 1

print(
    "modular-minor certificates exclude all six quadratic target "
    f"monomial Hamiltonians against {len(quadratic_partner_space)} "
    f"target monomials of degree <= {QUADRATIC_PARTNER_DEGREE}"
)
print(
    "RESULT: NO PAIR IN THIS BOUNDED LINEAR-HAMILTONIAN SEARCH; "
    "THE FIXED-PLANE TARGET SUBALGEBRA REMAINS A LIVE CONSTRUCTION ROUTE"
)
