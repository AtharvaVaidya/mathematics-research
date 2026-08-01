# The perfect-kernel Hušek--Šámal condition is a six-state transition CSP

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE EXACT REFORMULATION / NOT A FIVECDC
RESOLUTION**.

This note isolates the special case in which the kernel subgraph of the
selected binary functional is a perfect matching.  It gives an exact
finite-state formulation of clean fixed-projection lifting.  The
formulation is useful for proof search and certificate design, but the
Petersen graph already shows that it is not universally feasible.

## 1. Fixed perfect-matching projection

Let \(G\) be a finite loopless cubic graph and let \(N\) be a perfect
matching.  Put
\[
 h(e)=
 \begin{cases}
 0,&e\in N,\\
 1,&e\notin N.
 \end{cases}
\]
This is a binary flow because every vertex is incident with one edge of
\(N\) and two edges outside \(N\).

Let \(K=\mathbb F_2^2\), choose a vector \(b\notin K\), and consider
three-bit flows with fixed first coordinate \(h\):
\[
                         f(e)=b\,h(e)+s(e),                 \tag{1}
\]
where \(s:E(G)\to K\).  The map \(f\) is a flow exactly when \(s\) is a
\(K\)-flow.  It is nowhere zero exactly when
\[
                         s(e)\ne0\qquad(e\in N),             \tag{2}
\]
because the \(b\)-coordinate already makes every edge outside \(N\)
nonzero.

Contract every edge \(uv\in N\) to one vertex \(x\), obtaining the
four-regular quotient multigraph \(Q=G/N\).  The four incidences at \(x\)
come with a transition partition into two unordered pairs: the two
nonmatching edges incident with \(u\), and the two incident with \(v\).
Edge objects and incidences are retained, so parallel edges cause no
ambiguity.  If \(G\) is simple, no quotient loop arises from an edge
parallel to \(uv\).

For \(d\notin N\), call
\[
                              c(d)=s(d)\in K               \tag{3}
\]
its affine colour.  Thus there are four affine colours.

## 2. Exact local dichotomy

Fix \(uv\in N\), let \(x\) be its contracted vertex, and put
\(t_x=s(uv)\).  If the two transition pairs at \(x\) are
\(\{d_1,d_2\}\) and \(\{d_3,d_4\}\), flow conservation at \(u\) and
\(v\) says
\[
 c(d_1)+c(d_2)=t_x=c(d_3)+c(d_4).                         \tag{4}
\]
Condition (2) says \(t_x\ne0\).  Translation by a nonzero \(t_x\)
partitions the four points of \(K\) into two two-element orbits.  Hence
(4) has exactly two types:

1. both transition pairs use the same orbit; the four incident colour
   multiplicities are \(2,2,0,0\), in some order;
2. the transition pairs use the two complementary orbits; all four
   colours occur once.

The Hušek--Šámal component attached to \(uv\) is just the one-edge
component \(uv\) of the kernel subgraph.  Its defect bit is the common
parity of the four affine-colour multiplicities on its boundary.
Consequently type 1 is clean and type 2 is bad.

This proves the following exact reformulation.

> **Perfect-kernel transition theorem.**  The fixed projection \(h\)
> has a clean nowhere-zero lift (1) if and only if the edges of \(Q\)
> can be coloured by the four points of \(K\) so that, at every quotient
> vertex \(x\), there is a two-element set \(P_x\subset K\) and **each**
> of the two prescribed transition pairs receives the two distinct
> colours in \(P_x\).

### Proof of the converse

Given such a quotient colouring, put \(s(d)=c(d)\) on \(d\notin N\).
For \(uv\in N\), define
\[
                         s(uv)=\sum_{z\in P_x}z.             \tag{5}
\]
The two elements of \(P_x\) are distinct, so (5) is nonzero.  Each
transition pair sums to (5), proving flow conservation at both \(u\)
and \(v\).  Every matching component has affine multiplicities
\((2,2,0,0)\), hence is clean.  Formula (1) is therefore the required
nowhere-zero Hušek--Šámal-good lift.  The forward direction is the local
dichotomy above. \(\square\)

## 3. Six vertex states plus XOR

There are only six possible states \(P_x\in\binom K2\).  The theorem can
be split into a six-state vertex problem and a linear consistency check.

For an edge \(xy\) of \(Q\), its colour must lie in
\[
                              P_x\cap P_y.                  \tag{6}
\]
Thus adjacent states may not be disjoint.  If \(P_x\ne P_y\), their
nonempty intersection is a singleton and the edge colour is forced.  If
\(P_x=P_y\), the edge has the two colours in that common state available.

After the six-state assignment \(x\mapsto P_x\) is fixed, order the two
colours in each state.  Give every edge whose endpoint states agree one
binary variable selecting its colour.  Every edge with unequal endpoint
states has a forced local bit.  At each prescribed transition pair the
two local bits must differ.  These are ordinary affine XOR equations.

Hence:

> **XOR refinement.**  A six-state assignment lifts to a clean flow if
> and only if no adjacent states are disjoint and the resulting system
> of transition inequalities over \(\mathbb F_2\) is consistent.

This also gives short human-checkable negative certificates for a fixed
state assignment: either an edge joins disjoint states, or an XOR of
transition equations around a constraint cycle gives \(0=1\).  To prove
the whole fixed projection impossible one must still exclude all
\(6^{|V(Q)|}\) state assignments, normally with symmetry or a
certificate-producing finite search.

## 4. A minimal switch lock

The same local picture gives a precise obstruction to one family of
line-preserving switches.  Suppose \(uv\) is a bad one-edge kernel
component and \(t=f(uv)\in K-\{0\}\).  Its four affine boundary edges are
the four affine colours once each, with the two edges at \(u\) forming
one translation orbit under \(t\) and the two at \(v\) forming the other.

Any legal switch by \(t\) is supported on a binary cycle avoiding the
\(t\)-valued edge \(uv\).  At \(u\), such a cycle uses either both affine
edges or neither; the same holds at \(v\).  It therefore swaps whole
\(t\)-orbits and leaves all four boundary parities odd.

> **One-edge lock lemma.**  A bad one-edge kernel component of internal
> value \(t\) cannot be repaired by any sequence consisting only of legal
> \(t\)-cycle switches.  A fixed-line repair must use one of the other
> two nonzero kernel values, change the selected projection, or alter the
> flow by a more general move.

This is only a local switch obstruction.  It does not say that the
component is locked against the other two line values.

## 5. Scope and the surviving gap

The perfect-kernel transition theorem is not a universal existence
theorem.  For the Petersen graph, contracting any perfect matching gives
\(K_5\).  The certified fixed-line obstruction already retained in
`search/fano-two-cycle-petersen-countermodel-20260726/` proves that the
corresponding fixed perfect-matching projections have no clean lift.
The Petersen graph nevertheless has an explicit standard FiveCDC, using
a different projection.

Thus a FiveCDC proof cannot assume that some perfect matching is the
kernel of a good functional.  The exact remaining global obligation is
to choose both the three-bit flow and the binary projection; the
six-state theorem solves neither choice.

## AI-use disclosure

This transition-system reformulation, the XOR refinement, and the
one-edge lock proof were derived and drafted by an OpenAI Codex agent
under human direction.  They are elementary consequences of the
Hušek--Šámal component criterion and require independent human review
before scholarly use.  No FiveCDC resolution or novelty priority is
claimed.
