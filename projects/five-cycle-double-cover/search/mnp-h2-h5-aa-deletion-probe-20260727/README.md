# Prescribed-equal-label theorem for the reconstructed \(H_2,\ldots,H_5\)

Status: **FINITE EXPLICIT POSITIVE CERTIFICATE / ALL 97,608 INDEPENDENT
EDGE PAIRS / NOT A FIVE-CDC RESOLUTION**.

The retained graphs are the reconstructed high-flow-resistance snarks
\(H_2,H_3,H_4,H_5\) of Mattiolo, Negrini, and Pagani.  Their source
packages prove the graph premises and certify flow resistances
\(2,3,4,5\), respectively.  All four graphs were already known inside
this project to have standard five-cycle double covers.

This package proves the stronger finite prescribed-pair statement:

> For every independent pair of edges \(e,f\) in each retained graph
> \(H_2,H_3,H_4,H_5\), there is a fixed-five \(D_5\)-labelling in which
> \(e\) and \(f\) receive the same label.

The exact totals are:

| graph | vertices | edges | independent pairs | retained labellings |
|---|---:|---:|---:|---:|
| \(H_2\) | 82 | 123 | 7,257 | 79 |
| \(H_3\) | 122 | 183 | 16,287 | 92 |
| \(H_4\) | 162 | 243 | 28,917 | 103 |
| \(H_5\) | 202 | 303 | 45,147 | 120 |
| total | 568 | 852 | 97,608 | 394 |

Here
\[
 D_5=\binom{[5]}2
\]
is represented by the ten weight-two binary vectors.  A labelling assigns
one member of \(D_5\) to every edge and requires the xor of the three
incident labels to vanish at every cubic vertex.  Reading coordinate \(i\)
as membership in the \(i\)-th Eulerian subgraph gives five Eulerian
edge-subsets covering each edge exactly twice.

## Why this is exactly the \(AA\) boundary state

Let \(e=ab\) and \(f=cd\) be independent.  Cutting them produces four
distinct semiedges at \(a,b,c,d\).  If a \(D_5\)-labelling of the capped
graph gives both edges one label \(A\), the four new semiedges all have
label \(A\), so the deletion four-pole realizes boundary type \(AA\).
Conversely, an \(AA\) labelling caps back by restoring \(e,f\) with label
\(A\).  Vertex parity is unchanged in both directions.

Because the global \(S_5\) action is transitive on \(D_5\), asking for an
unspecified common label is equivalent to fixing both prescribed edges to
the representative `0011`.  This is the assumption used by
`cap_equal_label_cadical.cpp`.

## Explicit certificate compression

Running a fresh boundary solver on all 97,608 deletion poles is needlessly
expensive.  The retained generator instead builds one incremental CaDiCaL
instance per capped graph.  Whenever an independent pair remains
uncovered, it fixes that pair to `0011`, solves, and records the complete
edge labelling.  One labelling simultaneously certifies every independent
pair whose two edges receive any common label.  Greedy repetition covers
all pairs with only 394 explicit labellings.

`artifacts/equal-label-cover.tsv` contains every complete labelling.  Each
row records:

```text
source graph index
certificate index
pivot edge 1
pivot edge 2
newly covered pair count
one decimal D5-label index for every edge
```

The certificate is positive and directly checkable; no trust in the SAT
solver is needed after the models have been emitted.

## Independent replay

`verify.py` imports no solver code.  It:

1. checks the four graph6 identities;
2. independently checks cubicity, connectedness, and bridgelessness;
3. reconstructs every independent edge pair in graph6 edge order;
4. checks every displayed edge label is in \(D_5\);
5. checks the xor equation at every vertex;
6. checks each pivot has the fixed common label; and
7. recomputes the greedy coverage until all 97,608 pairs are covered.

Replay with:

```sh
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
```

This finite theorem is evidence for the focused prescribed-\(AA\) cap
hypothesis, even on graphs of growing flow resistance.  It is not a theorem
for arbitrary cyclically highly connected snarks, does not classify the
other nine boundary states, and does not resolve the Five-Cycle Double
Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the incremental
prescribed-pair test, generated the 394 labellings, wrote the independent
checker, and drafted this note.  The graph reconstruction and cited family
are prior work recorded in the source packages.  Every new finite claim in
this package is represented by explicit edge labellings checkable without
trusting an AI system or SAT solver.
