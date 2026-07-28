# Whole-fibre square expansion: exact finite frontier and a five-label lemma

Date: 2026-07-28

Status: **EXACT SOLVER-FREE CENSUS THROUGH ORDER 14 / HUMAN LOCAL
FIVE-LABEL LEMMA / NO UNIVERSAL PROOF OR COUNTERMODEL / NOT A
RESOLUTION OF FIVE-CDC**.

## 1. The surviving quantifier

Let \(H\) be a simple 3-edge-connected cubic graph, let \(r\) be a
vertex, and let \(AC,BD\) be independent edges not incident with \(r\).
Replace those edges by
\[
 Aa,\ Bb,\ Cc,\ Dd,\ ab,\ bc,\ cd,\ da
\]
to obtain the square expansion \(H^\square\).  A star packing at \(r\)
is an ordered triple of spanning trees in which each root edge occurs
once and every other edge occurs twice.  It is **exact-good** if the
odd-kernel component-parity criterion holds in at least one coordinate.

The statewise assertion is false: a selected exact-good packing need not
have any exact-good square-local lift, even after changing the good
coordinate.  The surviving assertion has different quantifiers:

> **(F)** If the whole star fibre of \((H,r)\) contains an exact-good
> state, then the whole star fibre of \((H^\square,r)\) contains an
> exact-good state.

The finite search below checks the stronger local-selection statement

> **(L)** For every eligible pair \(AC,BD\), some exact-good state
> downstairs has an exact-good square-local lift.

Here the selected downstairs state is allowed to depend on the edge
pair.  Thus (L) implies (F), while the known order-eight statewise
countermodel does not contradict either statement.

## 2. Exact extension criterion for a fixed five-cover

There is a small human lemma at the level of the original five Eulerian
subgraphs.  It explains a real local obstruction, but it does not by
itself prove (F).

Represent an indexed five-cycle double cover by labelling each edge with
the two-element set of cover indices which contain it.  At a vertex,
Eulerian parity is equivalent to the symmetric difference of the
incident labels being empty.

> **Lemma (fixed-cover square extension).**  Hold every label outside
> the square fixed.  Let the deleted edges \(AC\) and \(BD\) have
> two-subset labels \(P\) and \(Q\).  Their five-cover extends across
> the square if and only if
> \[
>                         P=Q\quad\hbox{or}\quad P\cap Q=\varnothing.
>                                                               \tag{1}
> \]

**Proof.**  Parity at the four old terminals forces the labels on
\(Aa,Cc\) to be \(P\), and those on \(Bb,Dd\) to be \(Q\).  Put
\(X=\lambda(ab)\).  Parity at \(a,b,c,d\), in order, forces
\[
\begin{aligned}
 \lambda(ab)&=X,\\
 \lambda(bc)&=X\mathbin\triangle Q,\\
 \lambda(cd)&=X\mathbin\triangle P\mathbin\triangle Q,\\
 \lambda(da)&=X\mathbin\triangle P.                       \tag{2}
\end{aligned}
\]
The fourth vertex equation is then automatic.  Every set in (2) must
have size two.

If \(P=Q\), choose a two-set \(X\) meeting \(P\) in one point.  If
\(P\cap Q=\varnothing\), choose \(X\) with one point in \(P\) and one
in \(Q\).  In either case all four sets in (2) have size two.

It remains to exclude \(|P\cap Q|=1\).  Write
\(P=\{p,q\}\) and \(Q=\{p,s\}\).  For a two-set \(R\),
\(|X\triangle R|=2\) is equivalent to \(|X\cap R|=1\).
Consequently (2) would require \(X\) to meet each of
\[
                  \{p,q\},\qquad\{p,s\},\qquad\{q,s\}
\]
in exactly one point.  If \(x_p,x_q,x_s\) are the corresponding
zero-one indicators, this says
\[
 x_p+x_q=x_p+x_s=x_q+x_s=1.
\]
The first two equations give \(x_q=x_s\), contradicting the third.
This proves (1). \(\square\)

This lemma concerns a **fixed compatible five-labeling**.  A square-local
tree lift can change odd-kernel membership on old outside edges even
though their tree membership is fixed, because the gadget may reconnect
the components left by deleting \(AC,BD\) differently.  Therefore (1)
is a useful sufficient route, not an equivalence with exact-good
tree-local liftability.  A proof of (F) still needs a global choice or
exchange argument.

## 3. Complete canonical censuses

The checker

```sh
python3 scratch/search_jaeger_star_square_existential_census.py --order 10
python3 scratch/search_jaeger_star_square_existential_census.py --order 12
```

contains the complete graph6 streams produced by

```sh
geng -cq -d3 -D3 10
geng -cq -d3 -D3 12
```

and independently filters them by deleting every set of at most two
edges.  It uses only the Python standard library.  For every retained
graph it:

1. enumerates every spanning tree;
2. enumerates the star fibre exactly from two trees and the forced third
   tree;
3. reconstructs every odd kernel from odd subtree sizes;
4. tests the exact component-parity criterion;
5. enumerates all \(2^8\) local masks for each of the three trees and
   joins them by their omitted-edge masks; and
6. accepts an instance only after reconstructing an exact-good lifted
   triple.

Order fourteen is larger, so it is certified differently.  The
witness-producing C++ search

```sh
clang++ -O3 -std=c++20 \
  scratch/search_jaeger_star_square_existential_order14.cpp \
  -o /tmp/search_square_order14
geng -cq -d3 -D3 14 |
  /tmp/search_square_order14 |
  gzip -9 >/tmp/square-order14-witnesses.tsv.gz
python3 scratch/verify_jaeger_star_square_existential_order14.py \
  /tmp/square-order14-witnesses.tsv.gz
```

emits one explicit downstairs/lifted tree certificate for every retained
labelled instance.  It quotients the coordinate \(S_3\) action by requiring
tree \(i\) to contain the \(i\)-th sorted root spoke.  This is sound because
every ordered star packing has exactly one coordinate permutation with that
property, and both exact-goodness and liftability are invariant under
coordinate permutation.  It enumerates the three six-edge omission sets,
prunes immediately unless their complements are trees, and supports
disjoint canonical graph-index shards as exact checkpoints.

The separately written Python checker does not call or import the discovery
program.  It regenerates the canonical graph stream, checks its frozen
SHA-256 digest, independently tests three-edge-connectivity, and requires
exactly one row for every retained graph, every labelled root, and all 120
eligible edge pairs.  From each row it reconstructs and checks all six
spanning trees, every edge multiplicity, the outside-edge agreement, and
both odd-kernel component-parity tests.  Thus the order-fourteen positive
result is a certificate census, not trust in a searcher's failure to find a
counterexample.

The completed totals are:

| downstairs order | connected cubic records | 3-edge-connected | labelled roots | eligible edge pairs | failures |
|---:|---:|---:|---:|---:|---:|
| 10 | 19 | 14 | 140 | 6,300 | 0 |
| 12 | 85 | 57 | 684 | 53,352 | 0 |
| 14 | 509 | 341 | 4,774 | 572,880 | 0 |

At order ten the search made 6,923 good-state/pair lift attempts.  At
order twelve it made 66,696 such attempts.  The latter count is larger
than the number of instances because the first exact-good state does not
always lift for every pair; changing the selected good state is
essential.

The deterministic witness-corpus digests are

```text
order 10  1ae75f2864163e8ec6b04c0d92f012f00375ab55f92cc1284ad8233d4c42ab8f
order 12  b6b5420643799ddfe9ab3f252b0447c7de7704b27ddd8e75eaed39613b567b4e
order 14  26dfe990a6655170f5fdcb6faf1424db279b57e8d094269417b7330fb5affd41
```

At order fourteen the search inspected 381,541 star states and 37,304
exact-good states before completing the pair covers, and made 802,185
local-lift attempts.  These are early-stopping work counts, not full-fibre
sizes.  The final corpus uses 24,268 distinct downstairs states.  The
canonical 509-record graph stream has SHA-256
`efac61759784a8a73305b746838dc0db6c41c4812644b738f90356398fabffd4`.

The SHA-256 hashes of the programs used for the final replays are

```text
order 10/12 checker  bf3ce5e8c82bce4d84a14c80b538cb5337fd4a4a56016d0043eb70a4d82dbcd8
order 14 discovery  f457fbf60bf5f2b94828bcf6295e0bf289b70205c55b70ab81d35de2fbc9697e
order 14 checker    81545f6d0fc1331783a3d7e1d9f267961172a3398a05c635096c093d6638a791
```

> **Finite theorem.**  Let \(H\) be a simple 3-edge-connected cubic
> graph on at most fourteen vertices, let \(r\in V(H)\), and let \(e,f\)
> be independent edges not incident with \(r\).  There is an exact-good
> star packing at \(r\) which has an exact-good square-local lift along
> \(e,f\).

For orders eight, ten, twelve, and fourteen this is exactly the statement
certified above.  Orders four and six can be checked by the same direct
enumeration and also follow from the separate order-six control checker.
The canonical generator has one isomorphism representative of each simple
connected cubic graph; the independent connectivity filter retains exactly
the graphs in the theorem.  Relabelling transports a retained certificate
to every graph in its isomorphism class, so the labelled-root and
labelled-edge-pair coverage proves the displayed finite theorem.

Combined with the separate exact order-eight checker, (L), hence (F),
has no simple 3-edge-connected cubic countermodel through downstairs
order fourteen.  This is a finite theorem only.

## 4. What this does and does not settle

Classical reducible-configuration work already shows that an
edge-minimal counterexample to ordinary Five-CDC can be assumed to have
large girth; in particular, four-cycles are excluded by reductions which
may use more than one smaller replacement.  That result does not imply
the one-fixed-smoothing, one-fixed-root star-fibre assertion (F).

The present work gives neither a proof nor a countermodel to (F).  It
does show:

* preserving one already-selected good state is too strong;
* a fixed five-cover has the exact local obstruction (1);
* allowing the downstairs state to depend on the edge pair repairs every
  canonical instance through order fourteen; and
* any future countermodel to (L) in the simple 3-edge-connected cubic
  class has downstairs order at least sixteen.

A countermodel to (L) would only eliminate this local-lifting proof
route.  A countermodel to (F) would be a countermodel to the stronger
universal star-fibre selection assertion, not automatically a
counterexample to Five-CDC.

## AI-use disclosure

OpenAI Codex, under human direction, formulated and proved the fixed-cover
extension lemma, wrote the exhaustive checker, froze the canonical
streams, and ran the order-ten, order-twelve, and order-fourteen censuses.
The checkers and the displayed proof are provided for human replay.  This
note makes no claim of independent peer review and no claim that Five-CDC
has been resolved.
