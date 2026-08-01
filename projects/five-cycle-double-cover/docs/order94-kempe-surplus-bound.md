# Short-factor switching excludes ambient orders through \(94\)

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE PROOF / INDEPENDENT CODEX-AGENT AUDIT PASSED /
SIZE-FOUR BRANCH ONLY / FIVE-CDC STILL OPEN**.

The independent reconstruction, arbitrary-surplus generalization, and
order-\(96\) frontier check are recorded in
`audit-and-generalization-order94-kempe.md`.

This note extends the order-\(88\) equality contradiction in
`equality88-kempe-girth-contradiction.md`.  It proves, subject to the
same minimum-counterexample reductions, that the connected eight-mark
exact-zero size-four branch cannot have ambient order
\[
                         88,\ 90,\ 92,\ \text{or }94.
\]

The argument is solver-free.  Its two ingredients are:

1. switching any marked core \(C_{10}\) can meet at most three circuits
   of the opposite bichromatic factor; and
2. ambient girth bounds the multiplicity with which short marked factor
   circuits can meet one another.

The disconnected \(4+4\) branch has already been eliminated at every
order by the four-mark core theorem, so only the connected eight-mark
branch is considered below.

## 1. Setup and the length surplus

Let \(G\), \(M\), \(K=G-M\), \(H\), and
\[
                         S=\{s_0,\ldots,s_7\}
\]
be the connected eight-mark objects from the extremal exact-zero
size-four reduction.  Thus:

- \(G\) is cubic and has girth at least ten;
- \(H\) is a connected simple Tait-colourable cubic core;
- \(S\) is a universally separated eight-edge matching of \(H\); and
- subdividing every member of \(S\) recovers \(K\).

Precolour all marks with one Tait colour \(c\), and call the other
colours \(a,b\).  Universal separation puts the eight marks on eight
distinct circuits of each of \(H[a,c]\) and \(H[b,c]\).  Every marked
core factor circuit has even length at least ten: after its unique mark
is subdivided, it becomes an odd circuit of \(G\) of length at least
eleven.

Write
\[
                       |V(G)|=88+2t.                 \tag{1}
\]
The suppressed core has
\[
                       |V(H)|=80+2t.                 \tag{2}
\]
When \(0\le t<5\), the eight marked factor circuits already occupy at
least 80 vertices, leaving fewer than ten vertices.  There can therefore
be no unmarked factor circuit.  In either factor the marked circuit
lengths have the form
\[
                       10+2h_0,\ldots,10+2h_7,
 \qquad h_i\ge0,\qquad \sum_i h_i=t.                 \tag{3}
\]
Call a circuit **short** when \(h_i=0\), that is, when it is a core
\(C_{10}\), and **long** otherwise.  Each factor has at least \(8-t\)
short circuits and at most \(t\) long circuits.

## 2. A short circuit meets at most three opposite circuits

Fix a short \(ac\)-factor circuit \(A\).  It has five \(c\)-edges.
Let \(B_1,\ldots,B_q\) be the distinct \(bc\)-factor circuits containing
those five edges.

Cut the five \(c\)-edges at their ten endpoints.  On those endpoints
define three perfect matchings:

- \(R\) pairs the endpoints of each removed \(c\)-edge;
- \(P\) pairs endpoints joined by a residual path in one of the
  cut-open \(B_j\)'s; and
- \(D\) pairs endpoints joined by one of the five \(a\)-edges of \(A\).

The two-matching graph \(R\cup P\) has \(q\) circuit components, one for
each original \(B_j\).  The graph \(R\cup D\) is the single 10-circuit
\(A\).  After the Kempe interchange \(a\leftrightarrow c\) on \(A\),
the affected circuits of the new \(bc\)-factor are obtained by joining
the \(P\)-paths with the \(D\)-edges.  Let
\[
                     d=c(D\cup P)                    \tag{4}
\]
be their number.

> **Lemma 2.1 (three-matching rank bound).**
> \[
                            q+d\le6.                 \tag{5}
> \]

### Proof

Let \(X=R\cup P\cup D\), regarding parallel matching edges as distinct.
It is a connected cubic multigraph on ten vertices: \(R\cup D\) is
already connected.  Hence its binary cycle space has dimension
\[
                    |E(X)|-|V(X)|+1=15-10+1=6.       \tag{6}
\]

Consider the following \(1+q+d\) bicoloured circuit vectors in that
cycle space:

- the one circuit of \(R\cup D\);
- the \(q\) circuits of \(R\cup P\); and
- the \(d\) circuits of \(D\cup P\).

Their sum is zero because every matching edge occurs in exactly two of
the listed vectors.  This is their only linear dependence.  Indeed, in
an arbitrary dependence, the coefficient on an \(R\)-edge says that
the coefficient of its \(R\cup P\) component equals the coefficient of
the unique \(R\cup D\) circuit.  Thus all \(q\) such coefficients are
equal.  Looking at the \(D\)-edges similarly makes all \(d\)
\(D\cup P\) coefficients equal to the same value.  The relation space
is therefore one-dimensional.

The listed vectors have rank \(q+d\), which cannot exceed (6).  This
proves (5). \(\square\)

Exactly one of the original \(B_j\)'s contains the mark of \(A\); that
marked edge is removed by the switch.  Every other one of the \(q-1\)
affected \(B_j\)'s retains its unique mark.  Universal separation in the
switched Tait colouring permits at most one retained mark on each of the
\(d\) new affected circuits.  Consequently
\[
                            d\ge q-1.                 \tag{7}
\]
Combining (5) and (7) gives
\[
                         2q-1\le6,
 \qquad\text{and hence}\qquad q\le3.                 \tag{8}
\]

> **Short-factor support lemma.**  Every marked core \(C_{10}\) in
> either bichromatic factor meets at most three circuits of the opposite
> factor.

This proof does not assume that the opposite factor circuits are short.

## 3. Two short circuits meet at most once

The overlap lemma from
`equality88-kempe-girth-contradiction.md` is local and applies verbatim
to any two short circuits.  Each lifts from a core \(C_{10}\) to a
\(C_{11}\) in \(K\subseteq G\).

- A diagonal pair already shares the two-edge path replacing its common
  mark.  A second common \(c\)-edge makes the symmetric difference have
  length at most 16; that edge is a chord producing a circuit of length
  at most nine.
- For an off-diagonal pair, three common edges give the same immediate
  chord contradiction.  With exactly two common edges, the symmetric
  difference is a \(C_{18}\).  Both common edges must be antipodal
  chords.  The alternating residual path lengths then give
  \(2\alpha=9\), impossible.

Thus
\[
 |E(A)\cap E(B)|\le1                                  \tag{9}
\]
whenever \(A\) and \(B\) are both short.

## 4. A \(C_{10}\) and a \(C_{12}\) meet at most twice

We also need one extension of (9).

> **Lemma 4.1 (mixed overlap).**  If \(A\) is a marked core
> \(C_{10}\) and \(B\) is a marked core \(C_{12}\) from the opposite
> factor, then
> \[
>                         |E(A)\cap E(B)|\le2.        \tag{10}
> \]

### Proof

The lifted circuits \(\widetilde A,\widetilde B\) have lengths 11 and
13.

If the pair is diagonal, its common mark lifts to a two-edge path.  If
the core multiplicity is \(r\ge3\), it also shares \(r-1\) ordinary
\(c\)-edges, and the symmetric difference has length
\[
                 11+13-2\bigl(2+(r-1)\bigr)
                    =22-2r\le16.                    \tag{11}
\]
It is one circuit by girth, and any common unmarked edge is a chord
forming a circuit of length at most nine.

Now suppose the pair is off-diagonal.  Its common edges are ordinary
unmarked \(c\)-edges.  If \(r\ge4\), the symmetric difference has length
\[
                         24-2r\le16,                 \tag{12}
\]
and the same chord contradiction applies.

It remains to exclude \(r=3\).  The symmetric difference has length 18,
so girth makes it one \(C_{18}\), say \(L\).  Each of the three common
edges is a chord of \(L\).  Both circuits made from that chord and the
two complementary \(L\)-arcs have length at least ten.  Since the arcs
sum to 18, both have length nine.  Thus all three common-edge chords
join antipodal points of the metric \(C_{18}\).

List the six chord endpoints in cyclic order as
\[
                         v_0,v_1,\ldots,v_5.
\]
Half-turn by distance nine preserves their set and pairs antipodes, so
after a cyclic relabelling the three chords are
\[
                         v_0v_3,\ v_1v_4,\ v_2v_5.   \tag{13}
\]
Let \(w_i>0\) be the length of the \(v_i\)-to-\(v_{i+1}\) residual
path on \(L\), with indices modulo six.  The paths alternate between
\(\widetilde A\) and \(\widetilde B\).  Antipodality gives
\[
                         w_i+w_{i+1}+w_{i+2}=9
 \quad(0\le i<6).                                    \tag{14}
\]
Subtracting consecutive equations yields
\[
                         w_i=w_{i+3}.                 \tag{15}
\]
The three-step shift exchanges the \(A\)-paths and \(B\)-paths.
Therefore their total residual lengths are equal.  But deleting three
ordinary edges from the lifted circuits gives totals
\[
                         11-3=8,\qquad13-3=10,        \tag{16}
\]
a contradiction.  This proves (10). \(\square\)

## 5. Degree budgets for \(t=0,1,2\)

In the \(bc\)-factor, a circuit of core length \(10+2h\) is incident
with \(5+h\) \(c\)-edges.  Let \(\mathcal B_L\) be the set of long
\(bc\)-circuits.  From (3),
\[
 \sum_{B\in\mathcal B_L}\deg_\Gamma(B)
     =5|\mathcal B_L|+t
     \le6t,                                           \tag{17}
\]
because every long circuit consumes at least one unit of surplus, so
\(|\mathcal B_L|\le t\).

Fix a short \(ac\)-circuit.  It has five incidence edges and, by the
short-factor support lemma, at most three opposite support vertices.
Every short opposite vertex contributes at most one edge by (9).
It follows that at least three of its five incidence edges go to long
opposite circuits.

There are at least \(8-t\) short \(ac\)-circuits, so
\[
 \sum_{B\in\mathcal B_L}\deg_\Gamma(B)
          \ge3(8-t).                                  \tag{18}
\]
For \(t=1,2\), inequalities (17) and (18) give respectively
\[
                       21\le6,\qquad18\le12,
\]
both impossible.  When \(t=0\), there is no long opposite circuit at
all, while a short row would need five distinct short neighbours,
contradicting its support bound three.  Thus ambient orders 88, 90, and
92 are excluded.

## 6. The \(t=3\) case

For \(t=3\), (18) requires at least 15 incidences at long \(bc\)-factor
vertices.  If there were one or two long circuits, (17) sharpens to,
respectively,
\[
                         5+3=8,\qquad10+3=13,
\]
which is still too small.  Hence the only surviving length partition
would have exactly three long circuits, each a core \(C_{12}\).  Their
total incidence capacity is
\[
                         3\cdot6=18.                  \tag{19}
\]

There are at least five short \(ac\)-circuits.  For any one of them,
the support bound permits at most three opposite circuits.  By (9), a
short opposite circuit contributes at most one incidence; by Lemma 4.1,
a long \(C_{12}\) contributes at most two.

One long and two short support vertices could contribute at most
\[
                         2+1+1=4<5.
\]
Thus the row uses at least two long support vertices.  If it uses two,
at most one short support remains and at least four of its five edges go
to the long vertices.  If it uses all three long support vertices, all
five do.  Every short row therefore contributes at least four
incidences to the three long \(B\)-vertices.  The five short rows demand
at least
\[
                         5\cdot4=20                  \tag{20}
\]
such incidences, exceeding the capacity 18 in (19).  This contradiction
excludes \(t=3\), or ambient order 94.

## 7. Scoped conclusion

Combining the four cases:

> **Short-factor surplus theorem.**  In the connected eight-mark
> extremal exact-zero size-four minimum-counterexample branch,
> \[
>                         |V(G)|\ge96.                \tag{21}
> \]

This is a branch-specific lower bound.  It does not prove that arbitrary
cubic graphs below order 96 have five-cycle double covers, and it does
not address:

- exact-zero supports of other sizes before the minimum-support
  reduction is invoked;
- the unresolved exchange step producing the extremal size-four branch;
- the cyclic four-cut exceptional-signature problem;
- the rooted component-parity obligation at the cyclic six-cut; or
- the connected eight-mark branch at order 96 and above.

The proof should not be promoted beyond **proof draft** until an
independent audit has checked the rank argument in Lemma 2.1 and the
antipodal ordering in Lemma 4.1.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the three-matching rank
bound, the surplus degree budget, and the mixed-overlap chord argument,
and drafted this note.  Every deduction is displayed for direct human
checking.  No finite search or solver output is used as proof.  This is
not independent human peer review and does not resolve five-CDC.
