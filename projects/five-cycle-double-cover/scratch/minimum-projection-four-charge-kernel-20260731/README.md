# Four-charge kernel counterexample

This package answers the bounded algebra question negatively.

An arbitrary two-support-circuit boundary state with exactly four
nonzero per-circuit charge blocks need not have a directly clean
extension.  The counterexample is smallest by number of complement
blocks: four blocks are impossible in the full tensor model, while the
displayed witness uses four charged blocks and one zero-charge block.

The compact literal witness has circuit lengths `16+4`, hence twenty
occurrences.  Its pair-tensor masks, in edge order

```text
01 02 03 04 12 13 14 23 24 34
```

are

```text
0 0 0 0 0 0 10 0 8 2
```

Only three rank-one gadgets are required.  `HUMAN-PROOF.md` gives a
two-case proof based on the relative translation $z\in\{0,1\}$.

## Files

- `HUMAN-PROOF.md` derives the charged tensor, proves the obstruction,
  explains exact scope, and records the descent and realization.
- `exact_abstract_sat.py` proves the four-block case UNSAT and the
  five-block case SAT.  The UNSAT proof is checked by CaDiCaL.
- `independent_boundary_verify.py` constructs the literal words without
  reading the SAT model and checks all 7,776 local-map assignments and
  all 32,256 integrable start pairs.
- `realization_verify.py` constructs a 38-vertex simple bridgeless cubic
  graph, verifies the displayed flow, checks 240 direct deletions and 96
  two-path Kempe deletions, and checks a proper 3-edge-colouring.
- `search_abstract_tensor.cpp` and the `abstract-n*-*.txt` files retain
  provenance from the preliminary deterministic hill climb.  The exact
  SAT result supersedes those nonzero local minima.
- `verification-output.txt` freezes the three exact checker outputs.
- `run_all.sh` replays the package and compares live output with the
  frozen transcript.

## Reproduction

From this directory:

```sh
./run_all.sh
```

CaDiCaL must be available as `cadical`, or set `CADICAL` to its path.
The expected final line is:

```text
PASS: four-charge counterexample, descent, and minimum-clean realization
```

## Exact scope

The pair-tensor model covers every arbitrary-occurrence two-circuit
boundary state, and every abstract tensor can be realized by zero-charge
four-occurrence gadgets.  The negative answer is therefore literal, not
an artifact of a relaxation.

The displayed cubic realization does not make the twenty-edge projection
globally minimum.  It is Tait-colourable, so its minimum extendable
projection is the empty, clean support.  Every component-map extension
also either deletes directly or reaches deletion by two complement
Kempe paths.  Nothing here is a FiveCDC counterexample.
