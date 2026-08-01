# Charge-rigid multi-circuit cleaning

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE UNBOUNDED SPECIAL-CASE THEOREM / EXACT
SMALL-INSTANCE AUDIT / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

This package isolates the first genuinely multi-circuit regime in which
the universal tensor argument still proves direct cleaning.

For each complement block `a` and support circuit `j`, let

\[
 D_{a,j}=\bigoplus_{i\in a\cap j}d_i\in\mathbb F_2^2
\]

be the low-flow charge of that block on that circuit.  Join `a` to `j`
when `D[a,j]` is nonzero.  On each connected component `Gamma` of this
charge-incidence graph, form

\[
 A_\Gamma:\mathbb F_2^{A_\Gamma}\longrightarrow
 (\mathbb F_2^2)^{J_\Gamma},\qquad
 (s_a)\longmapsto
 \left(\bigoplus_a s_aD_{a,j}\right)_j.
\]

The all-ones vector is always in `ker A_Gamma`.  The main theorem is:

> If it spans that kernel on every charge-incidence component, then the
> boundary state has a directly clean extension.

There is no bound on the number or lengths of support circuits, the number
of complement blocks, or their occurrence multiplicities.

A useful purely combinatorial corollary is that direct cleaning always
exists when the charge-incidence graph has maximum degree at most two.
Every nontrivial component is then a cycle with one common nonzero charge,
and its only scalar block dependency is the all-ones dependency.  In
particular, a two-support-circuit state is directly clean whenever at most
three complement blocks have nonzero per-circuit charge.

The proof has two stages.  Give all blocks in one charge component the same
local `GL(2,2)` map.  The tensor theorem chooses those component maps so the
sum of the quadratic obstruction over each charge component vanishes.
The exact translation system is then consistent because, by hypothesis,
these component sums are every possible left-kernel obstruction.

`HUMAN-PROOF.md` writes the argument out without relying on a search.
`verify.py` independently checks the finite algebra used in the proof,
exhausts all balanced charge matrices through `3 x 3`, tests deterministic
`4 x 4` matrices, and directly brute-forces small two-circuit boundary
states.

`audit_known_residuals.py` then parses the frozen direct residual lists from
the complete size-14 and size-15 censuses and the fixed-word size-16 census.
All 6,268 rows have one and the same charge profile: five nonzero block
rows on two circuits, rank two, and excess scalar-kernel nullity two.  This
is the Petersen charged core.  The parser verifies the emitted rows; it
does not independently reproduce the much larger source censuses.

Run:

```sh
python3 -B verify.py
python3 -B audit_known_residuals.py
shasum -a 256 -c SHA256SUMS
```

This theorem does not imply that every graph has a charge-rigid projection.
The Petersen two-circuit interaction has five nonzero-charge blocks and
extra kernel nullity; it is the smallest familiar warning.  A certified
162-vertex graph elsewhere in this project has a unique minimum projection
which is uncleanable.  Thus charge rigidity is a sufficient structural
condition, not a disguised proof of FiveCDC or of the refuted
minimum-projection selection principle.

The definitions, proof, program, and prose were produced by OpenAI Codex
under human direction.  They have not received independent human peer
review.
