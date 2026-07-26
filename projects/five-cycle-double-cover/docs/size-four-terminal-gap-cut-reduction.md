# Terminal-gap lift failures reduce to quotient cut certificates

## Status

This note tests the obstruction in
`docs/two-tjoin-cycle-lift-obstruction.md` against the actual connected
size-four minimum-counterexample reduction.

There are two conclusions.

1. The four-vertex minimal nonliftable quotient from that note cannot occur
   as the factor quotient of the connected eight-mark branch.  It violates
   the number of marked factor circuits, the marked-girth degree bound, and
   the paired cyclic-cut inequality.
2. More generally, an unavoidable failure at the gap containing one
   terminal is equivalent to an even-terminal 2-edge cut in the factor
   quotient.  The paired-cut inequality then turns it into a cyclic
   4- or 6-edge cut of the ambient graph containing respectively two or
   four edges of the zero matching.

There is also an exact cut-space certificate for simultaneous failure of
the terminal-gap conditions at several marked factor circuits.

This is a rigorous reduction of one obstruction pattern, not a closure of
the connected size-four branch.  It does not settle the remaining
same-parity gap equations, it does not treat all non-partitioning pairs of
quotient joins, and it does not resolve the five-cycle-double-cover
conjecture.

## 1. Exact hypotheses

Let \(H\) be a connected simple cubic graph, let \(S\subseteq E(H)\) be
an eight-edge matching, and let \(P\) be a perfect matching on the eight
edge objects in \(S\).  Subdivide every \(s\in S\) by a terminal \(t_s\),
and for every pair \(ss'\in P\) add \(t_st_{s'}\).  Call the resulting
cubic graph \(G\), and call the four added edges \(M\).

Assume the hypotheses inherited in the connected extremal size-four
branch:

1. \(H\) is Tait-colourable and \(S\) is universally separated;
2. the eight marks and hence the eight terminals are distinct;
3. every circuit \(D\) of \(H\) satisfies the marked-girth inequality
   \[
       |E(D)|+|E(D)\cap S|\ge 10;                    \tag{1}
   \]
4. \(G\) is cyclically 4-edge-connected, equivalently for the applications
   below it satisfies the paired-cut inequality derived from that
   connectivity; and
5. \(M\) is cardinality-minimum among exact-zero matchings of
   \(\mathbb F_2^2\)-flows on \(G\).

The fifth condition is part of the actual branch but is not needed for the
cut reduction proved here.  The point is useful: this obstruction pattern
is reduced before any new minimum-support exchange theorem is invoked.

Use universal precolouring to give all eight marks one Tait colour \(c\);
write the other colours as \(a,b\).  Let \(F\) be the lifted \(ac\)-factor
in \(K=G-M\).  Contract every factor circuit and retain all complementary
\(b\)-edges, including loops and parallel edge objects.  Denote the
resulting connected Eulerian multigraph by \(R\).

The eight terminal-containing factor circuits give eight distinct marked
vertices
\[
     U\subseteq V(R),\qquad |U|=8.                    \tag{2}
\]
The four edges of \(M\) induce the perfect matching \(P\) on \(U\).

For \(X\subseteq V(R)\), let
\[
 p_P(X)=|\{uv\in P:u\in X,\ v\notin X\}|.             \tag{3}
\]

## 2. Quotient restrictions forced by the actual branch

> **Lemma 2.1 (degree and paired-cut restrictions).**
> Every vertex of \(R\) has even degree at least 10, where a quotient loop
> contributes two.  Moreover, for every nonempty proper
> \(X\subset V(R)\),
> \[
>      |\delta_R(X)|+p_P(X)\ge4.                       \tag{4}
> \]

### Proof

A vertex \(q\) of \(R\) comes from an \(ac\)-circuit \(C\) of the core.
Every core vertex of \(C\) has one incident \(b\)-edge, so
\[
       d_R(q)=|V(C)|.                                  \tag{5}
\]
This equality counts both ends of a quotient loop.

The core circuit \(C\) is even.  Universal separation puts either zero or
one marks on it.  If it is unmarked, (1) gives \(|C|\ge10\).  If it is
marked, then
\[
       |C|+1\ge10,
\]
and evenness of \(|C|\) again gives \(|C|\ge10\).  Equation (5) proves the
degree assertion.

For (4), take the union \(Y\) in \(H\) of all \(ac\)-circuits represented
by \(X\).  Both \(H[Y]\) and its complement contain an \(ac\)-circuit.
All marks lie inside factor circuits, so no marked edge crosses this core
shore.  Its unpaired boundary consists exactly of the \(b\)-edge objects
in \(\delta_R(X)\).  In the expansion, the added matching edges that cross
are exactly the \(P\)-edges counted by \(p_P(X)\).  Hence the corresponding
cyclic cut of \(G\) has size
\[
       |\delta_R(X)|+p_P(X).
\]
Cyclic 4-edge-connectivity gives (4). \(\square\)

There is a useful singleton consequence.  If \(q\in U\), exactly one edge
of \(P\) leaves \(\{q\}\), so
\[
       |\delta_R(q)|+1\ge4.                            \tag{6}
\]
The nonloop incidence count \(|\delta_R(q)|\) is even because \(R\) is
Eulerian and loops contribute an even amount.  Thus
\[
       |\delta_R(q)|\ge4.                              \tag{7}
\]
Adding quotient loops cannot hide a two-edge attachment of a marked factor
circuit.

## 3. The four-vertex obstruction is excluded

The minimal quotient from
`docs/two-tjoin-cycle-lift-obstruction.md` has vertices
\[
 0,1,2,3
\]
and edges
\[
 a,a':03,\qquad b:12,\qquad c:13,\qquad d:23,          \tag{8}
\]
with all four vertices marked.  Its degrees are \(2,2,2,4\).

It cannot be the quotient \(R\) above for three independent reasons.

1. It has four marked vertices, whereas (2) requires eight distinct marked
   quotient vertices.
2. Its degrees violate the lower bound \(d_R(q)\ge10\).
3. At each of the marked vertices \(0,1,2\), the nonloop singleton boundary
   has size two.  Since exactly one \(P\)-edge leaves a marked singleton,
   the lifted cyclic cut would have size \(2+1=3\), contradicting (6).

The third point also rules out every attempted repair that merely adds
quotient loops to those three vertices.  Loops increase total degree but
do not cross the factor-circuit shore.

Thus the literal minimal obstruction is not a compliant candidate for the
connected size-four branch.

## 4. The exact terminal-gap equation for a partitioning pair

The Eulerian construction produces a \(U\)-join \(J\subseteq E(R)\) and
its complement
\[
       J'=E(R)\setminus J.
\]
Because \(R\) is Eulerian, \(J'\) is also a \(U\)-join.  The pair
\((J,J')\) partitions all quotient edges.

Fix a marked factor circuit \(C_q\), where \(q\in U\).  In the suppressed
core, its unique marked \(c\)-edge has endpoints \(u_q,v_q\).  Let
\[
       \ell_q,\ r_q\in E(R)                            \tag{9}
\]
be the two quotient \(b\)-edge objects incident with \(u_q,v_q\),
respectively.  These are the two ports immediately flanking the terminal
gap after the marked edge is subdivided.

The edge objects \(\ell_q,r_q\) are distinct.  If they were the same
original \(b\)-edge, it would join \(u_q\) to \(v_q\), parallel to the
marked \(c\)-edge in the simple core \(H\).

The one-terminal local lift criterion says that the two endpoints of the
terminal gap must have different quotient-join colours.  For the
partitioning pair \((J,J')\), this is precisely
\[
  1_J(\ell_q)+1_J(r_q)=1\pmod2.                        \tag{10}
\]

Equation (10) is necessary but not by itself sufficient for the full lift:
the other gaps in the same alternating class must have equal-coloured
endpoints.  We first analyze exactly when even this necessary equation is
unavoidable or repairable.

## 5. One terminal: repair by a quotient cycle or a 2-cut certificate

> **Theorem 5.1 (single terminal-gap cut alternative).**
> Let \(R\) be connected and Eulerian, let \(U\subseteq V(R)\) be even,
> and let \(\ell,r\) be distinct edge objects.  There is a \(U\)-join
> \(J\) satisfying
> \[
>       1_J(\ell)+1_J(r)=1                              \tag{11}
> \]
> unless
> \[
>       \delta_R(X)=\{\ell,r\}                          \tag{12}
> \]
> for some \(X\subseteq V(R)\) with
> \[
>       |X\cap U|\equiv0\pmod2.                         \tag{13}
> \]
> Conditions (12)--(13) are also sufficient to make (11) impossible for
> every \(U\)-join.

### Proof

The binary cycle space of a connected multigraph is orthogonal to its cut
space.  Loops are cycle-space coordinates and never occur in a cut.

Start with any \(U\)-join \(J_0\), which exists because \(R\) is connected
and \(|U|\) is even.  If the two-edge vector
\[
       \mathbf1_{\{\ell,r\}}
\]
is not in the cut space, orthogonality gives a binary cycle \(Z\) with
\[
       |Z\cap\{\ell,r\}|\equiv1\pmod2.
\]
Then \(J_0\mathbin{\triangle}Z\) is another \(U\)-join and has the
opposite value of the left side of (11).  One of \(J_0\) and
\(J_0\triangle Z\) therefore satisfies (11).

If the two-edge vector is in the cut space, it equals
\(\delta_R(X)\) for some \(X\).  For every \(U\)-join \(J\), summing its
boundary equation over \(X\) gives
\[
\begin{aligned}
  1_J(\ell)+1_J(r)
    &=|J\cap\delta_R(X)|\\
    &\equiv|X\cap U|\pmod2.                            \tag{14}
\end{aligned}
\]
Thus (11) holds for all \(U\)-joins when \(|X\cap U|\) is odd and fails
for all of them when it is even.  This proves both directions. \(\square\)

This theorem also gives a constructive repair.  Unless the cut certificate
exists, find a quotient cycle containing exactly one of the two flanking
edges and replace \(J\) by \(J\triangle Z\).  The complement changes by
the same switch, so the pair still partitions \(E(R)\).

The theorem repairs one terminal gap.  The cycle switch may change gap
conditions at other factor circuits, which is why it is not yet a
simultaneous closure theorem.

## 6. What the paired-cut inequality does to the certificate

Apply Theorem 5.1 with \(\ell=\ell_q,r=r_q\).  If the terminal gap at
\(q\) is impossible for every partitioning pair, there is a shore \(X\)
with
\[
       \delta_R(X)=\{\ell_q,r_q\},\qquad |X\cap U|
       \text{ even}.                                   \tag{15}
\]

For a perfect matching \(P\) on \(U\),
\[
       p_P(X)\equiv|X\cap U|\pmod2.                     \tag{16}
\]
Indeed, internal pairs contribute two vertices to \(X\), external pairs
contribute zero, and crossing pairs contribute one.

Equations (4), (15), and (16) imply
\[
       p_P(X)\ge2,\qquad p_P(X)\text{ even}.
\]
There are only four pairing edges, so
\[
       p_P(X)\in\{2,4\}.                                \tag{17}
\]

The corresponding cut of the ambient cubic graph \(G\) consists exactly
of:

- the two nonzero \(b\)-edges \(\ell_q,r_q\); and
- the \(p_P(X)\) zero edges of \(M\) whose terminal circuits lie on
  opposite shores.

Both shores contain factor circuits.  Hence:

> **Corollary 6.1.**
> An unavoidable single-terminal-gap failure in the actual branch forces
> either
>
> 1. a cyclic 4-edge cut containing exactly two edges of \(M\), or
> 2. a cyclic 6-edge cut containing all four edges of \(M\).

This is the promised graph-theoretic reduction of the local obstruction.
The cyclic 4-edge-connected hypothesis permits both outcomes; a further
four-/six-cut or minimum-support argument is required to eliminate them.

## 7. The minimal obstruction's forcing mechanism

In the four-vertex quotient (8), the failed marked factor circuit is the
one at vertex 3.  Its terminal-flanking edges are \(d,c\), and
\[
       \delta_R(\{1,2\})=\{c,d\}.                       \tag{18}
\]
The shore \(\{1,2\}\) contains two of the four quotient terminals, so its
terminal parity is even.  Equation (14) forces every \(T\)-join to use
either both of \(c,d\) or neither.  This is exactly why the endpoint
colours at the terminal gap are equal in both possible disjoint pairs.

Thus the small example is not an unexplained rotation accident.  Its
obstruction is the even-terminal 2-cut in (18).  The actual paired-cut
condition does not allow the example's additional marked degree-two
attachments, and any surviving version of its central forcing mechanism
must enter one of the two ambient cut branches in Corollary 6.1.

## 8. Simultaneous terminal-gap conditions

The eight equations (10) also have an exact human-checkable obstruction
certificate.

For \(W\subseteq U\), define the symmetric-difference edge vector
\[
       D(W)=
       \mathop{\triangle}_{q\in W}\{\ell_q,r_q\}.        \tag{19}
\]
Repeated edge objects cancel.

> **Theorem 8.1 (simultaneous cut-space criterion).**
> There is a \(U\)-join \(J\) satisfying
> \[
>       1_J(\ell_q)+1_J(r_q)=1
>       \qquad(q\in U)                                  \tag{20}
> \]
> if and only if, for every \(W\subseteq U\) and
> \(X\subseteq V(R)\) such that
> \[
>       D(W)=\delta_R(X),                                \tag{21}
> \]
> one has
> \[
>       |W|\equiv|X\cap U|\pmod2.                        \tag{22}
> \]

### Proof

Necessity follows by summing (20) over \(q\in W\):
\[
\begin{aligned}
 |W|
   &\equiv |J\cap D(W)|\\
   &=|J\cap\delta_R(X)|\\
   &\equiv|X\cap U|\pmod2.
\end{aligned}
\]

For sufficiency, write the \(U\)-join equations and (20) as one linear
system over \(\mathbb F_2\).  A linear dependency among its rows consists
of:

- a subset \(W\) of the gap equations; and
- a subset \(X\) of the vertex-boundary equations.

The left sides cancel exactly when (21) holds.  The corresponding right
sides are consistent exactly when (22) holds.  Therefore every row
dependency is consistent, which is the elementary solvability criterion
for a finite linear system. \(\square\)

A failed simultaneous system therefore has a concise certificate
\((W,X)\) satisfying (21) and violating (22).  The single-terminal theorem
is the case \(W=\{q\}\).

This criterion uses only the terminal gaps.  Once (20) is solved, the full
marked-circuit lift still requires equal-colour equations on every other
gap in the same alternating class.  Those are additional linear equations.
Every unmarked factor circuit contributes a choice between two alternating
classes, so the complete partitioning-pair problem is a small
XOR-with-phase-choice system rather than the purely linear system above.

## 9. Precisely what has and has not been reduced

Under all the stated size-four hypotheses, the following conclusions are
now rigorous.

1. The literal four-vertex minimal quotient cannot occur.
2. Merely adding quotient loops to its low-degree marked vertices cannot
   make it compliant.
3. A single marked terminal-gap obstruction that survives every
   Eulerian partitioning pair is equivalent to an even-terminal quotient
   2-cut.
4. The paired-cut inequality promotes that 2-cut to a cyclic ambient
   4-cut with two zero edges or a cyclic ambient 6-cut with four zero
   edges.
5. Simultaneous failure at several terminal gaps has the explicit
   cut-space certificate of Theorem 8.1.

The following statements are **not** proved.

- The cyclic 4- and 6-cut branches are not eliminated.
- Satisfying all terminal-gap equations is not yet the full local lift.
- A pair of edge-disjoint quotient \(U\)-joins need not partition all
  quotient edges; unused ports change the reduced cyclic word, and this
  note does not classify all such pairs.
- Cardinal minimum-support has not yet been converted into an inequality
  that excludes the certificates above.
- No compliant finite counterexample to the full size-four branch has
  been constructed.

Accordingly, this note closes one small obstruction pattern and identifies
the exact cut geometry of its surviving generalization.  It does not claim
a proof or disproof of five-cycle double cover.

## AI-use disclosure

This reduction, the cut-space formulation, and the exposition were
developed with substantial assistance from OpenAI Codex language-model
agents under human direction.  All hypotheses, parity equations, and
proofs are displayed explicitly.  The conclusions can be checked without
trusting an AI system or a computational search.
