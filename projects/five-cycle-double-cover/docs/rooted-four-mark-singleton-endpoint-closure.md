# The singleton endpoint obstruction closes

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE LEMMA / EXACT \(1+3\) SINGLETON BRANCH
CLOSED / CONDITIONAL ON THE SIMULTANEOUS PREMISES STATED BELOW**.

This note closes the last path obstruction isolated in
`rooted-four-mark-p4-row-star-reduction.md`.  The result is deliberately
scoped.  It assumes simultaneously the original two-separation
irreducibility, the four pairwise vertex-disjoint private circuits,
triple cyclability, and \(Z\)-acyclicity.  It does not assert that all of
these data survive an arbitrary one-terminal preprocessing reduction.

The only external input in the endpoint lemma is the path-obstruction
description in Section 4.9 of Kenta Ozeki's dissertation,
[*Structural Characterizations of Rooted Subdivisions on Four
Vertices*](https://repository.dl.itc.u-tokyo.ac.jp/record/2009547/files/A39572.pdf),
pages 79--80.  For transparency, the exact two outcomes used from that
description and the elementary degree contradictions are reproduced
below.

## 1. Exact setup

Let \(H\) be a finite simple 2-connected subcubic graph with four
distinct degree-two terminals
\[
                         Z=\{z_1,z_2,z_3,z_4\}.
\]
Assume:

1. no nonempty proper side of a 2-separation is terminal-free;
2. a proper side of a 2-separation containing exactly one terminal
   consists of that terminal alone;
3. there are pairwise vertex-disjoint circuits
   \(R_i\subseteq H\), with \(z_i\in V(R_i)\);
4. every three terminals lie on a circuit; and
5. no circuit contains all four terminals.

Suppose \(w,u\notin Z\), the components of \(H-\{w,u\}\) are
\[
                         \{z_1\}\quad\text{and}\quad B,
                                                        \tag{1}
\]
where \(z_2,z_3,z_4\in B\).  Thus \(N_H(z_1)=\{w,u\}\).
Put
\[
                         K=H-\{w,z_1\}.                \tag{2}
\]

The goal is to prove that \(K\) has a simple path with initial vertex
\(u\) which contains \(z_2,z_3,z_4\).

## 2. The large-side graph is 2-connected

> **Large-side block lemma.**
> The graph \(K\) is 2-connected.  Moreover,
> \[
>             \deg_K(u)=\deg_K(z_2)=\deg_K(z_3)=\deg_K(z_4)=2.
>                                                        \tag{3}
> \]

### Proof

The graph \(H-w\) is connected because \(H\) is 2-connected.  In
\(H-w\), the vertex \(z_1\) is a leaf adjacent to \(u\).  Deleting that
leaf shows that \(K\) is connected.  Also,
\[
                         K-u=B
\]
is connected by (1).

Suppose that \(x\) is a cut vertex of \(K\).  Then \(x\ne u\).  The
components of \(H-\{w,x\}\) are exactly the components of \(K-x\), with
\(z_1\) adjoined to the component containing \(u\).

Each such component contains a terminal.  Otherwise it and the
separator \(\{w,x\}\) give a forbidden terminal-free side.  A component
containing exactly one terminal would have to be the singleton
consisting of that terminal.  It cannot be the component containing
\(z_1\), because that component also contains \(u\).  Hence it would be
\(\{z_i\}\) for some \(i\in\{2,3,4\}\).

But a circuit through a degree-two vertex uses both of its incident
edges.  The singleton condition would make both neighbours of \(z_i\)
belong to \(\{w,x\}\), so \(R_i\) would contain \(w\).  The circuit
\(R_1\) also contains \(w\), because it uses the edge \(z_1w\).  This
contradicts the vertex-disjointness of \(R_1\) and \(R_i\).

Consequently every component of \(H-\{w,x\}\) contains at least two
terminals.  There are exactly two components, with a \(2+2\) terminal
split.  This is impossible under triple cyclability and
\(Z\)-acyclicity: a circuit through the two terminals on the first side
and one terminal on the second supplies a \(w\)-to-\(x\) path through
the first pair; the symmetric choice supplies a \(w\)-to-\(x\) path
through the second pair.  Their interiors lie in different components,
so their union is a circuit through all four terminals.

Thus \(K\) has no cut vertex and is 2-connected.

The vertex \(u\) loses precisely the edge \(uz_1\) on passing from \(H\)
to \(K\).  Since \(H\) is subcubic and \(K\) is 2-connected,
\[
                         2\le\deg_K(u)\le2.
\]
For \(i\ge2\), the circuit \(R_i\) is disjoint from \(R_1\), hence avoids
\(w\).  Since \(R_i\) uses both edges at \(z_i\), the vertex \(w\) is
not adjacent to \(z_i\).  Therefore deletion of \(w\) does not change
the degree of \(z_i\), and \(\deg_K(z_i)=2\).  This proves (3).
\(\square\)

## 3. A degree-two endpoint lemma

> **Subcubic endpoint-path lemma.**
> Let \(G\) be a finite simple 2-connected subcubic graph and let
> \(r,a,b,c\) be four distinct vertices of degree two.  Then \(G\)
> has a simple path starting at \(r\) and containing \(a,b,c\).

### Reduction to the irreducible path problem

Add a new leaf \(t\) adjacent to \(r\), and call the resulting graph
\(G^+\).  A path of \(G^+\) through
\[
                            \{t,a,b,c\}                \tag{4}
\]
has \(t\) as an endpoint.  Deleting \(t\) from it gives exactly the
required \(r\)-starting path in \(G\).

We may make Ozeki's one-terminal reductions without losing a possible
path.  Suppose \((A,B)\) is a 2-separation with separator
\(\{x,y\}\), and the proper interior \(A-B\) contains exactly one
terminal of the full set \(\{t,a,b,c\}\), namely
\(a\in\{a,b,c\}\), with \(|A-B|>1\).  The leaf \(t\) cannot belong to
the separator of a proper 2-separation, because
\(G^+-\{t,y\}=G-y\) is connected for every \(y\).  Thus \(t\notin A\).
Replace \(A\) by the fresh path
\[
                              x\,a'\,y,                \tag{5}
\]
transferring the terminal label from \(a\) to \(a'\).

Here are the lifting details, including the endpoint case.  Because
\(G\) is 2-connected, the original side contains an \(x\)-to-\(y\)
path through \(a\): take a circuit through \(a\) and a vertex in the
opposite proper side, and retain its segment in the displayed side.  It
also contains an \(x\)-to-\(a\) path avoiding \(y\), and a
\(y\)-to-\(a\) path avoiding \(x\), since \(G-y\) and \(G-x\) are
connected.  Therefore:

* if a path in the reduced graph uses \(x a' y\) internally, replace
  it by the original \(x\)-to-\(y\) path through \(a\);
* if it ends at \(a'\) through \(x a'\), replace that last edge by an
  \(x\)-to-\(a\) path avoiding \(y\); and
* use the symmetric replacement when it ends through \(y a'\).

The inserted paths meet the rest only at the used boundary vertices, so
the lifted path is simple.  The reduction preserves 2-connectivity and
subcubicity after the leaf \(t\) is deleted.  If a separator vertex is
one of the other degree-two terminals, 2-connectivity puts one of its
two incident edges on each proper side; replacing one side by one new
edge therefore preserves its degree.  Repeating the reduction
terminates.

The resulting pair \((G_*^+,\{t,a_*,b_*,c_*\})\) is irreducible in the
sense used in Ozeki's path description:

1. its only one-terminal side behind a cut vertex is the singleton
   leaf \(\{t\}\), because \(G_*^+-t\) is 2-connected; and
2. every one-terminal side behind a 2-separator whose terminal has
   degree two is a singleton, by construction.

All four terminal degrees are \(1,2,2,2\), respectively.

### The two obstruction outcomes are impossible

Section 4.9 of Ozeki's dissertation first observes, by the standard
augmentation argument, that in this irreducible \((1,2,2,2)\)-degree
case a four-terminal path exists if and only if there are three
internally disjoint terminal paths.  Mader's \(S\)-paths theorem
therefore gives, if there is no such path, a good
quasi-bipartite decomposition
\[
 (W;X_t,X_a,X_b,X_c;Y_1,\ldots,Y_m)                  \tag{6}
\]
of value at most two.  Put
\[
 s=|W|,\qquad h_i=|X_i\cap(Y_1\cup\cdots\cup Y_m)|,
 \qquad h=\sum_i h_i.
\]
Every \(Y_j\) meets at least three distinct \(X_i\), in an odd number
of vertices, and
\[
                 s+\frac{h-m}{2}\le2,\qquad h\ge3m.   \tag{7}
\]

The irreducibility and terminal degrees make the short case analysis
explicit.  For \(i\in\{a,b,c\}\),
\[
                              s+h_i\ge2,              \tag{8}
\]
since a boundary of order at most one would isolate the degree-two
terminal behind a one-separation.  Similarly \(s+h_t\ge1\).

If \(s=2\), (7) forces \(m=h=0\).  Thus deleting the two vertices of
\(W\) leaves no component containing two terminals.

If \(s=1\), inequalities (7)--(8) force
\[
                         m=1,\qquad h=3,
\]
and the single \(Y\)-part meets each of \(X_a,X_b,X_c\) once and misses
\(X_t\).  One-terminal irreducibility makes the proper interior of
each of those four parts its terminal alone.  Hence the unique vertex
of \(W\) is adjacent to \(t,a,b,c\).

Finally \(s=0\) is impossible: (8) gives \(h\ge7\), while (7) gives
\(h-m\le4\), hence \(m\ge3\); but then \(h\ge3m\) gives
\(h-m\ge2m\ge6\), a contradiction.  Values \(s>2\) are excluded by
(7).  Thus the only two possible obstruction forms are:

1. two nonterminals \(p,q\notin\{t,a,b,c\}\) can be deleted so that no
   component contains two terminals; or
2. there is one nonterminal \(p\notin\{t,a,b,c\}\) adjacent to all four
   terminals.

The second form is immediately impossible in a subcubic graph.

For the first form, work in the 2-connected graph
\(G_*=G_*^+-t\).  If \(r\notin\{p,q\}\), the component of
\(G_*-\{p,q\}\) containing \(r\), and each of the three components
containing \(a_*,b_*,c_*\), has at least two cut edges: a component
with cut edges only to one of \(p,q\) would make that vertex a cut
vertex of \(G_*\).  Thus at least eight edges are incident from
\(\{p,q\}\) to these four components.  If \(r\in\{p,q\}\), the leaf
\(t\) contributes its edge to the terminal separation, while the other
three terminal components each contribute at least two edges, for a
total of at least seven.  Both alternatives exceed
\[
                       \deg(p)+\deg(q)\le6.            \tag{9}
\]
These degrees are in \(G_*^+\).  If one of \(p,q\) is \(r\), then its
two edges in \(G_*\), together with the leaf edge \(rt\), still give
degree exactly three.
This contradiction eliminates the first form.

Hence \(G_*^+\), and therefore every earlier reduced graph, has a path
through (4).  Lifting all reductions and deleting \(t\) proves the
endpoint-path lemma. \(\square\)

## 4. Closure of the singleton branch

Apply the endpoint-path lemma to \(K\), with
\[
                         (r,a,b,c)=(u,z_2,z_3,z_4).
\]
The hypotheses follow from the large-side block lemma.  We obtain a
simple path in \(K\) starting at \(u\) and containing
\(z_2,z_3,z_4\), as required.

Adjoining the edge \(uz_1\) gives a path in \(H-w\) through all four
terminals.  Therefore:

> **Singleton-interface closure theorem.**
> Under the simultaneous premises of Section 1, the \(1+3\) singleton
> interface cannot be path-obstructing.

Together with the already proved \(2+2\) splicing lemma and the
three-vertex row-star elimination, this removes every path-obstructing
vertex in the exact irreducible/private-circuit state.

## 5. Finite transcription audit

The script `scratch/audit_subcubic_degree2_endpoint_path.py` exhaustively
checks the standalone endpoint lemma on every 2-connected simple cubic
graph through order \(12\), after subdividing every four-edge subset and
choosing each subdividing vertex in turn as the prescribed start.  It
checks \(1,100,688\) endpoint instances and finds no failure.
The frozen summary is
`scratch/subcubic-degree2-endpoint-path-audit-result.json`.  The audit
artifacts have SHA-256 hashes

```text
6f94b2049a3245aee2df48850f298d04a41b0540cc5a8eef343c5494542dc0c7  scratch/audit_subcubic_degree2_endpoint_path.py
59f831a6593905368615a7b8697f7dba2df6bc1da3325efc98159b05ecaa2e91  scratch/subcubic-degree2-endpoint-path-audit-result.json
```

This computation is only a transcription audit.  The proof above uses
no finite enumeration.

## AI-use disclosure

This lemma, its proof, and the audit program were developed by an OpenAI
Codex agent under human direction.  Ozeki's path-obstruction
description and Mader's \(S\)-paths theorem are prior work.  The new
contribution here is the large-side 2-connectivity argument, the
endpoint-sensitive lifting check, and the subcubic degree count joining
those inputs.  This is not independent human peer review and makes no
claim to resolve the Five-Cycle Double Cover Conjecture.
