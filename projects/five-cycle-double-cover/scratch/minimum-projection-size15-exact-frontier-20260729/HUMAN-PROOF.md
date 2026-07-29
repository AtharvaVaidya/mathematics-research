# Human audit of the size-fifteen boundary reduction

This note explains what the finite classifier proves without asking the
reader to infer graph theory from the program.  It does **not** prove the
Five-Cycle Double Cover Conjecture.

## 1. Boundary data

Let \(G\) be a finite connected bridgeless loopless cubic multigraph and
let \(f=(h,s)\) be a nowhere-zero
\(\mathbb F_2\times\mathbb F_2^2\)-flow.  Parallel edges are allowed.
Assume that the binary cycle \(h\) has minimum cardinality among all first
coordinates of such flows.

Write \(K=\mathbb F_2^2=\{0,1,2,3\}\).  On a circuit
\(e_0,\ldots,e_{m-1}\) of \(h\), put \(c_i=s(e_i)\).  At the support
vertex between \(e_{i-1}\) and \(e_i\), the unique edge outside \(h\) has
low value
\[
                         d_i=c_{i-1}+c_i.
\]
Nowhere-zeroness makes \(d_i\ne0\), so the \(c_i\)'s form a proper cyclic
word.  The minimum-projection exchange theorem says that every circuit
uses all four values of \(K\).

Let \(\pi_i\) name the component of \(G-h\) containing that outside
edge.  Summing the low-flow equation over one component gives
\[
                     \bigoplus_{\pi_i=a}d_i=0                 \tag{1}
\]
for every block \(a\).  Conversely, the classifier deliberately keeps
every set partition satisfying (1).  Some such abstract boundary states
may have no bridgeless cubic realization; retaining them is a safe
over-approximation for a universal cleaning theorem.

## 2. Exhaustive support shapes

A circuit component has length at least four because it contains all four
affine colours.  The integer partitions of fifteen into parts at least
four are exactly
\[
\begin{gathered}
15,\quad4+11,\quad5+10,\quad6+9,\quad7+8,\\
4+4+7,\quad4+5+6,\quad5+5+5.                 \tag{2}
\end{gathered}
\]
This also excludes parallel two-circuits from a size-fifteen minimum
support: a two-circuit cannot contain all four colours.

For later comparison with size fourteen, every proper all-four-colour
cyclic word of length at least five has a removable repeated-colour
position.  Indeed, suppose the contrary.  Pick a repeated colour \(x\).
At any occurrence of \(x\), its two neighbours must then be the same
colour \(y\).  Those are distinct occurrences because the length is at
least five, so \(y\) is repeated.  Applying the same assumption at the
next \(y\) forces the following colour to be \(x\), and induction makes
the whole circuit alternate \(x,y\), contrary to the use of four colours.
Deleting the chosen occurrence preserves properness and still uses all
four colours.

If the two derivative occurrences joined by this smoothing belong to
different complement blocks, their blocks must be merged to preserve
(1).  Cleaning the merged state need not clean the two original blocks
separately.  `verify_smoothing_obstruction.py` gives a literal example:
the size-fifteen state

```text
word=01010123|0101232
partition=001234404130002
```

has 320 feasible normalized component-map tuples and no direct clean or
deletion tuple.  Smoothing the first position of its second circuit and
merging blocks 4 and 1 gives

```text
word=01010123|101232
partition=00123110130002
```

with 56 feasible tuples, 16 of them clean.  Thus size fourteen does not
settle size fifteen by a bare smoothing induction.

## 3. What the classifier exhausts

`verify_sharded.cpp` does the following.

1. It generates every proper cyclic four-colour word using all four
   colours on every circuit.
2. It quotients words by the global affine colour action, independent
   dihedral actions on the circuits, and interchange of equal-length
   circuits.  Partitions of the labelled occurrences of each canonical
   word are then enumerated exactly; partitions are not further quotiented
   by word stabilizers.
3. It generates each block of a set partition only when its derivative
   xor is zero, which is exactly (1).
4. It fixes the map on the first complement component to the identity and
   exhausts the six maps in \(\operatorname{GL}(2,2)\) on every other
   component.  Fixing the first map merely divides out a common global
   linear action.
5. It rejects map tuples whose transformed derivatives do not close on
   every support circuit.  It integrates every remaining tuple, exhausts
   the independent relative starting values on the circuits, and checks
   every component/colour boundary parity.
6. If no clean tuple exists, it records whether some integrated circuit
   omits a low colour.  Translating by that colour and deleting the
   circuit produces a strictly smaller extendable projection, contradicting
   global minimum.

The shard files are disjoint by canonical-word index modulo sixteen.
`verify_summary.py` checks shard coverage, all accounting identities,
the frozen totals, the literal number of residual rows, and a SHA-256
digest of the sorted residual rows.

## 4. Independent zero-sum partition count for one circuit

For a single support circuit put
\[
 z_i={\bf1}_{c_{i-1}=0}+{\bf1}_{c_i=0}\pmod2.
\]
For a subset \(S\) of occurrences, the parity of zero-coloured support
edges crossing \(S\) is \(\sum_{i\in S}z_i\).  Consequently:

* a component block is charge-valid exactly when its \(d_i\)-labels xor
  to zero in \(\mathbb F_2^2\); and
* it is initially clean exactly when its \((d_i,z_i)\)-labels xor to
  zero in \(\mathbb F_2^3\).

The number of zero-sum set partitions of labelled items depends only on
the multiplicities of their group labels.  To count it, choose one
distinguished remaining item.  Enumerate the multiplicities of the
other items in its zero-sum block, multiply by the corresponding
binomial coefficients, and recurse on the remaining multiplicity
vector.  Every set partition is counted exactly once because its block
containing the distinguished item is unique.

`single15_zero_sum_partition_audit.py` implements this recurrence using
three nonzero \(\mathbb F_2^2\) label types and six possible
\((d_i,z_i)\) types.  It first independently reproduces the frozen
single-circuit size-fourteen row:

```text
canonical_words=7382
charge_valid=2038187702
initially_clean=289344806
dirty=1748842896
```

It then obtains the exact size-fifteen partition totals:

```text
canonical_words=20004
charge_valid=26634745428
initially_clean=3235970836
dirty=23398774592
```

This count does not by itself prove direct cleaning.  The universal
tensor proof below supplies that theorem.  As a logically separate
finite cross-check, the completed sixteen-shard anchor/Laplacian census
tests all 23,398,774,592 dirty states and finds

```text
direct_clean=23398774592
failures=0
```

An independently written parser checks all shard identities and
terminal rows, rejects every `COUNTERSTATE` line, and verifies exact
agreement with the zero-sum recurrence.  The anchor census uses a
different cleaning algorithm but imports the primary word/partition
generator; it is therefore a cross-check, not an independent full
census.

## 5. Human tensor proof for the single-circuit row

Let \(B\) be the nondegenerate alternating form on \(K\).  The following
lemma is stronger than the boundary statement needed here.

> **Tensor lemma.** Let \(V\) be finite.  For each unordered pair
> \(\{a,b\}\), orient the pair once and fix an arbitrary linear
> functional
> \(\phi_{ab}:\operatorname{Mat}_2(\mathbb F_2)\to\mathbb F_2\).
> There are maps \(L_a\in\operatorname{GL}(2,2)\) such that the graph
> with edge indicators
> \[
>                  w_{ab}=\phi_{ab}(L_a^{-1}L_b)
> \]
> has even degree at every vertex.

The displayed orientation is fixed independently for each unordered
pair.  Reversing it causes no ambiguity: inversion on
\(\operatorname{GL}(2,2)\) is linear in the four matrix entries, so it
can be absorbed into a different linear functional.

Here is a self-contained proof.  Regard functions
\(\operatorname{GL}(2,2)\to\mathbb F_2\) as a vector space and define
\[
 \lambda(f)=f(0132)+f(0213)+f(0321),
\]
where a four-digit string lists the images of \(0,1,2,3\).  Direct
inspection gives
\[
                  \lambda(1)=1,\qquad
                  \lambda(M\mapsto M_{rs})=0
                  \quad(1\le r,s\le2).                  \tag{3}
\]
Indeed the four coordinate rows of the three displayed matrices are
\((1,0,1,1),(0,1,1,0),(1,1,0,1)\), whose xor is zero.

Put \(Q_a=\sum_{b\ne a}w_{ab}\) and
\[
                  F((L_a))=\prod_{a\in V}(1+Q_a).
\]
This is the indicator of the desired assignments.  Apply
\(\Lambda=\lambda^{\otimes V}\) after expanding \(F\).  An expansion
chooses at most one incident edge at each vertex.  Since \(w_e^2=w_e\),
group terms by the simple graph \(H\) of distinct chosen edges.

If a nonempty \(H\) has a leaf, its monomial depends on the map at that
leaf through one linear matrix-coordinate function.  This uses
\[
 \begin{pmatrix}p&q\\r&s\end{pmatrix}^{-1}
 =\begin{pmatrix}s&q\\r&p\end{pmatrix}
 \quad\text{on }\operatorname{GL}(2,2).
\]
Equation (3) kills the monomial.  If \(H\) has no leaf, let \(S\) be the
vertices that selected an edge.  Then
\[
 |E(H)|\le |S|\le |V(H)|\le |E(H)|,
\]
where the last inequality is minimum degree at least two.  Equality
holds, so \(H\) is a disjoint union of cycles and every edge is selected
exactly once.  Each cycle has two cyclic selections.  Thus the
coefficient of a nonempty \(H\) is \(2^{c(H)}=0\) in \(\mathbb F_2\).
Only the constant term survives, giving
\[
                         \Lambda(F)=\lambda(1)^{|V|}=1.
\]
Hence \(F\) is nonzero, proving the tensor lemma.

To apply it, cut the one support circuit and write
\(z_i=L_{\pi_i}d_i\).  For distinct blocks \(a,b\), set
\[
 w_{ab}=\sum_{\substack{j<i\\\pi_j=b,\ \pi_i=a}}B(z_j,z_i). \tag{4}
\]
The reverse ordering has the same value because the xor of all
\(z_i\)'s in each block is zero by (1).  Thus (4) is symmetric and
cut-independent.  Preservation of \(B\) by
\(\operatorname{GL}(2,2)\) rewrites every summand as
\[
 B(L_bd_j,L_ad_i)=B(L_a^{-1}L_bd_j,d_i);
\]
for the fixed orientation of \(\{a,b\}\), their sum is therefore a
linear functional of \(L_a^{-1}L_b\).

Finally use \(q(x_1,x_2)=x_1x_2\) and
\[
                    q(x+y)+q(x)+q(y)=B(x,y).
\]
Let \(r_i\) be the integrated colour on support edge \(e_i\), so
\(r_i=r_{i-1}+z_i\).  The parity of colour \(11\) at block \(a\) counts
both support incidences at every owned boundary vertex:
\[
 P_a=\sum_{\pi_i=a}\bigl(q(r_{i-1})+q(r_i)\bigr).
\]
If both ends of a support edge belong to \(a\), this formula counts it
twice and correctly cancels it.  Polarization gives
\[
 P_a=\sum_{\pi_i=a}q(z_i)
     +\sum_{\pi_i=a}B(r_{i-1},z_i).
\]
After cutting the circuit, write
\(r_{i-1}=r_*+\sum_{j<i}z_j\).  The base term is
\(B(r_*,\sum_{\pi_i=a}z_i)=0\) by (1).  Therefore
\[
 P_a=\sum_{\pi_i=a}q(z_i)
     +\sum_{\substack{j<i\\\pi_i=a}}B(z_j,z_i).
\]
The same-block part cancels the first sum because
\[
 0=q\left(\sum_{\pi_i=a}z_i\right)
  =\sum_{\pi_i=a}q(z_i)
   +\sum_{\substack{j<i\\\pi_j=\pi_i=a}}B(z_j,z_i).
\]
Only cross-block pairs remain, exactly
\[
                         P_a=\sum_{b\ne a}w_{ab}=Q_a.
\]
The four colour parities at a block are equal by the degree and low-flow
cut equations, so \(P_a=0\) is full cleanliness.  The tensor lemma makes
every \(Q_a\) zero, hence every charge-valid single-circuit state is
directly cleanable.  This proves the size-fifteen single-circuit row
without relying on its enumeration.

There is also a precise several-circuit corollary.  If every block is
charge-balanced **separately on every support circuit**, apply (4) on
each circuit and sum the resulting functionals for each pair.  The
total obstruction is again one tensor instance, so the same maps clean
all circuits simultaneously.  The ordinary boundary equation (1)
requires only total balance across all circuits; separate balance is a
stronger condition and is not assumed by the multi-circuit census.

The complete tensor argument and independent finite audits are frozen
in `minimum-projection-single-circuit-tensor-frontier-20260729/`.

## 6. Kempe trust boundary

For two nonzero low colours \(x,y\), the \(x/y\) subgraph inside a
complement component pairs its boundary terminals by paths.  Switching
\(x\) and \(y\) on one path adds \(x+y\) at its two endpoints.  A
certificate is realization-independent only if its successful endpoint
pairs meet every possible perfect matching of those terminals.

`kempe_game.py` implements the exact one/two-path matching game used at
size fourteen.  `verify_targeted_kempe.py` checks all 6,180 distinct
same-block one-occurrence extensions of the 224 size-fourteen residual
rows.

The full completed \(7+8\) row has 6,036 residuals.  The separately
written induction checker canonicalizes the affine colour action,
dihedral circuit actions, circuit interchange, and block renaming.  It
checks all 6,036 rows and proves that each has a same-block smoothing
canonically equivalent to a frozen size-fourteen residual and belongs
to the targeted Kempe-rescued family.  The full residual rows represent
5,200 canonical classes and have canonical digest
`f2c0c2b53322c72f00672e3f9c7d807aeb26a6ba771357a673c84c2fdaf96206`.
Thus the realization-robust targeted strategies cover every residual
emitted by the completed multi-circuit census.

Combining the human tensor theorem for shape \(15\), the exact
clean/delete classification for the other seven shapes, and the
realization-robust Kempe coverage of all 6,036 residual rows proves the
size-fifteen step.  A direct deletion or a Kempe-produced deletion
contradicts global cardinality-minimality; every remaining state is
clean.

The tensor theorem is human-checkable; the multi-circuit exhaustion is
computational and awaits independent human review.  OpenAI Codex agents
under human direction designed and ran the searches, derived the tensor
and Kempe arguments, and wrote these audit notes.
