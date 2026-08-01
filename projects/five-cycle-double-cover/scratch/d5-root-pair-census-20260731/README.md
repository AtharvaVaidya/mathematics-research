# Root-universality certificate through order 28

This directory certifies the following finite statement.

> Every simple cyclically 4-edge-connected cubic graph on at most 28
> vertices, and every pair of independent edges in that graph, has a
> five-coordinate D5 flow for which one of the ten two-coordinate factors
> has a circuit containing both prescribed edges.

The analytic Tait-colourable case is the prescribed-Tait-factor theorem in
`../../preprint-d5-surface-kempe/main.tex`.  The retained complete non-Tait
corpora contain 14,009 graphs and 10,689,351 independent root pairs through
order 28.  Three compact certificate files record 30,858 explicit D5 flows
that cover all those pairs.

This is a finite theorem, conditional on the documented Snarkhunter 2.0b
option semantics and source completeness in
`../../search/focused-theta-choice-through28-20260727/`.  It is not the
Five-Cycle Double Cover Conjecture and does not prove the unresolved rooted
theorem for arbitrary order.

The existential cutoff is **not new**.  Brinkmann, Goedgebeur, Hagglund,
and Markstrom, JCTB 103 (2013), Observation 6.6, proved the stronger finite
result that every circuit in every bridgeless cubic graph through order 34
belongs to a 5-CDC.  Combined with two-edge insertion, their result already
implies the present rooted statement (indeed through reduced order 32).
The contribution of this directory is the explicit 30,858-flow certificate,
its solver-independent semantic checker, and an independently reproducible
specialized computation of that known finite phenomenon.

## Fast independent check

From `projects/five-cycle-double-cover` run:

```sh
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-through24.json
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-order26.json.gz
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-order28.json.gz
python3 -B search/focused-theta-choice-through28-20260727/verify.py
```

The first program does not import the SAT generator.  It reparses every
graph6 row, checks every displayed edge label and vertex XOR directly, forms
all ten factors, and exhausts every independent edge pair.  The second
program audits the source hashes, generator logs, counts, and the earlier
two-implementation census attached to the same canonical corpora.

`run_all.sh` performs both checks and audits the frozen hashes in
`SHA256SUMS`.

## Regeneration

The positive certificate can be rebuilt with CaDiCaL installed at
`/opt/homebrew/bin/cadical`:

```sh
python3 -B scratch/d5-root-pair-census-20260731/build_compact_certificate.py \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order10.g6 \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order18.g6 \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order20.g6 \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order22.g6 \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order24.g6 \
  --output scratch/d5-root-pair-census-20260731/compact-witnesses-through24.json
python3 -B scratch/d5-root-pair-census-20260731/build_compact_certificate.py \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order26.g6 \
  --output scratch/d5-root-pair-census-20260731/compact-witnesses-order26.json.gz \
  --progress-every 250
python3 -B scratch/d5-root-pair-census-20260731/build_compact_certificate.py \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order28.g6 \
  --output scratch/d5-root-pair-census-20260731/compact-witnesses-order28.json.gz \
  --progress-every 1000
```

The builder greedily asks for a flow covering the first still-uncovered root
pair and then credits that flow with every pair connected in any of its ten
factors.  Solver output is not trusted by the final checker.

## Files

- `HUMAN-PROOF.md`: theorem, semantic proof, finite reduction, and limits.
- `compact-witnesses-through24.json`: 377 literal positive flows through 24.
- `compact-witnesses-order26.json.gz`: 2,710 literal positive flows.
- `compact-witnesses-order28.json.gz`: 27,771 literal positive flows.
- `check_compact_certificate.py`: independent standard-library checker.
- `build_compact_certificate.py`: deterministic certificate builder.
- `census.py`: the slower all-pairs SAT census used through order 24 as a
  cross-check.
- `run_all.sh`: one-command replay.
- `SHA256SUMS`: frozen artifact ledger.

## AI disclosure

OpenAI Codex agents developed the encodings, wrote the programs and prose,
ran the computations, and organized the certificate.  A human author
directed the project and publication.  These files are intended to expose
every finite claim to ordinary mathematical and computational checking; AI
output is not treated as authority.
