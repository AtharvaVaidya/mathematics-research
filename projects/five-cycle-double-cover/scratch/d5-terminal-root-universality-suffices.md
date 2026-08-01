# Why terminal rooted universality would prove FiveCDC

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE CONDITIONAL REDUCTION / NOT A FIVECDC
RESOLUTION**.

## 1. Statement

Put
\[
 D_5=\binom{[5]}2\subseteq\mathbb F_2^5.
\]
A \(D_5\)-flow on a loopless graph is a map
\(q:E(G)\to D_5\) whose incident labels xor to zero at every vertex.
For a coordinate pair \(ij\), put
\[
 Y_{ij}(q)=\{e:|q(e)\cap\{i,j\}|=1\}.
\]
Every \(Y_{ij}\) is Eulerian; on a cubic graph its nonempty components
are circuits.  A component Kempe switch transposes \(i,j\) on one such
component.

Fix two graph edges \(r,s\).  A state is **\((r,s)\)-good** if one
component of one \(Y_{ij}\) contains both \(r\) and \(s\).  A Kempe
orbit is **root-universal** if it contains an \((r,s)\)-good state for
every pair \(r,s\).

The following implication explains why the rooted Kempe problem is a
resolution route rather than only an internal property of graphs that
already have a five-cycle double cover.

> **Conditional reduction theorem.**  Suppose every connected
> bridgeless cubic graph that has a \(D_5\)-flow has root-universal
> Kempe orbits.  Then every finite bridgeless graph has a standard
> five-cycle double cover.

It is enough to assume the stronger terminal-plateau conjecture from
`preprint-d5-surface-kempe/main.tex`: every terminal
equal-surface-\(\chi\) plateau is root-universal.  Indeed, every state
has a nondecreasing Kempe path to a terminal plateau, so that conjecture
implies root-universality of every orbit.

The proof below isolates the two elementary operations used in the
induction.

## 2. Root insertion

Let \(H\) be a loopless cubic graph with distinct edges
\[
 r=u_1u_2,\qquad s=v_1v_2.
\]
Construct \(G\) by subdividing \(r\) with a new vertex \(u\),
subdividing \(s\) with a new vertex \(v\), and adding the edge \(uv\).

> **Lemma 2.1 (two-root insertion).**  If \(q\) is an
> \((r,s)\)-good \(D_5\)-flow on \(H\), then \(G\) has a
> \(D_5\)-flow.

### Proof

Choose \(ij\) and a circuit component \(K\) of \(Y_{ij}(q)\) containing
both \(r\) and \(s\).  First subdivide \(r,s\), giving both halves of
each subdivided edge its old label.  The circuit \(K\) becomes a circuit
\(K^*\) through the new degree-two vertices \(u,v\).

Choose either \(u\)-to-\(v\) arc \(A\) of \(K^*\), and transpose
\(i,j\) on every edge of \(A\).  Every edge of \(A\) is active in
\(Y_{ij}\), so its label changes by the vector \(ij\) and remains in
\(D_5\).  At every internal vertex of \(A\), exactly two incident
labels change by \(ij\), so conservation is preserved.  At each of
\(u,v\), exactly one of the two incident labels changes; the local xor
is therefore \(ij\).  Give the new edge \(uv\) the label \(ij\).
This restores xor zero at both new cubic vertices.  All other vertex
equations are unchanged.  The result is a \(D_5\)-flow on \(G\).
\(\square\)

This construction is completely nonorientable: no direction is chosen
on a cover member.

## 3. Edge elimination preserves bridgelessness in the hard case

Let \(G\) be a simple cubic graph, let \(e=uv\), and write
\[
 N(u)-v=\{u_1,u_2\},\qquad N(v)-u=\{v_1,v_2\}.
\]
The **edge elimination**
\[
 H=G\div e
\]
deletes \(u,v\) and adds the two edges
\[
 r=u_1u_2,\qquad s=v_1v_2.
\]
The inverse operation is precisely Lemma 2.1.

> **Lemma 3.1.**  If \(G\) is a simple cyclically
> \(4\)-edge-connected cubic graph of girth at least five, then
> \(G\div e\) is a smaller simple \(3\)-edge-connected cubic graph for
> every edge \(e\).

### Proof

The girth hypothesis makes the four displayed neighbours distinct in
exactly the ways needed to prevent loops, parallel new edges, and the
standard triangle/4-cycle failures of edge elimination.  Equivalently,
the elementary edge-reduction criterion says that an edge of a
connected cubic graph is irreducible only if it is a bridge, has an
endpoint in a triangle not containing the edge, or has both endpoints
on a 4-cycle not containing the edge.  Thus \(H\) is a smaller simple
connected cubic graph.

It remains to exclude a bridge \(b\) of \(H\).  Let \(X,Y\) be the
shores of \(H-b\).

If \(b=r\), then \(u_1,u_2\) lie on opposite shores, while both ends of
\(s\) lie on one shore; otherwise \(s\) itself would reconnect the
shores.  Restoring \(u,v,e\) makes the edge from \(u\) to the isolated
\(u_i\)-shore the unique edge entering that shore, so \(G\) would have
a bridge.  This is impossible.  The case \(b=s\) is symmetric.

Suppose instead that \(b\) is an old edge of \(G\).  Neither \(r\) nor
\(s\) crosses \((X,Y)\), because \(b\) is the unique crossing edge in
\(H\).  Hence each pair \(\{u_1,u_2\}\) and \(\{v_1,v_2\}\) lies
within one shore.  If both pairs lie on the same shore, restoring
\(u,v,e\) leaves \(b\) as a bridge of \(G\).  If they lie on opposite
shores, then \(\{b,e\}\) is a 2-edge-cut of \(G\).  Both conclusions
contradict 3-edge-connectivity.  Therefore \(H\) is bridgeless.

Suppose now that \(\delta_H(X)\) is a 2-edge-cut, and let \(t\) be the
number of roots crossing it.  If \(t=2\), put the two reinserted
vertices on the same shore; one spoke from each root crosses, giving a
2-cut of \(G\).  If \(t=1\), put both new vertices on the shore of the
noncrossing root; one old cut edge and one spoke cross.  If \(t=0\) and
both roots lie in one shore, the old 2-cut persists.  In the only
remaining case, the roots lie in opposite shores, and the two old cut
edges together with the reinserted edge form a 3-cut of \(G\).  Both
shores contain circuits, since a tree shore would satisfy
\(3|X|=2(|X|-1)+2\), an impossibility.  Every case contradicts cyclic
\(4\)-edge-connectivity.  Hence \(H\) is 3-edge-connected.
\(\square\)

## 4. Minimal-counterexample contradiction

The fixed-five reconstructions are written out in
`preprint-d5-surface-kempe/main.tex` and independently audited in
`scratch/d5-terminal-root-universality-suffices-hostile-audit.md`.
They show that a minimum counterexample may be taken simple, cubic,
cyclically \(4\)-edge-connected, and non-3-edge-colourable.  Huck's
reducible-configuration theorem then gives girth at least ten.  No
convention-dependent use of the word “snark” is needed.

Assume the conditional theorem is false and choose such a minimum
cubic counterexample \(G\).  Pick any edge \(e\).  Lemma 3.1 gives the
smaller bridgeless cubic graph \(H=G\div e\).  By minimality, \(H\)
has a \(D_5\)-flow.  By the assumed rooted-universality theorem, its
Kempe orbit contains a state in which the two new edges \(r,s\) lie
on one factor circuit.  Lemma 2.1 then extends that state across the
inverse edge insertion and gives a \(D_5\)-flow on \(G\), a
contradiction.

Finally, the coordinate sets
\[
 C_i=\{e:i\in q(e)\},\qquad i\in[5],
\]
are Eulerian and cover every edge exactly twice.  Empty \(C_i\)'s are
allowed, so this is the standard “at most five” convention.

## 5. Exact remaining gap

Nothing above proves rooted Kempe universality.  For the induction it is
enough to prove the strictly narrower statement:

> If a simple 3-edge-connected cubic graph \(H\) has independent roots
> \(r,s\), girth at least eight, every 8-circuit contains both roots,
> every 9-circuit contains at least one root, and \(H\) has a
> \(D_5\)-flow, then it has some \(D_5\)-flow with \(r,s\) on one
> factor circuit.

The cycle restrictions follow because a circuit of \(H\) using zero,
one, or two roots lifts to a circuit of the girth-ten parent graph that
is longer by zero, one, or two edges.  The exact two-way edge-extension
equivalence and this narrowed frontier are proved in
`scratch/d5-independent-root-feasibility-desargues-frontier.md`.

The terminal surface-\(\chi\) conjecture is a sufficient strengthening
of this assertion.  Complete finite checks through the ranges recorded
in the project support it, while several simpler local, bounded-radius,
single-pair, and matroid-exchange strengthenings have exact
counterexamples.

## References and verification boundary

The edge-reduction criterion used in Lemma 3.1 is stated immediately
before Lemma 2.1 in
G. Brinkmann, J. Goedgebeur, and B. D. McKay, *Generation of cubic
graphs*, Discrete Mathematics and Theoretical Computer Science 13(2)
(2011), 69--80.

The girth reduction for a minimum FiveCDC counterexample is due to
A. Huck, *Reducible configurations for the cycle double cover
conjecture*, Discrete Applied Mathematics 99 (2000), 71--90,
DOI `10.1016/S0166-218X(99)00126-2`.

The fixed-five reductions, Lemmas 2.1 and 3.1, and the induction have
all been written out.  This closes the conditional implication only;
the narrowed rooted premise remains open.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified this implication,
wrote the two local proofs, and drafted this note.  The result is a
conditional reduction, not a proof of FiveCDC and not independent human
peer review.
