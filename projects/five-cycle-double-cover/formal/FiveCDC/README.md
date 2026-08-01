# Lean semantic formalization for five-cycle double covers

Status: **PARTIAL STRUCTURAL PROGRESS**.  This project does not prove or
disprove the five-cycle double cover conjecture.

The file `FiveCDC/Encoding.lean` defines:

- finite undirected multigraph data by finite vertex and edge types plus two
  endpoints per edge;
- incidence multiplicity, including multiplicity two for loops and distinct
  values for parallel edges;
- Eulerian/even edge-subsets;
- five indexed edge-subsets, exact double coverage, and the fixed-graph
  five-CDC predicate;
- the exact-two Boolean rows and incidence-parity rows of the SAT/XOR model;
- inverse `encode` and `decode` maps;
- a proved equivalence between valid assignments and five-CDCs;
- explicit loop and parallel-edge lemmas.
- a `Fin k` definition of an at-most-five indexed cover and a proof that
  padding with empty edge sets is equivalent to using five coordinates.
- the ten-label `D₅` restricted binary-flow formulation and an equivalence
  between its conserved labelings and five-CDC witnesses.

The following items are not formalized:

- graph-theoretic bridgelessness;
- the open universal existence claim;
- reductions to cubic graphs or snarks;
- CNF conversion and proof-certificate checking;
- orientable five-cycle double covers;
- the local cubic-triangle classification.

None is needed for the fixed-graph semantic equivalences proved here.

Build from this directory:

```sh
lake update
lake build
shasum -a 256 -c SHA256SUMS
```

Pinned inputs:

- Lean `v4.32.1`
- mathlib commit `520045ab14e26149ee970e2e617ca04b09bde5d6`
