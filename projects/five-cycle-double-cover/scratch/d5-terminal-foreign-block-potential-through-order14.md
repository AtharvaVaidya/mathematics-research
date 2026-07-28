# The terminal foreign-block potential \(b^*\)

Date: **2026-07-28**

Status: **EXHAUSTIVE THROUGH ORDER 14 / PROOF TARGET / NOT A
FIVECDC RESOLUTION**.

## 1. Definition

Fix two distinct root edges \(r,s\), a normalized five-coordinate
flow \(q\), and the exact factor-component-chain distance
\(d_q(r,s)>1\).

For every shortest ordered first pair \(C,D\), let \(P\) and \(Q\) be
their coordinate pairs, so \(r\in C\), \(C\cap D\ne\varnothing\), and
\(D\) is the first \(Q\)-component on the selected shortest chain
toward \(s\).  Let \(H\) be the \(Q\)-component containing \(r\).
This pair is eligible only when
\[
             |P\cap Q|=1,\qquad H\text{ exists},\qquad H\ne D. \tag{1}
\]
In the implementation a coordinate pair \(\{i,j\}\) is encoded by
the five-bit mask \((1\ll i)\mathbin{\vert}(1\ll j)\), and the first
condition in (1) is checked by requiring the population count of the
bitwise intersection of the \(P\)-mask and \(Q\)-mask to equal one.

Traverse the circuit \(C\), in either orientation from \(r\), stopping
at the first edge of \(D\).  Before that edge, count the maximal
blocks of edges belonging to \(Q\)-components other than \(H\) and
\(D\).  A later reentry into the same foreign component after a gap is
a new block.  Directly passing from one foreign component to a
different one also begins a new block.

Let
\[
 b^*_q(r,s)
\]
be the minimum count over both orientations and all eligible shortest
ordered first pairs.  If there is no eligible shared-coordinate pair,
set
\[
                         b^*_q(r,s)=0.                         \tag{2}
\]
This convention means only that the particular shared-coordinate
obstruction being counted is absent.  It does **not** mean that the
rooted distance is one or that descent has already succeeded.  Thus a
fixed-\((d,0)\) subplateau with \(d>1\) is subjected to exactly the same
descent test as every other value of \(b^*\).

The ordered diagnostic fixes the smaller-index edge as \(r\).  The
endpoint-symmetric potential is
\[
 \bar b^*_q(\{r,s\})=\min\{b^*_q(r,s),b^*_q(s,r)\}.
\]
The proposed secondary potential is the lexicographic pair
\[
                       (d_q(r,s),b^*_q(r,s))
\]
or, for the invariant version,
\[
                       (d_q(r,s),\bar b^*_q(\{r,s\})).
\]

## 2. Exact finite property audited

A terminal plateau is an entire connected component of the
equal-surface-\(\chi\) switch graph with no switch to a state of larger
\(\chi\).  For every terminal plateau, root pair, and value
\((d,b^*)\) with \(d>1\), the checker forms the complete connected
components using only neutral switches that preserve both \(d\) and
\(b^*\).

For each such fixed-\((d,b^*)\) component, it checks that some incident
neutral switch inside the terminal plateau either

1. strictly lowers \(d\); or
2. preserves \(d\) and strictly lowers \(b^*\).

In particular, alternative 2 is impossible at \(b^*=0\), so a
fixed-\((d,0)\) component passes only if its neutral boundary contains a
state of smaller \(d\).

This is stronger than testing one representative state: neutral
wandering within the entire fixed-potential subplateau is allowed
before strict descent.

## 3. Complete simple cubic order-12 census

The input is the complete `geng -C -d3 -D3 12` census of connected
bridgeless simple cubic graphs.  The flow enumeration is quotiented by
the global \(S_5\) action.

### Ordered lower-index root

\[
\begin{array}{c|r}
\text{graphs}&81\\
\text{normalized flows}&25\,960\\
\text{terminal equal-}\chi\text{ plateaus}&2\,659\\
\text{fixed-}(d,b^*)\text{ subplateaus}&33\,748\\
\text{failures}&0.
\end{array}
\]

### Symmetric endpoint reversal

\[
\begin{array}{c|r}
\text{graphs}&81\\
\text{normalized flows}&25\,960\\
\text{terminal equal-}\chi\text{ plateaus}&2\,659\\
\text{fixed-}(d,\bar b^*)\text{ subplateaus}&33\,674\\
\text{failures}&0.
\end{array}
\]

Thus both variants pass this complete finite census.

## 4. Complete simple cubic order-14 census

The same audit was run on the complete 480-graph
`geng -C -d3 -D3 14` census.

### Ordered lower-index root

\[
\begin{array}{c|r}
\text{graphs}&480\\
\text{normalized flows}&537\,418\\
\text{terminal equal-}\chi\text{ plateaus}&33\,598\\
\text{fixed-}(d,b^*)\text{ subplateaus}&646\,399\\
\text{failures}&0.
\end{array}
\]

### Symmetric endpoint reversal

\[
\begin{array}{c|r}
\text{graphs}&480\\
\text{normalized flows}&537\,418\\
\text{terminal equal-}\chi\text{ plateaus}&33\,598\\
\text{fixed-}(d,\bar b^*)\text{ subplateaus}&643\,528\\
\text{failures}&0.
\end{array}
\]

These are exhaustive finite results through order 14.  They are not a
proof for arbitrary graphs.

## 5. Reproduction

```text
clang++ -std=c++17 -O3 -DNDEBUG \
  scratch/audit_d5_terminal_foreign_block_potential.cpp \
  -o /tmp/audit_d5_terminal_foreign_block_potential

/opt/homebrew/bin/geng -Cq -d3 -D3 12 2>/dev/null |
  /tmp/audit_d5_terminal_foreign_block_potential

/opt/homebrew/bin/geng -Cq -d3 -D3 12 2>/dev/null |
  /tmp/audit_d5_terminal_foreign_block_potential --endpoint-reversal

/opt/homebrew/bin/geng -Cq -d3 -D3 14 2>/dev/null |
  /tmp/audit_d5_terminal_foreign_block_potential \
  > output/d5-terminal-foreign-block-potential/order14-ordered.jsonl

/opt/homebrew/bin/geng -Cq -d3 -D3 14 2>/dev/null |
  /tmp/audit_d5_terminal_foreign_block_potential --endpoint-reversal \
  > output/d5-terminal-foreign-block-potential/order14-symmetric.jsonl
```

The expected final lines are

```text
{"status":"SUMMARY","graphs":81,"flows_mod_s5":25960,"terminal_plateaus":2659,"metric_subplateaus":33748,"failures":0,"endpoint_reversal":0}
{"status":"SUMMARY","graphs":81,"flows_mod_s5":25960,"terminal_plateaus":2659,"metric_subplateaus":33674,"failures":0,"endpoint_reversal":1}
{"status":"SUMMARY","graphs":480,"flows_mod_s5":537418,"terminal_plateaus":33598,"metric_subplateaus":646399,"failures":0,"endpoint_reversal":0}
{"status":"SUMMARY","graphs":480,"flows_mod_s5":537418,"terminal_plateaus":33598,"metric_subplateaus":643528,"failures":0,"endpoint_reversal":1}
```

The SHA-256 hashes of the complete order-14 JSONL transcripts are

```text
e928f7a91a2f4235455a93756ae3f6343e20ce051058760a5ba6a9a3ac5d73f5  order14-ordered.jsonl
4db705e221a7fe08bb71bbbeaa824c7037cff021a62a6a2c7782a3bac5a903a1  order14-symmetric.jsonl
```

The focused standard-library verifier independently checks both
transcript hashes, parses every JSON record, checks consecutive graph
indices and graph6 uniqueness, accumulates all four numerical totals
from the 480 graph records, compares them with the summary record, and
requires every failure flag to be zero:

```text
python3 scratch/verify_d5_terminal_foreign_block_order14.py
shasum -a 256 -c \
  output/d5-terminal-foreign-block-potential/SHA256SUMS
```

It deliberately does not import the C++ enumerator and does not claim
to reperform the mathematical search; its role is independent
transcript-integrity and summary-arithmetic verification.

## 6. What remains to prove

The first-foreign splice lemma proves immediate nonincrease of \(d\)
when one orientation has no foreign \(Q\)-component before \(D\), the
case with no intervening foreign block.  Because convention (2) also
assigns zero to the absence of an eligible shared-coordinate pair,
\(b^*=0\) alone is not the hypothesis of that lemma.

A universal argument would still need to show, on every
terminal plateau and for every \(d>1\), that neutral switches can
either lower \(d\), lower \(b^*\), or move within the same
fixed-\((d,b^*)\) component until such a switch is available.  At
\(b^*=0\), it must specifically force smaller \(d\).

The censuses above identify that statement as a surviving proof
target; it does not prove it for arbitrary graphs.  In particular, it
does not establish the Five-Cycle Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the
foreign-block statistic, implemented the exhaustive checker, ran the
order-12 and order-14 censuses, and drafted this note.  The computation
is not peer review, and the mathematical interpretation should be
independently checked before citation.
