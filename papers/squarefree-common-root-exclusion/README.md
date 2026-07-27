# Squarefree common-root exclusion

This directory contains a standalone draft of:

> Atharva Vaidya, *Squarefree Common-Root Boundaries for Reciprocal
> Keller Pairs* (26 July 2026).

The theorem excludes one boundary architecture in the reciprocal
homogenization of a plane Keller pair.  It is not a proof of the
two-dimensional Jacobian conjecture.  Its conclusion is that a reciprocal
Keller pair whose boundary is
\[
P(X,0)=R(X)^a,\qquad Q(X,0)=R(X)^b
\]
cannot have squarefree \(R\).  Repeated-root boundaries remain outside the
theorem.

The source is [`main.tex`](main.tex).  From the repository root, compile
with any recent LaTeX distribution, for example:

```sh
tectonic papers/squarefree-common-root-exclusion/main.tex
```

The algebraic companion checks referenced in Appendix A are:

```text
current_context/verify_standard_system_single_binomial_face_no_scalar.py
current_context/verify_standard_system_strict_compact_face_bridge.py
current_context/verify_standard_system_squarefree_common_root_exclusion.py
current_context/verify_standard_system_repeated_root_compact_face.py
current_context/verify_standard_system_repeated_root_global_first_layer.py
current_context/verify_standard_system_repeated_root_kummer_nonlinear_audit.py
```

They use exact SymPy arithmetic.  They check displayed bracket identities,
weight gaps, reciprocal-degree bookkeeping, and finite integer lemmas; they
do not replace the proof.

The checked `main.pdf` was compiled from this source with Tectonic and
visually inspected page by page before release.
