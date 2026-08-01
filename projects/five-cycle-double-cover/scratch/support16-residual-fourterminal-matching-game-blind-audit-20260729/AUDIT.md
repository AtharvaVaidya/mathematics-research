# Blind audit of the support-16 four-terminal matching game

Date: **2026-07-29**

Status: **THE STATED EIGHT-STATE ONE-ROUND DICHOTOMY PASSES / ONE
NON-MATHEMATICAL CERTIFICATE-FIELD CLARIFICATION RECOMMENDED / NOT A
FIVE-CYCLE-DOUBLE-COVER OR MINIMUM-PROJECTION RESULT**.

This audit was written without importing candidate code.  The checker reads
only the published residual table and the frozen candidate certificate as
data.  It independently implements the boundary algebra, component maps,
matching game, graph construction, graph checks, path extraction, and Tait
colouring search.

## Verdict

No mathematical gap was found in the stated bounded result:

> Of the eight published direct residuals for
> `01010123|01012302`, six satisfy the one-colour-pair,
> matching-observed one-round reduction for every abstract componentwise
> terminal matching.  Each of the two remaining states has one adverse
> matching for each colour pair, and its three adverse matchings occur
> simultaneously in a literal 42-vertex simple cubic bridgeless graph.

Both realizing graphs are Tait-colourable.  They obstruct only this
one-round descent rule; they are neither FiveCDC counterexamples nor
globally minimum-projection obstructions.

The only publication note is nomenclature: the candidate certificate field
`reachable_transition_count` counts distinct transitions inspected before
the search stops at the first rescue in each matching row.  It is not the
number of all mathematically reachable transitions.  No proof claim uses
this field.  Before publication it should be renamed
`searched_transition_count` or its early-stopping meaning should be stated.

## 1. Reconstructing the eight source states

The audit reads
`../unrestricted-support16-interaction-frontier-20260729/residuals.tsv`,
whose SHA-256 is

```text
2c9cca62de4ce06bca6ababfbfced4878133b22c6f52d55417fd4e9afa28096e
```

It independently differentiates the two cyclic words:

```text
word        01010123|01012302
derivative  31111131|21113132
```

For every TSV row it reconstructs the block profile and per-circuit
occurrence matrix, verifies xor charge zero on every block, checks that
there is no interaction loop and that a higher-occurrence block is present,
and exhausts all \(6^4=1296\) normalized component-map tuples.  The eight
reconstructions are:

| partition | profile | per-circuit matrix | feasible/clean/delete |
|---|---|---|---:|
| `0001234000314200` | `8+2+2+2+2` | `4/4,1/1,1/1,1/1,1/1` | `320/0/0` |
| `0001234003144422` | `5+4+3+2+2` | `4/1,1/1,1/2,1/1,1/3` | `320/0/0` |
| `0012344041300022` | `6+3+3+2+2` | `3/3,1/1,1/2,1/1,2/1` | `320/0/0` |
| `0012344044130244` | `6+4+2+2+2` | `3/1,1/1,1/1,1/1,2/4` | `320/0/0` |
| `0012344400314200` | `6+4+2+2+2` | `2/4,1/1,1/1,1/1,3/1` | `320/0/0` |
| `0012344403144422` | `6+3+3+2+2` | `2/1,1/1,1/2,1/1,3/3` | `320/0/0` |
| `0123444441300022` | `5+4+3+2+2` | `1/3,1/1,1/2,1/1,4/1` | `320/0/0` |
| `0123444444130244` | `8+2+2+2+2` | `1/1,1/1,1/1,1/1,4/4` | `320/0/0` |

This audit reconstructs the eight rows from the published data; it does not
repeat the sibling package's full 8,046,330-partition census that produced
the residual table.

## 2. Quantifiers and legal moves

The verified quantifier order is

\[
 \exists P\quad
 \forall (M_W(P))_W\quad
 \exists\,\varnothing\ne S(M)\subseteq\mathop{\dot\bigcup}_W M_W(P)
\]

such that the selected path set is circuit-closed and, after observing the
matching and selecting the paths, some component maps and relative circuit
translation clean or delete.

Thus:

1. one colour pair \(P\) is chosen before Nature's matching tuple;
2. Nature independently chooses one abstract perfect matching in every
   component's \(P\)-terminal set;
3. the strategy sees that tuple before choosing \(S(M)\);
4. every selected path uses the same \(P\); and
5. component maps and the relative translation are existential choices
   after the switch.

The audit never combines matchings belonging to different colour pairs.
It also reconstructs all matching-independent endpoint actions.  The only
endpoint sets common to every perfect matching of one terminal set are the
empty set and the full terminal set.  All 240 stored nonempty,
circuit-closed combinations replay, and none cleans or deletes.  The six
positive results therefore genuinely use
\(\forall M\,\exists S(M)\), not an unobserved fixed action.

## 3. Exhaustive matching counts and stored witnesses

Each entry below is `rescued/all`:

| partition | pair `12` | pair `13` | pair `23` | robust pair |
|---|---:|---:|---:|---|
| `0001234000314200` | `14/15` | `14/15` | `2/3` | none |
| `0001234003144422` | `2/3` | **`9/9`** | `0/1` | `13` |
| `0012344041300022` | `2/3` | **`15/15`** | `0/1` | `13` |
| `0012344044130244` | `2/3` | **`9/9`** | `2/3` | `13` |
| `0012344400314200` | `2/3` | **`9/9`** | `2/3` | `13` |
| `0012344403144422` | `2/3` | **`15/15`** | `0/1` | `13` |
| `0123444441300022` | `2/3` | **`9/9`** | `0/1` | `13` |
| `0123444444130244` | `14/15` | `14/15` | `2/3` | none |

The six bold universal columns contain 66 matching rows.  Across all
partitions and all three pairs, the frozen candidate certificate contains
160 rows: 142 rescue witnesses and 18 adverse rows.  The audit replays every
row, checks every selected path against its matching, recomputes the changed
derivative, and validates every stored map tuple, integrated base word,
cleaning translation, or deleting missing colour.

As a separate exhaustive check, the audit enumerates all legal subsets of
all matchings, not just the candidate's successful search prefixes.  The
full numbers of distinct reachable changed derivatives are:

| profile type | pair `12` | pair `13` | pair `23` |
|---|---:|---:|---:|
| either `8+2+2+2+2` state | 127 | 255 | 7 |
| every other state | 63 | 255 | 3 or 7, as the matching count is 1 or 3 |

This is the basis for the certificate-field clarification in the verdict.
The independently ordered stream of first positive witnesses has SHA-256

```text
c0389f2fbe2d070db6244bf6326b4038a5f4d0ddbfcf2d4e5184e32608d55d6c
```

## 4. The two adverse triples

For `0001234000314200`, the independently recovered adverse systems are:

```text
12  0:(1-7,2-15,8-9); 1:(3-11); 2:(4-13); 3:(5-10)
13  0:(0-1,2-7,9-14); 1:(3-11); 2:(4-13); 3:(5-10); 4:(6-12)
23  0:(0-8,14-15); 4:(6-12)
```

For `0123444444130244`, they are:

```text
12  1:(1-10); 2:(2-13); 3:(3-11); 4:(4-15,5-7,8-9)
13  0:(0-12); 1:(1-10); 2:(2-13); 3:(3-11); 4:(4-7,5-6,9-14)
23  0:(0-12); 4:(6-8,14-15)
```

For each partition the three rows contain 6, 7, and 3 paths.  Circuit
closure leaves respectively 31, 63, and 3 nonempty legal subsets, for 97
subsets per adverse triple.  Every changed state independently classifies
as

```text
feasible=320  clean=0  delete=0
```

## 5. Literal graph realizations

The checker reconstructs each graph directly from the published pole
description: four \(K_4-e\) two-poles, one ten-vertex eight-terminal pole,
and the two support 8-circuits.  It does not call the candidate realization
program.

| partition | vertices | edges | simple | cubic | connected | bridgeless | displayed flow |
|---|---:|---:|---|---|---|---|---|
| `0001234000314200` | 42 | 63 | yes | yes | yes | yes | valid |
| `0123444444130244` | 42 | 63 | yes | yes | yes | yes | valid |

Simplicity is checked from all unordered edge pairs, cubicity from every
vertex degree, connectedness by traversal, and bridgelessness by deleting
each of the 63 edges in turn.  The displayed nowhere-zero
\(\mathbb F_2^3\) flow is checked at every vertex.

The audit then extracts each pole's literal bichromatic components and gets
exactly the two path triples above.  It rechecks all 97 legal subsets in
each graph.  Finally, an independent backtracking search finds and verifies
a proper Tait colouring of all 63 edges of each graph.  The exact labelled
graph6 strings, Tait strings, and path systems are frozen in
`audit-output.json`.

A Tait colouring supplies a nowhere-zero \(\mathbb F_2^2\) flow and hence
an extendable projection of size zero.  Therefore the displayed support-16
projection in either graph is not globally minimum.

## 6. Scope, integrity, and disclosure

The result is limited to:

- the eight published residual partitions for one fixed `8+8` word orbit;
- one bichromatic colour pair per play;
- one matching-observed Kempe round; and
- the direct clean-or-delete test after that round.

It does not cover the other support-16 word or shape orbits, multiple Kempe
rounds, support-changing exchanges outside this game, globally minimum
projections, or FiveCDC.

The candidate `SHA256SUMS` ledger matches all six candidate/source entries,
and the final candidate directory has no unledgered files.  The human proof
contains the correct scope disclaimers and discloses OpenAI Codex
assistance, Atharva Vaidya's direction, and the lack of independent human
peer review.  `SOURCE-SHA256SUMS` freezes the audited inputs; `SHA256SUMS`
freezes this audit.

An unledgered Python bytecode cache created during replay was removed from
the candidate directory.  No preprint or Git state was changed.

## Replay

From this audit directory:

```sh
python3 -B audit.py
```

The checker uses only the Python standard library and completes in about
12 seconds on the audit machine.  Its stdout must equal
`audit-output.json`.
