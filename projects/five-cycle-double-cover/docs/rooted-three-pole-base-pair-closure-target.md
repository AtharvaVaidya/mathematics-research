# A three-base-pair closure would eliminate the cyclic-three exceptional fork

Date: **2026-07-27**.

Status: **EXACT CONDITIONAL REDUCTION / VERIFIED FINITELY THROUGH ROOTED
ORDER 17 / UNIVERSAL CLOSURE OPEN**.

Fix the ordered connector triangle
\[
                              (01,02,12)
\]
of a rooted cubic three-pole.  As in
`exceptional-cyclic-three-root-signature-factorization.md`, let
\({\cal R}(Q,r)\subseteq D_5\) be the exact set of possible labels of
the distinguished proper root \(r\).

Define the three stabilizer-invariant **base pairs**
\[
\begin{aligned}
 P_0&=\{12,03,04\},\\
 P_1&=\{02,13,14\},\\
 P_2&=\{01,23,24\}.                                  \tag{1}
\end{aligned}
\]
In the seven-orbit bit order
\[
 \{01\},\{02\},\{12\},\{03,04\},\{13,14\},\{23,24\},\{34\},
\]
their masks are respectively
\[
                         0x0c,\qquad0x12,\qquad0x21.             \tag{2}
\]

The exact universal target suggested by the rooted census is:

> **Base-pair closure target.**  
> If \(r\) is a nonbridge and
> \({\cal R}(Q,r)\ne\varnothing\), then
> \[
>                         P_i\subseteq{\cal R}(Q,r)
> \]
> for at least one \(i\in\{0,1,2\}\).

This statement is not proved.

## 1. Why it would close the surviving fork

For nonempty label sets \(R,S\subseteq D_5\), recall that
\(\operatorname{rel}(R,S)\) records equality
\(\mathsf E\), one-point intersection \(\mathsf I\), and disjointness
\(\mathsf D\) among cross-pairs.

> **Lemma 1.1 (base pairs force both mixed relations).**  
> For every \(i,j\in\{0,1,2\}\),
> \[
>                    \{\mathsf I,\mathsf D\}
>                    \subseteq\operatorname{rel}(P_i,P_j).      \tag{3}
> \]

### Proof

For \(i=j=0\), the pair \(12,03\) is disjoint and the pair \(12,13\)
does not apply because \(13\notin P_0\); instead \(03,04\) intersects
in coordinate \(0\).  Thus both relations occur within
\(P_0\times P_0\).  The cases \(i=j=1,2\) follow by permuting
coordinates \(0,1,2\).

For \(i=0,j=1\), the pair \(12,02\) intersects and the pair \(03,14\)
is disjoint.  Cyclically permuting \(0,1,2\), and swapping the two
factors when necessary, gives every case with \(i\ne j\).
\(\square\)

Only one shore actually needs a base pair.  Let the seven
\(3\leftrightarrow4\)-orbits, in their fixed order, be
\[
 O_0=\{01\},\ O_1=\{02\},\ O_2=\{12\},\
 O_3=\{03,04\},\ O_4=\{13,14\},\
 O_5=\{23,24\},\ O_6=\{34\}.                          \tag{4}
\]
Direct comparison gives the following complete table:
\[
\begin{array}{c|ccccccc}
 &O_0&O_1&O_2&O_3&O_4&O_5&O_6\\ \hline
P_0&I&I&DE&DEI&DI&DI&DI\\
P_1&I&DE&I&DI&DEI&DI&DI\\
P_2&DE&I&I&DI&DI&DEI&DI
\end{array}                                                     \tag{5}
\]
Here, for example, \(DE\) denotes
\(\{\mathsf D,\mathsf E\}\).

> **Lemma 1.2 (one-sided exceptional avoidance).**  
> If \(S\subseteq D_5\) is nonempty and invariant under
> \(3\leftrightarrow4\), then for every \(i\)
> \[
> \operatorname{rel}(P_i,S)\notin
> \bigl\{\{\mathsf E\},\{\mathsf E,\mathsf I\},
>                    \{\mathsf D\}\bigr\}.                       \tag{6}
> \]

### Proof

The set \(S\) is a nonempty union of the orbits in (4), and its
relation set is the union of the corresponding entries in row \(i\)
of (5).  No table entry is contained in \(\{\mathsf E\}\) or
\(\{\mathsf D\}\).  The only entries avoiding \(\mathsf D\) are
\(I\), whose nonempty union does not contain \(\mathsf E\).
Thus none of the three relation sets in (6) can result.
\(\square\)

> **Theorem 1.3 (conditional elimination).**  
> If the base-pair closure target holds, then no reduced
> cyclic-three-cut cap can have either exceptional four-pole
> signature.

### Proof

Lemma 4.1 of `rooted-cycle-translation-obstruction.md` proves that the
two cap roots are nonbridges of their rooted shores.  The exact
factorization theorem gives nonempty root signatures \(R,S\).
Base-pair closure supplies \(P_i\subseteq R\) for some \(i\);
closure on the second shore is not needed.  The set \(S\) is
\(3\leftrightarrow4\)-invariant.  Lemma 1.2 excludes the three
relation sets
\[
 \{\mathsf E\},\qquad
 \{\mathsf E,\mathsf I\},\qquad
 \{\mathsf D\},                                                \tag{7}
\]
which are exactly the exceptional possibilities in Corollary 3.1 of
`exceptional-cyclic-three-root-signature-factorization.md`.
\(\square\)

This would eliminate only the cyclic-three outcome of the simple-cap
fork.  A cyclically four-edge-connected exceptional cap would still
remain, so even the universal base-pair theorem would not by itself
resolve the exceptional-signature conjecture or Five-CDC.

## 2. Finite evidence

`rooted_three_pole_csp.cpp` in
`search/rooted-three-pole-frontier-20260727/` computes exact seven-orbit
root signatures.  Complete canonical `geng` enumeration of connected
simple three-pole cores through order 13 gives the following numbers of
distinct nonempty nonbridge masks:

```text
order       3   5   7   9  11  13
distinct    3   9  18  22  22  22
```

The union contains exactly 22 masks.  Its three inclusion-minimal masks
are precisely (2), and every one of the 22 contains at least one of
them.  Pairing all \(22^2\) masks produces only the relation sets
\[
                         \{\mathsf I,\mathsf D\}
 \quad\text{and}\quad
                         \{\mathsf E,\mathsf I,\mathsf D\};      \tag{8}
\]
none produces any relation in (7).

This is finite evidence, not an induction.  The next exact falsification
search is a targeted canonical census for the first nonempty nonbridge
root signature containing none of the three masks in (2).  A positive
row would refute the closure target without refuting Five-CDC.

A dedicated targeted screen has now completed the next order as well.
For all \(50\,683\) canonical order-15 cores, the direct finite-domain
and independent incremental-SAT implementations tested all
\(1\,057\,568\) nonbridge roots.  Each implementation classified
\(29\,207\) signatures as empty and \(1\,028\,361\) as containing a
base pair, with zero violations.  Their complete streamed decision
transcripts have the same SHA-256 digest

```text
07e13a0c96f9aee26c84715ea61f1843d89ec9e21e1294828c113b617e2f3570
```

The next targeted screen contains all \(654\,676\) canonical order-17
cores.  The direct finite-domain and incremental-SAT implementations
test all \(15\,645\,623\) nonbridge roots.  Each implementation
classifies \(337\,059\) signatures as empty and \(15\,308\,564\) as
containing a base pair, with zero violations.  Their eight
corresponding streamed transcript digests agree shard by shard; the
independent aggregate verifier reports \(52\,216\,251\) solver calls
per implementation.

Thus base-pair closure is an exact finite theorem through rooted order
17.  The 22-mask and cross-relation statements above remain explicitly
scoped through order 13 because the adaptive order-15 and order-17
screens stop once they find a base pair rather than computing every
complete signature.  The next falsification order is 19.

The one-sided lemma turns this finite frontier into a cap reduction.
If an even-order cap \(G\) has a cyclic three-cut of the surviving
\(2+2\) kind, its two rooted shores have odd orders \(n_1,n_2\) with
\(n_1+n_2=|V(G)|\).  For \(|V(G)|\leq36\), at least one shore has
order at most 17.  The finite base-pair theorem on that shore and
Lemma 1.2 exclude all three exceptional gluing relations, regardless
of the size or exact signature of the other shore.  Consequently:

> **Corollary 2.1 (finite cap fork through order 36).**  
> A vertex-minimal, two-cut-reduced, bridge-free connected simple
> terminal-distinct four-pole of order at most 36 with an exceptional
> exact five-colour
> signature, if one exists, has a simple cap which is cyclically
> \(4\)-edge-connected.

This corollary combines the finite order-17 theorem with the
human-checkable simple-cap fork.  It says nothing about order 38,
repeated terminals, nonsimple cores, or arbitrary multipoles.

## 3. Relation to cycle translations

Theorem 3.1 of `rooted-cycle-translation-obstruction.md` proves a
necessary condition for any counterexample to base-pair closure whose
root signature is a fixed singleton: every root cycle must use a
spanning translation-blocking label graph, hence a non-bipartite
support or \(K_{1,4}\).  The base-pair target is stronger because it
also constrains every larger nonempty root signature.  A proof needs a
global rooted reconfiguration or reducibility argument beyond a single
constant cycle translation.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the three
inclusion-minimal census masks, proved the conditional relation
elimination, and drafted this target note.  The finite computations are
not a universal proof, external novelty has not been established, and
independent human review is still required.
