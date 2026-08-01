# Order-24 cyclically-four separated-triple witness

Status: **INDEPENDENTLY REPLAYED FINITE WITNESS / NOT A FIVE-CYCLE
DOUBLE COVER RESOLUTION**.

## Result

The graph

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

is a simple connected cubic graph on 24 vertices.  The three edges

```text
0-1, 2-3, 20-23
```

form a matching that is universally separated: in every proper
three-edge-colouring, no bichromatic circuit contains two of the three
marked edges.

The graph has exactly 36 Tait colourings modulo global permutation of
the three colours.  It has no cyclic edge cut of size at most three and
does have a cyclic edge cut of size four.  Its cyclic edge connectivity
is therefore exactly four.  It is nonplanar, has ordinary edge
connectivity three, vertex connectivity three, and girth four.

This is the first retained witness beyond the complete negative
order-22 frontier.  It refutes the provisional low-cut exposure
conjecture that every universally separated triple in a Tait-colourable
cubic graph must be exposed by a cyclic cut of size at most three.  It
does **not** prove or refute the five-cycle double cover conjecture.

The witness does **not** satisfy the stronger marked-girth condition
needed by the surviving connected-core branch.  Subdividing each marked
edge gives girth five, whereas that branch requires
\[
 |C|+|C\cap S|\ge10
\]
for every core circuit \(C\), equivalently marked-subdivision girth at
least ten.

## Construction

The witness is row 21,360 of a systematic marked four-sum screen.  Its
left factor is the order-20 graph

```text
S??????oD?B?HCOaM??q?B_?E_CB??BG?
```

with universally separated marks `3-15` and `8-19`.  Delete the host
edges `5-16` and `6-17`.  In a copy of \(K_4\), delete `0-1` and `2-3`.
Join the ordered host boundary `(5,16,6,17)` to the factor boundary
`(0,2,3,1)`, then relabel so the inherited host marks become `0-1` and
`2-3`.  The third universally separated edge found by the checker is
`20-23`.

The exact data are frozen in `construction.json`.

## Exact search scope

The complete order-20 connected simple cubic corpus was screened over
all proper three-edge-colourings.  Among 496,430 Tait-colourable rows,
250 cyclically four-edge-connected graphs have a universally separated
pair.  They contain:

- 934 literal separated pairs;
- 789 marked-host orbits under graph automorphisms;
- 257,214 eligible literal unmarked host port pairs;
- 233,670 marked-stabilizer port orbits.

For every port orbit, the generator combines the host with each of the
three \(K_4\) boundary-bijection orbits.  This gives 701,010 order-24
rows.  Only the inherited pair was fixed; the checker searched every
edge as a possible third mark.

The exact screen found 144 hits, representing 142 distinct emitted
graph6 rows, 20 unmarked graph isomorphism classes, and 46 marked-graph
isomorphism classes.  Marked isomorphism was computed by subdividing
all three marks and canonically labelling the resulting graphs; the 46
canonical subdivision rows are retained in
`marked-isomorphism-classes-subdivision.g6`.

The 144-versus-142 discrepancy is fully accounted for: the
factorwise-automorphism quotient is not a global deduplication of the
finished graph.  Rows 568,556 and 569,533 produce the same literal graph
and marked triple, as do rows 571,489 and 572,468.  Every other emitted
hit is literal-row distinct.

All 144 hits have ordinary girth four and marked-subdivision girth five.
Thus exactly zero of the 144 satisfy
\(|C|+|C\cap S|\ge10\) for every circuit.  This is forced visibly by the
four-cycle left in the \(K_4\) factor: it contains one selected mark, so
its marked length is five.

The complete 701,010-row stream was also rerun directly with
`--min-subdivided-girth 10`.  It found zero witnesses.  This confirms the
stronger statement that no alternative choice of the third mark repairs
the marked-girth failure in any displayed \(K_4\) sum.

The complete hit stream is `search-witnesses.jsonl`.  This is a
systematic theorem about the displayed construction scope, not about
all order-24 cubic graphs.

## Independent verification

Run:

```sh
python3 \
  search/cyclic4-universally-separated-triple-n24-20260726/independent_verifier.py
```

The clean-room checker uses only the Python standard library and imports
neither search implementation nor generator.  It:

1. decodes the literal graph6 record;
2. checks simplicity, connectedness, cubicity, and the marked matching;
3. tests all 36 one-edge, 630 two-edge, and 7,140 three-edge deletion
   sets for a cyclic cut;
4. finds an explicit cyclic four-edge cut;
5. independently enumerates all 36 normalized Tait colourings; and
6. checks every bichromatic component in every colouring.

Expected status: `VERIFIED`.

To replay all 144 retained hits with the same clean-room implementation:

```sh
python3 \
  search/cyclic4-universally-separated-triple-n24-20260726/batch_verifier.py
```

The frozen batch report independently confirms that all 144 records have
36 normalized Tait colourings, no cyclic cut below four, and universal
separation; it also confirms 142 distinct literal graph6 rows, girth four
for every hit, marked-subdivision girth five for every hit, and zero hits
passing the marked-girth-at-least-ten condition.

The one-command package replay also checks every SHA-256 manifest entry
and, when nauty is installed, the canonical graph6 record:

```sh
python3 \
  search/cyclic4-universally-separated-triple-n24-20260726/verify_package.py
```

## Scope and AI-use disclosure

OpenAI Codex agents designed and ran this search, extended the original
checker, implemented the automorphism quotient, found the witness, wrote
the clean-room verifier, and drafted this record under human direction.
The two programs are independently structured but both AI-written; this
is not independent human peer review.  A human graph theorist should
recheck the literal graph, enumeration argument, and implications before
citing the result.
