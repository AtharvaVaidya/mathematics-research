# Exact minimum-projection scan on the frozen strong-snark files

Date: 2026-07-29

Status: **exact finite evidence on the literal bundled graph6 rows**.  This
package makes no universal graph-theoretic claim and no Five-Cycle Double
Cover claim.

## Result

For every bundled graph, every minimum-cardinality extendable nonzero binary
projection is cleanable.

| order | graph6 rows | minimum-size profile | minimum extendable projections | per-graph range | uncleanable minima |
|---:|---:|:---|---:|:---|---:|
| 34 | 7 | `10:7` | 371 | 48–60 | 0 |
| 40 | 7,654 | `10:7654` | 433,359 | 16–85 | 0 |

Thus no counterexample was found in rows 0–6 of the order-34 input or rows
0–7,653 of the order-40 input.

## Exact input provenance

The inputs are literal copies of:

```text
projects/five-cycle-double-cover/search/strong_snarks/source/strongsnarks_34_5_cyc4.g6
projects/five-cycle-double-cover/search/strong_snarks/source/strongsnarks_40_5_cyc4.g6
```

They were copied from the worktree at Git `HEAD`
`58503186862885257053cf58d5388b19dfc31d88`; both files were unchanged from
the index.  Their Git blob IDs and SHA-256 digests are:

| input | Git blob | SHA-256 |
|:---|:---|:---|
| `strongsnarks_34_5_cyc4.g6` | `4bed72ba7e9cb4315dc5a9562198847cb0b86d45` | `2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f` |
| `strongsnarks_40_5_cyc4.g6` | `2c73f9ea0c6690bb39dbb4459c54b2037bf48777` | `61d7b01786e983084a6255bb0afe22a503cbb8645fe186b8a962d60609224e1d` |

The last commit touching the order-40 source was
`b38513624d0be7a874a6e2a873ae2834c20cae08` (2026-07-28,
“Prune lift routes and certify square frontier”).

The unconditional population claim of this package is about these exact
7,661 rows.  Any stronger interpretation of the source filenames or graph
class depends on their upstream provenance.

## Exact semantics

For a connected simple cubic graph \(G\), a nonzero binary cycle \(h\) is
called extendable when binary cycles \(p,q\) exist with

\[
                     E(G)-h \subseteq p\cup q.
\]

It is cleanable when such \(p,q\) can be chosen so that, for every component
\(W\) of the spanning subgraph with edge set \(E(G)-h\),

\[
                  |p\cap q\cap\delta(W)|=0\pmod 2.
\]

`scanner/reference/scan.cpp` is the audited linear-algebra scanner from the
repository.  For each fixed \(h,p\), it represents \(q\) in a binary cycle
basis.  Coverage fixes \(q_e=1\) on \((E-h)-p\); each component condition is
one further linear equation.  It enumerates every binary cycle by increasing
projection cardinality and tests every extendable projection at the first
extendable cardinality.

`scanner/exact_sat_scan.cpp` independently expresses the same semantics as
ordinary CNF:

- the three incident \(p\)-variables, and separately the \(q\)-variables,
  have even parity at every cubic vertex;
- each edge of \(E-h\) has the clause \(p_e\lor q_e\);
- a product variable represents \(p_e\land q_e\) on each component cut, and
  an XOR chain forces the cut-product parity to zero.

For each projection, clean SAT is tried first.  If it is UNSAT, extendability
without the component equations is tested.  SAT/UNSAT respectively gives an
exact witness decision; an extendable but clean-UNSAT projection is emitted
as `bad_minimum:1` and terminates the scan.

The SAT scanner enumerates every even edge set through weight 12 as a
vertex-disjoint union of simple circuits.  This is exhaustive because every
component of an even subgraph of a cubic graph is a circuit.  If no
extendable projection occurs through weight 12, it falls back to the complete
binary cycle space.  Every bundled graph reaches its first extendable level
at weight 10, so the exhaustive bounded branch decides every lower level and
every projection at the minimum level.

## Frozen results and independent cross-check

`results/strong34.jsonl` is the seven-row result.  The order-40 output is
partitioned only for four-process replay:

| result file | source row range | stored local row range |
|:---|:---|:---|
| `strong40-part0.jsonl` | 0–1,913 | 0–1,913 |
| `strong40-part1.jsonl` | 1,914–3,827 | 0–1,913 |
| `strong40-part2.jsonl` | 3,828–5,741 | 0–1,913 |
| `strong40-part3.jsonl` | 5,742–7,653 | 0–1,911 |

The concatenated order-40 result digest is
`97042fbc1b4f6079962d43582d7adb2cba4c1c5659c3bf5e049e88f3eca13d1e`.
The order-34 result followed by those four parts has digest
`becb7e4b648c000ec874509bccdf389df24f6f0d82bce2da49ba10d5b10d38e3`.

The independent SAT output was compared byte-for-byte with the reference
linear scanner on:

- all seven order-34 graphs; and
- order-40 source rows 0–4.

All fields matched: graph6 row, minimum size, number of minimum extendable
projections, and empty bad-mask list.  The limited order-40 cross-check scope
is stated explicitly; the full 7,654-row result was produced by the exact SAT
scanner.

## Replay

The frozen audit needs only Python 3:

```sh
cd scratch/minimum-projection-known-strong-snarks-20260729
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

This checks every embedded digest, every JSON graph6 row against its input
row, the zero-bad semantic assertions, the exact aggregates, and the
concatenated result digests.

The full exact scan needs a C++20 compiler and CaDiCaL headers/library.  The
recorded run used Apple clang 21.0.0 and CaDiCaL 3.0.1 on arm64 macOS.  With
the Homebrew paths used for the recorded run:

```sh
python3 verify.py --replay --jobs 4
```

Alternative CaDiCaL locations can be supplied explicitly:

```sh
python3 verify.py --replay --jobs 4 \
  --cadical-include /path/to/include \
  --cadical-library /path/to/libcadical.a
```

Reproduce the independent reference-scanner scope with:

```sh
python3 verify.py --reference-cross-check
```

The reference check takes roughly one minute on the recorded machine.  The
four-job full SAT replay took roughly four minutes while the machine was
otherwise idle enough to sustain four cores.

## AI-use disclosure

OpenAI Codex agents under human direction audited the exact definitions,
implemented the independent SAT encoding, ran the finite census, checked the
aggregates and hashes, and assembled this replay package.  The agent
cross-check is not independent human peer review.  The literal inputs,
scanner sources, frozen outputs, digests, and replay verifier are included so
the finite computation can be checked without trusting an AI-generated
summary.
