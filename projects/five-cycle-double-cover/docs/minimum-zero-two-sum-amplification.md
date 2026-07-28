# Two-edge sums amplify the minimum-zero extension gap

Status: **HUMAN-CHECKABLE COMPOSITION THEOREM / INFINITE ROUTE
COUNTERMODEL FAMILY / NOT A FIVE-CDC COUNTEREXAMPLE FAMILY**.

The exact 130-vertex graph in
`search/minimum-zero-exchange-countermodel-130v-20260727/` has

\[
 r_f(G)=r_M(G)=5,\qquad \eta(G)=6,
\]

where \(\eta(G)\) is the least matching size in a matching/four-flow
five-cover certificate.  This note shows that the gap
\(\eta-r_M\) can be made arbitrarily large even among connected simple
bridgeless cubic graphs.

## 1. The two-edge sum

Let \(G_1,G_2\) be disjoint connected bridgeless cubic graphs and choose
ordinary edges

\[
 e_1=u_1v_1,\qquad e_2=u_2v_2.
\]

Delete \(e_1,e_2\) and add

\[
 f=u_1u_2,\qquad g=v_1v_2.
\]

Call the resulting graph \(H=G_1\#_2G_2\).  The crossed pairing gives the
same conclusions.  The graph \(H\) is connected, cubic, and bridgeless.
It is simple when the factors are simple, because the new edges join
different factors.

## 2. Flow zero counts are additive

Let \(\phi\) be an \(\mathbb F_2^2\)-flow on \(H\).  Sum its conservation
equations over \(V(G_1)\).  Every internal edge cancels, leaving

\[
 \phi(f)+\phi(g)=0.
\]

Thus \(\phi(f)=\phi(g)=a\).  Restore \(e_i\) in each factor and assign it
the value \(a\).  This gives flows \(\phi_i\) on \(G_i\).

If \(a\ne0\), neither new cut edge nor either restored root edge is zero.
If \(a=0\), both new cut edges and both restored root edges are zero.
Consequently

\[
 |Z(\phi)|=|Z(\phi_1)|+|Z(\phi_2)|.                 \tag{1}
\]

Conversely, two factor flows having the same root value glue across the
two-edge cut.  For two identical rooted copies, identical minimum flows
therefore glue, and (1) gives

\[
 r_f(G\#_2G)=2r_f(G).                               \tag{2}
\]

When the factor zero sets are matchings, the glued zero set is a matching
as well.  In the zero-root case the two new zero edges are disjoint and
replace the two deleted matching edges.  Hence identical
matching-supported minimum flows also give

\[
 r_M(G\#_2G)=2r_M(G)                                \tag{3}
\]

whenever \(r_f(G)=r_M(G)\).

## 3. Matching/four-flow extensions are additive

Let \((M,A,B,\phi)\) be a matching/four-flow certificate on \(H\).  A
binary cycle crosses every cut evenly, so each of \(A\) and \(B\) contains
either both of \(f,g\) or neither.  Restore \(e_i\) with this common
membership in each factor.  The preceding flow argument restores their
common flow value.  The identities

\[
 M=A\cap B=Z(\phi)
\]

are preserved, as is the matching condition.  The matching count again
satisfies

\[
 |M|=|M_1|+|M_2|.                                   \tag{4}
\]

Therefore every certificate on the sum restricts to certificates on both
factors, giving

\[
 \eta(G_1\#_2G_2)\ge\eta(G_1)+\eta(G_2).
\]

For two identical rooted copies, glue identical minimum certificates.
Their root states agree in both cycle bits and both flow bits, so equality
holds:

\[
 \eta(G\#_2G)=2\eta(G).                              \tag{5}
\]

The same gluing applied to the reverse-lifted \(D_5\) labels assigns the
two new edges the old common root label.  Thus standard five-covers glue
as well.

## 4. Infinite connected family

Let \(G_0\) be the certified 130-vertex graph, and recursively form
\(G_{n+1}\) as a two-edge sum of two identical copies of \(G_n\), using
corresponding root edges and retaining any other edge as the next root.
Equations (2), (3), and (5) give

\[
\boxed{
 r_f(G_n)=r_M(G_n)=5\cdot2^n,\qquad
 \eta(G_n)=6\cdot2^n.
}
\]

Hence

\[
 \eta(G_n)-r_M(G_n)=2^n
\]

is unbounded.  Every \(G_n\) is finite, simple, connected, bridgeless, and
cubic, and every one has an explicit standard five-cover.

The family has a cyclic two-edge cut at every composition step.  It
therefore refutes the unrestricted minimum-zero exchange strategy very
strongly but does not refute a version restricted to cyclically
4-edge-connected, girth-at-least-ten minimum-counterexample candidates.

## AI disclosure

This composition argument was developed with substantial assistance from
OpenAI Codex agents under human direction.  The proof above is elementary
and self-contained; it requires no solver or trust in an AI system beyond
the separately certified finite base graph.
