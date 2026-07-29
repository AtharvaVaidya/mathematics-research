# Full F10 boundary relation preprint

Status: **AI-assisted research draft for independent human verification**.

This standalone note proves a computer-assisted positive boundary theorem
for one frozen 288-vertex six-pole, then gives a human all-size proof that
every trivalent network of copies of the pole has a five-cycle double cover.
It does not resolve the general Five-Cycle Double Cover Conjecture, and its
novelty assessment is provisional.

The complete certificate package is in:

```text
../scratch/f10-boundary-relation-20260729/
```

Run the fast independent audit from that directory:

```sh
shasum -a 256 -c SHA256SUMS
python3 verify_boundary_relation.py \
  f10-atom.txt s5-representatives.json \
  boundary-witnesses.jsonl relation-summary.json
```

Run the full producer replay, with the compiler and CaDiCaL dependencies
described in the package README:

```sh
python3 verify.py
```

Build this manuscript deterministically from its own directory:

```sh
SOURCE_DATE_EPOCH=1785283200 tectonic main.tex
```

The PDF must be rendered page by page and visually checked after every
material source change.  The source contains a prominent disclosure of the
material contributions made by OpenAI Codex agents.  Implementation
independence is not independent human review.
