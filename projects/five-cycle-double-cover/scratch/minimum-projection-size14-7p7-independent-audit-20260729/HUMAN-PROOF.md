# Independent proof for the size-fourteen \(7+7\) branch

Date: 2026-07-29

Status: **EXACT \(7+7\) BRANCH THEOREM / NOT A FIVECYCLE-DOUBLE-COVER
RESOLUTION**.

## 1. Statement and exact scope

Let \(G\) be a finite loopless cubic multigraph and let
\[
                     f=(h,q):E(G)\longrightarrow
                     \mathbb F_2\times\mathbb F_2^2
\]
be a nowhere-zero flow.  Suppose that the support \(H\) of \(h\) is the
disjoint union of two 7-circuits.  In the terminology of the
minimum-projection project, assume that this projection is globally
cardinality-minimum among all extendable projections of \(G\).

Then its \(7+7\) boundary state is cleanable.

This is a theorem only about this support shape in loopless cubic
multigraphs.  It allows parallel edges.  It does not cover loops,
noncubic graphs, any other size-fourteen shape, or support size greater
than fourteen.  On its own it does not prove FiveCDC.

## 2. Boundary model

Write \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition denoted by xor.
Orientations are immaterial in characteristic two.  Number the support
edges on the two circuits by
\[
       A=(0,\ldots,6),\qquad B=(7,\ldots,13),
\]
and let \(c_i\in K\) be the low value \(q\) on support edge \(i\).  At
the support vertex between edges \(i-1\) and \(i\), the unique
off-support edge has low value
\[
                              d_i=c_{i-1}+c_i.       \tag{1}
\]
It is nonzero because its first coordinate is zero and \(f\) is
nowhere zero.

Delete the support edges.  The remaining graph has degree one at each
of the fourteen displayed support vertices and degree three at every
other vertex.  Partition the displayed vertices according to their
connected component.  If \(S\) is one block, flow conservation gives
\[
                              \bigoplus_{i\in S}d_i=0. \tag{2}
\]

The independent census generates valid blocks in a deliberately
different way.  For each low colour \(\mu\), let \(p_\mu(S)\) be the
parity of support edges of colour \(\mu\) crossing between \(S\) and its
complement in \(A\mathbin{\dot\cup}B\).  Telescoping (1) gives
\[
       \bigoplus_{i\in S}d_i
       =\bigoplus_{\substack{e\in\delta_H(S)}}c_e.    \tag{3}
\]
The cut of a union of circuits has even size.  In the Klein four group,
the right side of (3) is zero exactly when
\[
                         p_0(S)=p_1(S)=p_2(S)=p_3(S). \tag{4}
\]
Thus the cut-parity block generator is exactly equivalent to the
zero-charge rule (2), without reusing the primary derivative-subset
generator.  A block is dirty precisely when this common parity is one.

Exact covers by valid blocks generate each component partition once:
at every recursion step the block containing the least uncovered
position is selected.

## 3. Complete independent census

The word generator independently enumerates proper cyclic four-colour
words, quotients by first-occurrence colour normalization, independent
dihedral actions on the two circuits, and interchange of the equal
circuits.  It obtains 333 word orbits.

This word list is exhaustive for a globally minimum state.  Equation
(1) makes adjacent support colours unequal, so both cyclic words are
proper.  If either circuit omitted one of the four low colours, the
translation-and-deletion operation in Section 6 would already decrease
the support.  Global minimality therefore forces both 7-circuit words
to use all four colours, exactly as required by the generator.

For every valid partition, the census tests all componentwise linear
automorphisms of \(K\).  There are six such automorphisms.  A common
postcomposition changes no clean-or-delete answer, so the map on the
first component is normalized to the identity.  The transformed
derivatives are integrated around both support circuits.  The four
relative translations of the second circuit are tested for cleanliness.
A circuit whose integrated word omits one of the four low colours is
recorded as deletable.

The complete independent result is

| quantity | exact value |
|---|---:|
| word orbits | 333 |
| charge-valid partitions | 91,481,505 |
| dirty states | 80,104,020 |
| direct-cleaning failures | 37,463 |
| failures of both cleaning and deletion | 224 |

The sorted 224-row failure set has SHA-256

```text
eec4d091247385ab4aef5c567e52377062d6a7eae8f68e988069c1a3920215ca
```

and agrees exactly with the independently parsed primary failure set.
Every row has five complement components.  Their size profiles are
\[
     46\text{ rows of }6+2+2+2+2,\qquad
     178\text{ rows of }4+4+2+2+2.                  \tag{5}
\]

## 4. The two-colour path lemma

Fix a complement component \(W\) and two distinct nonzero colours
\(x,y\in K\).  Retain in \(W\) only edges whose low value is \(x\) or
\(y\).

At every internal vertex of \(W\), the three incident low values are
nonzero and xor to zero.  They are therefore \(1,2,3\), one each, so
the retained degree is two.  At a displayed boundary vertex \(i\), the
retained degree is one exactly when \(d_i\in\{x,y\}\).  Consequently
the retained subgraph is a disjoint union of circuits and paths, and
its paths pair the selected boundary occurrences in a perfect matching.

Put \(\Delta=x+y\).  Interchanging \(x\) and \(y\) on one retained path
adds \(\Delta\) to both path edges at every internal vertex and hence
preserves the low-flow equation.  It adds \(\Delta\) to the boundary
derivative at each of the two endpoints.  All switched off-support
values remain nonzero.

If the endpoints lie on one support circuit, the two additions cancel
in its derivative sum.  If they lie on different support circuits, add
a compensating switch in another complement component having exactly
two selected boundary occurrences, one on each circuit.  Its retained
subgraph has exactly two path endpoints, so a path between them is
forced.  The second switch adds another \(\Delta\) to each circuit and
restores both derivative sums.

The loopless cubic hypothesis is used here.  It makes every internal
retained degree two and every selected boundary degree one.  This proof
does not silently extend to loops or arbitrary vertex degrees.

## 5. Why all perfect matchings are the right quantifier

For fixed \(W,x,y\), let \(S\) be its selected boundary occurrences.
The actual, unknown realization induces one perfect matching \(P_W\)
of \(S\), namely the endpoint pairs of its retained paths.  The finite
checker enumerates every abstract perfect matching of \(S\), a
superset that certainly contains \(P_W\).

For a candidate strategy it computes a set \(R\) of endpoint pairs
having literal deletion certificates.  It accepts the strategy only
after checking
\[
                         P\cap R\ne\varnothing
             \quad\hbox{for every perfect matching }P\text{ of }S. \tag{6}
\]
Applying (6) to the actual \(P_W\), one actual Kempe path has endpoints
in \(R\).  Switch that path, and use its recorded compensation if
needed.  Thus enumerating all terminal perfect matchings is sufficient;
it does not assume that an arbitrary terminal pair is joined by a path.
Enumerating matchings that no graph realizes is harmless because it
only strengthens (6).

Across the 224 states, the independent checker verifies 984
perfect-matching obligations.  Its deterministically selected
strategies contain 1,566 good endpoint-pair certificates: 750 need no
compensation and 816 use a forced two-terminal compensating path.
Every one of the 1,566 certificates is a deletion certificate; none
relies on a direct-clean verdict.

## 6. Why a recorded certificate really decreases the support

After the path switch, apply the recorded linear automorphism to every
low value in each complement component.  Linearity preserves every
internal flow equation and nonzero values.  The checker verifies the
two circuit derivative sums and integrates the displayed low values on
the support.

Suppose the integrated word on one 7-circuit omits \(\mu\in K\).
Add \(\mu\) to every low value on that circuit.  This preserves flow
conservation because two incident circuit edges change at every
circuit vertex.  No translated low value is zero.  Now set the first
coordinate to zero on the entire circuit.  Its two first-coordinate
contributions also cancel at every vertex, all edge values remain
nonzero, and the first-coordinate support decreases from fourteen
edges to seven.

Therefore none of the 224 census failures can occur in a globally
cardinality-minimum extendable projection.  Every other dirty \(7+7\)
state was already classified by the complete census as directly clean
or deletable.  A charge-valid block has all four cut-colour parities
equal by (4), so a state with no dirty block is already clean with the
original word.  A globally minimum \(7+7\) projection is consequently
cleanable.

## 7. Trust boundary and AI disclosure

The package contains a separate word-orbit generator, a cut-parity
valid-block exact-cover census, a second semantic evaluator for all 224
rows, universal terminal-matching checks, and full literal map/base/
missing-colour certificates.  The proof still relies on the broader
project's already stated equivalence between boundary cleanliness and
the relevant minimum-projection cleaning move; that general affine
lemma is not reproved here.

OpenAI Codex agents under human direction found and checked this
argument and wrote the software and exposition.  The complete sources,
data, certificates, and hashes are included so the claims can be
checked without trusting an AI-generated summary.  No independent
human peer review has yet occurred.
