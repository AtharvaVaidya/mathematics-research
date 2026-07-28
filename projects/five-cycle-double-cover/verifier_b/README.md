# Independent verifier B

This directory is an independent, standard-library-only Go implementation of
the graph-premise checker, 5-CDC witness checker, certificate-oriented CNF
generator, and small exact search requested by the lab protocol. It was
designed from the root statement and encoding ledgers without reading
`verifier_a/`.

## Formats

A graph is an indexed finite undirected multigraph:

```text
p mgraph 1 2 2
e 0 0 1
e 1 0 1
```

Vertex IDs are `0,...,n-1`. Edge IDs must occur exactly once and are
`0,...,m-1`. `u == v` is a loop; distinct IDs with the same unordered
endpoints are parallel edges. Blank lines and `#` comments are allowed.

A candidate assignment contains all five membership bits:

```text
p 5cdc 1 2
a 0 1 1 0 0 0
a 1 1 1 0 0 0
```

The `check` command separately tests weight exactly two for every edge and
even incidence parity at every `(vertex,coordinate)`. A loop is omitted from
the computed XOR because its two identical incidences cancel. It still has a
five-bit row and must have weight exactly two. Parallel edges are never
coalesced.

## Equivalence with indexed 5-CDCs

Given a Boolean assignment, define
`C_i = { e : x[e,i] = 1 }`. The degree of a vertex in `(V,C_i)` is the sum,
with multiplicity, of `x[e,i]` over incidences at that vertex. Reducing this
integer degree modulo two gives exactly the verifier's vertex XOR. A loop
appears twice in that incidence sum and therefore contributes zero modulo
two. Different parallel edge IDs give different summands. Consequently the
five vertex XORs vanish if and only if every `C_i` is an even (Eulerian)
edge-subset. The weight-two row condition says independently that each edge
belongs to exactly two distinct indexed coordinates. Thus satisfying
assignments and indexed 5-CDCs map to one another by inverse constructions.
Empty coordinates and equal coordinate edge-sets are preserved because the
coordinates are an indexed five-tuple.

For the CNF, a clause constructed from a Boolean row contains the complement
of every literal in that row, so it is false on that row and true on every
other row. Blocking exactly all non-weight-two edge rows leaves precisely the
exact-two assignments. Blocking exactly all odd incidence rows leaves
precisely the even-parity assignments. The conjunction therefore has exactly
the satisfying assignments described above.

## Commands and status codes

```sh
go test ./...
go build -o verifier-b .
./verifier-b premises -graph graph.mg
./verifier-b check -graph graph.mg -assignment cover.5cdc
./verifier-b cnf -graph graph.mg -out graph.cnf
./verifier-b solve -graph graph.mg -witness found.5cdc
```

Parsing errors use exit status 2. `premises` uses status 1 for a graph with a
bridge. `check` uses status 1 unless both the graph is bridgeless and the
assignment is a valid 5-CDC. The solver uses status 1 only for `UNKNOWN`
(node limit reached); both `SAT` and exhaustive `UNSAT` use status 0 because
they are completed searches.

## CNF construction

DIMACS variable `5*e+i+1` is `x[e,i]`. The generator deliberately uses no
auxiliary variables:

* for each edge it blocks every one of the 22 five-bit rows whose Hamming
  weight is not two;
* for each `(vertex,coordinate)` it blocks every odd row on the distinct
  non-loop incident edge IDs.

The second construction emits `5 * 2^(d-1)` clauses at a vertex of non-loop
degree `d`. This exponential representation is intended for independently
checkable small certificates, not high-degree production search. The command
defaults to refusing `d > 20`; `-max-parity-degree` may raise the explicit
limit only through 62, but output size becomes impractical much earlier.
Loops create no parity literals.

An UNSAT proof must be produced by a certificate-producing external SAT
solver on this DIMACS and checked independently (for example, LRAT/DRAT).
This program emits the complete CNF but does not itself emit or check such a
proof.

## Exact backtracking

`solve` branches deterministically over the ten two-subsets of five
coordinates. It propagates the final unassigned non-loop edge at a vertex
from the current five-bit parity. It also applies sound coordinate-symmetry
breaking independently in each non-loop connected component. In particular,
at a cubic anchor vertex it fixes two incident labels to `{0,1}` and `{0,2}`;
the third is then forced. Loops are assigned `{0,1}` immediately.

With no `-max-nodes`, an `UNSAT` solver result means the finite search tree was
exhausted. **It is not a certificate and is never sufficient for a
counterexample claim.** The solver exists for deterministic small tests and
candidate discovery. A limited run returns `UNKNOWN`.

## Frozen build record

Recorded only after `go test ./...`, `go vet ./...`, and
`go test -race ./...` all passed:

```text
verifier-b 0.1.0
Go toolchain: go1.26.5 darwin/arm64
Build: go build -trimpath -o verifier-b .
Executable SHA256:
78416436bb35a758841e535fe2aff7b98d0f014f05e3f526a112f9b2b90328fe
```

The executable checksum is platform/toolchain specific. Rebuilding from the
same source with another Go release or target can legitimately produce a
different binary; the version string and source should be audited as well.
