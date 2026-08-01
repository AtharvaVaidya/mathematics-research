# Universal separation makes every marked cycle trace attainable

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE LINEAR REDUCTION / COMPONENT TOPOLOGY STILL
OPEN**.

This note records a consequence of universal Tait separation that is
stronger than the previously used existence of one binary cycle
containing every mark.  It does not resolve the five-cycle double cover
conjecture.

## 1. Statement

Let \(H\) be a connected finite cubic graph with a proper
three-edge-colouring, and let \(S\) be a universally separated edge
matching.  Thus no bichromatic circuit in any proper
three-edge-colouring contains two members of \(S\).

Let
\[
 \rho_S:Z_1(H;\mathbb F_2)\longrightarrow\mathbb F_2^S
\]
be restriction of a binary cycle to the marked coordinates.

> **Marked trace-surjectivity theorem.**
> Under these hypotheses:
>
> 1. no nonempty cut of \(H\) is contained in \(S\);
> 2. \(H-S\) is connected; and
> 3. \(\rho_S\) is surjective.
>
> Consequently, for every prescribed subset \(R\subseteq S\), there is
> a binary cycle \(Q_R\) such that
> \[
>             Q_R\cap S=R.                              \tag{1}
> \]

Parallel edges cause no change if binary two-circuits and the usual
edge-object conventions are used.  A Tait-colourable cubic multigraph
has no loop, because a loop uses the same colour twice at its incident
vertex.

## 2. Arbitrary mark precolouring

Universal separation first gives the standard mark-precolouring lemma.
Every map
\[
             \sigma:S\longrightarrow\{a,b,c\}
\]
extends to a proper three-edge-colouring of \(H\).

Indeed, begin with any Tait colouring.  To change the colour of a mark
\(e\) from \(p\) to \(q\), switch \(p,q\) on the unique
\(pq\)-bichromatic circuit through \(e\).  Universal separation says
that this circuit contains no other mark.  Processing the marks one at
a time realizes the prescribed map without changing marks already
processed.

## 3. No marked cut

Suppose for a contradiction that
\[
             \varnothing\ne D=\delta_H(X)\subseteq S.    \tag{2}
\]
Put \(k=|D|\).  In every Tait colouring, the number \(d_i\) of
colour-\(i\) edges in this cut satisfies
\[
             d_i\equiv |X|\equiv k\pmod2                \tag{3}
\]
for each \(i\in\{a,b,c\}\).  The first congruence follows by summing the
degrees of the colour-\(i\) perfect matching over \(X\); the second
follows from
\[
             3|X|=2|E(H[X])|+|\delta_H(X)|.
\]

If \(k\) is odd, prescribe every edge of \(D\) colour \(a\).  The three
cut-colour counts then have parities \((1,0,0)\), contradicting (3).
If \(k\) is even, then \(k\ge2\); prescribe one edge colour \(a\), the
other \(k-1\) edges colour \(b\), and none colour \(c\).  Their parities
are \((1,1,0)\), again contradicting (3).  The precolouring lemma says
both prescriptions extend, so (2) is impossible.

Deleting \(S\) disconnects \(H\) if and only if a component shore after
deletion has a nonempty boundary contained in \(S\).  The preceding
paragraph therefore also proves that \(H-S\) is connected.

## 4. Cycle-space duality

Use the standard dot product on \(\mathbb F_2^{E(H)}\).  The orthogonal
complement of the binary cycle space is the cut space:
\[
             Z_1(H;\mathbb F_2)^\perp=B^1(H;\mathbb F_2).
                                                               \tag{4}
\]
If \(\rho_S\) were not surjective, some nonzero
\(y\in\mathbb F_2^S\) would annihilate its image.  Extend \(y\) by zero
on \(E(H)\setminus S\).  Equation (4) would make this extended vector a
nonzero cut-space vector supported inside \(S\).

Every nonzero binary cut-space vector is itself the incidence vector of
a nonempty cut \(\delta_H(X)\).  This would contradict Section 3.
Hence \(\rho_S\) has rank \(|S|\), proving surjectivity and (1).

Equivalently, every fibre below is a nonempty affine subspace, and the
standard rank identity gives its affine dimension:
\[
 \operatorname{affdim}\{Q\in Z_1(H;\mathbb F_2):Q\cap S=R\}
       =\dim Z_1(H;\mathbb F_2)-|S|                    \tag{5}
\]
for every \(R\subseteq S\).

## 5. Exact limit of the lemma

Taking \(R=S\) proves that some binary cycle contains all marks.  This
is strictly weaker than the two-\(T\)-join packing condition needed by
five-CDC: different circuit components of that binary cycle may still
contain odd numbers of marks.

The retained 44-vertex four-mark countermodel in
`extremal-marked-core-reduction.md` satisfies the theorem and still has
no all-mark binary cycle whose components are all marked-even.  Thus no
component-parity conclusion may be inferred from surjectivity alone.

For the connected eight-mark branch, (5) removes the entire linear
mark-containment issue in the full binary cycle space.  Any remaining
obstruction is necessarily in the way the selected edges join into
circuit components.  For a fixed selected cycle, this component-parity
condition is equivalently a signed-balance or
\(\mathbb F_2\)-holonomy condition.  Within the smaller family of cycles
obtained as symmetric differences of selected \(ac\)- and
\(bc\)-circuits, the exact selector/holonomy formulation is the one in
`eight-mark-bichromatic-code.md`.  That restricted incidence code need
not equal the full binary cycle space.

## AI-use disclosure

This lemma and exposition were developed by an OpenAI Codex agent under
human direction.  The proof is fully displayed so it can be checked
without trusting an AI system or a finite computation.  No claim of
five-CDC resolution or human peer review is made.
