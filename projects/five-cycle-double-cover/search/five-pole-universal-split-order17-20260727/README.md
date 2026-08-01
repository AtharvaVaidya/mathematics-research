# Order-17 universal split-state census

Status: **EXACT FINITE POSITIVE CENSUS / ROOTED THEOREM OPEN /
FIVECDC UNRESOLVED**.

This package records the complete order-17 screen of connected simple
internally bridgeless terminal-distinct cubic five-pole cores.  The
canonical source is

```sh
geng -Cq -d2 -D3 17 23:23
```

split into the eight canonical residue shards `0/8` through `7/8`.
There are 1,109,844 cores.

For each core, `primary_census.cpp` tests all ten choices of the two
doubled boundary positions.  The selected positions receive label `01`;
the other three receive `23,24,34`.  Every one of the 11,098,440 SAT
queries succeeded.

This is called a “universal split state” only within each tested pole:
all ten terminal-pair choices work.  It is not a proof that the state
exists for every five-pole of arbitrary order.

## Closed-graph interpretation

The human proof in
`../../scratch/vertex-edge-universal-split-state-frontier.md` shows that
this boundary state is equivalent to the following rooted property.  For
a cubic graph, a vertex \(v\), and an edge \(e\) whose endpoints lie
outside \(N[v]\), there is a standard 5-CDC in which the two members
containing \(e\) both avoid \(v\).

The same note gives a displayed proof of the equivalent prescribed
matching certificate: an exact-zero matching containing \(e\) and
avoiding \(\delta(v)\), an \(\mathbb F_2^2\)-flow with that exact zero
set, and two edge-disjoint boundary \(T\)-joins that both avoid
\(\delta(v)\).

That rooted statement is stronger than ordinary FiveCDC and remains
open.

## Trust boundary

`verify.py` is independently structured and uses only the Python standard
library.  It:

1. checks all retained summary hashes and totals;
2. reconstructs the local \(D_5\) split-state algebra;
3. regenerates all eight canonical `geng` shards;
4. parses every graph6 record independently;
5. checks uniqueness, the five-degree-two/twelve-degree-three profile,
   connectedness, and absence of proper-edge bridges; and
6. compares every shard count and byte-stream SHA-256 with `report.json`.

The retained summaries are aggregate positive SAT results.  Individual
models were not retained, so the primary C++ encoder and CaDiCaL remain
inside the SAT trust base.  The optional `--replay` mode recompiles the
primary program and demands byte-identical summaries, but it is still not
an independently implemented SAT solver.

No UNSAT claim about a FiveCDC candidate is made.

## Commands

Independent structural and corpus replay:

```sh
python3 search/five-pole-universal-split-order17-20260727/verify.py
```

Optional byte-identical SAT replay, requiring nauty, C++17, and CaDiCaL:

```sh
python3 search/five-pole-universal-split-order17-20260727/verify.py \
  --replay
```

Independent local-algebra audit:

```sh
python3 scratch/audit_vertex_edge_split_state_equivalence.py \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-0.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-1.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-2.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-3.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-4.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-5.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-6.txt \
  --census-output search/five-pole-universal-split-order17-20260727/results/order17-shard-7.txt
```

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, formulated the rooted
branch, wrote the code and prose, and ran or assisted the computations.
Agent cross-checks are not independent human verification or peer review.
The mathematical equivalences are displayed for human checking, and the
finite census is separated from them with its exact trust boundary.
