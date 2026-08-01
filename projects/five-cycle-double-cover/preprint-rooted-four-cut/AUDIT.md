# Theorem and source audit

Audit date: 2026-07-27.

## Human theorem 1: four-mark core closure

Audited against:

- `docs/four-mark-core-closure.md`;
- `docs/marked-three-edge-cut-signatures.md`;
- `docs/marked-core-cyclic-lift-condition.md`;
- items 50 and 52 of `docs/proof-obligation-ledger.md`; and
- the relevant sections of `docs/current-status.md`.

The proof in `main.tex` restates the two internal shore lemmas and their
proofs so the manuscript does not depend on project-local cross-references.
The common-colour hypothesis is the actual Tait-colouring input used after
the preliminary Kempe-switch lemma. Universal separation is only a sufficient
mechanism for producing that common-colour colouring.

Imported statements checked against primary sources:

- Knappe--Pitz, Fact 5.4 (`g(3)=3`);
- Aldred--Ellingham--Hemminger--Holton, Theorem 3.3 and its independent-edge
  consequence; and
- Nedela--Seifrtova--Skoviera, Theorem 6.1 (with Pastor as a second
  decomposition reference).

No proof defect was found in the narrowed theorem. This is an AI audit, not
human peer review.

## Human theorem 2: forbidden-root reduction

Audited against:

- `docs/root-edge-reduction-four-cut-gate.md`;
- item 52 of `docs/proof-obligation-ledger.md`; and
- the corresponding section of `docs/current-status.md`.

The preprint states the gate as a one-way implication:

> if no all-four cycle avoids the root, then the root lies in an independent
> cyclic four-cut.

It does not claim the converse. The cyclically 5-edge-connected corollary is
immediate. No unrestricted rooted theorem is claimed.

## Exact elliptic-flow reformulation

Audited against:

- `docs/five-cdc-elliptic-quadratic-flow-model.md`;
- the standard at-most-five convention recorded in `docs/current-status.md`;
  and
- Máčajová--Mazzuoccolo--Tabarelli, Definition 3.1, for the prior
  two-subset/CDC-colouring encoding.

The following points were checked directly.

- On the even-weight subspace \(\Gamma\leq\mathbb F_2^5\),
  \(q=e_2\) is one exactly on the ten weight-two vectors.
- Its polar form is the restricted dot product. Its radical is zero:
  orthogonality to every \(e_i+e_j\) makes all coordinates equal, while
  the all-one vector has odd weight.
- The five nonzero singular vectors span \(\Gamma\). Their faithful
  permutation action embeds \(O(\Gamma,q)\) in \(S_5\), and coordinate
  permutations realize the reverse inclusion. Hence
  \(O(\Gamma,q)\cong S_5\).
- The coordinate incidence map is a literal bijection between
  exact-two five-tuples of Eulerian edge sets and everywhere-anisotropic
  \(\Gamma\)-flows.
- A loop must be counted twice in a vertex incidence/XOR row, and hence
  cancels. Parallel edges remain distinct variables.

No defect was found. This is an elementary exact reformulation. The
two-subset encoding is prior work, and no exhaustive literature search has
established priority for the quadratic terminology or packaging.

## Human theorem 3: rooted cycle translation and factorization

Audited against:

- `docs/rooted-cycle-translation-obstruction.md`;
- `docs/exceptional-cyclic-three-root-signature-factorization.md`;
- `docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`; and
- the version-of-record exceptional signatures in
  Máčajová--Mazzuoccolo--Tabarelli.

The blocker proof was checked separately for weight-four and weight-two
translations. Weight-four shifts are excluded exactly by use of all five
coordinates. A weight-two shift survives exactly when every support edge
crosses its \(2+3\) cut. A cycle's distinct label set is connected under
edge adjacency because consecutive local labels are two edges of a triangle.
This gives exactly the non-bipartite/\(K_{1,4}\) blocker alternatives used in
the theorem.

The exact three-cut gluing argument was checked in both directions.
The ordered connector-triangle stabilizer has seven orbits; equality-only
cross-relations force one of four fixed singletons, and disjointness-only
cross-relations give exactly 26 ordered or 13 unordered patterns. The
shore-root nonbridge lemma follows from cubic degree counting and the
excluded cyclic two-cut.

Both archived finite replays were rerun from current source:

```text
PASS rooted cycle translation blocker replay
equality-only = 4
disjoint-only ordered/unordered = 26/13
equal-plus-intersection ordered = 231
```

The Python producers reproduced their frozen JSON files byte for byte, and
the independently written JavaScript checkers passed. No proof defect was
found. The result is only a necessary obstruction: it neither realizes nor
excludes the exceptional rooted signatures and does not resolve the
Five-Cycle Double Cover Conjecture.

## Fixed-five scope correction and cap reduction

The finite SAT/CSP signatures are \(\mathcal C_5(P)\): boundary types
realized inside one fixed five-coordinate \(D_5\) universe. They are not
the published unbounded-colour relation \(P^*\). The manuscript now makes
this distinction before every exceptional-signature consequence.

The non-Tait implication used in the simple-cap reduction remains sound in
the fixed-five model. The proof of Máčajová--Mazzuoccolo--Tabarelli,
Lemma 3.8, starts from a Tait colouring and constructs the required
CDC-colourings with at most four colours, so the same contradiction occurs
inside the fixed five-set.

The simple-cap proof was checked line by line:

- one of the three terminal matchings avoids existing edges, because a
  contrary transversal would be a forbidden terminal star or an isolated
  terminal triangle;
- adding that matching gives independent cap edges and a simple cubic
  graph;
- old edges remain on proper-core cycles and each cap edge closes a path,
  so the cap is bridgeless; and
- a Tait colouring of the cap restricts to one of the pole.

No claim is made about bridge-bearing, repeated-terminal, nonsimple, or
arbitrary-colour poles.

## Base-pair cut certificate

Audited against `docs/rooted-base-pair-cycle-cut-certificate.md`.

Complementation by the four-set avoiding coordinate \(a\) preserves every
two-subset label on a cycle avoiding \(a\), adds the same vector twice at
each cycle vertex, and leaves all boundary labels fixed. A missing
complementary root value therefore makes the root a bridge in the
coordinate-avoiding subgraph.

The exact root signature is invariant under \(3\leftrightarrow4\), since
that permutation fixes the ordered connector word \((01,02,12)\). This
validates all six inner/outer complement pairs and Theorem 3.1 of the note.

The proper-cut convention is essential and is explicit in the manuscript:
\(\delta_Q^{\mathrm p}(X)\) contains proper-core edges only, excluding
boundary semiedges. With that convention,
\[
\delta_Q^{\mathrm p}(X)=\{r\}\mathbin{\dot\cup}F_a
\]
is correct. For \(a=3,4\), the boundary uses neither coordinate, so the
coordinate support on proper edges is Eulerian and \(|F_a|\) is even.
If boundary semiedges were included in this cut, that displayed equality
would be false in general; the proof does not use that alternative
convention.

No defect remains after this clarification. The result is a necessary cut
certificate, not base-pair closure.

## Tait-cap closure and hostile correction

Audited against:

- `docs/rooted-three-pole-tait-cap-closure.md`;
- `docs/rooted-three-pole-base-pair-closure-target.md`;
- `docs/exceptional-cyclic-three-root-signature-factorization.md`;
- `docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`; and
- the cited cubic three-sum decomposition hypotheses.

The Tait-cap closure theorem itself survives line-by-line audit. At the cap
vertex the three colours can be mapped, in physical connector order, to
`01,02,12`. Every cubic vertex then has XOR sum zero. A nonbridge root lies
on a proper cycle, and translation of that cycle by `0123` and `0124`
changes the possible root values as follows:

```text
       01  02  12
+0123  23  13  03
+0124  24  14  04
```

All values remain in \(D_5\), each cycle vertex receives the translation
twice, and the connector word is unchanged. Thus the three root values form
exactly one base pair.

The originally proposed one-sided exceptional corollary was false. The exact
counterexample is
\[
 P_0=\{12,03,04\},\qquad
 R=P_0\cup\{01\},\qquad S=\{01\},
\]
for which \(R,S\) are \(3\leftrightarrow4\)-invariant,
\(P_0\subseteq R\), but
\(\operatorname{rel}(R,S)=\{\mathsf E,\mathsf I\}\).
The mistake was to apply a relation table for \(P_i\) itself after replacing
\(P_i\) by a larger signature \(R\); the additional label can introduce
equality.

The corrected exact consequences are:

- one Tait shore excludes equality-only and disjointness-only relations;
- two Tait shores force both intersection and disjointness, excluding all
  three exceptional relation sets; and
- in a surviving mixed relation with \(P_i\subseteq R\), the opposite
  signature is a nonempty subset of
  \(U_0=\{01,02\}\), \(U_1=\{01,12\}\), or
  \(U_2=\{02,12\}\), respectively, and intersects \(R\).

An independent exhaustive replay checked all three base pairs against all
127 nonempty invariant signatures and reproduced the displayed
\(3\times7\) orbit table. It also reproduced the counterexample above.

The factor-tree consequence initially received a second scope correction
because the cited published decomposition theorem assumes
3-vertex-connectivity. A subsequent elementary audit discharged rather than
assumed that premise. The minimal simple cap is simple, bridgeless, cubic,
and has no cyclic two-edge cut. A cutvertex would expose a bridge. A
two-vertex cut forces two three-edge attachments, and adjoining to one
component the vertex receiving two attachments exposes a cyclic two-edge
cut. Thus the cap is 3-connected and the decomposition theorem applies; the
factor tree is a path.
Both endpoints are non-Tait in the disjointness-only case. In the mixed
\(\mathcal E_4\) case, only an equality-only endpoint is forced non-Tait.

At this audit stage a dependent project-level order-28 lower bound was
withdrawn. The finite cyclically-four order-26 classification remained
valid, but it did not by itself reduce arbitrary exceptional poles to that
class. The later endpoint-factor audit below supplies a different sound
reduction and restores the scoped bound.

## Cap connectivity and fork-triple induction

The repaired cap-connectivity argument was checked line by line. Let \(G\)
be simple, cubic, bridgeless, and without a cyclic two-edge cut. A
cutvertex would leave some component attached by one incident edge, making
that edge a bridge. If \(\{u,v\}\) is a two-vertex cut, every component of
\(G-\{u,v\}\) has at least three boundary edges. A two-edge boundary has,
on either shore \(X\),
\[
 |E(G[X])|=(3|X|-2)/2.
\]
Parity excludes \(|X|=1\), simplicity excludes \(|X|=2\), and every larger
shore contains a cycle. Thus such a boundary would be a forbidden cyclic
two-edge cut. The six incidences at \(u,v\) then force \(uv\notin E(G)\),
exactly two components with three attachments each, and a \(2+1\)
attachment distribution. Adding to one component the vertex receiving its
two attachments creates another two-edge cut; the same count makes both
shores cyclic. Hence \(G\) is 3-connected. An independent exhaustive
small-graph check found no counterexample through order 12.

The subsequent triangle induction was audited against
`docs/rooted-cap-triangle-induction.md`. The following points were checked
independently.

- Contracting a triangle in a simple 3-connected cubic graph of order
  greater than four preserves simplicity and 3-connectivity. Its external
  neighbours are distinct; bridge and cyclic-two-cut obstructions lift
  through the triangle.
- The \(D_5\) contraction/expansion rule is bijective: the three external
  labels XOR to zero, and each internal triangle edge receives the label
  opposite it. A root outside the triangle, including an external edge,
  therefore retains its exact normalized signature.
- A root edge inside the triangle has precisely the three possible labels
  \(\{12,03,04\}\) after local normalization. These form a fork triple
  \(Q(p;q,r;s,t)=\{qr,ps,pt\}\).
- At a triangle containing the deleted connector vertex, the three
  effective connector words and all their coordinate normalizations
  reproduce the displayed base-pair table. More generally, one fixed
  inverse normalization acts simultaneously on all three labels of a
  contracted fork, so it maps that fork to another fork.
- When the connector vertex and root are both on the triangle, the
  remaining unrooted three-pole admits every ordered connector triangle by
  global \(S_5\)-transitivity. Expanding the three required words realizes
  \(12,03,04\).
- A triangle cannot cross a principal cyclic three-cut because that would
  put two cut edges at one shore vertex. A cyclically-four factor with a
  triangle is \(K_4\); an internal \(K_4\) loses two distinct gluing
  vertices, so exposed triangles occur only at the path ends. Connector-end
  contraction removes one \(K_4\) factor and preserves the path-rooted
  premises.

The first draft retained only the conclusion \(|R|\ge3\), which was
insufficient: \(R=S=\{01,02,12\}\) are invariant, contain no standard base
pair, and satisfy
\(\operatorname{rel}(R,S)=\{\mathsf E,\mathsf I\}\).
The corrected fork shape closes that gap. If
\(Q(p;q,r;s,t)=\{qr,ps,pt\}\subseteq R\) and the cross-relation has no
disjoint pair, every \(b\in S\) must meet all three fork labels. Meeting
\(ps\) and \(pt\) forces \(p\in b\) or \(b=st\); the latter misses \(qr\).
Therefore \(S\subseteq\{pq,pr\}\). Applying the fork induction to the
opposite shore is impossible because a fork has three distinct labels.

The upgraded standard-library checker and an independently written replay
both verify the three local root values, all connector normalizations, all
three base-pair rows, all 30 fork triples, coordinate-permutation closure,
and the two-element common-intersector set of every fork. The frozen hashes
are:

```text
checker 2c4dc8f501a3eb0db354146ae1ee9e83231cfe9d45af97b5fa03780d08481006
result  1047a5ddbe98c641cdae37a81c7e4bf30d50a6171fee612eca05fd964b8ead74
```

For a cap of order at most 26, the two capped shores of a principal cut
have total order at most 28 and each has order at least four, hence each
has order at most 24. The resulting mixed-branch elimination remains
conditional on the triangle-free 3-connected screen through order 24.
That screen was still running at this audit and was not treated as passed.
No order-28 lower bound was restored by that triangle-contraction argument
alone.

## Root-end factor lift and restored finite bound

The replacement proof in `docs/rooted-cap-end-factor-fork-lift.md` was
hostile-audited independently of the pending triangle-screen route.

- In a minimal simple cap, absence of cyclic two-cuts gives
  3-connectivity. Every cyclic three-cut separates the two cap edges, so
  the factor-incidence tree is the path \(F_1,\ldots,F_k\).
- Choose one whole-shore labelling. Its first principal cut has an ordered
  connector triangle \(\alpha\). Restrict and permanently fix the
  labelling of \(F_2,\ldots,F_k\), including \(\alpha\) and the far
  external word.
- A single coordinate permutation \(\sigma\) takes \(\alpha\) to the
  normalized word \((01,02,12)\). Apply the same \(\sigma^{-1}\) to all
  three endpoint labellings in a base pair. Each now has connector word
  \(\alpha\), hence all three glue to the same fixed remainder.
- Their root values are one coordinate image of the base pair, therefore
  a fork \(\{qr,ps,pt\}\). Restricting the original whole-shore labelling
  also proves endpoint-signature nonemptiness.
- The root is a nonbridge in the endpoint factor: the factor is
  3-connected (or \(K_4\)), and deleting the virtual vertex leaves a
  2-connected graph.

The fork-crossing lemma was checked line by line. If a two-set meets all
three members of \(\{qr,ps,pt\}\), it is one of \(\{pq,pr\}\); hence a
second three-member fork cannot avoid a disjoint cross-pair. If no unequal
intersecting cross-pair existed, the second fork would collapse to the
singleton \(\{qr\}\). Thus any two forks force both \(\mathsf I\) and
\(\mathsf D\). The one-sided equality-only and disjointness-only exclusions
also follow immediately.

An independent standard-library replay constructs all 60 ordered connector
triangles, verifies their two normalizations, enumerates all 30 forks, and
checks all \(30^2=900\) ordered fork pairs. The relation counts are:

```text
{I,D}       330
{E,I,D}     570
```

Frozen hashes:

```text
checker 2474c8869be64e3386b23a58e1b929e5e0f56227d19033e3d4316fbb17e1f136
result  738cbf30b1361b6de5bc18a13e4dfbafa9878a8bfdd9755e21b98afcda6dd513
```

The complete endpoint package proves base-pair closure through factor
order 26. Therefore the mixed cyclic-three branch has at least one endpoint
factor of order 28 or more. Reversing the vertex three-sums gives
\[
 |V(G)|\ge28+4+4(k-2)-2(k-1)=2k+26\ge30.
\]
For equality-only or disjointness-only, both endpoints have order at least
28 and
\[
 |V(G)|\ge28+28+4(k-2)-2(k-1)=2k+50\ge54.
\]
Together with the completed cyclically-four cap classifications through
order 26, this restores the bridge-free connected simple
terminal-distinct fixed-five exceptional-pole lower bound 28. At this
stage a first order-28 exception would have needed a cyclically
four-edge-connected cap.

The endpoint package's independently written `verify.py` was rerun after
the manuscript edit. It reconstructed all 38,244 cores and 1,360,452
nonbridge roots and reproduced `report.json` byte for byte.

## Order-28 two-orbit certificates and the scoped order-30 bound

The package `search/four-pole-order28-cyclic4-cap-20260727/` was audited
against its theorem, source stream, witness format, Python verifier, and
the independently written zlib/C++ checker.

The human mask gate is exact. In the frozen ten-orbit ordering, orbit 0 is
\((01,01,01,01)\) and orbit 2 is \((01,01,23,23)\). Directly reading the
six mask bits gives:

```text
mask     bit 0   bit 2
0x02b      1       0
0x053      1       0
0x119      1       0
0x2e4      0       1
0x3a4      0       1
0x3c4      0       1
```

Thus a positive orbit-2 witness excludes each first-family mask, and a
positive orbit-0 witness excludes each second-family mask. No negative
solver answer or UNSAT certificate is involved.

The corpus arithmetic is independently transparent. Every cubic order-28
cap has 42 edges. Simplicity makes the 84 adjacent edge pairs counted by
the 28 vertices disjoint as pairs, so each cap has
\[
 \binom{42}{2}-28\binom32=777
\]
independent edge pairs. Hence \(12\,517\cdot777=9\,725\,709\) deletion
rows and twice that number, \(19\,451\,418\), displayed labellings.

Both certificate checkers enumerate \(D_5\) independently, recover the
canonical boundary-orbit representatives, require the prescribed boundary
word, and xor the three incident labels at every completed cubic vertex.
The Python verifier additionally reconstructs every deletion from the cap
source and checks order, cubicity, connectedness, bridgelessness,
triangle-freeness, and non-Taitness. The C++ checker treats the compressed
pole stream as primary input and reconstructs incidence independently of
the producer and Python verifier. Both full replays were rerun for this
manuscript audit. The Python verifier reproduced `report.json` byte for
byte, and the C++ replay reproduced `independent-fast-replay.json`
exactly:

```text
rows       9,725,709
witnesses 19,451,418
missing            0
```

Canonical source completeness and cyclic four-connectivity are not
independently regenerated by either checker; as the theorem states, those
claims rely on Snarkhunter 2.0b and its documented command semantics. A
triangle cannot occur in a cyclically four-connected order-28 cap: its
three leaving edges separate it from a 25-vertex complement with 36
internal edges and hence a cycle. The retained girth-four source therefore
has the right mathematical scope, conditional on the generator provenance.

Combining the order-28 exclusion with the endpoint-fork lower bound 30 for
the cyclic-three branch leaves no scoped exception through order 28. Since
\(3n-4=2m\), \(n\) is even and the next possible order is 30. This proves
the bridge-free connected simple terminal-distinct fixed-five lower bound
30. Order 30 remains open, and Five-CDC remains unresolved.

The package documentation now has both intended checksum ledgers:
`SHA256SUMS` covers the retained package artifacts, while
`SOURCES.sha256` freezes the external source dependencies.  The integrity
command in `REPRODUCING.md` was replayed successfully, as were both full
semantic checks.

## Finite rooted frontiers

The order-17 base-pair package was checked with:

```text
python3 search/rooted-three-pole-frontier-20260727/verify_order17_base_pair_run.py \
  search/rooted-three-pole-frontier-20260727/artifacts/order17-base-pair
python3 search/rooted-three-pole-frontier-20260727/verify_report.py
```

The verifier reproduced `order17-base-pair-report.json` byte for byte.
Both engines report 654,676 canonical cores, 15,645,623 nonbridge roots,
337,059 empty signatures, 15,308,564 base-pair-closed signatures, zero
violations, and 52,216,251 solver calls. All eight paired transcript
digests match.

For the cyclically-four order-22 cap slice, the completed portion of
`verify_completed_run.py` was invoked directly through hard-corpus
identity, cyclically-four extraction, independent-edge expansion, full
signature comparison, and exceptional-query checks. It reconstructs:

```text
bridgeless non-Tait graphs       12,892
cyclically 4-connected caps          31
independent-edge deletion poles  14,322
full-type queries per engine     143,220
nonfull rows                           0
```

The CaDiCaL and CSP compressed outputs are byte-identical. Their
uncompressed SHA-256 is
`52edd8a189012acefd3565a79d5c58b6f209bbe40156560eb57e2c569fd7c091`,
and every row has mask `0x3ff`.

The later all-cap phase is now complete. Both classifiers agree across all
eight shards on \(5\,956\,104\) deletion poles and
\(23\,747\,129\) exact signature queries per implementation, with zero
exceptional hits. The independent verifier reconstructs the source,
deletion stream, shard digests, and summaries.

## Fano component-parity normal form

`docs/five-cdc-fano-component-parity-lift.md` was independently read.
The quadratic table, one-cycle lift, \(T\)-join component criterion,
converse singular-vector quotient, and loop convention are sound. Equation
(12) correctly uses the fact that the only XOR-zero subsets of the four
points outside a Fano line are the empty set and the full four-set.

This is a clean one-cycle normal form of the project's existing
quotient-lift theorem, not a new characterization. It was therefore omitted
from the manuscript rather than inflated into another contribution.

## Computational theorem: material correction

Audited against:

- `docs/order22-universal-four-separation-screen.md`;
- `scratch/order22-universal-four-separation-result.json`;
- `scratch/tait_all_coloring_mark_separation.cpp`;
- `scratch/verify_order22_separation_via_matchings.cpp`;
- item 53 of `docs/proof-obligation-ledger.md`; and
- the relevant experiment and status ledgers.

The earlier note's unqualified statement over all connected simple cubic
graphs was not what the programs establish. Both programs skip a graph after
finding no Tait colouring. The exact theorem is restricted to the 7,174,735
Tait-colourable graphs among the 7,319,447 generated order-22 graphs.

This qualifier cannot be treated as stylistic: with no Tait colourings,
"separated in every Tait colouring" is vacuously true. The audit found this
issue; the project report, JSON, status, experiment ledger, and proof ledger
were then corrected. The preprint states the corrected theorem explicitly.

Corrected artifact hashes:

```text
report  53faa21acfaf75e6bf1d54d6c7d73150a57207067be4f44e20c55be220c322a2
JSON    59d8e99cffb573de6ffa8a4df122099db3fd856d8e87803920e9cf69d6946ca8
```

Current source hashes agree with the frozen JSON. JSON shard totals were
recomputed. Complete order-12, order-16, and order-18 controls were rerun
with both current executables and matched the recorded counts.

## Final manuscript build

`tectonic main.tex --outdir output/pdf` completed without errors. The
resulting PDF has 29 letter-size pages and SHA-256

```text
8d0da87f5e07abf1dc5cc25e05f16faeb442a7dead8754f7b8bb4b88596f9b95
```

All 29 pages were rasterized with Poppler and inspected as a contact sheet;
the new theorem pages 22--24 and the first page were also inspected
individually at full rendered resolution. No clipping, overflow, missing
glyph, broken equation, or obvious layout defect was found. `pdftotext`
confirms that the endpoint-fork lift, order-28 two-orbit theorem, scoped
order-30 lower-bound theorem, Five-CDC disclaimer, and AI-use disclosure
are present. Every entry in `CHECKSUMS.sha256` verifies.

## Overall status

The manuscript is a research draft, not a Five-Cycle Double Cover resolution.
It separates:

- fully displayed human arguments;
- clearly named imported theorems; and
- exact but non-formal finite computations.

Independent human proof review and independent full-machine replay remain
required before publication.
