# Verifier A: exact five-cycle-double-cover encoding

Status: frozen verifier candidate `1.0.0`. This package checks graph premises,
generates two SAT encodings, and validates SAT models directly against the
mathematical semantics. It does **not** by itself independently check an UNSAT
certificate.

## Witness format

The strict JSON schema is:

```json
{
  "format": "five-cdc-multigraph-v1",
  "vertices": 3,
  "edges": [
    {"id": 0, "u": 0, "v": 1},
    {"id": 1, "u": 0, "v": 2},
    {"id": 2, "u": 1, "v": 2}
  ]
}
```

`vertices` is a nonnegative integer and denotes the vertex set
`{0,...,vertices-1}`. Edge IDs must equal array positions. Endpoints must be in
range and ordered `u <= v`. Consequently loops and parallel edges have exact,
distinct indexed representations. Unknown keys, duplicate JSON keys, booleans
used as integers, missing IDs, and out-of-range endpoints are rejected.

`canonicalize` uses sorted JSON keys, no insignificant whitespace, ASCII, and
one final LF. This is canonical for an already indexed graph. It is deliberately
not a graph-isomorphism canonical labeling algorithm.

An empty graph and a graph with isolated vertices are permitted. "Bridgeless"
means that no edge is a bridge, so such graphs are vacuously bridgeless.
Connectivity is reported separately. The empty graph is reported as not
connected; a one-vertex graph is connected. A loop does not connect components
and is never a bridge. The bridge DFS skips a parent edge ID rather than a
parent vertex, so parallel edges are handled correctly.

## Mathematical semantics

For edge `e` and coordinate `i in {1,...,5}`, variable `x[e,i]` says that edge
`e` belongs to indexed Eulerian edge-subset `C_i`.

For each edge, exactly two of its five variables must be true. For each vertex
and coordinate, the selected degree must be even. A non-loop edge contributes
once at each endpoint. A loop contributes twice at its one endpoint, exactly
as in undirected degree, and therefore cancels from the equation over GF(2).

These constraints are equivalent to the intended definition:

* If the constraints hold, define `C_i={e:x[e,i]=1}`. Every vertex has even
  degree in each `C_i`, so every `C_i` is an Eulerian edge-subset (empty sets
  are allowed), and exact-two gives the double cover.
* Conversely, five such indexed Eulerian edge-subsets define the variables;
  Eulerian parity supplies every vertex equation and double coverage supplies
  exact-two.

No connectivity of an Eulerian edge-subset is imposed. This matches "even
subgraph"/Eulerian edge-subset, not the distinct simple-cycle interpretation.

## Encodings

The base variable map is deterministic:

```text
var(x[e,i]) = 5*e + i
```

where edge IDs are zero-based and `i` is one-based.

For exact-two on five variables, ordinary CNF contains:

* all 10 negative three-literal clauses (at most two);
* all 5 positive four-literal clauses (at least two).

The native XOR file uses CryptoMiniSat extended DIMACS. CryptoMiniSat defines
an `x` row to have XOR of its listed literals equal to true, so an even equation
`a XOR b XOR ... = false` is written `x -a b ... 0`. An empty parity equation
is tautological and omitted. Exact-two remains ordinary CNF.

The certificate-oriented ordinary CNF converts every nontrivial parity row to
a left-associated XOR-gate chain. For `z <-> (a XOR b)`, it emits:

```text
a b -z 0
-a -b -z 0
a -b z 0
-a b z 0
```

The final accumulator is forced false. A singleton equation is a negative unit
clause and an empty equation is omitted. Auxiliary variables are allocated
after all base variables in vertex-major, then coordinate-major, then chain
order, and every variable is documented in DIMACS comments. Each XOR gate has
a unique output for fixed inputs. Thus a base assignment satisfies the original
semantics iff it has (indeed, has exactly one) satisfying auxiliary extension.
This is projection-equivalence, stronger than mere equisatisfiability.

## CLI

Run from the repository root:

```sh
python3 -m verifier_a check-graph graph.json
python3 -m verifier_a canonicalize graph.json canonical.json
python3 -m verifier_a encode graph.json --cnf instance.cnf --xor instance.xor.cnf
python3 -m verifier_a check-model graph.json solver.model
python3 -m verifier_a prove-unsat graph.json \
  --cnf instance.cnf --proof proof.lrat --log cadical.log
python3 -m unittest discover -s verifier_a/tests -v
```

`check-graph` exits 0 for a valid bridgeless graph and 1 for a valid graph with
a bridge. Format errors exit 2. `encode` refuses graphs with bridges by default;
`--allow-nonbridgeless` is available for encoding tests.

`check-model` accepts DIMACS competition `s`/`v` syntax (or integer-only model
lines), requires a value for every base variable, rejects contradictions and
out-of-range variables, ignores auxiliary values, and checks the original
exact-two/parity semantics rather than trusting the CNF.

`prove-unsat` first regenerates the ordinary CNF and requires `cadical
--version` to equal `3.0.1`. It invokes text LRAT production with internal
CaDiCaL proof checking enabled. CaDiCaL is the proof producer; its internal
check is not independent verification. No LRAT checker is bundled or currently
detected in the lab environment. Therefore an UNSAT result and `.lrat` file
from this command are only certificate artifacts, not an accepted
counterexample, until a separately implemented LRAT checker validates them.

## Frozen files

`SHA256SUMS` records hashes after the unit suite passes. It intentionally does
not hash itself. Changing any hashed file creates a new verifier version and
requires rerunning all candidate checks.
