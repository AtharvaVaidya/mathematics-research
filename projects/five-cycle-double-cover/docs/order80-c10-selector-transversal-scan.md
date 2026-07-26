# Exact selector scan on the all-\(C_{10}\) colourings of CVT[80,30]

Date: **2026-07-26**.

Status: **exact scoped finite positive result / no five-CDC conclusion**.

This note completes the bichromatic-selector test requested for the sole
girth-ten graph in the order-80 cubic vertex-transitive census.  Every
eligible factor-transversal mark set has a good selector.  The computation
does not range over arbitrary order-80 cubic graphs.

## 1. Input and candidate definition

The graph is census object CVT[80,30], line 425 of the
Potočnik--Spiga--Verret conversion cited in
`order80-vertex-transitive-control.md`.  It is connected, simple, cubic,
has 80 vertices and 120 edges, and has girth ten.

An exact normalized Tait-colouring enumeration has
\[
                   426\,256
\]
colourings modulo global \(S_3\) colour permutation.  Exactly 20 have all
three bichromatic factors equal to a disjoint union of eight 10-cycles.

Fix one of those 20 colourings and choose a common mark colour \(c\).
Let
\[
 H[a,c]=A_0\sqcup\cdots\sqcup A_7,\qquad
 H[b,c]=B_0\sqcup\cdots\sqcup B_7.
\]
The \(c\)-edges define a 5-regular bipartite incidence multigraph
\(\Gamma\) on the two sets of factor circuits.  An eligible mark set is an
eight-edge perfect matching of \(\Gamma\): equivalently, eight
\(c\)-edges containing exactly one edge from every \(A_i\) and every
\(B_j\).  These are precisely the \(c\)-coloured matchings that are perfect
transversals of both relevant factors.

For every eligible mark set, choose one endpoint factor of each marked
incidence edge.  The \(2^8=256\) choices give the all-mark bichromatic
selectors.  A selector is good when every circuit component of the
resulting symmetric difference contains an even number of marks.

## 2. Exact totals

There are \(20\cdot3=60\) colouring/common-colour cases.  In every case,
the permanent of the edge-object incidence matrix is
\[
                         1249.                        \tag{1}
\]
Thus the complete scan contains
\[
\begin{aligned}
 60\cdot1249 &= 74\,940
       &&\text{colouring/common-colour/mark-set records},\\
 74\,940\cdot256 &= 19\,184\,640
       &&\text{selector evaluations}.
\end{aligned}
\]
The 74,940 records use 74,415 distinct eight-edge subsets of the underlying
120-edge graph; repetition occurs when the same edge set is exposed by
more than one colouring/common-colour case.

Every one of the 74,940 records has a good selector.  More strongly, the
number of good selectors for an individual record lies between 94 and
138.  The exact distribution is:

| Good selectors | Records | Good selectors | Records |
|---:|---:|---:|---:|
| 94 | 60 | 99 | 1,920 |
| 102 | 3,840 | 103 | 2,880 |
| 104 | 3,120 | 105 | 2,400 |
| 106 | 4,800 | 107 | 3,840 |
| 108 | 12,480 | 109 | 3,360 |
| 110 | 6,120 | 111 | 5,760 |
| 112 | 4,800 | 113 | 2,880 |
| 114 | 5,280 | 115 | 1,440 |
| 116 | 5,040 | 117 | 2,400 |
| 118 | 120 | 119 | 960 |
| 120 | 480 | 121 | 480 |
| 122 | 240 | 134 | 120 |
| 138 | 120 |  |  |

In total there are
\[
                         8\,208\,840                  \tag{2}
\]
good selector records.  Their component profiles are:

| All-even marked profile | Selectors |
|---|---:|
| \(2+2+2+2\) | 20,640 |
| \(2+2+4\) | 562,080 |
| \(2+6\) | 1,891,680 |
| \(4+4\) | 1,496,640 |
| \(8\) | 4,237,800 |

These five counts sum to (2).  For completeness, the bad-selector
profiles are:

| Profile | Selectors | Profile | Selectors |
|---|---:|---|---:|
| \(1+1+1+1+1+1+1+1\) | 149,880 | \(1+1+1+2+3\) | 4,800 |
| \(1+1+1+5\) | 1,215,360 | \(1+1+2+2+2\) | 18,240 |
| \(1+1+2+4\) | 245,760 | \(1+1+3+3\) | 210,720 |
| \(1+1+6\) | 330,240 | \(1+2+2+3\) | 459,840 |
| \(1+2+5\) | 1,209,600 | \(1+3+4\) | 1,767,360 |
| \(1+7\) | 2,273,280 | \(2+3+3\) | 678,240 |
| \(3+5\) | 2,412,480 |  |  |

The good and bad profile counts together sum to 19,184,640.

## 3. Exact method

The main C++ checker uses the same normalization as the earlier full Tait
search: the three edge objects incident with vertex zero are assigned
colours \(0,1,2\) in their stored order.  It recursively enumerates every
proper colouring, retains exactly the all-\(C_{10}\) rows, and for every
choice of common colour:

1. computes the two eight-circuit factors;
2. recursively enumerates the edge-object perfect matchings of their
   incidence multigraph;
3. forms all 256 literal symmetric differences of selected factor
   circuits; and
4. traverses every resulting circuit and records its number of marks.

Parallel edges of the incidence multigraph remain distinct edge objects
throughout.  Mark sets are deduplicated only for the separately reported
74,415-subset statistic, never in the main 74,940-record scan.

The saved result includes the 20 complete 120-symbol colouring words, all
60 per-case summaries, the good-count histogram, and the complete
marked-component profile histogram.

## 4. Independent audit

The Python audit does not import the C++ implementation.  It decodes the
graph with NetworkX, reconstructs graph6 edge order, and verifies directly
that all 20 saved words:

- are proper normalized Tait colourings;
- are pairwise distinct; and
- have eight 10-cycles in every bichromatic factor.

It then checks that all 60 common-colour cases are colour-preservingly
isomorphic to one reference case, allowing exchange of the two noncommon
colours.  Consequently all selector statistics are identical in the 60
cases.  On the reference it independently enumerates all 1,249 perfect
transversals and all
\[
                       1249\cdot256=319\,744
\]
selectors using Python integer edge masks.  Its profile and good-count
histograms, multiplied by the 60 verified isomorphic cases, agree exactly
with the C++ result.  It additionally enumerates the transversals in all
60 labelled cases and independently obtains 74,940 records and 74,415
distinct edge sets.

Completeness of the outer Tait enumeration is also independently covered
by `tait_all_coloring_mark_separation.cpp`, whose earlier run obtained the
same 426,256 normalized colourings and the same 20 all-\(C_{10}\)
colourings using a separate recording path.

## 5. Scope

There is no no-good mark set in this scan.  Therefore the conditional
follow-up tests for unrestricted two-\(T\)-join packing and universal
separation are not triggered.

This closes the bichromatic-selector question only for CVT[80,30] and only
for the factor-transversal candidates arising from its 20 all-\(C_{10}\)
colourings.  The previous universal-separation census already shows that
CVT[80,30] has no universally separated matching of size eight, so the
graph was not a surviving equality core in any case.  Vertex-transitivity
is not a minimum-counterexample reduction.

The result should be contrasted with the abstract decorated incidence
countermodel in `equality88-incidence-rotation-countermodel.md`, which has
no good selector but fails girth and universal separation.  The present
girth-ten vertex-transitive control lies decisively on the positive side:
every eligible mark-set record has at least 94 good selectors.

## 6. Reproduction

Convert census line 425 to graph6 as in
`order80-vertex-transitive-control.md`, save it as `/tmp/cvt80_30.g6`, and
run:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  scratch/order80_c10_selector_scan.cpp \
  -o /tmp/order80_c10_selector_scan

/tmp/order80_c10_selector_scan < /tmp/cvt80_30.g6 \
  > scratch/order80-c10-selector-scan-result.json

python3 -B scratch/audit_order80_c10_selector_scan.py
```

The main scan takes about 70 seconds on the development machine.  The
independent audit takes about 9 seconds.

Artifact SHA-256 values:

```text
9790e70f1261477929bed1bdd76ed20677557b1f565d828934fcee01ad000218  order80_c10_selector_scan.cpp
10949815176f8044c588063b9ddf67bc3520d86b72c00308d7a17df70d45cfd2  order80-c10-selector-scan-result.json
5ce837518a17dcfbfa6b682522b1c6c29dbf026d01b7a8f1f2c2068ab074a08d  audit_order80_c10_selector_scan.py
0858fb26125a8a9698aa43475680ecf28a61fce1aeb8ccd86d37f8c779c7e611  order80-c10-selector-audit-result.json
```

## AI-use disclosure

OpenAI Codex agents, under human direction, designed and ran the finite
search, wrote the independent audit, and drafted this note.  Every reported
selector is checked by exact finite enumeration, but this is not human peer
review.  No claim of resolving the five-cycle double cover conjecture is
made.
