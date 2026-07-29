# Counterexample to minimum Fano-projection selection

This directory contains a concise standalone preprint about the verified
162-vertex strict-lock construction.

The paper proves that a unique cardinality-minimum extendable binary
projection of a nowhere-zero \(\mathbb F_2^3\)-flow need not be
cleanable. It does **not** disprove the Five-Cycle Double Cover
Conjecture: the same graph has explicit five-cover certificates.

## Deterministic build

From this directory:

```sh
SOURCE_DATE_EPOCH=1785283200 tectonic main.tex
```

The build uses Tectonic 0.16.0 or a compatible release. Repeating the
command with the same sources and epoch should reproduce `main.pdf`
byte-for-byte in the audited environment.

## Verification sources

The preprint summarizes two frozen packages:

- `../scratch/minimum-projection-strict-parity-lock-20260729/`
- `../scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/`

Replay them from the repository root:

```sh
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-parity-lock-20260729/verify.py
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/verify.py
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/independent_audit.py
```

See `HUMAN-REVIEW.md` for the proof and artifact checklist and
`NOVELTY-ASSESSMENT.md` for the deliberately provisional literature
assessment. `VISUAL-QA.md` records the PDF render inspection.

Verify the release hashes with:

```sh
shasum -a 256 -c SHA256SUMS
```

## Disclosure

OpenAI Codex agents, directed by Atharva Vaidya, developed the route,
found and minimized the strict lock, wrote checkers, generated
certificates, performed cross-audits, and drafted the manuscript. The
result has not received independent human peer review. No
literature-wide novelty or priority claim is made.
