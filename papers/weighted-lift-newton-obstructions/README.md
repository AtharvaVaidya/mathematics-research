# Newton-vertex obstructions for the weighted lift

This directory contains a standalone computer-assisted research-note draft
proving a nonhomogeneous target theorem for polynomial-graph descents of the
Gallagher weighted lift.

For the exact second-subduction coordinate \(\mathcal U\), every polynomial
graph, every target polynomial \(R(A,B,C)\) of degree at most two, and every
nonconstant \(Q(A,B,C)\) of degree at most eleven satisfy

\[
J_{x,y}(\mathcal U+R,Q)\notin\mathbb C^\times.
\]

The same conclusion holds in arbitrary target degree when no two support
exponents of \(Q\) differ by a nonzero multiple of
\((5,-6,4)\). Exact triangular replacements by products of \(T,W,U\)
resolve the primitive cusp collision and all its multiples through degree
eleven.
Degree eight remains sharp only for the collision-free criterion:
\(B^6\) and \(A^5C^4\) are the primitive colliding pair.

## Contents

- `main.tex` — self-contained definitions, theorem statements, boundary
  proof, exact-computation interface, scope limitations, and disclosure.
- `main.pdf` — compiled manuscript.
- Exact symbolic checks remain in `current_context/` so there is one
  canonical implementation of every certificate.

## Verification

From the repository root:

```bash
.venv/bin/python \
  current_context/verify_weighted_lift_degree_six_graph_projection_no_go.py
.venv/bin/python \
  current_context/verify_weighted_lift_global_minimal_boundary_face_closure.py
.venv/bin/python \
  current_context/verify_weighted_lift_nonhomogeneous_newton_vertex_closure.py
.venv/bin/python \
  current_context/verify_weighted_lift_nonhomogeneous_degree_nine_cusp_closure.py
.venv/bin/python \
  current_context/verify_weighted_lift_nonhomogeneous_degree_ten_newton_basis_closure.py
.venv/bin/python \
  current_context/verify_weighted_lift_nonhomogeneous_degree_eleven_newton_basis_closure.py
.venv/bin/python \
  current_context/verify_weighted_lift_sagbi_saturation_next_generator_audit.py
```

The first verifier checks the three-dimensional Keller identity. The second
expands the exact seed and checks all 77 terms of the second-subduction
numerator and the uniform seed gaps. The third checks the Newton-vertex
identities, endpoint formulas, lattice kernel, primitive degree cutoff, and
first-coordinate separation. The fourth checks the exact degree-nine
\(T\)-replacement. The fifth checks the four degree-ten collision classes,
triangular basis, augmented regular atoms, and exceptional polar Wronskian.
The sixth checks all ten degree-eleven collision classes, the exact
augmented basis, regular \(L=1\) gaps, polar-face exhaustion, both
resonant rays, and their local Laurent-jet determinants. The seventh is
a scope audit: it proves that the known five boundary
generators are not yet a complete SAGBI basis.

The immutable repository view for this manuscript is:

<https://github.com/AtharvaVaidya/mathematics-research/tree/weighted-lift-newton-obstructions-v3>

The degree-eight and degree-ten versions remain archived immutably at
<https://github.com/AtharvaVaidya/mathematics-research/tree/weighted-lift-newton-obstructions-v1>
and
<https://github.com/AtharvaVaidya/mathematics-research/tree/weighted-lift-newton-obstructions-v2>.

## Build

With a standard TeX distribution:

```bash
cd papers/weighted-lift-newton-obstructions
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is unavailable, run `pdflatex` twice.

The archived PDF was built with Tectonic in an isolated container:

```bash
docker run --rm --platform linux/amd64 \
  --mount "type=bind,src=$PWD,dst=/data" -w /data \
  dxjoke/tectonic-docker:latest-alpine-biber tectonic main.tex
```

## Scope and review status

This is a preprint research draft, not a submitted or human-refereed paper.
It excludes one broad descent architecture; it does not prove the
two-dimensional Jacobian conjecture and does not construct a counterexample.

The underlying theorem note and the repaired standalone manuscript passed
adversarial independent proof reviews with no remaining fatal or major
mathematical issue. A targeted current web/arXiv search found no matching
polynomial-graph Newton-vertex theorem, but that is not a priority claim.
The v3 PDF compiles without errors and passed a fresh page-by-page visual
inspection. Before submission, obtain a human line-by-line proof check
and perform a broader MathSciNet/zbMATH novelty review.
