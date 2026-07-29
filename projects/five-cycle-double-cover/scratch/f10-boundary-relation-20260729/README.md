# F10 full boundary relation

This package proves a complete positive closure theorem for the retained
288-vertex F10 six-pole used in the target-standard FiveCDC search.

The exact six-port \(D_5\) relation is all ordered duad words whose total
XOR is zero.  Consequently every finite network formed by connecting copies
of this pole to trivalent junctions has a FiveCDC.  The proof and the
loop/parallel-incidence conventions are in `HUMAN-PROOF.md`.

This is a computer-assisted finite boundary lemma followed by a human
all-size graph-theoretic argument.  It is not a resolution of the general
Five-Cycle Double Cover Conjecture, not a counterexample, and not an UNSAT
claim.

## Frozen facts

- pole: 288 vertices, 429 internal edges, 6 ports;
- ordered six-duad words: 1,000,000;
- XOR-zero words: 62,560;
- \(S_5\) coordinate orbits: 571;
- positive certified orbits: 571;
- negative orbits: 0;
- emergent \(S_6\) port symmetry;
- \(S_5\times S_6\) relation orbits: 11.

`boundary-witnesses.jsonl` supplies one complete 435-label witness for each
of the 571 coordinate orbits.  `verify_boundary_relation.py` is an
independently written standard-library checker.  It calls no SAT solver.

## Fast audit

```sh
python3 verify_boundary_relation.py \
  f10-atom.txt s5-representatives.json \
  boundary-witnesses.jsonl relation-summary.json
shasum -a 256 -c SHA256SUMS
```

## Full producer replay

The full replay requires Python 3, a C++20 compiler, and CaDiCaL headers and
static library in the Homebrew paths shown below:

```sh
python3 verify.py
```

The replay independently checks the frozen witnesses, regenerates the
62,560-word/571-orbit census, uses the hash-checked standalone
`f10-atom.txt`, compiles the boundary producer, reruns all 571 incremental
SAT queries, and directly checks the new positive witnesses.
The producer labels an UNSAT response `UNSAT_UNCERTIFIED`; this package
contains no such row.

## Files

- `f10-atom.txt`: standalone pole topology and ordered ports.
- `export_atom_text.py`: provenance utility used to export that topology
  from `search.candidate_domain.construct.karabas_f10`; it is not needed by
  the clean-clone replay.
- `generate_s5_representatives.py`: exhaustive boundary-orbit generator.
- `s5-representatives.json`: frozen 571 representatives.
- `enumerate_f10_boundary.cpp`: CaDiCaL positive-witness producer.
- `boundary-witnesses.jsonl`: frozen direct semantic certificates.
- `verify_boundary_relation.py`: independent certificate checker.
- `summarize_relation.py`, `relation-summary.json`: relation quotient.
- `HUMAN-PROOF.md`: checkable proof of the universal network theorem.
- `verify.py`: end-to-end replay.

## AI disclosure

OpenAI Codex agents designed the search, wrote the programs and exposition,
ran the computations, and checked the artifacts.  The mathematical claims
must be judged from the explicit proof and independently replayable
certificates, not from the authority of the AI system.
