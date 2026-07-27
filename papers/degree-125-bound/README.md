# Degree-125 bounded exclusion preprint

This directory contains a concise preprint draft for the exact
computer-assisted theorem

\[
\max\{\deg P,\deg Q\}\ge 125
\]

for a hypothetical noninvertible plane Keller pair over an algebraically
closed field of characteristic zero.

This is a bounded result, not a proof of the plane Jacobian conjecture.
It imports the public preprint reduction of
Guccione--Guccione--Horruitiner--Valqui (GGHV) and does not claim an
independent reproof of that reduction. An independent announcement of the
same numerical bound exists, so the draft makes no priority claim.

## Contents

- `main.tex` — theorem statement, exact external dependencies, proof
  architecture, weighted-projective specialization argument, certificate
  protocol, limitations, and references.
- The executable certificates remain at the repository root and under
  `current_context/`; they are not duplicated here.

## Build

With a standard LaTeX distribution:

```bash
cd papers/degree-125-bound
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is unavailable:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Reproduce the mathematical certificate

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python \
  current_context/verify_case_c_full_certificate_bridge.py
.venv/bin/python \
  current_context/verify_case_c_full_certificate_bridge.py \
  --run-special-fiber
.venv/bin/python route_bd_ab_hurwitz_count.py
.venv/bin/python route_bd_case_c_n3_hurwitz_bridge.py
.venv/bin/python route_bd_case_c_n3_generic_charts.py
.venv/bin/python scratch_case_c_n3_special_charts_Q.py
.venv/bin/python route_bd_universal_radial_kernel_theorem.py
.venv/bin/python route_bd_allscale_marked_cusp_obstruction.py
.venv/bin/python current_context/verify_gghv_allscale_scope.py
```

The following commands launch optional direct homogeneous
characteristic-zero generic-chart experiments:

```bash
.venv/bin/python scratch_case_c_n3_generic_charts_Q.py \
  --skip-modular-crosscheck --chart L_NE_0 --one-certificate
.venv/bin/python scratch_case_c_n3_generic_charts_Q.py \
  --skip-modular-crosscheck --chart L_EQ_0_A_NE_0 --one-certificate
```

The \(L\ne0\) homogenized run was stopped after a bounded audit window,
and no successful `HPOWER` output is archived. These experiments are not
part of the proof. The characteristic-zero theorem instead uses
emptiness of the complete finite-field weighted-projective fiber and
proper specialization.

Singular 4.4 or newer is required for the standard-basis stages. The
pinned Python dependency is SymPy 1.14.0.

## Clean-room replay requirement

Before treating a run as a publication artifact, move these runtime
caches out of `tmp/`:

```text
tmp/case_c_n3_generic_charts_Q.pkl
tmp/case_c_n3_special_charts_Q.pkl
tmp/case_c_n3_special_recurrence_Q.pkl
```

Then run the canonical reconstruction driver from the repository root:

```bash
publication_artifacts/degree-125-bound/cleanroom-2026-07-25/replay.sh
```

Archive:

1. stdout and stderr;
2. Python, SymPy, Singular, and `modstd.lib` versions;
3. SHA-256 hashes of scripts and logs;
4. the exact-to-modular coefficient comparisons and all finite-field
   standard-basis reductions; and
5. regenerated cache hashes as diagnostics, never as proof premises.

## Dependency boundary

The draft imports these results from GGHV, arXiv:2204.14178:

- Theorem 2.1;
- Proposition 4.1;
- Proposition 4.3;
- Theorem 5.1; and
- Corollary 5.7.

The new work in this repository is the elimination of both alternatives
in Proposition 4.3: the all-scale consecutive five-block obstruction and
the exact case-c weighted-projective certificate.

## Submission status

The publication bundle includes a cache-free clean-room replay with its
immutable log and software/source hashes. Before journal submission it
should additionally have:

- a repository commit or release tag matching those artifacts; and
- an independent human line-by-line check of the imported GGHV
  implications.

The source deliberately does not print the very large outer quintic.
The verifier reconstructs it exactly, checks irreducibility, and records
its complete good reduction at \(p=32003\).
