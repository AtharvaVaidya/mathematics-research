# Connected cubic-cover exclusion at normal degrees (9,6)

This directory contains a standalone draft of:

> Atharva Vaidya, *A Connected Cubic-Cover Exclusion at Normal Degrees
> (9,6)* (26 July 2026).

The theorem concerns a plane Keller pair with \(y\)-degrees \(9\) and
\(6\), whose leading \(y\)-coefficients are constant multiples of
\(h^3\) and \(h^2\). It excludes the connected cubic-cover chart, in
which \(h\) is not a cube in \(\mathbb C(x)\).

The result is deliberately scoped. It does not cover the chart in which
\(h\) is a cube (including constant \(h\)); it does not prove or
disprove the two-dimensional Jacobian conjecture. The arithmetic
discussion locating \((9,6)\) is a repackaging of prior partial- and
total-degree criteria, not a new degree-classification theorem.

The checked PDF is [`main.pdf`](main.pdf), and its source is
[`main.tex`](main.tex). From the repository root, compile with a recent
LaTeX distribution, for example:

```sh
tectonic papers/normal-degree-96-connected-exclusion/main.tex
```

The exact symbolic companion is:

```text
current_context/verify_normal_degree_arithmetic_frontier_and_96_connected_reduction.py
```

It checks the displayed expansions, derivative identities, centered
factorization, branch formulas, resultant, cusp Jacobian, valuation
identity, and the small arithmetic enumeration. It is a regression
check and does not replace the proof.

The literature statement in the draft is intentionally conservative:
within a scoped audit of the five cited sources, no prior theorem was
located that states this connected noncube-\(h\) exclusion. This is not
an absolute priority claim.
