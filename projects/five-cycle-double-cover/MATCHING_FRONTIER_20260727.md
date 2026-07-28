# Prescribed-root matching frontier, 2026-07-27

Status: **human-checkable scoped theorems and reductions / standard
all-singleton branch closed / exact finite census through order 28 /
prescribed-root singleton case open / Five-CDC unresolved**.

This index collects the current prescribed-root matching branch of the
Five-Cycle Double Cover research archive. It neither proves nor disproves
the standard Five-Cycle Double Cover Conjecture. It makes no orientable
Five-CDC claim.

## What is proved on paper

- [`docs/prescribed-root-matching-deficiency-frontier.md`](docs/prescribed-root-matching-deficiency-frontier.md)
  proves that deleting the endpoints of two independent edges from a
  finite 3-edge-connected loopless cubic graph leaves matching deficiency
  at most two. It also proves the exact theta-versus-dumbbell complement
  dichotomy and the cyclic-four tight-barrier restrictions.
- [`docs/boundary-eight-rotation-closure-frontier.md`](docs/boundary-eight-rotation-closure-frontier.md)
  proves the exact Gallai--Edmonds incidence form when the four deleted
  endpoints have boundary eight. It also gives a checked 18-vertex
  non-Tait countermodel to a weaker local rotation-closure lemma. That
  graph has a cyclic 3-edge-cut, so it does not refute the cyclically
  4-edge-connected target.
- [`docs/singleton-ge-tait-frontier.md`](docs/singleton-ge-tait-frontier.md)
  treats the canonical Gallai--Edmonds case in which every \(D\)-component
  is a singleton. It proves the target implication when the associated
  bipartite cross-graph \(J\) is disconnected and reduces every remaining
  counterexample or proof obligation to connected \(J\). The connected
  **prescribed-root theta** case is open.
- [`docs/root-insertion-two-factor-frontier.md`](docs/root-insertion-two-factor-frontier.md)
  proves a separate standard closure of the entire all-singleton branch.
  A degree count leaves exactly three edges inside the non-singleton
  shore.  An edge-prescribed perfect matching uses exactly one of them,
  so its complementary 2-factor has zero or two odd circuits.  The
  zero case is Tait-colourable; the two-odd-circuit case is covered by
  Huck--Kochol's 1995 theorem.  This argument is displayed in full and
  does not establish the stronger prescribed-root flow needed for the
  current gluing construction.
- The more developed marked-circuits and rooted-interface results are in
  [`preprint-rooted-four-cut/`](preprint-rooted-four-cut/), including the
  complete LaTeX source, 29-page PDF, audit, novelty assessment, checksums,
  and a prominent AI-use disclosure. Its strongest lower bound is scoped;
  it is not a Five-CDC resolution.

These notes display their assumptions and proofs in full. The finite
checkers are supporting evidence and countermodel verification, not
substitutes for the universal arguments.

## Exact finite evidence

[`docs/focused-theta-choice-census-frontier.md`](docs/focused-theta-choice-census-frontier.md)
and
[`search/focused-theta-choice-through28-20260727/`](search/focused-theta-choice-through28-20260727/)
classify every independent root pair in the retained complete
cyclically 4-edge-connected non-Tait simple cubic corpora at every even
order from 10 through 28:

| graphs | root pairs | perfect after deletion | deficiency-two with a theta choice | all dumbbell |
|---:|---:|---:|---:|---:|
| 14,009 | 10,689,351 | 10,567,773 | 121,578 | 0 |

This is a bounded two-implementation theorem over the recorded corpora.
Canonical source completeness and the meanings of the generator options
are inherited from the retained Snarkhunter 2.0b runs. The zero in the
last column is not a proof at arbitrary order.

The root-insertion note gives a second, more restrictive finite screen.
It starts with a perfect matching containing one root, inserts the other
root, and tests whether the resulting complement is bridgeless.  The C++
producer and a separately written Python replay agree on every order:

| deficient root pairs | local insertion witnesses | failures | all-singleton pairs | singleton failures |
|---:|---:|---:|---:|---:|
| 121,578 | 119,652 | 1,926 | 807 | 0 |

The unrestricted failures begin at order 24 and show that local insertion
is not a universal method.  The zero in the all-singleton column is exact
only for the retained finite corpora through order 28.  The reports,
shards, sources, and compact cross-checker are under `scratch/` and frozen
by `ROOT_INSERTION_SHA256SUMS`.

## Additional bounded rooted-cap screen

[`search/rooted-three-pole-c3-cap-frontier-through24-20260727/`](search/rooted-three-pole-c3-cap-frontier-through24-20260727/)
records a separate two-implementation screen of 10,824,084 proper roots
in 330,790 vertex-deleted three-poles from 13,901 retained triangle-free
3-connected non-Tait caps at orders 20, 22, and 24. Every signature is
nonempty and contains a normalized base pair. Together with the
human-checkable
[`docs/rooted-cap-triangle-induction.md`](docs/rooted-cap-triangle-induction.md),
this closes a bounded mixed cyclic-three branch through cap order 26.
The stronger current scoped lower bound remains order 30 by another route.

The compact Git package omits two byte-identical 34,355,648-byte
compressed transcripts. It retains both hashes, source corpora, logs,
statuses, summaries, verifier, compact report, and exact regeneration
instructions in `PUBLICATION-OMISSIONS.md`. This is finite evidence and
does not resolve Five-CDC.

## Reproduction

Run from `projects/five-cycle-double-cover/`:

```sh
python3 -B scratch/prescribed-root-matching-deficiency-checker.py
python3 -B scratch/rotation-closure-countermodel-checker.py
shasum -a 256 -c ROOT_INSERTION_SHA256SUMS
python3 -B scratch/check-root-insertion-published.py
(
  cd search/focused-theta-choice-through28-20260727
  shasum -a 256 -c SHA256SUMS
  python3 verify.py > /tmp/focused-theta-report.json
  cmp /tmp/focused-theta-report.json report.json
)
(
  cd search/rooted-three-pole-c3-cap-frontier-through24-20260727
  shasum -a 256 -c CHECKSUMS-PUBLISHED.sha256
  shasum -a 256 -c SOURCES.sha256
  python3 -m py_compile verify.py
  python3 -m json.tool report.json >/dev/null
)
```

The compact commands check the displayed finite countermodels, the
retained source identities, and all aggregate census fields. Full
re-execution of the independent C++ and Python classifiers is documented
in
[`search/focused-theta-choice-through28-20260727/REPRODUCING.md`](search/focused-theta-choice-through28-20260727/REPRODUCING.md).

## AI-use disclosure

OpenAI Codex agents, directed by Atharv Vaidya, developed or revised the
arguments, programs, computations, audits, and prose in this branch.
Agent cross-checks are not independent human verification or peer review.
A human graph theorist should independently check every proof and
attribution, rerun the finite verifiers, perform a specialist novelty
search, and assume normal scholarly responsibility before submission.
