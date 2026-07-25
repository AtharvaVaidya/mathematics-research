#!/usr/bin/env python3
"""Shear-correct global audit of the five surviving delta=1 cells.

The exact characteristic-zero conclusions are:

* (7,11) and (5,8): empty;
* analytic-quadratic (4,14): entirely composite;
* analytic-quadratic (3,10): the required order-10 coefficient vanishes
  on the radical, hence the actual cell is empty.

For (3,5), this script records only the original modular diagnostic.
The later companion ``route_bd_ab_delta1_35_wronskian.py`` supplies the
exact characteristic-zero proof.

Singular is used only after triangular approximate-root reduction.
"""

from __future__ import annotations

import shutil
import subprocess

import sympy as sp


h = sp.symbols("h")
a = sp.symbols("a0:8")
b = sp.symbols("b0:12")


def triangular_data() -> tuple[sp.Expr, sp.Expr, sp.Poly]:
    A = h**8 + sum(a[index] * h**index for index in range(8))
    trial = h**12 + sum(b[index] * h**index for index in range(12))
    initial = sp.Poly(sp.expand(trial**2 - A**3), h)
    solved: dict[sp.Symbol, sp.Expr] = {}
    for degree in range(23, 11, -1):
        equation = sp.expand(initial.coeff_monomial(h**degree).subs(solved))
        variable = b[degree - 12]
        answers = sp.solve(equation, variable)
        assert len(answers) == 1
        solved[variable] = sp.factor(answers[0])
    B_tilde = sp.expand(trial.subs(solved))
    remainder = sp.Poly(sp.expand(B_tilde**2 - A**3), h)
    return A, B_tilde, remainder


def numerator(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(expression).as_numer_denom()[0])


def singular_expression(expression: sp.Expr) -> str:
    return str(expression).replace("**", "^")


def run_singular(program: str, timeout: int = 90) -> str:
    executable = shutil.which("Singular")
    assert executable is not None, "Singular is required for this verifier"
    completed = subprocess.run(
        [executable, "-q"],
        input=program,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=True,
    )
    assert completed.stderr == ""
    return completed.stdout.strip()


def fractional_system(
    A: sp.Expr,
    B_tilde: sp.Expr,
    remainder: sp.Poly,
    m: int,
    n: int,
) -> tuple[list[sp.Expr], tuple[sp.Symbol, ...], sp.Expr]:
    substitutions = {a[index]: 0 for index in range(1, m)}
    substitutions[a[m]] = 1
    normalized_A = sp.expand(A.subs(substitutions))
    normalized_B = sp.expand(B_tilde.subs(substitutions))

    # Completing the square in the general cubic replaces the original
    # B by B_tilde=B+ell*A+constant.  The cell conditions belong to B,
    # so ell must be retained.  Its value is forced by the h^m term.
    tangent = normalized_B.coeff(h, m)
    original_B = sp.expand(normalized_B - tangent * normalized_A)
    equations = [
        original_B.coeff(h, degree)
        for degree in range(1, n)
    ]
    equations.extend(
        remainder.coeff_monomial(h**degree).subs(substitutions)
        for degree in (11, 10, 9)
    )
    equations = [numerator(eq) for eq in equations if eq != 0]
    variables = tuple([a[0], *[a[index] for index in range(m + 1, 8)]])
    leading = numerator(original_B.coeff(h, n))
    return equations, variables, leading


def quadratic_system(
    A: sp.Expr,
    B_tilde: sp.Expr,
    remainder: sp.Poly,
    m: int,
    contact: int,
) -> tuple[list[sp.Expr], tuple[sp.Symbol, ...], sp.Expr]:
    c2, c3 = sp.symbols("c2 c3")
    substitutions = {a[index]: 0 for index in range(1, m)}
    substitutions[a[m]] = 1
    normalized_A = sp.expand(A.subs(substitutions))
    normalized_B = sp.expand(B_tilde.subs(substitutions))
    x = normalized_A - normalized_A.subs(h, 0)
    tangent = normalized_B.coeff(h, m)
    transverse = sp.expand(
        normalized_B
        - normalized_B.subs(h, 0)
        - tangent * x
        - c2 * x**2
        - c3 * x**3
    )
    equations = [
        transverse.coeff(h, degree) for degree in range(1, contact)
    ]
    equations.extend(
        remainder.coeff_monomial(h**degree).subs(substitutions)
        for degree in (11, 10, 9)
    )
    equations = [numerator(eq) for eq in equations if eq != 0]
    variables = tuple(
        [a[0], *[a[index] for index in range(m + 1, 8)], c2, c3]
    )
    leading = numerator(transverse.coeff(h, contact))
    return equations, variables, leading


def ring_and_ideal(
    equations: list[sp.Expr],
    variables: tuple[sp.Symbol, ...],
    characteristic: int = 0,
) -> tuple[str, str]:
    names = ",".join(map(str, variables))
    generators = ",".join(singular_expression(eq) for eq in equations)
    return f"ring r={characteristic},({names}),dp;", f"ideal I={generators};"


def verify_empty_fractional_cells(
    A: sp.Expr, B_tilde: sp.Expr, remainder: sp.Poly
) -> None:
    for m, n in ((7, 11), (5, 8)):
        equations, variables, _leading = fractional_system(
            A, B_tilde, remainder, m, n
        )
        ring, ideal = ring_and_ideal(equations, variables)
        output = run_singular(
            f"{ring} {ideal} ideal G=std(I); "
            'print("FIRST"); print(G[1]); quit;'
        )
        assert output == "FIRST\n1"


def verify_quadratic_414_is_composite(
    A: sp.Expr, B_tilde: sp.Expr, remainder: sp.Poly
) -> None:
    equations, variables, _leading = quadratic_system(
        A, B_tilde, remainder, 4, 14
    )
    a0, a5, a6, a7, c2, c3 = variables
    expected = (
        a5,
        a6,
        a7,
        2 * c2 + c3 - 1,
        12 * a0 + 8 * c2 - 9,
    )
    ring, ideal = ring_and_ideal(equations, variables)
    expected_text = ",".join(singular_expression(eq) for eq in expected)
    output = run_singular(
        'LIB "primdec.lib"; '
        f"{ring} {ideal} ideal R=radical(I); "
        f"ideal E={expected_text}; "
        "ideal R1=reduce(E,std(R)); ideal R2=reduce(R,std(E)); "
        'print("R1"); print(R1); print("R2"); print(R2); quit;'
    )
    assert "R1\n0,\n0,\n0,\n0,\n0" in output
    assert "R2\n0,\n0,\n0,\n0,\n0" in output

    # The radical forces A=h^8+h^4+a0, hence A and B_tilde are both
    # polynomials in h^4 and the boundary parametrization is nonprimitive.
    assert sp.factor(
        A.subs({a[1]: 0, a[2]: 0, a[3]: 0, a[4]: 1, a5: 0, a6: 0, a7: 0})
    ) == a0 + h**8 + h**4


def verify_quadratic_310_is_empty(
    A: sp.Expr, B_tilde: sp.Expr, remainder: sp.Poly
) -> None:
    equations, variables, leading = quadratic_system(
        A, B_tilde, remainder, 3, 10
    )
    ring, ideal = ring_and_ideal(equations, variables)
    leading_text = singular_expression(leading)
    output = run_singular(
        'LIB "primdec.lib"; '
        f"{ring} {ideal} ideal R=radical(I); ideal L={leading_text}; "
        "ideal Z=reduce(L,std(R)); "
        'print("LEAD"); print(Z); quit;'
    )
    assert output.endswith("LEAD\n0")


def verify_fractional_35_modular_diagnostic(
    A: sp.Expr, B_tilde: sp.Expr, remainder: sp.Poly
) -> None:
    equations, variables, leading = fractional_system(
        A, B_tilde, remainder, 3, 5
    )
    aux = sp.symbols("aux")
    augmented = [*equations, aux * leading - 1]
    augmented_variables = (*variables, aux)
    ring, ideal = ring_and_ideal(
        augmented, augmented_variables, characteristic=32003
    )
    output = run_singular(
        f"{ring} {ideal} ideal G=slimgb(I); "
        'print("MODULAR_FIRST"); print(G[1]); quit;'
    )
    assert output == "MODULAR_FIRST\n1"


def main() -> None:
    A, B_tilde, remainder = triangular_data()
    verify_empty_fractional_cells(A, B_tilde, remainder)
    verify_quadratic_414_is_composite(A, B_tilde, remainder)
    verify_quadratic_310_is_empty(A, B_tilde, remainder)
    verify_fractional_35_modular_diagnostic(A, B_tilde, remainder)
    print("verified exact emptiness of the (7,11) and (5,8) cells")
    print("verified every (4,14) point is composite")
    print("verified exact emptiness of the saturated (3,10) cell")
    print("verified modular emptiness of saturated (3,5) at p=32003")
    print("RESULT HERE: FOUR CELLS DIE EXACTLY; (3,5) IS MODULAR ONLY")
    print("COMPANION RESULT: THE WRONSKIAN VERIFIER KILLS (3,5) OVER Q")


if __name__ == "__main__":
    main()
