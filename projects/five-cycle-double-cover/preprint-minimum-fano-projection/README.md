# Minimum extendable Fano projections

This directory contains a short AI-assisted working preprint about a
minimum-support route to the standard five-cycle double cover conjecture.

**Resolution status:** FiveCDC remains open. The paper proves a
human-checkable exchange theorem and a complete minimum-projection theorem
through support size seven, reports exact finite censuses, and states the
remaining universal selection principle as an explicit conjecture. It
claims neither a proof nor a counterexample.

Build from this directory with:

```sh
tectonic main.tex
```

Run the exhaustive order-18 checker from the project root with:

```sh
python3 scratch/check_husek_samal_minimum_projection_frontier.py \
  --order 18
```

The checker requires:

- Python 3;
- nauty `geng` on `PATH`; and
- `scratch/search_fano_all_bad_projection_subspaces.py`.

It has no SAT-solver, network, or nonstandard Python-package dependency.
The expected canonical hard-record SHA-256 is:

```text
82b01cc2f01d4f50f7745f4bdb1b3dc46ade798d452a9d4f11d4a91d738a7834
```

Replay the dependency-free case split and explicit low-flow repairs for
the size-at-most-five theorem with:

```sh
python3 scratch/minimum-projection-size5-theorem-20260729/verify.py
```

Replay the cumulative exact boundary theorem through size seven with:

```sh
python3 scratch/minimum-projection-through7-cleanability-20260729/verify.py
```

The size-six/seven proof combines exhaustive affine boundary
classification with a displayed telescoping span theorem. Every boundary
state not eliminated by a componentwise \(\mathrm{GL}(2,2)\) Tait repair
has exactly two complement components, and one valid line switch cleans it.

Run the expanded exact replay with:

```sh
python3 scratch/minimum-projection-census-through28-20260729/verify_summary.py
```

It checks 14,009 frozen cyclically-4 non-Tait records through order 28
and a separate 12,892-row hard order-22 source. All 147,539 minimum
extendable projections in those literal files are cleanable. The broader
population completeness statements are inherited from the documented
upstream generation packages.

The retained order-34/order-40 strong-snark scan is:

```sh
python3 scratch/minimum-projection-known-strong-snarks-20260729/verify.py
```

It checks frozen outputs for 7,661 literal graph6 rows and 433,730 minimum
projections, all cleanable and all of minimum size ten. The bundled package
contains its exact SAT scanner and a second linear-algebra implementation;
the latter cross-checks all seven order-34 rows and the first five order-40
rows. Population completeness beyond the literal files is inherited.

The certified 130-vertex stress test is:

```sh
python3 search/minimum-projection-n130-20260729/verify.py
```

It proves minimum extendable-projection size 42, exhausts exactly 11,264
minimum supports, and checks that all are cleanable. Two LRAT certificates
establish the lower bound and enumeration completeness. The same graph has
minimum nonzero Fano value-class size \(\rho_3=5\), showing that the two
minimization parameters are distinct.

The prose, proof route, checker, and research workflow were developed by
OpenAI Codex agents under Atharva Vaidya's direction. The disclosure in the
paper must remain. Before public submission, the draft requires
line-by-line review by a human graph theorist, a clean independent census
rerun, bibliography audit, and a venue-specific authorship/disclosure
decision.
