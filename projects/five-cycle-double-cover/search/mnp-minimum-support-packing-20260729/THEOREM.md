# A globally minimum nonzero value class that packs in the reconstructed MNP family

Date: 2026-07-29

Status: **human-checkable infinite-family theorem, conditional only on the
stated figure transcription; not a universal FiveCDC theorem**.

## The statement

Let \(\widehat H_n\), \(n\geq2\), be the deterministic reconstruction
retained from the vector figures and labelled recursion of Mattiolo,
Negrini, and Pagani (MNP).  Let

\[
M_n=\{\epsilon_1,\ldots,\epsilon_n\}
\]

be the exact zero set of their displayed
\(\mathbb F_2^2\)-flow.

> **Theorem.** For every \(n\geq2\), \(M_n\) is a matching and there are
> edge-disjoint sets
> \(J^1_n,J^2_n\subseteq E(\widehat H_n)\setminus M_n\) such that
> \[
> \partial J^1_n=\partial J^2_n=\partial M_n.
> \]
> They can be chosen with
> \[
> |J^1_n|=12n+3,\qquad |J^2_n|=11n+26.
> \]

Here \(\partial A\) denotes the set of vertices having odd degree in the
edge set \(A\).  Thus each \(J^i_n\) is a
\(\partial M_n\)-join, and the theorem says that the distinguished support
packs two such joins.

MNP Lemma 3.5 constructs the flow with exact zeros
\(\epsilon_1,\ldots,\epsilon_n\), and MNP Theorem 3.6 proves
\(r_f(H_n)=n\).  Subject to the transcription identity
\(\widehat H_n=H_n\), it follows that \(M_n\) is a globally
cardinality-minimum exact-zero support.

A further consequence, proved below, is that the minimum cardinality of a
**nonzero** value class over nowhere-zero \(\mathbb F_2^3\)-flows on
\(\widehat H_n\) is \(n\), and one minimum nonzero class is \(M_n\) and
packs.  The qualification is essential: the zero-value class of a
nowhere-zero flow is empty.

## Four labels and one parity equation

Label every edge by one of

```text
R = (0,0)   J1 = (1,0)   J2 = (0,1)   M = (1,1).
```

The intended meanings are: unused, first join, second join, and matching.
The two joins are disjoint because no edge is assigned both `J1` and `J2`.
At a vertex, XOR of the two-bit labels is zero precisely when the odd
degrees in \(J^1\) and \(J^2\) are both equal to the incidence parity of
\(M\).  Hence, once \(M\) is a matching and the four labels partition the
edges, the local XOR equation proves both join equalities.

## Stable interface

The newest closure of \(\widehat H_n\) consists of an edge
\(\pi_n=\alpha_n\gamma_n\) and a vertex \(x_n\) incident with the three
spokes \(\beta_n,\delta_n,\epsilon_n\).  The stable state, in role order, is

```text
role     alpha  gamma  beta  delta  epsilon
label       R      R     J2     J1        M
```

Thus \(\pi_n\) is unused; the beta spoke is in the second join; the delta
spoke is in the first join; and the epsilon spoke is in the matching.

## Literal base

Decode the graph6 string in `certificate.json` and sort the 123 normalized
endpoint pairs lexicographically; the index in that list is the edge ID
used here.  On the frozen order-82 graph \(\widehat H_2\), take

```text
M2 = {34,122}

J1_2 =
{33,35,36,38,40,41,42,43,44,45,52,65,66,69,71,77,79,
 91,100,101,103,108,110,112,113,116,117}

J2_2 =
{0,2,3,5,6,9,10,11,16,17,20,21,22,23,25,26,27,29,32,
 48,49,51,55,58,59,60,61,62,63,73,74,76,81,83,85,86,
 89,90,92,94,95,97,98,104,106,118,120,121}.
```

These sets are disjoint as required and direct endpoint parity gives

```text
partial(M2) = partial(J1_2) = partial(J2_2)
            = {19,79,80,81}.
```

The closure edge is ID 68 and has label `R`; the beta spoke is ID 76 and
has label `J2`; the delta spoke is ID 103 and has label `J1`; and the
epsilon spoke is matching edge 122.  Thus the base has the stable state.
The sizes are \(2,27,48,46\) for \(M,J^1,J^2,R\), respectively.

## Literal recurring tile

Use the local vertex and lexicographic edge IDs of the 42-vertex graph
`J` encoded in `certificate.json`.  Make an open tile by removing input
vertex 38, output vertex 39, and trimming input edge
`56=(34,36)` and output edge `4=(1,18)`.  Equivalently, the internal edge
IDs are all IDs `0,...,62` except

```text
4 12 39 56 57 59 61 62.
```

The boundary attachments are

```text
role:    alpha gamma beta delta epsilon
input:      36    34   37    35      41
output:      1    18    6    23      40.
```

Assign the stable label to each boundary half-edge.  Internally take

```text
P1 = {36,37,41,42,45,46,47,49,52,53,54}
P2 = {9,10,18,19,20,23,24,25,27,60},
```

and label every other internal edge `R`.  The sets have sizes 11 and 10
and are disjoint.

The following is the complete local check.  A row lists the three objects
incident with an internal vertex.  Labels `0,1,2,M` mean
`R,J1,J2,M`; `i` and `o` denote input and output half-edges.  In every
row, the two-bit XOR of the three labels is zero.
The second letter of a boundary abbreviation is the role initial
`a,g,b,d,e`.

| vertex | three incident labelled objects |
|---:|---|
| 0 | e0:0, e1:0, e2:0 |
| 1 | e0:0, e3:0, oa:0 |
| 2 | e5:0, e6:0, e7:0 |
| 3 | e8:0, e9:2, e10:2 |
| 4 | e1:0, e5:0, e11:0 |
| 5 | e3:0, e6:0, e8:0 |
| 6 | e9:2, e11:0, ob:2 |
| 7 | e13:0, e14:0, e15:0 |
| 8 | e2:0, e13:0, e16:0 |
| 9 | e10:2, e17:0, e18:2 |
| 10 | e17:0, e19:2, e20:2 |
| 11 | e14:0, e21:0, e22:0 |
| 12 | e16:0, e23:2, e24:2 |
| 13 | e18:2, e21:0, e25:2 |
| 14 | e19:2, e22:0, e23:2 |
| 15 | e24:2, e25:2, e26:0 |
| 16 | e7:0, e20:2, e27:2 |
| 17 | e28:0, e29:0, e30:0 |
| 18 | e28:0, e31:0, og:0 |
| 19 | e32:0, e33:0, e34:0 |
| 20 | e35:0, e36:1, e37:1 |
| 21 | e29:0, e32:0, e38:0 |
| 22 | e31:0, e33:0, e35:0 |
| 23 | e36:1, e38:0, od:1 |
| 24 | e40:0, e41:1, e42:1 |
| 25 | e30:0, e40:0, e43:0 |
| 26 | e37:1, e44:0, e45:1 |
| 27 | e44:0, e46:1, e47:1 |
| 28 | e41:1, e48:0, e49:1 |
| 29 | e43:0, e50:0, e51:0 |
| 30 | e45:1, e48:0, e52:1 |
| 31 | e46:1, e49:1, e50:0 |
| 32 | e51:0, e52:1, e53:1 |
| 33 | e34:0, e47:1, e54:1 |
| 34 | e15:0, e55:0, ig:0 |
| 35 | e42:1, e55:0, id:1 |
| 36 | e26:0, e58:0, ia:0 |
| 37 | e58:0, e60:2, ib:2 |
| 40 | e53:1, e60:2, oe:M |
| 41 | e27:2, e54:1, ie:M |

This table is a finite proof of the tile parity invariant.  It also makes
clear that the two join colors never occupy the same internal edge.

## Gluing lemma and induction

Assume \(\widehat H_n\) has
\(M_n,J^1_n,J^2_n\) in the stable state.  Delete \(\pi_n\), delete
\(x_n\) and its three spokes, and expose the five old role vertices.  Glue
the input of a fresh certified tile to the matching roles.  Close the output
with a fresh unused alpha-gamma edge and a fresh cubic vertex whose beta,
delta, and epsilon spokes have labels `J2`, `J1`, and `M`.

At an old role vertex, deleting its old closure edge leaves a parity defect
equal to that edge's two-bit label; the new connector has the same label
and cancels the defect.  At a tile input vertex, replacing the certified
half-edge by that connector leaves its verified equation unchanged.  The
same argument applies when output half-edges are replaced by the four new
closure edges.  At the new cubic vertex,

\[
(0,1)+(1,0)+(1,1)=(0,0).
\]

Every other vertex equation is unchanged.  Hence the two new join
boundaries both equal the new matching boundary.

The old matching minus its epsilon closure spoke is still a matching.  Its
new input epsilon connector uses the exposed old epsilon vertex and a fresh
tile vertex; the new output epsilon spoke uses two other fresh vertices.
Thus the new \(M\) is again a matching.  Label classes are disjoint by
construction.  The output closure is again in the stable state, completing
the induction.

For \(J^1\), a step removes the old delta spoke and adds 11 internal tile
edges, one delta input connector, and one delta output spoke, a net increase
of 12.  For \(J^2\), it removes the old beta spoke and adds 10 internal
edges plus two beta edges, a net increase of 11.  From base sizes 27 and 48,

\[
|J^1_n|=27+12(n-2)=12n+3,\qquad
|J^2_n|=48+11(n-2)=11n+26.
\]

The matching gains one edge at each step, so \(|M_n|=n\).  The total graph
has \(40n+2\) vertices and \(60n+3\) edges; the unused class has
\(36n-26\) edges.

## Global minimum and the \(\mathbb F_2^3\) lift

MNP define \(r_f(G)\) as the minimum number of edges whose deletion leaves
a nowhere-zero \(\mathbb F_2^2\)-flow.  This equals the minimum number of
zeros in an \(\mathbb F_2^2\)-flow on \(G\): delete its zeros in one
direction, and extend a flow by zero in the other.  Their displayed flow
has exact zero set \(M_n\), and their Theorem 3.6 proves
\(r_f(H_n)=n\).  Hence \(M_n\) is globally minimum, conditional on the
stated reconstruction identity.

For completeness, this also gives a minimum nonzero value class in a
nowhere-zero \(\mathbb F_2^3\)-flow.  Fix nonzero
\(a\in\mathbb F_2^3\), identify
\(\mathbb F_2^3/\langle a\rangle\) with \(\mathbb F_2^2\), and choose a
linear section \(s\).  Let \(\phi_n\) be the MNP flow.  Since
\(\partial M_n=\partial J^1_n\), the indicator
\(h=1_{M_n\mathbin{\triangle}J^1_n}\) is a binary flow.  (The sets are
disjoint, so the symmetric difference is their union.)  Define

\[
f=s\phi_n+a h.
\]

On \(M_n\), \(f=a\).  Off \(M_n\), \(\phi_n\ne0\), so its lifted value is
outside \(\langle a\rangle\); adding either zero or \(a\) makes it neither
zero nor \(a\).  Thus \(f\) is nowhere-zero and
\(f^{-1}(a)=M_n\).

Conversely, project any nowhere-zero \(\mathbb F_2^3\)-flow modulo any
nonzero value \(a\).  The zero set of the projected
\(\mathbb F_2^2\)-flow is exactly \(f^{-1}(a)\).  MNP's lower bound
therefore gives \(|f^{-1}(a)|\ge n\), proving the claimed global minimum.

## Provenance, novelty, and scope

The MNP source contains vector figures and a labelled recursion, but no
author-supplied machine-readable graph.  The retained \(\widehat H_2\) is a
deterministic figure transcription, and later \(\widehat H_n\) are
generated by the literal recurring substitution.  The theorem must remain
qualified until a human independently compares that transcription with the
figures or the authors provide an edge list.

MNP prove that their graphs are cyclically 5-edge-connected.  That is a
cyclic-connectivity statement, not a girth statement.  The reconstructed
graphs checked here through \(n=100\) have girth 5.  No all-\(n\) girth
claim is part of the packing induction.
Accordingly, this result supplies **no evidence for the separate
girth-at-least-10 restriction**.
This proof neither uses nor repairs any separate source-literal construction
gap in the project's girth-at-least-10 branch; that issue is unrelated to
the concrete reconstructed MNP graphs treated here.

The theorem establishes the surviving minimum-support packing property on
one cyclically 5-edge-connected family with unbounded flow resistance.  It
does not prove the property for all bridgeless graphs, does not assert that
every minimum support packs, and does not resolve FiveCDC.  A targeted
literature review has not yet established whether this narrow packing
refinement is new, so no priority claim is made.

Primary source:
[Mattiolo--Negrini--Pagani, arXiv:2604.22501v1](https://arxiv.org/abs/2604.22501).
The exact imported items are Lemma 3.5, Theorem 3.6, and the cyclic
connectivity theorem in Section 4.

## AI-use disclosure

The stable packing state, finite tile certificate, induction, and
verification strategy were found with substantial assistance from OpenAI
Codex agents under human direction on 2026-07-29.  The literal certificate,
full local table, and dependency-free checker are included so that none of
the new assertions requires trusting an AI system.  Independent human
review is required before a standalone scholarly submission or priority
claim.
