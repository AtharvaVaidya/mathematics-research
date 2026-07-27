# The exceptional cyclic-three-cut fork has a seven-state rooted factorization

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE EXACT INTERFACE REDUCTION / THE ROOTED
SIGNATURES ARE NOT YET ELIMINATED**.

The simple-cap reduction in
`exceptional-four-pole-simple-cap-enumeration-reduction.md` leaves one
specific low-connectivity outcome.  A minimal exceptional four-pole
\(P\) has a simple cap
\[
                         G=P+\{e,f\}
\]
with a cyclic three-edge cut \(C\) disjoint from \(e,f\).  The cut
splits the four original terminals \(2+2\), and one whole cap edge lies
on each shore.

This note proves an exact factorization across \(C\).  Once the three
connector labels are normalized to a fixed triangle, each shore is
described by only seven possible orbits for its distinguished cap-edge
label.  The exceptional four-type and five-type signatures impose
sharp cross-relations on the two rooted shore signatures.

The result reduces the five-pole interface; it does not prove that the
remaining rooted signatures are unrealizable.

## 1. The rooted three-poles

Cut the three members of \(C\).  The two shores become cubic
three-poles \(Q_1,Q_2\).  The distinguished proper root edge of \(Q_1\)
is \(e\), and that of \(Q_2\) is \(f\).

In every five-coordinate partial labelling, the three ordered connector
labels \(a,b,c\in D_5=\binom{[5]}2\) satisfy
\[
                         a\mathbin\triangle
                         b\mathbin\triangle c=\varnothing.       \tag{1}
\]
They are therefore the three edges of a triangle on three coordinate
names.  Apply one global coordinate permutation and fix the ordered
connector word
\[
                         \tau=(01,02,12).                       \tag{2}
\]
The stabilizer of this ordered word fixes \(0,1,2\) and may only swap
\(3,4\).  It has seven orbits on \(D_5\):
\[
\begin{array}{c|c}
\text{class}&\text{root labels}\\ \hline
B_1&\{01\}\\
B_2&\{02\}\\
B_3&\{12\}\\
M_1&\{03,04\}\\
M_2&\{13,14\}\\
M_3&\{23,24\}\\
W&\{34\}.
\end{array}                                             \tag{3}
\]

For a rooted ordered three-pole \((Q,r)\), define
\[
 {\cal R}(Q,r)=
 \{A\in D_5:\text{\(Q\) has a partial five-coordinate labelling
 with connector word \(\tau\) and \(r\) labelled \(A\)}\}.       \tag{4}
\]
This set is a union of the seven classes in (3).

Write
\[
                         R={\cal R}(Q_1,e),\qquad
                         S={\cal R}(Q_2,f).                       \tag{5}
\]

## 2. Exact gluing

Let \(\pi\in\{2,3,4\}\) be the terminal pairing of the two ends of
each deleted cap edge.  A boundary word of \(P\) extends across both
cap edges exactly when it has the doubled form
\[
                         (A,A,B,B)                               \tag{6}
\]
in the pairing \(\pi\).  Its four-pole type is
\[
\begin{array}{c|c}
\text{relation between \(A,B\)}&\text{type}\\ \hline
A=B&AA\\
|A\cap B|=1&AT_\pi\\
A\cap B=\varnothing&T_\pi T_\pi.
\end{array}                                             \tag{7}
\]

For nonempty \(R,S\subseteq D_5\), let
\[
 \operatorname{rel}(R,S)\subseteq
 \{\mathsf E,\mathsf I,\mathsf D\}                       \tag{8}
\]
record which of equality, one-point intersection, and disjointness
occur among pairs \((A,B)\in R\times S\).

> **Theorem 2.1 (rooted cyclic-three factorization).**  
> The exact intersection of the boundary signature of \(P\) with the
> three doubled types at pairing \(\pi\) is
> \[
> \begin{split}
> {\cal C}(P)\cap\{AA,AT_\pi,T_\pi T_\pi\}
>   =\{&AA:\mathsf E\in\operatorname{rel}(R,S)\}\\
>    {}\cup\{&AT_\pi:\mathsf I\in\operatorname{rel}(R,S)\}\\
>    {}\cup\{&T_\pi T_\pi:
>                 \mathsf D\in\operatorname{rel}(R,S)\}.
>                                                               \tag{9}
> \end{split}
> \]

### Proof

Take a labelling of \(P\) of one of the three types on the left of
(9).  Its boundary word has form (6), so adding \(e\) with label \(A\)
and \(f\) with label \(B\) preserves coordinate parity at all four
terminal vertices.  Cutting \(C\) gives partial labellings of
\((Q_1,e)\) and \((Q_2,f)\) with one common ordered triangle on their
three connectors.  One global coordinate permutation normalizes that
triangle to (2), placing the transformed root labels in \(R\) and
\(S\).  Equation (7) gives the corresponding relation in (8).

Conversely, choose \(A\in R\) and \(B\in S\), take their defining
partial labellings with the identical connector word (2), and glue the
three corresponding semiedges.  Delete the two root edges while
retaining their labels on the resulting semiedges.  This is a partial
labelling of \(P\) with boundary word (6), whose type is given by (7).
Both inclusions in (9) follow. \(\square\)

## 3. Consequences for the exceptional pair

Use the notation of Máčajová--Mazzuoccolo--Tabarelli:
\[
\begin{aligned}
 {\cal E}_4(i;j,k)&=\{AA,AT_j,AT_k,T_jT_k\},\\
 {\cal E}_5(i;j,k)&=\{T_iT_i,T_jT_j,T_kT_k,T_iT_j,T_iT_k\},
                                                               \tag{10}\\
 \{i,j,k\}&=\{2,3,4\}.
\end{aligned}
\]

Intersecting (10) with the three types in (9) gives immediately:

> **Corollary 3.1 (exceptional root relations).**
>
> 1. If \(P\) has signature \({\cal E}_4(i;j,k)\) and
>    \(\pi=i\), then
>    \[
>                       \operatorname{rel}(R,S)=\{\mathsf E\}.
>                                                               \tag{11}
>    \]
> 2. If \(P\) has signature \({\cal E}_4(i;j,k)\) and
>    \(\pi\in\{j,k\}\), then
>    \[
>                       \operatorname{rel}(R,S)
>                       =\{\mathsf E,\mathsf I\}.                \tag{12}
>    \]
> 3. If \(P\) has signature \({\cal E}_5(i;j,k)\), then for every
>    \(\pi\),
>    \[
>                       \operatorname{rel}(R,S)=\{\mathsf D\}.
>                                                               \tag{13}
>    \]

In particular \(R,S\) are nonempty in all three cases.

## 4. Literal classification of the equality and disjoint cases

The sparse relations (11) and (13) have a short complete
classification.

> **Lemma 4.1 (equality only).**  
> For nonempty stabilizer-invariant \(R,S\subseteq D_5\),
> \[
>               \operatorname{rel}(R,S)=\{\mathsf E\}
> \]
> if and only if
> \[
> R=S=\{A\},\qquad
> A\in\{01,02,12,34\}.                                  \tag{14}
> \]

### Proof

If every cross-pair is equal, choose \(A\in R\).  Every member of
\(S\) equals \(A\), and then every member of \(R\) equals the chosen
member of \(S\).  Thus both sets are the same singleton.  A singleton
is invariant under the stabilizer of (2) exactly when its label is
fixed by the swap \(3\leftrightarrow4\), giving the four labels in
(14).  The converse is immediate. \(\square\)

> **Lemma 4.2 (disjointness only).**  
> For nonempty stabilizer-invariant \(R,S\subseteq D_5\),
> \[
>               \operatorname{rel}(R,S)=\{\mathsf D\}
> \]
> if and only if, after possibly swapping \(R,S\), there is a nonempty
> set
> \[
>                         A\subseteq\{01,02,12\}         \tag{15}
> \]
> such that
> \[
> R=A,\qquad
> \varnothing\ne S\subseteq
> N(A):=\{d\in D_5:d\cap a=\varnothing
>                    \text{ for every }a\in A\},        \tag{16}
> \]
> and \(S\) is stabilizer-invariant.

### Proof

Every set described by (15)--(16) plainly has only disjoint
cross-pairs.

Conversely, suppose all cross-pairs are disjoint.  If one side contains
an edge of the triangle on \(\{0,1,2\}\), orient the two sides so that
this is \(R\).  Any additional nontriangle edge in \(R\) forces the
opposite side to consist of triangle edges; swap the two sides in that
event.

It remains to see that one of the two sides must contain a triangle
edge.  If a side contains \(34\), every edge disjoint from it is a
triangle edge.  If it contains a mixed edge \(u3\), stabilizer
invariance also puts \(u4\) on that side; every edge disjoint from both
is the unique triangle edge on
\(\{0,1,2\}\setminus\{u\}\).  Thus, after swapping, \(R\) is a nonempty
subset of the three triangle edges.  The assertion that all
cross-pairs are disjoint is then exactly (16). \(\square\)

There are only thirteen unordered patterns in Lemma 4.2.  If
\(|A|=1\), the common disjoint neighbourhood consists of one
two-element mixed orbit and \(\{34\}\), giving three nonempty invariant
choices for \(S\).  This contributes \(3\cdot3=9\) patterns.  If
\(|A|=2\), then \(N(A)=\{34\}\), contributing three patterns.  The
three-edge choice \(A=\{01,02,12\}\) contributes one more:
\[
                              9+3+1=13.                 \tag{17}
\]

## 5. Exact remaining rooted obligations

Combining Corollary 3.1 with Lemmas 4.1--4.2 reduces the cyclic-three
fork to:

1. an \({\cal E}_4\) cut in its missing \(AT_i\) orientation requires
   both rooted three-poles to have the same one-label signature, one of
   the four singleton rows (14);
2. an \({\cal E}_4\) cut in either allowed \(AT_j,AT_k\) orientation
   requires two nonempty root signatures which are cross-intersecting,
   share at least one label, and also contain an unequal intersecting
   pair; and
3. an \({\cal E}_5\) cut requires one of the thirteen disjoint
   patterns (15)--(17).

These conditions are exact consequences of the exceptional signature,
not merely necessary boundary-parity filters.  What remains is to prove
that the corresponding rooted three-pole signatures cannot occur in
the reduced cyclic shores, or to realize one of them.  The present note
does neither.

The cap geometry supplies one further restriction.  By Lemma 4.1 of
`rooted-cycle-translation-obstruction.md`, both distinguished cap
edges are nonbridges of their rooted shores: a bridge root together
with one of the three connectors would form a cyclic two-edge cut in
the reduced cap.  For the equality-only case (11), every cycle through
either root must therefore have one of the translation-blocking label
supports classified in Theorem 3.1 of that note.

## 6. Literal replay

The human proof of Lemmas 4.1--4.2 is complete without computation.
For error detection, the Python producer
`scratch/rooted_three_pole_signature_factorization.py` enumerates all
\(127^2=16\,129\) ordered pairs of nonempty seven-orbit signatures.
It finds:

```text
equality only                         4
disjointness only, ordered           26
disjointness only, unordered         13
equality plus intersection, ordered  231
```

The independently written JavaScript replay reconstructs the orbits
and all relation types without importing the producer:

```sh
python3 scratch/rooted_three_pole_signature_factorization.py \
  --output /tmp/rooted-three-pole.json
cmp scratch/rooted-three-pole-signature-factorization-result.json \
  /tmp/rooted-three-pole.json
node scratch/verify_rooted_three_pole_signature_factorization.mjs
```

The frozen SHA-256 values are:

```text
771033803ba491066a14dee028358189976d1d71c62e4266a54b3545e321ad91  producer
c9c42fe9a29b6d9e269aa8a0bff5e09617518ae1055b3aab898e8730bcc7f8c5  result
51a31300703d78e3bc70e8c8cd5e504b7ff3c01cbc24201e92c5b848c820c27d  independent replay
```

## Primary-source attribution

The ten four-pole types and the exceptional signatures (10) are from:

E. Máčajová, G. Mazzuoccolo, and G. Tabarelli, “Cycle separating cuts
in possible counterexamples to the cycle double cover and the
Berge--Fulkerson conjectures,” *Ars Mathematica Contemporanea* **26**
(2026), #P2.03,
<https://doi.org/10.26493/1855-3974.3409.c13>.

The seven-state rooted factorization and the classification above are
deductions developed within this project.  Their external novelty has
not yet been established by a specialist literature review.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the rooted
three-pole normalization, proved the exact gluing equality, classified
the equality-only and disjoint-only signatures, and drafted this note.
All arguments are displayed for line-by-line human checking.  This is
not independent human review and not a resolution of either the
exceptional-signature conjecture or the Five-Cycle Double Cover
Conjecture.
