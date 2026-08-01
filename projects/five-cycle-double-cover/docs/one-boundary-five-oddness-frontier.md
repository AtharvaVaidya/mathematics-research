# The one-boundary-five oddness frontier

Status: **HUMAN-CHECKABLE CONDITIONAL REDUCTION / EXACT
COUNTEREXAMPLES TO TWO MATCHING LEMMAS / NO FIVE-CDC RESOLUTION**.

This note isolates the remaining one-boundary-five
Gallai--Edmonds branch of the standard Five-Cycle Double Cover
Conjecture.  It proves the exact matching count and a conditional
oddness-four reduction.  It also gives small explicit counterexamples to
the proposed odd-ear shortcut and to its one-odd-circuit weakening.

The counterexamples below are factor-critical and internally
bridgeless.  They are not cyclically four-edge-connected poles.
Consequently they refute the purely factor-critical matching claims,
but they do not refute a possible strengthening which uses the full
minimum-counterexample hypotheses.

## 1. The precise branch

Let \(G\) be a finite simple bridgeless cubic graph and let \(R\) be two
independent root edges with endpoint set \(U\).  Put \(H=G-U\).  In the
one-boundary-five branch of the canonical Gallai--Edmonds decomposition
of \(H\), write

\[
                  W=A\mathbin{\dot\cup}U,\qquad |A|=s.
\]

There is one nontrivial factor-critical \(D\)-component \(Q\) with
\(|\delta_G(Q)|=5\), and there are \(s+1\) singleton \(D\)-components;
call their set \(Z\).  The remaining structural facts are

\[
 |W|=s+4,\qquad |Z|=s+1,
\]

and the only edges with both endpoints in \(W\) are the two roots.
Every edge outside \(Q\) which is not a root joins \(Z\) to \(W\).

These are the hypotheses used below.  No prescribed-root theta claim is
made.

## 2. A factor-critical core has distinct boundary endpoints

**Lemma 2.1.**  A connected factor-critical graph of order greater than
one has no bridge.

**Proof.**  Suppose the bridge \(xy\) separates shores \(X\ni x\) and
\(Y\ni y\).  Their orders have opposite parity.  Suppose without loss
that \(|X|\) is even.  Delete the endpoint \(x\) on the even shore.
There is now no edge from \(X-\{x\}\), of odd order, to \(Y\), also of
odd order.  The resulting graph cannot have a perfect matching,
contrary to factor-criticality. \(\square\)

**Corollary 2.2.**  The five cut edges in \(\delta_G(Q)\) have five
distinct endpoints in \(Q\).

**Proof.**  A vertex incident with at least two cut edges has internal
degree at most one because \(G\) is cubic.  Internal degree zero is
incompatible with connectedness of the nontrivial graph \(Q\), while
an internal degree-one edge would be a bridge of \(Q\), contrary to
Lemma 2.1. \(\square\)

Thus \(Q\), considered as a five-pole, has exactly five degree-two
vertices and all its other vertices have degree three.

**Lemma 2.3 (the exact inherited local cut condition).**  For every
proper nonempty \(X\subset V(Q)\) for which \(Q[X]\) contains a circuit,
\[
              3|X|-2|E(Q[X])|=|\delta_G(X)|\ge4.       \tag{2.1}
\]

**Proof.**  Put \(O=G-Q\).  In the one-boundary-five profile,
\[
 |V(O)|=|W|+|Z|=2s+5,\qquad
 |E(O)|=\frac{3|V(O)|-5}{2}=3s+5.
\]
If every component of \(O\) were a forest, then, writing \(c\ge1\) for
its number of components,
\[
                  3s+5=|E(O)|\le |V(O)|-c=2s+5-c,
\]
which would give \(s+c\le0\), impossible.  Hence \(O\), and therefore
\(G-X\), contains a circuit.  If the displayed cut had size at most
three, it would be a cycle-separating cut of size at most three in
\(G\), contrary to cyclic four-edge-connectivity.  The degree-sum
identity gives the equality in (2.1). \(\square\)

## 3. Exact perfect-matching count at the five-cut

Choose either root \(t\).  Schönberger's edge-prescribed strengthening
of Petersen's theorem gives a perfect matching \(M\) of \(G\) containing
\(t\).  Let

* \(r\) be the number of the two roots which belong to \(M\); and
* \(k=|M\cap\delta_G(Q)|\).

Every singleton in \(Z\) must use a distinct matching edge to \(W\), so
these edges cover \(s+1\) vertices of \(W\).  The \(k\) matching edges
from \(Q\) cover \(k\) more, and the \(r\) roots cover \(2r\).  Since
every vertex of \(W\) is covered exactly once,

\[
                    (s+1)+k+2r=s+4,
 \qquad\text{hence}\qquad k+2r=3.                 \tag{3.1}
\]

The prescribed root gives \(r\ge1\).  Equation (3.1) therefore forces

\[
                              r=1,\qquad k=1.      \tag{3.2}
\]

Let \(q\) be the endpoint in \(Q\) of the unique cut edge in \(M\).
Then \(M\cap E(Q)\) is a perfect matching of \(Q-q\).  Conversely, it
may be replaced by **any** perfect matching \(N\) of \(Q-q\), without
altering the matching outside \(Q\).

### 3.1 At least two boundary terminals can be attained

The preceding prescribed-edge argument supplies one terminal at a time.
The perfect-matching polytope gives a stronger conclusion which is useful
below.

**Lemma 3.1 (two attainable terminals).**  In the one-boundary-five
branch, there are at least two distinct cut edges \(e_1,e_2\in
\delta_G(Q)\) with the following property: for each \(e_j\), some perfect
matching of \(G\) contains \(e_j\) and exactly one root.  Equivalently, at
least two distinct boundary vertices \(q\) of \(Q\) can occur as the
unique endpoint selected in (3.2).

**Proof.**  The constant vector \(x_e=1/3\) belongs to the perfect-matching
polytope of the bridgeless cubic graph \(G\).  Indeed,
\(x(\delta(v))=1\) at every vertex.  If \(|S|\) is odd, then
\(|\delta(S)|\) is odd; it cannot be one because \(G\) is bridgeless, so
\(x(\delta(S))=|\delta(S)|/3\ge1\).  Edmonds' perfect-matching-polytope
theorem therefore writes \(x\) as a convex combination of incidence
vectors of perfect matchings (J. Edmonds, *J. Res. Nat. Bur. Standards
Sect. B* 69B (1965), 125--130, DOI `10.6028/jres.069B.013`).

Choose a perfect matching at random according to this convex
combination.  Equation (3.1) applies to every outcome.  Its only
possibilities are
\[
              (k,r)=(3,0)\quad\hbox{or}\quad(k,r)=(1,1).
\]
The expected number of selected roots is \(2/3\), because each of the
two root edges has marginal \(1/3\).  Hence the total convex weight of
the outcomes of type \((1,1)\) is exactly \(2/3\).

Every particular cut edge also has total marginal \(1/3\).  If all the
type-\((1,1)\) outcomes used the same cut edge, that edge would have
marginal at least \(2/3\), a contradiction.  Thus at least two distinct
cut edges occur.  Corollary 2.2 says that their endpoints in \(Q\) are
distinct. \(\square\)

## 4. The exact conditional oddness-four reduction

For a perfect matching \(N\) of \(Q-q\), let \(c_{\rm odd}(N)\) be the
number of odd circuit components of \(Q-N\).

The vertex \(q\) has degree two in \(Q-N\).  The other four boundary
vertices have degree one, and every remaining vertex has degree two.
Consequently \(Q-N\) consists of exactly two path components together
with some circuit components.

**Theorem 4.1 (conditional closure).**  If, for the endpoint \(q\)
obtained in (3.2), there is a perfect matching \(N\) of \(Q-q\) with
\[
                           c_{\rm odd}(N)\le2,      \tag{4.1}
\]
then \(\omega(G)\le4\).  Hence \(G\) has a standard five-cycle double
cover by Huck's small-oddness theorem.

**Proof.**  Replace \(M\cap E(Q)\) by \(N\), retaining the name \(M\),
and put \(L=G-M\).  Four cut edges belong to \(L\).  On each side of
the cut, the four corresponding semiedges are paired by two path
components.  This statement includes a zero-internal-edge path when
two outside semiedges meet the same vertex.  Gluing the two pairings
creates at most two cut-crossing circuit components of \(L\).

Every circuit of \(L\) wholly outside \(Q\) uses only \(Z\)--\(W\)
edges and possibly a root.  Exactly one root is unused by \(M\).
Thus every outside circuit which avoids that root is bipartite and
even, and at most one outside-only circuit can be odd.

Apart from the internal circuit components of \(Q-N\), the 2-factor
\(L\) therefore has at most three odd circuits: at most two crossing
the cut and at most one wholly outside.  Under (4.1), \(L\) has at
most five odd circuits.  A cubic graph has even order, and the parity
of the number of odd components of a 2-factor equals the parity of its
total order.  Thus \(L\) actually has at most four odd circuits.  This
proves \(\omega(G)\le4\). \(\square\)

If \(Q-N\) is a forest, the same argument gives at most three odd
circuits, and parity of the order of \(G\) improves this to at most two.
The next two sections show that neither forestness nor (4.1) follows
from factor-criticality alone.

Combining Lemma 3.1 with Theorem 4.1 gives a sharper exact target.

**Corollary 4.2 (at-most-one-bad-terminal closure).**  Call a boundary
vertex \(q\) of \(Q\) *bad* when every perfect matching \(N\) of \(Q-q\)
has \(c_{\rm odd}(N)\ge3\).  If \(Q\) has at most one bad boundary
vertex, then \(G\) has a standard five-cycle double cover.

**Proof.**  Lemma 3.1 supplies two distinct attainable boundary
vertices, so at least one is not bad.  Use a type-\((1,1)\) perfect
matching attaining that vertex, replace its restriction to \(Q-q\) by
a witnessing \(N\), and apply Theorem 4.1. \(\square\)

## 5. Why the proposed odd-ear proof fails

An odd-ear decomposition may contain length-one ears, namely edges
whose two endpoints are already present.  Equivalently, one may first
construct a spanning factor-critical subgraph by nontrivial odd ears
and then add the remaining edges as length-one ears.  The usual
near-perfect matching construction matches consecutive pairs of new
internal vertices on each nontrivial ear.  Every unmatched edge of such
an ear has a new endpoint, but a length-one ear has no new endpoint and
can close a circuit in the complement.  The assertion that *every*
unmatched ear edge has a new endpoint is therefore false.

This is not merely a technical defect in the proof.

**Counterexample 5.1.**  Let \(Q_9\) have graph6 encoding

```text
H?b@bQS
```

and edge set

\[
\begin{split}
 \{&04,05,08,15,17,26,27,36,38,47,58\}.
\end{split}
\]

Its degree-two vertices are \(1,2,3,4,6\); the other four vertices have
degree three.  It is connected, internally bridgeless, and
factor-critical.  For reference, one matching of \(Q_9-v\) for every
\(v\) is:

\[
\begin{array}{c|l}
v&\text{matching}\\ \hline
0&15,26,38,47\\
1&04,27,36,58\\
2&04,17,36,58\\
3&04,17,26,58\\
4&05,17,26,38\\
5&04,17,26,38\\
6&04,15,27,38\\
7&04,15,26,38\\
8&04,15,27,36
\end{array}
\]

When the boundary vertex \(q=6\) is exposed, the perfect matching of
\(Q_9-q\) is unique:

\[
                         N=\{04,15,27,38\}.
\]

Its complement consists of

\[
             0\,5\,8\,0,\qquad 1\,7\,4,\qquad 2\,6\,3.
\]

Thus \(Q_9-N\) contains a triangle and is not a forest.

The cyclic-four hypothesis is genuinely absent: the triangle
\(\{0,5,8\}\) has three incident edges in the completed pole.

## 6. One odd circuit is too strong; two are sharp

**Counterexample 6.1.**  Let \(Q_{15}\) have graph6 encoding

```text
N??CA?oI?gX?AoP_Og?
```

and edge set

\[
\begin{split}
\{&06,0\,11,0\,14,17,1\,11,1\,13,28,29,38,3\,10,49,4\,11,4\,12,\\
  &5\,10,5\,13,5\,14,6\,12,6\,13,7\,12,7\,14\}.
\end{split}
\]

The degree-two vertices are \(2,3,8,9,10\).  The graph is connected,
internally bridgeless, and factor-critical.  Expose \(q=2\).  There are
exactly two perfect matchings of \(Q_{15}-2\):

\[
\begin{split}
N_1={}&\{0\,11,1\,13,38,49,5\,10,6\,12,7\,14\},\\
N_2={}&\{0\,14,1\,11,38,49,5\,10,6\,13,7\,12\}.
\end{split}
\]

For \(N_1\), the complement components are the two 5-circuits

\[
       0\,6\,13\,5\,14\,0,\qquad1\,7\,12\,4\,11\,1
\]

and paths on vertex sets \(\{2,8,9\}\) and \(\{3,10\}\).  For \(N_2\),
the two 5-circuits are

\[
       0\,6\,12\,4\,11\,0,\qquad1\,7\,14\,5\,13\,1,
\]

with the same two path vertex sets.  Hence every near-perfect matching
exposing \(2\) has

\[
                          c_{\rm odd}(N)=2.          \tag{6.1}
\]

Again this pole is outside the cyclic-four domain.  For example, the
ten-vertex shore

\[
                 \{0,1,4,5,6,7,11,12,13,14\}
\]

contains circuits and has an internal two-edge boundary.

There is also an all-terminal counterexample to the assertion that
*some* boundary vertex must satisfy (4.1).  Start with the retained
40-vertex graph

```text
artifacts/structured/graphs/lukotka_R2_oddness6.json
```

and delete the induced path \(8-6-9\).  The resulting 37-vertex core is
connected, internally bridgeless, factor-critical, and has boundary
vertices \(1,3,4,5,7\) in the source numbering.  Exact enumeration gives

\[
\begin{array}{c|ccccc}
q&1&3&4&5&7\\ \hline
\#\text{ near-perfect matchings}&64&32&32&32&32\\
c_{\rm odd}(N)\text{ for every }N&4&4&4&4&4.
\end{array}
\]

The order-15 terminals with value two satisfy the corrected sufficient
bound (4.1) sharply.  The R2 core, whose minimum is four at every
terminal, really does refute (4.1) under factor-criticality alone.

For the four endpoint-neighbour terminals \(3,4,5,7\), the lower bound
also has a short conceptual check.  A near-perfect matching of the core
extends over the deleted path to a perfect matching of the source
graph.  At most two new 2-factor circuits use the deleted path.  Since
the source graph has exact oddness six, at least four odd circuits must
already be internal to the core.  The checker enumerates all 192 source
perfect matchings and finds six odd complementary circuits for every
one; it separately handles the middle-neighbour terminal \(1\).

This 37-vertex core still has inherited cyclic two-edge cuts; for
example the ten-vertex block \(\{20,\ldots,29\}\) attaches by two edges.
It therefore does not settle the cyclic-four strengthening.

## 7. Exact checker and bounded census

The standard-library checker

```text
scratch/audit_factor_critical_ear_forest.py
```

independently verifies both explicit small counterexamples:

```sh
python3 scratch/audit_factor_critical_ear_forest.py --self-check
```

It also verifies the all-terminal path-deletion example and replays the
source graph's exact oddness:

```sh
python3 scratch/audit_factor_critical_ear_forest.py \
  --r2-json artifacts/structured/graphs/lukotka_R2_oddness6.json
```

For an exact simple-graph census, pipe graph6 records into the same
program.  For example:

```sh
for n in 5 7 9 11 13 15; do
  m=$(((3*n-5)/2))
  geng -cq -d2 -D3 "$n" "$m:$m" |
    python3 scratch/audit_factor_critical_ear_forest.py
done
```

The complete census of connected simple graphs with the stated degree
profile gives:

\[
\begin{array}{c|r|r|r|r}
|Q|&\text{degree profile}&\text{factor-critical}&
\text{forest failures}&c_{\rm odd}\le1\text{ failures}\\ \hline
5&1&1&0&0\\
7&6&3&0&0\\
9&52&26&3&0\\
11&536&290&41&0\\
13&6\,374&3\,866&530&0\\
15&86\,577&58\,578&7\,168&1
\end{array}
\]

These census rows are finite evidence only.  The explicit graph6
counterexamples and their direct matching enumerations carry the
logical conclusions.

An independent C++ implementation,

```text
scratch/factor-critical-five-pole-oddness-census.cpp
```

tests the stricter one-odd-circuit diagnostic directly.
For every graph where that diagnostic fails it also enumerates every proper
vertex subset \(X\) and computes
\[
                  3|X|-2|E(Q[X])|,
\]
the size of the corresponding cut after the five semiedges are attached.
It calls the pole locally cyclic-four admissible exactly when no
circuit-containing \(X\) has value at most three.

Through order 17 the exact result is:

\[
\begin{array}{c|r|r|r|r|r}
|Q|&\text{degree profile}&\text{factor-critical}&
\text{graphs with a terminal of minimum \(>1\)}&
\text{locally cyclic-four among them}&
\text{with at least two such terminals locally}\\ \hline
5&1&1&0&0&0\\
7&6&3&0&0&0\\
9&52&26&0&0&0\\
11&536&290&0&0&0\\
13&6\,374&3\,866&0&0&0\\
15&86\,577&58\,578&1&0&0\\
17&1\,318\,496&976\,228&21&1&0
\end{array}
\]

The unique locally cyclic-four pole with a terminal of minimum greater
than one at order 17 has graph6
encoding

```text
P???C@?K@OA__aq?@o?J??h?
```

and terminals \(1,2,3,7,9\).  Terminal \(9\) is sharp for (4.1): every
matching of \(Q-9\) leaves two odd internal circuits.  For each of the other four
terminals, an independently enumerated matching leaves no odd internal
circuit.  A separately written Python subset audit finds that the
minimum completed cut of a circuit-containing vertex set is four.
Thus cyclic-four connectivity does **not** force the stronger bound one.
Under the corrected threshold two, every terminal in the complete census
through order 17 is good.

The retained order-17 aggregate is
`scratch/factor-critical-five-pole-oddness-order17.json`.  It records
1,318,496 input graphs, 976,228 factor-critical poles, 34 instances in
21 poles where the minimum exceeds one, one locally cyclic-four pole
with such a terminal, and no locally cyclic-four pole with two such
terminals.  This is bounded evidence only.

## 8. Exact remaining target

The factor-critical odd-ear route is closed in its unrestricted form.
Lemma 3.1 and Corollary 4.2 reduce the still viable oddness route to the
following local statement:

> A factor-critical cubic five-pole which occurs as the five-boundary
> shore in the cyclically four-edge-connected one-boundary-five profile
> has at most one bad boundary vertex.

The type-\((1,1)\) convex-support argument is global, so the local
statement need not force every terminal to be good.  Neither the examples
nor the census here proves the at-most-one statement.  The order-17 pole
above shows that the threshold two in Theorem 4.1 cannot be lowered even
in the exact local connectivity domain.  A five-cut
minimality reduction or an exact \(D_5\) boundary-signature theorem also
remains open.

## 9. AI-use disclosure

The conditional reduction, counterexample search, checker, and
exposition were developed with substantial assistance from OpenAI Codex
under human direction.  The universal statements proved here are
written out in full.  The finite claims have deterministic replay code,
and the two smallest logical counterexamples have complete matching
lists.  No result in this note is represented as a proof or disproof of
the Five-Cycle Double Cover Conjecture.
