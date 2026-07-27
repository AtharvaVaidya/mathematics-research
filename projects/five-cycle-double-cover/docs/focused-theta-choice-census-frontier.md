# Focused theta-choice census and alternating-exchange frontier

## Status

This memo records a finite exact result, not a universal theorem.

For every independent root pair in the retained complete
cyclically-4-edge-connected non-Tait simple cubic corpora at every even
order from \(10\) through \(28\), either

1. deleting the four root endpoints leaves a graph with a perfect
   matching; or
2. it leaves a graph of matching deficiency two for which at least one
   maximum near-perfect matching has a theta complement.

No root pair for which every maximum near-perfect matching has a
loop--link--loop complement was found.  The screen covers 14,009 graphs
and 10,689,351 independent root pairs.  This census does **not** prove
the corresponding assertion for arbitrary order, and it does not resolve
the Five-Cycle Double Cover Conjecture.

## 1. Definitions and the exact three-way classification

Let \(G=(V,E)\) be one of the simple cubic graphs in the stated corpus.
Let \(R=\{r_1,r_2\}\) be two independent edges, let \(U=V(r_1)\cup
V(r_2)\), and put \(H=G-U\).

The previously proved deficiency theorem gives
\[
                 \operatorname{def}(H)
                 = |V(H)|-2\nu(H)\leq 2.
\]
The order of \(H\) is even, so its deficiency is even.  Consequently,
an unsuccessful perfect-matching test implies
\(\operatorname{def}(H)=2\), not merely a lower bound.

For every maximum matching \(P\) of such an \(H\), exactly two vertices
of \(H\) are exposed.  In
\[
                         F=G-(R\cup P),
\]
those two vertices have degree three and every other vertex has degree
two.  The proved two-branch core dichotomy says that, after suppressing
degree-two paths, the component containing the branch vertices is
either a theta or a loop--link--loop.  The former case is equivalent to
\(F\) having no bridge; the latter has a bridge on its link.  Any
separate degree-two components are circuits and contain no bridge.
Thus the following computational classification is exact:

* `def0`: \(H\) has a perfect matching;
* `def2_theta`: \(H\) has no perfect matching, and some maximum
  near-perfect matching \(P\) makes \(F\) bridgeless;
* `def2_all_dumbbell`: \(H\) has no perfect matching, and exhaustive
  enumeration of its maximum near-perfect matchings finds a bridge in
  every corresponding \(F\).

There is no optimization or heuristic hidden in this trichotomy.

## 2. Corpus scope

The census uses exactly these retained graph6 files:

| order | graphs | retained source | SHA-256 |
|---:|---:|:---|:---|
| 10 | 1 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order10.g6` | `7aec0fba73c081d7eebc551fc46b2484e73e58b2d36718dee105dbb6226e76aa` |
| 12 | 0 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order12.g6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 14 | 0 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order14.g6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 16 | 0 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order16.g6` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 18 | 2 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order18.g6` | `2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd` |
| 20 | 6 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order20.g6` | `a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1` |
| 22 | 31 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order22.g6` | `2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223` |
| 24 | 155 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order24.g6` | `37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456` |
| 26 | 1,297 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order26.g6` | `1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760` |
| 28 | 12,517 | `search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order28.g6` | `b4f6494c23793a40158a03ccd7c0943ae2e397c90a1467e27814bd007789be1f` |

The retained Snarkhunter 2.0b logs give the exact command
`snarkhunter n 4 S s C4 o g` at every displayed order.  The bundled
sources at orders 20 through 28 are byte-identical to the previously
audited packages.  This memo inherits the documented generator
completeness and option semantics; its classifiers do not constitute a
second canonical generator.

## 3. Exact results

| order | independent root pairs | def0 | def2, some theta | def2, all dumbbell |
|---:|---:|---:|---:|---:|
| 10 | 75 | 60 | 15 | 0 |
| 12 | 0 | 0 | 0 | 0 |
| 14 | 0 | 0 | 0 | 0 |
| 16 | 0 | 0 | 0 | 0 |
| 18 | 594 | 569 | 25 | 0 |
| 20 | 2,250 | 2,183 | 67 | 0 |
| 22 | 14,322 | 14,047 | 275 | 0 |
| 24 | 86,490 | 85,156 | 1,334 | 0 |
| 26 | 859,911 | 848,725 | 11,186 | 0 |
| 28 | 9,725,709 | 9,617,033 | 108,676 | 0 |
| **total** | **10,689,351** | **10,567,773** | **121,578** | **0** |

The programs additionally classified \(|\delta_G(U)|\) for every
deficiency-two pair.  All \(121,578\) instances had boundary eight; none
had boundary six.  This is an empirical pattern in these ten corpora,
not a theorem at arbitrary order.

The total `near_matchings_checked` count is 560,804.  Enumeration stops
at the first theta matching, so this is a reproducibility diagnostic,
not the total number of maximum near-perfect matchings.

## 4. Two independent exact implementations

The primary implementation is
`scratch/focused-theta-choice-census.cpp`.  It:

1. parses each graph6 record and verifies the simple cubic degree
   condition;
2. visits every unordered pair of vertex-disjoint edges;
3. decides perfect matchability by an exact bit-mask recursion;
4. after a negative decision, exposes every unordered pair of
   \(H\)-vertices and recursively enumerates every perfect matching of
   the remaining vertices until a theta is found;
5. uses an edge-indexed Tarjan bridge test on \(G-(R\cup P)\).

The independent replay is
`scratch/verify-focused-theta-choice-census.py`.  It neither runs nor
imports the C++ implementation.  It has a separately written graph6
parser, matching recurrence, near-perfect enumeration, and Tarjan
bridge audit.  It checks all ten corpus hashes and asserts every
count in the table.

Reproduction commands from the repository root are:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  scratch/focused-theta-choice-census.cpp \
  -o /tmp/focused-theta-choice-census

for n in 10 12 14 16 18 20 22 24 26 28; do
  /tmp/focused-theta-choice-census "$n" \
    "search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order$n.g6"
done

python3 scratch/verify-focused-theta-choice-census.py
```

The frozen machine-readable result is
`scratch/focused-theta-choice-census-result.json`.

## 5. Human-checkable alternating-exchange facts

The census suggests looking for a matching-exchange proof, but the
following are the facts presently established.

### Lemma 5.1 (exposed-vertex rotation)

Let \(P\) be a maximum matching of a graph \(H\), and let \(a\) be
exposed by \(P\).  Suppose
\[
        Q=a v_1 v_2\ldots v_{2k}=z
\]
is a simple even path whose edges alternate outside \(P\), inside
\(P\), outside \(P\), inside \(P\), and so on.  Then
\[
                         P'=P\mathbin{\triangle}E(Q)
\]
is a maximum matching of the same cardinality.  It matches \(a\),
exposes \(z\), and agrees with \(P\) off \(Q\).

#### Proof

At every internal vertex of \(Q\), toggling removes its unique
\(P\)-edge on \(Q\) and inserts its unique non-\(P\) edge on \(Q\).
At \(a\) it inserts the first edge; at \(z\) it removes the last edge.
Thus \(P'\) is a matching.  The path contains equally many inserted and
removed edges, so \(|P'|=|P|\), and maximum cardinality is preserved.
\(\square\)

The same local degree check proves that toggling an even alternating
cycle preserves both cardinality and the exposed set.

### Lemma 5.2 (difference of two maximum near-perfect matchings)

If \(P\) and \(Q\) are maximum matchings of an even-order graph and each
exposes exactly two vertices, every component of
\(P\mathbin{\triangle}Q\) is an alternating even circuit or an
alternating path.  The path endpoints are precisely the vertices
exposed by exactly one of \(P,Q\).  Consequently \(Q\) can be obtained
from \(P\) by cardinality-preserving circuit switches and the
exposed-vertex rotations of Lemma 5.1.

#### Proof

Every vertex has degree at most two in the symmetric-difference graph,
and a degree-two vertex is incident with one edge from each matching.
Its components are therefore alternating circuits and paths.  Circuit
lengths are even.  A path endpoint is incident with exactly one of the
two matchings and hence is exposed by the other.  No path can contain
one more \(Q\)-edge than \(P\)-edge, because toggling just that component
would augment the maximum matching \(P\).  By symmetry, no path can
contain one more \(P\)-edge than \(Q\)-edge.  Every path therefore has
the same number of edges from the two matchings and is even.  Toggling
its components one at a time gives the stated sequence of
cardinality-preserving rotations and circuit switches. \(\square\)

For the present root problem, every such exchange occurs wholly in
\(H\), so the prescribed root matching \(R\) remains fixed.

## 6. Where the universal proof attempt stops

For a maximum near-perfect \(P\), let
\[
                  \beta(P)=\#\{\text{bridges of }G-(R\cup P)\}.
\]
The theta goal is exactly \(\beta(P)=0\).  If a universal counterexample
exists, choose \(P\) minimizing \(\beta(P)>0\).

For every link bridge \(g\) of this minimal dumbbell, Lemma 3.2 of the
deficiency memo gives at least one non-root matching edge of \(P\)
crossing the cyclic cut determined by \(g\).  Hence every bad bridge has
an exchange *chord*.  Lemmas 5.1 and 5.2 show exactly which alternating
paths and circuits may be switched without moving the roots or reducing
the matching size.

The missing implication is:

> From a \(P\)-edge crossing a link cut, construct a
> \(P\)-alternating even path or circuit whose switch strictly decreases
> \(\beta(P)\) (or otherwise yields a theta complement).

Lemma 3.2 alone does not supply this.  Its crossing \(P\)-edge need not
lie in an alternating circuit, and the alternating path reaching it
may end at the wrong exposed vertex, may cross the same cut again, or
may replace the destroyed bridge by another bridge.  Tight-barrier
rigidity controls the odd components of \(H-S\), but does not by itself
provide the required alternating reachability.  Claiming the missing
implication would therefore be circular.

A sound next target is a **rotation-closure lemma**: prove that a
\(\beta\)-minimal dumbbell matching in the boundary-eight tight-barrier
configuration cannot be closed under every exposed-vertex rotation and
alternating-cycle switch.  The finite census says this obstruction does
not occur through order 28 in the retained class; it does not say why.

## 7. Provenance and AI disclosure

This memo, the primary classifier, and the independent replay were
written with OpenAI Codex assistance.  The mathematical statements
above are intentionally limited to arguments displayed in full or to
the cited, separately retained deficiency/core lemmas.  Every finite
claim is reproducible from hashed input files by two source-independent
implementations.  No computational output is represented as a proof of
the unresolved universal statement.

## 8. Frozen artifact hashes

The source and result files used for the final replay have these
SHA-256 digests:

```text
d82dbfd6daa03d267f433184f823c43ceb52fcdbee5dc708de6bb0eda7183ae5  scratch/focused-theta-choice-census.cpp
101b52b3da2e739948598ce4f274aeb38591f2f587a4ba7590495ea21d15b833  scratch/verify-focused-theta-choice-census.py
79f52d8b554c500b6c65c2539ede4b913b341ec69daba4475f61c7b365c53b38  scratch/focused-theta-choice-census-result.json
af05f455b7f691c4e3b00c912fef82366d9f8cff939c5a271443d76250eec33f  search/focused-theta-choice-through28-20260727/primary-results.ndjson
8881cf170162d48bdd4a2c8c00e72581349cdd06655a0f38a326540ad5576522  search/focused-theta-choice-through28-20260727/independent-replay-through26.json
2a339e5b5efcb21e88d67433435ca6dae9ec5580a95f26f9150001c5f65f930c  search/focused-theta-choice-through28-20260727/independent-replay-order28.json
```
