# Every Petersen--Foster edge elimination is root-feasible

Date: **2026-07-31**.

Status: **EXPLICIT FINITE POSITIVE CERTIFICATE / NOT A FIVECDC
RESOLUTION**.

This package checks all 1,335 edge eliminations of the 890-vertex
Petersen--Foster graph.  For every parent edge `e`, delete its two
endpoints and join the two remaining neighbours on each side.  The two
new edges are the roots `r,s` of a simple cubic graph on 888 vertices.

For every one of the 1,335 reduced instances, the retained certificate
displays a `D5` edge labelling for which the roots belong to one component
of

```text
Y_01 = {edge labels containing exactly one of coordinates 0 and 1}.
```

The two compressed JSON shards contain the literal labels, not merely SAT
status lines or model hashes.  `checker.py` reconstructs the parent and
every reduced graph without importing the producer.  It then verifies:

1. the parent graph identity, simplicity, cubicity, bridgelessness, and
   girth ten;
2. every elimination index, endpoint pair, artificial root, and reduced
   graph digest;
3. reduced simplicity, bridgelessness, and girth nine;
4. Hamming weight two for every displayed edge label;
5. zero XOR of the three labels at every reduced vertex; and
6. one `Y_01` component containing both roots, including the displayed
   transition path.

Run:

```sh
./run_all.sh
```

The construction and the short mathematical implication are written in
`HUMAN-PROOF.md`.

## Production provenance

The retained shards were produced from
`../d5-root-transition-sat-20260731/search.py` (source SHA-256
`6d935e12caaf5086d591c64cb171d1e00699d8531ba3f75d4f67555a8a05b14c`)
with Python 3.14.5 and CaDiCaL 3.0.1:

```sh
python3 ../d5-root-transition-sat-20260731/search.py \
  --petersen-foster --all-eliminations --start 0 --limit 668 \
  --include-labels --output /tmp/pf-root-transition-labels-0000-0667.json

python3 ../d5-root-transition-sat-20260731/search.py \
  --petersen-foster --all-eliminations --start 668 --limit 667 \
  --include-labels --output /tmp/pf-root-transition-labels-0668-1334.json
```

No random seed is used.  The stored `.json.gz` files are deterministic
`gzip -n -9` compressions of those outputs.  Search provenance is useful
for regeneration, but it is outside the final trust base: the standard-
library checker independently reconstructs every graph and validates every
literal label assignment.

No priority claim is made for this named-graph computation pending a
specialist literature search.

## Exact limitation

This is a finite positive control.  The Petersen--Foster graph is non-Tait
and has girth ten, but the three links incident with any substituted pole
form a cyclic three-edge cut.  It is not a candidate minimum counterexample
in the cyclically-four reduction, and
the package proves nothing about arbitrary graphs.  SAT found positive
models in every row, so no UNSAT certificate is involved.

## AI-use disclosure

OpenAI Codex agents, under human direction, designed and ran the search,
retained the literal witnesses, wrote the semantic replay, and drafted
this note.  Agent cross-checking is not independent human verification.
The mathematical claim rests on the displayed finite data and executable
checker; expert review is required before scholarly citation.
