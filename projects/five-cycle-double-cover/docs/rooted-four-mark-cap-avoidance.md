# Rooted four-mark cap avoidance: exact trace lemma and current gap

Date: **2026-07-26**.

Status: **ROOT-AVOIDING TRACE PROVED / NAIVE ROOTED THEOREM
REFUTED / FULL INHERITED CLOSED-STATE THEOREM OPEN**.

This note continues `cyclic-six-cut-four-mark-interface.md`.  Its purpose
is to distinguish three statements which must not be conflated:

1. a binary cycle containing four marks and avoiding a specified edge;
2. such a binary cycle with an even number of marks on every circuit
   component; and
3. the second conclusion for the particular caps inherited from the
   terminal-flanked six-cut of a cardinality-minimum exact-zero matching.

The first statement is automatic from the inherited Tait colouring.  The
second is false under Tait-colourability and universal separation alone.
The retained countermodel fails exactly the marked cyclic-cut inequality
used in the unrooted four-mark theorem and has marked-subdivision girth
five.  It therefore does not refute the second statement with that
inequality, and it does not enter the full inherited six-cut branch.

The cyclic-decomposition proof in `four-mark-core-closure.md` does not
currently provide the missing root avoidance.  Its central prescribed
cycle step can already require all four slots of the applicable
quasi-\(4\)-connected theorem.

No conjecture-resolution claim is made.

## 1. Three exact rooted statements

Let \(L\) be a connected simple cubic graph, let \(S\) be a four-edge
matching, and let \(f\in E(L)\setminus S\).  A **closed rooted
certificate** is a binary cycle \(Q\) such that
\[
 S\subseteq Q,\qquad f\notin Q,
\]
and every circuit component of \(Q\) contains an even number of edges of
\(S\).

The weakest tempting assertion is:

> **Naive rooted assertion.**  If \(L\) is Tait-colourable, \(S\) is
> universally separated, and some Tait colouring gives all members of
> \(S\) one colour and \(f\) another colour, then a closed rooted
> certificate exists.

Section 4 gives an exact finite countermodel.

The natural strengthening adds the hypothesis of the audited unrooted
four-mark theorem:
\[
 |\delta_L(X)|+|S\cap E(L[X])|\ge4                 \tag{1}
\]
whenever \(L[X]\) contains a circuit.  Call this the **standard rooted
assertion**.  It is not refuted here, but it is also not proved by the
published prescribed-cycle results or by the existing cyclic-decomposition
argument.

Finally, the **inherited closed-state assertion** concerns the two caps
arising in `cyclic-six-cut-four-mark-interface.md`.  It includes the
original core's marked-girth condition, its paired cyclic-cut condition,
and the cardinality-minimality of the exact-zero matching.  This statement
is strictly different from the standard rooted assertion:

- the flanked cap is a multigraph and visibly violates (1) on the
  marked/cap parallel pair;
- its smoothed simple graph has a new marked edge, but (1) is not known
  to inherit;
- the opposite cap is simple, but (1) is automatic only on shores
  containing at most one cap endpoint; and
- minimum-support is global information about the original expansion,
  not an intrinsic hypothesis on an arbitrary rooted four-mark graph.

The inherited closed-state assertion remains open.

## 2. The cap edge is not a cycle-space obstruction

The following lemma settles the linear part of the rooted problem.
It requires neither universal separation nor a cut inequality once the
displayed colouring is given.

> **Root-avoiding trace lemma.**  Let \(L\) be a connected cubic graph
> with a Tait colouring \(\kappa\).  Let \(S\subseteq E(L)\) have one
> common colour \(c\), and let \(f\notin S\) have colour different from
> \(c\).  Then there is a binary cycle \(Q\) with
> \[
>                  S\subseteq Q,\qquad f\notin Q.   \tag{2}
> \]

### Proof

Work over \(\mathbb F_2\).  Let \(Z\) be the binary cycle space and put
\(R=S\cup\{f\}\).  Prescribe the trace
\[
 t_e=1\quad(e\in S),\qquad t_f=0.                  \tag{3}
\]
The standard cycle/cut orthogonality says that \(t\) belongs to the
restriction of \(Z\) to \(R\) if and only if
\[
       |D\cap S|\equiv0\pmod2                     \tag{4}
\]
for every cut \(D\) contained in \(R\).  For completeness, the
orthogonal complement of the restricted space is precisely the set of
vectors on \(R\) whose zero extension belongs to \(Z^\perp\), the cut
space.  Orthogonality to (3) is exactly (4).

It remains to check (4).  In a Tait-coloured cubic graph, every cut has
the same parity in each of the three colour classes: summing the
incidence of one colour over a shore gives the order of that shore
modulo two.

If \(f\notin D\), then every edge of \(D\) has colour \(c\).  The other
two colour counts are zero, so the \(c\)-count is even.  Thus
\(|D\cap S|\) is even.

If \(f\in D\), the cut has zero edges of one colour and exactly one edge
of the colour of \(f\).  Those two colour counts have different parity,
contrary to the Tait cut-parity identity.  Hence no such cut exists.

Thus (4) holds for every cut supported in \(R\), so the required
binary cycle exists. \(\square\)

Universal separation supplies an all-one-colour mark precolouring in an
arbitrary marked Tait graph.  In the six-cut application, more is true:
the inherited all-\(c\) core colouring already gives the cap edge the
common colour of the original two-edge cut, different from the four
marked \(c\)-edges.  Therefore both capped shores have a root-avoiding
all-mark binary cycle before componentwise parity is imposed.

This sharpens the exact obligation from the preceding note:

> the closed-state gap is entirely the requirement that every selected
> circuit component have even marked parity.

It is not a failure of the affine cycle-space trace.

## 3. Why the prescribed-cycle literature does not close the root

The primary prescribed-cycle source used by the unrooted proof is
R. E. L. Aldred, M. N. Ellingham, R. L. Hemminger, and D. A. Holton,
[*Cycles in quasi 4-connected
graphs*](https://ajc.maths.uq.edu.au/pdf/15/ocr-ajc-v15-p37.pdf),
Australas. J. Combin. 15 (1997), 37--46.

Their Theorem 3.3 says that a free edge system of size at most four in a
quasi \(4\)-connected graph lies on a cycle.  Four independent edges are
the special case used in `four-mark-core-closure.md`.  The paper also
has a genuine avoidance theorem, Theorem 3.5, but it concerns cycles
through \(4-k\) prescribed vertices while avoiding \(k\) prescribed
vertices, for \(k\le2\), with stated degree-three exceptions.  It does
not assert a cycle through four prescribed edges while avoiding a fifth
edge.

Subdividing \(f\) and asking to avoid the new vertex does not repair the
count: the four marked edges already occupy all four prescribed slots,
and the subdivision also destroys the literal quasi-\(4\)-connected
hypothesis.  Avoiding an endpoint of \(f\) is not equivalent when a
selected marked edge is incident with that endpoint.

The second source is P. Knappe and M. Pitz,
[*Circuits through prescribed
edges*](https://arxiv.org/abs/1810.09323), J. Graph Theory 93 (2020),
470--482.  The part used by the unrooted proof is the three-edge case:
in a \(3\)-edge-connected graph a prescribed set of at most three edges
lies in a circuit exactly when it contains no odd cut.  It gives no
four-included-plus-one-forbidden conclusion needed here.

The failure to inherit root control occurs at two places in the
cyclic-decomposition proof:

1. the central cyclically \(4\)-edge-connected factor can require four
   distinct same-colour selected edges, so the Aldred et al. step is
   saturated; and
2. if the root lies in a one-mark branch, the one-mark shore lemma gives
   a marked path for every boundary pair but does not assert that the
   path avoids a specified internal edge.

Consequently the published inputs validate the unrooted proof but do not
validate a root-avoiding rewrite of it.

## 4. An exact countermodel to the naive rooted assertion

Consider the order-\(28\) connected simple cubic graph with graph6 record

```text
[??????O@?R?d?EGGSAK?H_?HG?Ao@A_A?????????????C?G?C???M???B_???[
```

and marks
\[
 S=\{(3,11),(6,15),(7,18),(22,26)\}.
\]
Take
\[
             f=(0,20),\qquad h=(8,24).              \tag{5}
\]

The four marks are universally separated.  The independent checker
`scratch/verify_rooted_four_mark_countermodel.py` enumerates all \(162\)
proper edge-colourings modulo global colour permutation and checks every
bichromatic circuit in each one.

There is a Tait colouring whose three colour classes are
\[
\begin{aligned}
a:\;&(0,11),(1,9),(2,19),(3,12),(4,13),(5,15),(6,16),\\
   &(7,17),(8,14),(10,18),(20,23),(21,26),(22,25),(24,27);\\
b:\;&(0,20),(1,15),(2,16),(3,13),(4,11),(5,12),(6,14),\\
   &(7,19),(8,24),(9,18),(10,17),(21,25),(22,27),(23,26);\\
c:\;&(0,12),(1,14),(2,10),(3,11),(4,17),(5,16),(6,15),\\
   &(7,18),(8,13),(9,19),(20,25),(21,24),(22,26),(23,27).
\end{aligned}                                      \tag{6}
\]
Thus all four marks have colour \(c\), while \(f\) has colour \(b\).
The displayed lists permit a direct check that every vertex occurs once
in each colour class.

Nevertheless no closed rooted certificate exists.  This has a short
human proof independent of cycle-space enumeration.  The set
\[
                  \{f,h\}                           \tag{7}
\]
is a two-edge cut.  Its shores are
\[
\begin{aligned}
 A&=\{0,1,\ldots,19\},\\
 B&=\{20,21,\ldots,27\},
\end{aligned}
\]
and the marks split \(3+1\) between \(A\) and \(B\).

Every binary cycle meets every cut evenly.  If a binary cycle avoids
\(f\), it must therefore avoid \(h\) as well.  All of its components
then lie within one shore.  If every component had even marked parity,
the total number of marks on each shore would be even.  The actual
totals are three and one, a contradiction.  Hence every even-component
all-four binary cycle contains \(f\).

The exhaustive cycle-space check agrees with the proof:

\[
\begin{array}{c|r}
\text{all-four binary cycles} & 2048\\
\text{all-four binary cycles avoiding \(f\)} & 1024\\
\text{even-component all-four binary cycles} & 360\\
\text{even-component all-four cycles avoiding \(f\)} & 0.
\end{array}
\]

The middle two rows exhibit the precise distinction proved in Section 2:
root-avoiding trace feasibility holds, but every such trace has an
odd-marked component.

This example lies outside both stronger rooted statements.  The
eight-vertex shore \(B\) contains one mark and has boundary two, so
\[
 |\delta(B)|+|S\cap E(L[B])|=2+1=3<4.              \tag{8}
\]
Its marked-subdivision girth is five, not ten.  Thus the obstruction is
excluded by the standard marked-cut hypothesis and by the inherited
marked-girth hypothesis.

More generally, (7) proves the following elementary obstruction.

> **Odd-shore two-cut lemma.**  If \(\delta(X)=\{f,h\}\), no mark lies
> on the cut, and \(X\) contains an odd number of the marks, then every
> all-mark binary cycle with even marked parity on every component uses
> both \(f\) and \(h\).

The proof is the preceding cut-parity argument.  For four marks the
opposite shore is odd as well.

## 5. Reproducibility and finite lower-order screen

Run

```sh
python3 scratch/verify_rooted_four_mark_countermodel.py
```

The output is frozen in
`scratch/rooted-four-mark-countermodel-result.json`.  The SHA-256 hashes
at the time of this note are

```text
061b0f8d5b167ac1e28f1d4506a3cc3582be602bd99fe35f0a6f4b1eb9de3bb2  scratch/verify_rooted_four_mark_countermodel.py
d89626451b7c14980eae76c13d1c1f347960bebac81b34199e24d7613dd5fc9b  scratch/rooted-four-mark-countermodel-result.json
```

As a separate diagnostic, the complete connected simple cubic corpus
through order \(20\) was screened for a universally separated four-edge
matching satisfying (1).  No such marked graph exists.  At order \(20\)
the command was

```sh
geng -cq -d3 -D3 20 |
  scratch/tait_all_coloring_mark_separation \
    --target 4 --marked-cyclic-connectivity 4 --progress 25000
```

It checked \(510489\) graphs, of which \(496430\) were Tait-colourable,
and enumerated \(5015828\) Tait colourings modulo global colour
permutation.  It found zero marked witnesses.  The same complete screen
found none at each even order from \(8\) through \(18\).
The per-order counts and checker hashes are frozen in
`scratch/rooted-four-mark-order20-screen-result.json`, with SHA-256

```text
30bf57789a4ce1a16c75673c96f3ac5f193be88dd0d8acaae9c2ec236ea8e22b  scratch/rooted-four-mark-order20-screen-result.json
```

This is only a finite lower-order theorem.  In particular, it supplies
neither a countermodel nor positive evidence decisive enough to settle
the standard rooted assertion.

## 6. Exact remaining obligation

What is now proved:

1. both six-cut caps admit an all-four binary cycle avoiding the cap
   edge;
2. the existing prescribed-cycle results do not automatically make that
   trace componentwise even; and
3. the simplest root-forcing obstruction is an odd \(3+1\) marked
   cyclic two-cut, which the standard marked-cut inequality excludes.

What remains open is to prove or refute either of the following:

- the standard rooted assertion under (1); or
- the more specialized inherited closed-state assertion using the
  original marked-girth, paired-cut, and minimum-support information
  even where (1) does not pass to the cap.

A proof must add a component-merging argument which preserves the trace
\((S=1,f=0)\), or a genuinely root-avoiding version of the cyclic
decomposition with a forbidden-edge shore lemma.  A disproof must satisfy
the exact stronger hypotheses; the order-\(28\) graph above does not.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the cycle-space
trace lemma, audited the primary prescribed-cycle statements, found and
checked the finite rooted countermodel, ran the lower-order screen, and
drafted this note.  The root-forcing obstruction and trace lemma are
displayed as line-by-line human-checkable arguments.  The
universal-separation and finite census claims are exhaustive computer
checks, not human peer review.  This work does not resolve the
five-cycle double cover conjecture.
