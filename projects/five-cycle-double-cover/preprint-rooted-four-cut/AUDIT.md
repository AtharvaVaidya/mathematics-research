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

The factor-tree consequence received a second scope correction. The
minimal simple-cap argument proves that every relevant cyclic three-cut
separates the cap edges and proves 3-edge-connectivity. The cited published
decomposition theorem assumes 3-vertex-connectivity. The preprint therefore
assumes a 3-connected cap (or, equivalently for the deduction, that the
factor tree has already been supplied); it does not promote
3-edge-connectivity to 3-connectivity. Under that premise the tree is a path.
Both endpoints are non-Tait in the disjointness-only case. In the mixed
\(\mathcal E_4\) case, only an equality-only endpoint is forced non-Tait.

This audit also withdrew a dependent project-level global order-28 lower
bound. The finite cyclically-four order-26 classification remains valid, but
it does not by itself reduce arbitrary exceptional poles to that class.

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

The verifier's later all-cap phase was not run because its 5.9-million-row
artifact was still pending. The manuscript claims only the completed
cyclically-four slice and says so explicitly.

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

## Overall status

The manuscript is a research draft, not a Five-Cycle Double Cover resolution.
It separates:

- fully displayed human arguments;
- clearly named imported theorems; and
- exact but non-formal finite computations.

Independent human proof review and independent full-machine replay remain
required before publication.
