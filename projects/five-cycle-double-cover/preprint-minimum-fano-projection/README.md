# Minimum extendable Fano projections

This directory contains a short AI-assisted working preprint about a
minimum-support route to the standard five-cycle double cover conjecture.

**Resolution status:** FiveCDC remains open. The paper proves a
human-checkable exchange theorem and a complete minimum-projection theorem
through support size fifteen for connected bridgeless loopless cubic
graphs, reports exact finite censuses, and states the remaining universal
selection principle as an explicit conjecture. It claims neither a proof
nor a counterexample to FiveCDC. An elementary incidence-cluster theorem
reduces the standard conjecture for arbitrary finite bridgeless multigraphs
to the cubic setting, but the minimum-projection theorem itself remains
cubic.

Build from this directory with:

```sh
SOURCE_DATE_EPOCH=1785283200 tectonic main.tex
```

Run the exhaustive order-18 checker from the project root with:

```sh
python3 scratch/check_husek_samal_minimum_projection_frontier.py \
  --order 18
```

The checker requires:

- Python 3;
- nauty `geng` on `PATH`; and
- `scratch/search_fano_all_bad_projection_subspaces.py`.

It has no SAT-solver, network, or nonstandard Python-package dependency.
The expected canonical hard-record SHA-256 is:

```text
82b01cc2f01d4f50f7745f4bdb1b3dc46ade798d452a9d4f11d4a91d738a7834
```

Replay the dependency-free case split and explicit low-flow repairs for
the size-at-most-five theorem with:

```sh
python3 scratch/minimum-projection-size5-theorem-20260729/verify.py
```

Replay the cumulative cleanability theorem through size fifteen with:

```sh
python3 scratch/minimum-projection-through11-cleanability-20260729/verify_through10.py
python3 scratch/minimum-projection-through11-cleanability-20260729/verify.py
python3 scratch/minimum-projection-through12-clean-or-delete-20260729/verify_output.py
python3 scratch/minimum-projection-size12-independent-audit-20260729/replay.py
python3 scratch/minimum-projection-through13-clean-or-delete-20260729/verify_output.py
python3 scratch/minimum-projection-size13-independent-audit-20260729/replay.py
python3 scratch/minimum-projection-size14-dichotomy-counterstate-20260729/verify.py
python3 scratch/minimum-projection-size14-dichotomy-counterstate-20260729/analyze_realization.py
python3 scratch/minimum-projection-size14-independent-audit-20260729/verify_abstract.py
python3 scratch/minimum-projection-size14-independent-audit-20260729/verify_realization.py
python3 scratch/minimum-projection-through14-cleanability-20260729/verify_summary.py
python3 scratch/minimum-projection-size14-7p7-independent-audit-20260729/replay_full_census.py
python3 scratch/minimum-projection-size14-7p7-independent-audit-20260729/independent_audit.py
python3 scratch/minimum-projection-size14-kempe-escape-20260729/verify_all_certificates.py
python3 scratch/minimum-projection-size15-exact-frontier-20260729/verify_summary.py
python3 scratch/minimum-projection-size15-induction-audit-20260729/audit_induction.py \
  scratch/minimum-projection-size15-exact-frontier-20260729/7p8-shard16-*.txt \
  --expect-full-7p8
python3 scratch/minimum-projection-size15-anchor-single-audit-20260729/audit_anchor_shards.py \
  scratch/minimum-projection-size15-exact-frontier-20260729/15-shard16-*.txt
python3 scratch/minimum-projection-single-circuit-tensor-frontier-20260729/independent_audit.py
python3 scratch/minimum-projection-two-occurrence-interaction-20260729/verify.py
python3 scratch/minimum-projection-two-occurrence-interaction-20260729/independent_audit.py
python3 scratch/cubic-reduction-standard-fivecdc-20260729/verify_local_relations.py
python3 scratch/general-kempe-descent-static-exchange-obstruction-20260729/verify.py
python3 scratch/general-kempe-descent-static-exchange-obstruction-20260729/independent_audit.py
python3 scratch/general-kempe-descent-static-exchange-obstruction-20260729/kempe_state_graph.py
python3 scratch/minimum-projection-dynamic-kempe-frontier-20260729/verify.py
python3 scratch/minimum-projection-dynamic-kempe-frontier-20260729/independent_audit.py
```

The dependency-free checker exhausts every support shape allowed by the
minimum-exchange theorem through size ten.  For every proper affine word
and every conserved component partition, it constructs independent
\(\mathrm{GL}(2,2)\) maps on the complement components and new low values
on the projection circuits.  All 125,178 valid dirty canonical
word/partition states are directly cleaned through size ten.  At size
eleven, 14 direct-repair failures occur in the \(5+6\) shape, but every
one has a checked size-five replacement and therefore cannot be globally
minimum.  A second independently written implementation reproduced all
size-eleven counts and the 14 replacement certificates.  At size twelve,
13,788,824 dirty states split into 13,788,432 direct repairs and 392
strict circuit-deletion certificates, with zero residuals.  A separately
written word-orbit/exact-cover auditor reproduces the entire size-twelve
census.  At size thirteen, two independently written exact classifiers
agree on all five support shapes and all 189,998,862 charge-valid states.
Of the 159,369,966 dirty states, 159,362,292 clean directly and 7,674
admit a strict circuit deletion; again there are zero residuals.
At size fourteen the primary exact classifier enumerates 9,481 word
orbits and 2,616,134,989 charge-valid states.  Among 2,255,478,176 dirty
states, 2,255,331,588 clean directly and 146,364 admit strict circuit
deletion, leaving 224 residuals.  Every residual has shape \(7+7\).
A separately written full \(7+7\) enumerator independently reproduces
all 333 word orbits, 91,481,505 charge-valid states, and the identical
224-row failure set.  A human-checkable two-colour path-switch lemma and
724 literal matching-robust certificates give every residual a strict
size-seven deletion escape in every cubic realization.  Hence every
globally minimum extendable projection of size at most fourteen is
cleanable.

At size fifteen the exact classifier covers all eight support shapes:
26,492 canonical word orbits and 35,247,202,556 charge-valid abstract
states. Among 31,088,622,592 dirty states, 31,086,255,789 clean directly,
2,360,767 admit strict circuit deletion, and 6,036 remain after those two
tests. Every residual has shape \(7+8\). A separately written canonical
induction checker links every residual to a frozen size-fourteen
matching-robust Kempe family. A separate literal matching-game checker
verifies a realization-robust rescue directly on every residual.
The single-circuit row is also settled without enumeration by a new
human-checkable relative-\(\mathrm{GL}(2,2)\) tensor theorem: every
charge-valid one-circuit boundary directly cleans at arbitrary length.
The completed 16-shard anchor census agrees, finding zero failures among
23,398,774,592 dirty one-circuit states; a zero-sum-partition recurrence
independently reproduces the partition totals. Hence every globally
minimum extendable projection of size at most fifteen is cleanable.

The tensor theorem also cleans several support circuits when every
complement component is charge-balanced separately on each circuit.
Ordinary boundary conservation requires only total balance across all
circuits, so this corollary does not settle the general multi-circuit
case.

That stronger per-circuit hypothesis cannot simply be omitted.  When every
complement component has two support occurrences, feasible component-map
images are exactly nowhere-zero \(\mathbb F_2^2\)-flows on the interaction
multigraph whose vertices are support circuits.  The two occurrences are
clean exactly when they traverse the same unoriented edge of the \(K_4\)
on the low colours.  The Petersen graph, with its two 5-circuits as
support and perfect matching as complement, gives the smallest loopless
two-occurrence abstract failure of direct cleaning.  All 60 interaction
flows fail to clean, but every one omits a colour on one support circuit
and strictly deletes it.  An explicit deletion reaches a globally minimum
size-five clean projection.  This is a sharp boundary-method obstruction,
not a FiveCDC counterexample.

The unrestricted boundary dichotomy still first fails at size fourteen,
on an explicit \(7+7\) state.  Its 18-vertex simple bridgeless cubic realization
has 15,360 ordered extensions of the displayed projection and none is
clean.  Exact cycle-space enumeration nevertheless finds minimum
projection size five, four minimum supports, and all four cleanable.  This
is a sharp counterexample to the support-preserving boundary method, not
to FiveCDC; the new theorem first changes the low flow along one or two
Kempe paths and only then deletes a circuit.
The size-fourteen package includes `HUMAN-PROOF.md`, which proves the
failure by four affine-line constraints without relying on its 40-row
finite certificate.  The Kempe package has its own human proof, exhaustive
certificate builder, independently structured literal checker, frozen
outputs, and hash ledger.

The human-checkable reduction showing that, for fixed component maps,
cleaning is an affine XOR system is written in full at
`scratch/minimum-projection-fixed-map-affine-cleaning-20260729/README.md`.
The companion derivation
`scratch/clean-or-delete-quadratic-reduction-20260729.md` also derives the
dual system and the new identity in one notation.  The manuscript now proves a
six-map parity identity: postcomposing the maps on the components selected
by any one dual inconsistency witness preserves circuit integrability, and
one of the six \(\operatorname{GL}(2,2)\) choices changes that witness's
obstruction bit from one to zero.  The independent audit at
`scratch/clean-or-delete-quadratic-reduction-audit-20260729/` recomputes
the 16-entry local table and checks both identities on 126,258 balanced
circuit rows through length eight.  This neutralizes one chosen witness
only; it is not a simultaneous cleaning or termination theorem.  The
exact dynamics package
`scratch/minimum-projection-dual-neutralization-dynamics-20260729/`
shows why: the forty reduced map states of the size-fourteen boundary
form one strongly connected neutralization graph and contain a displayed
four-step cycle.  A literal graph cycle gives an exchange gain \(6-2=4\)
at one state for every relative translation, so the orbit is excluded
from global minimality in that realization.  The conclusion is a
failed-approach certificate, not a FiveCDC counterexample.

The complementary LP boundary is isolated in
`scratch/minimum-projection-tjoin-dual-zero-price-20260729/`.  A
human-checkable shortest-\(T_c\)-join duality proof shows that every cut
which is a union of components of \(G-h\) has coefficient zero in every
optimal dual, for all four affine colours.  Hence the rainbow witness cut
is already zero-priced; a neutralizing switch removes four zero
variables, and the aggregate four-dual optimum remains \(3|h|\).  Every
positive dual shore must instead split a complement component.  The same
proof gives
\[
 |E-h|\ge |h|-|M_c|\quad(c\in\mathbb F_2^2),\qquad
 |h|\le 6|V|/7
\]
in a cubic graph.  Thus any viable dual descent must transport interior
metric or Kempe-pairing information.

The same reduction records the exact size-fourteen counterstate.  The
Kempe escapes show how internal two-colour paths supply additional
information absent from the abstract map-choice implication.  The
unresolved frontier starts at support size sixteen and, structurally, in
multi-circuit states that are not circuitwise balanced.

The exact standard convention and general-to-cubic/snark reductions are
proved in
`scratch/cubic-reduction-standard-fivecdc-20260729/README.md`.  Its
pushforward proof includes loops by incidence multiplicity.  A hostile
second audit checked the structural reductions separately from the finite
\(D_5\)-label checker.  The reduction is standard in character and is not
claimed as novel.

The proof-method boundary is sharpened in
`scratch/general-kempe-descent-static-exchange-obstruction-20260729/`.
Its human proof shows that a chain of coloured \(K_4-e\) two-poles
preserves the support, complement-component partition, and every
two-colour boundary pairing while forcing all four static exchange
inequalities.  The literal 230-vertex example defeats all 97 nonempty
one-round fixed-colour path multiswitches, but a checked two-round sequence
reaches a strict circuit deletion.  The graph is Tait-colourable and its
minimum projection is empty, so this is not a counterexample to the
selection conjecture or FiveCDC.  It proves that the unresolved argument
must use the exchange theorem dynamically after neutral recolourings.
The full-cycle and shortest-\(T\)-join checkers verify the four inequalities
by different methods; an agent hostile audit passed after correcting the
terminal-distance exposition, but no independent human has reviewed it.

The next dynamic boundary is isolated in
`scratch/minimum-projection-dynamic-kempe-frontier-20260729/`.  A complete
human proof shows that when the support is one circuit and every complement
component has exactly two vertices on it, componentwise linear maps and
reintegration always produce a clean extension.  This is an unbounded
theorem.  A second proof shows that chains of the \(K_{3,3}-e\) two-pole
reflect every boundary-changing three-colour Kempe move.  Consequently,
any hypothetical goal-free base orbit can be inflated so that all four
minimum-exchange inequalities hold after every reachable recolouring,
without creating a new clean or deletion boundary state.  No such base
orbit is known, so the transfer theorem is conditional and does not
construct a FiveCDC counterexample or a globally minimum positive
projection.  Two independently written dependency-free checkers audit the
finite pole and incidence claims; a hostile agent audit passed, but no
independent human has reviewed the new lemmas.

Run the expanded exact replay with:

```sh
python3 scratch/minimum-projection-census-through28-20260729/verify_summary.py
```

It checks 14,009 frozen cyclically-4 non-Tait records through order 28
and a separate 12,892-row hard order-22 source. All 147,539 minimum
extendable projections in those literal files are cleanable. The broader
population completeness statements are inherited from the documented
upstream generation packages.

The retained order-34/order-40 strong-snark scan is:

```sh
python3 scratch/minimum-projection-known-strong-snarks-20260729/verify.py
```

It checks frozen outputs for 7,661 literal graph6 rows and 433,730 minimum
projections, all cleanable and all of minimum size ten. The bundled package
contains its exact SAT scanner and a second linear-algebra implementation;
the latter cross-checks all seven order-34 rows and the first five order-40
rows. Population completeness beyond the literal files is inherited.

The certified 130-vertex stress test is:

```sh
python3 search/minimum-projection-n130-20260729/verify.py
```

It proves minimum extendable-projection size 42, exhausts exactly 11,264
minimum supports, and checks that all are cleanable. Two LRAT certificates
establish the lower bound and enumeration completeness. The same graph has
minimum nonzero Fano value-class size \(\rho_3=5\), showing that the two
minimization parameters are distinct.

The prose, proof route, checker, and research workflow were developed by
OpenAI Codex agents under Atharva Vaidya's direction. This includes the
universal tensor lemma and obstruction identity, the size-fifteen census
and induction lift, the Petersen interaction dictionary and descent, the
two-terminal cleaning lemma, the orbit-reflecting \(K_{3,3}-e\) use, and
their checkers and internal hostile audits. The
disclosure in the paper must remain. Before public submission, the draft requires
line-by-line review by a human graph theorist, a clean independent census
rerun, bibliography audit, and a venue-specific authorship/disclosure
decision.
