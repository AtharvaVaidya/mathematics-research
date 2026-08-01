# Five-pole realizability frontier

Status: **HUMAN LEMMAS / EXACT FINITE EVIDENCE / UNIVERSAL CLAIM OPEN**.

This note records the graph-realizability branch exposed by the complete
five-boundary calculation.  It does not prove the five-cycle double cover
conjecture and it does not exhibit a counterexample.

## 1. Boundary states

Let \(P\) be a connected simple graph with five distinguished, distinct
degree-two vertices and every other vertex of degree three.  Attach one
semiedge at each distinguished vertex.  A \(D_5\)-labeling assigns to every
edge and semiedge a two-element subset of \(\{0,1,2,3,4\}\), with symmetric
difference zero at every completed cubic vertex.

The five semiedge labels form an ordered boundary word

\[
q=(q_1,\ldots,q_5)\in D_5^5,\qquad
q_1\mathbin\triangle\cdots\mathbin\triangle q_5=\varnothing.
\]

There are 6,240 such words and 62 orbits under permutation of the five
colors.  Write \(S(P)\) for the subset of the 62 orbits admitted by \(P\).
If two ordered poles are joined terminal by terminal, their labelings glue
exactly when their boundary states agree.  Thus the joined graph has a
standard five-cycle double cover if and only if the two state sets
intersect.

The preceding statements are direct consequences of the local
\(D_5\)-flow equations.  They are independent of the finite census below.

## 2. Why internal bridges are absent in the reduced domain

The following elementary lemma justifies the bridge-free restriction used
in the minimum-counterexample branch.

**Lemma.**  Let a cycle-separating five-edge cut of a cubic graph \(G\)
have distinct endpoints on a shore \(P\).  If \(G\) has no
cycle-separating edge cut of size at most three, then the core of \(P\)
has no bridge.

**Proof.**  Suppose that an internal edge \(e\) is a bridge of the core.
Choose a component \(X\) of \(P-e\) containing \(k\leq2\) of the five
terminals.  In the original cubic graph,

\[
|\delta_G(X)|=k+1\leq3.
\]

The component \(X\) contains a cycle.  Indeed, if \(n=|V(X)|\) and \(X\)
were a tree, then summing degrees in the original cubic graph would give

\[
3n=2(n-1)+(k+1),
\]

and hence \(n=k-1\), contradicting \(n\geq k\) (and also excluding
\(k=0\)).  The other side of \(\delta_G(X)\) contains the cycle on the
opposite shore of the original five-edge cut.  Therefore
\(\delta_G(X)\) is a cycle-separating cut of size at most three, a
contradiction. \(\square\)

In particular, once the standard minimum-counterexample reduction to
cyclically 4-edge-connected cubic graphs has been made, no internal pole
bridge may be excluded merely as a search heuristic: it is excluded by
this lemma.  Conversely, bridged poles outside that reduced domain can
have much smaller state sets and must not be silently folded into the
bridge-free claim.

## 3. Current finite observation

Two independently written exact constraint solvers agree on every
aggregate through pole order 11.  A larger diagnostic census reaches all
connected, simple, internally bridgeless, terminal-distinct cubic
five-poles of odd orders \(5,7,9,11,13\).  Its current totals are:

- 5,214 canonical poles;
- no pole with fewer than 46 admitted color-orbits;
- 298 poles with exactly 46 orbits; and
- every one of those 298 extremal relations is exactly one of the twelve
  ordered \(C_5\)-cap relations.

The order-by-order number of extremal poles is

\[
1,\ 1,\ 6,\ 34,\ 256.
\]

A threshold-only extension now exhausts the 69,243 internally bridgeless
cores of order 15.  Every record reaches 46 satisfiable orbits before the
classifier stops; hence there is no order-15 counterexample to the lower
bound.  Because that run stops at 46, it does not determine the full
order-15 size profile or the number of genuinely extremal relations.  Its
transcripts, fresh-corpus structural replay, and optional byte-identical
CaDiCaL replay are frozen in
`search/five-pole-46-threshold-order15-20260727/`.

This is finite evidence, not the following universal theorem:

> Every connected internally bridgeless cubic five-pole admits at least
> 46 of the 62 boundary color-orbits.

The evidence is especially suggestive because 46 is sharp: the five-cycle
cap itself has exactly 46 states.  The stronger statement that every pole
*contains* a complete \(C_5\)-cap relation is false; already at small order
there are 56- and 58-state poles containing none of the twelve cap sets.

## 4. The universal lower bound would resolve Five-CDC

The universal 46-state statement is not merely a five-cut reduction.
Already the assertion that every pole in its stated domain has one
boundary state would imply the full conjecture on finite simple bridgeless
cubic graphs.

**Path-extension lemma.**  Let \(G\) be a finite connected simple
bridgeless cubic graph and let \(e=uv\).  Delete \(e\), add a new path

\[
             u z_1z_2z_3z_4z_5 v,
\]

and regard \(z_1,\ldots,z_5\) as five distinct terminals, each with one
semiedge.  Call the resulting five-pole \(P_e\).  Then:

1. the proper core of \(P_e\) is connected, simple, and internally
   bridgeless; and
2. \(P_e\) has a \(D_5\)-labelling if and only if \(G\) has a standard
   five-cycle double cover.

**Proof.**  Every old edge \(f\ne e\) lies on a circuit of \(G\).  If that
circuit uses \(e\), replace \(e\) on it by the new path.  Thus \(f\)
still lies on a circuit of the proper core.  Since \(e\) is not a bridge,
\(G-e\) has a \(u\)--\(v\) path; its union with the new path is a circuit
containing every new path edge.  Hence the core is internally bridgeless.
Connectedness and simplicity are immediate.

Suppose first that \(P_e\) has a \(D_5\)-labelling.  Sum its vertex
equations over the old vertex set \(V(G)\).  Every old proper edge occurs
twice and cancels.  The only surviving labels are those on \(uz_1\) and
\(z_5v\), so those two labels are equal.  Delete the new path and its five
semiedges, restore \(e\), and give \(e\) that common label.  The vertex
equations on \(G\) now hold, giving a standard five-cycle double cover.

Conversely, suppose \(G\) has a \(D_5\)-labelling and normalize the label
of \(e\) to \(01\).  On the six successive edges of the new path use

\[
       01,\quad02,\quad03,\quad01,\quad02,\quad01.
\]

Give the five successive semiedges the xor labels

\[
       12,\quad23,\quad13,\quad12,\quad12.
\]

Every displayed label is a two-subset of \([5]\), and at each \(z_i\) the
two path labels xor to the semiedge label.  The old endpoint equations are
unchanged because the first and last path labels both equal the old label
of \(e\).  A global colour permutation supplies the same construction for
an arbitrary label of \(e\).  This extends the labelling to \(P_e\).
\(\square\)

Consequently,

> Every connected internally bridgeless simple terminal-distinct cubic
> five-pole has a nonempty boundary relation

is already equivalent, after the usual cubic/simple reduction, to the
standard Five-Cycle Double Cover Conjecture.  The proposed 46-of-62 lower
bound is a strict strengthening of this nonemptiness assertion.  Its
finite census must therefore be understood as a re-encoding of bounded
Five-CDC evidence, not as evidence for an auxiliary lemma known to be
strictly easier than the original conjecture.

There remains a useful cut consequence.  If the 46-state lower bound were
proved and a graph were split by a terminal-distinct cycle-separating
five-edge cut into internally bridgeless shores \(P_1,P_2\), then

\[
|S(P_1)\cap S(P_2)|
\geq |S(P_1)|+|S(P_2)|-62
\geq 30.
\]

The corresponding pole labelings would glue and give a standard
five-cycle double cover of the graph.  This cut statement is valid, but it
is weaker than the path-extension consequence above.  A repeated endpoint
in a five-edge cut still requires a separate cut argument; that caveat
does not affect the path-extension reduction, whose five terminals are the
new vertices \(z_1,\ldots,z_5\).

## 5. Present logical gap

Every realizable state relation is closed under bichromatic path switches.
The current audit also enforces one globally coherent pairing of boundary
ends for all ten bichromatic subgraphs and transports those pairings under
same-pair and disjoint-pair switches.  The known abstract 8-state and
10-state disjoint relations still satisfy these stronger conditions.

The missing datum is the internal intersection topology of bichromatic
path systems.  For color pairs sharing one color, the old boundary
pairings do not determine the pairing after a switch.  Thus no sound proof
may infer an overlapping-pair transition from the 62 undecorated boundary
orbits alone.  A successful finite-state proof would need a richer
realizability object, such as a transition-matroid or circuit-partition
signature, together with a proved composition rule.

The same limitation already appears in the four-pole branch.  The two
hypothetical signatures in Máčajová--Mazzuoccolo--Tabarelli Conjecture 3.7
survive the coherent pairing/transport test as abstract decorated
relations: the size-four signature has five compatible decorated schemes,
and the size-five signature has eight.  This does not realize either
signature by a graph, but it proves that the present boundary-only
machinery cannot establish their nonexistence.

## 6. Publication boundary

The two-subset encoding, multipole state sets, gluing criterion, and
bichromatic switching are prior machinery; see Máčajová, Mazzuoccolo, and
Tabarelli, *Ars Mathematica Contemporanea* 26 (2026), #P2.03,
Definition 3.1 and Remark 3.2.  The bridge lemma above is elementary.  The
46-state observation is currently a bounded computation without a
certificate archive at publication standard.

Accordingly, this note supplies no resolution claim.  A proof of the
universal 46-state theorem would itself resolve standard Five-CDC, while a
realizable smaller state relation would only refute that stronger route
unless it participated in a certified incompatible gluing.  The
path-extension lemma is a human-checkable scope correction and exact
reformulation; it is not a proof of the missing nonemptiness assertion.

## 7. AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, developed the
path-extension reformulation, ran the finite census, and drafted and
audited this note.  Agent cross-checks are not independent human
verification or peer review.  The mathematical lemmas are displayed for
line-by-line human checking, while the bounded computation and its trust
boundary are stated separately.
