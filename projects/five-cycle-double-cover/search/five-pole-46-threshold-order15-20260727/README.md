# Order-15 five-pole 46-state threshold screen

Status: **EXACT FINITE THRESHOLD SCREEN / UNIVERSAL THEOREM OPEN /
FIVE-CDC UNRESOLVED**.

This package exhausts all connected simple internally bridgeless graphs
with:

- 15 vertices;
- exactly five degree-two vertices, used as distinct terminals; and
- every other vertex of degree three.

Nauty `geng -Cq -d2 -D3 15 20:20` produces 69,243 canonical records.
For each record, `primary_classifier.cpp` encodes a \(D_5\)-label on every
proper edge and semiedge.  The ten allowed values are the two-subsets of
\([5]\), and the three incident labels at every completed cubic vertex
must xor to zero.  It tests representatives of the 62 ordered-boundary
orbits under the global \(S_5\) action.

The run uses `--stop-at 46`.  Every one of the 69,243 records reaches 46
satisfiable boundary orbits.  Consequently there is no order-15
counterexample to

> every connected internally bridgeless terminal-distinct cubic
> five-pole admits at least 46 of the 62 boundary orbits.

The retained masks contain the first 46 admitted orbits in classifier
order.  They are not full state relations and must not be used to count
exactly-46 poles.

## Trust boundary

`verify.py` is a standard-library structural replay.  It independently:

1. parses every graph6 record;
2. checks the degree sequence and absence of proper-edge bridges;
3. checks record uniqueness, threshold counts, and mask populations; and
4. regenerates the canonical corpus with `geng` and compares it exactly
   with the retained records.

With `--replay`, it also recompiles the classifier, reruns all eight
canonical shards, and demands byte-identical transcripts.

This is a reproducible bounded computation, not a proof of the universal
46-state assertion.  Positive SAT answers are ordinary checkable models,
but the package does not retain 3,185,178 individual models.  The
classifier and CaDiCaL are therefore inside the replay trust base.  No
UNSAT result about a candidate Five-CDC counterexample is asserted.

The path-extension lemma in
`../../docs/five-pole-realizability-frontier.md` shows that even universal
nonemptiness for this class would imply standard Five-CDC.  Thus the
46-state theorem is stronger than the original conjecture, not a settled
auxiliary lemma.

## Commands

Quick structural replay:

```sh
python3 search/five-pole-46-threshold-order15-20260727/verify.py
```

Full classifier replay (requires nauty, a C++17 compiler, and CaDiCaL):

```sh
python3 search/five-pole-46-threshold-order15-20260727/verify.py --replay
```

## AI-use disclosure

OpenAI Codex, under human direction, designed and ran the census, wrote
the verification material, and drafted this explanation.  The result has
not been independently peer reviewed.  Any publication should rerun the
artifacts, inspect the mathematical encoding, and disclose AI assistance
according to the venue's policy.
