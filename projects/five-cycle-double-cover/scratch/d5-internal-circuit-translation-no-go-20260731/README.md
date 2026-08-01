# Internal-circuit translation cannot create a new external mode

Date: **2026-07-31**

Status: **human-checkable local lemma with exhaustive finite replay; not a
Five-Cycle Double Cover proof or disproof**.

This package isolates one failed route for the typed-cap problem.  Start with
a `D5`-flow whose factor circuit through the root and cap vertex is in internal
mode.  Modify that same circuit by adding one fixed even vector to every edge
label.  If the modified circuit is an external factor circuit, then it was
already an external factor circuit before the modification (possibly for a
different coordinate pair).

The result rules out only **uniform symmetric-difference translation of the
existing circuit** as a source of genuinely new external modes.  It does not
rule out sequences of component switches that change the circuit, and it does
not prove external port coverage, a double-star signature, rooted universality,
or FiveCDC.

## Files

- `HUMAN-PROOF.md` gives the complete six-case proof.
- `verify_translation_no_go.py` independently enumerates all normalized local
  translations and every possible set of labels on the internal circuit.
- `expected-output.txt` freezes the checker's output.
- `run_all.sh` checks the replay and the file hashes.
- `SHA256SUMS` freezes all substantive package files.

## Reproduction

Requirements: POSIX shell, Python 3, `diff`, and `shasum`.

```sh
./run_all.sh
```

The checker uses only the Python standard library.

## Scope and novelty caution

This is an elementary local obstruction and has not received a specialist
literature review.  It should be treated as a route delimiter inside an open
problem project, not as a standalone publishable resolution.  No external
novelty claim is made.

## AI-use disclosure

OpenAI Codex, under human direction, found the six-case normalization, wrote
the proof and checker, and assembled this package.  The argument is displayed
for line-by-line human verification.  Passing computation is not independent
human peer review.
