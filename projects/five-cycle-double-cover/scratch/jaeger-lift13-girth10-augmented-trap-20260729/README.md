# Exact girth-10 augmented-trap witness

Status: **PARTIAL STRUCTURAL PROGRESS / FAILED LOCAL-PROOF ROUTE**, checked
2026-07-29.

This package gives an exact local obstruction to one auxiliary descent
strategy for the Five-Cycle Double Cover Conjecture. It is **not** a
counterexample to FiveCDC and does **not** resolve FiveCDC.

## Result

Use the 130-vertex, 195-edge cubic graph in
`../../artifacts/structured/graphs/lift13_petersen_girth10.json`, root
vertex 0, and order its edges by the graph6 convention

```text
(u,v) with u < v, sorted by (v,u).
```

The retained project metadata gives exact oddness zero: this graph is
Tait-colourable.  It is therefore a high-girth positive control, **not** a
snark-domain test.  None of the local-trap conclusions below should be
extrapolated to a smallest-counterexample class on the basis of girth alone.

The three root-spoke edge IDs are `(4,39,70)`. Delete the root and its
spokes. Number the remaining 192 internal edges in their induced order.
Their omitted-tree labels are the 192 entries in
`trap-directed-first-row.json`; equivalently, the three omitted masks are

```text
1902229645176197274522822155328007954167884912115462602784
1180262355923595958564565032730611406877382141243382314309
3194609734286887530748402235149047055057088391105189595802
```

Each class has size 64. Restoring one distinct root spoke to the complement
of each class gives three spanning trees. Their odd-kernel sizes are
`(67,68,67)`.

Under the exact seven-functional Jaeger/Fano evaluation used by the local
descent project, this state has

```text
profile = (20,24,10,18,10,16,2)
Psi     = (minimum profile entry, sum of kernel sizes) = (2,202)
parallel successful span flags = 0
```

There are `3 * 64 * 64 = 12,288` label swaps between two classes. Exactly
436 are reciprocal graphic-matroid basis exchanges. Exact evaluation of
all 436 shows:

- no neighbor has a lexicographically smaller `Psi`;
- no neighbor has a successful parallel span flag;
- the minimum active fundamental-circuit length is exactly 10.

Thus this is an **augmented trap** and it refutes the tentative universal
auxiliary lemma:

> Every augmented trap has an active reciprocal-exchange circuit of length
> at most 9.

It also supplies a sharp girth-10 obstruction to any proof of that precise
form. In fact, `fivecdc-witness.txt` supplies an explicit standard FiveCDC
of this very graph, independently checked by `verify_fivecdc_witness.py`.
Thus the graph is definitively **not** a counterexample to FiveCDC.

The trap is shallow. Of its 436 legal neighbors, 107 have equal `Psi` and
329 have higher `Psi`. Its exact shortest augmented escape distance is 2:

```text
start:
  profile (20,24,10,18,10,16,2), kernels (67,68,67), Psi (2,202), flags 0
swap 1:
  coordinates (0,1), local (113,136), full edges (116,139)
  profile (20,24,10,18,10,16,2), kernels (67,68,67), Psi (2,202), flags 0
swap 2:
  coordinates (0,1), local (109,169), full edges (112,172)
endpoint:
  profile (14,24,8,22,6,16,2), kernels (67,67,67), Psi (2,201), flags 0
```

The full first-neighborhood audit proves there is no distance-1 escape,
while the displayed legal two-swap path proves distance at most 2.

## Eight-trap sampled escape audit

The 500-step discovery run sampled eight augmented traps, at steps
`11,109,196,217,259,367,413,461`. The independent
`verify_all_eight_escapes.py` checker reconstructs all eight states and
exhausts their complete first neighborhoods: 98,304 candidate swaps and
3,220 legal neighbors in total. Every sampled trap has exact augmented
escape distance 2:

| Step | Start `Psi` | Equal neighbors | Endpoint `Psi` | Endpoint flags |
|---:|:---:|---:|:---:|---:|
| 11  | (2,202) | 107 | (2,201) | 0 |
| 109 | (2,204) | 110 | (2,203) | 0 |
| 196 | (2,203) | 82  | (2,202) | 0 |
| 217 | (2,205) | 120 | (0,205) | 3 |
| 259 | (2,200) | 109 | (0,201) | 3 |
| 367 | (2,198) | 117 | (0,198) | 3 |
| 413 | (2,208) | 101 | (2,207) | 0 |
| 461 | (2,203) | 115 | (0,205) | 3 |

This is exact for the eight displayed states but is **sampled evidence
only**, not an exhaustive theorem about all states of the graph or all
graphs. In particular it neither proves nor refutes a universal
radius-three escape claim.

## Literal length-10 circuit

For coordinates `(0,1)`, swap internal local positions `(49,73)`. On tree
coordinate 0, full edge 51 is inserted and active full edge 76 is removed.
The fundamental circuit is

```text
edge set:      (7,15,26,45,46,51,52,76,138,139)
cyclic vertices:
  (3,20,28,39,58,6,76,111,49,55,3)
cyclic edges:
  (7,15,26,52,51,76,139,138,46,45)
```

All edge IDs use the graph6 edge order above.

## Verification

From this directory:

```bash
python3 independent_verify.py
python3 verify_all_eight_escapes.py
python3 verify_fivecdc_witness.py
shasum -a 256 -c SHA256SUMS
```

`independent_verify.py` uses only the Python standard library. It was
written independently of the discovery program. It:

1. decodes the frozen graph6 record and cross-checks it against the
   structured graph artifact;
2. checks simplicity, cubicity, connectivity after deleting every set of
   at most two edges, and girth 10;
3. reconstructs all three trees, odd kernels, seven profile entries, and
   all 21 parallel span tests;
4. enumerates all 12,288 candidate swaps and reconstructs all 436 legal
   neighbors;
5. compares the complete reconstructed neighborhood to the frozen producer
   row; and
6. recomputes the complete active-circuit histogram and the literal
   length-10 circuit; and
7. verifies the literal shortest two-exchange escape.

An additional exhaustive metadata check verifies cyclic
4-edge-connectivity:

```bash
clang++ -O3 -std=c++20 check_cyclic4.cpp -o /tmp/check_cyclic4
/tmp/check_cyclic4 \
  ../../artifacts/structured/graphs/lift13_petersen_girth10.json
```

It examines all `C(195,3) = 1,216,865` edge triples. Exactly 130 triples
disconnect the graph, all isolating a single cubic vertex; zero separate
two cyclic components.

The heuristic search that found the state is not an exhaustive search of
all states. The local trap assertion for the displayed state *is*
exhaustive.

The FiveCDC witness labels each structured-JSON edge by a two-character
subset of `01234`. The checker verifies that every label has size two and
that, for each coordinate, every vertex has even selected degree. The five
Eulerian edge-set sizes are `(64,82,94,71,79)`.

## Discovery provenance

The state was found with seed 101, root 0, and 500 trap-directed heuristic
steps. The frozen 500-step run contained 8 exact augmented traps and 2
old-objective-only traps among 499 distinct sampled states. The first
augmented trap occurred at step 11 and is the row included here.

The current experimental producer is
`../search_jaeger_high_girth_star_samples.cpp`; the frozen witness and
independent verifier, rather than the heuristic trajectory, are the basis
of the mathematical claim above.

## AI-use disclosure

The construction search, program development, exact computations, audits,
and exposition were performed with OpenAI Codex agents under human
direction. The claims are deliberately limited to what the included exact
checker verifies. Any public write-up should retain this disclosure and
should not describe this auxiliary obstruction as a resolution of
FiveCDC.
