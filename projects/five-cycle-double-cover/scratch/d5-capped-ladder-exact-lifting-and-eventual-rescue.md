# Exact cut-word lifting and eventual rescue on capped ladders

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE EVENTUAL-RESCUE THEOREM FOR A GRAPH FAMILY /
NOT A FIVECDC RESOLUTION**.

## 1. Setup

Let \(L_m\) be the capped ladder with nested two-edge cuts
\[
                         D_0,D_1,\ldots,D_{m+1}.
\]
Choose one noncentral internal edge in each terminal \(K_4-e\) diamond
as roots \(r,s\).  “Noncentral” means any of the four diamond edges
incident with an attachment vertex, rather than the edge joining the
two inner vertices.

For an arbitrary \(D_5\)-flow \(q\), write
\[
 \rho=q(r),\qquad \lambda_j=q(D_j),\qquad \sigma=q(s).          \tag{1}
\]
The notation \(q(D_j)\) is sound: xor the vertex equations on one side
of the two-edge cut, and its two labels are equal.

Regard a weight-two label as a vertex of the Johnson graph
\[
 J(5,2),
\]
where two labels are adjacent when they share exactly one coordinate.

## 2. Exact local lifting lemma

**Lemma 1 (cell transfer).**  Consecutive cut labels
\(\lambda_j,\lambda_{j+1}\) are adjacent in \(J(5,2)\).  For a
coordinate transposition \(\tau\):

- if \(\tau\) is active on both cut labels, the two selected factor
  strands pass straight through the ladder cell;
- if it is active on the left label and inactive on the right, the
  rung joins the two left strands in a U-turn;
- the reverse statement holds from the right.

**Proof.**  If \(L,R\) are the two rail labels and \(T\) the rung label,
the two cubic vertex equations both give
\[
                              L+R+T=0.
\]
All three are weight two, so they are the three sides of a coordinate
triangle; in particular \(L,R\) are adjacent.  Apply the binary
activity functional for \(\tau\):
\[
                              t(L)+t(R)+t(T)=0.
\]
If \(t(L)=t(R)=1\), then \(t(T)=0\), giving the two straight strands.
If \(t(L)=1,t(R)=0\), then \(t(T)=1\), giving the U-turn. \(\square\)

**Lemma 2 (cap transfer).**  In a terminal diamond, the label of a
noncentral root edge is adjacent to the attachment-cut label.  If a
factor is active on the root, its root component reaches both
attachment edges if and only if the factor is active on their common
label.

**Proof.**  Name the attachment vertices \(a,b\), the inner vertices
\(p,q\), and the cut edges \(aa',bb'\).  The five internal diamond
edges are
\[
                         ap,aq,bp,bq,pq.
\]
By symmetry take the noncentral root to be \(ap\).  At \(a\), cubic
parity makes the labels of \(aa',ap,aq\) the three sides of one
coordinate triangle, so the root and cut labels are adjacent.

Assume a factor is active on \(ap\).  If it is also active on the cut
label, then both \(aa'\) and \(bb'\) are active.  At \(a\), local even
degree pairs \(aa'\) with \(ap\), so the root component already contains
one cut edge.  Delete the two external portions of the cut edges.  The
selected factor subgraph inside the diamond has odd degree only at
\(a,b\) and degree zero or two at \(p,q\).  Starting along
\(aa',ap\), its degree-two continuation is therefore a single path
ending at \(b\), hence at \(bb'\); it cannot close earlier or enter a
different component.  Thus the same root component contains both cut
edges.

If the cut label is inactive, both cut edges are absent.  Local even
degree at \(a\) then pairs the active root \(ap\) with \(aq\), and the
root component remains wholly inside the diamond.  This proves both
directions at the component level.  The literal checker independently
exhausts all 180 diamond labelings. \(\square\)

It follows that
\[
                W(q)=(\rho,\lambda_0,\ldots,\lambda_{m+1},\sigma) \tag{2}
\]
is a walk in \(J(5,2)\).

For a transposition \(\tau\), call a walk vertex **active** if its
two-subset contains exactly one coordinate moved by \(\tau\).

**Exact lifting lemma.**  Switching the \(\tau\)-factor component
containing \(r\) applies \(\tau\) to precisely the maximal
\(\tau\)-active prefix of \(W(q)\).  Switching at \(s\) applies it to
the maximal active suffix.  Conversely, every such abstract
prefix/suffix move is the word image of that actual root-component
switch.

This is immediate from Lemmas 1 and 2: straight transfers continue
through active cut labels, and the first inactive label forces the
U-turn.

## 3. The Johnson-walk theorem

An **endpoint move** on a walk in \(J(5,2)\) transposes its maximal
active prefix or suffix.

**Lemma 3 (endpoint recoloring).**  Holding the penultimate walk vertex
\(u\) fixed, its last neighbor \(x\) can be changed to any other
neighbor \(y\) using at most two suffix moves supported only on the last
vertex.

**Proof.**  Write \(u=\{a,b\}\).  A neighbor of \(u\) is specified by
the coordinate of \(u\) that it removes and the coordinate outside
\(u\) that it adds.  Transposing \(a,b\) changes the removed coordinate.
Transposing two coordinates outside \(u\), one of them the currently
added coordinate, changes the added coordinate.  Both transpositions
fix \(u\), are active on the last vertex when used, and generate all
\(2\cdot3=6\) neighbors. \(\square\)

**Theorem 4 (walk alternation).**  Every finite walk in \(J(5,2)\) can
be transformed by endpoint moves into a walk alternating between two
adjacent labels.

**Proof by induction on the walk length.**  Length at most two is
already alternating.  Let \(W^-\) be the walk with its last vertex
deleted.  By induction, \(W^-\) has an endpoint-move sequence to an
alternating walk.

Lift that sequence to \(W\).  A prefix move lifts directly: its
restriction to \(W^-\) is unchanged, whether or not it also reaches the
extra last vertex.  For a suffix move \(\tau\) of \(W^-\), let \(u\) be
the current last vertex of \(W^-\).  By Lemma 3, first change the extra
last vertex to \(\tau(u)\), without changing \(u\).  Now the actual
suffix \(\tau\)-move passes through the extra vertex and has exactly the
same restriction to \(W^-\) as the prescribed move.

After the lifted sequence, \(W^-\) alternates between adjacent labels
\(A,B\).  Its extra last vertex is a neighbor of the penultimate one.
Use Lemma 3 once more to change it to the required next label \(A\) or
\(B\).  The whole walk now alternates. \(\square\)

## 4. Eventual rescue theorem

**Theorem 5.**  For every \(D_5\)-flow on \(L_m\) and every choice of
one noncentral root edge in each cap, a finite sequence of
root-component switches makes the two roots share a factor circuit.

**Proof.**  Apply Theorem 4 to \(W(q)\), and lift every endpoint move
using the exact lifting lemma.  Let the final word alternate between
adjacent labels \(A,B\).  Their symmetric difference
\[
                              \tau=A+B
\]
is a coordinate pair and is active on both \(A\) and \(B\).  Hence its
factor is active at both roots and on every cut.  Lemmas 1 and 2 show
that the root component passes through every cell and contains both
roots. \(\square\)

Thus capped ladders have no closed bad rooted orbit for these roots.
Together with the \(H=0\) lower-bound construction, the family has
finite but unbounded rescue delay.

## 5. \(H=0\) corollary

In the uniform \(H=0\) construction, choose the right root to be any
noncentral cap edge.  Its Tait label is one of \(01,02,12\), hence is
disjoint from the transformed left-root label \(34\).  According to the
missing coordinate \(h\in\{0,1,2\}\), one of
\[
 (04,34,03),\qquad(13,34,14),\qquad(24,34,23)
\]
has
\[
 K_1=K_3=\{0,1,2,3\},\qquad
 K_2=\{0,3,4,5,6,7\}.
\]
Therefore \(H=0\) and \(Z=\{1,2,4,5,6,7\}\), while the cut-word theorem
still gives delay at least \(\lfloor(m+1)/3\rfloor\).  Theorem 5 proves
that every member is nevertheless eventually rescued.

## 6. Scope

This settles the exact lifting question for a serial chain of cubic
ladder cells capped by diamonds.  It does not extend automatically
across a branching network, a cyclic chain, a higher-order multipole,
or arbitrary cubic graph.  The missing global problem is no longer
word termination on a path, but whether a minimal closed bad rooted
orbit can be reduced to path-like transfer blocks.

## Reproduction

```text
python3 scratch/check_d5_capped_ladder_exact_lifting.py
```

The checker exhausts the local diamond and cell labelings, checks the
constructive Johnson-walk induction on every normalized walk through
length six, and directly lifts the produced word moves to actual
capped-ladder factor components for \(L_2,\ldots,L_8\).

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the exact transfer
rules, proved the Johnson-walk induction and eventual-rescue theorem,
implemented independent exhaustive checks, and drafted this note.  This
is not peer review and is not a resolution of FiveCDC.
