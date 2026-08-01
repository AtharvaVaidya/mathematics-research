# Independent semantic audit

Audit date: 2026-07-25

Audited against:

- the original five-cycle-double-cover mission statement;
- `docs/statement-ledger.md`;
- `FiveCDC/Encoding.lean`;
- `FiveCDC/Padding.lean`;
- `FiveCDC/D5Flow.lean`;
- the project `README.md`;
- the project and root reproducibility manifests.

No Lean definition was changed during this audit.

## Verdict

| Check | Result |
|---|---|
| Fixed-graph five-CDC semantics | **PASS** |
| SAT/XOR witness equivalence semantics | **PASS** |
| At-most-five padding semantics | **PASS** |
| Restricted ten-label `D₅` semantics | **PASS** |
| Absence of an accidental universal existence theorem | **PASS** |
| `lake build` | **PASS** |
| `formal/FiveCDC/SHA256SUMS` | **PASS** |
| Root `reproducibility/package-manifest.json` cross-reference | **PASS** |

Overall, the Lean definitions faithfully formalize the fixed-graph witness
predicate and its two equivalent encodings. The project remains deliberately
partial: it does not formalize bridgelessness, the universal conjecture, or
its exact negation. The semantic result is therefore **PASS within the
documented fixed-graph scope**, not a proof or disproof of the conjecture.

The root reproducibility manifest was refreshed during the audit and then
rechecked. Its Lean-project entries now agree with the current files:

```text
source manifest  eff6b65d1eaeab826b22b389a46dc97eb3ddcb7a28454db6260ab2286514ed59
Encoding.lean    1d10503dd36557e4c66f51d8e732681c37d30d1443f8c4a90741b20ccf1f5ac1
Padding.lean     65b3acecb8226fe26c870cbbe98aa854f18e7f4730b77c76739e35e9ed773da7
D5Flow.lean      4b27498c2d621a6371b0d6c1718e72a14eae8044c3a98d7ad9754c0059ea93c5
```

The earlier stale `Encoding.lean` hash finding is resolved.

## Statement-by-statement semantic comparison

### Finite undirected multigraph representation — PASS

`MultiGraph` has separate vertex and edge types and an endpoint pair

```lean
ends : Edge → Vertex × Vertex
```

for each edge. All definitions that enumerate vertices or edges require the
corresponding `Fintype` instances, so the formalized graphs are finite.

Although the endpoint pair is stored in an order, every semantic use in this
project goes through `incidenceMultiplicity`, which adds the two endpoint
tests symmetrically. Reversing an edge's stored endpoints therefore cannot
change degree, evenness, parity rows, `IsFiveCDC`, `ValidAssignment`, or
`IsD5Flow`. The ordered representation is redundant data, not a directed
orientation.

Scope gap: endpoint-reversal invariance is evident from the definitions but
is not stated as a Lean theorem.

### Loops — PASS

If `ends edge = (vertex, vertex)`, `incidenceMultiplicity` is `1 + 1 = 2`.
Consequently:

- a selected loop contributes two to the degree of its endpoint;
- it contributes zero modulo two to a parity row;
- it remains one distinct edge in `Finset Edge`;
- its five Boolean membership bits are still subject to `ExactTwo`.

Theorems `incidenceMultiplicity_loop` and `loop_incidence_cancels` explicitly
check the incidence side. This matches the statement ledger exactly.

### Parallel edges — PASS

Parallel edges are distinct values of `Edge`, so they occupy distinct
positions in finite sums, assignments, and edge sets even when their
endpoints agree. `MultiGraph.Parallel` also accepts reversed endpoint order,
and `parallel_pair_card` confirms that a parallel pair has two edge-set
members. No simple-graph quotient accidentally collapses them.

### Even edge-subsets — PASS

`EvenEdgeSet` states

```lean
∀ vertex, G.degree edges vertex % 2 = 0
```

for a spanning edge-subset. It imposes no connectivity, nonemptiness,
2-regularity, circuit decomposition, or orientation. Vertices of degree
four, six, and so on are permitted, and isolated vertices impose a vacuous
zero-degree condition. This is the intended “Eulerian edge-subset” or even
subgraph semantics.

### Five indexed coordinates — PASS

`FiveFamily Edge := Fin 5 → Finset Edge` is an indexed family, not a literal
set of sets. Therefore:

- all five positions exist;
- a position may be empty;
- two or more positions may contain equal edge sets;
- equal positions still count separately in coverage.

No definition requires a coordinate to be used, nonempty, or different from
another coordinate.

### Exact double coverage — PASS

`FamilyDoubleCovered` filters the five-element index set by membership of a
fixed edge and requires the resulting natural-number cardinality to equal
`2`. `ExactTwo` does the same with the Boolean row. This is integer
exact-two coverage, not parity-only coverage: weights zero and four are
rejected.

An edge belongs at most once to a given coordinate because coordinates are
`Finset Edge`; the formalization does not accidentally permit two traversals
of one edge inside one coordinate.

### `IsFiveCDC` quantifiers — PASS

For a fixed finite graph and fixed five-family,

```lean
IsFiveCDC G family := AllEven G family ∧ FamilyDoubleCovered family
```

has exactly the two intended conjuncts. `AllEven` quantifies over every slot
and `EvenEdgeSet` over every vertex; `FamilyDoubleCovered` quantifies over
every edge.

It is correct that `IsFiveCDC` itself contains no bridgelessness premise:
bridgelessness is a hypothesis of the open universal theorem, whereas this
predicate describes what constitutes a witness for a fixed graph.

### `ValidAssignment` and encoding equivalence — PASS

`Assignment Edge := Edge → Fin 5 → Bool` has one Boolean for every
edge/coordinate pair.

`ValidAssignment G x := ExactTwo x ∧ ParityRows G x` matches the mandatory
encoding:

- `ExactTwo` counts true entries in each five-bit edge row and requires
  exactly two;
- `AssignmentDegree` sums incidence multiplicity for selected edges;
- `ParityRows` requires every vertex/slot sum to be zero modulo two.

`encode` and `decode` are characteristic-function conversions. The project
proves both inverse laws, the degree identity, parity/evenness equivalence,
exact-two/double-coverage equivalence, and finally a genuine equivalence of
witness subtypes. This is stronger than mere equisatisfiability and has the
correct quantifier direction.

No CNF conversion or proof-certificate checker is formalized; the README
correctly lists this as out of scope.

### At-most-five padding — PASS

`HasAtMostFiveCDC` existentially chooses `k ≤ 5`, an indexed
`Fin k → Finset Edge` family, and an `IsKCDC` proof. This preserves repeated
members because positions remain indexed.

`padFamily` embeds the first `k` coordinates in `Fin 5` and assigns the empty
edge set to every remaining coordinate. The proved lemmas show that:

- empty padding preserves evenness;
- selected-slot cardinalities are preserved exactly;
- a `k`-cover pads to an `IsFiveCDC`;
- five coordinates are already an at-most-five family.

Thus `hasAtMostFiveCDC_iff_hasFiveCDC` faithfully justifies the convention
used in the statement ledger. The edge-free graph is also handled correctly,
including the possible `k = 0` witness.

### Ten-label `D₅` formulation — PASS

`D5Label` is a finite support in `Fin 5` with natural-number cardinality
exactly two, so it has precisely the intended weight-two semantics.
`D5Labeling` assigns one such label to every distinct edge.

`IsD5Flow` imposes coordinatewise incidence parity at every vertex. Loops
cancel through incidence multiplicity and parallel edges remain separate
summands. Characteristic-function conversion supplies exact-two
automatically. The subtype equivalences with `ValidAssignment` and
`IsFiveCDC` have the correct direction and do not assert that such a
labeling exists.

The name is documented as a restricted binary-flow formulation. It should
not be cited as a formalization of a conventional nowhere-zero group flow
without this qualification.

### No orientability conflation — PASS

There are no direction variables, directed balance conditions, or
opposite-direction requirements. The stored endpoint order is ignored by
the incidence semantics. The formalization is therefore the standard
unoriented problem only, as required.

### No accidental universal theorem — PASS

The project defines fixed-graph witness predicates and proves conversions
between witness types. It contains no theorem of the form

```lean
∀ G, Bridgeless G → HasFiveCDC G
```

and does not define `Bridgeless`. It also contains no `axiom`, `sorry`, or
`admit` in the project Lean sources. The README prominently says that the
project neither proves nor disproves the conjecture.

## Documented scope gaps

The following are absent and must not be inferred from the successful build:

1. A graph-theoretic definition of bridge or bridgelessness.
2. The universally quantified five-cycle-double-cover conjecture.
3. Its exact existential/UNSAT negation.
4. A formal counterexample or universal existence proof.
5. CNF or pseudo-Boolean translation and certificate checking.
6. Reductions to cubic graphs, snarks, or high cyclic connectivity.
7. Circuit-decomposition equivalence.
8. The orientable five-cycle-double-cover branch.
9. A theorem explicitly proving invariance under reversing stored endpoints.

Items 1–8 are already disclosed in the README, apart from the exact-negation
wording and circuit-decomposition item, which would be useful additions in a
future scope summary. None is a mismatch in the definitions actually claimed.

## Independent command results

Run from `formal/FiveCDC`:

```text
$ lake build
Build completed successfully (694 jobs).

$ shasum -a 256 -c SHA256SUMS
lean-toolchain: OK
lakefile.toml: OK
lake-manifest.json: OK
FiveCDC.lean: OK
FiveCDC/Encoding.lean: OK
FiveCDC/Padding.lean: OK
FiveCDC/D5Flow.lean: OK
README.md: OK
```

The project toolchain is pinned to Lean `v4.32.1`, and `lakefile.toml` pins
mathlib to commit `520045ab14e26149ee970e2e617ca04b09bde5d6`.

## Resolution-status guard

This audit certifies only semantic fidelity of the fixed-graph definitions
and their machine-checked witness equivalences. It supplies no proof of
universal existence and no counterexample. The correct project status remains
**PARTIAL STRUCTURAL PROGRESS**.
