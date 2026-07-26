# Cubic pseudoplane exclusion

This directory contains a standalone research-note draft proving

\[
\text{there is no étale morphism }
S(2,2,1)\longrightarrow \mathbb A^2_{\mathbb C}
\text{ of geometric degree }3,
\]

where

\[
S(2,2,1)
=\operatorname{Spec}
\mathbb C[u,v,w]/(w^2-u-u^2v).
\]

The draft includes the full cubic normalization and log-topology collapse
used by the final homology-line and monodromy contradiction. It does not
cite internal research notes as proof premises.

## Contents

- `main.tex` — self-contained theorem statement and proof, limited plane
  Keller corollary, literature comparison, scope limitations, references,
  and AI/human-verification disclosure.
- The exact diagnostic verifiers remain under `current_context/`; they are
  not duplicated here.

## Build

With a standard LaTeX distribution:

```bash
cd papers/cubic-pseudoplane-exclusion
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is unavailable:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Verification

From the repository root:

```bash
.venv/bin/python \
  current_context/verify_route_a_log_topology_cubic_collapse.py
.venv/bin/python \
  current_context/verify_route_a_contractible_retained_sheet_cubic_exclusion.py
```

These scripts check elementary algebra, finite fiber types, Euler-balance
arithmetic, and the final subgroup obstruction. The completion,
plumbing, Alexander--Lefschetz duality, normalization, Zaidenberg, and
Abhyankar--Moh--Suzuki inputs remain theorem-level arguments.

## Exact scope

The result also excludes geometric-degree-six plane Keller maps whose
coordinate pair factors through the canonical quadratic chart
\(\mathbb A^2\to S(2,2,1)\) and has a cubic second stage.

It does **not**:

- exclude arbitrary geometric-degree-six plane Keller maps;
- improve a total polynomial-degree bound for arbitrary Keller maps; or
- prove the two-dimensional Jacobian conjecture.

Dubouloz--Palka's nonproper étale maps are endomorphisms
\(S(2,2,1)\to S(2,2,1)\), so they do not conflict with this result.
Miyanishi's earlier no-map theorem for sources mapping to
\(\mathbb A^2\) covers \(\mathrm{ML}_0\) pseudoplanes, whereas
\(S(2,2,1)\) is \(\mathrm{ML}_1\). His later lecture theorem for
pseudoplanes of type \((d,n,r)\) excludes \(r\ne2\); this surface has
\(r=2\), the exceptional case not settled by that canonical-divisor
argument.

## Review status

This is a preprint-ready research draft, not a submitted or
human-refereed paper. Two adversarial proof-review passes found no
remaining fatal or major mathematical issue after the manuscript added
explicit singular-duality, local-branch, local-monodromy, and quadratic
chart arguments. OpenAI Codex assisted with symbolic verification,
literature discovery, drafting, and those review passes. The named
author retains responsibility for all claims.

Before submission:

1. obtain an independent human line-by-line proof check;
2. perform a broader MathSciNet/zbMATH and expert novelty review; and
3. compile under a full TeX distribution and inspect the rendered PDF.
