#!/usr/bin/env python3
"""Exact characteristic-zero obstruction for the final a/b (3,5) cell.

Keep the degree-12 approximate root T instead of first substituting its
dense triangular formulas.  If

    D = T^2 - A^3

has degree at most eight, then

    T * (2*A*T' - 3*A'*T) = A*D' - 3*A'*D

forces the Wronskian W=2*A*T'-3*A'*T to have degree at most three.
The local (3,5) conditions are b1=b2=0 and b4=b3*a4.  The coefficients
W_18,...,W_12 solve successively for b11,...,b5.  This leaves eight
equations in seven variables.

The script checks the a7=0 chart is empty over Q.  On a7!=0 it makes an
invertible coordinate change and uses Singular's certified modular primary
decomposition over Q.  The radical is the coordinate plane

    z=y=x=v=r=0,  u*t=1.

In the original variables this says

    a5=0,  a7^2=4*a6,  a4*a7=2,

with two further linear relations.  The contact-five coefficient
b5-b3*a5 reduces to zero modulo both checked primary components.  It
therefore belongs to the original closure ideal itself, so the saturated
(3,5) cell is empty.
"""

from __future__ import annotations

import shutil
import subprocess

import sympy as sp

from route_bd_ab_delta1_five_cell_global import singular_expression


def numerator(expression: sp.Expr) -> sp.Expr:
    return sp.expand(sp.together(expression).as_numer_denom()[0])


def run_singular(program: str, timeout: int = 900) -> str:
    executable = shutil.which("Singular")
    assert executable is not None, "Singular is required"
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


def build_wronskian_system() -> dict[str, object]:
    h = sp.symbols("h")
    a0, a4, a5, a6, a7 = sp.symbols("a0 a4 a5 a6 a7")
    b = sp.symbols("b0:12")

    A = (
        h**8
        + a7 * h**7
        + a6 * h**6
        + a5 * h**5
        + a4 * h**4
        + h**3
        + a0
    )
    T = h**12 + sum(b[index] * h**index for index in range(12))
    D = sp.expand(T**2 - A**3)
    W = sp.expand(2 * A * sp.diff(T, h) - 3 * sp.diff(A, h) * T)

    assert sp.expand(
        T * W - (A * sp.diff(D, h) - 3 * sp.diff(A, h) * D)
    ) == 0

    # The (3,5) tangent conditions for B=T-b3*A.
    local = {b[1]: 0, b[2]: 0, b[4]: b[3] * a4}
    w_poly = sp.Poly(W.subs(local), h)
    assert w_poly.degree() == 18

    # Since T is monic, deg(T*W)<=15 implies W_18=...=W_4=0.
    rows = {
        degree: sp.expand(w_poly.coeff_monomial(h**degree))
        for degree in range(4, 19)
    }
    solved: dict[sp.Symbol, sp.Expr] = {}
    for degree, variable in (
        (18, b[11]),
        (17, b[10]),
        (16, b[9]),
        (15, b[8]),
        (14, b[7]),
        (13, b[6]),
        (12, b[5]),
    ):
        equation = sp.expand(rows[degree].subs(solved))
        answers = sp.solve(equation, variable)
        assert len(answers) == 1
        solved[variable] = sp.factor(answers[0])

    residual = [
        numerator(rows[degree].subs(solved))
        for degree in range(11, 3, -1)
    ]
    leading = sp.factor((b[5] - b[3] * a5).subs(solved))
    return {
        "h": h,
        "a": (a0, a4, a5, a6, a7),
        "b": b,
        "A": A,
        "T": T,
        "D": D,
        "W": W,
        "rows": rows,
        "solved": solved,
        "residual": residual,
        "leading": leading,
    }


def verify_a7_zero_is_empty(data: dict[str, object]) -> None:
    a0, a4, a5, a6, a7 = data["a"]
    b = data["b"]
    residual = data["residual"]
    variables = (a0, a4, a5, a6, a7, b[0], b[3])
    names = ",".join(map(str, variables))
    generators = ",".join(
        singular_expression(equation) for equation in (*residual, a7)
    )
    output = run_singular(
        f"ring R=0,({names}),dp; "
        f"ideal I={generators}; ideal G=slimgb(I); "
        'print("FIRST"); print(G[1]); quit;'
    )
    assert output == "FIRST\n1"


def transformed_system(
    data: dict[str, object],
) -> tuple[list[sp.Expr], tuple[sp.Symbol, ...], sp.Expr]:
    a0, a4, a5, a6, a7 = data["a"]
    b = data["b"]
    residual = data["residual"]
    leading = data["leading"]

    r, v, x, y, z, u, t, q = sp.symbols("r v x y z u t q")
    a4_value = (x + 2) * u
    a6_value = (t**2 - y) / 4
    a0_value = (8 * q - 3 * a4_value + r) * u / 6
    b0_value = (6 * a0_value - a4_value * q + v) * u / 3
    substitutions = {
        a7: t,
        a4: a4_value,
        a6: a6_value,
        a5: z,
        a0: a0_value,
        b[0]: b0_value,
        b[3]: q,
    }

    # These are the inverse coordinate definitions on u*t=1:
    # x=a4*a7-2, y=a7^2-4*a6, z=a5,
    # r=6*a0*a7+3*a4-8*b3,
    # v=3*a7*b0+a4*b3-6*a0.
    inverse_checks = (
        a4 * a7 - 2 - x,
        a7**2 - 4 * a6 - y,
        a5 - z,
        6 * a0 * a7 + 3 * a4 - 8 * b[3] - r,
        3 * a7 * b[0] + a4 * b[3] - 6 * a0 - v,
    )
    for check in inverse_checks:
        pulled_back = sp.expand(check.subs(substitutions).subs(u, 1 / t))
        assert sp.cancel(pulled_back) == 0

    equations = [
        numerator(equation.subs(substitutions))
        for equation in residual
    ]
    equations.append(u * t - 1)
    transformed_leading = numerator(leading.subs(substitutions))
    variables = (r, v, x, y, z, u, t, q)
    return equations, variables, transformed_leading


def verify_localized_radical(
    equations: list[sp.Expr],
    variables: tuple[sp.Symbol, ...],
    transformed_leading: sp.Expr,
) -> tuple[int, int, int]:
    r, v, x, y, z, u, t, _q = variables
    expected = (z, y, x, v, r, u * t - 1)

    # The desired contact coefficient vanishes on the expected radical.
    assert sp.expand(
        transformed_leading.subs({r: 0, v: 0, x: 0, y: 0, z: 0})
    ) == 0

    names = ",".join(map(str, variables))
    generators = ",".join(
        singular_expression(equation) for equation in equations
    )
    expected_text = ",".join(
        singular_expression(equation) for equation in expected
    )
    target_text = singular_expression(transformed_leading)
    program = (
        'LIB "modprimdec.lib"; '
        f"ring R=0,({names}),dp; "
        f"ideal I={generators}; ideal E={expected_text}; "
        f"ideal Target={target_text}; "
        # modPrimdecGTZ performs its exact final decomposition check by
        # default.  Intersecting the associated primes gives radical(I),
        # including any embedded primes without relying on their order.
        "list L=modPrimdecGTZ(I); "
        "ideal Rad=L[1][2]; int i; "
        "for(i=2;i<=size(L);i++){Rad=intersect(Rad,L[i][2]);} "
        "ideal A=reduce(Rad,std(E)); ideal B=reduce(E,std(Rad)); "
        # The target is stronger than merely radical membership: it reduces
        # to zero modulo every exact primary component, hence belongs to
        # their checked intersection I itself.
        'print("COMPONENTS"); print(size(L)); '
        'print("RAD_TO_EXPECTED"); print(A); '
        'print("EXPECTED_TO_RAD"); print(B); '
        "for(i=1;i<=size(L);i++){"
        'print("TARGET_COMPONENT"); print(i); '
        "print(reduce(Target,std(L[i][1])));"
        "} quit;"
    )
    output = run_singular(program)
    assert "COMPONENTS\n2" in output
    assert "RAD_TO_EXPECTED\n0,\n0,\n0,\n0,\n0,\n0" in output
    assert "EXPECTED_TO_RAD\n0,\n0,\n0,\n0,\n0,\n0" in output
    assert "TARGET_COMPONENT\n1\n0" in output
    assert "TARGET_COMPONENT\n2\n0" in output
    return 2, len(expected), 2


def main() -> None:
    data = build_wronskian_system()
    verify_a7_zero_is_empty(data)
    equations, variables, transformed_leading = transformed_system(data)
    components, radical_generators, target_primary_remainders = (
        verify_localized_radical(
            equations,
            variables,
            transformed_leading,
        )
    )
    print("Wronskian degree bound: 3")
    print("top triangular rows solved: W18 through W12")
    print("a7=0 chart: empty over Q")
    print("localized primary components:", components)
    print("localized radical generators:", radical_generators)
    print(
        "zero target remainders on primary components:",
        target_primary_remainders,
    )
    print("contact-five coefficient: in the exact Q closure ideal")
    print("RESULT: CONTACT-FIVE LEAD IS IN THE CLOSURE IDEAL OVER Q")


if __name__ == "__main__":
    main()
