# Root-end factor forks lift through a cubic three-sum path

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE LIFT / FINITE ENDPOINT CONSEQUENCE /
NOT FIVE-CDC**.

This note repairs a gap between the completed endpoint-factor census and
the mixed cyclic-three branch of the exceptional four-pole reduction.  A
base pair in an endpoint factor need not remain one of the three
distinguished base pairs after transport through the rest of the
three-sum path.  It does, however, remain a **fork triple**.  That weaker
shape is enough when both shores are considered.

Fix
\[
                         D_5=\binom{[5]}2
\]
and the normalized ordered connector triangle
\[
                         \tau=(01,02,12).
\]
For five distinct coordinates \(p,q,r,s,t\), put
\[
                 Q(p;q,r;s,t)=\{qr,ps,pt\}.                    \tag{1}
\]
Call every set of this form a fork.  The three base pairs
\[
\{12,03,04\},\qquad
\{02,13,14\},\qquad
\{01,23,24\}                                                   \tag{2}
\]
are forks, and every coordinate permutation takes a fork to a fork.

## 1. Endpoint lift

Let a simple 3-connected cubic graph \(H\) be reconstructed as a path of
vertex three-sums
\[
                         F_1,F_2,\ldots,F_k.                    \tag{3}
\]
Suppose a distinguished proper root edge \(r\) lies in \(F_1\), while
the vertex whose deletion supplies the three external connectors lies
in \(F_k\).  Let \(w\) be the virtual vertex of \(F_1\) corresponding to
the first principal three-cut.

Write \(R(H,r)\) for the root signature after the three external
connectors are fixed to \(\tau\).  Write \(R(F_1,w,r)\) for the endpoint
factor signature after the three edges formerly incident with \(w\) are
fixed, in their physical order, to \(\tau\).

> **Endpoint-fork lift.**  
> Assume \(R(H,r)\ne\varnothing\).  If \(R(F_1,w,r)\) contains one of
> the base pairs in (2), then \(R(H,r)\) contains a fork.

### Proof

Choose one \(D_5\)-labelling of the rooted graph \(H\).  On the first
principal three-cut, its three labels form an ordered triangle
\[
                              \alpha=(a,b,c),                   \tag{4}
\]
because their xor is zero and all three belong to \(D_5\).  There is a
coordinate permutation \(\sigma\in S_5\) taking \(\alpha\), in its
physical order, to \(\tau\).  Indeed, the three labels in (4) are the
three edges of a triangle in \(K_5\), and every ordered permutation of
those three edges is induced by a permutation of its three vertices.

Restrict the chosen labelling to the part of the path
\(F_2,\ldots,F_k\), retaining the ordered boundary word \(\alpha\) at
its \(F_1\)-interface.  Keep this labelling fixed.

By hypothesis, for every \(A\) in one base pair \(P\) from (2), the
endpoint pole \(F_1-w\) has a labelling with connector word \(\tau\)
and root value \(A\).  Apply \(\sigma^{-1}\) to all labels in each of
these three endpoint labellings.  Their common connector word is now
\(\alpha\), so each glues to the one fixed labelling of
\(F_2,\ldots,F_k\).  The three resulting labellings of \(H\) have root
values
\[
                            \sigma^{-1}(P).                     \tag{5}
\]
Since coordinate permutations preserve forks, (5) is a fork contained
in \(R(H,r)\). \(\square\)

The proof also covers \(k=1\) trivially.  Side branches are absent in the
reduced exceptional-cap geometry because its factor-incidence tree is
the path between the two cap edges.  More generally, any side factor
already carrying one labelling is transparent: a global coordinate
permutation makes its ordered connector triangle equal to any prescribed
ordered triangle.

The proper root in \(F_1-w\) is a nonbridge.  Each cyclically
4-edge-connected simple cubic factor, and \(K_4\), is 3-connected;
deleting one vertex leaves a 2-connected graph.  Thus the nonbridge
hypothesis in the endpoint base-pair theorem is available at the factor,
not merely in the whole shore.

## 2. Two forks force the two forbidden cross-relations

For nonempty label sets \(R,S\subseteq D_5\), let
\(\operatorname{rel}(R,S)\) record equality \(\mathsf E\), unequal
one-coordinate intersection \(\mathsf I\), and disjointness
\(\mathsf D\) among cross-pairs.

> **Fork-crossing lemma.**  
> If \(R\) and \(S\) each contain a fork, then
> \[
>                 \{\mathsf I,\mathsf D\}
>                    \subseteq\operatorname{rel}(R,S).          \tag{6}
> \]

### Proof

It is enough to compare forks \(P\subseteq R\) and \(Q\subseteq S\).
Write
\[
                         P=\{qr,ps,pt\}.                        \tag{7}
\]

Suppose first that no member of \(Q\) is disjoint from a member of
\(P\).  A two-set meeting both \(ps\) and \(pt\) either contains \(p\)
or equals \(st\).  The latter misses \(qr\).  In the former case,
meeting \(qr\) leaves only \(pq\) or \(pr\).  Thus every member of
\(Q\) would lie in the two-element set \(\{pq,pr\}\), impossible
because a fork has three distinct members.  Hence a disjoint cross-pair
exists.

Now suppose that no unequal intersecting cross-pair exists.  A label
which is equal to \(ps\) intersects \(pt\) unequally, and conversely, so
neither \(ps\) nor \(pt\) can belong to \(Q\).  Any label not equal to a
member of \(P\) would have to be disjoint from all three members of
\(P\), but their union is all five coordinates.  Therefore every member
of \(Q\) would have to equal \(qr\), again impossible for a fork.
Hence an unequal intersecting cross-pair exists.  This proves (6).
\(\square\)

The same argument gives the useful one-sided facts: a set containing a
fork cannot have an equality-only relation or a disjointness-only
relation with any nonempty opposite signature.  Equality-only would
force both sides to be the same singleton, while no two-set is disjoint
from all three members of a fork.

## 3. Consequence for reduced exceptional caps

Use the vertex-minimal, two-cut-reduced, bridge-free, connected, simple,
terminal-distinct exceptional four-pole hypotheses of
`exceptional-four-pole-simple-cap-enumeration-reduction.md`.  Let
\[
                            G=P+\{e,f\}                          \tag{8}
\]
be its simple cubic cap.  If \(G\) has a cyclic three-edge cut, the
standard decomposition used in the existing reduction gives a factor
path
\[
                            F_1,\ldots,F_k,\qquad k\ge2,         \tag{9}
\]
whose endpoint factors contain \(e\) and \(f\), respectively.

The complete endpoint package
`../search/rooted-three-pole-nontait-endpoint-frontier-20260727/`
and the human Tait-cap theorem together prove base-pair closure for every
cyclically 4-edge-connected endpoint factor of order at most \(26\):
the Tait case is constructive, and the non-Tait cases through order 26
are independently classified by direct finite-domain and incremental-SAT
implementations.

Choose any principal cut in (9).  Its two rooted shores are nonempty under
each exceptional relation.  Applying the endpoint-fork lift on the two
sides and then the fork-crossing lemma excludes all three exceptional
relations
\[
             \{\mathsf E\},\qquad
             \{\mathsf E,\mathsf I\},\qquad
             \{\mathsf D\}                                    \tag{10}
\]
whenever both endpoint factors \(F_1,F_k\) have order at most \(26\).
Consequently:

> **Finite mixed-relation endpoint bound.**  
> In the cyclic-three branch of a reduced exceptional simple cap, at
> least one of the two endpoint factors has order at least \(28\).
> Hence
> \[
>                              |V(G)|\ge30.                     \tag{11}
> \]

Indeed, every cubic factor has order at least four, and reversing the
\(k-1\) vertex three-sums gives
\[
 |V(G)|=\sum_{i=1}^k|V(F_i)|-2(k-1)
 \ge28+4+4(k-2)-2(k-1)\ge30.                                  \tag{12}
\]

For the two pure relations \(\{\mathsf E\}\) and \(\{\mathsf D\}\), the
one-sided fork observation applies at either end separately.  Both
endpoint factors must then have order at least \(28\), recovering the
stronger pure-relation bound
\[
                              |V(G)|\ge54.                     \tag{13}
\]

Equation (11) removes the mixed cyclic-three branch through cap order 28.
Together with the already complete cyclically-four cap census through
order 26, it restores the simple terminal-distinct exceptional-pole lower
bound of order 28.  A first order-28 exception, if one exists, must have a
cyclically 4-edge-connected cap.  The retained order-28 source has not yet
been fully classified, so no order-30 global bound is claimed.

These statements concern the fixed-five exceptional-signature reduction.
They do not cover repeated terminals, nonsimple pole cores, arbitrary
numbers of CDC colours, or orientability, and they do not resolve
Five-CDC.

## 4. Literal finite check of the fork-crossing table

There are 30 labelled forks.  Enumerating all \(30^2=900\) ordered pairs
gives exactly
\[
\begin{array}{c|r}
\text{cross-relation}&\text{ordered pairs}\\ \hline
\{\mathsf I,\mathsf D\}&330\\
\{\mathsf E,\mathsf I,\mathsf D\}&570.
\end{array}
\]
This table is only an error check; the proof of the fork-crossing lemma is
complete without it.  The standard-library replay
`../scratch/verify_rooted_end_factor_fork_lift.py` independently constructs
all 60 ordered connector triangles, checks their two normalizations, and
reconstructs all 900 ordered fork-pair relations.  Its retained output is
`../scratch/rooted-end-factor-fork-lift-replay.json`.  Their SHA-256
values are

```text
2474c8869be64e3386b23a58e1b929e5e0f56227d19033e3d4316fbb17e1f136  verifier
738cbf30b1361b6de5bc18a13e4dfbafa9878a8bfdd9755e21b98afcda6dd513  result
```

## AI-use disclosure

OpenAI Codex, under human direction, found the endpoint-lift argument,
identified the invariant fork shape, proved the fork-crossing lemma, and
drafted this note.  The finite endpoint classifications and their
independent programs were also produced with substantial Codex
assistance.  Every mathematical step is displayed for line-by-line human
checking; this is not independent human peer review and is not a
resolution of the Five-Cycle Double Cover Conjecture.
