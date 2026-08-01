# Exact finite-state cut signatures for external cap coverage

Date: **2026-08-01**

Status: **HUMAN-CHECKABLE COMPOSITION THEOREM AND FINITE REPLAY / NOT A
UNIVERSAL EXTERNAL-COVERAGE THEOREM / NOT A PROOF OF FIVECDC**.

## 1. Setting

Identify a `D5` label with a two-subset of `[5]`, or with its weight-two
incidence vector in `F_2^5`.  A partial `D5` flow on a cubic multipole labels
every ordinary edge and semiedge by a member of `D5` and has xor zero at each
internal vertex.

For a coordinate pair `P`, put

\[
        Y_P(q)=\{e:|q(e)\cap P|=1\}.
\]

At every internal vertex this set has degree zero or two.  Its components in
a multipole are therefore circuits and paths between active semiedges.

Let a 2- or 3-edge cut separate a proper root edge `r` from a cap vertex `z`.
Assume that the cut is disjoint from the three cap edges.  Cutting its members
produces a root pole `R` and a cap pole `Z`, with corresponding ordered
semiedges.

## 2. Boundary normal forms

Xor all vertex equations on one shore.  Every ordinary shore edge occurs
twice and cancels, leaving

\[
                  q(c_1)\mathbin\triangle\cdots
                  \mathbin\triangle q(c_k)=\varnothing.       \tag{1}
\]

For `k=2`, (1) says that the two labels are equal.  A global coordinate
permutation normalizes the ordered word to

\[
                              (01,01).                          \tag{2}
\]

For `k=3`, three weight-two vectors with xor zero are the three distinct
edges of a triangle in `K_5`.  A global coordinate permutation normalizes
the ordered word to

\[
                              (01,02,12).                       \tag{3}
\]

There are exactly ten words before normalization in (2), and exactly
`C(5,3) 3! = 60` ordered words before normalization in (3).

Fix either normalized word.  For every factor `P`, zero or two boundary
semiedges are active.  If two are active, they are joined by one unique
`Y_P` path: the active subgraph has degree zero or two internally, and its
only two degree-one ends are those semiedges.

## 3. The two finite shore states

For one partial flow `q_R` on the root pole, define

\[
 \rho(q_R)=\{P\in D_5:\text{the unique boundary `Y_P` path contains `r`}\}.
                                                               \tag{4}
\]

For one partial flow `q_Z` on the cap pole and physical cap pair
`j in {ab,ac,bc}`, define

\[
 \epsilon_j(q_Z)=\{P\in D_5:\text{the boundary `Y_P` path contains `z`,
 uses physical pair `j`, and is external at `z`}\}.             \tag{5}
\]

“External” in (5) means that the inactive cap-edge label is disjoint from
`P`; the local triangle law says that the only alternative is equality with
`P`, the internal mode.

The boundary-active factors are exactly the six pairs crossing `01` in the
2-pole normal form.  They are the nine pairs other than `34` in the 3-pole
normal form.  Consequently a literal root state needs at most 6 or 9 bits.
A literal cap state is a triple of such bitsets.  Crude exact finite upper
bounds are therefore

\[
  2^6\ \hbox{and}\ 4^6
  \quad\hbox{for a 2-cut},\qquad
  2^9\ \hbox{and}\ 4^9
  \quad\hbox{for a 3-cut}.                                  \tag{6}
\]

The `4^k` bound assigns each boundary-active factor to no external physical
pair or to one of the three pairs.  Realizable cap states form a much smaller
subset.

For a whole pole, retain the **relations**

\[
 \mathcal R=\{\rho(q_R):q_R\text{ is a partial flow with fixed boundary}\},
\quad
 \mathcal E=\{(\epsilon_{ab},\epsilon_{ac},\epsilon_{bc})(q_Z):q_Z
              \text{ is such a partial flow}\}.              \tag{7}
\]

It is essential to retain the sets in (7), rather than unioning factors
over unrelated flows.  The latter would commit exactly the forbidden
quantifier error behind several false orbitwise strengthenings.

## 4. Exact natural-join theorem

> **Theorem 4.1 (separated-marker cut composition).**  Partial flows on the
> two shores with the same ordered boundary word glue bijectively to whole
> `D5` flows having that word on the cut.  For a glued pair `(q_R,q_Z)`, its
> external physical-pair mask is exactly
>
> \[
>   \{j:\rho(q_R)\cap\epsilon_j(q_Z)\ne\varnothing\}.          \tag{8}
> \]
>
> In particular, one whole flow simultaneously externally covers all three
> physical ports exactly when some pair of states in
> `mathcal R x mathcal E` makes at least two of the three intersections in
> (8) nonempty.

**Proof.**  Matching boundary labels makes the two copies of every cut edge
one labelled edge.  All internal vertex equations are already satisfied, so
gluing is a whole flow.  Restriction of a whole flow gives the inverse map.

Fix `P`.  If the whole `Y_P` circuit through `r` crosses the cut, its
restriction to the root shore is the unique boundary path, so
`P in rho(q_R)`.  It reaches `z` in external physical mode `j` exactly when
its restriction to the cap shore is the unique boundary path specified in
(5), so `P in epsilon_j(q_Z)`.  Gluing the two paths gives the converse.
This proves (8).  Two distinct edges of the three-port triangle cover all
three ports, proving the final assertion. `square`

Thus the all-flow simultaneous target across a separated 2- or 3-cut is an
exact finite relational join, not a heuristic connectivity summary.  This
is the requested code/homomorphism formulation for these cuts.

For existence only, inclusion-dominated states may be deleted.  If
`rho subset rho'`, then `rho'` succeeds against every cap state against which
`rho` succeeds.  The same holds componentwise for cap triples.  Retaining
only inclusion-maximal states therefore preserves whether the maximum mask
in (8) has at least two bits.  This is an exact antichain compression.

## 5. Constant circuit translations in the state graph

Let `C` be a circuit and add the same nonzero even vector `h` to every label
on `C`.  Vertex xor is preserved because each circuit vertex changes twice.
There are two nontrivial legality cases:

1. if `|h|=2`, every old label on `C` must cross `h`; this is the ordinary
   component/Kempe translation;
2. if `|h|=4`, write `h=[5] - {s}`; every old label on `C` must avoid `s`.

Both assertions follow immediately from

\[
                   |A\mathbin\triangle h|
                   =2+|h|-2|A\cap h|.                          \tag{9}
\]

Whenever the translation is legal, factor membership obeys the exact law

\[
  1_{Y_P(q+h1_C)}(e)=1_{Y_P(q)}(e)+|h\cap P|\pmod2
  \quad(e\in C).                                             \tag{10}
\]

For a weight-four shift missing `s`, (10) toggles precisely the four factors
`P` containing `s`.  These complement switches can cross ordinary Kempe
orbits.  If `C` is internal to one shore, they preserve the normalized
boundary word and give explicit edges of the finite shore-state transition
graph.  The natural-join theorem needs no orbit assumption and already
contains both endpoints.

No connectivity theorem for this enlarged transition graph is asserted.
Small graphs have multiple enlarged orbits, so “all flows lie in one such
orbit” is false.

## 6. Literal independent replay

`verify.py` exhausts all local algebra above and two complete graph examples:

- graph6 `GCXmd_`, cut edges `(7,10)`, cap `z=0`, root edge `5`, normalized
  2-cut word `(01,01)`;
- graph6 `GCZJd_`, cut edges `(2,3,6)`, cap `z=3`, root edge `1`, normalized
  3-cut word `(01,02,12)`.

For each example it independently enumerates every partial shore flow and
every direct whole flow with the normalized boundary.  It checks equality
between the Cartesian glued words and the direct words, then compares (8)
with a fresh whole-graph factor-component traversal for every glued flow.
It also verifies that antichain compression preserves the best achievable
number of external physical pairs.

The 2-cut has `18*18=324` normalized flows.  The 3-cut has `3*9=27`.
Every word and every external mask is checked literally; no SAT solver or
unchecked negative answer is used.

The checker also freezes two cross-Kempe-orbit complement translations from
the published orbit delimiters:

- on order-12 graph6 ``K?`@EQgLAcAo``, the triangle of edge indices
  `(0,3,5)` avoids coordinate `4`; adding `0123` changes typed/external data
  from `(32,4)` to `(10,3)`, hence reaches a simultaneous flow;
- on order-14 graph6 `M??CBAPqB_B_H_B_?`, the 5-circuit
  `(0,6,8,18,20)` avoids coordinate `3`; adding `0124` changes
  typed/external data from `(19,1)` to `(51,5)`.  This circuit avoids both
  the root and all three cap edges, so it is a particularly clean internal
  state transition.

These literal transitions explain why the orbitwise failures do not survive
the larger legal-translation graph.  They do not prove that every failure
has such an exit.

## 7. Bounded realizable-relation census

`search_through10.py` uses `geng -Cq -d3 -D3` to generate the complete
biconnected simple cubic census at orders 8 and 10: 5 plus 18 host graphs.
It takes both connected shores of every nontrivial 2- and 3-edge cut, every
proper root edge, every cap vertex not incident with the cut, and all six
orders of the normalized 3-cut triangle.  It then deduplicates the exact
relations (7) and crosses every root relation with every cap relation of the
same cut size, even when the two poles came from different hosts.

The exact result is:

|cut|root relations|cap relations|cross-pairs best 2|cross-pairs best 3|bad|
|---:|---:|---:|---:|---:|---:|
|2|7|9|14|49|0|
|3|108|222|2,040|21,936|0|

Thus no realizable bad pair occurs in this bounded pole source.  Every one
of the 24,039 cross-pairs has a joined flow with at least two external
physical pairs.  This is a development census, not an induction base for
arbitrary poles: larger poles can realize new relations.

## 8. Complete abstract local-axiom frontier

There is a sharp distinction between **local admissibility** and a relation
realized by a whole pole.  Fix the normalized boundary word and let `H` be
its residual coordinate stabilizer.  It has order 12 for `(01,01)` and order
2 for the ordered triangle `(01,02,12)`.

At the purely local level, a root state may be any subset of the factors
which are active on both some root label and the boundary.  A cap state may
be any subchoice of the locally eligible external factors for some ordered
cap triangle.  A locally admissible abstract relation is any nonempty union
of `H`-orbits of these states.  `abstract_relations.py` exhausts these
definitions literally and obtains:

|cut|root states|root orbits|abstract root relations|cap states|cap orbits|abstract cap relations|
|---:|---:|---:|---:|---:|---:|---:|
|2|64|13|`2^13-1`|478|51|`2^51-1`|
|3|238|138|`2^138-1`|1,774|922|`2^922-1`|

Build a bipartite graph whose vertices are root-state orbits and cap-state
orbits, with an edge when every cross-pair is unsafe.  An arbitrary pair of
abstract invariant relations is unsafe **if and only if** its selected orbit
sets form a nonempty biclique in this graph.  This gives a compact complete
enumeration of all the exponentially many relation pairs.  The graph has

|cut|unsafe orbit edges|good orbit edges|
|---:|---:|---:|
|2|281|382|
|3|74,985|52,251|

The checker hashes the complete canonical orbit lists and unsafe edge lists,
not only these counts.

The empty root/cap states give vacuous unsafe pairs.  Exclude those by
requiring every root state to be nonempty and every cap state to offer at
least two physical pairs.  Lexicographically minimize maximum root support,
maximum total cap support, orbit product, and orbit sum.  The smallest
remaining forbidden patterns are:

1. For a 2-cut, the root relation is the residual-stabilizer orbit
   \[
      \{\{02\},\{03\},\{04\},\{12\},\{13\},\{14\}\}.
   \]
   The cap relation is
   \[
   \begin{split}
   \{&(\varnothing,\{02\},\{12\}),
       (\varnothing,\{03\},\{13\}),
       (\varnothing,\{04\},\{14\}),\\
     &(\varnothing,\{12\},\{02\}),
       (\varnothing,\{13\},\{03\}),
       (\varnothing,\{14\},\{04\})\}.
   \end{split}                                             \tag{11}
   \]
   Among the 36 state pairs, 24 join with no external physical pair, six
   with only `ac`, and six with only `bc`.
2. For a 3-cut, both orbits are singletons:
   \[
          \mathcal R=\{\{01\}\},\qquad
          \mathcal E=\{(\varnothing,\{01\},\{02\})\}.       \tag{12}
   \]
   Their join has only physical pair `ac`.

These states obey every stated boundary-parity, root-label, cap-triangle,
external-mode, and residual-symmetry rule.  For example, cap triangles
`(03,13,01)` and `(13,23,12)` locally support representatives of (11) and
(12), respectively.  Therefore the abstract natural-join algebra is closed
around an unsafe pair: a finite-state induction from only these local axioms
is false.

The bounded connected-shore census tests the precise repair obligation.  It
finds no pole whose **complete** relation equals any relation in (11) or
(12).  The 2-cut bad root orbit occurs inside eight complete root relations,
but the bad cap orbit occurs inside none.  For 3-cuts the two bad orbits occur
inside 64 root and five cap relations, respectively, yet companion states
make every cross-pair of complete relations good.  This is finite evidence
for, but not a proof of, the missing theorem:

> A connected bridgeless realizable shore containing a forbidden local state
> must also contain a compatible companion state.

Any successful finite-state induction must prove such a realizability or
switch-closure axiom.  Parity and `S5` invariance alone cannot do it.

## 9. Consequence and exact remaining gap

The global reentry obstruction is now localized precisely: for a separated
small cut, it is not additional graph connectivity hidden during gluing; it
is the possible absence of a compatible pair in the two finite relations
(7).  A recursive proof may compute these relations bottom-up.  A recursive
counterexample search may seek a realizable bad pair of relations.  Either
route must impose realizability; arbitrary bitsets satisfying only the crude
bounds (6) contain immediate abstract bad pairs.

The theorem does not handle a cut with `r` and `z` on the same shore without
enlarging the boundary state, does not prove that every relevant cap has a
good join, and does not resolve FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the finite-state join,
the antichain compression, and the constant-translation integration, and
wrote the literal replay.  The mathematical proof is displayed in full and
can be checked independently of the program.  No novelty, peer review,
universal theorem, or FiveCDC resolution is claimed.
