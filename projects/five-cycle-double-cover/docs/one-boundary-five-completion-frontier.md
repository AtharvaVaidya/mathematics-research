# One-boundary-five completion frontier

Status: exact structural lemma plus reproducible finite checks.  This note
does **not** resolve the Five-Cycle Double Cover Conjecture.

## Setup

Let \(Q\) be the 67-vertex factor-critical five-pole checked by
`check_cyclic4_all_bad_threshold_three_core.py`.  Its five boundary
terminals have source labels

\[
3,\ 7,\ 8,\ 9,\ 12.
\]

For each terminal \(q\), every perfect matching of \(Q-q\) leaves at least
four odd circuit components wholly inside \(Q\).  Thus all five terminals
fail the sufficient threshold \(c_{\rm odd}(Q-N)\leq 2\).  This refutes a
purely local proposed lemma, but by itself it does not place \(Q\) in the
special Gallai--Edmonds outside required by the one-boundary-five branch.

Write \(s=|A|\), \(W=A\cup U\), and let \(Z\) be the \(s+1\) singleton
components of \(D(G-U)\).  The four vertices of \(U\) are the endpoints of
the two independent root edges.

## Human proof excluding \(s=0\) in the cyclic-4 branch

For \(s=0\), \(W=U\) has four vertices and \(Z=\{z\}\).  The cubic singleton
\(z\) is adjacent to three of the four vertices of \(W\).  The two root
edges form a perfect matching of \(W\).

Among three vertices split into the two root pairs, one root pair lies
entirely in \(N(z)\).  Its two endpoints and \(z\) therefore induce a
triangle \(T\).

Each endpoint of that root has already used two incident edges inside
\(T\): its root edge and its edge to \(z\).  Its third edge is a boundary
edge to \(Q\).  The third edge at \(z\) goes to the remaining vertex in
\(N(z)\).  Consequently

\[
|\delta_G(V(T))|=3.
\]

The triangle is a circuit, and the other shore contains the nontrivial
internally bridgeless component \(Q\), hence contains a circuit.  This is a
cyclic 3-edge-cut.  Therefore:

> No \(s=0\) completion of any nontrivial internally bridgeless \(Q\) in
> this branch is cyclically 4-edge-connected.

This argument is independent of terminal assignments and does not use a
solver.

For bookkeeping, the number of labelled \(s=0\) assignments is

\[
3\cdot 4\cdot {5\choose 2}\cdot 3! = 720.
\]

The factors choose the root pairing, the unique non-neighbour of \(z\), the
two \(Q\)-terminals incident with that vertex, and the bijection from the
remaining three terminals to the other three vertices.  The checker
explicitly reconstructs all 720 graphs.  All 720 are simple cubic and
bridgeless, and all 720 exhibit the triangle cut above.

## A cyclic-4 completion at \(s=1\)

Let

\[
W=\{w_0,w_1,w_2,w_3,a\},\qquad Z=\{z_0,z_1\}.
\]

Take root edges \(w_0w_1,w_2w_3\) and proper outside edges

\[
\begin{aligned}
N(z_0)&=\{w_0,w_2,a\},\\
N(z_1)&=\{w_1,w_3,a\}.
\end{aligned}
\]

This outside is a theta graph between \(z_0\) and \(z_1\), with path
lengths \(2,3,3\).  Every vertex of \(W\) has exactly one unused incidence,
so attach source terminals \((3,7,8,9,12)\) to
\((w_0,w_1,w_2,w_3,a)\), respectively.

The resulting graph \(G_{74}\) is simple cubic of order 74 and size 111.
Deleting the four root endpoints \(U\), then deleting
\(A=\{a\}\), leaves the factor-critical components

\[
Q,\quad \{z_0\},\quad \{z_1\}.
\]

Moreover \(a\) is adjacent to all three of these components, so the strict
Hall inequality is \(|N(\{a\})|=3>1\).  This gives exactly the advertised
one-boundary-five Gallai--Edmonds structure.

The finite checker verifies every cut of size at most three and finds no
cyclic cut, so \(G_{74}\) is cyclically 4-edge-connected.  Its exhaustive
perfect-matching census is:

| odd circuits in the complementary 2-factor | perfect matchings |
|---:|---:|
| 4 | 43,137 |
| 6 | 2,660 |
| 8 | 408 |
| 10 | 4 |

Thus \(G_{74}\) is non-Tait and has exact oddness 4.  It is **not** an
oddness-six obstruction.  A direct five-CDC constraint search also finds
the instance satisfiable; this is consistent with the known
oddness-at-most-four theorem.  The current checker records the stronger
human-auditable oddness census, not a solver certificate for that SAT
observation.

The same enumeration separates the two possible perfect-matching types.
Here \(k\) is the number of matching edges in the five-edge boundary of
\(Q\), and \(r\) is the number of matching root edges:

| \((k,r)\) | 4 odd | 6 odd | 8 odd | 10 odd |
|---:|---:|---:|---:|---:|
| \((1,1)\) | 24,242 | 1,960 | 88 | 0 |
| \((3,0)\) | 18,895 | 700 | 320 | 4 |

Every row satisfies the structural identity \(k+2r=3\).  In particular,
the fact that every exposed-terminal matching inside \(Q\) leaves four
internal odd circuits does not force global oddness six: 24,242 matchings
of the prescribed-root type already have exactly four odd circuits in the
completed 2-factor.

The independent full-bijection checker
`check_s1_theta_q67_completions.py` repeats the cut and matching calculations
with separately written routines.  Across all \(5!=120\) terminal
bijections:

* every completion is simple cubic, bridgeless, and cyclically
  4-edge-connected;
* each completion has exactly 74 three-edge-cuts, all of them trivial
  vertex-star cuts, and has no smaller edge-cut;
* nauty `labelg` gives 30 isomorphism classes, each represented by four
  labelled bijections; and
* every completion has exact oddness 4.

Thus no assignment in this entire \(s=1\) theta family gives oddness at
least six.  Perfect-matching counts range from 43,191 to 52,068.

## First \(s=2\) completion

The exact outside census retains 128 locally cyclic-four \(s=2\) incidence
patterns.  Their boundary-multiplicity shapes are:

| nonzero multiplicities | patterns |
|---|---:|
| \(2+1+1+1\) | 96 |
| \(1+1+1+1+1\) | 32 |

After quotienting the indistinguishable stubs at a common \(W\)-vertex,
these patterns have 9,600 terminal-to-\(W\) assignments in total.  This is
an outside-incidence count.  A batched nauty `labelg` calculation quotients
the resulting full graphs into exactly 570 isomorphism classes: 540 classes
have labelled multiplicity 16 and 30 have multiplicity 32.

The lexicographically first retained pattern has

\[
\begin{aligned}
N(z_0)&=\{w_0,w_2,w_4\},\\
N(z_1)&=\{w_0,w_2,w_5\},\\
N(z_2)&=\{w_1,w_3,w_4\},
\end{aligned}
\]

and its five boundary stubs occur at
\((w_1,w_3,w_4,w_5,w_5)\).  Attaching source terminals
\((3,7,8,9,12)\) in that order gives a simple cubic graph of order 76 and
size 114.  The checker finds it bridgeless and cyclically
4-edge-connected.  The strict Hall checks for
\(A=\{w_4,w_5\}\) have neighbourhood sizes \(3,2,4\) for
\(\{w_4\},\{w_5\},A\), against required lower bounds \(2,2,3\).

Its exact perfect-matching census is

\[
\{4:40562,\quad 6:24346,\quad 8:400\},
\]

so it has 65,308 perfect matchings and exact oddness 4.  This is one checked
\(s=2\) witness, not a full cut or oddness census of all 570 classes.

## What this changes

The all-five-bad \(Q\) really can occur inside the exact Gallai--Edmonds
branch of a cyclically 4-edge-connected non-Tait cubic graph.  Therefore a
proof cannot use only the statement

> two attainable boundary terminals exist, and one of them must have a
> matching leaving at most two internal odd circuits.

That local conclusion is false even in a globally admissible \(s=1\)
completion.  However, the completed graph still has oddness four, in both
matching types.  The surviving target must therefore exploit how the two
open paths in the core complement close through the outside, rather than
merely count the odd circuits wholly inside \(Q\).

## Reproduction

Run:

```sh
python3 scratch/check_cyclic4_all_bad_threshold_three_core.py
python3 scratch/check_one_boundary_five_completion_frontier.py
python3 scratch/check_s1_theta_q67_completions.py \
  --output /tmp/s1-theta-q67-census.json
python3 scratch/check_s2_q67_completion_classes.py \
  --skip-class-cuts \
  --output /tmp/s2-q67-classes.json
```

The second command is standard-library only and imports the first checker
from the same directory.  It performs the 720-case \(s=0\) audit, the exact
cyclic-cut checks and perfect-matching censuses for the displayed \(s=1\)
and \(s=2\) completions.
The third command checks all 120 terminal bijections; canonicalization uses
the optional nauty `labelg` executable and the mathematical census does not
depend on it.  The fourth regenerates and canonically quotients all 9,600
\(s=2\) gluings, then performs the exact cut and matching census only for
the displayed lexicographic witness.  Omitting `--skip-class-cuts` also
classifies small cuts in one representative of every isomorphism class.
