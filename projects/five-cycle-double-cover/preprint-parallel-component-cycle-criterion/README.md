# Parallel component-cycle criterion preprint

Status: **provisional AI-assisted research draft for independent human
verification**.

This standalone manuscript proves two human-checkable statements for finite
connected loopless cubic multigraphs:

1. a fixed parallel six-point one-hole system is soluble exactly when its
   component defect belongs to an explicit span of outside-circuit switch
   vectors; and
2. existentially choosing the flow, plane, and direction in that criterion
   is equivalent to the existence of a standard five-cycle double cover.

The second statement is an exact reformulation, not a universal existence
proof. The Five-Cycle Double Cover Conjecture remains open, and the orientable
variant is not considered.

The paper builds on the companion draft
`../preprint-six-point-one-hole-affine/` and compares the new criterion
directly with Hušek and Šámal, *Exponentially Many Circuit Double Covers*,
arXiv:2607.24724v1, especially Theorem 3.16. The provisional novelty language
in the paper makes no priority claim.

## Fixed-flow audit

Run the structurally independent, standard-library-only checker:

```sh
python3 verify.py --output RESULT.json
```

It generates all 900 `GL(3,2)`-orbits of nowhere-zero flows on the frozen
rigid 12-vertex graph and compares 18,900 original affine decisions with the
component-span criterion. It also checks:

- the scalar local affine rows recover each literal allowed-potential set
  exactly;
- the defect is independent of the chosen outside value; and
- the per-circuit boundary-vector identity and literal whole-circuit flow
  switch update.

This implementation is independent of the discovery implementation in
structure, but both are AI-authored. It is not independent human review.

## Through-order-16 selector census

The separate exact producer package is:

```text
../output/six-point-parallel-selector-through16/
```

It contains the graph corpus, 30 MB JSONL census, result, exact C++ sources,
self-contained reproduction driver, and manifest. Check it from that
directory:

```sh
shasum -a 256 -c SHA256SUMS
```

The frozen manifest has SHA-256:

```text
e398550c6277476770c8b017dd4bbcc57b5b2bd104eb4993afbe143cd5eec850
```

The central frozen hashes are:

```text
901acfc0b09951e2ac5c76f03a43b7aa2ff318778b238ed663a8772819af9701  graphs.g6
6622f32547582a666de0ca8d0516db106cd528094c650a14a89fa4e1f6d21693  census.jsonl
51dfedaac06d9828e7bdbc0accf4aec9c2d252d318807bdfad770050ee1cb99f  RESULT.json
```

To rerun the complete census into a new sibling directory (requires nauty
`geng`, CaDiCaL 3.0.1, and Homebrew paths matching the driver):

```sh
python3 ../output/six-point-parallel-selector-through16/reproduce.py \
  --workers 4
```

The producer found a parallel-odd witness in all 50,894 feasible rooted star
fibres of all 4,461 simple biconnected cubic graphs through order 16. The
producer and semantic checks are AI-authored, and the exhaustive run has no
independently checked SAT proof certificate. This is finite evidence only.

## Build and render

Build deterministically:

```sh
SOURCE_DATE_EPOCH=1785283200 tectonic main.tex
```

Render for visual review:

```sh
mkdir -p tmp/render
pdftoppm -png -r 150 main.pdf tmp/render/page
```

Finally verify this directory:

```sh
shasum -a 256 -c SHA256SUMS
```

The PDF was rendered page by page and visually inspected before freezing.

## AI-use disclosure

OpenAI Codex agents using GPT-5-series models, under Atharva Vaidya's
direction, discovered the formulation, derived the proof, wrote the
implementations, performed the computations, conducted the cited-paper
comparison, and drafted the manuscript and this README. No independent human
proof check, computational reimplementation, peer review, or priority review
is claimed. A human author must perform those checks and accept scholarly
responsibility before submission.
