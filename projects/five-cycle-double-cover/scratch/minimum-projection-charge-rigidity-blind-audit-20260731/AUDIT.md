# Adversarial audit of the charge-rigidity theorem

Date: **2026-07-31**

Verdict: **THE STATED SPECIAL-CASE THEOREM SURVIVED THE AUDIT.  THIS IS
NOT A RESOLUTION OF THE FIVE-CYCLE-DOUBLE-COVER CONJECTURE.**

This audit was written independently from the implementation in
`minimum-projection-charge-rigidity-20260731`.  The checker in this
directory does not import, execute, or share helper code with that package's
checker.  The theorem and its human proof were, necessarily, the objects
read and audited.  This is an AI-authored adversarial review, not independent
human peer review.

## 1. The two suspected failure points

Let (K=\mathbb F_2^2), let (D_{a,j}\in K) be the charge of original
block (a) on support circuit (j), and let \(\Gamma\) range over the
components of the bipartite nonzero-incidence graph of (D).  Both row and
column xors of (D) are zero.

### 1.1 Are the tensor-selected maps actually integrable?

The proof uses one map (L_\Gamma\in\operatorname{GL}(K)) for every
charge component, not one map for every original block.  For a fixed
component and circuit put

\[
 E_{\Gamma,j}=\bigoplus_{a\in A_\Gamma}D_{a,j}.
\]

This vector is always zero.  If circuit node (j) lies in \(\Gamma\), the
sum is the entire (j)-th column sum, which is zero.  If it does not lie in
\(\Gamma\), every summand is zero: a nonzero summand would itself be an
incidence edge joining (j) to \(\Gamma\).  Consequently

\[
 \bigoplus_{i\in C_j}L_{\Gamma(a(i))}d_i
 =\bigoplus_\Gamma L_\Gamma E_{\Gamma,j}=0.
\]

Thus **every** tuple of component maps is circuit-integrable.  In
particular, the tuple later selected by the tensor lemma is integrable.
There is no earlier choice of maps with which the tensor choice must be
reconciled.

This also proves the exact hypothesis needed for the tensor step: after
contracting every \(\Gamma\) to one meta-block, every meta-block has zero
charge on every circuit separately.  The multi-circuit tensor lemma is
applied once to the xor-sum of all circuit pair-functionals.  It is not
applied circuit-by-circuit with potentially incompatible choices.

### 1.2 Does the translation left kernel really decompose?

For fixed component maps, translating circuit (j) by (z_j\in K)
changes the obstruction row of block (a\in\Gamma) by

\[
 B(z_j,L_\Gamma D_{a,j}).
\]

A scalar row selector (s\in\mathbb F_2^A) is a left dependency exactly
when, for every (j),

\[
 \bigoplus_a s_aL_{\Gamma(a)}D_{a,j}=0. \tag{1}
\]

This equivalence uses only the nondegeneracy of (B).  All nonzero terms
in (1) belong to the unique incidence component containing (j); terms
from every other component are literally zero.  Inside that component the
common invertible (L_\Gamma) factors out.  Therefore the full left kernel
is the direct product

\[
 \prod_\Gamma\ker\partial_\Gamma,
\]

including the one-dimensional kernel contributed by each isolated block.
Under charge rigidity this is precisely the span of the disjoint component
indicators.  Hence the affine translation system is consistent exactly
when

\[
 R_\Gamma=\bigoplus_{a\in A_\Gamma}Q_a(0)=0
 \quad\text{for every }\Gamma. \tag{2}
\]

There is no coupling hidden in a circuit on which two components both have
occurrences: if a component does not contain that circuit node, each of its
block charges there is zero, so its translation coefficients there vanish.
Its occurrences can still contribute quadratic cross-terms, but those are
handled by the tensor step, not by the translation kernel.

## 2. Compatibility of the meta-block obstruction

The remaining equality is not merely formal.  Summing the original block
obstructions over (a\in A_\Gamma) counts a support edge internal to the
meta-block twice and a support edge crossing its boundary once.  Over
\(\mathbb F_2\), the internal contributions cancel.  Thus the obstruction
of meta-block \(\Gamma\) is exactly (R_\Gamma) in (2).

The circuitwise charge-zero tensor lemma therefore supplies one simultaneous
tuple \((L_\Gamma)_\Gamma\) for which every (R_\Gamma=0).  These are the
same common component maps used in Sections 1.1 and 1.2.  Equation (2) then
gives circuit translations making every original (Q_a) zero.

I also rechecked the tensor lemma's universal parity argument.  Its
functional \(\lambda\) has \(\lambda(1)=1\) and kills all four matrix
coordinate functions.  In the expansion of
\(\prod_\Gamma(1+R_\Gamma)\), a nonempty selected-edge graph with a leaf is
killed at that leaf.  With no leaf, the constraint that each selected
vertex chose at most one incident edge forces a disjoint union of simple
cycles; its two orientations cancel in characteristic two.  The constant
term remains.  This reasoning also covers a repeated selection of the same
edge, because Boolean edge functions satisfy (w_e^2=w_e) and the resulting
simple graph has leaves.

## 3. Other equality checks and edge cases

The polarization identity

\[
 q(x+y)+q(x)+q(y)=B(x,y),\qquad q(x_1,x_2)=x_1x_2,
\]

gives the displayed translation formula directly.  A block has even
boundary degree and zero xor in each low coordinate, so the parities of its
four low colours are equal; their common value is the (q)-sum called
(Q_a).  Componentwise maps preserve the zero total block charge.

Isolated circuits create zero columns in the translation system and can be
discarded.  An isolated block creates one zero row, whose whole scalar
domain is exactly the span of its one-entry all-ones vector; the tensor
lemma treats it as a circuitwise-balanced meta-block.  Repeated occurrences,
parallel interactions, and interaction loops do not alter any xor or
double-counting step.

The maximum-incidence-degree-two corollary is also correct.  Balance rules
out degree one.  A nontrivial component is consequently a cycle, and the two
charges at each node are equal, forcing one common nonzero charge around the
cycle.  Its scalar kernel consists only of the two constant selectors.  For
two circuits, every nonzero row is \((x,x)\); with at most three nonzero rows,
balance forces either two equal vectors or the three distinct nonzero
vectors, again leaving only the all-ones dependency.

## 4. Independent exhaustive falsification attempt

Run:

```sh
python3 -B independent_checker.py
python3 -B residual_profile_check.py
```

The first program uses 2-bit vectors and literal (2\times2) matrices.  It
does not use the original verifier's permutation representation, raw-word
loop, base-colour enumeration, or random (4\times4) sampling.

It performed the following exact checks:

* all 4,096 three-meta-block tensor systems (all 16 linear functionals on
  each of the three pairs);
* all 270,763 balanced charge tables with one through four rows and columns;
* 274,885 literal comparisons between the mapped global left kernel and the
  direct product of component kernels, including every component-map tuple
  through (3\times3) and a nonuniform deterministic tuple for every
  (4\times4) table;
* all 1,421,109 **circuit-balanced** labelled boundary states in the reported
  three-block shapes through total support length seven and four-block shapes
  through total support length six; and
* all 85,329 of those states that also satisfy the block-balance equations,
  for which it independently searched component maps and solved the
  circuit-translation equations by GF(2) elimination, then checked the
  resulting colours directly.

No counterexample was found.  The table census contained 12,285 non-rigid
tables, so the rigidity test was not vacuous.  The small semantic boundary
census happened to lie entirely in the rigid regime after its conservation
filters; this is why the separate matrix-level non-rigidity census matters.

For every semantic map trial the program separately asserts:

1. transformed derivatives close on every circuit;
2. the sum of constituent block obstructions equals the directly measured
   meta-block obstruction;
3. the translation equations are solvable if and only if all component
   obstruction sums vanish; and
4. the reconstructed translations make every original block obstruction
   zero.

The second program independently reparsed all frozen residual rows from the
size-14, size-15, and fixed-word size-16 files.  It found respectively
224, 6,036, and 8 rows.  Every row has five active charges on two circuits,
charge rank two, excess scalar-kernel nullity two, and nonzero-charge
multiplicities (3,1,1).  This confirms the new parser's finite corollary,
but does **not** reproduce or certify the upstream graph censuses that emitted
those rows.

## 5. Scope of the verdict

The audited implication is

\[
 \text{charge-rigid chosen projection}
 \Longrightarrow \text{directly clean extension}.
\]

The audit found no missing algebraic condition in that implication.  It did
not find, and the theorem does not provide, a reason that every bridgeless
graph has a charge-rigid projection.  In fact the frozen residual rows all
have the same five-block, two-circuit, excess-nullity-two core and lie outside
the theorem's hypothesis.  Publication claims must therefore describe this
as an unbounded special-case theorem and structural reduction, not as a
resolution of FiveCDC.

All audit prose and code in this directory were produced by OpenAI Codex
under human direction.  They have not received independent human peer review.
