# Curated artifact inventory

This bundle was assembled on **2026-07-26** from the local laboratory at
`/Users/atharvavaidya/Documents/conjectures`.  The source workspace was
copied into a separate clean clone; it was not modified or committed.

## Included

- Both compiled research drafts and their complete LaTeX/BibTeX sources.
- The standalone computer-free four-mark proof.
- Current status, publication assessment, encoding proof, marked-cut
  reductions, and proof-obligation ledger.
- The latest connected eight-mark notes: Kempe transversality and marked
  girth plus its clean-room scope audit, the bichromatic signed code, the
  paired cyclic-cut condition, and the explicitly refuted cyclic-four
  separated-triple atom.
- The factor-quotient lifting theorem, literal local obstruction, terminal
  gap cut reduction, cyclic four- and six-cut frontier audits, and the
  complementary-quotient no-go theorem at equality.
- The explicit order-80 abstract incidence/rotation countermodel and two
  independent selector checkers.  This refutes an incidence-only
  intermediate implication, not five-CDC.
- The solver-free equality-\(88\) contradiction, the positive-surplus
  order-\(94\) bound and audits, and the abstract order-\(96\) incidence
  frontier checker.  Their exact conclusion is only the
  \(|V(G)|\ge96\) bound in the connected eight-mark extremal exact-zero
  size-four minimum-counterexample branch.
- The rooted four-mark cap-avoidance and bridge-elimination reductions,
  exact order-28 countermodel, frozen finite-screen summaries, and compact
  checkers.  The rooted theorem remains open.
- The exact exceptional four-pole rooted-packing algebra, frozen 640-word
  table, independent JavaScript verifier, and human-checkable reduction.
  Máčajová--Mazzuoccolo--Tabarelli Conjecture 3.7 remains open.
- The complete compact order-80 vertex-transitive control and all-\(C_{10}\)
  selector scan: source, saved result, 20 colouring words, and independent
  isomorphism audit.  No broad census file or compiled binary is committed.
- Complete compact packages for the 10-, 40-, and 46-vertex
  countermodels, including canonical graph encodings, construction data,
  human proofs, frozen results, and independently structured checkers.
- The complete compact order-24 separated-triple package, including the
  144-hit stream, 46 canonical marked isomorphism classes, exact scope
  report, SHA-256 manifest, and clean-room single and batch verifiers.
- The frozen \(H_4\) graph, compact CNFs, upper model, generators,
  checker sources, result summaries, and the original SHA-256 ledger.
- The native-XOR five-CDC encoder and its unit test.

The two compiled PDFs have SHA-256 digests:

```text
863f24bcad7780067e5c264e2253e673ea4b9d50e94f28a6cf6cf389cc20bcb0  output/pdf/two-connected-countermodels-five-cdc-preprint.pdf
7a88cd04139344babf371c6b949d26b50e6733ac8db5a6a495f842e4e706dafc  output/pdf/four-universally-separated-marks-preprint-20260726.pdf
```

The original source files for those PDFs have SHA-256 digests:

```text
f244876a123a0c0fe3ead39805ddd7c3aa18c7b7ed1e4762484f008052564ddc  preprint-fano-one-switch/main.tex
3c30aff3bc44a1163646eab8a41461d0859a44db04972be4a8810e0e0e2fa3dd  preprint-four-mark-core/main.tex
```

Package-local `SHA256SUMS` files freeze the countermodel and \(H_4\)
records.  The manifests are retained even when a large artifact named in
them is intentionally absent, so that a separately obtained artifact can
be authenticated.

## Deliberately omitted

The following were excluded from ordinary Git:

- LaTeX build auxiliaries (`.aux`, `.bbl`, `.blg`, `.log`, `.out`) and
  duplicate build-directory PDFs.
- Python caches, `.DS_Store`, temporary files, solver logs, and
  exploratory scratch output.
- Broad graph censuses and unrelated conjecture branches.
- The \(H_4\) projected-support corpus and full certificates:

| Local file | Size (bytes) | SHA-256 |
|---|---:|---|
| `search/h4-all-minimum-support-packing-20260726/supports.tsv` | 69,371,056 | `a7ede3be51d3b937bacf702d67aa51431192bcdea9b008bf835e25f82967b483` |
| `search/h4-all-minimum-support-packing-20260726/all-supports-blocked.cnf` | 108,556,195 | `12061f07adc80081c6c329b1882201a734d004445a1e84d493f9bd7cd3743741` |
| `search/h4-all-minimum-support-packing-20260726/packing-witnesses.bin` | 152,874,330 | `040fd474e7f3dfae0e530eed5579a4892bafcada1cbf0f85418393e3cbd297c3` |
| `search/h4-all-minimum-support-packing-20260726/all-supports-blocked.lrat` | 973,056,379 | `6bdeaff7fe3f37dca1c34c6653f0d1f1477490ffdd50f2d954fd88cc2c649934` |
| `search/h4-all-minimum-support-packing-20260726/flow-at-most-three-zero.lrat` | 12,538,449 | `10b5805e94ad9731bcd8abf7b4ed83964b583acfbd8e2a5f8f177ba83809f235` |

Those files remain in the source laboratory under the absolute local
paths shown above.  The frozen result summaries report successful
verification with C `lrat-check`, verified CakeML `cake_lpr`, and the
solver-free positive witness checker.  Because the large proofs are not
in this Git bundle, those reports are provenance records rather than a
standalone replay of the complete \(H_4\) theorem.

## Scope warning

The countermodel certificates refute intermediate strategies, not
five-CDC.  The \(H_4\) result concerns one fixed graph.  The four-mark
theorem closes one marked-core branch under additional hypotheses.
The retained 240-row rooted screen is a frozen result; this bundle does
not claim a fresh full replay of its consumer analysis.  A fresh replay
did regenerate all 13,824 producer rows and 240 target witnesses.  The
repair diagnostic in that frozen record names the historical generator
hash `637b2590...`, while the included source has hash `f81ab01c...`
after a later `--json` output option was added.  This is an explicit
source-hash mismatch, not a bit-for-bit replay claim.  A fresh run of the
current repair generator nevertheless reproduced the semantic result:
512 rows and no universally separated required-mark witness.  Together
these artifacts are research progress, not a resolution of the standard
or orientable five-cycle double cover conjecture.
