#!/usr/bin/env python3
"""Finite-field consistency probe for one r2/e3 exceptional component."""

from __future__ import annotations

import subprocess

import sympy as sp

from route_bd_case_c_constant_descent_r2 import build_d4_recurrence


recurrence, r, s, w, e = build_d4_recurrence()
for grade in (15, 14, 13):
    recurrence.introduce(grade)
rows12 = dict(recurrence.introduce(12)[0])
recurrence.substitute({e[0]: 0, e[1]: 0, e[2]: 0})
rows11 = dict(recurrence.introduce(11)[0])
rows10 = dict(recurrence.introduce(10)[0])
rows9 = dict(recurrence.introduce(9)[0])
rows8 = dict(recurrence.introduce(8)[0])

q9, q7, q5 = sp.symbols("q9_9 q7_7 q5_5")
p30, p31 = sp.symbols("p3_0 p3_1")
values = {
    e[0]: 0,
    e[1]: 0,
    e[2]: 0,
    e[3]: 1,
    r[2]: 1,
    r[3]: 0,
    r[4]: 1,
    s[0]: sp.Rational(1, 8),
    s[1]: 0,
    s[2]: 0,
    s[3]: 0,
    w[0]: 0,
    w[1]: 32,
    w[2]: 0,
    q9: 48,
    p30: 0,
    p31: sp.Rational(9, 4),
}
values[q7] = sp.solve(rows11[6].subs(values), q7)[0]
values[q5] = sp.solve(rows10[6].subs(values), q5)[0]

equations = []
equation_groups = []
for rows in (rows12, rows11, rows10, rows9, rows8):
    group = []
    for row in rows.values():
        specialized = sp.cancel(row.subs(values).subs(values))
        numerator = sp.together(specialized).as_numer_denom()[0]
        if numerator != 0:
            expanded = sp.expand(numerator)
            equations.append(expanded)
            group.append(expanded)
    equation_groups.append(group)
base_equation_count = len(equations)
pre_e8_count = sum(map(len, equation_groups[:4]))

recurrence.q[-1] = (recurrence.h + sp.symbols("t")) ** 2
identity7 = sp.expand(
    sum(
        recurrence.bracket_term(p_grade, q_grade)
        for p_grade in recurrence.p
        for q_grade in recurrence.q
        if p_grade + q_grade == 7
    )
)
identity7 = sp.expand(
    sp.cancel(identity7.subs(values).subs(values))
)
for degree in range(25):
    coefficient = sp.together(
        identity7.coeff(recurrence.h, degree)
    ).as_numer_denom()[0]
    if coefficient != 0:
        equations.append(sp.expand(coefficient))

symbols = sorted(
    set().union(*(equation.free_symbols for equation in equations)),
    key=str,
)
parameters = ()
symbols = [symbol for symbol in symbols if symbol not in parameters]
names = ",".join(map(str, symbols))
polynomials = ",\n".join(
    str(equation).replace("**", "^") for equation in equations
)
base_polynomials = ",\n".join(
    str(equation).replace("**", "^")
    for equation in equations[:base_equation_count]
)
pre_e8_polynomials = ",\n".join(
    str(equation).replace("**", "^")
    for equation in equations[:pre_e8_count]
)
e8_sequential = []
previous_e8 = "IPRE"
for index, equation in enumerate(equation_groups[4]):
    polynomial = str(equation).replace("**", "^")
    ideal_name = f"IE{index}"
    basis_name = f"GE{index}"
    e8_sequential.append(
        f"ideal {ideal_name}={previous_e8},{polynomial}; "
        f"ideal {basis_name}=std({ideal_name}); "
        f'"E8STEP_{index}"; {basis_name}[1];'
    )
    previous_e8 = ideal_name
e8_sequential_code = "\n".join(e8_sequential)
reduction_lines = "\n".join(
    f'"E7_{index}"; reduce({str(equation).replace("**", "^")},G0);'
    for index, equation in enumerate(equations[base_equation_count:])
)
sequential_lines = []
previous_ideal = "I0"
for index, equation in enumerate(equations[base_equation_count:]):
    polynomial = str(equation).replace("**", "^")
    ideal_name = f"J{index}"
    basis_name = f"H{index}"
    sequential_lines.append(
        f"ideal {ideal_name}={previous_ideal},{polynomial}; "
        f"ideal {basis_name}=std({ideal_name}); "
        f'"STEP_{index}"; {basis_name}[1];'
    )
    previous_ideal = ideal_name
sequential_code = "\n".join(sequential_lines)
elimination_product = "*".join(
    str(symbol) for symbol in symbols if str(symbol) != "p1_0"
)
print(
    "debug counts:",
    base_equation_count,
    len(equations),
    identity7 == 0,
    flush=True,
)
first_e7 = (
    str(equations[base_equation_count + 1]).replace("**", "^")
    if len(equations) > base_equation_count + 1
    else "0"
)
script = f"""
ring R=0,({names}),dp;
option(redSB);
ideal IPRE=
{pre_e8_polynomials};
{e8_sequential_code}
ideal I0=
{base_polynomials};
ideal G0=std(I0);
ideal EP=eliminate(G0,{elimination_product});
"ELIM_P1_0";
EP;
"FIRST_E7_REDUCTION";
reduce({first_e7},G0);
"""
print(
    "probe variables/equations:",
    len(symbols),
    len(equations),
    flush=True,
)
result = subprocess.run(
    ["/opt/homebrew/bin/Singular", "-q"],
    input=script,
    text=True,
    capture_output=True,
    timeout=300,
)
print(result.stdout)
print(result.stderr)
