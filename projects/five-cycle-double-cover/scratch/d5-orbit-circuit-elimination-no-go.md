# Orbit circuits do not form a matroid circuit family

Date: **2026-07-28**

Status: **EXACT PROOF-STRATEGY NO-GO / NOT A FIVECDC
COUNTEREXAMPLE**.

## 1. The proposed axiom

Fix a Kempe orbit \(\mathcal O\) of \(D_5\)-flows.  Let
\(\mathcal C(\mathcal O)\) consist of every circuit component of every
factor
\[
                         Y_{ij}=C_i\mathbin\triangle C_j
\]
which appears in a state of the orbit.

A natural route to rooted transitivity is to prove the matroid circuit
elimination axiom:
\[
 A,B\in\mathcal C(\mathcal O),\ f\in A\cap B
 \quad\Longrightarrow\quad
 \exists D\in\mathcal C(\mathcal O):
 D\subseteq(A\cup B)-f.                                      \tag{1}
\]
Then the usual connected-component relation of a matroid would make
“two edges occur on a common orbit circuit” transitive.

The Petersen graph refutes (1).

## 2. The four local factor-pair types

Let a shared graph edge have \(D_5\)-label \(L\).  A factor pair active
on that edge chooses one coordinate of \(L\) and one coordinate outside
\(L\).  Thus the six active factor pairs are the six edges of
\(K_{2,3}\).  Up to the stabilizer \(S_2\times S_3\) of \(L\), an
ordered pair \(P,Q\) of active factors has four local types:

1. \(P=Q\);
2. \(P,Q\) share their coordinate in \(L\);
3. \(P,Q\) share their coordinate outside \(L\);
4. \(P,Q\) are disjoint.

The first type is harmless: intersecting components of the same factor
are equal.  In types 2 and 3, \(|P\cap Q|=1\).  Switching on a
\(Y_Q\)-component \(B\) changes
\[
                         Y_P\longmapsto Y_P\triangle B.          \tag{2}
\]
Consequently the components of \(A\triangle B\) are orbit circuits and
give the ordinary elimination conclusion for distinct intersecting
circuits \(A,B\).

In type 4, the transpositions on \(P\) and \(Q\) commute and a
\(Q\)-switch does not change \(Y_P\).  The following example shows that
this is a genuine obstruction to (1), not merely a missing proof.

## 3. A literal Petersen witness

Use the Petersen graph with ordered edges
\[
\begin{array}{c|rrrrrrrrrrrrrrr}
e&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\ \hline
uv&01&04&05&12&16&23&27&34&38&49&57&58&68&69&79.
\end{array}
\]
Give these edges the \(D_5\)-labels
\[
\begin{array}{c|rrrrrrrrrrrrrrr}
e&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\ \hline
q(e)&01&02&12&12&02&23&13&24&34&04&14&24&23&03&34.
\end{array}                                                     \tag{3}
\]
Here, for example, the hexadecimal mask `0c` in the checker denotes
the label \(23\).  At each vertex the three incident labels are the
three sides of a coordinate triangle, so (3) is a \(D_5\)-flow by a
ten-vertex local check.

In this state, the \((0,3)\)-factor is the 9-circuit
\[
 A=\{0,1,4,5,6,8,9,12,14\},
\]
and one component of the \((2,4)\)-factor is the 5-circuit
\[
 B=\{3,4,5,8,12\}.
\]
The factor pairs \(\{0,3\}\) and \(\{2,4\}\) are disjoint.  They share
the four-edge path
\[
                    \{4,12,8,5\}=16,68,38,23.
\]
Eliminate \(f=4\).  The only graph-theoretic circuit contained in
\((A\cup B)-f\) is
\[
                   A\triangle B=\{0,1,3,6,9,14\},               \tag{4}
\]
the 6-circuit \(0,1,2,7,9,4,0\).

An exact traversal of the full Kempe orbit, quotienting only by global
\(S_5\), has 25 states and 47 distinct nonempty factor-circuit edge sets.
None is contained in \((A\cup B)-f\); in particular (4) never occurs.
As a direct control, the checker also traverses all 3,000 labeled states
without any \(S_5\) quotient and obtains exactly the same 47 circuit
edge sets.
Thus (1) is false.

## 4. Exact scope

This witness does **not** refute orbit-rooted transitivity.  In fact,
for every \(a\in A\) and \(b\in B\), some factor circuit in the initial
state (3) already contains \(a,b\).  Those mediator circuits leave
\(A\cup B\), exactly the behavior forbidden by the matroid containment
axiom.

Therefore any successful circuit-family proof must use a genuinely
non-matroid elimination rule which permits mediator circuits outside
the two original circuits.  The two intersecting local types are
controlled by (2); the disjoint type is the unresolved structural case.

## 5. Reproduction

Run

```text
python3 scratch/audit_d5_orbit_circuit_elimination_no_go.py \
  --output scratch/d5-orbit-circuit-elimination-no-go.json
```

The standalone checker validates every local xor equation, generates
all component switches, canonicalizes only by the 120 global coordinate
permutations, checks the 25-state orbit, enumerates all 47 nonempty circuit
masks, repeats the traversal on all 3,000 unquotiented states, and
independently enumerates every graph circuit in the allowed edge set.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and exhaustively
checked this finite no-go, classified the four local factor-pair types,
and drafted this note.  The displayed witness and complete checker are
provided for human inspection.  This is not peer review and is not
presented as a resolution of FiveCDC.
